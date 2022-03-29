from django.shortcuts import render
from django.http import HttpResponse
from .models import Wearable, Sensor, Sensor_Values, Configuration

import paho.mqtt.client as mqtt
import time
import json
import ast

import math
from random import gauss
import datetime
import pandas as pd
import paho.mqtt.client as mqtt
import time
import json
import threading
import numpy as np
from django.urls import reverse
from django.http import HttpResponse
import random

import os
import psutil

# Create your views here.

def create_Dataset():
    # HR per min
    mean_list_asc = [70, 73, 76, 75, 73, 80, 78, 77, 75, 76]
    mean_list_desc = [95, 90, 92, 88, 87, 85, 79, 78, 79, 77]

    my_variance = 1

    listOfListsHR = []

    counter = 0
    list_of_counter = []
    for my_mean in mean_list_asc + mean_list_desc:
        random_numbers = [gauss(my_mean, math.sqrt(my_variance)) for i in range(150)]

        for count in range(150):
            counter = counter + count
            list_of_counter.append(counter)

        listOfListsHR.extend(random_numbers)

    #plt.plot(list_of_counter, listOfListsHR)

    # temperature

    mean_list_asc = [97.7, 98.0, 98.5, 98.9, 98.6, 98.7, 98.7, 98.8, 98.9, 98.99]
    mean_list_desc = [99.0, 98.5, 98.0, 97.7, 97.8, 97.95, 97.99, 97.8, 97.82, 97.81]

    my_variance = 1

    listOfListsTemp = []

    counter = 0
    list_of_counter = []
    for my_mean in mean_list_asc + mean_list_desc:
        random_numbers = [gauss(my_mean, math.sqrt(my_variance)) for i in range(150)]

        for count in range(150):
            counter = counter + count
            list_of_counter.append(counter)

        listOfListsTemp.extend(random_numbers)

    #plt.plot(list_of_counter, listOfListsTemp)

    # HRV
    mean_list_asc = [70, 73, 76, 75, 73, 80, 78, 77, 75, 76]
    mean_list_desc = [95, 90, 92, 88, 87, 85, 79, 78, 79, 77]

    my_variance = 1

    listOfListsHRV = []

    counter = 0
    list_of_counter = []
    for my_mean in mean_list_asc + mean_list_desc:
        random_numbers = [gauss(my_mean, math.sqrt(my_variance)) for i in range(150)]

        for count in range(150):
            counter = counter + count
            list_of_counter.append(counter)

        listOfListsHRV.extend(random_numbers)

    #plt.plot(list_of_counter, listOfListsHRV)

    # convert to dataset

    data = {'wearableId': ['1'], 'sensorName': 'HR',
            'timeStamp': [datetime.datetime.now()],
            'sensorValue': [84]}

    # create dataframe
    df = pd.DataFrame(data)


    # add

    for index in range(len(listOfListsHRV)):
        new_row_HR = {'wearableId': '1', 'sensorName': 'HR', 'timeStamp': datetime.datetime.now(),
                      'sensorValue': str(listOfListsHR[index])}
        new_row_Temperature = {'wearableId': '1', 'sensorName': 'Temerature', 'timeStamp': datetime.datetime.now(),
                               'sensorValue': str(listOfListsTemp[index])}
        new_row_HRV = {'wearableId': '1', 'sensorName': 'HRV', 'timeStamp': datetime.datetime.now(),
                       'sensorValue': str(listOfListsTemp[index])}

        # append row to the dataframe
        df = df.append(new_row_HR, ignore_index=True)
        df = df.append(new_row_Temperature, ignore_index=True)
        df = df.append(new_row_HRV, ignore_index=True)

    # steps per day
    steps_per_day = random.randint(2000, 9000)
    new_row_steps = {'wearableId': '1', 'sensorName': 'steps', 'timeStamp': datetime.datetime.now(),
                   'sensorValue': str(steps_per_day)}

    df = df.append(new_row_steps, ignore_index=True)

    return df





def setNumberOfWearables(df, wearablesvar):
    numberOfWearables = None
    numberOfWearables = wearablesvar

    df['wearableId'] = np.random.randint(1, int(numberOfWearables) + 1, df.shape[0])

    return df


def normalise_row(row, sensorFrequency):
    return sensorFrequency[row['sensorName']]


def setFrequencyOfSensors(df, sensorFrequency):
    df["sleepBeforePublishing"] = 1
    df['sleepBeforePublishing'] = df.apply(lambda row: normalise_row(row, sensorFrequency), axis=1)
    return df


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def send_batch(batch, client, df):
    #all_sensors=df.sensorName.unique()
    #Sensors_caught_in_batches={}

    #if all_sensors==:

    try:
        input1 = json.dumps(batch)
        client.publish('Wearabllll', payload=input1)
        #print(input1)
        #print(os.getpid())
    except:
        print('failed sending')

    #print(input1)


