#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// Create the servo driver instance
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Define the min and max pulse lengths
#define SERVOMIN  150 // This is the pulse length count for 0 degrees
#define SERVOMAX  600 // This is the pulse length count for 180 degrees

// Function to map angle to pulse length
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

// Open eyelids
int open_lids_0 = angleToPulse(65); // left top 65
int open_lids_1 = angleToPulse(75); // left bottom 75
int open_lids_2 = angleToPulse(125); // right top 125
int open_lids_3 = angleToPulse(75); // right bottom 75

// Close eyelids
int close_lids_0 = angleToPulse(110); // left top 110
int close_lids_1 = angleToPulse(30); // left bottom 30
int close_lids_2 = angleToPulse(75); // right top 75
int close_lids_3 = angleToPulse(120); // right bottom 120

// Mouth movements
int mouth_open_6 = angleToPulse(100);
int mouth_open_7 = angleToPulse(100);

int mouth_closed_6 = angleToPulse(190);
int mouth_closed_7 = angleToPulse(190);

int mouth_neutral_6 = angleToPulse(140);
int mouth_neutral_7 = angleToPulse(140);



void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(60); // Analog servos run at ~60 Hz
  delay(10); // Wait for initialization

  // Seed the random number generator
  randomSeed(analogRead(A0)); // Read from an unconnected analog pin for randomness
}

void loop() {
  // Talk seconds
  int talk_seconds = random(0, 2);

  // Vertical eyeball range
  int vertical_eye_4 = angleToPulse(random(60, 131)); // Random angle mapped to pulse

  // Horizontal eyeball range
  int horizontal_eye_5 = angleToPulse(random(60, 121)); // Random angle mapped to pulse
  
  // Random number for use in conditional
  int random_num = random(0,10);

  // Print values
  Serial.println(random_num);
  Serial.println(talk_seconds);

  // talk_seconds == 0 (no talking)
  if (talk_seconds == 0) {
    // Conditions
    if (random_num < 3) { // Move eyes 
      // move eyes
      pwm.setPWM(4, 0, vertical_eye_4); // Set servo 4 (vertical eyeball) to random position
      // pwm.setPWM(4, 0, angleToPulse(60)); // low
      // delay(2000);
      // pwm.setPWM(4, 0, angleToPulse(130)); // high
      // delay(2000);


      pwm.setPWM(5, 0, horizontal_eye_5); // Set servo 5 (horizontal eyeball) to random position
      delay(2000); // Wait for servos to reach position
      // pwm.setPWM(5, 0, angleToPulse(60)); // low
      // delay(2000);
      // pwm.setPWM(5, 0, angleToPulse(120)); // high
      // delay(2000); // Wait for servos to reach position
    } 
    
    if (random_num > 7) { // Blink eyes
      // Reset eyes to neutral position before we operate eyelids
      pwm.setPWM(4, 0, angleToPulse(90)); // vertical eyes, neutral position
      pwm.setPWM(5, 0, angleToPulse(90)); // horizontal eyes, neutral position

      // close eyelids
      pwm.setPWM(0, 0, close_lids_0); // Set servo 0 to close top left eyelid position
      pwm.setPWM(1, 0, close_lids_1); // Set servo 1 to close bottom left eyelid position
      pwm.setPWM(2, 0, close_lids_2); // Set servo 2 to close top right eyelid position
      pwm.setPWM(3, 0, close_lids_3); // Set servo 3 to close bottom righ eyelid position
      delay(500); // Wait for servos to reach position

      // open eyelids
      pwm.setPWM(0, 0, open_lids_0); // Set servo 0 to open top left eyelid position
      pwm.setPWM(1, 0, open_lids_1); // Set servo 1 to open bottom left eyelid position
      pwm.setPWM(2, 0, open_lids_2); // Set servo 2 to open top left eyelid position
      pwm.setPWM(3, 0, open_lids_3); // Set servo 3 to open bottom right eyelid position
      delay(2000); // Wait for servos to reach position
    }
  }
  
  // talk_seconds > 0 (yes talking)
  elif (talk_seconds > 0) { // Talk for length of talk_seconds
    // Repeat mouth open and close 7 times
    int count = 0; // Initialize counter
    while (count < talk_seconds * 2) {
      // mouth open
      pwm.setPWM(6, 0, mouth_open_6); // Set servo 6 to open mouth position
      pwm.setPWM(7, 0, mouth_open_7); // Set servo 6 to open mouth position
      delay(250);

      // mouth closed
      pwm.setPWM(6, 0, mouth_closed_6); // Set servo 6 to closed mouth position
      pwm.setPWM(7, 0, mouth_closed_7); // Set servo 6 to closed mouth position
      delay(250);
      count++; // Increment counter
    }

    // mouth neutral
    pwm.setPWM(6, 0, mouth_neutral_6); // Set servo 6 to closed mouth position
    pwm.setPWM(7, 0, mouth_neutral_7); // Set servo 6 to closed mouth position
    delay(200);
  }
}
