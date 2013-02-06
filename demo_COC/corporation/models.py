#-*- coding: UTF-8 -*-
from PIL import Image
from mongoengine import Document,fields,PULL
from accounts.models import Student


# Create your models here.


class Corporation(Document):
    url_number = fields.IntField()
    name = fields.StringField(required=True,verbose_name=u'社团名称')
    logo = fields.ImageField()
    birthyear = fields.IntField()#创建年份
    introduction = fields.StringField(required=True,verbose_name=u'社团简介')
    tags = fields.ListField(fields.StringField())#社团标签
    school = fields.StringField()
    who_watches = fields.ListField(fields.ReferenceField(Student,reverse_delete_rule=PULL))
    
    def has_student(self):#得到社团成员名片列表
        from accounts.models import S_C_Card
        return S_C_Card.objects(corporation=self)
        
    def has_topics(self):#得到论坛主题列表
        from forum.models import Topic
        from accounts.models import S_C_Card
        sccard = S_C_Card.objects(corporation=self)
        return Topic.objects(s_c_card=sccard)
    
    def has_activity(self):#得到活动列表
        from activity.models import Activity
        return Activity.objects(sponsor=self)
    
    def enter_corporation(self,student,position='成员'):#加入社团
        from accounts.models import S_C_Card
        s = S_C_Card(user=student,corporation=self,position=position)
        return s.save()
    
    def quit_corporation(self,student):#退出社团
        from accounts.models import S_C_Card
        return S_C_Card.objects(Q(user=student)|Q(corporation=self)).delete()
        
    def is_entered_corporation(self,student):#是不是你加入的社团
        from accounts.models import S_C_Card
        if S_C_Card.objects(Q(user=student)|Q(corporation=self)):
            return True
        else:
            return False
    
    def add_watch(self,student):#添加关注社团
        return self.update(push__who_watches=student)
    
    def cancle_watch(self,student):#取消关注社团
        return self.update(pull__who_watches=student)
    
    def is_watches(self,student):#是不是你关注的社团
        if student in self.who_watches:
            return True
        else:
            return False
    
    
    