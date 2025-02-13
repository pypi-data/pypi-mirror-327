#!/usr/bin/env python3

'''
Created on 12/01/2015

@author: dedson
'''

import sqlalchemy
import sqlalchemy.orm

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.engine import reflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm.collections import InstrumentedList, InstrumentedDict, InstrumentedSet

from .Base import Base
from .Class import Class

from jsonweb.encode import to_object
from jsonweb.decode import from_object

@from_object()
@to_object(suppress=['parent','clasz'])
class Instance(Base):
	'''
	this represents an object instance of a particular class and version
	'''

	__tablename__ = 'instance'
	
	id		  = Column(Integer, primary_key=True)
	name	  = Column(String(256))
	modified  = Column(DateTime)
	parent_id = Column(Integer, ForeignKey('instance.id'))
	parent	  = relationship("Instance", uselist=False, foreign_keys=[parent_id], remote_side=[id])
	clasz_id  = Column(Integer, ForeignKey('class.id'), nullable=False)
	clasz	  = relationship("Class", uselist=False, foreign_keys=[clasz_id])
	children  = relationship("Instance", uselist=True, back_populates='parent')
	
	def __init__(
		self,
		id=None,
		name=None,
		modified=None,
		parent_id=None,
		parent=None,
		clasz_id=None,
		clasz=None,
		children=[]
	):
		self.name = name
		self.parent_id = parent_id
		if parent:
			self.parent = parent 
			self.parent_id = parent.id
		self.clasz_id = clasz_id
		if clasz:
			self.clasz = clasz
			self.clasz_id = clasz.id
		self.children = children
		return

	def __dir__(self):
		return [
			'id',
			'name',
			'modified',
			'parent_id',
			'parent',
			'clasz_id',
			'clasz',
			'children'
		]


