# Gregorio
# 

from app import db
from models.music import Music


class User(db.Document):
    name = db.StringField(max_length=30, required=True)
    gender = db.StringField()
    language = db.StringField()
    

    def __str__(self):
        return "name:{} - language:{}".format(self.name, self.language)
    
