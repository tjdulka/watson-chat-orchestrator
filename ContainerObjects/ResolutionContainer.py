import os, json, logging
import os, json, logging
from helpers import session_mgr, lookup, config
from services import watson
from services.CustomService import CustomService
from flask import session
from ContainerObjects.ContextContainer import ContextContainer
from ContainerObjects.MessageContainer import MessageContainer

CHAT_TEMPLATE = config.CHAT_TEMPLATE
QUESTION_INPUT = config.QUESTION_INPUT
WKS_ANNOTATOR_MODEL_ID = config.WKS_ANNOTATOR_MODEL_ID
#--No longer used, delete if nothing breaks
#CURSOR_INPUT = config.CURSOR_INPUT
#FORM_INPUT = config.FORM_INPUT
#SEARCH_TYPE_INPUT = config.SEARCH_TYPE_INPUT
#SEARCH_VALUE_INPUT = config.SEARCH_VALUE_INPUT
#####
# Overwrites by env variables
#####
if 'CHAT_TEMPLATE' in os.environ:
	CHAT_TEMPLATE = os.environ['CHAT_TEMPLATE']
if 'QUESTION_INPUT' in os.environ:
	QUESTION_INPUT = os.environ['QUESTION_INPUT']
if 'WKS_ANNOTATOR_MODEL_ID' in os.environ:
	WKS_ANNOTATOR_MODEL_ID = os.environ['WKS_ANNOTATOR_MODEL_ID']
#--No longer used, delete if nothing breaks
#if 'CURSOR_INPUT' in os.environ:
	#CURSOR_INPUT = os.environ['CURSOR_INPUT']
#if 'FORM_INPUT' in os.environ:
	#FORM_INPUT = os.environ['FORM_INPUT']
#if 'SEARCH_TYPE_INPUT' in os.environ:
	#SEARCH_TYPE_INPUT = os.environ['SEARCH_TYPE_INPUT']
#if 'SEARCH_VALUE_INPUT' in os.environ:
	#SEARCH_VALUE_INPUT = os.environ['SEARCH_VALUE_INPUT']

def extract_entities_from_question(question):
	global WKS_ANNOTATOR_MODEL_ID
	entities = {}
	print('----------------------')
	print('--extract_entities_from_question()')
	print(question)
	if WKS_ANNOTATOR_MODEL_ID is not None:
		parameters = {}
		parameters['text'] = question.encode('ascii','ignore')
		parameters['extract'] = 'entities'
		parameters['disambiguate'] = '1'
		parameters['model'] = WKS_ANNOTATOR_MODEL_ID
		response = watson.BMIX_call_alchemy_api('/text/TextGetRankedNamedEntities', parameters)
		if 'entities' in response:
			for entity in response['entities']:
				entity_type = entity['type']
				entity_text = entity['text'].encode('ascii','ignore')
				if entity_type not in entities:
					entities[entity_type] = entity_text
				elif type(entities[entity_type]) is str:
					entities[entity_type] = [entities[entity_type]]
					entities[entity_type].append(entity_text)
				else:
					entities[entity_type].append(entity_text)
	print(entities)
	return entities


class ResolutionContainer:
	chat = None
	form = None
	service_results = None
	message = None
	invoke_custom_service = None
	custom_service_name = None

	
	def __init__(self):
		#self.chat = ''
		#self.form = ''
		#self.custom_service_name = ''
		self.service_results = {}
		self.message = MessageContainer()
		invoke_custom_service = False

		
	def set_form(self, text):
		self.form = ''
		if config.PRESENT_FORM in text:
			responses = text.split(config.PRESENT_FORM)
			self.form = responses[1]
		return self.form


	def set_chat(self, text):
		self.chat = text
		if config.PRESENT_FORM in text:
			responses = text.split(config.PRESENT_FORM)
			self.chat = responses[0]
		if (self.chat.startswith(config.INVOKE_CUSTOM_SERVICE)):
			self.invoke_custom_service = True
			self.chat = self.chat.replace(config.INVOKE_CUSTOM_SERVICE, '')
			self.custom_service_name = self.chat
		else:
			self.invoke_custom_service = False
			self.custom_service_name = None
			
		#self.chat = lookup.substitute_hash_values(self.chat)
		return self.chat


	def has_service_results(self):
		return self.service_results


	def converse(self):
		local_message = MessageContainer()
		local_message.put_dict_msg_updates(self.message.get_msg_dict())
		local_message.context.hide_private_values()
		local_message = watson.BMIX_converse(local_message)

		local_context = ContextContainer()
		local_context.put_dict_context_updates(self.message.context.get_context_dict())
		local_context.put_dict_context_updates(local_message.context.get_context_dict())
		
		local_message.context = local_context
		self.message = local_message
		session_mgr.set('MESSAGE', self.message.get_msg_dict())

	#--	Below is only code needed before adding logic to hide private values from conversation
	#	self.message = watson.BMIX_converse(self.message)
	#	session_mgr.set('MESSAGE', self.message.get_msg_dict())
		return self.message

		
	def resolve(self):
		logging.debug("in ResolutionContainer.resolve")
		
		self.service_results = {}
		formatted_text = self.message.get_output_text()

		logging.debug("in ResolutionContainer.resolve - formatted text is currently :")
		logging.debug(formatted_text)

		self.set_chat(formatted_text)
		self.set_form(formatted_text)

		if (self.invoke_custom_service):
			custom_service = CustomService()
			self.service_results = custom_service.invoke_custom_service(self.chat, self.message.context)

		return self


	def orchestrate(self, input_question, input_context):
		logging.debug("in ResolutionContainer.orchestrate")

		self.message = MessageContainer()
		local_question = input_question
		local_context = input_context
		#modified for WKS-ALCHEMY integration
		wks_entities = {}
		wks_entities[config.WKS_ENTITIES] = extract_entities_from_question(local_question)
		#print('--Entities extracted with WKS')
		#print(wks_entities)
		local_context.put_dict_context_updates(wks_entities)

		while True:
			logging.debug("### in ResolutionContainer.orchestrate while loop")
			self.message.update_message(local_question, local_context)
			logging.debug("%%% Message container before inc CONVERSE call is ")
			self.message.message_info_dump()
			self.converse()
			logging.debug("&&& Message container after inc CONVERSE call is ")
			self.message.message_info_dump()
			self.resolve()
			
			if self.has_service_results():
				local_context = ContextContainer()
				local_context.put_dict_context_updates(self.service_results)
				local_question = self.chat
				logging.debug(local_question)
				logging.debug(local_context.get_context_dict())
			else:
				break
			
		return self
		
