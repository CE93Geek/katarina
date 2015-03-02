#!/usr/bin/python
"""
  ARDrone3 demo with autonomous navigation to two color Parrot Cap
  usage:
       ./demo.py <task> [<metalog> [<F>]]
"""
import sys
import cv2

from bebop import Bebop
from video import VideoFrames
from capdet import detectTwoColors, loadColors

# this will be in new separate repository as common library fo robotika Python-powered robots
from apyros.metalog import MetaLog, disableAsserts
from apyros.manual import myKbhit, ManualControlException

TMP_VIDEO_FILE = "video.bin"


g_vf = None

def videoCallback( data ):
    global g_vf
    g_vf.append( data )
    frame = g_vf.getFrame()
    if frame:
        print "Video", len(frame)
        # workaround for a single frame
        f = open( TMP_VIDEO_FILE, "wb" )
        f.write( frame )
        f.close()
        cap = cv2.VideoCapture( TMP_VIDEO_FILE )
        ret, img = cap.read()
        cap.release()
        if ret:
            img, detected = detectTwoColors( img, loadColors("cap-colors.txt") )
            print "Detected", detected
#            cv2.imshow('image', img)
#            key = cv2.waitKey(10)
    


def demo( drone ):
    print "Follow 2-color cap ..."
    global g_vf
    g_vf = VideoFrames( onlyIFrames=True, verbose=False )
    drone.videoCbk = videoCallback
    drone.videoEnable()
    for i in xrange(100):
        print i,
        drone.update( cmd=None )

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(2)
    metalog=None
    if len(sys.argv) > 2:
        metalog = MetaLog( filename=sys.argv[2] )
    if len(sys.argv) > 3 and sys.argv[3] == 'F':
        disableAsserts()

    drone = Bebop( metalog=metalog )
    demo( drone )
    print "Battery:", drone.battery

# vim: expandtab sw=4 ts=4 
