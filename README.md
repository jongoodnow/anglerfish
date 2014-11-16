anglerfish
==========

A presentation app that utilizes the Xbox Kinect to allow the speaker to interact with their presentation.

A HackRPI 2014 Project Keaton Brandt and Jonathan Goodnow.

Setup
-----

Install the applications in requirements.txt.

Clone the repo:

	$ git clone https://github.com/jongoodnow/anglerfish.git

Initialize the server powering the kinect with:

	$ python anglerfish/src/kinect/app.py

When you start, you will see a picture of what your Kinect can see. Click on the four corners of your screen or projection to show it where the projection is.

Initialize the server powering the web app with:

	$ cd src/server
	$ ipython

	In[1]: run -i app

Visit the app on a mobile phone at the IP stated in the console, and visit the presentation page on a large screen or projector. Put the Kinect near the projector so that it faces you.

Features
--------

* Point at the screen or projection to use your finger as a laser pointer.

* Swipe pictures and notes on your phone to show them on the display.

* Thrust your arms outwards to clear all the visible entries.

* Ask your audience to open the app too, so they can ask questions and you can display them with just a swipe.