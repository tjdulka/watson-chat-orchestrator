from helpers import config
import os, requests, json, logging
from ContainerObjects.SearchContainer import SearchContainer

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------

class knowledgeWareSearchContainer(SearchContainer):

	def populate_entity_from_search_result(self, result):
	#	this method to be reimplemented by child class for custom searches
		entity = {}
		entity['id'] = result['id']
		entity['body'] = result['text']
		entity['title'] = result['title']
		entity['category'] = result['ADSKCategory-local']
		entity['score'] = result['score']
		return entity


	def search_by_preferred_method(self, question):
	#	this method may be reimplemented by child class for custom searches
		return self.search_discovery(question)

	
def search_discovery(message_context):
	question = message_context.get_last_utterance()
	search_container = knowledgeWareSearchContainer()
	
	wks_entities = {}
	if config.WKS_ENTITIES in message_context.get_context_dict():
		wks_entities = message_context.get_context_dict()[config.WKS_ENTITIES]
		
	search_container.set_discovery_config(config.DISCOVERY_ENVIRONMENT, config.DISCOVERY_COLLECTION, config.WKS_ANNOTATOR_MODEL_ID_DISCOVERY, wks_entities)
	response = search_container.search(question)
	service_results = response
	return service_results

	