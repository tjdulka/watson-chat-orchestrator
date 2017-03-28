import os, json, logging, sys
from helpers import config
from services.CustomService import CustomService
from services import watson
from ContainerObjects.ContextContainer import ContextContainer
from ContainerObjects.ResolutionContainer import ResolutionContainer
from ContainerObjects.ResolutionContainer import CHAT_TEMPLATE
from ContainerObjects.ResolutionContainer import QUESTION_INPUT
from beaker.middleware import SessionMiddleware
from flask import Flask, request, render_template, session
from flask.sessions import SessionInterface
from helpers import session_mgr

# Logging config
loglevel = logging.getLevelName(config.LOGGING_LEVEL)
logpath = config.PROJECT_ROOT + "/" + config.LOGGING_LOCATION
logformat = config.LOGGING_FORMAT

if config.LOGGING_LOCATION == "Bluemix": 
	logpath = "DEFAULT BLUEMIX LOCATION"
 	logging.basicConfig(level=loglevel, format=logformat)
	logging.info("Logging on Bluemix")

else:
	logging.basicConfig(filename=logpath, level=loglevel, format=logformat)
	
logging.info("Logging initialized with level " + logging.getLevelName(loglevel) + " to " + logpath + " with FORMAT=\"" + logformat + "\"")
print("Logging initialized with level " + logging.getLevelName(loglevel) + " to " + logpath + " with FORMAT=\"" + logformat + "\"")

logging.debug(os.environ)

#  Session config
session_opts = {
	# 'session.type': 'ext:memcached',
	# 'session.url': 'localhost:11211',
	'session.data_dir': '/tmp/cache',
	'session.cookie_expires': 'true',
	'session.type': 'file',
	'session.auto': 'true'
}

class BeakerSessionInterface(SessionInterface):
	def open_session(self, app, request):
		session = request.environ['beaker.session']
		return session

	def save_session(self, app, session, response):
		session.save()


#	Security tokens for Watson speech services
#STT_TOKEN = watson.BMIX_get_stt_token()
#TTS_TOKEN = watson.BMIX_get_tts_token()

#  Flask app objct & endpoints
app = Flask(__name__)

@app.route('/')
def Index():
	logging.debug("in Index -- root get method")

#	Initialize session
	session_mgr.initialize_session()

	#global STT_TOKEN, TTS_TOKEN
	session_mgr.set('STT_TOKEN', watson.BMIX_get_stt_token())
	session_mgr.set('TTS_TOKEN', watson.BMIX_get_tts_token())
	session_mgr.session_info_dump(session)

#	Get initial chat greeting
	resolution_container = ResolutionContainer()
	resolution_container.converse()

#	Display chat greeting
	session_mgr.post_watson_response(resolution_container.message.get_output_text())
	
#	Log message	
	logging.debug("Message is : " + str(resolution_container.message))

#	Render page
	return render_template(CHAT_TEMPLATE,
						   posts=session_mgr.get('POSTS', []),
						   form='',
						   stt_token=session_mgr.get('STT_TOKEN', watson.BMIX_get_stt_token()),
						   tts_token=session_mgr.get('TTS_TOKEN', watson.BMIX_get_tts_token()))


@app.route('/', methods=['POST'])
def Index_Post():
	logging.debug("in Index_Post -- root post method")

#	Capture and display user question
	local_question = request.form[QUESTION_INPUT]
	session_mgr.post_user_input(local_question)

#	Get chat response
	resolution_container = ResolutionContainer()
	resolution_container.orchestrate(local_question, ContextContainer())

#	Display chat response
	session_mgr.post_watson_response(resolution_container.chat)

#	Log message	and session
	logging.debug("Message is : ")
	logging.debug(session['MESSAGE'])
	logging.debug("Session is : ")
	logging.debug(session)
	
