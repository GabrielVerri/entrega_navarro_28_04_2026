import paho.mqtt.client as mqtt
import time
import random

# Credenciais do HiveMQ
BROKER_HOST = "8c9c50b649574d99b63c65de60dcc576.s2.eu.hivemq.cloud"
BROKER_PORT = 8883  # Porta padrão para MQTT sobre TLS
USERNAME = "teste"
PASSWORD = "Teste123"
TOPIC = "sensor/data" # Tópico para publicar os dados do sensor

# Função de callback quando o cliente se conecta ao broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
    else:
        print(f"Falha na conexão, código de retorno: {rc}\n")

# Cria uma instância do cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Define as funções de callback
client.on_connect = on_connect

# Configura credenciais
client.username_pw_set(USERNAME, PASSWORD)

# Habilita TLS/SSL para conexão segura (HiveMQ Cloud exige)
# Note: paho-mqtt requer que você forneça o caminho para o certificado CA do broker
# Para HiveMQ Cloud, você pode usar os certificados raiz da Let's Encrypt ou ISRG.
# Para simplificar, vou usar o modo TLS sem validação rigorosa aqui (INSECURE),
# mas para produção, você deve usar `tls_set()` com os certificados apropriados.
client.tls_set()

# Conecta ao broker
try:
    client.connect(BROKER_HOST, BROKER_PORT, 60)
except Exception as e:
    print(f"Erro ao conectar ao broker: {e}")
    sys.exit(1)

# Inicia um loop em uma thread separada para lidar com eventos de rede
client.loop_start()

print(f"Publicando dados simulados para o tópico: {TOPIC}")

try:
    for i in range(10): # Publica 10 mensagens de exemplo
    # while True:
        temperature = round(random.uniform(20.0, 30.0), 2) # Temperatura simulada
        humidity = round(random.uniform(50.0, 70.0), 2)    # Umidade simulada
        
        # Converte o timestamp para milissegundos para facilitar o uso em JavaScript
        payload = f"{{\"timestamp\": {int(time.time() * 1000)}, \"temperature\": {temperature}, \"humidity\": {humidity}}}"
        
        client.publish(TOPIC, payload)
        print(f"Publicado: {payload}")
        time.sleep(2) # Espera 2 segundos antes de enviar a próxima mensagem

except KeyboardInterrupt:
    print("Publicação interrompida pelo usuário.")
except Exception as e:
    print(f"Ocorreu um erro durante a publicação: {e}")
finally:
    # Desconecta do broker
    client.loop_stop()
    client.disconnect()
    print("Desconectado do broker MQTT.")