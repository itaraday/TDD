from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

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

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'
		
		response = home_page(request)
		
		self.assertIn('A new list item', response.content.decode())
		expected_html = render_to_string(
			'home.html',
			{'new_item_text': 'A new list item'}
		)
		self.assertEqual(response.content.decode(), expected_html, "didn't find new list item")		


class ItdemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The First (ever) list item'
		first_item.save()
		
		second_item = Item()
		second_item.text = 'not The First item'
		second_item.save()
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2, "only expected 2 items")
		self.assertEqual(saved_items[0].text, first_item.text, "item 1 is not saved item 1")
		self.assertEqual(saved_items[1].text, second_item.text, "item 2 is not saved item 2")
		