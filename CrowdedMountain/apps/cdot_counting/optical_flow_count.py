#!/usr/bin/env python
import cv2
import sys
import numpy as np

lk_params = dict(winSize = (15,15), 
                 maxLevel= 2,
                 criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

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

    #based on sample from github.com/ltseez/opencv/blob/master/samples/python2/lk_track.py
    def track_LK(self):
        cur_frame = self.grab_next_frame()

        while True:
            next_frame = self.grab_next_frame()
            vis = next_frame.copy()

            if len(self.tracks) > 0:

                #setup p0 to be the same size as the number of features 
                #   found in the last round that features were found
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(cur_frame, next_frame, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(next_frame, cur_frame, p1, None, **lk_params)
                #returns the minimum distance between original features and predicted original features 
                #  along the last axis
                d = abs(p0 - p0r).reshape(-1,2).max(-1)
            
                #TODO: find a good measure for being too far from the predicted point
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    #each time optical flow is found, append the next predicted 
                    #   point for the feature based on the optical flow
                    tr.append((x,y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x,y), 2, (0, 255, 0), -1)
                
                self.tracks = new_tracks
                #draw the optical flow for the last `self.track_len` frames
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(vis, (20, 20), 'track count: %d' %len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                #starts here:
                #  mask is the size of the current frame, all 255's (i.e. 1's)
                mask = np.zeros_like(cur_frame)
                mask[:] = 255

                #TODO: should this ordering flipped so that new features are drawn and not old ones
                #create a circle for each tracked feature in self.tracks, marked with a dot
                # taking the last element in the track (as an int)
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)

                #find "good features", these are features that are relatively invariant across multiple frames 
                #  mostly Harris corner detectors
                p = cv2.goodFeaturesToTrack(cur_frame, mask = mask, **feature_params)

                #p is the vector of features found
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x,y)])


            self.frame_idx += 1
            cur_frame = next_frame
            
            if self.display:
                ch = 0xFF & cv2.waitKey(100)
                cv2.imshow('lk_track', vis)


    def display_farneback_flow(self):
        cur_frame = self.grab_next_frame()

        while True:
            next_frame = self.grab_next_frame()
            flow_frame = cv2.calcOpticalFlowFarneback(cur_frame, next_frame, None, pyr_scale=0.5, levels=3, winsize=15, iterations=1, poly_n=5, poly_sigma=1.2, flags=0)
            cur_frame = next_frame
            
            if self.display:
                if flow_frame is not None:
                    cv2.imshow('Flow Vid', self.draw_farneback_flow(cur_frame, flow_frame))
                    cv2.waitKey(100)


    #modified version from OpenCV samples at 
    #github.com/ltseez/opencv/blob/master/samples
    #used regular lines instead of polylines, removed
    # indices that have no movement, and removed circles at points
    def draw_farneback_flow(self, img, flow, step=4):
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

        #Is this a Expectation Maximization Problem??

        fx = fx[good_indices]
        fy = fy[good_indices]
        x = x[good_indices]
        y = y[good_indices]
        
        
        
        lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
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
