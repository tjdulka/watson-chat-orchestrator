import os
import ConfigParser
from flask import current_app as app
            
APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

config = ConfigParser.RawConfigParser()
config.read(os.path.join(PROJECT_ROOT, 'config.properties'))

# MISC Section
SERVER_IP_LISTENER                      =config.get('MISC', 'SERVER_IP_LISTENER')
if 'VCAP_APP_HOST' in os.environ: SERVER_IP_LISTENER = os.environ['VCAP_APP_HOST']
SERVER_PORT_LISTENER                    =config.get('MISC', 'SERVER_PORT_LISTENER')
if 'PORT' in os.environ: SERVER_PORT_LISTENER = os.environ['PORT'] #port = os.getenv('PORT', '5000')
GUNICORN_SECRET_KEY                     =config.get('MISC', 'GUNICORN_SECRET_KEY')

# WATSON Section
PERSONA_NAME                            =config.get('WATSON', 'PERSONA_NAME')
PERSONA_IMAGE                           =config.get('WATSON', 'PERSONA_IMAGE')
PERSONA_STYLE                           =config.get('WATSON', 'PERSONA_STYLE')
WATSON_NAME                             =config.get('WATSON', 'WATSON_NAME')
WATSON_IMAGE                            =config.get('WATSON', 'WATSON_IMAGE')
WATSON_STYLE                            =config.get('WATSON', 'WATSON_STYLE')
CHAT_TEMPLATE                           =config.get('WATSON', 'CHAT_TEMPLATE')
QUESTION_INPUT                          =config.get('WATSON', 'QUESTION_INPUT')
CONVERSATION_WORKSPACE_ID               =config.get('WATSON', 'CONVERSATION_WORKSPACE_ID')
CONVERSATION_VERSION                    =config.get('WATSON', 'CONVERSATION_VERSION')
CONVERSATION_USERNAME                   =config.get('WATSON', 'CONVERSATION_USERNAME')
CONVERSATION_PASSWORD                   =config.get('WATSON', 'CONVERSATION_PASSWORD')
CURSOR_INPUT                            =config.get('WATSON', 'CURSOR_INPUT')
FORM_INPUT                              =config.get('WATSON', 'FORM_INPUT')
SEARCH_TYPE_INPUT                       =config.get('WATSON', 'SEARCH_TYPE_INPUT')
SEARCH_VALUE_INPUT                      =config.get('WATSON', 'SEARCH_VALUE_INPUT')
TTS_USERNAME                            =config.get('WATSON', 'TTS_USERNAME')
TTS_PASSWORD                            =config.get('WATSON', 'TTS_PASSWORD')
STT_USERNAME                            =config.get('WATSON', 'STT_USERNAME')
STT_PASSWORD                            =config.get('WATSON', 'STT_PASSWORD')
SOLR_CLUSTER_ID                         =config.get('WATSON', 'SOLR_CLUSTER_ID')
SOLR_COLLECTION_NAME                    =config.get('WATSON', 'SOLR_COLLECTION_NAME')
RANKER_ID                               =config.get('WATSON', 'RANKER_ID')
RANDR_SEARCH_ARGS                       =config.get('WATSON', 'RANDR_SEARCH_ARGS')
RETRIEVE_AND_RANK_USERNAME              =config.get('WATSON', 'RETRIEVE_AND_RANK_USERNAME')
RETRIEVE_AND_RANK_PASSWORD              =config.get('WATSON', 'RETRIEVE_AND_RANK_PASSWORD')
WKS_ANNOTATOR_MODEL_ID                  =config.get('WATSON', 'WKS_ANNOTATOR_MODEL_ID')
ALCHEMY_API_APIKEY                      =config.get('WATSON', 'ALCHEMY_API_APIKEY')
DISCOVERY_USERNAME                      =config.get('WATSON', 'DISCOVERY_USERNAME')
DISCOVERY_PASSWORD                      =config.get('WATSON', 'DISCOVERY_PASSWORD')
DISCOVERY_ENVIRONMENT                   =config.get('WATSON', 'DISCOVERY_ENVIRONMENT')
DISCOVERY_COLLECTION                    =config.get('WATSON', 'DISCOVERY_COLLECTION')
WKS_ANNOTATOR_MODEL_ID_DISCOVERY        =config.get('WATSON', 'WKS_ANNOTATOR_MODEL_ID_DISCOVERY')
WKS_QUERY_ENTITIES                      =config.get('WATSON', 'WKS_QUERY_ENTITIES')


