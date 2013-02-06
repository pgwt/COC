#-*- coding: UTF-8 -*-
import os
import datetime
from PIL import Image
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from demo_COC.settings import STATIC_URL,MEDIA_ROOT,MEDIA_URL
from django.http import HttpResponseRedirect
from django.contrib.auth import *
from forms import CreatGroupForm
from models import Group
from forum.models import Topic,Post
from forum.forms import NewTopicForm,NewPostForm
from accounts.models import S_G_Card
from django.template import RequestContext
from mongoengine.django.sessions import MongoSession
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def creat_group(request):
    if request.method == "POST":
        form = CreatGroupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            introduction = form.cleaned_data['introduction']
            grouptype = form.cleaned_data['grouptype']
            group = Group(name=name,introduction=introduction,grouptype=grouptype,logo=STATIC_URL+'img/face.png')
            url_number = len(Group.objects) + 1
            group.url_number = url_number
            group.birthday = datetime.datetime.now()
            if request.FILES:
                path = 'img/group/' + str(url_number)
                if not os.path.exists(MEDIA_ROOT+path):
                    os.makedirs(MEDIA_ROOT+path)
                
                img = Image.open(request.FILES['logo'])
                if img.mode == 'RGB':
                    filename = 'logo.jpg'
                elif img.mode == 'P':
                    filename = 'logo.png'
                filepath = '%s/%s' % (path, filename)
                #获得图像的宽度和高度
                width,height = img.size
                #计算高宽比
                ratio = 1.0 * height / width
                #计算新的高度
                new_height = int(260 * ratio)
                new_size = (260, new_height)
                #插值缩放图像，
                out = img.resize(new_size, Image.ANTIALIAS)
                out.save(MEDIA_ROOT+filepath)
                group.logo = MEDIA_URL + filepath
                
            group.save()
            sgcard = S_G_Card(user=request.user,group=group,is_active=True,creat_time=datetime.datetime.now())
            sgcard.save()
            return HttpResponseRedirect('/group/' + str(url_number) + '/')
        
    else:
        form = CreatGroupForm()
        return render_to_response('group/creat_group.html',{'form':form,'STATIC_URL':STATIC_URL,'current_user':request.user}, context_instance=RequestContext(request))
                
                 
def group(request,gurl_number):
    group = Group.objects(url_number=gurl_number).get()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            topic = Topic(title=title)
            turl_number = len(Topic.objects) + 1
            topic.url_number = turl_number
            topic.content = content
            topic.creat_time = datetime.datetime.now()
            topic.is_active = True
            topic.is_locked = False
            topic.is_top = False
            topic.clicks = 0
            topic.update_time = datetime.datetime.now()
            topic.update_author = request.user
            sgcard = S_G_Card.objects(user=request.user,group=group).get()
            topic.creator = sgcard
            topic.save()
            return HttpResponseRedirect('/group/' + str(gurl_number) + '/topic/' + str(turl_number) + '/')
            
            
    else:
        form = NewTopicForm()
        return render_to_response('group/group.html',{'form':form, 'group':group,'STATIC_URL':STATIC_URL,'current_user':request.user}, context_instance=RequestContext(request))
        
    
def entergroup(request,url_number):
    group = Group.objects(url_number=url_number).get()
    if S_G_Card.objects(user=request.user,group=group):
        S_G_Card.objects(user=request.user,group=group).update(set__is_active=True,set__creat_time=datetime.datetime.now())
    else:
        S_G_Card(user=request.user,group=group,is_active=True,creat_time=datetime.datetime.now()).save()
    return HttpResponse('success')
    
def quitgroup(request,url_number):
    group = Group.objects(url_number=url_number).get()
    S_G_Card.objects(user=request.user,group=group,is_active=True).update(set__is_active=False)
    return HttpResponse('success')
    
    
def showtopic(request,gurl_number,turl_number):
    group = Group.objects(url_number=gurl_number).get()
    topic = Topic.objects(url_number=turl_number).get()
    topic.clicks += 1
    topic.save()
    if request.method == 'POST':
        form = NewPostForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            post = Post(content=content)
            post.author = request.user
            post.creat_time = datetime.datetime.now()
            post.floor = Post.objects(topic=topic).count() + 1
            post.topic = topic
            post.is_active = True
            post.save()
            topic.update_author = request.user
            topic.update_time = datetime.datetime.now()
            topic.save()
            return HttpResponseRedirect('/group/'+ str(gurl_number) + '/topic/' + str(turl_number) + '/')
        
    else:
        form = NewPostForm()
        return render_to_response('group/group_topic.html',{'group':group, 'form':form,'topic':topic,'STATIC_URL':STATIC_URL,'current_user':request.user}, context_instance=RequestContext(request))

    
    
    
    
                