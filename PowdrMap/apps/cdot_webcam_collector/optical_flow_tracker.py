#!/usr/bin/env python
import cv2
import sys
import numpy as np
import scipy as sp

lk_params = dict(winSize = (15,15), 
                 maxLevel= 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

kmeans_params = dict(termcrit = (cv2.TERM_CRITERIA_EPS, 30, 0.1),
                     attempts = 1,
                     flags = cv2.KMEANS_PP_CENTERS)

feature_params = dict(maxCorners = 500,
                      qualityLevel = 0.2,
                      minDistance = 7,
                      blockSize = 7)



def draw_str(dst, (x, y), s):
    cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255))


class CarVideo:
    def __init__(self, vid_loc=None, display=False):
        self.display = display
        self.tracks = []
        self.frame_idx = 0
        self.detect_interval = 5
        self.track_len = 10

        try:
            self.stream = cv2.VideoCapture(vid_loc)
        except:
            print "No video found with name " + vid_loc
            sys.exit(1)
        if not self.stream.isOpened():
            print "video file " + vid_loc + " failed to open."
            sys.exit(1)

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


    def display_farneback_flow(self):
        cur_frame = self.grab_next_frame()

        while True:
            next_frame = self.grab_next_frame()
            flow_frame = cv2.calcOpticalFlowFarneback(cur_frame, next_frame, None, pyr_scale=0.5, levels=3, winsize=15, iterations=1, poly_n=5, poly_sigma=1.2, flags=0)
            cur_frame = next_frame

            flow_vectors = self.cluster_moving_objects(cur_frame, flow_frame)
            
            if self.display:
                if flow_frame is not None:
                    cv2.imshow('Flow Vid', self.draw_farneback_flow(cur_frame, flow_vectors))
                    cv2.waitKey(100)


    def cluster_moving_objects(self, img, flow, step=1):
        
        h, w = img.shape[:2]

        #meshgrid: a 3D array with dims of size: (step - step/2)/h, (step - step/2)w, 2
        #reshaped to be 2D with dims of size: 2, (step - step/2)/h * (step - step/2)w
        A = np.mgrid[step/2:h:step, step/2:w:step]
        y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1)

        #take the flow picture to get fx, fy at each point
        fx, fy = flow[y,x].T
        fx[np.abs(fx) < 1e0] = 0
        fy[np.abs(fy) < 1e0] = 0
 
        good_indices = np.logical_and(fx != 0, fy != 0)

        fx = fx[good_indices]
        fy = fy[good_indices]
        x = x[good_indices]
        y = y[good_indices]        

        cluster_data = np.vstack([x, y, (x + fx), (y + fy)])
        centers = np.zeros(x.shape.max() / 2, 4)
        
        true_number_clusters = cv2.flann.hierarchicalClustering<cv::L2<float> >(samples, centers, kmean_params );

        ret, labels, centers = cv2.kmeans(cluster_data, centers, 

        return np.vstack([x, y, (x + fx), (y + fy)])

    #modified version from OpenCV samples at 
    #github.com/ltseez/opencv/blob/master/samples
    #used regular lines instead of polylines, removed
    # indices that have no movement, and removed circles at points
    def draw_farneback_flow(self, img, flow_vectors):

        lines = flow_vectors.T.reshape(-1, 2, 2)
        lines = np.int32([lines])
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        #error in sample fixed with opencv-polylines-
        #  function-in-python-throws-exception from SO
        #cv2.polylines(vis, lines, 0, (0, 255, 0))
        for line in lines:
            for (x1, y1), (x2, y2) in line:
                if y2 > y1:
                    cv2.line(vis, (x1, y1), (x2, y2), (0, 0, 255))
                else:
                    cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0))
        return vis

if __name__ == '__main__':
    #run tests
    if len(sys.argv) >= 2:
        video = CarVideo(sys.argv[1], True)
        video.display_farneback_flow()
        #video.track_LK()
    else:
        print "No video file provided at command line"
