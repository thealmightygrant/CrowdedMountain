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
            flow_frame = cv2.calcOpticalFlowFarneback(cur_frame, next_frame, None, pyr_scale=0.5, levels=3, winsize=15, iterations=1, poly_n=5, poly_sigma=1.2, flags=0)
            cur_frame = next_frame
            
            if self.display:
                if flow_frame is not None:
                    cv2.imshow('Flow Vid', self.draw_flow(cur_frame, flow_frame))
                    cv2.waitKey(100)


    def grab_next_frame(self):
        good_frame, next_color_frame = self.stream.read()
        
        if not good_frame:
            #maybe call this in its own method??
            self.stream.release()
            cv2.destroyAllWindows()
            print "No more frames or frame error"
            sys.exit(0)

        #convert to black and white
        return cv2.cvtColor(next_color_frame, cv2.COLOR_BGR2GRAY)

    #modified version from OpenCV samples at 
    #github.com/ltseez/opencv/blob/master/samples
    #used regular lines instead of polylines, removed
    # indices that have no movement, and removed circles at points
    def draw_flow(self, img, flow, step=4):
        h, w = img.shape[:2]
        #print 'h: ' + str(h) + ' w: ' + str(w)
        #meshgrid: a 3D array with dims of size: (step - step/2)/h, (step - step/2)w, 2
        #reshaped to be 2D with dims of size: 2, (step - step/2)/h * (step - step/2)w
        A = np.mgrid[step/2:h:step, step/2:w:step]
        #print 'A: ' + str(A.shape)
        y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)
        #print 'orig y: ' + str(y.shape) + ' x: ' + str(x.shape)        
        #take the flow picture to get fx, fy at each point
        fx, fy = flow[y,x].T
        fx[np.abs(fx) < 1e0] = 0
        fy[np.abs(fy) < 1e0] = 0
 
        good_indices = np.logical_and(fx != 0, fy != 0)

        fx = fx[good_indices]
        fy = fy[good_indices]
        x = x[good_indices]
        y = y[good_indices]
        
        #print fx
        #print fy

        #print 'y: ' + str(y.shape) + ' x: ' + str(x.shape)    
        #print 'fy: ' + str(fy.shape) + ' fx: ' + str(fx.shape)    
        lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
        #lines = lines + 0.5
        lines = np.int32([lines])
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        #error in sample fixed with opencv-polylines-
        #  function-in-python-throws-exception from SO
        #cv2.polylines(vis, lines, 0, (0, 255, 0))
        for line in lines:
            for (x1, y1), (x2, y2) in line:
                cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255))
        #        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
        return vis

if __name__ == '__main__':
    #run tests
    if len(sys.argv) >= 2:
        video = CarVideo(sys.argv[1], True)
        video.display_flow()
    else:
        print "No video file provided at command line"
