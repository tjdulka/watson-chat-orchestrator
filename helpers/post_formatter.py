def format_post_history(posts):
	post_history = ''
	for post in posts:
		#If condition to discount posts with JS code to call chat service | should not be needed
		#if "window._laq" not in post['text']:
		text = post['text'].rstrip()
		name = post['name']
		post_history = post_history + '[##' + name.upper() + '##] \\n ' + text + ' \\n '
	##Escaping all necessary JSON charachters
	post_history = post_history.replace('<br>', '')
	post_history = post_history.replace('</a>', "")
	post_history = post_history.replace('/', '\\/')
	post_history = post_history.replace('"', "'")
	post_history = post_history.replace('\r', "\\r")
	post_history = post_history.replace('\n', "\\n")
	post_history = post_history.replace("<a href='#' class='buttonText'>", "")
	post_history = post_history.replace('class=buttonText', "")
	return post_history