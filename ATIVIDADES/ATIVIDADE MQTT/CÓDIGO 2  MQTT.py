import paho.mqtt.client as mqtt

host_mqtt = "0.tcp.sa.ngrok.io" 
porta_mqtt = 14277

def requestIMUStream():
    client.publish('cmd2dev9840','{"op":1,"simulationTime":"3",'+
                    '"frequence":20,"sensorType":2}')
def stopIMU():
    client.publish('dev9840ss',{'op':22})

def on_connect(client, userdata, flags, rc):
    print("Connect with result code " + str(rc))
    client.subscribe("newdev")
    client.subscribe("dev9840ss")
    requestIMUStream()

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    posicao_pri = str(msg.payload).find(',')
    posicao_pro = str(msg.payload).find(',', posicao_pri + 1)
    print(str(msg.payload)[posicao_pri+1:posicao_pro])

    if str(msg.payload)[posicao_pri+1:posicao_pro] > '0.93':
        print("Conectado com sucesso.")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,1,0",' +
     
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}')
    else:
        print("Falha na conexão.")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}')

    if msg.topic == "dev9840ss":
        client.publish("seu_topico_de_saida", msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host_mqtt, porta_mqtt, 60)

client.loop_start()

while True:
    pass
