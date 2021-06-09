from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .forms import CommentForm
from .models import Post

# Create your views here.

class CommentView(View):
    form_class = CommentForm
    template_name = 'posts/post.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, self.template_name, {'form':form})