# CRM Section
RETRIEVE_CURRENT_ADDRESS_REQUEST        =config.get('CRM', 'RETRIEVE_CURRENT_ADDRESS_REQUEST')
UPDATE_CURRENT_ADDRESS_REQUEST          =config.get('CRM', 'UPDATE_CURRENT_ADDRESS_REQUEST')
BILLING_ADDRESS_TYPE                    =config.get('CRM', 'BILLING_ADDRESS_TYPE')
MAILING_ADDRESS_TYPE                    =config.get('CRM', 'MAILING_ADDRESS_TYPE')

# PREDICTIVE_ANALYTICS Section
PREDICTIVE_ANALYTICS_ACCESS_KEY         =config.get('PREDICTIVE_ANALYTICS', 'PREDICTIVE_ANALYTICS_ACCESS_KEY')
PREDICTIVE_ANALYTICS_CONTEXT_ID         =config.get('PREDICTIVE_ANALYTICS', 'PREDICTIVE_ANALYTICS_CONTEXT_ID')

#CAST IRON Section
CASTIRON_USERNAME                       =config.get('CAST_IRON', 'CASTIRON_USERNAME')
CASTIRON_PASSWORD                       =config.get('CAST_IRON', 'CASTIRON_PASSWORD')
CIRON_URL_CREATE_CASE                   =config.get('CAST_IRON', 'CIRON_URL_CREATE_CASE')

#Tokens Section
SUCCESS                                 =config.get('TOKENS', 'SUCCESS')
CASE_CREATE_SUCCESS                     =config.get('TOKENS', 'CASE_CREATE_SUCCESS')
BLANK_VALUE                             =config.get('TOKENS', 'BLANK_VALUE')
ERROR_FLAG_MSG                          =config.get('TOKENS', 'ERROR_FLAG_MSG')
FORM_FLAG_MSG                           =config.get('TOKENS', 'FORM_FLAG_MSG')
ACTIVATION_FORM_MSG                     =config.get('TOKENS', 'ACTIVATION_FORM_MSG')
CASE_FORM_MSG                           =config.get('TOKENS', 'CASE_FORM_MSG')
HELLO_HANDOFF_MSG                       =config.get('TOKENS', 'HELLO_HANDOFF_MSG')
ACTIVATION_SUCCESS_MSG                  =config.get('TOKENS', 'ACTIVATION_SUCCESS_MSG')
CASE_SUCCESS_MSG                        =config.get('TOKENS', 'CASE_SUCCESS_MSG')
GET_7_FIELDS_FORM_MSG                   =config.get('TOKENS', 'GET_7_FIELDS_FORM_MSG')
GET_OVERACTIVATION_REASON_FORM_MSG      =config.get('TOKENS', 'GET_OVERACTIVATION_REASON_FORM_MSG')
LIVE_AGENT_REQUEST                      =config.get('TOKENS', 'LIVE_AGENT_REQUEST')
GENERIC_VALS                            =config.get('TOKENS', 'GENERIC_VALS')
CHAT_TRANSFER                           =config.get('TOKENS', 'CHAT_TRANSFER')
OPEN_CASE_REQUEST                       =config.get('TOKENS', 'OPEN_CASE_REQUEST')
REQUEST_A_CODE_REQUEST                  =config.get('TOKENS', 'REQUEST_A_CODE_REQUEST')
GET_EMAIL_ERROR_MSG                     =config.get('TOKENS', 'GET_EMAIL_ERROR_MSG')
NO_PREV_ELIGIBILITY                     =config.get('TOKENS', 'NO_PREV_ELIGIBILITY')
CUSTOMER_ACTIVATION                     =config.get('TOKENS', 'CUSTOMER_ACTIVATION')
CHAT_SUBMIT                             =config.get('TOKENS', 'CHAT_SUBMIT')
SEARCH_WITH_RANDR                       =config.get('TOKENS', 'SEARCH_WITH_RANDR')
SEARCH_WITH_WEX                         =config.get('TOKENS', 'SEARCH_WITH_WEX')
EVALUATE_PREDICTIVE_MODEL               =config.get('TOKENS', 'EVALUATE_PREDICTIVE_MODEL')
INVOKE_CUSTOM_SERVICE                   =config.get('TOKENS', 'INVOKE_CUSTOM_SERVICE')
PRESENT_FORM                            =config.get('TOKENS', 'PRESENT_FORM')
WKS_ENTITIES                            =config.get('TOKENS', 'WKS_ENTITIES')

