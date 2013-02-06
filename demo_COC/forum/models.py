#-*- coding: UTF-8 -*-   
from accounts.models import Student,S_G_Card
from mongoengine import Document,fields,DO_NOTHING,CASCADE
# Create your models here.

class Topic(Document):
    title = fields.StringField(verbose_name=u'标题')
    content = fields.StringField(verbose_name=u'内容')
    url_number = fields.IntField()
    creator = fields.ReferenceField(S_G_Card,reverse_delete_rule=DO_NOTHING)#发布人
    creat_time = fields.DateTimeField()#发布时间
    
    update_time = fields.DateTimeField()#更新时间
    update_author = fields.ReferenceField(Student,reverse_delete_rule=DO_NOTHING)#最后回复人
    
    clicks = fields.IntField()#浏览数
    
    is_active = fields.BooleanField(verbose_name=u'可见')
    is_locked = fields.BooleanField(verbose_name=u'锁帖')
    is_top = fields.BooleanField(verbose_name=u'置顶')
    
    def get_post_list(self):
        return Post.objects(topic=self).all()


class Post(Document):
    content = fields.StringField(verbose_name=u'内容')
    author = fields.ReferenceField(Student,reverse_delete_rule=DO_NOTHING)#发布人
    creat_time = fields.DateTimeField()#发布时间
    floor = fields.IntField()#楼层
    is_active = fields.BooleanField(verbose_name=u'可见')
    topic = fields.ReferenceField(Topic,reverse_delete_rule=CASCADE)
    
    
    