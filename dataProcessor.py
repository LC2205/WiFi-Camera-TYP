import os
import sys
import time
import socket
import random
import threading
import numpy as np
import statistics as s
import matplotlib.pyplot as plt

def setimg(rgbval):
    image = plt.imshow([[rgbval]])
    return image

def updateimg(rgbval, image):
    print(rgbval)
    image.set_data([[rgbval]])
    plt.draw()
    plt.pause(1)

def rgb(val):
    b = int(max(0, 255 * (1 - val)))
    r = int(max(0, 255 * (val - 1)))
    g = 255 - b - r
    return r, g, b

milli_timestamp = lambda: int(round(time.time() * 1000))
def readData(conn, timing):
    flag = False
    tid = 0
    first = True
    image = 0

    while True:
        try:
            if flag == False:
                tid = milli_timestamp()
                flag = True

            ts = milli_timestamp()

            data = conn.recv(1024)
            if not data:
                break

            if (ts - tid) < timing and flag == True:
                if first:
                    image = setimg(rgb(s.mean(data) / 100))
                    first = False
                else:
                    updateimg(rgb(s.median(data) / 100), image)
            
            else:
                flag = False
        except Exception as e:
            print("Error occurred")
            print(e)

            break
    return

def runStream():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 5000))

    readData(sock, 1000)
    return

def main():
    runStream()

if __name__ == "__main__":
    main()