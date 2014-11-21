anglerfish
==========

A presentation app that utilizes the Xbox Kinect to allow the speaker to interact with their presentation.

A HackRPI 2014 Project Keaton Brandt and Jonathan Goodnow.

Setup
-----

Clone the repo:

	$ git clone https://github.com/jongoodnow/anglerfish.git
	$ cd anglerfish

Install the prerequisites:

	$ pip install tornado
	$ sudo apt-get install -r requirements.txt

Start the server powering the web app with:

	$ ./runapp

The server for running the Kinect has only been tested on Ubuntu 14.04 LTS. You may need to run these commands before you can get output from the Kinect:

	$ sudo modprobe -r gspca_kinect 
	$ sudo modprobe -r gspca_main

Now start the server powering the Kinect with:

	$ ./runkinect <IP ADDRESS>

where <IP ADDRESS> is the IP of the server running the web app. When you start, you will see a picture of what your Kinect can see. Click on the four corners of your screen or projection to tell it where the projection is.

Visit the app on a mobile phone at the IP stated in the console, and visit the presentation page on a large screen or projector. Put the Kinect near the projector so that it faces you.

On your projector/display, go to `<IP ADDRESS>:8888/render/index.html` in a web browser.

On your mobile phone or laptop, go to `<IP ADDRESS>:8888/control/index.html`.

Finally, tell your audience to `<IP ADDRESS>:8888/contribute/index.html` so they can ask you questions or send you comments, pictures, or videos.

Now you're ready to present, good luck!

Features
--------

* Point at the screen or projection to use your finger as a laser pointer.

* Swipe pictures and notes on your phone to show them on the display.

* Thrust your arms outwards to clear all the visible entries.

* Ask your audience to open the app too, so they can ask questions and you can display them with just a swipe.