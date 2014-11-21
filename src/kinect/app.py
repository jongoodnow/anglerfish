from __future__ import division
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from Tkinter import *
import Image, ImageTk
import time
import urllib2
import matplotlib.pyplot as plt
import sys
from scipy import stats

def save_img():
    global rgb
    (rgb,_) = get_video()
    cv.SaveImage('/tmp/anglerfish-img.jpg', cv.fromarray(np.array(rgb)))


def get_corners():
    save_img()
    root = Tk()

    image = Image.open('/tmp/anglerfish-img.jpg')
    size = image.size
    canvas = Canvas(root, width=size[0], height=size[1])
    canvas.pack()

    img = ImageTk.PhotoImage(image)
    canvas.create_image(0,0,image=img, anchor="nw")

    global board_corners, corners_counted
    board_corners = []
    corners_counted = [0]

    def get_corner_coords(event):
        x, y = event.x, event.y
        board_corners.append((x, y))
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, 
            fill='#F00', outline='#F00')
        corners_counted[0] += 1
        if corners_counted[0] == 4:
            root.quit()
    
    canvas.bind("<Button 1>", get_corner_coords)
    root.mainloop()
    return board_corners


def get_bg_depth():
    global corners
    corners = get_corners()
    mtx = np.matrix(corners)
    mean = mtx.mean(0)
    middle_coords = (int(mean.item((0, 0))), int(mean.item((0, 1))))
    corners_arr = np.array(corners)
    global lower_bound, upper_bound
    lower_bound = np.amin(corners_arr, axis=0)
    upper_bound = np.amax(corners_arr, axis=0)
    global depth
    (depth,_) = get_depth()
    #d3 = np.dstack((depth, depth, depth)).astype(np.uint8)
    d3 = np.array(depth)
    d3 = np.array([y[lower_bound[0]:upper_bound[0]] 
        for y in d3[lower_bound[1]:upper_bound[1]]])
    mean_vertical = d3.min(axis=0)
    return mean_vertical.min(axis=0)


def yposition(x, bg_depth):
    d3 = np.array(depth)
    column = d3[:, x].astype(np.int8)
    columnslice = column[lower_bound[1]:upper_bound[1]]
    mode = stats.mode(columnslice)
    #plt.clf()
    #plt.scatter(np.arange(columnslice.size), columnslice)
    return 128


def main(ip_address):
    bg_depth_orig = get_bg_depth()
    bg_depth_unsigned = bg_depth_orig.astype(np.uint8)
    bg_depth = bg_depth_orig.astype(np.int8)
    print bg_depth
    plt.ion()
    plt.show()
    corners_arr = np.array(corners)
    while True:
        (depth,_) = get_depth()
        depth_array = np.array(depth).astype(np.int8)
        d3 = np.array([y[lower_bound[0]:upper_bound[0]] 
            for y in depth_array[lower_bound[1]:upper_bound[1]]])
        depths_per_x = d3.min(axis=0) - bg_depth
        mean_depths_per_x = d3.mean(axis=0) - bg_depth
        mean_depths_per_x = np.array([i if i < -3 else 0 for i in mean_depths_per_x])
        depths_per_x = np.array([i if i < -3 else 0 for i in depths_per_x])
        minimum = np.amin(mean_depths_per_x)
        if minimum != 0:
            spanleft = None
            spanright = None
            bodyx = None
            for pos, i in enumerate(depths_per_x):
                if spanleft is None:
                    if i < -10:
                        spanleft = pos + 5
                if i < -10:
                    spanright = pos - 5
            for pos, i in enumerate(mean_depths_per_x):
                if i == minimum:
                    bodyx = pos
                    break
            if spanleft == None or spanright == None:
                return

            bodyy = yposition(bodyx, bg_depth)
            bodyz = depth_array[bodyx][bodyy]
            lefty = yposition(spanleft, bg_depth)
            leftz = depth_array[spanleft][lefty]
            righty = yposition(spanright, bg_depth)
            rightz = depth_array[spanright][righty]
            yrange = upper_bound[1] - lower_bound[1]
            xxrange = upper_bound[0] - lower_bound[0]
            if spanleft < bodyx - 25:
                pointx, pointy, pointz = spanleft, lefty, leftz
                urllib2.urlopen(
                    "http://%s:8888/update?pointer=%f,%f&position=%f,%f,%f" %(ip_address,
                    pointx / xxrange / 2, pointy / yrange, spanleft/xxrange, bodyx/xxrange, 
                    spanright/xxrange)).read()
            elif spanright > bodyx + 25:
                pointx, pointy, pointz = spanright, righty, rightz
                urllib2.urlopen(
                    "http://%s:8888/update?pointer=%f,%f&position=%f,%f,%f" %(ip_address,
                    pointx / xxrange / 2, pointy / yrange, spanleft/xxrange, 
                    bodyx/xxrange, spanright/xxrange)).read()
            else:
                urllib2.urlopen(
                    "http://%s:8888/update?pointer=0,0&position=%f,%f,%f" %(ip_address,
                    spanleft/xxrange, bodyx/xxrange, spanright/xxrange)).read()
        else:
            urllib2.urlopen(
                "http://%s:8888/update?pointer=0,0" %ip_address).read()
        plt.clf()
        plt.scatter(np.arange(depths_per_x.size), depths_per_x)
        plt.ylim([-255, 255])
        plt.draw()
    

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Please provide the IP address of the app server as an argument."
    else:
        main(sys.argv[1])