import paho.mqtt.client as mqtt #import the library
import time
import datetime
from influxdb import InfluxDBClient
from flask import Flask, request, json
from flask_restful import Resource, Api
import subprocess
import requests

# Set up a client for InfluxDB
# dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'sensordata')


def on_message(client, userdata, message):
    print("Light value sensor received: " + str(message.payload)) #print incoming messages

    # DB related
    # topic = message.topic
    # #write value to db
    # receiveTime = datetime.datetime.utcnow()
    # message=message.payload
    # val = float(message)
    # json_body = [
    #     {
    #         "measurement": topic,
    #         "time": receiveTime,
    #         "fields": {"value": val }
    #     }
    # ]
    # dbclient.write_points(json_body)

broker_address="192.168.1.4"    #broker address (your pis ip address)

client = mqtt.Client() #create new client instance

client.connect(broker_address) #connect to broker

client.on_message=on_message #set the on message function

##client.subscribe("/sLight") #subscribe to topic


#api definition
app = Flask(__name__)
api = Api(app)

#led state
led_state = {'red':0, 'green':0}

class Led(Resource):#define api resource

    def get(self): #get method return led state
        return led_state
    def post(self): #post mmethod change led and update led state
        data = json.loads(request.get_data())
        if data['led'] == 'green':
            if data['state'] == 'off':
                led_state['green'] = 0
                client.publish("/test3" ,"2")
            else:    
                led_state['green'] = 1
                client.publish("/test3" ,"1")
        if data['led'] == 'red':
            if data['state'] == 'off':
                led_state['red'] = 0
                client.publish("/test3" ,"4")
            else:    
                led_state['red'] = 1
                client.publish("/test3" ,"3")


        
        return led_state
api.add_resource(Led, '/led')#add api resource

#main

username = 'panda123'
password = 'asdasd'

#start ngrok as subprocess
ngrok = subprocess.Popen(['./ngrok', 'http', '5000'], stdout = subprocess.PIPE)
#ngrok api
localhost_url = "http://localhost:4040/api/tunnels"
tunnel_url = requests.get(localhost_url).text

j = json.loads(tunnel_url)
#get ngrok url to login server
url = 'http://104.248.57.252:5000/url'
headers = {'conten-type': 'application/json'}
response = requests.post(url, json={"username":username, "password":password, "url": tunnel_url})

client.loop_start() #start client

if __name__ == '__main__': # start api
    app.run(debug=True)






#do something

# while True:
    #if led_state['red'] == 1:
     #   client.publish("/test" ,"1")
         
    #if led_state['red'] == 0:
      #  client.publish("/test" ,"2")
   # time.sleep(10)     
    #if led_state['green'] == '1':
   # client.publish("/test3" ,"1")
         
    #if led_state['green'] == 0:
       # client.publish("/test" ,"2")
         
#     time.sleep(10)
#     #query db for average light value from past 30 secs
#     query = 'select mean("value") from "/sLight" where "time" > now() - 10s'
#     result = dbclient.query(query)
#     #print(result)
#     try:
#         light_avg = list(result.get_points(measurement='/sLight'))[0]['mean']
#         print "Average light value: " + str(light_avg)
#         if light_avg < 200:
#             client.publish("/test","1")
#         elif light_avg >= 200:
#             client.publish("/test","2")
#     except:
#         print 'exception'
#         pass
#
client.loop_stop() #stop client
