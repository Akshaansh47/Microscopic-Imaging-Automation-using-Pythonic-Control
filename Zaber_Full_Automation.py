from zaber_motion import Units
from zaber_motion.ascii import Connection
import numpy as np
import keyboard
import pyautogui


def automatic():
    l = input("Enter desired capture length of sample (mm): ")
    l = int(np.ceil(float(l)))
    w = input("Enter desired capture width of sample (mm): ")
    w = int(np.ceil(float(w)))
    s = input("Enter field of view (mm): ")
    o = input("Enter overlap percentage: ")
    step = ((100 - float(o)) / 100)  # Step size for motion
    return l,w,step


def manual():
    sn_type = input("Would you like to:\n"
                    "1. Snake by rows?\n"
                    "2. Snake by columns?\n")
    sn_type = int(sn_type)
    if sn_type == 1:
        row_manual()
    elif sn_type == 2:
        col_manual()


def input_step():
    step = input("Enter step size in mm: ")
    print("Thank you. If you would like to change your step size at any point, press 'c'.")
    print("Please use arrow keys to navigate. Hit 'f' to finish\n")
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
    pyautogui.press('backspace')


def set_origin():
    origin = input("Enter your origin in mm(x,y): ")
    a, b = origin.split(",")
    axis1.move_absolute(float(a), Units.LENGTH_MILLIMETRES)
    axis2.move_absolute(float(b), Units.LENGTH_MILLIMETRES)


def col_manual():
    l,w,step = automatic()
    i = 0
    j = 0
    k = 0 # Image counter
    while i<l:
        if (i % 2 == 0):
            j = 0
            while (j < w):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                if keyboard.is_pressed('spacebar'):
                    up(step)
                    j += 1
                    k += 1

        else:
            j = w
            while (j > 0):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                if keyboard.is_pressed('spacebar'):
                    down(step)
                    j -= 1
                    k += 1
        keyboard.wait('spacebar')
        right(step)
        i += 1


def row_manual():
    l,w,step = automatic()
    i = 0
    j = 0
    k = 0 # Image counter
    while i<w:
        if (i % 2 == 0):
            j = 0
            while (j < l):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                if keyboard.is_pressed('spacebar'):
                    right(step)
                    j += 1
                    k += 1

        else:
            j = l
            while (j > 0):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                if keyboard.is_pressed('spacebar'):
                    left(step)
                    j -= 1
                    k += 1
        keyboard.wait('spacebar')
        up(step)
        i += 1


def snake_columns():
    l, w, step = automatic()
    k = 0  # Image counter
    for i in range(0, l):
        if (i % 2 == 0):
            j = 0
            while (j < w):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                up(step)
                j += 1
                k += 1

        else:
            j = w
            while (j > 0):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                down(step)
                j -= 1
                k += 1

        right(step)


def snake_rows():
    l, w, step = automatic()
    k = 0  # Image counter
    for i in range(0, w):
        if (i % 2 == 0):
            j = 0
            while (j < l):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                right(step)
                j += 1
                k += 1

        else:
            j = l
            while (j > 0):
                # get_image()
                # save_image(tile_{k}.tif) to directory
                left(step)
                j -= 1
                k += 1

        up(step)


def reset():
    axis1.move_absolute(12.5, Units.LENGTH_MILLIMETRES)
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

    option = input("Welcome! Would you like to:\n"
                   "1. Move the Zaber manually (with your keyboard)\n"
                   "2. Snake automatically for sample inspection?\n"
                   "3. Snake for image capture (using spacebar).\n")
    option = int(option)

    set_in = input("Set origin by coordinates (1) or manually by keyboard (2)?\n")
    set_in = int(set_in)
    if set_in == 1:
        set_origin()
    elif set_in == 2:
        free_move()

    if option == 1:
        print("You have chosen to move the Zaber stages manually")
        free_move()
    elif option == 2:
        sn = input("1. Snake by rows? \n2. Snake by columns?\n")
        sn = int(sn)
        if sn == 1:
            snake_rows()
        elif sn == 2:
            snake_columns()
    elif option == 3:
        manual()
    else:
        print("Invalid, try again")


# Close the serial port when done
connection.close()