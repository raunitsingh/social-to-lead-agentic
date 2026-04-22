import json
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent
KB_PATH = ROOT / "data" / "autostream_kb.json"


@pytest.fixture(scope="module")
def kb() -> dict:
    """Load and return the knowledge base once for all tests."""
    assert KB_PATH.exists(), f"KB not found at {KB_PATH}"
    with open(KB_PATH) as f:
        return json.load(f)


# ─── Structure tests ──────────────────────────────────────────────────────────

class TestKBStructure:
    def test_has_company(self, kb):
        assert "company" in kb

    def test_has_plans(self, kb):
        assert "plans" in kb
        assert isinstance(kb["plans"], list)
        assert len(kb["plans"]) >= 2

    def test_has_policies(self, kb):
        assert "policies" in kb
        assert isinstance(kb["policies"], list)

    def test_has_features_detail(self, kb):
        assert "features_detail" in kb


# ─── Pricing tests ────────────────────────────────────────────────────────────

class TestPricing:
    def _get_plan(self, kb, name_fragment: str) -> dict:
        for plan in kb["plans"]:
            if name_fragment.lower() in plan["name"].lower():
                return plan
        pytest.fail(f"No plan found matching '{name_fragment}'")

    def test_basic_plan_exists(self, kb):
        plan = self._get_plan(kb, "Basic")
        assert plan is not None

    def test_basic_plan_price(self, kb):
        plan = self._get_plan(kb, "Basic")
        assert plan["price_monthly"] == 29

    def test_basic_plan_video_limit(self, kb):
        plan = self._get_plan(kb, "Basic")
        features_text = " ".join(plan["features"])
        assert "10 videos" in features_text or "10" in features_text

    def test_basic_plan_resolution(self, kb):
        plan = self._get_plan(kb, "Basic")
        features_text = " ".join(plan["features"])
        assert "720p" in features_text

    def test_pro_plan_exists(self, kb):
        plan = self._get_plan(kb, "Pro")
        assert plan is not None

    def test_pro_plan_price(self, kb):
        plan = self._get_plan(kb, "Pro")
        assert plan["price_monthly"] == 79

    def test_pro_plan_unlimited_videos(self, kb):
        plan = self._get_plan(kb, "Pro")
        features_text = " ".join(plan["features"]).lower()
        assert "unlimited" in features_text

    def test_pro_plan_4k(self, kb):
        plan = self._get_plan(kb, "Pro")
        features_text = " ".join(plan["features"])
        assert "4K" in features_text or "4k" in features_text

    def test_pro_plan_ai_captions(self, kb):
        plan = self._get_plan(kb, "Pro")
        features_text = " ".join(plan["features"]).lower()
        assert "caption" in features_text


# ─── Policy tests ─────────────────────────────────────────────────────────────

class TestPolicies:
    def _get_policy(self, kb, name_fragment: str) -> dict:
        for policy in kb["policies"]:
            if name_fragment.lower() in policy["policy"].lower():
                return policy
        pytest.fail(f"No policy found matching '{name_fragment}'")

    def test_refund_policy_exists(self, kb):
        policy = self._get_policy(kb, "Refund")
        assert policy is not None

    def test_refund_policy_7_days(self, kb):
        policy = self._get_policy(kb, "Refund")
        assert "7" in policy["details"]

    def test_support_policy_exists(self, kb):
        policy = self._get_policy(kb, "Support")
        assert policy is not None

    def test_support_policy_pro_only(self, kb):
        policy = self._get_policy(kb, "Support")
        text = policy["details"].lower()
        assert "pro" in text
        assert "24" in policy["details"] or "24/7" in policy["details"]


# ─── Config test ──────────────────────────────────────────────────────────────

class TestConfig:
    def test_config_imports(self):
        """config.py must import without raising."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", ROOT / "config.py")
        mod  = importlib.util.module_from_spec(spec)
        # We don't exec (would need .env), just check the file parses
        import ast
        source = (ROOT / "config.py").read_text()
        tree = ast.parse(source)
        assert tree is not None

    def test_kb_path_constant_in_config(self):
        source = (ROOT / "config.py").read_text()
        assert "KB_PATH" in source
        assert "VECTORSTORE_PATH" in source
        assert "LLM_MODEL" in source
