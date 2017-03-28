import datetime, os, logging
from flask import session
from helpers import config

PERSONA_NAME = config.PERSONA_NAME
PERSONA_IMAGE = config.PERSONA_IMAGE
PERSONA_STYLE = config.PERSONA_STYLE
WATSON_NAME = config.WATSON_NAME
WATSON_IMAGE = config.WATSON_IMAGE
WATSON_STYLE = config.WATSON_STYLE

if 'PERSONA_NAME' in os.environ:
	PERSONA_NAME = os.environ['PERSONA_NAME']
if 'PERSONA_IMAGE' in os.environ:
	PERSONA_IMAGE = os.environ['PERSONA_IMAGE']
if 'PERSONA_STYLE' in os.environ:
	PERSONA_STYLE = os.environ['PERSONA_STYLE']
if 'WATSON_NAME' in os.environ:
	WATSON_NAME = os.environ['WATSON_NAME']
if 'WATSON_IMAGE' in os.environ:
	WATSON_IMAGE = os.environ['WATSON_IMAGE']
if 'WATSON_STYLE' in os.environ:
	WATSON_STYLE = os.environ['WATSON_STYLE']

# Session var set and get funcs ------------------
def set(key, value):
	session[key] = value
	return session[key]


def get(key, default_value):
	if not key in session.keys():
		session[key] = default_value
	return session[key]


# Session update functions
def initialize_session():
	set('POSTS', [])
	set('MESSAGE', {})


def create_session_post(style, icon, text, datetime, name):
	post = {}
	post['style'] = style
	post['icon'] = icon
	post['text'] = text
	post['datetime'] = datetime
	post['name'] = name
	return post


def post_watson_response(response):
	global WATSON_STYLE, WATSON_IMAGE, WATSON_NAME
	now = datetime.datetime.now()
	post = create_session_post(WATSON_STYLE, WATSON_IMAGE, response, now.strftime('%Y-%m-%d %H:%M'), WATSON_NAME)
	get('POSTS', []).append(post)
	return post


def post_user_input(input):
	global PERSONA_STYLE, PERSONA_IMAGE, PERSONA_NAME
	now = datetime.datetime.now()
	post = create_session_post(PERSONA_STYLE, PERSONA_IMAGE, input, now.strftime('%Y-%m-%d %H:%M'), PERSONA_NAME)
	get('POSTS', []).append(post)
	return post


def flush_msg_to_session(message_obj):
	set('MESSAGE', message_obj.get_msg_dict())


def session_info_dump(session_obj):
	for key, value in sorted(session_obj.items()):
		logging.debug("Session key: " + str(key))
		logging.debug("Contains: " + str(value))
	logging.debug("End of session dump")
