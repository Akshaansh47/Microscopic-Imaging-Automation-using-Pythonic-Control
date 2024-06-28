import msvcrt

from zaber_motion import Units
from zaber_motion.ascii import Connection
import numpy as np
import keyboard
import pyautogui


def input_step():
    step = input("Enter step size in mm: ")
    print("Thank you. If you would like to change your step size at any point, press 'c'.")
    print("Please use arrow keys to navigate to your origin. Hit 'f' to finish")
    return float(step)


def free_move():

    step = input_step()
    while not keyboard.is_pressed('f'):
        if keyboard.is_pressed('left'):
            left(step)
            pyautogui.press('right')
        elif keyboard.is_pressed('right'):
            right(step)
            pyautogui.press('left')
        elif keyboard.is_pressed('up'):
            up(step)
            pyautogui.press('down')
        elif keyboard.is_pressed('down'):
            down(step)
            pyautogui.press('up')
        elif keyboard.is_pressed('c'):
            pyautogui.press('backspace')
            step = input_step()
        else:
            continue


def set_origin(a,b):

    axis1.move_absolute(float(a),Units.LENGTH_MILLIMETRES)
    axis2.move_absolute(float(b), Units.LENGTH_MILLIMETRES)


def reset():

    axis1.move_absolute(12.5,Units.LENGTH_MILLIMETRES)
    axis2.move_absolute(12.5, Units.LENGTH_MILLIMETRES)


def left(a):
    try:
        axis1.move_relative(float(a), Units.LENGTH_MILLIMETRES)
    except Exception:
        print("Out of Range - left")

def right(a):
    try:
        axis1.move_relative(-float(a), Units.LENGTH_MILLIMETRES)
    except Exception:
        print("Out of Range - right")

def up(a):
    try:
        axis2.move_relative(-float(a), Units.LENGTH_MILLIMETRES)
    except Exception:
        print("Out of Range - up")

def down(a):
    try:
        axis2.move_relative(float(a), Units.LENGTH_MILLIMETRES)
    except Exception:
        print("Out of Range - down")

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


    print("Done")
    origin = input("Enter your origin in mm(x,y): ")
    a,b = origin.split(",")
    a = float(a)
    b = float(b)
    set_origin(a,b)
    free_move()


    l = input("Enter desired capture length of sample (mm): ")
    l = int(np.ceil(float(l)))
    w = input("Enter desired capture width of sample (mm): ")
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