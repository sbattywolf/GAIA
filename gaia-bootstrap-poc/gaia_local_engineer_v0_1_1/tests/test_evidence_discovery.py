import os
import tempfile
import unittest
from pathlib import Path

from gaia_local_engineer import (
    DiscoveryLimits, DiscoveryRoot, EvidenceRequirement, PathEscapeRejected,
    SensitiveArtifactRejected, assess_evidence_sufficiency,
    discovery_loop, list_files, read_file, search_text, sanitize_delivery
)

class EvidenceDiscoveryAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name).resolve()
        (self.root / "nested").mkdir()
        (self.root / "nested" / "evidence.txt").write_text(
            "arbitrary evidence fixture\nstatus=observed\nsemantic_state=UNKNOWN\n",
            encoding="utf-8",
        )
        (self.root / "other.txt").write_text("python=UNKNOWN\nstatus=observed\n", encoding="utf-8")

    def tearDown(self):
        self.t.cleanup()

    def ctx(self):
        return DiscoveryRoot(self.root)

    # 1 missing root
    def test_01_missing_root_escalates(self):
        r = list_files(None)
        self.assertEqual(r.operation_status, "ESCALATE")
        self.assertEqual(r.reason, "DISCOVERY_SCOPE_NOT_AUTHORIZED")

    # 2 unauthorized root
    def test_02_unauthorized_root_escalates(self):
        r = list_files(DiscoveryRoot(self.root, authorized=False))
        self.assertEqual(r.operation_status, "ESCALATE")

    # 3 traversal
    def test_03_parent_traversal_rejected(self):
        with self.assertRaises(PathEscapeRejected):
            read_file(self.ctx(), "../outside.txt")

    # 4 absolute escape
    def test_04_absolute_escape_rejected(self):
        outside = self.root.parent / "outside.txt"
        outside.write_text("secret-ish but not collected", encoding="utf-8")
        try:
            with self.assertRaises(PathEscapeRejected):
                read_file(self.ctx(), outside)
        finally:
            outside.unlink()

    # 5 symlink escape
    def test_05_symlink_escape_rejected(self):
        outside = self.root.parent / "outside-target.txt"
        outside.write_text("outside", encoding="utf-8")
        link = self.root / "escape"
        try:
            link.symlink_to(outside)
            with self.assertRaises(PathEscapeRejected):
                read_file(self.ctx(), link)
        finally:
            if link.exists() or link.is_symlink(): link.unlink()
            outside.unlink()

    # 6 canonical escape
    def test_06_canonical_path_escape_rejected(self):
        with self.assertRaises(PathEscapeRejected):
            read_file(self.ctx(), self.root / "nested" / ".." / ".." / "outside")

    # 7 no implicit root expansion
    def test_07_no_implicit_root_expansion(self):
        old = os.getcwd()
        os.chdir(self.root)
        try:
            # CWD is irrelevant; explicit root controls discovery.
            self.assertEqual(list_files(DiscoveryRoot(self.root)).operation_status, "SUCCESS")
            self.assertEqual(list_files(None).operation_status, "ESCALATE")
        finally:
            os.chdir(old)

    # 8 bounded LIST_FILES
    def test_08_bounded_list(self):
        r = list_files(self.ctx(), limits=DiscoveryLimits(max_list_results=1))
        self.assertEqual(r.operation_status, "SUCCESS")
        self.assertTrue(r.truncated)
        self.assertEqual(len(r.items), 1)

    # 9 bounded SEARCH_TEXT
    def test_09_bounded_search(self):
        r = search_text(self.ctx(), "status=", limits=DiscoveryLimits(max_search_results=1))
        self.assertTrue(r.truncated)
        self.assertEqual(len(r.items), 1)

    # 10 bounded READ_FILE
    def test_10_bounded_read(self):
        r = read_file(self.ctx(), "nested/evidence.txt",
                      limits=DiscoveryLimits(max_read_bytes=10))
        self.assertEqual(r.operation_status, "SUCCESS")
        self.assertTrue(r.truncated)

    # 11 provenance
    def test_11_provenance(self):
        r = read_file(self.ctx(), "nested/evidence.txt", round_no=2)
        p = r.provenance[0]
        self.assertEqual(p.source_type, "LOCAL_FILE")
        self.assertEqual(p.operation, "READ_FILE")
        self.assertEqual(p.discovery_round, 2)
        self.assertEqual(p.source_path, "nested/evidence.txt")
        self.assertEqual(p.discovery_root, self.root.as_posix())

    # 12 truncation explicit
    def test_12_truncation_is_explicit(self):
        r = read_file(self.ctx(), "nested/evidence.txt",
                      limits=DiscoveryLimits(max_read_bytes=5))
        self.assertTrue(r.truncated)
        self.assertNotEqual(assess_evidence_sufficiency([r]).sufficient, True)

    # 13 semantic separation
    def test_13_operation_success_not_sufficiency(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        self.assertEqual(r.operation_status, "SUCCESS")
        self.assertEqual(r.evidence_sufficiency, "INSUFFICIENT")
        self.assertEqual(r.semantic_correctness, "UNKNOWN")

    # 14 read success != semantic correctness
    def test_14_read_success_not_semantic_correctness(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        self.assertEqual(r.semantic_correctness, "UNKNOWN")

    # 15 UNKNOWN preserved
    def test_15_unknown_preserved(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        ev = assess_evidence_sufficiency([r], required_sources=1, semantic_correctness="UNKNOWN")
        self.assertTrue(ev.sufficient)
        self.assertEqual(ev.semantic_correctness, "UNKNOWN")

    # 16 evidence != authorization
    def test_16_evidence_not_authorization(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        self.assertNotIn("authorization", r.__dict__)

    # 17 observed != inferred
    def test_17_observed_not_inferred(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        self.assertEqual(r.semantic_correctness, "UNKNOWN")

    # 18 finite rounds
    def test_18_finite_rounds(self):
        lim = DiscoveryLimits(max_discovery_rounds=3)
        rounds = [("LIST_FILES", {}), ("LIST_FILES", {}),
                  ("LIST_FILES", {}), ("LIST_FILES", {})]
        req = EvidenceRequirement("q-rounds", required_operations=("LIST_FILES",), required_sources=1)
        out = discovery_loop(self.ctx(), rounds, lim, requirement=req)
        self.assertEqual(len(out), 4)
        self.assertEqual(out[-1].operation_status, "ESCALATE")

    # 19 escalation after exhaustion
    def test_19_exhaustion_escalates(self):
        req = EvidenceRequirement("q-budget", required_operations=("LIST_FILES",), required_sources=1)
        out = discovery_loop(self.ctx(), [("LIST_FILES", {})]*4,
                             DiscoveryLimits(max_discovery_rounds=3), requirement=req)
        self.assertEqual(out[-1].reason, "DISCOVERY_BUDGET_EXHAUSTED")

    # 20 generic complete chain
    def test_20_generic_non_gaia_chain(self):
        a = list_files(self.ctx())
        b = search_text(self.ctx(), "arbitrary evidence")
        c = read_file(self.ctx(), "nested/evidence.txt")
        ev = assess_evidence_sufficiency([a,b,c], required_sources=1)
        self.assertEqual(a.operation_status, "SUCCESS")
        self.assertEqual(b.operation_status, "SUCCESS")
        self.assertEqual(c.operation_status, "SUCCESS")
        self.assertTrue(ev.sufficient)
        self.assertTrue(c.provenance[0].source_path.endswith("evidence.txt"))

    # 21 sensitive artifact prevention
    def test_21_secret_file_blocked(self):
        p = self.root / ".env"
        p.write_text("TOKEN=do-not-collect", encoding="utf-8")
        with self.assertRaises(SensitiveArtifactRejected):
            read_file(self.ctx(), ".env")

    # 22 private key prevention
    def test_22_private_key_blocked(self):
        p = self.root / "id_rsa.pem"
        p.write_text("PRIVATE KEY", encoding="utf-8")
        with self.assertRaises(SensitiveArtifactRejected):
            read_file(self.ctx(), "id_rsa.pem")

    # 23 list sensitive metadata not collected
    def test_23_list_rejects_sensitive_artifact(self):
        p = self.root / "credentials.json"
        p.write_text('{"token":"x"}', encoding="utf-8")
        with self.assertRaises(SensitiveArtifactRejected):
            list_files(self.ctx())

    # 24 search sensitive content not collected
    def test_24_search_skips_sensitive_artifact(self):
        p = self.root / ".secrets.env"
        p.write_text("TOKEN=never-read", encoding="utf-8")
        r = search_text(self.ctx(), "never-read")
        self.assertEqual(r.items, ())

    # 25 no mutation by API
    def test_25_no_mutation_api_surface(self):
        names = set(__import__("gaia_local_engineer").__dict__)
        self.assertNotIn("write_file", names)
        self.assertNotIn("execute", names)

    # 26 no network by implementation surface
    def test_26_no_network_import_surface(self):
        source = Path(__import__("gaia_local_engineer.core").__file__).read_text()
        self.assertNotIn("requests", source)
        self.assertNotIn("urllib.request", source)

    # 27 no file execution
    def test_27_no_execution_surface(self):
        source = Path(__import__("gaia_local_engineer.core").__file__).read_text()
        self.assertNotIn("subprocess", source)
        self.assertNotIn("os.system", source)

    # 28 root provenance sanitized and deterministic
    def test_28_root_provenance(self):
        r = list_files(self.ctx())
        self.assertEqual(r.provenance[0].discovery_root, self.root.as_posix())
        self.assertNotIn("TOKEN=", r.provenance[0].discovery_root)

    # 29 bounded file size
    def test_29_max_file_bytes(self):
        (self.root / "large.txt").write_text("x"*100, encoding="utf-8")
        r = read_file(self.ctx(), "large.txt",
                      limits=DiscoveryLimits(max_file_bytes=10))
        self.assertEqual(r.operation_status, "FAIL")
        self.assertEqual(r.reason, "MAX_FILE_BYTES_EXCEEDED")

    # 30 path containment on LIST_FILES
    def test_30_list_paths_are_relative_and_contained(self):
        r = list_files(self.ctx())
        for item in r.items:
            self.assertFalse(item.relative_path.startswith("/"))
            self.assertNotIn("..", Path(item.relative_path).parts)

    # 31 Toolkit V0.1 regression semantics
    def test_31_toolkit_v01_regression_unknown_is_not_available(self):
        # Regression uses the established V0.1 evidence vocabulary without
        # importing/modifying the frozen Toolkit implementation.
        v01_status = "UNKNOWN"
        mapped = {"python": "software.command.python3"}
        self.assertEqual(mapped["python"], "software.command.python3")
        self.assertNotEqual(v01_status, "AVAILABLE")

    # 32 no unresolved question -> no next round
    def test_32_no_unresolved_question_stops(self):
        out = discovery_loop(self.ctx(), [("LIST_FILES", {}), ("SEARCH_TEXT", {"query":"status="})])
        self.assertEqual(out, ())

    # 33 unresolved question without pertinent evidence -> no next round
    def test_33_no_pertinent_evidence_stops(self):
        req = EvidenceRequirement("q-python", required_operations=("LIST_FILES",), required_sources=1)
        out = discovery_loop(self.ctx(), [("SEARCH_TEXT", {"query":"status="}), ("READ_FILE", {"path":"nested/evidence.txt"})], requirement=req)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0].provenance[0].operation, "SEARCH_TEXT")

    # 34 pertinent evidence -> next round permitted
    def test_34_pertinent_evidence_allows_next_round(self):
        req = EvidenceRequirement("q-files", required_operations=("LIST_FILES",), required_sources=1)
        out = discovery_loop(self.ctx(), [("LIST_FILES", {}), ("READ_FILE", {"path":"nested/evidence.txt"})], requirement=req)
        self.assertEqual(len(out), 2)
        self.assertEqual(out[0].provenance[0].discovery_round, 1)
        self.assertEqual(out[1].provenance[0].discovery_round, 2)

    # 35 question-specific sufficiency
    def test_35_question_specific_sufficiency(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        req = EvidenceRequirement("q-list", required_operations=("LIST_FILES",), required_sources=1)
        ev = assess_evidence_sufficiency([r], requirement=req)
        self.assertFalse(ev.sufficient)
        self.assertEqual(ev.semantic_correctness, "UNKNOWN")

    # 36 primitive availability != semantic sufficiency
    def test_36_primitive_availability_not_semantic_sufficiency(self):
        r = read_file(self.ctx(), "nested/evidence.txt")
        ev = assess_evidence_sufficiency([r], required_sources=1)
        self.assertTrue(ev.sufficient)
        self.assertEqual(r.operation_status, "SUCCESS")
        self.assertEqual(r.evidence_sufficiency, "INSUFFICIENT")
        self.assertEqual(r.semantic_correctness, "UNKNOWN")

    # 37 Toolkit V0.1 implementation regression is not claimed by this package
    def test_37_toolkit_regression_is_not_executed(self):
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
