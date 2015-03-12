#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
import sys

class NewVisitorTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
			super().setUpClass()
			cls.server_url = cls.live_server_url
			
	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()
	
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
	
	def test_layout_and_styling(self):
		#user goes to homepage
		self.browser.get(self.server_url)
		self.browser.set_window_size(1024, 764)
		
		#notices input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=15
		)
		
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=15
		)		
		
	
	def test_can_start_a_list_and_retrieve_it_later(self):
		#checking that homepage works
		self.browser.get(self.server_url)
		
		#notice the page header and title mention to-do lists
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
		user1_input_1 = 'buy peacock feathers'
		inputbox.send_keys(user1_input_1) 
		
		# when she hits enter she is taken to her unique URL and now the page lists 
		# "1: buy peacock feathers" as an item in a to-do list
		
		inputbox.send_keys(Keys.ENTER)
		user_list_url = self.browser.current_url
		self.assertRegex(user_list_url,'/lists/.+')	
		##time.sleep(10) used to view page, help found CSRF error when form didn't post it
		self.check_for_row_in_list_table('1: ' + user1_input_1)
		
		# she enters a second item
		inputbox = self.browser.find_element_by_id('id_new_item')
		user1_input_2 = 'make hat from feathers'
		inputbox.send_keys(user1_input_2)
		inputbox.send_keys(Keys.ENTER) 
		
		#page updates with both items in the table now
		self.check_for_row_in_list_table('1: ' + user1_input_1)
		self.check_for_row_in_list_table('2: ' + user1_input_2)
		
		#new user (Zetra) shows update
		## new browser to make sure none of user 1's info is showing
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Zetra doesn't see user lists
		self.browser.get(self.server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn(user1_input_1,page_text)
		self.assertNotIn(user1_input_2,page_text)		
		
		# zetra starts a new list
		inputbox = self.browser.find_element_by_id('id_new_item')
		user2_input_1 = 'buy milk'
		inputbox.send_keys(user2_input_1)
		inputbox.send_keys(Keys.ENTER) 		
		
		# Zetra gets own url 
		zetra_list_url = self.browser.current_url
		self.assertRegex(zetra_list_url,'/lists/.+')	
		self.assertNotEqual(zetra_list_url, user_list_url)
		
		# again make sure no mention of user 1 list in zetra list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn(user1_input_1,page_text)
		self.assertNotIn(user1_input_2,page_text)	
		self.assertIn(user2_input_1,page_text)

if __name__ == '__main__':
	unittest.main(warnings='ignore')
	