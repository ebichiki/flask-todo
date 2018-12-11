# coding: utf-8
from todo import db
from sqlalchemy import *
from datetime import datetime

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(Integer, primary_key=True)
    text = db.Column(Text)
    completed = db.Column(Integer,default=0)
    created_at = db.Column(DateTime, default=datetime.now())
    updated_at = db.Column(DateTime, default=datetime.now())
    elaps = ""

    def __repr__(self):
        return "<Entry id{} = text={!r}>".format(self.id,self.text)

def init():
    db.create_all()