#	Render page
	#global STT_TOKEN, TTS_TOKEN
	return render_template(CHAT_TEMPLATE,
						   config=config,
						   posts=session_mgr.get('POSTS', []),
						   form=resolution_container.form,
						   context=resolution_container.message.context,
						   stt_token=session_mgr.get('STT_TOKEN', watson.BMIX_get_stt_token()),
						   tts_token=session_mgr.get('TTS_TOKEN', watson.BMIX_get_tts_token()))

						   
@app.route('/converse', methods=['POST'])
def Converse_Post():
	logging.debug("in Converse_Post -- service interface (conversation message input and output)")

#	If conversation_id not explicitly passed, reset session
	input_message = json.loads(request.data)
	if 'context' not in input_message:
		session_mgr.initialize_session()
	elif 'conversation_id' not in input_message['context']:
		session_mgr.initialize_session()

#	Create message from post data -- should be in the form of a conversation message. Extract input text.
	resolution_container = ResolutionContainer()
	resolution_container.message.put_json_msg_updates(request.data)
	local_question = resolution_container.message.get_input_text(default='')

#	Get chat response
	resolution_container.orchestrate(local_question, ContextContainer())

#	Display chat response - Not applicable in service call
	#session_mgr.post_watson_response(resolution_container.chat)

#	Log message	and session
	logging.debug("Message is : ")
	logging.debug(session['MESSAGE'])
	logging.debug("Session is : ")
	logging.debug(session)
	
	return resolution_container.message.get_msg_json()


@app.route('/custom', methods=['POST'])
def Custom_Post():
	logging.debug("in Custom_Post -- external endpoint to invoke CustomServices")

#	Get data from post -- should be include "custom_service_name" and "custom_service_dict"
	custom_service_invocation = json.loads(request.data)
	custom_service_name = custom_service_invocation['custom_service_name']
	custom_service_dict = custom_service_invocation['custom_service_dict']

#	Init context object
	custom_service_context = ContextContainer()
	custom_service_context.put_dict_context_updates(custom_service_dict)

#	Call custom service
	custom_service = CustomService()
	service_results = custom_service.invoke_custom_service(custom_service_name, custom_service_context)

#	Log CustomService and service_results
	logging.debug("CustomService is : ")
	logging.debug(custom_service)
	logging.debug("service_results is: ")
	logging.debug(service_results)

	return json.dumps(service_results)


@app.route('/form', methods=['POST'])
def Form_Post():
	logging.debug("in Form_Post -- endpoint to process forms")

#	Capture form values
	form_context = ContextContainer()
	form_context.put_dict_context_updates(request.form)

#	Get chat response
	resolution_container = ResolutionContainer()
	resolution_container.message.update_message(question='', update_context=form_context)
	
#	Call CustomService if needed
	if 'form_type' in request.args:
		custom_service = CustomService()
		service_results = custom_service.invoke_custom_service(request.args['form_type'], resolution_container.message.context)
		resolution_container.message.context.put_dict_context_updates(service_results)

#	Get conversational response
	resolution_container.converse()
	resolution_container.resolve()

#	Display chat response
	session_mgr.post_watson_response(resolution_container.chat)

#	Log message	and session
	logging.debug("Message is : ")
	logging.debug(session['MESSAGE'])
	logging.debug("Session is : ")
	logging.debug(session)

#	Render page
	#global STT_TOKEN, TTS_TOKEN
	return render_template(CHAT_TEMPLATE,
						   posts=session_mgr.get('POSTS', []),
						   form=resolution_container.form,
						   context=resolution_container.message.context,
						   stt_token=session_mgr.get('STT_TOKEN', watson.BMIX_get_stt_token()),
						   tts_token=session_mgr.get('TTS_TOKEN', watson.BMIX_get_tts_token()))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # for gunicorn


if __name__ == "__main__":
	app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
	app.session_interface = BeakerSessionInterface()
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	#app.run(host=config.SERVER_IP_LISTENER, port=int(config.SERVER_PORT_LISTENER), threaded=True)		
	app.run(host=config.SERVER_IP_LISTENER, port=int(config.SERVER_PORT_LISTENER))		
	app.run()

	