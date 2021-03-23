# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 18:31:19 2020

@author: Donghee Lee
"""


"""
A tracker class for controlling the Tello and some sample code for showing how
it works. you can test it using your webcam or a video file to make sure it works.

it computes a vector of the ball's direction from the center of the
screen. The axes are shown below (assuming a frame width and height of 600x400):
+y                 (0,200)


Y  (-300, 0)        (0,0)               (300,0)


-Y                 (0,-200)
-X                    X                    +X

Based on the tutorial:
https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

Usage:
for existing video:
python tracker.py --video ball_tracking_example.mp4
For live feed:
python tracking.py

@author Leonie Buckley and Jonathan Byrne
@copyright 2018 see license file for details
"""
"""
Created on Thu Feb 13 13:34:25 2020

@author: Donghee Lee
"""
# import the necessary packages
import argparse
import time
import cv2
import imutils
from imutils.video import VideoStream
import numpy as np

"""main 함수는 tello에서는 사용하는 것이 아니고, 이 프로그램 자체를 실행할 때 쓰는 부분"""
def main():
    """Handles inpur from file or stream, tests the tracker class"""
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument("-v", "--video",
                           help="path to the (optional) video file")
    args = vars(arg_parse.parse_args())

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space. NB the hue range in
    # opencv is 180, normally it is 360
    green_lower = (50, 50, 50)
    green_upper = (70, 255, 255)
    # red_lower = (0, 50, 50)
    # red_upper = (20, 255, 255)
    # blue_lower = (110, 50, 50)
    # upper_blue = (130, 255, 255)

    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
        vid_stream = VideoStream(src=0).start()

    # otherwise, grab a reference to the video file
    else:
        vid_stream = cv2.VideoCapture(args["video"])

    # allow the camera or video file to warm up
    time.sleep(2.0)
    stream = args.get("video", False)
    frame = get_frame(vid_stream, stream)
    height, width = frame.shape[0], frame.shape[1]
    greentracker = HSV_Tracker(height, width, green_lower, green_upper)

    # keep looping until no more frames
    more_frames = True
    while more_frames:
        greentracker.hsv_track(frame)
        frame = greentracker.draw_arrows(frame)
        show(frame)
        frame = get_frame(vid_stream, stream)
        if frame is None:
            more_frames = False

    # if we are not using a video file, stop the camera video stream
    if not args.get("video", False):
        vid_stream.stop()

    # otherwise, release the camera
    else:
        vid_stream.release()

    # close all windows
    cv2.destroyAllWindows()


def get_frame(vid_stream, stream):
    """grab the current video frame"""
    frame = vid_stream.read()
    # handle the frame from VideoCapture or VideoStream
    frame = frame[1] if stream else frame
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        return None
    else:
        frame = imutils.resize(frame, width=600)
        return frame


def show(frame):
    """show the frame to cv2 window"""
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        exit()


class HSV_Tracker:
    """이것이 색깔 찾는 class"""
    """
    A basic color tracker, it will look for colors in a range and
    create an x and y offset valuefrom the midpoint
    """

    def __init__(self, height, width, color_lower, color_upper):
        self.color_lower = color_lower
        self.color_upper = color_upper
        self.midx = int(width / 2)
        self.midy = int(height / 2)
        self.xoffset = 0
        self.yoffset = 0

    def draw_arrows(self, frame):
        """Show the direction vector output in the cv2 window"""
        #cv2.putText(frame,"Color:", (0, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, thickness=2)
        cv2.arrowedLine(frame, (self.midx, self.midy),
                        (self.midx + self.xoffset, self.midy - self.yoffset),
                        (0, 0, 255), 5)
        return frame

    def hsv_track(self, frame):
        """Simple HSV color space tracking"""
        """이 함수가 색깔을 찾는 함수"""
        """gaussianblur,erode,dilate등등 기능들이 있는데, 일단 드론영상과 스테이션 영상에 필요한 부분만 골라 씀"""
        """현재 드론은 gaussianblur, erode, dilate 다 안쓴상태"""
        # resize the frame, blur it, and convert it to the HSV
        # color space
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        # hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        # when using without blur
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.color_lower, self.color_upper)
        mask = cv2.erode(mask, None, iterations=5)
        mask = cv2.dilate(mask, None, iterations=5)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] #if imutils.is_cv2() else cnts[1]
        # center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            
            # rect = cv2.minAreaRect(c)
            
            self.x, self.y, self.w, self.h = cv2.boundingRect(c)
            rect = [self.x, self.y, self.w, self.h]
            
            # M = cv2.moments(c)
            # if M["m00"] == 0 :
            #     center = (self.midx,self.midy)
            # else:
            #     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            
            # only proceed if the radius meets a minimum size
            """특정 색깔의 최소반지름 이상의 것들만 찾는것"""
            # if radius > 8:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            # cv2.circle(frame, (int(x), int(y)), int(radius),
            #            (0, 0, 255), 2)
            # cv2.circle(frame, center, 5, (0, 0, 255), -1)

            
            self.label = rect
            # else:
            #     self.xoffset = 0
            #     self.yoffset = 0
            #     self.radius = 0
        else:
            self.x = 0
            self.y = 0
            self.w = 0
            self.h = 0
            self.label = [self.x, self.y, self.w, self.h]
        return self.label
'''
if __name__ == '__main__':
    main()
'''