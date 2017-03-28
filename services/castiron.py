import requests, json, os, logging
from helpers import config

CASTIRON_USERNAME = config.CASTIRON_USERNAME
CASTIRON_PASSWORD = config.CASTIRON_PASSWORD
CASTIRON_PASSWORD = config.CASTIRON_PASSWORD
CIRON_URL_CREATE_CASE = config.CIRON_URL_CREATE_CASE

#####
# Overwrites by env variables
#####
if 'CASTIRON_USERNAME' in os.environ:
	CASTIRON_USERNAME = os.environ['CASTIRON_USERNAME']
if 'CASTIRON_PASSWORD' in os.environ:
	CASTIRON_PASSWORD = os.environ['CASTIRON_PASSWORD']
if 'CIRON_URL_CREATE_CASE' in os.environ:
	CIRON_URL_CREATE_CASE = os.environ['CIRON_URL_CREATE_CASE']

def CIRON_create_case(data):
	response = {}
	try:
		POST_SUCCESS = 200
		global CIRON_URL_CREATE_CASE, CASTIRON_USERNAME, CASTIRON_PASSWORD
		logging.debug('---CIRON_create_caseX')
		# ugly hack pt 1 to reconcile dev/stage and prod castiron
		response['Status_Message'] = None #prod
		response['success'] = False # stage/dev
		response['Message'] = None # prod
		response['errorMessage'] = 'The service request to the backend systems was not successful. Please try again.' # stage/dev
		response['Case_Number'] = None # prod
		response['caseNumber'] = '' # stage/dev
		url = CIRON_URL_CREATE_CASE
		logging.debug('attempting to make castiron create case request')
		logging.debug('CASTIRON USER is' + CASTIRON_USERNAME)
		logging.debug('CASTIRON password is' + CASTIRON_PASSWORD)
		logging.debug('Data is ' + data)
		logging.debug('url is ' + url)
		r = requests.post(url, auth=(CASTIRON_USERNAME, CASTIRON_PASSWORD), data=data)
		logging.debug('---r.status_code')
		logging.debug(r.status_code)
		print('----------------------')
		print('--CIRON_create_case()')
		if r.status_code == POST_SUCCESS:
			response = r.json()
			print(response)
			# ugly hack to reconcile dev/stage and prod castiron
			if 'Status_Message' in response:
				response['success'] = bool(response['Status_Message'])
			if 'Message' in response:
				response['errorMessage'] = response['Message']
			if 'Case_Number' in response:
				response['caseNumber'] = response['Case_Number']
			logging.debug('---r.content')
			logging.debug(r.content)
			logging.debug('---response')
			logging.debug(response)
		else:
			response['Status_Message'] = 'Cast Iron service call failed with return code: [' + str(r.status_code) + ']'
			print(r.status_code)

	except Exception as e:
		logging.debug("*** In create_case - EXCEPTION.  e is:")
		logging.debug(e)
		response['Status_Message'] = 'An exception occured in the create_case service call. Check the log file.'

	return response
	
