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
