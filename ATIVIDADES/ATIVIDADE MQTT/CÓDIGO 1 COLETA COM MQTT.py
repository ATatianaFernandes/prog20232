import paho.mqtt.client as mqtt  #Importando as bibliotecas
import json
import csv
import math
import socket
import numpy as np   

#arrays Numpy vazios para armazenar dados dos sensores e ângulos
sensor1 = np.array([])    
sensor2 = np.array([])
sensor3 = np.array([])
sensor4 = np.array([])
variaveis = ('ax','ay','az','gx','gy','gz')
angulo = np.array([])

caminho = 'dadosSensor.txt' #O código cria um arquivo chamado 'dadosSensor.txt' e escreve uma linha inicial indicando informações de simulação e IMU.

with open(caminho, 'w') as arquivo:
    arquivo.write('Simulation Time: 3, Frequence: 20, Dados do IMU\n')


host_mqtt = "0.tcp.sa.ngrok.io" 
porta_mqtt = 14277

def requestIMUStream():
    client.publish('cmd2dev9840','{"op":1,"simulationTime":"3",'+
                    '"frequence":20,"sensorType":2}')
def stopIMU():
    client.publish('dev9840ss',{'op':22})

def on_connect(client, userdata, flags, rc):    #Callbacks para Conexão e Recebimento de Mensagens 
    if rc == 0:
        print("Conectado com sucesso." + str(rc))
        client.subscribe("newdev")
        client.subscribe("dev9840ss")
        requestIMUStream()
    else:
        print(f"Falha na conexão. Código de retorno: {rc}")
    client.reconnect()

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

    posicao_pri = str(msg.payload).find(',')
    posicao_pro = str(msg.payload).find(',', posicao_pri + 1)
    print(str(msg.payload)[posicao_pri+1:posicao_pro])

    if str(msg.payload)[posicao_pri+1:posicao_pro] > '0.93':
        print("Ligado")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,1,0",' +
     
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}')
    else:
        print("Não ligado")
        client.publish('cmd2dev3632',
                   '{"op":2,"m":0,0,0,0",' +
                   '"t":200,"p":20000}')

    if msg.topic == "dev9840ss":
        client.publish("seu_topico_de_saida", msg.payload)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Desconexão inesperada. Tentando reconectar... Código: {rc}")
        client.reconnect()     

client = mqtt.Client ()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.connect(host_mqtt, porta_mqtt, 60)
try:
    client.connect("10.1.0.18", 1883, 60)
    client.loop_start()
except socket.timeout:
    print("Erro: Timeout de conexão excedido. Verifique o endereço IP e as configurações de rede.")

client.loop_start()

while True:
    pass

# Separando Sensores
def separa_sensores(arquivo):     
    arquivo = open("coletasensores.csv", "r")  #ESTÁ CSV e lá em cima TXT

    lista_dados_braço_esquerdo = []
    lista_dados_braço_direito = []
    lista_dados_perna_esquerda = []
    lista_dados_perna_direita = []

    for line in arquivo:
        dados_dos_sensores = line.split('],""[')
        braço_esquerdo = dados_dos_sensores[0].split('[')[1]   #inclui todos os valores
        braço_direito = dados_dos_sensores[1].split(",")[:6]
        perna_esquerda = dados_dos_sensores[1].split(",")[6:12]
        perna_direita = dados_dos_sensores[1].split(",")[12:]

        for lista_dados, sensor_data in zip(
            [lista_dados_braço_esquerdo, lista_dados_braço_direito,
             lista_dados_perna_esquerda, lista_dados_perna_direita],
            [braço_esquerdo, braço_direito, perna_esquerda, perna_direita]
        ):
            sensor_data = sensor_data.split(",")
            sensor_data = [float(value) for value in sensor_data]
            lista_dados.append(sensor_data)

    return(lista_dados_braço_esquerdo,
           lista_dados_braço_direito,
           lista_dados_perna_esquerda,
           lista_dados_perna_direita)

# Função p/ Calcular Ângulo
def calcular_angulo(lista_dados_sensor):
    angulo_lista = []
    for item in lista_dados_sensor:
        M = 0.98
        dt = 0.05
        dado_w = item[3]
        dado_a = (math.atan(item[0] / math.sqrt((item[1]) * 2 + (item[2]) ** 2))) * (180 / math.pi)

        angulo = (M*(dado_w * dt) + (1- M) * (dado_a))/(1-M)
        angulo_lista.append(angulo)
    return angulo_lista

# Função para Calcular Somatório

def somatorio(angulos):
    somatorio = angulos.sum()
    print("Somatorio: ", somatorio)

# Função para Calcular Média
def media(angulos):
    media = angulos.mean()
    print("Media: ", media)

# Leitura dos Sensores
    
lista_angulos_braço_esquerdo = []
lista_angulos_braço_direito = []
lista_angulos_perna_esquerda = []
lista_angulos_perna_direita = []

try:
    with open("coletasensores.csv", "r") as arquivo:
        (lista_angulos_braço_esquerdo,
         lista_angulos_braço_direito,
         lista_angulos_perna_esquerda,
         lista_angulos_perna_direita) = separa_sensores(arquivo)

    #lista_angulos_braço_esquerdo,
   # lista_angulos_braço_direito,
   # lista_angulos_perna_esquerda,
   # lista_angulos_perna_direita = separa_sensores()

except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
except Exception as e:
    print(f"Erro durante a leitura dos sensores: {e}")


# ARRAY . # Cálculo dos Ângulos
angulo_braço_esquerdo_array = np.array(calcular_angulo(lista_angulos_braço_esquerdo))
angulo_braço_direito_array = np.array(calcular_angulo(lista_angulos_braço_direito))
angulo_perna_esquerda_array = np.array(calcular_angulo(lista_angulos_perna_esquerda))
angulo_perna_direita_array = np.array(calcular_angulo(lista_angulos_perna_direita))

# EXECUÇÃO DAS FUNÇÕES
somatorio(angulo_braço_esquerdo_array)
somatorio(angulo_braço_direito_array)
somatorio(angulo_perna_esquerda_array)
somatorio(angulo_perna_direita_array)

media(angulo_braço_esquerdo_array)
media(angulo_braço_direito_array)
media(angulo_perna_esquerda_array)
media(angulo_perna_direita_array)

# (Chamadas para outras funções semelhantes)

# Escreve os ângulos no arquivo de texto
with open('anguloProcessado.txt', 'w') as arquivoTxt:
    arquivoTxt.write('Sensor 1:\n')
    arquivoTxt.write('\n'.join(map(str, angulo_braço_esquerdo_array)))

# Escreve os ângulos no arquivo CSV
with open('anguloProcessado.csv', 'w', newline='') as arquivo_csv:
    spamwriter = csv.writer(arquivo_csv, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Ângulos'])  # Cabeçalho
    spamwriter.writerows(angulo_braço_esquerdo_array.reshape(-1, 1))  # Escreve os ângulos

# Fecha os arquivos
arquivoTxt.close()
arquivo_csv.close()

# Imprime saídas processadas
print('Saídas geradas')
print('Somatório: ', np.around(angulo.sum(), decimals=2))
print('Média: ', np.around(angulo.mean(), decimals=2))
print('Ângulo menor: ', np.around(angulo.min(), decimals=2))
print('Ângulo maior: ', np.around(angulo.max(), decimals=2))
print('Integral: ', np.around(np.trapz(angulo), decimals=2))
print('Variância: ', np.around(angulo.var(), decimals=2))
print('Diferença entre ângulos: ', np.around(np.diff(angulo), decimals=2))
