import json, logging
from helpers import session_mgr
from ContainerObjects.ContextContainer import ContextContainer

class MessageContainer:
	input = None
	context = None
	entities = None
	intents = None
	alternate_intents = None
	output = None

	
	def __init__(self):
		# self.input = {}
		self.context = ContextContainer()
		# self.entities = []
		# self.intents = []
		# self.alternate_intents = []
		# self.output = {}

		
	def __getattribute__(self, name):
		logging.debug("getattr fired")
		if name == 'context':
			return self.context.get_context_dict()
		return self.__getattribute__(name)


	def put_json_msg_updates(self, json_msg):
		dict_msg = json.loads(json_msg)
		self.put_dict_msg_updates(dict_msg)


	def put_dict_msg_updates(self, dict_msg):
		for key in dict_msg:
			if key == 'context':
				self.context.put_dict_context_updates(dict_msg[key])
			else:
				setattr(self, key, dict_msg[key])
			logging.debug("attribute set: " + key)


	def get_msg_dict(self):
		dict_msg = {}
		for key in self.__dict__:
			if key == 'context':
				dict_msg[key] = self.context.get_context_dict()
			else:
				dict_msg[key] = getattr(self, key)
		return dict_msg


	def get_msg_json(self):
		return json.dumps(self.get_msg_dict())


	def get_output_text(self):
		logging.debug("In get_output_text - object is: " + str(self))
		logging.debug("Self output is: " + str(self.output))
	#	"formatted_text" is the default response if, for whatever reason, a valid answer is not returned from Conversation service
	#	-- could externalize in properties, but also
	#	-- may revisit error handling, to receive contextual messages about errors, unavailability etc.
		formatted_text = 'Sorry, but I did not get a response from the chat-bot. Try again if you like or you can request to transfer to a live agent.'
		if self.output:
			logging.debug("self output found")
			if 'text' in self.output:
				logging.debug("text found in output")
				formatted_text = ''
				response_text = self.output['text']
				for response_line in response_text:
					if str(response_line) != '':
						if len(formatted_text) > 0:
							formatted_text = formatted_text + ' ' + response_line
						else:
							formatted_text = response_line

		return formatted_text


	def update_message(self, question, update_context):
		logging.debug("firing object update message")
		self.input = {'text': question}
		#Resetting output text is neccesitated by changed behavior in new conversation service
		if self.output:
			if 'text' in self.output:
				self.output['text'] = []
		previous_message = MessageContainer().get_msg_from_session()
		if previous_message.has_context():
			# verify - may need to overload copy on object
			self.context = previous_message.context
		self.context.put_dict_context_updates(update_context.get_context_dict())
		self.context.put_last_utterance(question)

		return self


	def has_context(self):
		if self.context.conversation_id is not None:
			return True
		else:
			return False


	def get_msg_from_session(self):
		from flask import session
		session_mgr.session_info_dump(session)
		self.put_dict_msg_updates(session_mgr.get('MESSAGE', '{}'))
		return self


	def message_info_dump(self):
		temp_message_item = self.get_msg_dict()
		for key, value in sorted(temp_message_item.items()):
			logging.debug("Message key: " + key)
			logging.debug("Contains: " + str(value))
		logging.debug("End of message dump")

		
	def get_input_text(self, default):
		text = default
		if self.input is not None:
			if self.input['text'] is not None:
				text = self.input['text']
		return text

