from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		#force browser open for at least 3 seconds
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.quit()
	
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])		
	
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
		inputbox.send_keys('buy peacock feathers') 
		
		#when she hits enter the page updates and now the page lists 
		# "1: buy peacock feathers" as an item in a to-do list
		inputbox.send_keys(Keys.ENTER) 
		#used to view page, help found CSRF error when form didn't post it
		#time.sleep(10)
		self.check_for_row_in_list_table('1: buy peacock feathers')
		
		# she enters a second item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('make hat from feathers')
		inputbox.send_keys(Keys.ENTER) 
		
		#page updates with both items in the table now
		self.check_for_row_in_list_table('1: buy peacock feathers')
		self.check_for_row_in_list_table('2: make hat from feathers')
		
		#the website generates a unique URL for the user to return to their lists		
		self.fail('Finish the test!')


if __name__ == '__main__':
	unittest.main(warnings='ignore')
	