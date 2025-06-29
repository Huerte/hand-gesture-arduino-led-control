const int LED_ONE = 8;
const int LED_TWO = 9;
const int LED_THREE = 10;
const int LED_FOUR = 11;
const int LED_FIVE = 12;

void setup() {

  Serial.begin(9600);

  pinMode(LED_ONE, OUTPUT);
  pinMode(LED_TWO, OUTPUT);
  pinMode(LED_THREE, OUTPUT);
  pinMode(LED_FOUR, OUTPUT);
  pinMode(LED_FIVE, OUTPUT);

}

void loop() {

  if (Serial.available() > 0){

    char msg = Serial.read();

    if (msg == '1') {
      digitalWrite(LED_ONE, HIGH);
      digitalWrite(LED_TWO, HIGH);
      digitalWrite(LED_THREE, HIGH);
      digitalWrite(LED_FOUR, HIGH);
      digitalWrite(LED_FIVE, HIGH);
    } else if (msg == '0') {
      digitalWrite(LED_ONE, LOW);
      digitalWrite(LED_TWO, LOW);
      digitalWrite(LED_THREE, LOW);
      digitalWrite(LED_FOUR, LOW);
      digitalWrite(LED_FIVE, LOW);
    }

  }

}
