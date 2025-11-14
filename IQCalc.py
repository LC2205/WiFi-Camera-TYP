import math as m
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import random

class IQComplex():

    def __init__(self, IFile, QFile):
        self.IFile = IFile
        self.QFile = QFile
        self.IArr = []
        self.QArr = []        

    def calcIQ(self, IValArr, QValArr):
        IQArr = []
        for IVal, QVal in zip(IValArr, QValArr):
            IQArr.append(m.sqrt((float(IVal)**2 + float(QVal)**2)))
        IQArr.sort()
        plt.plot(IQArr, norm.pdf(IQArr, s.mean(IQArr), s.stdev(IQArr)))
        #plt.plot(IQArr, norm.pdf(IQArr, s.mean(IQArr), s.stdev(IQArr)))
        #plt.hist(IQArr, density=True)
        plt.show()
        return s.mean(IQArr)

    def readIQ(self, filename):
        randomindex = random.sample(range(0,100000), 10000)
        for x in range(len(randomindex)):
            randomindex[x] = (randomindex[x] // 2) * 2
        tempIArr = []
        tempQArr = []
        with open(self.QFile, "rb") as f:
            lines = np.fromfile(f, dtype=np.float32)
            for i in randomindex:
                tempIArr.append(lines[i])
                tempQArr.append(lines[i+1])
        return [tempIArr, tempQArr]
            #for qVal in lines:
            #    QArr.append(qVal / 32768)
            

    def readI(self, filename):
        tempIArr = []
        with open(self.IFile, "rb") as f:
            lines = np.fromfile(f, dtype=np.int16)
            for i in range(1000):
                print(lines[i])
                tempIArr.append(lines[i]/32768)
        return tempIArr
            #for iVal in lines:
            #    IArr.append(iVal / 32768)

    def plotGraph(self):
            plt.subplot(1,2,1)
            plt.plot(self.IArr, 'o')
            plt.title("I VALUES")

            plt.subplot(1,2,2)
            plt.plot(self.QArr, 'o')
            plt.title("Q VALUES")

            plt.show()

    def initiateCalc(self):
        IQArr = self.readIQ(self.QFile)
        self.IArr = IQArr[0]
        self.QArr = IQArr[1]
        #self.IArr = self.readI(self.IFile)
        #self.QArr = self.readQ(self.QFile)
        self.plotGraph()
        return self.calcIQ(self.IArr, self.QArr)
    
def main():
    IQ = IQComplex("Real.bin", "Complex.bin")
    result = IQ.initiateCalc()
    print(result)

if __name__=="__main__":
    main()
    