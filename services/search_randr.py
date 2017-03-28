from helpers import config
import os, requests, json, logging
from ContainerObjects.SearchContainer import SearchContainer

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------

class runBookSearchContainer(SearchContainer):

	def populate_entity_from_search_result(self, result):
	#	this method to be reimplemented by child class for custom searches
		entity = {}
		entity['id'] = result['id']
		entity['body'] = result['body'][0]
		entity['title'] = result['title'][0]
		entity['author'] = result['author'][0]
		entity['RunBook_URL'] = result['RunBook_URL'][0]
		return entity


	def search_by_preferred_method(self, question):
	#	this method may be reimplemented by child class for custom searches
		return self.search_randr(question)

	
def search_randr(message_context):
	question = message_context.get_last_utterance()
	search_container = runBookSearchContainer()
	search_container.set_randr_config(config.SOLR_CLUSTER_ID, config.SOLR_COLLECTION_NAME, config.RANKER_ID, config.RANDR_SEARCH_ARGS)
	response = search_container.search(question)
	service_results = response
	return service_results

