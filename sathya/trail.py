import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import _thread
import pyaudio
import example

pygame.init()

def video():
    lowerBound = np.array([33,80,40])
    higherBound = np.array([102,255,255])
    cam = cv2.VideoCapture(0)
    # Defining kernel sizes for smoothing the image
    kernelOpen = np.ones((5,5))
    kernelClose = np.ones((20,20))
    timeMes = 0
    # font for text
    # font = cv2.InitFont(cv2.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
    keyPressed= []
    keysCo = {}
    coordinates = []
    recKeys = []
    pygame.display.set_caption("OpenCV camera stream on Pygame")
    screen = pygame.display.set_mode([1100,600])
    try:
        while True:
            ret, frame = cam.read()
            screen.fill([0,0,0])
            cv2.rectangle(frame,(0,0),(50,50),(255,255,255),thickness=cv2.FILLED)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        sys.exit(0)

    except (SystemExit):
        example.stop_AVrecording()
        cv2.destroyAllWindows()
        pygame.quit()

# conversion code taken from stack overflow

from time import gmtime, strftime
timePrint = strftime("%Y-%m-%d %H:%M:%S", gmtime())

#
if __name__ == "__main__":
    example.start_audio_recording()
    video()