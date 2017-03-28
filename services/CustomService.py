import json, logging
from services import PredictiveAnalytics, crm, search_randr, search_discovery, castiron
from helpers import config, castiron_mapper

class CustomService:
	service_results = None

	def __init__(self):
		self.service_results = {}

	def invoke_custom_service(self, custom_service_name, message_context):
		try:
			custom_service = getattr(self, custom_service_name)
		except AttributeError:
			return {}
		else:
			self.service_results = custom_service(message_context)
			return self.service_results

#--	IMPLEMENT METHOD FOR EACH CUST SERVICE USING THIS CONTRACT
#--	1 param (message_context), returns 'service_results' a dict
#--------------------------------------------------------------
	def search_discovery(self, message_context):
		logging.debug("search_discovery fired")
		service_results = search_discovery.search_discovery(message_context)
		return service_results


	def search_randr(self, message_context):
		logging.debug("search_randr fired")
		service_results = search_randr.search_randr(message_context)
		return service_results


	def evaluate_predictive_model(self, message_context):
		logging.debug("evaluate_predictive_model fired")
		service_results = PredictiveAnalytics.evaluate_predictive_model(message_context)
		return service_results


	def retrieve_crm_address(self, message_context):
		logging.debug("retrieve_crm_address fired")
		service_results = {}
		request_form = message_context.get_context_dict()
		if request_form[config.QUESTION_INPUT] == config.RETRIEVE_CURRENT_ADDRESS_REQUEST:
			logging.debug('--request_form dict right before "retrieve_crm_address" call to CRM')
			logging.debug(request_form)
			service_results = crm.retrieve_crm_address(message_context)
		return service_results

		
	def update_crm_address(self, message_context):
		logging.debug("update_crm_address fired")
		service_results = {}
		request_form = message_context.get_context_dict()
		if request_form[config.QUESTION_INPUT] == config.UPDATE_CURRENT_ADDRESS_REQUEST:
			logging.debug('--request_form dict right before "update_crm_address" call to CRM')
			logging.debug(request_form)
			service_results = crm.update_crm_address(message_context)
		return service_results

		
	def open_case(self, message_context):
		logging.debug("open_case fired")
		service_results = {}
		request_form = message_context.get_context_dict()
		if request_form[config.QUESTION_INPUT] == config.OPEN_CASE_REQUEST:
			case = castiron_mapper.case_remapper_for_castiron(request_form)
			logging.debug('--case object right before "Create a Case" call to Cast Iron')
			logging.debug(case)
			service_results['castiron_response'] = castiron.CIRON_create_case(json.dumps(case, separators=(',',':')))
		return service_results

