from enlace import *
import time
from crc import Crc16, Calculator
import datetime

serialName = "COM5"  # Porta serial a ser utilizada

HEAD_SIZE = 12
PAYLOAD_MAX_SIZE = 50
EOP = b'\xAA\xBB\xCC'  # Exemplo de EOP de 3 bytes

def main():
    def extract_head(head):
        #head = package[:HEAD_SIZE]
        message_type = head[0]
        error_type = head[1]
        pacote_num = int.from_bytes(head[2:5], byteorder='big')
        total_pacotes = int.from_bytes(head[5:8], byteorder='big')
        payload_size = int.from_bytes(head[8:], byteorder='big')
        #payload = package[HEAD_SIZE:-3]
        return message_type, error_type, pacote_num, total_pacotes, payload_size
    
    # def create_new_package(message_type, crc, pacote_num, total_pacotes, payload_size, payload):
    #     head = (message_type.to_bytes(1, byteorder='big') + 
    #             crc.to_bytes(2, byteorder='big') + 
    #             pacote_num.to_bytes(3, byteorder='big') + 
    #             total_pacotes.to_bytes(3, byteorder='big') + 
    #             payload_size.to_bytes(4, byteorder='big'))
    #     package = head + payload + EOP
    #     return package

    # def calculate_crc(payload):
    #     calculadora = Calculator(Crc16.XMODEM)
    #     crc = calculadora.checksum(payload)
    #     return crc

    lista_pacotes = []
    lista_payloads = []
    
    # log = '=========================================='
    
    try:
        com2 = enlace(serialName)

        print("-------------------------")
        print("Iniciou o main")
        
        com2.enable()
        print("Abriu a comunicação")
        print("-------------------------")
        
        print("\nEsperando 1 byte de sacrifício")
        rxBuffer, nRx = com2.getData(1)

        com2.rx.clearBuffer()
        time.sleep(.1)

        print("Servidor pronto")

        # Handshake para iniciar a comunicação
        while True:
            if com2.rx.getBufferLen() > 0:
                handshake, _ = com2.getData(9)
                if handshake == b'handshake':
                    com2.sendData(b's')
                    print("Handshake realizado")
                    break

        
        pacote_num = 1
        received_data = b''

        while True:
            # Recebe o cabeçalho do pacote
            # bytes_pacote, _ = com2.getData(PAYLOAD_MAX_SIZE + 3)
            head_pacote, _ = com2.getData(HEAD_SIZE)
            mensagem_type, crc, pacote_atual, total_pacotin, size_payload = extract_head(head_pacote)

            print('='*100)
            print(f"Pacote atual: {pacote_atual}")
            # print(lista_pacotes)


            # Recebe o payload e o EOP
            payload_eop, _ = com2.getData(size_payload + len(EOP))
            payload = payload_eop[:size_payload]
            eop = payload_eop[-len(EOP):]
            
            #total_pacotes = len(str(total_pacotin))
            print(f'Total pacotes: {total_pacotin}')


            # Verifica se o tamanho do payload corresponde ao esperado
            if len(payload) == size_payload and eop == EOP and pacote_atual not in lista_pacotes and payload not in lista_payloads:
                lista_pacotes.append(pacote_atual)
                lista_payloads.append(payload)
                # Se o tamanho do payload for correto, envia o pacote de volta com erro_type = 1
                resposta = b's'
                com2.sendData(resposta)
                print(f"Pacote {pacote_atual} recebido corretamente, enviando confirmação com erro_type = 1")
                print('Esperando próximo pacote\n')

                # log += f'\n{datetime.now()}/recebi/2/{bytes_pacote}/{pacote_atual}/{total_pacotin}/{crc}'

                if pacote_atual == total_pacotin:
                    break

            elif pacote_atual in lista_pacotes:
                resposta = b'n'
                com2.sendData(resposta)
                # log += f'\n{datetime.now()}/enviei/3/{pacote_atual}'
                lista_pacotes.remove(pacote_atual)
                lista_payloads.remove(payload)
                time.sleep(1)

            else:
                # Se o tamanho do payload estiver incorreto, envia o pacote de volta com erro_type = 2
                resposta = b'n'
                com2.sendData(resposta)

                # log += f'\n{datetime.now()}/enviei/3/{bytes_pacote}/{pacote_atual}/{total_pacotin}/{crc}'

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
