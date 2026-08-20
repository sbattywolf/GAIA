import unittest,tempfile
from pathlib import Path
from gaia_agent_host_check.core import *

class ToolkitTests(unittest.TestCase):
    def test_t01_generic_host(self): self.assertTrue(host_discovery())
    def test_t02_profile_composition(self): self.assertEqual({"generic","1070","3090"},{"generic","1070","3090"})
    def test_t03_runtime_distinction(self): self.assertEqual(runtime_source(True,False),"NATIVE"); self.assertEqual(runtime_source(False,True),"CONTAINER")
    def test_t04_compose_plugin(self): self.assertEqual(classify_compose(True,False),"DOCKER_COMPOSE_PLUGIN")
    def test_t05_legacy_compose(self): self.assertEqual(classify_compose(False,True),"DOCKER_COMPOSE_LEGACY_BINARY")
    def test_t06_ollama_native(self): self.assertEqual(runtime_source(True,False),"NATIVE")
    def test_t07_ollama_docker(self): self.assertEqual(runtime_source(False,True),"CONTAINER")
    def test_t08_models(self): self.assertEqual(model_inventory("NAME  ID\nqwen3:8b  abc")[0].value["name"],"qwen3:8b")
    def test_t09_skill(self): self.assertEqual(skill_precheck("coding_agent",{"python","git","test_runner"})[0].status,"PASS"); self.assertEqual(skill_precheck("coding_agent",{"python"})[0].status,"BLOCKED")
    def test_t10_scopes(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); (p/"x.py").write_text(""); self.assertEqual(script_scope(p,"GAIA")[0].value,["x.py"])
    def test_t11_secret_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/".env"; p.write_text("TOKEN=secret"); self.assertEqual(security_metadata([p])[0].value["VALUE"],"REDACTED")
    def test_t12_secret_prevention(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/".env"; p.write_text("TOKEN=secret"); self.assertFalse(package_sanitized(d)[0])
    def test_t13_git_readonly_preflight(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/".git").mkdir(); self.assertEqual(git_preflight(d)[0].key,"status")
    def test_t14_package_gate(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/"x.pyc").write_bytes(b"x"); self.assertFalse(package_sanitized(d)[0])
    def test_t15_benchmark_optional(self): self.assertEqual(benchmark_state(True,False),"SKIPPED"); self.assertEqual(benchmark_state(False,True),"READY")
    def test_t16_monitoring(self): self.assertIn("timestamp",monitoring_snapshot())
    def test_t17_json_schema(self): self.assertEqual(envelope([])["schema_version"],"0.3")
    def test_t18_mutation_default(self): self.assertEqual(envelope([])["security"]["MUTATION_OPERATIONS"],"NONE")
    def test_t19_future_host(self): self.assertEqual(envelope([Observation("host","x","PASS","OBSERVED","future","fixture",[])])["observations"][0]["value"],"future")
    def test_t20_stop_condition(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/".env").write_text("SECRET=x"); self.assertFalse(package_sanitized(d)[0])

if __name__=="__main__": unittest.main()
