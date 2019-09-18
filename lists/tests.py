from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve("/")
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):

		name = "Benny William Pardede"
		npm = "1606917550"
		role = "trequartista"

		request = HttpRequest()
		response = home_page(request)
		html = response.content.decode('utf8')
		self.assertTrue(html.startswith('<html>'))
		self.assertIn('<title>HomePage</title>', html)
		self.assertIn(name, html)
		self.assertIn(npm, html)
		self.assertIn(role, html)
		self.assertTrue(html.endswith('</html>'))