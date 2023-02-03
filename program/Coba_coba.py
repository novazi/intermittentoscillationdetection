import paho.mqtt.client as mqttClient
import joblib
import tsfel
import numpy as np
import pandas as pd
import random
import warnings
import os
warnings.filterwarnings("ignore")

cgf_file = tsfel.get_features_by_domain()

topic = input("topic : ")

class main():
    def __init__(self, topic):
        self.broker = "127.0.0.1"       #Broker untuk TEP
        self.port = 1883
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'
        self.topic1 = topic
        self.topic2 = ["IDV(4)", "IDV(14)", "gain_10"]
        self.data = []
        self.dat = pd.DataFrame()
        self.time = 0
        self.deteksi_model = joblib.load("deteksi_model")
        self.fitur_deteksi = ["0_Median absolute diff",
                              "0_Median absolute deviation",
                              "0_Min",
                              "0_Max"]
        self.hasil_deteksi = ""
        self.data_deteksi = pd.DataFrame(columns=["Time", "PV", "IDV(1)", "IDV(2)", "IDV(3)", "Prediksi"])
        if os.path.isdir(r'hasil deteksi'):
            pass
        else :
            os.mkdir('hasil deteksi')
            
        if os.path.exists('hasil deteksi/data deteksi.csv') :
            pass
        else :
            self.data_deteksi.to_csv('hasil deteksi/data deteksi.csv', index = False)
        
    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Subscriber Connected to MQTT Broker!")
            else:
                    print("Subscriber Failed to connect, return code %d\n", rc)

        global client_id, broker, port
        client = mqttClient.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def on_message(self, client, userdata, message):
        df = float(message.payload)
        self.data.append(df)
        self.time += 1
        print("Time: ", self.time, "   PV: ", "{:.3f}".format(self.data[-1]))
    def run(self):
        client = self.connect_mqtt()
        client.subscribe(self.topic1)
        client.subscribe(self.topic2)
        client.on_message = self.on_message
        client.loop_forever()

if __name__ == "__main__":
    main(topic).run()
