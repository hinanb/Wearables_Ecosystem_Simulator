from django.shortcuts import render
from django.http import HttpResponse
from .models import Wearable, Sensor, Sensor_Values
from django.http import HttpResponse

import paho.mqtt.client as mqtt
import time
import json
import ast




def on_message(client, userdata, message):
    my_dict = json.loads(message.payload.decode("utf-8") ) 
    #print(my_dict['sensorValue'])
    wearableId=my_dict['wearableId']
    sensor_value=ast.literal_eval(my_dict['sensorValue'])
    sensorName=my_dict['sensorName']
    timeStamp=my_dict['timeStamp']

    if Wearable.objects.get(user_name=wearableId).exists()==False:
         wearable_obj=Wearable.objects.create(user_name=wearableId)
    else:
        wearable_obj=Wearable.objects.get(user_name=wearableId)

    if Sensor.objects.get(name=sensorName).exists() == False:
        sensor_obj=Sensor.objects.create(name=wearableId, wearable=wearable_obj)
    else:
        sensor_obj=Sensor.objects.get(name=sensorName)

    Sensor_Values.objects.create(wearable= wearable_obj, sensor=sensor_obj, value=my_dict['sensorValue'], timeStamp=my_dict['timeStamp'] )


    print(my_dict)
    


    

mqttBroker ="mqtt.eclipseprojects.io"

client = mqtt.Client("Smartphone")
client.connect("broker.emqx.io", 1883, 60)

client.subscribe("Wearabllll")
client.on_message=on_message 

time.sleep(30)
client.loop_stop()