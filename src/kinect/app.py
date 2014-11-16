from __future__ import division
from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from Tkinter import *
import Image, ImageTk
import time
import urllib2

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
    lower_bound = np.amin(corners_arr, axis=0)
    upper_bound = np.amax(corners_arr, axis=0)
    global depth
    (depth,_) = get_depth()
    #d3 = np.dstack((depth, depth, depth)).astype(np.uint8)
    d3 = np.array(depth)
    d3 = np.array([y[lower_bound[0]:upper_bound[0]] 
        for y in d3[lower_bound[1]:upper_bound[1]]])
    mean_vertical = d3.mean(axis=0)
    return mean_vertical.mean(axis=0).astype(np.uint8)


def yposition(x):
    d3 = np.array(depth)
    column = d3[x].astype(np.uint8)
    ypos = None
    mindepth = 255
    for pos, i in enumerate(column):
        if i < mindepth:
            ypos = pos
            mindepth = i
    return ypos


def main():
    import matplotlib.pyplot as plt
    bg_depth = get_bg_depth()
    print bg_depth
    plt.ion()
    plt.show()
    corners_arr = np.array(corners)
    lower_bound = np.amin(corners_arr, axis=0)
    upper_bound = np.amax(corners_arr, axis=0)
    while True:
        (depth,_) = get_depth()
        depth_array = np.array(depth).astype(np.uint8)
        d3 = np.array([y[lower_bound[0]:upper_bound[0]] 
            for y in depth_array[lower_bound[1]:upper_bound[1]]])
        d3 = d3
        depths_per_x = d3.mean(axis=0) - bg_depth
        depths_per_x = np.array([i if i < -3.5 else 0 for i in depths_per_x])
        minimum = np.amin(depths_per_x)
        if minimum != 0:
            spanleft = None
            spanright = None
            bodyx = None
            for pos, i in enumerate(depths_per_x):
                if spanleft is None:
                    if i < 0:
                        spanleft = pos
                if i < 0:
                    spanright = pos
                if i == minimum:
                    bodyx = pos
            righty = yposition(spanright)
            bodyy = yposition(bodyx)
            rightz = depth_array[spanright][righty]
            bodyz = depth_array[bodyx][bodyy]
            pointz = None
            if spanleft < bodyx - 29:
                pointx = spanleft
                pointy = yposition(spanleft)
                pointz = depth_array[spanleft][pointy]
            elif spanright > bodyx + 29:
                pointx = spanright
                pointy = yposition(spanright)
                pointz = depth_array[spanright][pointy]
            if pointz is not None and pointz < bodyz and pointy != bodyy and pointx != bodyx:
                xzslope = (pointz - bodyz) / (pointx - bodyx)
                yzslope = (pointz - bodyz) / (pointy - bodyy)
                zdiff = bg_depth - bodyz
                xdist = zdiff / xzslope
                ydist = zdiff / yzslope
                xcoord = (xdist + bodyx) / upper_bound[1]
                ycoord = (ydist + bodyy) / upper_bound[0]
                urllib2.urlopen(
                    "http://129.161.90.185:8888/update?pointer=%f,%f" %(xcoord, ycoord)).read()
        plt.clf()
        plt.scatter(np.arange(depths_per_x.size), depths_per_x)
        plt.ylim([-255, 0])
        plt.draw()
    

if __name__ == '__main__':
    main()