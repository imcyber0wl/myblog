from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, JsonResponse
from .forms import *
from .models import *
from django.core.files.storage import FileSystemStorage
import json 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging

logger= logging.getLogger('django')

@cache_page(60 * 15)
def main(request):
    page = request.GET.get('page', 1)
    articles=Article.objects.all()
    paginator = Paginator(articles, 10)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request,"main.html",{"articles":articles})

@cache_page(60 * 150)
def article(request,num):
    article=Article.objects.filter(id=num).first()
    nolike=0 #user can like
    edit=0
    cache.set('maincache',article,100*60)
    if not request.user.is_authenticated:
        return render(request,"article.html",{"article":article,"like":'',"nolike":1,"edit":edit})
    try:
        likes=Likes.objects.get(user=request.user,articleid=num)        
    except:
        likes=Likes.objects.create(user=request.user,articleid=num)
        likes.save()
    if request.user == article.author.user:
        edit=1 #allow editing
    return render(request,"article.html",{"article":article,"like":likes.like,"nolike":nolike,"edit":edit})


@login_required(login_url='/login/')
def write(request):
    logger.info('User '+str(request.user)+" visited new-article ")
    if request.method=='POST':
        form=WriteForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            content=form.cleaned_data.get('content')
            if request.FILES['img']:
                image = request.FILES['img']
                fs = FileSystemStorage()
                file_name = fs.save(image.name, image)
                file_url = fs.url(file_name)
                img=file_url
            else:
                img=''
            profile=Profile.objects.get(user=request.user)
            obj=Article.objects.create(author=profile,
                                       likes=0,
                                       title=title,
                                       content=content,
                                       img=img)
            obj.save()

            return HttpResponseRedirect('')
    else:
        form=WriteForm()
        return render(request,"write.html",{"form":form})
    
@login_required(login_url='/login/')
def myprofile(request):
    page = request.GET.get('page', 1)
    logger.info('User '+str(request.user)+" visited profile "+str(page))
    profile=Profile.objects.get(user=request.user)
    articles=Article.objects.filter(author=profile).all()
    paginator = Paginator(articles, 5)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    return render(request,"myprofile.html",{"profile":profile, "articles":articles,})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                return redirect('main')
            else:
                return render(request, "login.html",{"form":LoginForm(),"msg":"Wrong username/password"})
                
    else:
        form=LoginForm()
        return render(request, "login.html",{"form":form})


def register(request):
    if request.user.is_authenticated:
        return redirect('main')
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile=Profile.objects.create(user=user)
            profile.save()
            return redirect('login')
        else:
            return render(request, "register.html",{"form":RegisterForm(), "msg":"Please enter valid data",})
    else:
        form=RegisterForm()
        return render(request, "register.html",{"form":form})


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        logout(request)
        return redirect('main')


@login_required(login_url='/login/')
def like(request):
    data=json.loads(request.body)
    likes,created=Likes.objects.get_or_create(user=request.user,articleid=data['article'])

    if likes.like==0:
        likes.like=1
        article=Article.objects.get(id=data['article'])
        article.likes+=1
        article.save()
    else:
        likes.like=0
        article=Article.objects.get(id=data['article'])
        article.likes-=1
        article.save()
        
    likes.save()
    return JsonResponse({'foo':'bar'})
    
@login_required(login_url='/login/')
def edit_profile(request):
    if request.method=="POST":
        form=EditProfileForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            bio=form.cleaned_data.get('bio')
            profile=Profile.objects.get(user=request.user)
            img=profile.img
            if request.FILES['img']:
                image = request.FILES['img']
                fs = FileSystemStorage()
                file_name = fs.save(image.name, image)
                file_url = fs.url(file_name)
                img=file_url
            profile.name=name
            profile.bio=bio
            profile.img=img
            profile.save()
            return redirect('profile')
        else:
            profile=Profile.objects.get(user=request.user)
            context={"form":EditProfileForm(),
            "name":profile.name,
            "bio":profile.bio,}
            return render(request, "editprofile.html", context)
    else:
        profile=Profile.objects.get(user=request.user)
        context={"form":EditProfileForm(),
        "name":profile.name,
        "bio":profile.bio,}
        return render(request, "editprofile.html", context)


@login_required(login_url='/login/')
def edit_article(request,num):
    profile=Profile.objects.get(user=request.user)
    article=Article.objects.get(id=num)
    if profile.user != article.author.user:
        return redirect('main')
    
    if request.method=='POST':
        form=WriteForm(request.POST)
        if form.is_valid():
            img=article.img
            title=form.cleaned_data.get('title')
            content=form.cleaned_data.get('content')
            if request.FILES['img']:
                image = request.FILES['img']
                fs = FileSystemStorage()
                file_name = fs.save(image.name, image)
                file_url = fs.url(file_name)
                img=file_url

            article.title=title
            article.content=content
            article.img=img
            article.save()
            return HttpResponseRedirect('')

        else:
            article=Article.objects.get(id=num)
            context={"form":WriteForm(), "title":article.title,
                 "content":article.content}
            return render(request,"editarticle.html",context)

    else:
        article=Article.objects.get(id=num)
        context={"form":WriteForm(), "title":article.title,
                 "content":article.content}
        return render(request,"editarticle.html",context)
