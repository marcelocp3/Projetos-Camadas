// Definindo os parâmetros do programa
int txPin = 8;
int baudRate = 9600;
char caractere = 'K';

void setup() {
  pinMode(txPin, OUTPUT);
  digitalWrite(txPin, HIGH);
}

void loop() {
  envia_char(caractere);
  delay(10);
}

// Função que envia o caractere
void envia_char(char data) {
  // Bit de inicio
  digitalWrite(txPin, LOW);
  _sw_uart_wait_T();

  // Envia os 8 bits do caractere e espera meio período para o próximo bit
  for(int i = 0; i < 8; i++){
    digitalWrite(txPin, (data >> i) & 0x01);
    _sw_uart_wait_T();
  }

  // Bit de paridade
  int paridade = calc_even_parity(data);
  digitalWrite(txPin, paridade);
  _sw_uart_wait_T();

  // Stop bit
  digitalWrite(txPin, HIGH);
  _sw_uart_wait_T();
}


// Função de espera de meio período
void _sw_uart_wait_half_T() {
  for(int i = 0; i < (155); i++) {
    asm("NOP");
  }
}

// Função de espera de um período inteiro
void _sw_uart_wait_T() {
  for(int i = 0; i < (310); i++) {
    asm("NOP");
  }
}

// Cálculo de paridade
int calc_even_parity(char data) {
  int ones = 0;

  for(int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }

  return ones % 2;
}
