# created by Josiah Coad and Noah Coad on 2017-08-03

# pip3 install bottle pymongo twilio

# mongo commands
# mongo ds117093.mlab.com:17093/journalbot -u jbot -p hackcity
# db.checkins.find()

# example how to forward a port from a remote maching to this one
# ssh -R 8092:localhost:8092 digger:bubblejuice@neo.coad.net

from twilio.rest import Client
from bottle import route, run, template, post, request
from pymongo import MongoClient

# J's live creds
twilio_account_sid = "AC7b3d8053222eb828ab629df9cecf6ee1"
twilio_auth_token  = "fda89d5d104147ee51138242906a4065"
twilio_from = "+12086238429" # from Josiah acct

# connect to database
dbcon = "mongodb://jbot:hackcity@ds117093.mlab.com:17093/journalbot"
db = MongoClient(dbcon).get_default_database()

# connect to twilio
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# user commands
txtcmds = {
	"log": lambda x: ", ".join([x['body'] for x in x['db'].checkins.find({'from': x['msg']['From']}, {'body': 1, '_id': 0})]),
	"secret": lambda x: "you are the master hacker. I bow before you.",
	"help": lambda x: "commands: log, <something else, wahaha>"
}

@route('/')
def index():
	return '<b>Welcome user</b>!'

# send user a txt msg
@route('/hitme/<phone>')
def register(phone):
	message = twilio_client.messages.create(to="+1%s" % phone, from_=twilio_from, body="One word. How are you feeling?")
	return template("<b>Asking how you're doing at {{phone}}</b> w SID {{sid}}!", phone=phone, sid=message.sid)

# recieve user's txt msgs
# http://neo.coad.net:8092/twilio/incoming_sms
@route('/twilio/incoming_sms', method='POST')
def incoming_sms():
	msg = {x:request.forms.get(x) for x in ['Body', 'From']}
	if msg['Body'][4:] in txtcmds.keys():
		response = txtcmds[msg['Body'][4:]]({'db': db, 'msg': msg})
		if response: message = twilio_client.messages.create(to=msg['From'], from_=twilio_from, body=response)
	else:
		db.checkins.insert({'from': msg['From'], 'body': msg['Body']})
		message = twilio_client.messages.create(to=msg['From'], from_=twilio_from, body="Thanks.  I've logged it.")
	print("Incoming txt: %s" % msg)

run(host='0.0.0.0', port=8092, reloader=True)
