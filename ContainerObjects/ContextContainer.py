import json, logging

class ContextContainer:
	origin = None
	cust_id = None
	Address_Type = None
	Last_Name = None
	Group = None
	castiron_response = None
	caseStatus = None
	topic = None
	response_input = None
	Follow_Up_Request = None
	Overactivation_Reason = None
	Email = None
	subject = None
	subOrigin = None
	system = None
	comments = None
	type = None
	Phone_Number = None
	Address_Line_1 = None
	Address_Line_2 = None
	City = None
	State = None
	Zip = None
	Sub_Area = None
	productKey = None
	Field_Order = None
	conversation_id = None
	Description = None
	First_Name = None
	Case_Area = None
	systemName = None
	Request_Code = None
	Product_Key = None
	Product_Name = None
	SCCMEmail = None
	Product_Year = None
	Serial = None
	Country = None
	Existing_Issue = None
	__appendVars = None
	__lastUtterance = None


	def __init__(self):
		self.__appendVars = []
		self.__privateVars = ['First_Name', 'Last_Name', 'Address_Line_1', 'Address_Line_2', 'City', 'State', 'Zip', 'Email', 'Phone_Number']

		
	def put_json_context_updates(self, json_context):
		dict_context = json.loads(json_context)
		self.put_dict_context_updates(dict_context)

		
	def put_dict_context_updates(self, dict_context):
		for key in dict_context:
			if not hasattr(self, key):
				logging.debug("Found new attribute for context with key/val: " +  key + "/" + str(dict_context[key]))
				self.__appendVars.append(key)
			setattr(self, key, dict_context[key])

			
	def put_context_from_form(self, form):
		self.put_dict_context_updates(form)

		
	def get_context_dict(self):
		dict_context = {}
		for key in self.__dict__:
			dict_context[key] = getattr(self, key)
		return dict_context

		
	def get_context_json(self):
		return json.dumps(self.get_context_dict())
		
		
	def dv(self, key):
		if key in self.__dict__:
			if getattr(self, key) != None:
				return getattr(self, key)
		return ''


	def put_last_utterance(self, question):
		self.__lastUtterance = question
		
		
	def get_last_utterance(self):
		return self.__lastUtterance
		
		
	def hide_private_values(self):
		for private_variable in self.__privateVars:
			if getattr(self, private_variable, None) != None:
				delattr(self, private_variable)
				logging.debug("Dropping private variable from context with key: " +  private_variable)
		
		