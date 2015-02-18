from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		#force browser open for at least 3 seconds
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self):
		#checking that homepage works
		self.browser.get('http://localhost:8000')
		
		#notice the page header and tiotle mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		#invite user to make a to-do list
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		#use enters 'buy peacock feathers' in input
		input.send_keys('buy peacock feathers') 
		
		#when she hits enter the page updates and now the page lists 
		# "1: buy peacock feathers" as an item in a to-do list
		input.send_keys(keys.ENTER) 
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_element_by_tag_name('tr')
		self.assertTrue(any(row.text == "1: buy peacock feathers"))
		
		# she enters a second time
		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
	