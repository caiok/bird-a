#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------- #
# Enables python3-like strings handling
from __future__ import unicode_literals
str = unicode
# -------------------------------------- #

import json
import colander
import cornice

import jsons.individuals
import birda.storage as storage

from __init__ import ServiceError, is_verbose, do_commit
from jsons.individuals import IndividualsInfos, SearchQuery

# ============================================================================ #

# FIXME
# Workaround: used individuals-search instad of individuals/search because url
# matching takes erroneously the individuals/* rule. To be fixed. 

individuals_search = cornice.Service(
		name='individuals_search',
		path='/api/individuals-search',
		description="Individuals search")

individuals_search_v1 = cornice.Service(
		name='individuals_search_v1',
		path='/api/v1/individuals-search',
		description="Individuals search")

# ---------------------------------------------------------------------------- #

@individuals_search.post()
@individuals_search_v1.post()
def individuals_search(request):
	
	lang = request.GET.get('lang','en').lower()
	limit = request.GET.get('lang','0')
	offset = request.GET.get('lang','0')
	form_uri = request.GET.get('form_uri','')
	
	if not form_uri:
		raise ServiceError(status=400, msg="'form_uri' must be passed in GET parameters", connections=[]) 
	if not request.json_body:
		raise ServiceError(status=400, msg="A valid JSON object have to be passed in POST body", connections=[]) 
	
	try:
		in_json = SearchQuery().deserialize(request.json_body)
	except colander.Invalid as e:
		raise ServiceError(status=400, msg="JSON validation error", additional=e.asdict(), connections=[])
	
	forms_factory = request.find_service(name='FormsFactory')
	
	w_form = forms_factory.get_form(form_uri)
	if not w_form:
		raise ServiceError(status=404, msg="Form '%(form_uri)s' not found" % vars(), connections=[]) 
	
	iConn = storage.Storage.connect(request.registry.settings, dataset='indiv', verbose=False)
	
	individuals_factory = request.find_service(name='IndividualsFactory')
	j = individuals_factory.search(iConn, in_json, w_form, lang, limit, offset)
	
	iConn.close()
	return j

# ============================================================================ #

individual = cornice.Service(
		name='individual',
		path='/api/individuals/*individual_uri',
		description="Individuals CRUD operations")

individual_v1 = cornice.Service(
		name='individual_v1',
		path='/api/v1/individuals/*individual_uri',
		description="Individuals CRUD operations")

# ---------------------------------------------------------------------------- #

def individual_initialization(request):
	u = request.matchdict['individual_uri']
	
	if not u:
		raise ServiceError(status=400, msg="Individual URI is mandatory in method %s" % request.method, connections=[])
		
	individual_uri = u[0] + '//' + '/'.join(u[1:])
	form_uri = request.GET.get('form_uri','')
	lang = request.GET.get('lang','en').lower()
	
	if not form_uri:
		raise ServiceError(status=400, msg="Querystring parameter 'form_uri' is mandatory" % vars(), connections=[])
	
	forms_factory = request.find_service(name='FormsFactory')
	individuals_factory = request.find_service(name='IndividualsFactory')
	
	w_form = forms_factory.get_form(form_uri)
	if not w_form:
		raise ServiceError(status=404, msg="Form '%(form_uri)s' not found" % vars(), connections=[]) 
	
	iConn = storage.Storage.connect(request.registry.settings, dataset='indiv', verbose=False)
	ind = individuals_factory.get_individual(iConn, individual_uri, form_uri)
	
	return iConn, lang, ind

# ---------------------------------------------------------------------------- #

@individual.get()
@individual_v1.get()
def individual_get(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if not ind.is_present_at_db():
		raise ServiceError(status=404, msg="Individual '%s' not found" % ind.individual_uri, connections=[iConn])
	
	j = ind.get_json(lang)
	j = {
		"individuals": [ j ] 
	}
	
	try:
		deserialized = IndividualsInfos().deserialize(j)
	except colander.Invalid as e:
		raise ServiceError(status=500, msg="JSON validation error", additional=e.asdict(), connections=[iConn])
	
	iConn.close()
	
	return deserialized

# ---------------------------------------------------------------------------- #

@individual.put()
@individual_v1.put()
@individual.post()
@individual_v1.post()
def individual_put_post(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if (request.method == 'PUT') and (ind.is_present_at_db()):
		raise ServiceError(status=409, msg="Individual '%s' already present at DB" % ind.individual_uri, connections=[iConn])
	
	if (request.method == 'POST') and (not ind.is_present_at_db()):
		raise ServiceError(status=404, msg="Individual '%s' not found" % ind.individual_uri, connections=[iConn])	
	
	try:
		j = IndividualsInfos().deserialize(request.json_body)
	except colander.Invalid as e:
		raise ServiceError(status=400, msg="JSON validation error", additional=e.asdict(), connections=[iConn])
	
	if len(j['individuals']) != 1:
		raise ServiceError(status=400, msg="There should be only one individual in PUT/POST json", connections=[iConn])
	
	issues = ind.load_json(j['individuals'][0])
	
	if issues:
		raise ServiceError(status=500, msg="JSON validation error", additional=issues, connections=[iConn])
	
	modified = ind.update_db(verbose=is_verbose(request))
	
	j = ind.get_json(lang)
	j = {
		"individuals": [ j ] 
	}
	
	try:
		deserialized = IndividualsInfos().deserialize(j)
	except colander.Invalid as e:
		raise ServiceError(status=500, msg="JSON validation error", additional=e.asdict(), connections=[iConn])
	
	if modified and do_commit(request):
		iConn.commit()
	iConn.close()
	
	return deserialized

# ---------------------------------------------------------------------------- #

@individual.delete()
@individual_v1.delete()
def individual_delete(request):
	
	iConn, lang, ind = individual_initialization(request)
	
	if not ind.is_present_at_db():
		#raise ServiceError(status=404, msg="JSON validation error", additional=e.asdict())
		request.response.status = 202
		if is_verbose(request): print "Not found"
	else:
		ind.delete()
		request.response.status = 204
		if is_verbose(request): print "Deleted!!"
	
	if do_commit(request):
		iConn.commit()
	iConn.close()
	
	return {}

# ============================================================================ #
