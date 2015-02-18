from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		new_item_text = request.POST.get('item_text', '')
		Item.objects.create(text=new_item_text)
		return redirect('/')
	items = Item.objects.all()
	context = { "items": items }
	template = 'home.html'
	return render(request, template, context)
	