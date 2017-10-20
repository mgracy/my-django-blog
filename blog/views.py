from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone
import logging

# Create your views here.
# trackback: https://tutorial.djangogirls.org/en/django/

logger = logging.getLogger(__name__)
print('__name__ is {}'.format(__name__))

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})	

def post_new(request):
	form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})	