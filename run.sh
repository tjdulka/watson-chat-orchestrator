export CASTIRON_PASSWORD=adskotto
export CASTIRON_USERNAME=otto_development@autodesk.com

export CONVERSATION_WORKSPACE_ID='a72f8f3b-ef51-4086-a6bb-6bc453ea38f2'
export CONVERSATION_VERSION='2016-07-11'
export CONVERSATION_USERNAME='e28a8b8e-8ea0-45ae-b5e7-6832216c6d77'
export CONVERSATION_PASSWORD='nBaSsF4eRqxH'

gunicorn -p gunicorn.pid -b dev-otto.autodesk.com -w 4 welcome:app
