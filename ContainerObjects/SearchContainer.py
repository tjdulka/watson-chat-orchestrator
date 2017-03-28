import json, logging
from services import watson

SUCCESS = 200
NO_CONTENT = 204


class SearchContainer:
	search_results = None
	entities = None
	SOLR_CLUSTER_ID = None
	SOLR_COLLECTION_NAME = None
	RANKER_ID = None
	RANDR_SEARCH_ARGS = None
	DISCOVERY_ENVIRONMENT = None
	DISCOVERY_COLLECTION = None
	WKS_ANNOTATOR_MODEL_ID_DISCOVERY = None
	WKS_ENTITIES = None

	
	def __init__(self):
		self.reset_search_results()

		
	def reset_search_results(self):
		self.search_results = []
		self.entities = []


	def set_randr_config(self, SOLR_CLUSTER_ID, SOLR_COLLECTION_NAME, RANKER_ID, RANDR_SEARCH_ARGS):
		self.SOLR_CLUSTER_ID = SOLR_CLUSTER_ID
		self.SOLR_COLLECTION_NAME = SOLR_COLLECTION_NAME
		self.RANKER_ID = RANKER_ID
		self.RANDR_SEARCH_ARGS = RANDR_SEARCH_ARGS
	
	
	def set_discovery_config(self, DISCOVERY_ENVIRONMENT, DISCOVERY_COLLECTION, WKS_ANNOTATOR_MODEL_ID_DISCOVERY, WKS_ENTITIES):
		self.DISCOVERY_ENVIRONMENT = DISCOVERY_ENVIRONMENT
		self.DISCOVERY_COLLECTION = DISCOVERY_COLLECTION
		self.WKS_ANNOTATOR_MODEL_ID_DISCOVERY = WKS_ANNOTATOR_MODEL_ID_DISCOVERY
		self.WKS_ENTITIES = WKS_ENTITIES
	
	
	def populate_entities(self):
		for result in self.search_results:
			entity = self.populate_entity_from_search_result(result)
			self.entities.append(entity)


	def populate_entity_from_search_result(self, result):
	#	this method to be reimplemented by child class for custom searches
		entity = {}
		return entity

		
	def search_randr(self, question):
		self.search_results = watson.BMIX_retrieve_and_rank(question, self.SOLR_CLUSTER_ID, self.SOLR_COLLECTION_NAME, self.RANKER_ID, self.RANDR_SEARCH_ARGS)

		
	def search_discovery(self, question):
		self.search_results = watson.BMIX_discovery(question, self.WKS_ENTITIES, self.DISCOVERY_ENVIRONMENT, self.DISCOVERY_COLLECTION, self.WKS_ANNOTATOR_MODEL_ID_DISCOVERY)

		
	def search_by_preferred_method(self, question):
	#	this method may be reimplemented by child class for custom searches
		return self.search_randr(question)

		
	def search(self, question):
		response = {}

		self.search_by_preferred_method(question)
		self.populate_entities()

		global SUCCESS, NO_CONTENT
		if len(self.entities):
		#	A populated entities list confirms success, an empty list could be an error/or there may be no results for quesry
		#	-- may revisit error handling, to receive contextual messages about errors, unavailability etc.
			logging.debug("*** In search - success.  SearchContainer.entities list is " + str(self.entities))
			logging.debug("*** In search - success.  SearchContainer.entities list is ")
			logging.debug(self.entities)
			
			response['Payload'] = self.entities
			response['Status_Message'] = 'Success'
			response['Status_Code'] = SUCCESS

		else:
			response['Status_Message'] = 'No content'
			response['Status_Code'] = NO_CONTENT
			
		return response
	
