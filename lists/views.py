from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

# Create your views here.
def home_page(request):
	template = 'home.html'
	return render(request, template)

def view_list(request):
	items = Item.objects.all()
	context = { "items": items }
	template = 'list.html'
	return render(request, template, context)
	
def new_list(request):
	list_ = List.objects.create()
	new_item_text = request.POST.get('item_text', '')
	Item.objects.create(text=new_item_text, list=list_)
	return redirect('/lists/My-Only-List')
	