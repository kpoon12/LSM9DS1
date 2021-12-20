from multiprocessing import Process
import sys
import getopt
import csv
import smbus
import time
import RPi.GPIO as GPIO

# Get I2C bus
bus = smbus.SMBus(1)

# GPIO 16 with INT_A/G input
intrrupt_gpio = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(intrrupt_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Check sensor
GyroID = bus.read_byte_data(0x6A, 0x0F)
print ("Sensor ID: %d" %GyroID)

MagID = bus.read_byte_data(0x1C, 0x0F)
print ("Sensor ID: %d" %MagID)

# LSM9DS1 Accel/Gyro address, 0x6A(106)
# Select control register1, 0x10
bus.write_byte_data(0x6A, 0x0C, 0x00)
#bus.write_byte_data(0x6A, 0x10, 0xBB)
#bus.write_byte_data(0x6A, 0x20, 0xA0)
bus.write_byte_data(0x6A, 0x10, 0xBB)
bus.write_byte_data(0x6A, 0x20, 0xA0)
bus.write_byte_data(0x6A, 0x0C, 0x82)
time.sleep(0.5)

# LSM9DS1 Mag address, 0x1C
bus.write_byte_data(0x1C, 0x22, 0x24)
time.sleep(0.5)

cmd = 0;

def func_input_cmd():
    global cmd;
    print ("Please")
    #cmd = input()
    while (True):
       if (cmd == 1):
           print("Start print output")
       
def func_get_sensor_data():
    num_row = 0
    f = open('csv_file.csv', 'w')
    writer = csv.writer(f)
    header = ["Index", "ts", "xGyro", "yGyro", "zGyro", "xAccl", "yAccl", "zAccl", "xMag", "yMag", "zMag"]
    writer.writerow(header)

    while (num_row < 200):
        if GPIO.input(intrrupt_gpio):
            ts = time.time()

            # LSM9DS0 Gyro address, 0x6A(106)
            # Read data back from 0x28(40), 2 bytes
            # X-Axis Gyro LSB, X-Axis Gyro MSB
            data0 = bus.read_byte_data(0x6A, 0x28)
            data1 = bus.read_byte_data(0x6A, 0x29)

            # Convert the data
            xGyro = data1 * 256 + data0
            if xGyro > 32767 :
                xGyro -= 65536

            # LSM9DS0 Gyro address, 0x6A(106)
            # Read data back from 0x2A(42), 2 bytes
            # Y-Axis Gyro LSB, Y-Axis Gyro MSB
            data0 = bus.read_byte_data(0x6A, 0x2A)
            data1 = bus.read_byte_data(0x6A, 0x2B)

            # Convert the data
            yGyro = data1 * 256 + data0
            if yGyro > 32767 :
                yGyro -= 65536

            # LSM9DS0 Gyro address, 0x6A(106)
            # Read data back from 0x2C(44), 2 bytes
            # Z-Axis Gyro LSB, Z-Axis Gyro MSB
            data0 = bus.read_byte_data(0x6A, 0x2C)
            data1 = bus.read_byte_data(0x6A, 0x2D)

            # Convert the data
            zGyro = data1 * 256 + data0
            if zGyro > 32767 :
                zGyro -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x28(40), 2 bytes
            # X-Axis Accl LSB, X-Axis Accl MSB
            data0 = bus.read_byte_data(0x6A, 0x18)
            data1 = bus.read_byte_data(0x6A, 0x19)

            # Convert the data
            xAccl = data1 * 256 + data0
            if xAccl > 32767 :
                xAccl -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x2A(42), 2 bytes
            # Y-Axis Accl LSB, Y-Axis Accl MSB
            data0 = bus.read_byte_data(0x6A, 0x1A)
            data1 = bus.read_byte_data(0x6A, 0x1B)

            # Convert the data
            yAccl = data1 * 256 + data0
            if yAccl > 32767 :
                yAccl -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x2C(44), 2 bytes
            # Z-Axis Accl LSB, Z-Axis Accl MSB
            data0 = bus.read_byte_data(0x6A, 0x1C)
            data1 = bus.read_byte_data(0x6A, 0x1D)

            # Convert the data
            zAccl = data1 * 256 + data0
            if zAccl > 32767 :
                zAccl -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x08(08), 2 bytes
            # X-Axis Mag LSB, X-Axis Mag MSB
            data0 = bus.read_byte_data(0x1C, 0x28)
            data1 = bus.read_byte_data(0x1C, 0x29)

            # Convert the data
            xMag = data1 * 256 + data0
            if xMag > 32767 :
                xMag -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x0A(10), 2 bytes
            # Y-Axis Mag LSB, Y-Axis Mag MSB
            data0 = bus.read_byte_data(0x1C, 0x2A)
            data1 = bus.read_byte_data(0x1C, 0x2B)

            # Convert the data
            yMag = data1 * 256 + data0
            if yMag > 32767 :
                yMag -= 65536

            # LSM9DS0 Accl and Mag address, 0x1E(30)
            # Read data back from 0x0C(12), 2 bytes
            # Z-Axis Mag LSB, Z-Axis Mag MSB
            data0 = bus.read_byte_data(0x1C, 0x2C)
            data1 = bus.read_byte_data(0x1C, 0x2D)

            # Convert the data
            zMag = data1 * 256 + data0
            if zMag > 32767 :
                zMag -= 65536
            
            sensor_data = []
            sensor_data.extend((num_row, ts, xGyro, yGyro, zGyro, xAccl, yAccl, zAccl, xMag, yMag, zMag))
            num_row += 1
            writer.writerow(sensor_data)
            print (sensor_data)
            # Output data to screen
            #print ("X-Axis of Rotation : %d" %xGyro)
            #print ("Y-Axis of Rotation : %d" %yGyro)
            #print ("Z-Axis of Rotation : %d" %zGyro)
            #print ("Acceleration in X-Axis : %d" %xAccl)
            #print ("Acceleration in Y-Axis : %d" %yAccl)
            #print ("Acceleration in Z-Axis : %d" %zAccl)
            #print ("Magnetic field in X-Axis : %d" %xMag)
            #print ("Magnetic field in Y-Axis : %d" %yMag)
            #print ("Magnetic field in Z-Axis : %d" %zMag)
                    
    f.close()
    
if __name__=='__main__':
    p1 = Process(target = func_input_cmd)
    p1.start()
    p2 = Process(target = func_get_sensor_data)
    p2.start()
    # This is where I had to add the join() function.
    p1.join()
    p2.join()
