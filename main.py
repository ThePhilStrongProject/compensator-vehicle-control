from imu import MPU6050
from time import sleep, ticks_ms
from machine import Pin, I2C
import math

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

previousTime = ticks_ms()
currentTime = ticks_ms()
gyroAngleX = 0
gyroAngleY = 0
accAngleX = 0
accAngleY = 0
roll = 0
pitch = 0
yaw = 0

while True:
    AccX=round(imu.accel.x,2)
    AccY=round(imu.accel.y,2)
    AccZ=round(imu.accel.z,2)
    GyroX=round(imu.gyro.x)
    GyroY=round(imu.gyro.y)
    GyroZ=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    #print("ax",ax,"\t","ay",ay,"\t","az",az,"\t","gx",gx,"\t","gy",gy,"\t","gz",gz,"\t","Temperature",tem,"        ",end="\r")
    
    # Calculating Roll and Pitch from the accelerometer data
    accAngleX = (math.atan(AccY / math.sqrt(math.pow(AccX, 2) + math.pow(AccZ, 2))) * 180 / math.pi) - 0.58 # AccErrorX ~(0.58) See the calculate_IMU_error()custom function for more details
    accAngleY = (math.atan(-1 * AccX / math.sqrt(math.pow(AccY, 2) + math.pow(AccZ, 2))) * 180 / math.pi) + 1.58 # AccErrorY ~(-1.58)
  
    # === Read gyroscope data === //
    previousTime = currentTime # Previous time is stored before the actual time read
    currentTime = ticks_ms() # Current time actual time read
    elapsedTime = (currentTime - previousTime) / 1000; # Divide by 1000 to get seconds

    # Correct the outputs with the calculated error values
    GyroX = GyroX + 0.56 # GyroErrorX ~(-0.56)
    GyroY = GyroY - 2 # GyroErrorY ~(2)
    GyroZ = GyroZ + 0.79 # GyroErrorZ ~ (-0.8)
  
    # Currently the raw values are in degrees per seconds, deg/s, so we need to multiply by sendonds (s) to get the angle in degrees
    gyroAngleX = roll + GyroX * elapsedTime # deg/s * s = deg
    gyroAngleY = pitch + GyroY * elapsedTime
    yaw =  yaw + GyroZ * elapsedTime
    
    # Complementary filter - combine acceleromter and gyro angle values
    roll = 0.9 * gyroAngleX + 0.1 * accAngleX
    pitch = 0.9 * gyroAngleY + 0.1 * accAngleY
    print("roll: ", round(roll,2), "\tpitch: ", round(pitch,2), "\ttime: ", elapsedTime)
    
