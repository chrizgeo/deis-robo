/***********************************************************************
 * Martin Varghese
 * markoo19@student.hh.se
 * Nov 2020
 * Serial drive 
***********************************************************************/

#include <RedBot.h>

RedBotMotors motors;
RedBotEncoder encoder = RedBotEncoder(A2, 10);  // initializes encoder on pins A2 and 10
RedBotAccel accelerometer;

RedBotSensor rightIRSensor = RedBotSensor(A7);
RedBotSensor middleIRSensor = RedBotSensor(A3);
RedBotSensor leftIRSensor = RedBotSensor(A6);

int leftMotorPower, rightMotorPower ;// variables for setting the drive power
int leftIRVal, middleIRVal, rightIRVal;

const int speaker = 9;
int thresholdVal = 995;

// Pins
const int TRIG_PIN = A1;
const int ECHO_PIN = A0;

const unsigned int MAX_DIST = 23200;


void setup(void)
{
    Serial.begin(115200); 
    leftMotorPower = 100;
    rightMotorPower = 100;

    pinMode(speaker, OUTPUT);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop(void)
{

  unsigned long t1;
  unsigned long t2;
  unsigned long pulse_width;
  float cm;
  float inches;

  // Hold the trigger pin high for at least 10 us
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, LOW);

  // Wait for pulse on echo pin
  while ( digitalRead(ECHO_PIN) == 0 );

  // Measure how long the echo pin was held high (pulse width)
  // Note: the micros() counter will overflow after ~70 min
  t1 = micros();
  while ( digitalRead(ECHO_PIN) == 1);
  t2 = micros();
  pulse_width = t2 - t1;

  // Calculate distance in centimeters and inches. The constants
  // are found in the datasheet, and calculated from the assumed speed
  //of sound in air at sea level (~340 m/s).
  cm = pulse_width / 58.0;
  inches = pulse_width / 148.0;

  // Print out results
  if ( pulse_width > MAX_DIST ) {
    leftMotorPower = 0;
  rightMotorPower = 0;
  motors.leftMotor(leftMotorPower);
  motors.rightMotor(rightMotorPower);
  } 
    readSensorValues();
    if(middleIRVal > thresholdVal){
      driveForward();
    }
    else if(leftIRVal > thresholdVal){
      turnRight();
    }
    else if(rightIRVal > thresholdVal){
      turnLeft();
    }
    driveForward();
    
}


void readSensorValues(){
  leftIRVal = leftIRSensor.read();
  rightIRVal = rightIRSensor.read();
}

void turnRight(){
  leftMotorPower = -100;
  rightMotorPower = 150;
  motors.leftMotor(leftMotorPower);
  motors.rightMotor(rightMotorPower);
  delay(100);
}

void turnLeft(){
  leftMotorPower = 150;
  rightMotorPower = -100;
  motors.leftMotor(leftMotorPower);
  
  motors.rightMotor(rightMotorPower);
  delay(100);
}

void driveForward(){
  leftMotorPower = 150;
  rightMotorPower = 150;
  motors.leftMotor(leftMotorPower);
  motors.rightMotor(rightMotorPower);
}