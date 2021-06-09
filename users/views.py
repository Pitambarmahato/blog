import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View

from .models import CustomUser, Profile, Following
from .forms import CustomUserCreationForm, ProfileForm
from posts.models import Post
# Create your views here.
class SignupView(View):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        # print('heool')
        # print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context = {
                'form':form,
            }
            return render(request, self.template_name, context)
    

class ProfileView(View):
    template_name = 'profile.html'
    model = Profile
    form_class = ProfileForm

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id = pk)
        form = self.form_class
        context = {
            'profile':profile,
            'posts':posts,
            'articles':posts.count(),
            'form':form,
            'user':user
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        print(user_id)
        profile = Profile.objects.get(user_id = user_id)
        form = self.form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # profile = Profile.objects.update(user_id = user_id, image = form.cleaned_data['image'], bio = form.cleaned_data['bio'])
            form.save()
            return redirect(reverse('profile', kwargs={'pk': user_id}))

        return redirect(reverse('profile', kwargs={'pk': user_id}))
        

def follow(request, pk):
    user = request.user
    to_follow = CustomUser.objects.get(id = pk)
    
    #check if already following
    following = Following.objects.filter(followed_to=user, followed_by = to_follow)
    print(following)
    is_following = True if following else False

    if is_following:
        Following.unfollow(user, to_follow)
        is_following = False
    else:
        Following.follow(user, to_follow)
        is_following = True
    
    resp = {
        "following":is_following,
    }
    response = json.dumps(resp)

    return HttpResponse(response, content_type="application/json")