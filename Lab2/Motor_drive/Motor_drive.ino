/***********************************************************************
 * Exp6_2_LineFollowing_IRSensors
 *
 * This code reads the three line following sensors on A3, A6, and A7
 * and controls the motor speed for the robot drive. 
 *
 ***********************************************************************/

#include <RedBot.h>
RedBotSensor left = RedBotSensor(A3);   // initialize a left sensor object on A3
RedBotSensor center = RedBotSensor(A6); // initialize a center sensor object on A6
RedBotSensor right = RedBotSensor(A7);  // initialize a right sensor object on A7

// constants that are used in the code. LINETHRESHOLD is the level to detect 
// if the sensor is on the line or not. If the sensor value is greater than this
// the sensor is above a DARK line.
//
// SPEED sets the nominal speed

#define LINETHRESHOLD 800
#define SPEED 60  // sets the nominal speed.

RedBotMotors motors;
int leftSpeed;   // variable used to store the leftMotor speed
int rightSpeed;  // variable used to store the rightMotor speed

void setup()
{
	Serial.begin(9600);
	Serial.println("Welcome to experiment 6.2 - Line Following");
	Serial.println("------------------------------------------");
	delay(2000);
	Serial.println("IR Sensor Readings: ");
	delay(500);
}

void loop()
{
	Serial.print(left.read());
	Serial.print("\t");  // tab character
	Serial.print(center.read());
	Serial.print("\t");  // tab character
	Serial.print(right.read());
	Serial.println();

	// if ther is no line under the sensor drive left and right at the same speed (left is CCW / right is CW)
	if(center.read() > LINETHRESHOLD)
	{
		leftSpeed = 250; 
		rightSpeed = 250;
	}
	
	// if the line is under the right sensor, adjust relative speeds to turn to the right
	else if(right.read() > LINETHRESHOLD)
	{
		leftSpeed = 100;
		rightSpeed = 250;
	}

	// if the line is under the left sensor, adjust relative speeds to turn to the left
	else if(left.read() > LINETHRESHOLD)
	{
		leftSpeed = 250;
		rightSpeed = 100;
	}
	
	// if all sensors are on black or up in the air, stop the motors.
	// otherwise, run motors given the control speeds above.
	if((left.read() > LINETHRESHOLD) && (center.read() > LINETHRESHOLD) && (right.read() > LINETHRESHOLD) )
	{
		motors.stop();
	}
	else
	{
		motors.leftMotor(leftSpeed);
		motors.rightMotor(rightSpeed);
		
	}
	delay(0);  // add a delay to decrease sensitivity.
}
