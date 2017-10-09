from django import forms
from .models import Post

class PostForm(form.ModelForm):
	class Meta:
		model = Post
		fields = ('title', 'text',)