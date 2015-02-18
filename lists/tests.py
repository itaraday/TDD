from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		#self.assertTrue(response.content.startswith(b'<html>'))
		#self.assertIn(b'<title>To-Do lists</title>', response.content)
		#self.assertTrue(response.content.endswith(b'</html>'))
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
	
	#def test_home_page_displays_all_list_items(self):
	#	Item.objects.create(text='test 1')
	#	Item.objects.create(text='test 2')
	#	
	#	request = HttpRequest()
	#	response = home_page(request)
	#	
	#	self.assertIn('test 1', response.content.decode())
	#	self.assertIn('test 2', response.content.decode())
	
class ListAndItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		
		first_item = Item()
		first_item.text = 'The First (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'not The First item'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2, "only expected 2 items")
		self.assertEqual(saved_items[0].text, first_item.text, "item 1 is not saved item 1")
		self.assertEqual(saved_items[0].list, list_)
		self.assertEqual(saved_items[1].text, second_item.text, "item 2 is not saved item 2")
		self.assertEqual(saved_items[1].list, list_)

# this will replace most of HomePageTest
class ListViewTest(TestCase):
	def test_displays_all_list_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='test 1')
		Item.objects.create(text='test 2')

		response = self.client.get('/lists/My-Only-List/')
		
		self.assertContains(response, 'test 1')
		self.assertContains(response, 'test 2')
		
class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/My-Only-List/')
		self.assertTemplateUsed(response, 'list.html')
		
class NewListTest(TestCase):
	def test_save_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'}
		)
		self.assertEqual(Item.objects.count(),1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
	
	def test_redirects_after_post(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text':'A new list item'}
		)
		self.assertRedirects(response, '/lists/My-Only-List/')
		#self.assertEqual(response.status_code, 302)
		#self.assertEqual(response['location'], '/lists/My-Only-List/')