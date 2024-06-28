from zaber_motion import Units
from zaber_motion.ascii import Connection
import numpy as np


def set_origin(a,b):

    axis1.move_absolute(float(a),Units.LENGTH_MILLIMETRES)
    axis2.move_absolute(float(b), Units.LENGTH_MILLIMETRES)


def reset():

    axis1.move_absolute(12.5,Units.LENGTH_MILLIMETRES)
    axis2.move_absolute(12.5, Units.LENGTH_MILLIMETRES)


def left(a):
    axis1.move_relative(float(a), Units.LENGTH_MILLIMETRES)


def right(a):
    axis1.move_relative(-float(a), Units.LENGTH_MILLIMETRES)


def up(a):
    axis2.move_relative(-float(a), Units.LENGTH_MILLIMETRES)


def down(a):
    axis2.move_relative(float(a), Units.LENGTH_MILLIMETRES)


with Connection.open_serial_port("COM5") as connection:
    connection.enable_alerts()

    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))
    print(device_list)

    dev1 = device_list[0]
    dev2 = device_list[1]

    axis1 = dev2.get_axis(1)
    axis2 = dev1.get_axis(1)

    if not axis1.is_homed():
      axis1.home()

    if not axis2.is_homed():
      axis2.home()

    origin = input("Enter your origin in mm(x,y): ")
    a,b = origin.split(",")
    a = float(a)
    b = float(b)
    set_origin(a,b)

    l = input("Enter desired capture length of sample (mm): ")
    l = int(np.ceil(float(l)))
    w = input("Enter desired captre width of sample (mm): ")
    w = int(np.ceil(float(w)))
    s = input("Enter field of view (mm): ")
    o = input("Enter overlap percentage: ")
    step = ((100 - float(o))/100) # Step size for motion
    k = 1 # Image Counter

    for i in range(0,l):
        if (i%2 == 0):
            j = 0
            while(j<w):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                up(step)
                j += 1
                k += 1

        else:
            j = w
            while(j>0):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                down(step)
                j -= 1
                k += 1

        right(step)

# Close the serial port when done
connection.close()