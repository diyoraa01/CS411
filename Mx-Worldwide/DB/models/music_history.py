#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db

class MH(db.Document):
    user_name = db.StringField()
    music_name = db.StringField()
    artist = db.StringField()

    
    
    def __str__(self):
        return "user_id:{} - music_id:{}".format(self.user_id, self.music_id)