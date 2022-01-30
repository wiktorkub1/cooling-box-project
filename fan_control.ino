int count = 0;
unsigned long start_time;
int rpm;
float temperature = 0;

void setup()
{
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), counter, RISING);
  pinMode(7, OUTPUT);
  digitalWrite(7, LOW);
}

void loop()
{
  start_time = millis();
  count = 0;
  while ((millis() - start_time) < 1000) {}
  
  rpm = count * 60 / 2;
  temperature = float(analogRead(A0)) * 500.0 / 1024.0;
  
  if (temperature > 30)
  {
    digitalWrite(7, HIGH);
  }
  else
  {
    digitalWrite(7, LOW);
  }
  
  Serial.println((String)temperature + ";" + rpm);
}

void counter()
{
  count++;
}
