/*
 * @author: Jin Yuhan
 * @date: 2020-11-25 13:53:59
 * @lastTime: 2021-01-27 15:47:33
 */

// #define ARDUINO_DEBUG

#include "gyro.h"
#include "pressures.h"
#include "py_package.h"
#include <SoftwareSerial.h>

#define BAUDRATE 9600
#define DELAY 0

uint8_t sensors[PRESSURE_SENSOR_COUNT] = {A0, A1, A2, A3, A4, A5};

Gyro gyro;
Pressures pressures(sensors);
SoftwareSerial rpiSerial(2, 3); // RX=2, TX=3

void setup()
{
  gyro.OnFinishReceivingData(SendPackage);

  Serial.begin(BAUDRATE);
  rpiSerial.begin(BAUDRATE);
}

void loop()
{
  while (Serial.available())
  {
    gyro.Update(Serial.read());
  }

  delay(DELAY);
}

void SendPackage(GyroData data)
{
#ifdef ARDUINO_DEBUG
  Serial.print("Acceleration:");
  Serial.print((float)data.Acceleration.X / 32768 * 16 * 9.8f, 4);
  Serial.print(" ");
  Serial.print((float)data.Acceleration.Y / 32768 * 16 * 9.8f, 4);
  Serial.print(" ");
  Serial.println((float)data.Acceleration.Z / 32768 * 16 * 9.8f, 4);

  Serial.print("AngularVelocity:");
  Serial.print((float)data.AngularVelocity.X / 32768 * 2000, 4);
  Serial.print(" ");
  Serial.print((float)data.AngularVelocity.Y / 32768 * 2000, 4);
  Serial.print(" ");
  Serial.println((float)data.AngularVelocity.Z / 32768 * 2000, 4);

  Serial.print("Rotation:");
  Serial.print((float)data.Rotation.X / 32768 * 180, 4);
  Serial.print(" ");
  Serial.print((float)data.Rotation.Y / 32768 * 180, 4);
  Serial.print(" ");
  Serial.println((float)data.Rotation.Z / 32768 * 180, 4);
#else
  PyPackage package;
  package.Flag0 = PACKAGE_FLAG_0;
  package.Flag1 = PACKAGE_FLAG_1;
  package.GyroData = data;
  pressures.ReadData(package.PressureData);
  
  rpiSerial.write((char *)&package, sizeof(PyPackage));
#endif
}
