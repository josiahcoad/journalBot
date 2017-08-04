# created by Josiah Coad and Noah Coad on 2017-08-03

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

@route('/')
def index():
	return '<b>Welcome user</b>!'

@route('/hitme/<phone>')
def register(phone):
	message = client.messages.create(to="+12088192625", from_=from_, body="Hello from Python!")
	return template('<b>Saying Hello to {{phone}}</b> w SID {{sid}}!', phone=phone, sid=message.sid)

# http://neo.coad.net:8092/twilio/incoming_sms
@route('/twilio/incoming_sms', method='POST')
def incoming_sms():
	fields = {x:request.forms.get(x) for x in ['Body', 'From']}
	print(fields)
	return "thank you"

@route('/capture/json', method='POST')
def capture():
	with template.TemporaryFile(mode='w', suffix='.json', dir='captures') as f:
		f.write(request.json)

# run(host='localhost', port=8092)
run(host='0.0.0.0', port=8092, reloader=True)
