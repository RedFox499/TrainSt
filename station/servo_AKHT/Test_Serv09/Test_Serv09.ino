#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Создаем объект для работы с шилдом PCA9685
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

#define TURNOUTS_NUM 16   // Полная плата: ровно 16 стрелок (от 0 до 15)

// Настройки плавности хода
int stepSize = 1;      
int delayTime = 25;     

struct TurnoutPosition { 
    uint16_t plus; 
    uint16_t minus; 
}; 

// МАКСИМАЛЬНАЯ ТАБЛИЦА КАЛИБРОВКИ НА ВСЕ 16 КАНАЛОВ ПЛАТЫ
const TurnoutPosition turnout[TURNOUTS_NUM] = {
  {245, 215}, // стрелка 0
  {245, 215}, // стрелка 1  
  {210, 230}, // стрелка 2  
  {220, 210}, // стрелка 3  
  {230, 210}, // стрелка 4  
  {230, 210}, // стрелка 5
  {230, 210}, // стрелка 6
  {230, 210}, // стрелка 7
  {230, 210}, // стрелка 8
  {230, 210}, // стрелка 9
  {230, 210}, // стрелка 10
  {230, 210}, // стрелка 11
  {230, 210}, // стрелка 12
  {230, 210}, // стрелка 13
  {230, 210}, // стрелка 14
  {230, 210}  // стрелка 15 (последний свободный канал на шилде)
};

// Храним текущие положения стрелок: 0 — неизвестно при старте
uint8_t currentPos[TURNOUTS_NUM] = {0}; 

// Функция плавного движения
void moveServoSlow(uint8_t id, uint16_t fromPos, uint16_t toPos) {
  if (fromPos < toPos) {
    for (uint16_t p = fromPos; p <= toPos; p += stepSize) {
      pwm.setPWM(id, 0, p);
      delay(delayTime);
    }
  } else {
    for (uint16_t p = fromPos; p >= toPos; p -= stepSize) {
      pwm.setPWM(id, 0, p);
      delay(delayTime);
      if (p < stepSize) break; 
    }
  }
  delay(500);                
  pwm.setPWM(id, 0, 0); // Глушим ШИМ, чтобы моторы не зудели
}

// Логика перевода стрелки
void moveTurnout(uint8_t id, uint8_t targetPos) {
  if (id >= TURNOUTS_NUM) return;

  // Считаем точку старта
  uint16_t fromPos;
  if (currentPos[id] == 1) {
    fromPos = turnout[id].plus;
  } else if (currentPos[id] == 2) {
    fromPos = turnout[id].minus;
  } else {
    fromPos = (turnout[id].plus + turnout[id].minus) / 2;
  }

  // Считаем точку финиша
  uint16_t toPos;
  if (targetPos == 1) {
    toPos = turnout[id].plus;
  } else if (targetPos == 2) {
    toPos = turnout[id].minus;
  } else if (targetPos == 3) {
    toPos = (turnout[id].plus + turnout[id].minus) / 2;
  } else {
    return;
  }

  if (fromPos == toPos && currentPos[id] != 0) return;

  moveServoSlow(id, fromPos, toPos);
  currentPos[id] = targetPos;
}

// Супер-прогон для тотальной проверки ВСЕХ 16 сервоприводов
void runExpressTest() {
  for (int i = 0; i < TURNOUTS_NUM; i++) {
    moveTurnout(i, 1); // В плюс
    delay(100);
    moveTurnout(i, 2); // В минус
    delay(100);
    moveTurnout(i, 3); // В нейтраль
    delay(100);
  }
}

void setup() {
  // Наглухо фиксируем пины 6 и 7 для реле/индикаторов сразу при старте
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);

  Serial.begin(9600);
  Serial.setTimeout(50); 
  
  pwm.begin();
  pwm.setPWMFreq(60); 
  delay(10);

  // ПОЛНАЯ ТИШИНА НА СТАРТЕ (все сервы расслаблены)
  for (int i = 0; i < TURNOUTS_NUM; i++) {
    currentPos[i] = 0;    
    pwm.setPWM(i, 0, 0);  
  }

  Serial.println("=== МАКСИМАЛЬНАЯ СИСТЕМА АКТИВНА: ВСЕ 16 КАНАЛОВ ГОТОВЫ ===");
}

void loop() {
  // Держим уровни 6 и 7 в каждом цикле
  digitalWrite(6, HIGH);
  digitalWrite(7, LOW);

  if (Serial.available() > 0) {
    char header = Serial.read();

    if (header == 'W') {
      delay(5); 
      int swId = Serial.parseInt();    
      int posMode = Serial.parseInt(); 

      // Валидация под расширенный лимит массива (0-15)
      if (swId >= 0 && swId < TURNOUTS_NUM && posMode >= 1 && posMode <= 3) {
        moveTurnout(swId, posMode);
      }
    }
    else if (header == 'T') {
      runExpressTest();
    }
  }
}