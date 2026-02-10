import time
import socket
import numpy as np
import statistics as s
import matplotlib.pyplot as plt
import zmq
import keyboard

def getkey():
    keyboard.read_key()

def milli_timestamp():
    return time.monotonic() * 1000

def setimg(rgbval):
    image = plt.imshow([[rgbval]])
    return image

def updateimg(rgbval, image, timing):
    print(rgbval)
    image.set_data([[rgbval]])
    plt.draw()
    plt.pause(timing / 1000)

def rgb(val):
    b = int(max(0, 255 * (1 - val)))
    r = int(max(0, 255 * (val - 1)))
    g = 255 - b - r
    return r, g, b

def readData(conn, timing):
    t = milli_timestamp()
    first = True
    img = 0
    while True:
        dt = milli_timestamp()
        if (dt - t) > timing:
            t, dt = milli_timestamp(), milli_timestamp()
            if conn.poll() != 0:
                msg = conn.recv()
                print(len(msg))
                data = np.frombuffer(msg, dtype=np.float32, count=-1)
                print(s.mean(data))
                if first:
                    val = ((s.median(data) + 10) + 60) / 60
                    print("VAL:", val)
                    img = setimg(rgb(val))
                    first = False
                else:
                    val = ((s.median(data) + 10) + 60) / 60
                    print("VAL:", val)
                    updateimg(rgb(val), img, timing)
        else:
            empty_sink = conn.recv()

def readSet(conn):
    print("Reading started")
    iters = 0
    calibration = 60
    while True:
        if keyboard.is_pressed("c"):
            msg = conn.recv()
            data = np.frombuffer(msg, dtype=np.float32, count=-1)
            calibration = s.mean(data)
            print(f"Calibration set to {calibration}")
            time.sleep(1)
            print("ACTIVE")
        elif keyboard.is_pressed("e"):
            msg = conn.recv()
            data = np.frombuffer(msg, dtype=np.float32, count=-1)
            val = ((s.median(data) + 10) + calibration) / calibration
            print(f"Value: {val}")
            with open (f"Reading{iters}.txt", "w") as f:
                f.write(val)
            iters += 1
            time.sleep(1)
            print("ACTIVE")
        elif keyboard.is_pressed("q"):
            break
        else:
            empty_sink = conn.recv()

def runStream():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://127.0.0.1:5000")
    socket.setsockopt(zmq.SUBSCRIBE, b'')

    readSet(socket)
    #readData(socket, 250)
    return

def main():
    runStream()

if __name__ == "__main__":
    main()