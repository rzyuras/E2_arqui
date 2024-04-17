from paho.mqtt import client as mqtt
import json
import requests

url = 'http://app:3000/flights'

class MQTTClient:
    def __init__(self, broker, port, user, password):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.host = broker
        self.port = port
        self.user = user
        self.password = password
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

        client.subscribe("flights/info")

    def on_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode('utf-8'))[0]
            flights = json.loads(data['flights'])
            emissions = json.loads(data['carbonEmission'])
            dic = {
                "price": int(data['price']),
                "currency": data['currency'],
                "carbon_emissions": int(emissions['this_flight']),
                "airline_logo_url": data['airlineLogo'],
                "departure_airport_name": flights[0]['departure_airport']['name'],
                "departure_airport_id": flights[0]['departure_airport']['id'],
                "departure_airport_time": flights[0]['departure_airport']['time'],
                "arrival_airport_name": flights[0]['arrival_airport']['name'],
                "arrival_airport_id": flights[0]['arrival_airport']['id'],
                "arrival_airport_time": flights[0]['arrival_airport']['time'],
                "duration": int(flights[0]['duration']),
                "airplane": flights[0]['airplane'],
                "airline": flights[0]['airline'],
                "airline_logo": flights[0]['airline_logo']
            }
            response = requests.post(url, json=dic)
            print(response.json())
            print("Message processed and saved successfully")
            
        except Exception as e:
            print(f"An error ocurred saving or processing the message: {e}")

        
    def connect(self):
        self.client.username_pw_set(self.user, self.password)
        self.client.connect(self.host, self.port)
        self.client.loop_forever()



# Datos de conexión MQTT
mqtt_broker = 'broker.iic2173.org'
mqtt_port = 9000
mqtt_user = 'students'
mqtt_password = 'iic2173-2024-1-students'

# Crear instancia de MQTTClient con los datos directamente
mqtt_client = MQTTClient(mqtt_broker, mqtt_port, mqtt_user, mqtt_password)

# Conectar al broker MQTT
mqtt_client.connect()


