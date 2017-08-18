from django.shortcuts import render

# Create your views here.
# trackback: https://tutorial.djangogirls.org/en/django/

def post_list(request):
	return render(request, 'blog/post_list.html', {})