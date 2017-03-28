# Imports
import csv

# Global variables
HASH_VALUES = {}

#local
def load_hash_values(app):
	hash_values = {}
	with app.open_resource('artifacts/hash.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			hash_values[row['key']] = row['value']
	return hash_values

	
def substitute_hash_values(chat):
	global HASH_VALUES
	tokens = chat.split()
	for token in tokens:
		if token in HASH_VALUES:
			chat = chat.replace(token, HASH_VALUES[token])
	return chat

