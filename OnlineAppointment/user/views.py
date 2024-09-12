from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render , redirect
from django.views import View
from .forms import UserREgisterForm , UserLoginForm , CommentForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login , authenticate , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Comment

# Create your views here.

class HomeView(View):
    def get(self , request):
        return render(request , 'user/index.html')
    def post (self , request):
        return render(request , 'user/index.html')

class UserRegisterView(View):
    form_class = UserREgisterForm
    template_name = 'user/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})
    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('user:home')
        return render(request , self.template_name , {'form':form})
    

class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'user/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get (self, request):
        form = self.form_class
        return render(request , self.template_name , {'form':form})
    def post (self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username = cd['username'], password = cd['password'])
            if user is not None:
                login(request , user)
                messages.success(request , 'you login successfully','success')
                return redirect('user:home')    
            messages.error(request , 'username or password is wrong' , 'warning')
        return render(request, self.template_name , {'form':form})    
    
class UserLogoutView(LoginRequiredMixin,View):
    def get(self , request):
        logout(request)
        messages.success(request , 'you logout successfully' , 'success')    
        return redirect('user:home')
    
def add_comment(request):
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect('user:home')
    else:
        form = CommentForm()
    return render(request,'comment.html',{'form':form})        