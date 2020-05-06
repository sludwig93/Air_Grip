int prescaler = 256; // set this to match whatever prescaler value you set in CS registers below

// intialize values for the PWM duty cycle set by pots
float potDC1 = 0;
float potDC2 = 0;
float potDC3 = 0;
float potDC4 = 0;

#include <PID_v1.h>

double Setpoint ;
double Input ;
double Output ;
double Kp=18;     //18    //30
double Ki=0;    //0   //0.2
double Kd=0.025  ;    //0.025   //3

PID myPID(&Input, &Output, &Setpoint, Kp, Ki, Kd, DIRECT);

int bfset = 40; // set pressure target for back flow

void setup() {

  Serial.begin(9600);

  Setpoint = 42; // set pressure target for claw (max pressure of 50)
  
  myPID.SetMode(AUTOMATIC);
  myPID.SetTunings(Kp, Ki, Kd);

  // input pins for valve switches
  pinMode(50, INPUT);
  pinMode(51, INPUT);
  pinMode(52, INPUT);
  pinMode(53, INPUT);

  // output pins for valve PWM
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);

  int eightOnes = 255;  // this section speeds up PID reaction
  TCCR3A &= ~eightOnes;   // this operation (AND plus NOT), set the eight bits in TCCR registers to 0 
  TCCR3B &= ~eightOnes;
  TCCR4A &= ~eightOnes;
  TCCR4B &= ~eightOnes;

  // set waveform generation to frequency and phase correct, non-inverting PWM output. again this speeds up PID reaction 
  TCCR3A = _BV(COM3A1);
  TCCR3B = _BV(WGM33) | _BV(CS32);
  
  TCCR4A = _BV(COM4A1) | _BV(COM4B1) | _BV(COM4C1);
  TCCR4B = _BV(WGM43) | _BV(CS42);
}

void pPWM(float pwmfreq, float pwmDC1, float pwmDC2, float pwmDC3, float pwmDC4) {

  // set PWM frequency by adjusting ICR (top of triangle waveform)
  ICR3 = F_CPU / (prescaler * pwmfreq * 2);
  ICR4 = F_CPU / (prescaler * pwmfreq * 2);
  
  // set duty cycles
  OCR3A = (ICR4) * (pwmDC1 * 0.01);
  OCR4A = (ICR4) * (pwmDC2 * 0.01);
  OCR4B = (ICR4) * (pwmDC3 * 0.01);
  OCR4C = (ICR4) * (pwmDC4 * 0.01);
}

void loop() {


  if (Serial.available()) { 
    //only if RPi is communicating with Arduino
    int engage = (Serial.read() - '0'); //this will report either a 1 or a 0. 1 will start claw inflation, 0 will stop inflation
    if (engage == 1) {
      potDC2 = analogRead(A2)*100.0/1024.0;
      float potPWMfq = analogRead(A7)*100.0/1024.0; // scale values from pot to 0 to 100, which gets used for frequency (Hz)
      potPWMfq = round(potPWMfq/5)*5+1; //1 to 91 Hz in increments of 5 (rounding helps to deal with noisy pot)
  
      int Raw = analogRead(A8); //set value of raw to frequency value read by claw pressure sensor
      Input=Raw; //change raw to Input value needed for PID function to work
      Input = map(Raw, 90, 200, 0, 50); //scaling range from 90-200 to 0-50
      myPID.Compute(); //computing PID
      Output=map(Output,0,255,0,100); //scaling kHZ output to potentiometer values for solenoid
      potDC2=Output;

      // update PWM output based on the above values from pots
      pPWM(potPWMfq,potDC1,potDC2,potDC3,potDC4);

      // transfer function for sensor Honeywell ABPDANT015PGAA5 (15 psi, 5V, A-calibration): Papplied = (Vout/Vsupply - 0.1)*(Pmax - Pmin)/0.8 + Pmin;

      // read output voltages from sensors and convert to pressure reading in PSI
      float P1 = (analogRead(A8)/1024.0 - 0.1)*100.0/0.8;
      float BackP= ((analogRead(A13)/1024.0-0.04)/0.0018)*0.145;
      if (potDC2 <= 10) { //if 2nd solenoid is barely open
        int Bf = analogRead(A13); //set value of Bf to frequency value read by backflow pressure sensor
        if (Bf >= bfset) { //if backflow sensor value is greater than set pressure goal
          analogWrite(8,125); //open 4th solenoid halfway
        }
        else {
        analogWrite(8,0); //close 4th solenoid completely
        }
      }
      else {
        analogWrite(8,0); //if 2nd solenoid is open more than 10% then keep 4th solenoid closed
      }
      // print pressure readings
      //Serial.print("Input ");Serial.print(Input);Serial.print("\t");
      //Serial.print("Pressure = "); Serial.print(P1); Serial.print("\t");
      //Serial.print("Backpressure = "); Serial.print(BackP); Serial.print("\n");
      }
  }
}
