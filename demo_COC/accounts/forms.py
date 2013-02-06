#-*- coding: UTF-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.http import HttpRequest
from accounts.models import Student


class AccountsSignupForm(forms.Form):
    email    = forms.EmailField()
    password = forms.CharField()
    realname = forms.CharField()
    
    gender = forms.CharField()

    
        
     
class AccountsLoginForm(forms.Form):
    login_email    = forms.EmailField(max_length=128, label=u'电子邮件',
                                error_messages={'required': u'请输入电子邮件地址', 'invalid': u'请输入有效的电子邮件地址'})
    login_password = forms.CharField(min_length=6,label=u'密码',
                                error_messages={'required': u'请输入密码','invalid':u'密码至少6位'})
    remember_me = forms.CharField(required=False)
    
    
    

class AccountsModifyProfileForm(forms.Form):
    
    realname = forms.CharField(label=u'真实姓名',max_length=5,min_length=1,
                               error_messages={'required':u'请输入真实姓名'})
    
    
    face = forms.ImageField(label=u'头像',required=False)
    
    school = forms.CharField(label=u'学校',required=False)
    
    birthday = forms.DateField(label=u'生日')
    
class NewFeedForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    

     
class AccountsModifyPasswordForm(forms.Form):       
    pass