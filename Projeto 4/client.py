from enlace import *
import time
import numpy as np
from crc import Calculator, Crc16
import crcmod
import datetime

serialName = "COM3"  # Porta serial a ser utilizada

# Definição dos campos do pacote
HEAD_SIZE = 12
PAYLOAD_MAX_SIZE = 50
EOP = b'\xAA\xBB\xCC'  # Exemplo de EOP de 3 bytes
pacotes_dict = {}

# head de 12 bytes
# 1 byte: tipo da mensagem
# 1 byte: tipo do erro
# 3 bytes: número do pacote
# 3 bytes: número total de pacotes
# 4 bytes: tamanho do payload


#new head 12 bytes
# 1 byte: tipo da mensagem
# 2 bytes: CRC-16
# 3 bytes: numero do pacote
# 3 bytes: numero total de pacotes
# 3 bytes: tamanho do payload

# def create_package(message_type, error_type, pacote_num, total_pacotes, payload_size, payload):
#     head = (message_type.to_bytes(1, byteorder='big') + 
#             error_type.to_bytes(1, byteorder='big') + 
#             pacote_num.to_bytes(3, byteorder='big') + 
#             total_pacotes.to_bytes(3, byteorder='big') + 
#             payload_size.to_bytes(4, byteorder='big'))
#     package = head + payload + EOP
#     return package

# def extract_package(package):
#     head = package[:HEAD_SIZE]
#     message_type = head[0]
#     error_type = head[1]
#     pacote_num = int.from_bytes(head[2:5], byteorder='big')
#     total_pacotes = int.from_bytes(head[5:8], byteorder='big')
#     payload_size = int.from_bytes(head[8:], byteorder='big')
#     payload = package[HEAD_SIZE:-len(EOP)]
#     return message_type, error_type, pacote_num, total_pacotes, payload_size, payload

def create_new_package(message_type, crc, pacote_num, total_pacotes, payload_size, payload):
    head = (message_type.to_bytes(1, byteorder='big') + 
            crc.to_bytes(2, byteorder='big') + 
            pacote_num.to_bytes(3, byteorder='big') + 
            total_pacotes.to_bytes(3, byteorder='big') + 
            payload_size.to_bytes(3, byteorder='big'))
    package = head + payload + EOP
    return package

def extract_new_package(package):
    head = package[:HEAD_SIZE]
    message_type = head[0]
    crc = int.from_bytes(head[1:3], byteorder='big')
    pacote_num = int.from_bytes(head[3:6], byteorder='big')
    total_pacotes = int.from_bytes(head[6:9], byteorder='big')
    payload_size = int.from_bytes(head[9:], byteorder='big')
    payload = package[HEAD_SIZE:-len(EOP)]
    return message_type, crc, pacote_num, total_pacotes, payload_size, payload

def calculate_crc(payload):
    calculadora = Calculator(Crc16.XMODEM)
    crc = calculadora.checksum(payload)
    return crc

def main():
    with open('log.txt', 'w') as log:
        log.write("")

    try:
        com1 = enlace(serialName)
        com1.enable()
        time.sleep(0.2)
        
        print("Abriu a comunicação para enviar o byte de sacrifício")
        com1.sendData(b'\x00')  # Enviando o byte de sacrifício
        time.sleep(1)
        print('----------------------\n')
        
        print("Comunicação aberta")

        # Enviar mensagem de handshake
        com1.sendData(b'handshake')
        start_time = time.time()

        while True:
            if com1.rx.getBufferLen() > 0:
                response, _ = com1.getData(1)
                if response == b's':
                    print("Servidor pronto para receber")
                    break
            elif time.time() - start_time > 5:
                retry = input("Servidor inativo. Tentar novamente? S/N: ")
                if retry.lower() == 's':
                    com1.sendData(b'handshake')
                    start_time = time.time()
                else:
                    com1.disable()
                    return

        # Fragmentar o arquivo e enviar pacotes
        data = open('arquivo.txt', 'rb').read()
        tamanho_imagem = len(data)

        resto = len(data) % PAYLOAD_MAX_SIZE
        total_pacotes = len(data) // PAYLOAD_MAX_SIZE + (1 if resto > 0 else 0)

        print(f"Fragmentando imagem em {total_pacotes} pacotes")
        print(f"Tamanho da imagem: {tamanho_imagem} bytes")
        print(f"Enviando {total_pacotes} pacotes")

        pacote_num = 1
    
        while pacote_num <= total_pacotes:
            if len(data) >= PAYLOAD_MAX_SIZE:
                payload = data[:PAYLOAD_MAX_SIZE]
                data = data[PAYLOAD_MAX_SIZE:]
            else:
                payload = data
                data = b''

            payload_size = len(payload)
            #package = create_package(1, 0, pacote_num, total_pacotes, payload_size, payload)

            if pacote_num == 8:
                new_package = create_new_package(1, calculate_crc(payload) + 157, pacote_num, total_pacotes, payload_size, payload)

            else:
                new_package = create_new_package(1, calculate_crc(payload), pacote_num, total_pacotes, payload_size, payload)
            
            print(f"Enviando pacote {pacote_num} de {total_pacotes}")
            print(f'{calculate_crc(payload)}')
            print('-----------------------------------------------------------------')
            with open ('log.txt', 'a') as log:
                log.write(f"{datetime.datetime.now()} / envio / 1 / {payload_size} / {pacote_num} / {total_pacotes} / {calculate_crc(payload)}\n")

            com1.sendData(np.asarray(new_package))
            pacotes_dict[pacote_num] = new_package

            max_retries = 30
            retries = 0

            while retries < max_retries or pacote_num == total_pacotes:
                time.sleep(1)

                if com1.rx.getBufferLen() > 0:
                    response, _ = com1.getData(1)  # Tamanho do pacote de resposta
                    print(f"Resposta recebida para pacote {pacote_num}: {response} \n")



                    if response == b's':
                        print(f"Pacote {pacote_num} enviado com sucesso")

                        with open ('log.txt', 'a') as log:
                            log.write(f"{datetime.datetime.now()} / receb / 2 / {calculate_crc(payload)} \n")
                            log.write("   \n")

                        pacote_num += 1
                        break
                                        
                    elif response == b'n':  # Reenviar o pacote
                        print(f"Erro no pacote {pacote_num}, reenviando...")

                        with open ('log.txt', 'a') as log:
                            log.write(f"{datetime.datetime.now()} / receb / 3 / \n")
                            log.write("   \n")

                        com1.sendData(np.asarray(new_package))
                        retries += 1
                else:
                    print(f"Nenhuma resposta recebida para pacote {pacote_num}. Tentativa {retries+1}/{max_retries}")
                    new_package = create_new_package(1, 0, pacote_num, total_pacotes, payload_size, payload)
                    com1.sendData(np.asarray(new_package))
                    print(f"Enviando pacote {pacote_num} de {total_pacotes}")
                    with open ('log.txt', 'a') as log:
                        log.write(f"{datetime.datetime.now()} / envio / 1 / {payload_size} / {pacote_num} / {total_pacotes} / {calculate_crc(payload)}\n")
                        log.write("   \n")

                    retries += 1

                    if retries >= max_retries:
                        print("Timeout esperando resposta do servidor")
                        com1.disable()
                        return

        print("Todos os pacotes foram enviados")
        with open ('log.txt', 'a') as log:
            log.write("   \n")
            log.write("Todos os pacotes foram enviados")
            log.write("   \n")

        com1.disable()

    except Exception as erro:
        print("Erro:", erro)
        com1.disable()

if __name__ == "__main__":
    main()