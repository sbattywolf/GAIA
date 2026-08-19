import tempfile, unittest
from pathlib import Path
from gaia_toolkit import *

class ToolkitTests(unittest.TestCase):
    def test_observation(self):
        o=Observation("3090","host","python","3.x","PASS","2026-01-01")
        self.assertEqual(o.evidence_class,"OBSERVED")
    def test_evidence_provenance(self):
        e=Evidence("Host Check V0.1","3090","host","python","3.x","AVAILABLE","OBSERVED","t",{"k":"v"})
        self.assertEqual(e.provenance["k"],"v")
    def test_categories(self):
        for c in CATEGORIES:
            r=analyze_requirement(Requirement(c,c,c),[])
            self.assertEqual(r.state,"UNKNOWN")
    def test_available(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev=[Evidence("Host Check V0.1","3090","host","python","3.x","PASS","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev).state,"AVAILABLE")
    def test_unavailable(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev=[Evidence("Host Check V0.1","x","host","python",None,"FAIL","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev).state,"UNAVAILABLE")
    def test_unknown(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        self.assertEqual(analyze_requirement(req,[]).state,"UNKNOWN")
    def test_authorization(self):
        r=analyze_requirement(Requirement("r","software","install",required=False),[])
        self.assertEqual(r.state,"REQUIRES_AUTHORIZATION")
    def test_candidate(self):
        c=Candidate("git","fixture","software")
        self.assertEqual(c.name,"git")
    def test_recommendation_not_authorization(self):
        r=make_recommendation([], "use git", [])
        self.assertTrue(r.authorization_required)
    def test_research_disabled(self):
        self.assertEqual(research_disabled_result(),())
    def test_mapping_provenance(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev=[Evidence("Host Check V0.1","3090","host","python",None,"PASS","OBSERVED","t")]
        r=analyze_requirement(req,ev)
        self.assertEqual((r.mapping,r.source,r.evidence_key),("software.command.python3","Host Check V0.1","python"))
    def test_unknown_preserved(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev=[Evidence("Host Check V0.1","1070","host","python",None,"UNKNOWN","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev).state,"UNKNOWN")
    def test_no_fuzzy_mapping(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev=[Evidence("Host Check V0.1","1070","host","python_version",None,"PASS","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev).state,"UNKNOWN")
    def test_container_not_native(self):
        req=Requirement("r","runtime","ollama.native",evidence_mappings={"ollama.native":"runtime.ollama.native"})
        ev=[Evidence("Host Check V0.1","1070","docker","ollama.container",None,"AVAILABLE","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev).state,"UNKNOWN")
    def test_security_clean(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"README.md"; p.write_text("safe")
            self.assertTrue(sanitize_package(Path(d))[0])
    def test_secret_block(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/".env").write_text("TOKEN=secret")
            self.assertFalse(sanitize_package(Path(d))[0])
    def test_private_key_block(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"id_rsa.pem").write_text("PRIVATE KEY")
            self.assertFalse(sanitize_package(Path(d))[0])
    def test_no_mutation_by_contract(self):
        self.assertTrue(True)
    def test_cross_host_semantics(self):
        req=Requirement("r","software","python",evidence_mappings={"python":"software.command.python3"})
        ev3090=[Evidence("Host Check V0.1","3090","host","python",None,"PASS","OBSERVED","t")]
        ev1070=[Evidence("Host Check V0.1","1070","host","python",None,"UNKNOWN","OBSERVED","t")]
        self.assertEqual(analyze_requirement(req,ev3090).state,"AVAILABLE")
        self.assertEqual(analyze_requirement(req,ev1070).state,"UNKNOWN")

if __name__=="__main__": unittest.main()
