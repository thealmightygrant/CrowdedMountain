#!/usr/bin/env python
import cv2
import sys
import numpy as np

class CarVideo:
    def __init__(self, vid_loc=None, display=False):
        self.display = display
        try:
            self.stream = cv2.VideoCapture(vid_loc)
        except:
            print "No video found with name " + vid_loc
            sys.exit(1)
        if not self.stream.isOpened():
            print "video file " + vid_loc + " failed to open."
            sys.exit(1)
        
    def display_flow(self):
        cur_frame = self.grab_next_frame()

        while True:
            next_frame = self.grab_next_frame()
            flow_frame = cv2.calcOpticalFlowFarneback(cur_frame, next_frame, None, pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2, flags=0)
            cur_frame = next_frame
            
            if self.display:
                if flow_frame is not None:
                    cv2.imshow('Flow Vid', self.draw_flow(cur_frame, flow_frame))
                    cv2.waitKey(2000)


    def grab_next_frame(self, cur_frame=None, next_frame=None):
        good_frame, next_color_frame = self.stream.read()
        
        if not good_frame:
            #maybe call this in its own method??
            self.stream.release()
            cv2.destroyAllWindows()
            print "No more frames or frame error"
            sys.exit(0)

        #convert to black and white
        return cv2.cvtColor(next_color_frame, cv2.COLOR_BGR2GRAY)

    #from OpenCV samples at github.com/ltseez/opencv/blob/master/samples
    #seems to work, but is difficult to tell, too many lines
    def draw_flow(self, img, flow, step=16):
        h, w = img.shape[:2]
        y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
        fx, fy = flow[y,x].T
        lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
        lines = lines + 0.5
        lines = np.int32([lines])
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        #error in sample fixed with opencv-polylines-
        #  function-in-python-throws-exception from SO
        cv2.polylines(vis, lines, 0, (0, 255, 0))
        for line in lines:
            for (x1, y1), (x2, y2) in line:
                cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
        return vis

if __name__ == '__main__':
    #run tests
    if len(sys.argv) >= 2:
        video = CarVideo(sys.argv[1], True)
        video.display_flow()
    else:
        print "No video file provided at command line"
