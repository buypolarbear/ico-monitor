from django.test import TestCase
from .utils import get_token_info
# Create your tests here.
class UtilsTest(TestCase):
    def test_get_info(self):
        info = get_token_info("0xf6Fd82dEdBBe0ffadb5e1ecc2a283AB52B9ED2B0")  # Token Etheal
        self.assertEqual(info.get("symbol",""), "HEAL")
        self.assertEqual(info.get("decimals",""), "18")

