# Microscopic-Imaging-Automation-using-Pythonic-Control

**Overview**

The goal is to automate the motion of actuating stages with a sample on them, capture images of a set location and traverse through the entire sample space, and finally stitch all the images into the desired "microscopic profile" of the sample.

**About**

The process of microscopic imaging requires the continuous motion of the sample across a desired field of view. This is achieved by using mechanical (actuating) stages that are controlled by electronic signals fed through a software. Once this motion can be simulated successfully, the next goal is to use a camera to capture images at each location. The images taken by the camera need to be saved in order to be stitched together post-processing and obtain a good microscopic view of the desired sample dimension.

**Functionality**

This project aims to automate this process in two ways:
1. Complete automation, wherein the user has no reason to change the focus of the camera at any point in the actuating and imaging process.
2. Partial automation, wherein the user has to constantly change the focus of the camera at each point in the motion of the stages.

**Hardware & Software**

The software that are used for these purposes are:
1. Actuating stages (Zaber X-LRM025A-E03 x 2) - Zaber Launcher
2. Camera (Teledyne FLIR Grasshopper3 USB) - PointGrey FlyCapture2
3. Image Stitching (Software) - Fiji ImageJ

**APIs for Pythonic implementation**

The suggested APIs for the Pythonic control that would achieve these levels of automation are:
1. Zaber Motion - https://software.zaber.com/motion-library/docs/tutorials/install/py
2. Rotpy (using Spinnaker SDK) - https://github.com/matham/rotpy
3. PyImageJ - https://github.com/imagej/pyimagej

# Zaber Full Automation Guide:

The motion discussed in this section is intended to control what is being seen on the camera, more than the actual motion of the stages. The idea is that the stages actually move in the direction opposite to that of the actual motion, which results in the image displayed on the screen to move in the intended direction. This also helps with the stitching process.
The code to optimize the Zaber stages has 3 primary functions, each of which can be accessed using the input prompts that are coded into the script. Once the user decides the function, they set the origin either by entering coordinates or via manual actuation.

**1. User-controlled motion (for inspection):**

This is a completely free-form motion environment, wherein one can control the motion of the stages using the arrow keys on the keyboard. It is characterized by the free_move() function, which enables completely user-defined motion, down to the desired step size. The primary purpose of this mode is for simple inspection pre-imaging, wherein the user can get an understanding of the area of the sample they'd like to capture.

**2. Fully automated snaking (for setup):**

This is an environment that allows the user to automate the snaking process as desired (either by rows or columns). For now, this is useful for inspection and confirmation that their snaking process will allow for a complete capture as desired by them. It is characterized by the snake_rows() and snake_columns() functions and will be modified in the future to include camera capture and image stitching functionality for further automation.

**3. User-automated snaking (for imaging):**

This environment combines 1 & 2, providing the user with a mode where they can perform the snaking manually. This would be helpful in case camera settings are required to be changed at each stage, with the 'spacebar' key resulting in the continuation of the motion as desired. Once the user inputs their snaking pattern, they control the step size and the motion of the stages, in order to manually capture images at each desired point. It is characterized by the col_manual() and row_manual() functions and is currently the best option for surfaces with varying depths, since these surfaces require constant refocusing for enhanced image clarity.

**4. Fully automated (for snaking, imaging and saving):**

This environment brings together all functionalities to enable the user to simply hit 'enter' after inputting their desired outcomes. The code runs the Zaber stages and automatically clicks and saves the pictures in real time. A slight delay is added in order to negate the motion artifacts brought about by the rapid consistent motion, which allows for clearer images. This mode is particularly useful in case there is no constant refocussing required with the camera, and cuts down runtime to much less than it would be. The saved files are initialized with the ImageJ stitching format.
