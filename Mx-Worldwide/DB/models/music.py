#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db

# 类名定义 collection
class Music(db.Document):
    # 字段
    musicname = db.StringField()
    author = db.StringField()
    
    def __str__(self):
        return "musicname:{} - author:{}".format(self.devicename, self.author)

