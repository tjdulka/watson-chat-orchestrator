import os, requests, json, logging
from helpers import config

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------
def retrieve_crm_address(message_context):
	customer_identifiers = extract_customer_identifiers(message_context)
	response = BMIX_get_current_adress(customer_identifiers['cust_id'], customer_identifiers['email'])
	service_results = get_service_results_from_customer_profile(response, message_context.Address_Type)
	return service_results

	
def extract_customer_identifiers(message_context):
	customer_identifiers = {}
	customer_identifiers['cust_id'] = message_context.dv('cust_id')
	#Note the inconsistency in attr name. Called one thing by in Context def, something else in CRM system
	customer_identifiers['email'] = message_context.dv('Email')
	return customer_identifiers

	
def BMIX_get_current_adress(cust_id, email):
	response = {}
	try:
		POST_SUCCESS = 200

		url = 'http://wow-crm-plus-1.mybluemix.net/profile?cust_id=' + cust_id + '&cust_email=' + email
		r = requests.get(url, headers={'content-type': 'application/json', 'accept': 'application/json'})

		if r.status_code == POST_SUCCESS:
			response['Payload'] = r.json()
			logging.debug("*** In retrieve_current_adress - success.  Response dict is " + str(response))
			logging.debug("*** In retrieve_current_adress - success.  Response dict is ")
			logging.debug(response)
			response['Status_Message'] = 'Success'
			response['Status_Code'] = POST_SUCCESS
		else:
			response['Status_Message'] = 'BMIX_get_current_adress service call failed with return code: [' + str(r.status_code) + ']'
			response['Status_Code'] = r.status_code
			
	except Exception as e:
		logging.debug("*** In get_current_adress - EXCEPTION.  e is:")
		logging.debug(e)
		response['Status_Message'] = 'An exception occured in the get_current_adress service call. Check the log file.'
		response['Status_Code'] = -999

	return response
	

def get_service_results_from_customer_profile(response, address_type):
	service_results = {}
	if 'Payload' in response:
		customer_profile = response['Payload']
		if address_type == config.BILLING_ADDRESS_TYPE:
			service_results['Address_Line_1'] = customer_profile['billing_address']['address_line_1']
			service_results['Address_Line_2'] = customer_profile['billing_address']['address_line_2']
			service_results['City'] = customer_profile['billing_address']['city']
			service_results['State'] = customer_profile['billing_address']['state']
			service_results['Zip'] = customer_profile['billing_address']['zip']
			service_results['Address_Type'] = config.BILLING_ADDRESS_TYPE
		elif address_type == config.MAILING_ADDRESS_TYPE:
			service_results['Address_Line_1'] = customer_profile['mailing_address']['address_line_1']
			service_results['Address_Line_2'] = customer_profile['mailing_address']['address_line_2']
			service_results['City'] = customer_profile['mailing_address']['city']
			service_results['State'] = customer_profile['mailing_address']['state']
			service_results['Zip'] = customer_profile['mailing_address']['zip']
			service_results['Address_Type'] = config.MAILING_ADDRESS_TYPE
	else:
		service_results = response
	return service_results


#	functions supporting update_crm_address
def update_crm_address(message_context):
	customer_profile = extract_customer_profile(message_context)
	response = BMIX_update_current_adress(customer_profile)
	service_results = response
	return service_results

	
def extract_customer_profile(message_context):
	customer_profile = {}
	customer_profile['cust_id']= message_context.dv('cust_id')
	customer_profile['Email'] = message_context.dv('Email')
	customer_profile['Address_Type'] = message_context.dv('Address_Type')
	address_type = 'billing_address'
	if message_context.dv('Address_Type') == config.MAILING_ADDRESS_TYPE:
		address_type = 'mailing_address'
	customer_profile[address_type] = {}
	customer_profile[address_type]['address_line_1'] = message_context.dv('Address_Line_1')
	customer_profile[address_type]['address_line_2'] = message_context.dv('Address_Line_2')
	customer_profile[address_type]['city'] = message_context.dv('City')
	customer_profile[address_type]['state'] = message_context.dv('State')
	customer_profile[address_type]['zip'] = message_context.dv('Zip')
	return customer_profile


def BMIX_update_current_adress(customer_profile):
	response = {}
	try:
		POST_SUCCESS = 200

		url = 'http://wow-crm-plus-1.mybluemix.net/sync?cust_id=' + customer_profile['cust_id'] + '&cust_email=' + customer_profile['Email'] + '&address_type=' + customer_profile['Address_Type']
		r = requests.post(url, headers={'content-type': 'application/json', 'accept': 'application/json'}, data=json.dumps(customer_profile))

		if r.status_code == POST_SUCCESS:
			logging.debug("*** In update_current_adress - success.  Response dict is " + str(response))
			logging.debug("*** In update_current_adress - success.  Response dict is ")
			logging.debug(response)
			response['Status_Message'] = 'Success'
			response['Status_Code'] = POST_SUCCESS
		else:
			response['Status_Message'] = 'BMIX_update_current_adress service call failed with return code: [' + str(r.status_code) + ']'
			response['Status_Code'] = r.status_code
			
	except Exception as e:
		logging.debug("*** In update_current_adress - EXCEPTION.  e is:")
		logging.debug(e)
		response['Status_Message'] = 'An exception occured in the update_current_adress service call. Check the log file.'
		response['Status_Code'] = -999

	return response
	
