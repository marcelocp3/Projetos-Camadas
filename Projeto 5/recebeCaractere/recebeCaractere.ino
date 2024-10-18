// Definindo parâmetros
int rxPin = 8;
int baudRate = 9600;

void setup() {
  pinMode(rxPin, INPUT);
  Serial.begin(9600);
}

void loop() {
  char caractere = recebe_char();

  Serial.print("Caractere recebido: ");
  Serial.println(caractere);
}

char recebe_char() {
  char data = 0;

  while(digitalRead(rxPin) == HIGH);

  _sw_uart_wait_half_T();
  _sw_uart_wait_T();

  // Recebendo os bits do caractere
  for (int i = 0; i < 8; i++) {
    data |= (digitalRead(rxPin) << i);
    _sw_uart_wait_T();
  }

  int received_parity = digitalRead(rxPin);
  _sw_uart_wait_T();

  int calculated_parity = calc_even_parity(data);
  if (calculated_parity != received_parity) {
    return '*'; // Erro: paridade incorreta
  }

  return data;
}


// Função de espera para meio período
void _sw_uart_wait_half_T() {
  for (int i = 0; i < 155; i++) {
    asm("NOP");
  }
}

// Função de espera para um período inteiro
void _sw_uart_wait_T() {
  for (int i = 0; i < 310; i++) {
    asm("NOP");
  }
}

// Cálculo de paridade (paridade par)
int calc_even_parity(char data) {
  int ones = 0;

  for (int i = 0; i < 8; i++) {
    ones += (data >> i) & 0x01;
  }

  return ones % 2; // Retorna 0 se for par, 1 se for ímpar
}