# sensor multithread for each client
def sensor_publish(df, sensor_name, client, BatchFrequency):
    sensor_filterd_data = df[df['sensorName'] == sensor_name]

    batch = []

    wearable_id_var=None
    for index, row in sensor_filterd_data.iterrows():
        NumberOfPacketsToSendInBatch =int(BatchFrequency)/int(row['sleepBeforePublishing'])


        batch.append( {'wearableId': row['wearableId'], 'timeStamp': str(datetime.datetime.now()),
                             'sensorName': row['sensorName'], 'sensorValue': row['sensorValue']})
        #list of dict


        time.sleep(int(row['sleepBeforePublishing']))

        if len(batch)==int(NumberOfPacketsToSendInBatch):
            send_batch(batch, client, df)
            batch=[]

        wearable_id_var= row['wearableId']
        #input1 = json.dumps({'wearableId': row['wearableId'], 'timeStamp': str(datetime.datetime.now()),
         #                    'sensorName': row['sensorName'], 'sensorValue': row['sensorValue']})
        #client.publish('Wearabllll', payload=input1)

    # steps per day
    steps_per_day = random.randint(2000, 9000)

    batch.append({'wearableId': row['wearableId'], 'timeStamp': str(datetime.datetime.now()),
                  'sensorName': 'steps', 'sensorValue': str(steps_per_day)})
    send_batch(batch, client, df)
    batch = []


# multithreaded each wearable functionality
def publish_each_wearable_data(df, wearable_id, client, BatchFrequency):
    each_wearable_df = df[df['wearableId'] == wearable_id]

    sensor_thread_list = []
    for sensor_name in each_wearable_df.sensorName.unique():
        thread = threading.Thread(target=sensor_publish, args=(each_wearable_df, sensor_name, client,BatchFrequency, ))
        sensor_thread_list.append(thread)

    for thread in sensor_thread_list:
        thread.start()

    for thread in sensor_thread_list:
        thread.join()

def index(request):
    template_name = 'fetch/MainPage.html'
    
    wearablesvar = request.GET.get('wearables')
    HRFrequencyvar = request.GET.get('HRFrequency')
    TemperatureFrequencyvar = request.GET.get('TemperatureFrequency')
    HRVFrequencyvar = request.GET.get('HRVFrequency')
    BatchFrequencyvar= request.GET.get('Batch_Frequency')


    try:
        config_obj = Configuration(numberOfWearables=int(wearablesvar), HRVFrequency=int(HRFrequencyvar),
                          HRFrequency= int(TemperatureFrequencyvar), TemperatureFrequency=int(HRVFrequencyvar),
                                   BatchFrequency= int(BatchFrequencyvar))

        config_obj.save()
    except:
        pass
    
    return render(request, 'fetch/MainPage.html')
    #return redirect(reverse('publish-home', kwargs={'wearablesvar': wearablesvar, 'HRFrequencyvar':HRFrequencyvar, 'TemperatureFrequencyvar':TemperatureFrequencyvar
                                                         # ,'HRVFrequencyvar':HRVFrequencyvar }))




def index__(request):
    #deleting all the running simulations as we will be starting off with new simulation

    #process_pid = os.getpid()
    #p = psutil.Process(process_pid)
    #p.terminate()


    # simulator dataset


    client = mqtt.Client('Heart Rate_Device1')
    client.on_connect = on_connect
    client.connect("broker.emqx.io", 1883, 60)

    df = create_Dataset()
    
    sensorFrequency = {}
    conf_obj = Configuration.objects.last()
    sensorFrequency['HR'] = conf_obj.HRFrequency
    sensorFrequency['HRV'] = conf_obj.HRVFrequency
    sensorFrequency['Temerature'] = conf_obj.TemperatureFrequency
    sensorFrequency['steps'] = 1
    time.sleep(5)
    print(conf_obj)

    Batch_Frequency=conf_obj.BatchFrequency
    wearablesvar= conf_obj.numberOfWearables

    print('this')
    print(sensorFrequency)
    time.sleep(5)

    df = setNumberOfWearables(df, wearablesvar)


    # get user input for each sensor frequency




    #for sensor_name in df.sensorName.unique():
     #   sensorFrequency[sensor_name] = input("Enter duration of frequency of : " + sensor_name + 'sensor')
        # sensorFrequency[sensor_name] =simpledialog.askstring(title="Simulator",
        #                        prompt="Insert Frequency of "+sensor_name)

    df = setFrequencyOfSensors(df, sensorFrequency)

    thread_list = []
    for wearable_id in df.wearableId.unique():
        t1 = threading.Thread(target=publish_each_wearable_data, args=(df, wearable_id,client,Batch_Frequency ))
        thread_list.append(t1)

    print(thread_list)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    return HttpResponse('<h1>Publishing Data </h1>')


