#-*- coding: UTF-8 -*-
from mongoengine import Document,fields
# Create your models here.
class Group(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True,verbose_name=u'小组名称')
    logo = fields.StringField()#logo路径
    birthday = fields.DateTimeField()#创建日期
    introduction = fields.StringField(required=True,verbose_name=u'小组简介')
    #tags = fields.ListField(fields.StringField())#小组标签
    #school = fields.StringField()
    grouptype = fields.StringField()#小组类型，是否为私密小组
    
    def get_topic_list(self):
        from accounts.models import S_G_Card
        creator = S_G_Card.objects(group=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator).all()
    
    def get_member_list(self):
        from accounts.models import S_G_Card
        return S_G_Card.objects(group=self,is_active=True).scalar('user')
        
        
        
        