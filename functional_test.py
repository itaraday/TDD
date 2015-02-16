from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		#force browser open for at least 3 seconds
		self.browser.implicity_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		#checking that homepage works
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
	