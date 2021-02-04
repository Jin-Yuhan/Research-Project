/*
 * @author: Jin Yuhan
 * @date: 2020-12-16 17:06:53
 * @lastTime: 2020-12-26 19:05:26
 */

#include "gyro.h"

Gyro::Gyro(void)
{
  this->dataHandler = NULL;
  this->isDataValid = true;
  this->ucRxSum = 0;
  this->ucRxCount = 0;

  // memset(&this->dataCache, 0, sizeof(GyroData));
  // memset(this->ucRxBuffer, 0, sizeof(unsigned char) * RX_BUFFER_LEN);
}

void Gyro::Update(unsigned char ucData)
{
  this->ucRxBuffer[this->ucRxCount++] = ucData;

  if (ucRxBuffer[0] != 0x55)
  {
    this->ucRxCount = 0;
    return;
  }

  if (this->ucRxCount < RX_BUFFER_LEN)
  {
    this->ucRxSum += ucData;
  }
  else
  {
    // 进入到该分支时，ucData是SUM的值，被写入了缓冲区的[10]
    bool isValid = (this->ucRxSum == ucData);

    switch (this->ucRxBuffer[1])
    {
    case 0x51:
      this->isDataValid &= isValid;
      memcpy(&this->dataCache.Acceleration, &ucRxBuffer[2], sizeof(Vector3));
      break;

    case 0x52:
      this->isDataValid &= isValid;
      memcpy(&this->dataCache.AngularVelocity, &ucRxBuffer[2], sizeof(Vector3));
      break;

    case 0x53:
      memcpy(&this->dataCache.Rotation, &ucRxBuffer[2], sizeof(Vector3));

      if (this->dataHandler && this->isDataValid && isValid)
      {
        // 为 dataCache 创建一个防御性副本
        this->dataHandler(this->dataCache); // 触发事件
      }

      this->isDataValid = true;
      break;
    }

    this->ucRxSum = 0;
    this->ucRxCount = 0;
  }
}

void Gyro::OnFinishReceivingData(GyroDataHandler handler)
{
  this->dataHandler = handler;
}
