'''
Created on 2013-2-4

@author: lcy
'''
from django.conf.urls import url, patterns
urlpatterns = patterns('group.views',
    url(r'^my_groups_news/$','my_groups_news'),
    url(r'^my_groups_reply/$','my_groups_reply'),
    url(r'^my_groups_creat/$','my_groups_creat'),
    url(r'^creat_group/$', 'creat_group'),
    url(r'^(\d+)/$', 'group'),
    url(r'^(\d+)/enter/$', 'entergroup'),
    url(r'^(\d+)/quit/$', 'quitgroup'),
    url(r'^(\d+)/topic/(\d+)/$', 'showtopic'),
)