#Form Types Section
OPEN_CASE_FORM_TYPE                     =config.get('FORM_TYPES', 'OPEN_CASE_FORM_TYPE')
REQUEST_A_CODE_FORM_TYPE                =config.get('FORM_TYPES', 'REQUEST_A_CODE_FORM_TYPE')
OVERACTIVATE_FORM_TYPE                  =config.get('FORM_TYPES', 'OVERACTIVATE_FORM_TYPE')

# Data Files Section
OVERACTIVATION_REASON_OPTIONS_POPULATED =config.get('DATA_FILES', 'OVERACTIVATION_REASON_OPTIONS_POPULATED')
PRODUCT_NAME_OPTIONS_POPULATED          =config.get('DATA_FILES', 'PRODUCT_NAME_OPTIONS_POPULATED')
PRODUCT_YEAR_OPTIONS_POPULATED          =config.get('DATA_FILES', 'PRODUCT_YEAR_OPTIONS_POPULATED')
SCCM_OPTIONS_POPULATED                  =config.get('DATA_FILES', 'SCCM_OPTIONS_POPULATED')
HASH_FILE                               =config.get('DATA_FILES', 'HASH_FILE')
  
# Logger Configurations
LOGGING_FORMAT                          =config.get('LOGGING', 'LOGGING_FORMAT')
LOGGING_LOCATION                        =config.get('LOGGING', 'LOGGING_LOCATION')
LOGGING_LEVEL                           =config.get('LOGGING', 'LOGGING_LEVEL')
if 'VCAP_APP_HOST' in os.environ: LOGGING_LOCATION = "Bluemix" # if on Bluemix

# Live agent
LIVE_AGENT_URL                          =config.get('LIVE_AGENT', 'LIVE_AGENT_URL')
if 'LIVE_AGENT_URL' in os.environ: LIVE_AGENT_URL = os.environ['LIVE_AGENT_URL']              
LIVE_AGENT_PARAM1                       =config.get('LIVE_AGENT', 'LIVE_AGENT_PARAM1')
if 'LIVE_AGENT_PARAM1' in os.environ: LIVE_AGENT_PARAM1 = os.environ['LIVE_AGENT_PARAM1']  
LIVE_AGENT_PARAM2                       =config.get('LIVE_AGENT', 'LIVE_AGENT_PARAM2')
if 'LIVE_AGENT_PARAM2' in os.environ: LIVE_AGENT_PARAM2 = os.environ['LIVE_AGENT_PARAM2']        
LIVE_AGENT_BUTTONID                     =config.get('LIVE_AGENT', 'LIVE_AGENT_BUTTONID')
if 'LIVE_AGENT_BUTTONID' in os.environ: LIVE_AGENT_BUTTONID = os.environ['LIVE_AGENT_BUTTONID']
