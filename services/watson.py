import os, requests, json, logging
from helpers import config
from watson_developer_cloud import AuthorizationV1 as Authorization
from watson_developer_cloud import SpeechToTextV1 as SpeechToText
from watson_developer_cloud import TextToSpeechV1 as TextToSpeech

# ------------------------------------------------
# GLOBAL VARIABLES -------------------------------
# ------------------------------------------------
CONVERSATION_WORKSPACE_ID = config.CONVERSATION_WORKSPACE_ID
CONVERSATION_VERSION = config.CONVERSATION_VERSION
CONVERSATION_USERNAME = config.CONVERSATION_USERNAME
CONVERSATION_PASSWORD = config.CONVERSATION_PASSWORD
TTS_USERNAME = config.TTS_USERNAME
TTS_PASSWORD = config.TTS_PASSWORD
STT_USERNAME = config.STT_USERNAME
STT_PASSWORD = config.STT_PASSWORD
RETRIEVE_AND_RANK_USERNAME = config.RETRIEVE_AND_RANK_USERNAME
RETRIEVE_AND_RANK_PASSWORD = config.RETRIEVE_AND_RANK_PASSWORD
ALCHEMY_API_APIKEY = config.ALCHEMY_API_APIKEY
DISCOVERY_USERNAME = config.DISCOVERY_USERNAME
DISCOVERY_PASSWORD = config.DISCOVERY_PASSWORD


#####
# Overwrites by env variables
#####
if 'CONVERSATION_WORKSPACE_ID' in os.environ:
	CONVERSATION_WORKSPACE_ID = os.environ['CONVERSATION_WORKSPACE_ID']
if 'CONVERSATION_VERSION' in os.environ:
	CONVERSATION_VERSION = os.environ['CONVERSATION_VERSION']
if 'CASTIRON_USERNAME' in os.environ:
	CASTIRON_USERNAME = os.environ['CASTIRON_USERNAME']
if 'CASTIRON_PASSWORD' in os.environ:
	CASTIRON_PASSWORD = os.environ['CASTIRON_PASSWORD']
if 'CIRON_URL_CREATE_CASE' in os.environ:
	CIRON_URL_CREATE_CASE = os.environ['CIRON_URL_CREATE_CASE']
if 'CIRON_URL_ACTIVATION' in os.environ:
	CIRON_URL_ACTIVATION = os.environ['CIRON_URL_ACTIVATION']
if 'CIRON_URL_GET_SERIAL' in os.environ:
	CIRON_URL_GET_SERIAL = os.environ['CIRON_URL_GET_SERIAL']
if 'VCAP_SERVICES' in os.environ:
	if len('VCAP_SERVICES') > 0:
		vcap_services = json.loads(os.environ['VCAP_SERVICES'])
		if 'conversation' in vcap_services.keys():
			conversation = vcap_services['conversation'][0]
			CONVERSATION_USERNAME = conversation["credentials"]["username"]
			CONVERSATION_PASSWORD = conversation["credentials"]["password"]
		if 'speech_to_text' in vcap_services.keys():
			stt = vcap_services['speech_to_text'][0]
			STT_USERNAME = stt["credentials"]["username"]
			STT_PASSWORD = stt["credentials"]["password"]
		if 'text_to_speech' in vcap_services.keys():
			tts = vcap_services['text_to_speech'][0]
			TTS_USERNAME = tts["credentials"]["username"]
			TTS_PASSWORD = tts["credentials"]["password"]
		if 'retrieve_and_rank' in vcap_services.keys():
			retrieve_and_rank = vcap_services['retrieve_and_rank'][0]
			RETRIEVE_AND_RANK_USERNAME = retrieve_and_rank["credentials"]["username"]
			RETRIEVE_AND_RANK_PASSWORD = retrieve_and_rank["credentials"]["password"]
		if 'alchemy_api' in vcap_services.keys():
			alchemy_api = vcap_services['alchemy_api'][0]
			ALCHEMY_API_APIKEY = alchemy_api["credentials"]["apikey"]
		if 'discovery' in vcap_services.keys():
			discovery = vcap_services['discovery'][0]
			DISCOVERY_USERNAME = discovery["credentials"]["username"]
			DISCOVERY_PASSWORD = discovery["credentials"]["password"]

# ------------------------------------------------
# FUNCTIONS --------------------------------------
# ------------------------------------------------
def format_discovery_query_string(wks_entities):
	wks_entity_query_strings = []

	for wks_query_entity in config.WKS_QUERY_ENTITIES.split(','):
		if wks_query_entity in wks_entities:
			wks_entity_query_strings.append('%28enriched_text.entities.type%3A' + wks_query_entity + '%2Cenriched_text.entities.text%3A' +  wks_entities[wks_query_entity] + '%29')
	
	discovery_query_string = ''
	if len(wks_entity_query_strings) >= 1:
		discovery_query_string = wks_entity_query_strings[0]
	if len(wks_entity_query_strings) > 1:
		discovery_query_string = '%28' + discovery_query_string
		for i in range(1, len(wks_entity_query_strings)):
			discovery_query_string = discovery_query_string + ',' + wks_entity_query_strings[i]
		discovery_query_string = discovery_query_string + '%29'
	
	return discovery_query_string

	
#Speech to Text and Text to Speech Services
def BMIX_get_stt_token():
	token = ''
	try:
		global STT_USERNAME, STT_PASSWORD
		token = Authorization(username=STT_USERNAME, password=STT_PASSWORD).get_token(url=SpeechToText.default_url)

	except Exception as e:
		logging.debug("*** In get_stt_token - EXCEPTION.  e is:")
		logging.debug(e)

	return token

	
