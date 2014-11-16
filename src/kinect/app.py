from freenect import sync_get_depth as get_depth, sync_get_video as get_video
import cv
import numpy as np
from Tkinter import *
from tkFileDialog import askopenfilename
import Image, ImageTk

def saveimg():
    global rgb
    (rgb,_) = get_video()
    cv.SaveImage('/tmp/anglerfish-init.jpg', cv.fromarray(np.array(rgb)))

if __name__ == "__main__":
    saveimg()
    root = Tk()

    image = Image.open('/tmp/anglerfish-init.jpg')
    size = image.size
    canvas = Canvas(root, width=size[0], height=size[1])
    canvas.pack()

    img = ImageTk.PhotoImage(image)
    canvas.create_image(0,0,image=img, anchor="nw")

    board_corners = []
    corners_counted = 0

    def get_corner_coords(event):
        global board_corners, corners_counted
        board_corners.append((event.x,event.y))
        canvas.create_oval(event.x - 5, event.y - 5, event.x + 5, event.y + 5, fill='#F00', outline='#F00')
        corners_counted += 1
        if corners_counted == 4:
            root.quit()
            print board_corners
    
    canvas.bind("<Button 1>", get_corner_coords)
    root.mainloop()

def doloop():
    global depth, rgb
    while True:
        # Get a fresh frame
        (depth,_), (rgb,_) = get_depth(), get_video()
        # Build a two panel color image
        d3 = np.dstack((depth,depth,depth)).astype(np.uint8)
        da = np.hstack((d3,rgb))
        # Simple Downsample
        cv.ShowImage('both', cv.fromarray(np.array(da[::2,::2,::-1])))
        cv.WaitKey(5)