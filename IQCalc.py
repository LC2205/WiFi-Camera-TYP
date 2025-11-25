import math as m
from decimal import Decimal
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from datetime import datetime

class IQComplex():

    def __init__(self, IQFile):
        self.IQFile = IQFile
        self.IArr = []
        self.QArr = []   

    def calcIQ(self, IValArr, QValArr):

        IQArr = np.hypot(IValArr, QValArr)
        IQArrSquelch = IQArr[IQArr >= 0.9]
        print(10* np.log10(min(IQArrSquelch)))
        print(10 * np.log10(max(IQArrSquelch)))
        powerFunc = lambda x: 10 * np.log10(x, where= x > 0)
        IQArrSquelchdB = np.array(powerFunc(IQArr))
        print(min(IQArrSquelchdB))
        print(s.mean(IQArrSquelchdB))

        plt.hist(IQArrSquelchdB, bins=300, density=True, range=[-40, 10])
        plt.title("Squelched relative dB")
        plt.show()

        IQArrSquelch.sort()
        IQArr.sort()

        plt.plot(IQArr, norm.pdf(IQArr, s.mean(IQArr), s.stdev(IQArr)))
        plt.hist(IQArr, bins=100, density=True, color='r')
        plt.title("Normal IQ (Mean)")
        plt.xlabel("IQ value")
        plt.ylabel("Probability Density function")

        plt.show()

        plt.plot(IQArrSquelch, norm.pdf(IQArrSquelch, s.mean(IQArrSquelch), s.stdev(IQArrSquelch)))
        plt.hist(IQArrSquelch, bins=100, density=True, color='r')
        plt.title("Normal rdB Squelch (Mean)")
        plt.xlabel("dB value")
        plt.ylabel("Probability Density function")

        plt.show()
        return s.mean(IQArrSquelch)

    def readIQ(self, filename):
        try:
            with open(self.IQFile, "rb") as f:
                lines = np.fromfile(f, dtype=np.float32)
                tempIArr = np.array(lines[::2], dtype=np.float32)
                tempQArr = np.array(lines[1::2], dtype=np.float32)
                return [tempIArr, tempQArr]
        except:
            print("File not found")
            return 0
        
    def readFile(self, filename):
        try:
            with open(filename, "rb") as f:
                return (s.mean(np.fromfile(f, np.float32)) / 100)
        except:
            print("File not found")
            return 0
        
    def initiateCalc(self):
        IQArr = self.readIQ(self.IQFile)
        self.IArr = IQArr[0]
        self.QArr = IQArr[1]
        return self.calcIQ(self.IArr, self.QArr)
    
def rgb(val):
    b = int(max(0, 255 * (1 - val)))
    r = int(max(0, 255 * (val - 1)))
    g = 255 - b - r
    return r, g, b
    
def main():
    IQ = IQComplex("IQ.bin")
    print(datetime.time(datetime.now()))
    #result = IQ.initiateCalc()
    avg = IQ.readFile("TYP.bin")
    colours = rgb(avg)

    plt.imshow([[colours]])
    plt.show()
    print(colours)
    #print(result)

if __name__=="__main__":
    main()
    