def BMIX_get_tts_token():
	token = ''
	try:
		global TTS_USERNAME, TTS_PASSWORD
		token = Authorization(username=TTS_USERNAME, password=TTS_PASSWORD).get_token(url=TextToSpeech.default_url)

	except Exception as e:
		logging.debug("*** In get_tts_token - EXCEPTION.  e is:")
		logging.debug(e)

	return token

	
#Conversation Service	
def BMIX_converse(input_message):
	local_message = input_message
	try:
		POST_SUCCESS = 200

		global CONVERSATION_WORKSPACE_ID, CONVERSATION_USERNAME, CONVERSATION_PASSWORD, CONVERSATION_VERSION
		url = 'https://gateway.watsonplatform.net/conversation/api/v1/workspaces/' + CONVERSATION_WORKSPACE_ID + '/message?version=' + CONVERSATION_VERSION
		authinfo = (CONVERSATION_USERNAME, CONVERSATION_PASSWORD)
		headerinfo = {'content-type': 'application/json'}

		r = requests.post(url, auth=authinfo, headers=headerinfo, data=local_message.get_msg_json())

		if r.status_code == POST_SUCCESS:
			dict_msg = r.json()
			logging.debug("*** In converse - success.  Response dict is:")
			logging.debug(dict_msg)
			local_message.put_dict_msg_updates(dict_msg)
		
	except Exception as e:
		logging.debug("*** In converse - EXCEPTION.  e is:")
		logging.debug(e)

	return local_message


#Alchemy API
def BMIX_call_alchemy_api(request, parameters):
	response = {}
	try:
		POST_SUCCESS = 200
		
		global ALCHEMY_API_APIKEY
		parameters['apikey'] = ALCHEMY_API_APIKEY
		parameters['outputMode'] = 'json'
		url = 'https://gateway-a.watsonplatform.net/calls' + request

		r = requests.post(url, data=parameters)
		
		if r.status_code == POST_SUCCESS:
			response = r.json()
			
	except Exception as e:
		logging.debug("*** In alchemy_api - EXCEPTION.  e is:")
		logging.debug(e)

	return response
	

#Retrieve and Rank service
def BMIX_retrieve_and_rank(question, SOLR_CLUSTER_ID, SOLR_COLLECTION_NAME, RANKER_ID, RANDR_SEARCH_ARGS):
	docs = []
	try:
		POST_SUCCESS = 200

		question = str(question).decode('ascii', 'ignore')
		url = 'https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/' + SOLR_CLUSTER_ID + '/solr/' + SOLR_COLLECTION_NAME + '/fcselect?ranker_id=' + RANKER_ID + '&q=' + question + '&wt=json&fl=' + RANDR_SEARCH_ARGS

		global RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD
		r = requests.get(url, auth=(RETRIEVE_AND_RANK_USERNAME, RETRIEVE_AND_RANK_PASSWORD), headers={'content-type': 'application/json; charset=utf8'})

		if r.status_code == POST_SUCCESS:
			docs = r.json()['response']['docs']
			logging.debug("*** In retrieve and rank - success.  Response docs is ")
			logging.debug(docs)

	except Exception as e:
		logging.debug("*** In retrieve_and_rank - EXCEPTION.  e is:")
		logging.debug(e)

	return docs


#Discovery service
def BMIX_discovery(question, wks_entities, DISCOVERY_ENVIRONMENT, DISCOVERY_COLLECTION, WKS_ANNOTATOR_MODEL_ID_DISCOVERY):
	docs = []
	try:
		POST_SUCCESS = 200

		product = ''
		product_release = ''
		if 'Product' in wks_entities:
			product = wks_entities['Product']
		if 'Product_Release' in wks_entities:
			product_release = wks_entities['Product_Release']

		question = str(question).decode('ascii', 'ignore')
		discovery_query_string = format_discovery_query_string(wks_entities)
		url = 'https://gateway.watsonplatform.net/discovery/api/v1/environments/' + DISCOVERY_ENVIRONMENT + '/collections/' + DISCOVERY_COLLECTION + '/query?version=2016-11-07&query=' + discovery_query_string + '&count=&offset=&aggregation=&filter=&return='

		print('----------------------')
		print('--BMIX_discovery()')
		print(discovery_query_string)
		print(url)
		#url = 'https://gateway.watsonplatform.net/discovery/api/v1/environments/' + DISCOVERY_ENVIRONMENT + '/collections/' + DISCOVERY_COLLECTION + '/query?version=2016-11-07&query=((enriched_text.entities.type:product,enriched_text.entities.text:' +  product + '),(enriched_text.entities.type:product_release,enriched_text.entities.text:' +  product_release + '))&count=&offset=&aggregation=&filter=text:install*&return='

		global DISCOVERY_USERNAME, DISCOVERY_PASSWORD
		r = requests.get(url, auth=(DISCOVERY_USERNAME, DISCOVERY_PASSWORD), headers={'content-type': 'application/json; charset=utf8'})

		if r.status_code == POST_SUCCESS:
			print(r.json()['matching_results'])
			docs = r.json()['results']
			logging.debug("*** In discovery - success.  Response docs is ")
			logging.debug(docs)

	except Exception as e:
		logging.debug("*** In discovery - EXCEPTION.  e is:")
		logging.debug(e)

	return docs

