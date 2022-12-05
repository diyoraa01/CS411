#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db

class Music(db.Document):
    musicname = db.StringField()
    author = db.StringField()
    
    def __str__(self):
        return "musicname:{} - author:{}".format(self.musicname, self.author)

