from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	context = {
		'new_item_text': request.POST.get('item_text', ''),
	}
	template = 'home.html'
	return render(request, template, context)
	
	if request.method == 'POST':
		return HttpResponse(request.POST['item_text'])

	return render(request, 'home.html')