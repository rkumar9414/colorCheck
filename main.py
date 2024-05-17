import tkinter as tk
import cv2
import numpy as np
from PIL import Image

# bgr values for each color
colors = {
    'Red': (0, 0, 255),
    'Orange': (0, 165, 255),
    'Yellow': (0, 255, 255),
    'Green': (0, 255, 0),
    'Blue': (255, 0, 0)
}

# convert bgr to hex for tkinter button colors
def bgr_to_hex(bgr):
    return "#{:02x}{:02x}{:02x}".format(bgr[2], bgr[1], bgr[0])

def get_limits(color):
    # convert bgr to hsv
    color_bgr = np.uint8([[color]])
    color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV)[0][0]
    
    # color range in hsv
    lower_limit = np.array([color_hsv[0] - 10, 100, 100])
    upper_limit = np.array([color_hsv[0] + 10, 255, 255])
    
    return lower_limit, upper_limit

def color_detection(color):
    cap = cv2.VideoCapture(0)  # video from webcam

    while True:
        ret, frame = cap.read()  #frame by frame

        hsvImageConverted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to hsv

        lowerLimit, upperLimit = get_limits(color)

        mask = cv2.inRange(hsvImageConverted, lowerLimit, upperLimit)  # mask

        maskPIL = Image.fromarray(mask)  # convert to pil for bbox

        boundingbox = maskPIL.getbbox()

        if boundingbox is not None:  # draw bbox if color is detected
            xLeft, yUp, xRight, yDown = boundingbox

            frame = cv2.rectangle(frame, (xLeft, yUp), (xRight, yDown), (0, 255, 0), 5)
            cv2.putText(frame, 'Detected', (xLeft, yUp - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('frame', frame)  # shows the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):  # exit on 'q' key
            break

    cap.release()
    cv2.destroyAllWindows()

def on_button_click(color_name):
    color = colors[color_name]
    color_detection(color)  # calls color detection method when button is clicked

# main application window
root = tk.Tk()
root.title("Color Detection")

#  button for each color
for color_name, bgr in colors.items():
    hex_color = bgr_to_hex(bgr)
    if color_name == 'Yellow' or color_name == 'Green':
        button = tk.Button(root, text=color_name, command=lambda cn=color_name: on_button_click(cn), bg=hex_color, fg='black')
    else:
        button = tk.Button(root, text=color_name, command=lambda cn=color_name: on_button_click(cn), bg=hex_color, fg='white')
    button.pack(pady=5, padx=10, fill=tk.X)

# tkinter event loop
root.mainloop()
