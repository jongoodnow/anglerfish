from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from Tkinter import *
import Image, ImageTk
import time

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
    global depth
    (depth,_) = get_depth()
    d3 = np.dstack((depth, depth, depth)).astype(np.uint8)
    return d3[middle_coords[0]][middle_coords[1]][0]


def main():
    import matplotlib.pyplot as plt
    bg_depth = get_bg_depth()
    plt.ion()
    plt.show()
    while True:
        (depth,_) = get_depth()
        d3 = np.array(depth) #np.dstack((depth, depth, depth)).astype(np.uint8)
        corners_arr = np.array(corners)
        lower_bound = np.amin(corners_arr, axis=0)
        upper_bound = np.amax(corners_arr, axis=1)
        d3 = d3[lower_bound[0]:upper_bound[0], lower_bound[1]:upper_bound[1]]
        #fixed_depth = np.subtract(d3[:][:, 0], bg_depth)
        depths_per_x = d3.mean(axis=0)
        #cv.ShowImage('both',cv.fromarray(d3))
        #cv.WaitKey(5)
        #depth_hist = np.histogram(fixed_depth, bins=np.arange(320))
        plt.clf()
        plt.plot(np.arange(depths_per_x.size), depths_per_x)
        plt.draw()
    


if __name__ == '__main__':
    main()