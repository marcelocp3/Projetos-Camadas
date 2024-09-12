#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


from enlace import *
import time
import numpy as np
import struct

serialName = "COM4"

def main():
    try:
        print("Iniciou o main")
        com1 = enlace(serialName)
        
        com1.enable()

        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)


        print("Abriu a comunicação")   



    
        
                  
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        # imageR = "imagem.png"
        # # Transforma a imagem em um array de bytes
        # with open(imageR, "rb") as image:
        #     f = image.read()
        #     txBuffer = bytearray(f)
        
        # print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
                
        # com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        # time.sleep(0.1)
        
        # txSize = com1.tx.getStatus()
        # print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        # while i < len(rxBuffer):
        #     byte, nRx = com1.getData(i)  # Recebe um byte de cada vez
        #     if nRx > 0:
        #         rxBuffer += byte
        # print("Mensagem recebida:", rxBuffer.decode())


        i = 480
        receba = com1.getData(i)
        print(receba)

        print("recebeu {} bits" .format((receba[1])))

        receba_sliced = [receba[0][i:i+32] for i in range(0, len(receba[0]), 32)]


        for i in range(len(receba_sliced)):
            time.sleep(0.1)
            print("recebeu {}" .format(receba_sliced[i]))

        print("recebeu {} pacotes" .format(len(receba_sliced)))
        print("recebeu {}" .format(receba_sliced))



        soma = 0 #EDITAR AQUI PARA ERRO DE SOMA
        for j in range(len(receba_sliced)):
            valor = binary32_to_float(receba_sliced[j])
            soma += valor




        print("soma = {}" .format(soma))    



        txBuffer = float_to_binary32(soma).encode()

        txBuffer_array = [txBuffer[i:i+32] for i in range(0, len(txBuffer), 32)]

        # Converte a string binária em bytes

        # Envia os bytes


        # time.sleep(7)
        com1.sendData(txBuffer)



        time.sleep(0.1) #mudar esse tambem
        print("enviou {}" .format(txBuffer))

        com1.sendData(np.asarray(txBuffer_array))

        txSize = com1.tx.getStatus()


        print("-------------------------")
        time.sleep(0.1)
        print("Enviou {}" .format(txSize + 32))
        print("-------------------------")
        




        # for i in range(len(rxBuffer)):
        #     print("recebeu {}" .format(rxBuffer[i]))
        
        
        
        # # imageR = "imagem.png"
        # # # Transforma a imagem em um array de bytes
        # # with open(imageR, "rb") as image:
        # #     f = image.read()
        # #     txBuffer = bytearray(f)



        # com1.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
        
        # time.sleep(0.1)
        
        # txSize = com1.tx.getStatus()
        # print('enviou = {}' .format(txSize))

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

def binary32_to_float(binary_str):
        """Converte uma string binária IEEE 754 (32 bits) para um número float."""
        # Converte a string binária de volta para inteiro
        int_value = int(binary_str, 2)
        # Converte o inteiro para bytes
        packed_value = int_value.to_bytes(4, byteorder='big')
        # Usa struct.unpack para desempacotar os bytes para float
        float_value = struct.unpack('>f', packed_value)[0]
        return float_value

def float_to_binary32(value):
    bits, = struct.unpack('!I', struct.pack('!f', value))
    return f'{bits:032b}'       

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
