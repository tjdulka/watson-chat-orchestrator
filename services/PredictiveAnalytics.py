import os, requests, json, logging
from helpers import config

# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
PREDICTIVE_ANALYTICS_CONTEXT_ID = config.PREDICTIVE_ANALYTICS_CONTEXT_ID
PREDICTIVE_ANALYTICS_ACCESS_KEY = config.PREDICTIVE_ANALYTICS_ACCESS_KEY

#####
# Overwrites by env variables
#####
if 'PREDICTIVE_ANALYTICS_CONTEXT_ID' in os.environ:
	PREDICTIVE_ANALYTICS_CONTEXT_ID = os.environ['PREDICTIVE_ANALYTICS_CONTEXT_ID']
if 'VCAP_SERVICES' in os.environ:
	if len('VCAP_SERVICES') > 0:
		vcap_services = json.loads(os.environ['VCAP_SERVICES'])
		if 'pm-20' in vcap_services.keys():
			pm_20 = vcap_services['pm-20'][0]
			PREDICTIVE_ANALYTICS_ACCESS_KEY = pm_20["credentials"]["access_key"]

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------
def evaluate_predictive_model(message_context):
	model = extract_predictive_model(message_context)
	response = BMIX_evaluate_predictive_model(model)
	service_results = get_service_results_from_predictive_model(response)
	return service_results

	
def extract_predictive_model(message_context):
	model = {}
	if message_context.predictive_model is not None:
		model = message_context.predictive_model
	return model

	
def BMIX_evaluate_predictive_model(model):
	response = {}
	try:
		POST_SUCCESS = 200

		global PREDICTIVE_ANALYTICS_ACCESS_KEY, PREDICTIVE_ANALYTICS_CONTEXT_ID
		url = 'https://palbyp.pmservice.ibmcloud.com/pm/v1/' + PREDICTIVE_ANALYTICS_CONTEXT_ID + '?accesskey=' + PREDICTIVE_ANALYTICS_ACCESS_KEY
		r = requests.post(url, headers={'content-type': 'application/json', 'accept': 'application/json'}, data=json.dumps(model))

		if r.status_code == POST_SUCCESS:
			response['Payload'] = r.json()
			logging.debug("*** In evaluate_predictive_model - success.  Response dict is " + str(response))
			logging.debug("*** In evaluate_predictive_model - success.  Response dict is ")
			logging.debug(response)
			response['Status_Message'] = 'Success'
			response['Status_Code'] = POST_SUCCESS
		else:
			response['Status_Message'] = 'Predictive Analytics service call failed with return code: [' + str(r.status_code) + ']'
			response['Status_Code'] = r.status_code

	except Exception as e:
		logging.debug("*** In evaluate_predictive_model - EXCEPTION.  e is:")
		logging.debug(e)
		response['Status_Message'] = 'An exception occured in the Predictive Analytics service call. Check the log file.'
		response['Status_Code'] = -999

	return response
	

def get_service_results_from_predictive_model(response):
	service_results = {}
	if 'Payload' in response:
		entity = response['Payload']
		if type(entity) is list:
			campaign = entity[0]
			attr_names = campaign['header']
			attr_values = campaign['data'][0]
			i = 0
			for attr_name in attr_names:
				service_results[attr_name.replace('$', '').replace(' ', '_').replace('-', '_')] = attr_values[i]
				i += 1
		elif type(entity) is dict:
			for key in entity:
				service_results[key] = entity[key]
	else:
		service_results = response
	return service_results

