#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import time
import collections

from birda import storage

from birda.storage import CO, BIRDA
from birda.storage.utils import get_types, get_property, prettify, get_co_list

# ============================================================================ #

class Widget(object):
	conn = None
	rdfw = None
	
	uri = ''
	instantiaton_time = None
	
	actionable = False
	hierarchical = False
	
	type = ''
	type_name = ''
	attributes = {}
	#core_attributes = {}
	descendants = []
	
	# --------------------------------- #
	
	def __init__(self, conn, rdfw=None, uri='', actionable=False, hierarchical=False):
		assert uri, "Uri is mandatory"
		
		self.conn = conn
		if not rdfw:
			# Creates a new RDFWrapper if not given
			rdfw = storage.RDFWrapper()
		self.rdfw = rdfw
		
		self.uri = uri
		self.instantiaton_time = time.time()
		
		self.actionable = actionable
		self.hierarchical = hierarchical
		
		self.type = Widget.get_type(self.conn, self.uri, rdfw=self.rdfw)
		self.type_name = Widget.get_type_name(self.type)
		
		self.attributes = self._get_attributes()
		
		if self.hierarchical:
			self.descendants = self._get_descendants()
		
	# --------------------------------- #
	
	def _get_attributes(self):
		"""
		Get the attributes of the widget
		
		:return: Dictionary containing widget properties
		"""
		
		a = collections.OrderedDict(())
		a['labels'] = get_property(self.conn, self.uri, BIRDA.hasLabel, rdfw=self.rdfw, lexical=True)
		a['descriptions'] = get_property(self.conn, self.uri, BIRDA.hasDescription, rdfw=self.rdfw, lexical=True)
		a['maps_property'] = get_property(self.conn, self.uri, BIRDA.mapsProperty, rdfw=self.rdfw, single=True)
		a['at_least'] = get_property(self.conn, self.uri, BIRDA.atLeast, rdfw=self.rdfw, single=True)
		a['at_most'] = get_property(self.conn, self.uri, BIRDA.atMost, rdfw=self.rdfw, single=True)
		
		return a
		
	# --------------------------------- #
	
	def _get_descendants(self):
		"""
		For hierarchical widgets, get descendant widgets
		
		:return: List of Widgets Objs 
		"""
		
		if not self.hierarchical:
			return []
		
		el_list = get_co_list(self.conn, self.uri, rdfw=self.rdfw)
		return [ Widget.create_instance(self.conn, uri, rdfw=self.rdfw) for uri in el_list ]
		
	# --------------------------------- #
	
	def __str__(self, indentation_level=0):
		indent = '    '*indentation_level
		s = []
		s += [indent + '-'*50]
		s += [indent + ' %s (%s)' % (self.type_name, prettify(self.uri))]
		s += [indent + '-'*50]
		
		for k in self.attributes.keys():
			if ( self.attributes[k] ) and ( type(self.attributes[k]) in [type([]), type(())] ):
				for v in self.attributes[k]:
					s += [indent + '    > %s: %s'%(k,v) ]
			else:
				s += [indent + '    > %s: %s'%(k,self.attributes[k]) ]
		
		for des in self.descendants:
			s += ['']
			s += [ des.__str__(indentation_level=indentation_level+1) ]
		
		return '\n'.join(s)
	
	# ================================= #
	
	@staticmethod
	def get_type(conn, uri, rdfw=None):
		"""
		Get the rdf type of the widget
		
		:param conn: RDF connection
		:param uri: Widget URI
		:param rdfw: Object RDFWrapper
		:return: String containing the uri (in the birda namespace)
		"""
		
		types = get_types(conn, uri, rdfw=rdfw)
		for type in types:
			if type.startswith(BIRDA):
				return type
		
		raise Error("No type found")
	
	# --------------------------------- #
	
	@staticmethod
	def get_type_name(type_uri):
		"""
		Get the rdf type human name of the widget
		
		:param type_uri: RDF connection
		:return: String containing the friendly name of the type
		"""
		
		return type_uri.replace(BIRDA,'')
	
	# --------------------------------- #
	
	@staticmethod
	def create_instance(conn, uri, rdfw=None):
		"""
		Create the right Widget instance for the specified widget URI
		
		:param conn: RDF connection
		:param uri: Widget URI
		:param rdfw: Object RDFWrapper
		:return: *Widget Obj
		"""
		
		type_name = Widget.get_type_name( Widget.get_type(conn, uri, rdfw=rdfw) )
		
		# TODO
		#if type_name == 'Form':
		#	return ...
		
		return Widget(
			conn, rdfw=rdfw, uri=uri,
			actionable=True, hierarchical=True)

# ---------------------------------------------------------------------------- #


# ============================================================================ #

if __name__ == '__main__':
	bConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='birda', verbose=False)
	iConn = storage.Storage.connect(storage.FAKE_SETTINGS, dataset='indiv', verbose=False)
		
# 	w = Widget(
# 			bConn, rdfw=storage.RDFWrapper(), uri=getattr(storage.BINST,'PersonLight-Form'),
# 			actionable=True, hierarchical=True)
	
	w = Widget.create_instance(bConn, getattr(storage.BINST,'PersonNormal-Form'))
	print
	print w.rdfw.dumps('turtle')
	print
	print w
	print
	
