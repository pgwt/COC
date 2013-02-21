# -*- coding: UTF-8 -*-
from mongoengine import Document, fields, PULL
from accounts.models import Student


# Create your models here.


class Corporation(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True, verbose_name=u'社团名称')
    logo = fields.StringField()  # logo路径
    birthyear = fields.IntField()  # 创建年份
    introduction = fields.StringField(required=True, verbose_name=u'社团简介')
    tags = fields.ListField(fields.StringField())  # 社团标签
    school = fields.StringField()
    who_watches = fields.ListField(fields.ReferenceField(Student, reverse_delete_rule=PULL))
    
    def get_member_list(self):  # 得到社团成员名片列表
        from accounts.models import S_C_Card
        return S_C_Card.objects(corporation=self, is_active=True).scalar('user')
        
    def get_topic_list(self):  # 得到论坛主题列表
        from accounts.models import S_C_Card
        creator = S_C_Card.objects(corporation=self).all()
        from forum.models import Topic
        return Topic.objects(creator__in=creator).all()
    
    def get_activity_list(self):  # 得到活动列表
        from activity.models import Activity
        return Activity.objects(sponsor=self).all()
        
    
    def add_watch(self, student):  # 添加关注社团
        return self.update(push__who_watches=student)
    
    def cancle_watch(self, student):  # 取消关注社团
        return self.update(pull__who_watches=student)
    
    def is_watches(self, student):  # 是不是你关注的社团
        if student in self.who_watches:
            return True
        else:
            return False
    
    
    
