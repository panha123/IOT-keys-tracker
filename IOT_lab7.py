import paho.mqtt.client as mqtt #import the library
import time
import datetime
from flask import Flask, request, json
from flask_restful import Resource, Api
import subprocess
import requests
from twilio.rest import Client

# Set up a client for InfluxDB
# dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'sensordata')

# twilio setting
account_sid = "AC42181481ffbaee9b0072e3264910606e"
auth_token = "14e75d314498f4247ead22e4377f970a"
user = Client(account_sid, auth_token)


def on_message(client, userdata, message):
    print("Key state value sensor received: " + str(message.payload)) #print incoming messages

    temp = int(message.payload)
    if temp == 1:
        message = user.messages \
                    .create(
                         body="Hello from the key finder device!!!",
                         from_='+19783212977',
                         to='+19789350718'
                    )
        print(message.sid)

broker_address="192.168.86.39"    #broker address (your pis ip address)

client = mqtt.Client() #create new client instance

client.connect(broker_address) #connect to broker

client.on_message=on_message #set the on message function

client.subscribe("/test1")

#api definition
app = Flask(__name__)
api = Api(app)

#key state
key_state = {'state':0}

class Key(Resource):#define api resource

    def get(self): #get method return led state
        return key_state
    def post(self): #post mmethod change led and update led state
        data = json.loads(request.get_data())
        if data['state'] == 'off':
            key_state['state'] = 0
            client.publish("/test3" ,"2")
        else:
            key_state['state'] = 1
            client.publish("/test3" ,"1")

        return key_state
api.add_resource(Key, '/key')#add api resource

#main

username = 'panda123'
password = 'asdasd'

#start ngrok as subprocess
ngrok = subprocess.Popen(['./ngrok', 'http', '5000'], stdout = subprocess.PIPE)
#ngrok api
localhost_url = "http://localhost:4040/api/tunnels"
tunnel_url = requests.get(localhost_url).text

j = json.loads(tunnel_url)
#get ngrok url
tunnel_url = j['tunnels'][0]['public_url']
#get ngrok url to login server
url = 'http://104.248.57.252:5000/url'
headers = {'conten-type': 'application/json'}
response = requests.post(url, json={"username":username, "password":password, "url": tunnel_url})

client.loop_start() #start client

if __name__ == '__main__': # start api
    app.run(debug=True)
#do something

while True:
    if key_state['state'] == 1:
        client.publish("/test" ,"1")
client.loop_stop() #stop client
