import paho.mqtt.client as mqttClient
import joblib
import tsfel
import numpy as np
import pandas as pd
import random
import warnings
warnings.filterwarnings("ignore")


cgf_file = tsfel.get_features_by_domain()      #extract TSFEL

topic = input("topic : ")                      #choose topic according to TEP simulation

class main():
    def __init__(self):
        #MQTT connection
        self.broker = "localhost"              #Broker Address
        self.port = 1883                       #Port Broker
        self.client_id = f'python-mqtt-{random.randint(0, 100)}' #Client_id
        self.topic = topic
        self.data = []                         #input data for detection
        self.time = 0                          #initiation time

        self.deteksi_model = joblib.load("deteksi_model")  #SSL KNN-based Model
        self.label_scaler_model = joblib.load("label_scaler_model1")
        #features will be used
        self.fitur_deteksi = ["0_Median absolute diff",
                              "0_Median absolute deviation",
                              "0_Min",
                              "0_Max"]
        self.hasil_deteksi = ""

    #function to connect MQTT
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

    def on_message(self, client, userdata, message):  #function to receive data from Broker
        self.data.append(float(message.payload))      #input data into list
        self.time += 1                                #count number of data
        #start oscillation detection
        if len(self.data) > 150: #when window size = 150
            del self.data[0]
            data_awal = np.array(self.data)
            scaled_result = pd.DataFrame((data_awal - data_awal.mean())/data_awal.std())
            x_t = tsfel.time_series_features_extractor(cgf_file, scaled_result[0], fs=75, verbose=0)
            #features scaling
            X_detect = x_t[self.fitur_deteksi]
            scaled_feature = self.label_scaler_model.transform(X_detect.values)
            scaled_features_df_detect = pd.DataFrame(scaled_feature, index=X_detect.index, columns=X_detect.columns)

            X_pred_detect = scaled_features_df_detect
            y_pred_detect = self.deteksi_model.predict(X_pred_detect)
            #determination detection status
            if y_pred_detect == 0:
                self.hasil_deteksi = "IDV(0)"
            elif y_pred_detect == 1:
                self.hasil_deteksi = "IDV(1)"
            elif y_pred_detect == 2:
                self.hasil_deteksi = "IDV(2)"
            elif y_pred_detect == 3:
                self.hasil_deteksi = "IDV(3)"
            #present result of detection in UI
            print("Time: ", self.time, "   ;  PV:   ", "{:.2f}".format(self.data[-1]), "   ; Detection Status: ", self.hasil_deteksi)
        else: #when window size < 150
            y_pred_detect = 0
            #present result of detection in UI
            print("Time: ", self.time, "   ;  PV:   ", "{:.2f}".format(self.data[-1]), "   ; Detection Status: Detection has not started")
    def run(self): #funtion to subscribe topic
        client = self.connect_mqtt()
        client.subscribe(self.topic, qos=1)
        client.on_message = self.on_message
        client.loop_forever()

if __name__ == "__main__":
    main().run()
