from enlace import *
import time
from crc import Crc16, Calculator
import datetime

serialName = "COM5"  # Porta serial a ser utilizada

HEAD_SIZE = 12
PAYLOAD_MAX_SIZE = 50
EOP = b'\xAA\xBB\xCC'  # Exemplo de EOP de 3 bytes

def main():
    def extract_package(head):
        # head = package[:HEAD_SIZE]
        message_type = head[0]
        crc = int.from_bytes(head[1:3], byteorder='big')
        pacote_num = int.from_bytes(head[3:6], byteorder='big')
        total_pacotes = int.from_bytes(head[6:9], byteorder='big')
        payload_size = int.from_bytes(head[9:], byteorder='big')
        # payload = package[HEAD_SIZE:-len(EOP)]
        return message_type, crc, pacote_num, total_pacotes, payload_size
    
    # def create_new_package(message_type, crc, pacote_num, total_pacotes, payload_size, payload):
    #     head = (message_type.to_bytes(1, byteorder='big') + 
    #             crc.to_bytes(2, byteorder='big') + 
    #             pacote_num.to_bytes(3, byteorder='big') + 
    #             total_pacotes.to_bytes(3, byteorder='big') + 
    #             payload_size.to_bytes(4, byteorder='big'))
    #     package = head + payload + EOP
    #     return package

    def calculate_crc(payload):
        calculadora = Calculator(Crc16.XMODEM)
        crc = calculadora.checksum(payload)
        return crc

    lista_pacotes = []
    lista_payloads = []

    with open('log.txt', 'w') as file:
        file.write('')
    
    try:
        com2 = enlace(serialName)

        print("-------------------------")
        print("Iniciou o main")
        
        com2.enable()
        print("Abriu a comunicação")
        print("-------------------------")
        
        print("\nEsperando 1 byte de sacrifício")
        rxBuffer, nRx = com2.getData(1)

        with open('log.txt', 'a') as file:
            file.write(f'{datetime.datetime.now()}/ 2 / {len(rxBuffer)}\n')

        com2.rx.clearBuffer()
        time.sleep(.1)

        print("Servidor pronto")

        # Handshake para iniciar a comunicação
        while True:
            if com2.rx.getBufferLen() > 0:
                handshake, _ = com2.getData(9)
                with open('log.txt', 'a') as file:
                    file.write(f'{datetime.datetime.now()}/ 2 / {len(handshake)}\n')
                if handshake == b'handshake':
                    com2.sendData(b's')
                    with open('log.txt', 'a') as file:
                        file.write(f'{datetime.datetime.now()}/ 1 / handshake\n')
                    print("Handshake realizado")
                    break

        # pacote_num = 1
        # received_data = b''

        while True:
            # Recebe o cabeçalho do pacote
            head_pacote, _ = com2.getData(HEAD_SIZE)
            mensagem_type, crc, pacote_atual, total_pacotin, size_payload = extract_package(head_pacote)

            print('='*100)
            print(f"Pacote atual: {pacote_atual}")
            # print(lista_pacotes)


            # Recebe o payload e o EOP
            payload_eop, _ = com2.getData(size_payload + len(EOP))
            payload = payload_eop[:size_payload]
            eop = payload_eop[-len(EOP):]
            bytes_pacote = len(payload)

            crc_calculado = calculate_crc(payload)
            
            #total_pacotes = len(str(total_pacotin))
            print(f'Total pacotes: {total_pacotin}')


            # Verifica se o tamanho do payload corresponde ao esperado
            if len(payload) == size_payload and eop == EOP and pacote_atual not in lista_pacotes and payload not in lista_payloads and crc_calculado == crc: #tirar o and pra testar o teste sem o cabo
                lista_pacotes.append(pacote_atual)
                lista_payloads.append(payload)
                # Se o tamanho do payload for correto, envia o pacote de volta com erro_type = 1
                resposta = b's'
                com2.sendData(resposta)
                print(f"Pacote {pacote_atual} recebido corretamente, enviando confirmação com erro_type = 1")
                print(f'CRC: {crc}')
                print(f'CRC calculado: {crc_calculado}')
                print('Esperando próximo pacote\n')

                with open('log.txt', 'a') as file:
                    file.write(f'{datetime.datetime.now()} / enviei / 2 / {len(resposta)}\n')
                    file.write(f'{datetime.datetime.now()} / recebi / 1 / {bytes_pacote} / {pacote_atual} / {total_pacotin} / {crc}\n')

                if pacote_atual == total_pacotin:
                    break
            
            elif crc != crc_calculado:
                if pacote_atual in lista_pacotes:
                    resposta = b'n'
                    com2.sendData(resposta)
                    print('ERRO: erro no crc do pacote')
                    with open('log.txt', 'a') as file:
                        file.write(f'{datetime.datetime.now()} / enviei / 3 / {len(resposta)}\n')
                    lista_pacotes.remove(pacote_atual)
                    lista_payloads.remove(payload)
                    time.sleep(1)
                else:
                    lista_pacotes.append(pacote_atual)
                    lista_payloads.append(payload)

            elif pacote_atual in lista_pacotes:
                resposta = b'n'
                com2.sendData(resposta)
                print('ERRO: erro no pacote')
                with open('log.txt', 'a') as file:
                    file.write(f'{datetime.datetime.now()} / enviei / 3 / {len(resposta)}\n')
                lista_pacotes.remove(pacote_atual)
                lista_payloads.remove(payload)
                time.sleep(1)

            # elif pacote_atual in lista_pacotes or crc != crc_calculado:
            #     resposta = b'n'
            #     com2.sendData(resposta)
            #     print('ERRO: erro no pacote')
            #     # log += f'\n{datetime.now()}/enviei/3/{pacote_atual}'
            #     if len(lista_pacotes) != 0 and len(lista_payloads) != 0:
            #         lista_pacotes.remove(pacote_atual)
            #         lista_payloads.remove(payload)
            #     time.sleep(1) #crc

            else:
                # Se o tamanho do payload estiver incorreto, envia o pacote de volta com erro_type = 2
                resposta = b'n'
                com2.sendData(resposta)

                with open('log.txt', 'a') as file:
                    #file.write(f'{datetime.datetime.now()} / ')
                    file.write(f'{datetime.datetime.now()} / enviei / 3 / {pacote_atual}\n')

                print("Erro na recepção, enviando confirmação com erro_type = 2")


        # Salva o arquivo recebido
        received_data2 = b''

        for i in lista_payloads:
            received_data2 += i
        
        with open('arquivo_recebido.txt', 'wb') as file:
            file.write(received_data2)

        print("Arquivo recebido com sucesso")
        com2.disable()

    except Exception as erro:
        print("Erro:", erro)
        com2.disable()

if __name__ == "__main__":
    main()
