from helpers import session_mgr, post_formatter

# Everything in here to help reformat the case call for CastIron
# Can be converted to use a context object, or have the context object do
# some of this work if worthwhile

def case_remapper_for_castiron(context_dict):
	case = {}
	for key in context_dict:
		#Some exceptions to harmonize field values and cast iron names until reconciled
		if key == 'First_Name':
			case['fname'] = context_dict[key]
		elif key == 'Last_Name':
			case['lname'] = context_dict[key]
		else:
			case[key] = context_dict[key]
	chat_vars = format_chat_vars(context_dict)
	post_history = post_formatter.format_post_history(session_mgr.get('POSTS', []))
	if 'Description' in context_dict:
		if context_dict['Description'] is None or context_dict['Description'] == '':
			case['Description'] = chat_vars + post_history
		else:
			case['Description'] = chat_vars + 'Customer Comments: \\n ' + context_dict.get('Description', '') + ' \\n ' +  post_history
	return case


def format_chat_vars(context):
	# 'Header'
	chat_vars = ' CHAT VARIABLES \\n '
	# required vars from form
	first_name = context.get('First_Name', '')
	last_name = context.get('Last_Name', '')
	email = context.get('Email', '')
	phone_number = context.get('Phone_Number', '')
	chat_vars = chat_vars + \
				'Requestor First Name: ' + first_name + \
				' Requestor Last Name: ' + last_name + \
				' Requestor Email: ' + email + \
				' Requestor Phone Number: ' + phone_number + '\\n'

	# sorted vars from context
	field_order_list = get_field_order_list(context.get('Field_Order', ''))
	sorted_vars = sort_vars(context, field_order_list)
	chat_vars = chat_vars + sorted_vars
	return chat_vars


def get_field_order_list(field_order):
	field_order.replace(" ", "")
	field_order_list = field_order.split(",")
	return field_order_list


def sort_vars(context, field_order_list):
	# global EXCLUDED_VARS
	sorted_vars = ''
	for field in field_order_list:
		value = context.get(str(field.lstrip()), '')
		# if not (value is None or value == '') and not value in EXCLUDED_VARS:
		if not (value is None or value == ''):
			sorted_vars = sorted_vars + str(field) + ': ' + value + ' '
	return sorted_vars.strip() + '\\n'