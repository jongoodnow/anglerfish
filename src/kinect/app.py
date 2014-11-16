from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from Tkinter import *
import Image, ImageTk

def save_img():
    global rgb
    (rgb,_) = get_video()
    cv.SaveImage('/tmp/anglerfish-img.jpg', cv.fromarray(np.array(rgb)))


def save_depth():
    global depth
    (depth,) = get_depth()
    cv.SaveImage('/tmp/anglerfish-depth.jpg', cv.fromarray(np.array(depth)))


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
    corners = get_corners()
    mtx = np.matrix(corners)
    mean = mtx.mean(0)
    middle_coords = (int(mean.item((0, 0))), int(mean.item((0, 1))))
    #save_depth()
    #im = Image.open('/tmp/anglerfish-depth.jpg')
    #pix = im.load()
    #return pix[middle_coords[0]][middle_coords[1]]
    (depth,_) = get_depth()
    d3 = np.dstack((depth,depth,depth)).astype(np.uint8)
    return d3[middle_coords[0]][middle_coords[1]][0]