from selenium import webdriver
import unittest

class HomePageTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_can_access_homepage_view_with_fullname_innit(self):

		name = "Benny William Pardede"
		npm = "1606917550"
		role = "trequartista"

		# Benny needs to show make an introductory homepage of himself
		# Benny had filled the landing page with internal gags within himself
		# Benny needs help

		# He opens the browser to open the page
		self.browser.get('http://localhost:8000')

		# He notices the page title goes 'Homepage'
		self.assertEquals('Homepage', self.browser.title)

		# There's his birth name
		self.assertIn(name, self.browser.find_element_by_id('name'))

		# That's just his alias
		self.assertIn(role, self.browser.find_element_by_id('alias'))

		# His Student Id
		self.assertIn(npm, self.browser.find_element_by_id('npm'))

if __name__ == '__main__':
	unittest.main(warnings='ignore')