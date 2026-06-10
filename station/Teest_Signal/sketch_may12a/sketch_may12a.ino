// Пины для сдвиговых регистров (74HC595)
#define DATA_PIN  13  // DS
#define LATCH_PIN 12  // ST_CP
#define CLOCK_PIN 11  // SH_CP

// Храним 2 байта состояния светофоров (0xFF - всё выключено по умолчанию)
byte signalBytes[2] = {0xFF, 0xFF}; 

void setup() {
  Serial.begin(9600);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  
  // При старте гасим абсолютно всё
  updateHardware();
  Serial.println("SYSTEM: 2-BYTE LIGHTS MODE READY");
}

void loop() {
  // Крутимся в цикле, пока в буфере Serial есть хоть какие-то данные
  while (Serial.available() > 0) {
    
    // Заглядываем в самый первый байт в очереди, не удаляя его
    if (Serial.peek() == 'L') {
      // Маркер 'L' на месте! Проверяем, долетели ли 2 байта данных
      if (Serial.available() >= 3) {
        Serial.read();                  // Теперь со спокойной душой выкидываем маркер 'L'
        signalBytes[0] = Serial.read(); // Читаем 1 БАЙТ (H, Ч1, Ч2, Ч3)
        signalBytes[1] = Serial.read(); // Читаем 2 БАЙТ (Ч4, Ч5, РЕЗЕРВ)
        updateHardware();               // Шлем ровный кадр в регистры
      } else {
        // Буква 'L' пришла, но сами байты цвета ещё ползут по кабелю.
        // Выходим из цикла чтения и ждем их в следующем цикле loop.
        break; 
      }
    } else {
      // Если наткнулись НЕ на 'L' — это мусор или сдвиг кадра.
      // Безжалостно удаляем этот байт и смотрим, что идет за ним.
      Serial.read(); 
    }
  }
}

void updateHardware() {
  digitalWrite(LATCH_PIN, LOW);
  
  // Проталкиваем 2 байта в цепочку регистров
  for (int i = 1; i >= 0; i--) {
    shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, signalBytes[i]);
  }
  
  digitalWrite(LATCH_PIN, HIGH);
}