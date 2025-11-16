import math as m
from decimal import Decimal
import statistics as s
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class IQComplex():

    def __init__(self, IQFile):
        self.IQFile = IQFile
        self.IArr = []
        self.QArr = []       

    def calcIQ(self, IValArr, QValArr):
        IQArr = []
        IQArrSquelch = []
        for IVal, QVal in zip(IValArr, QValArr):
            IQ = m.sqrt((float(IVal)**2 + float(QVal)**2))
            if IQ > m.sqrt(2)/2.0:
                IQArrSquelch.append(IQ)
            IQArr.append(IQ)
        print(len(IQArr))
        print(len(IQArrSquelch))
        plt.plot(IQArr, 'o')
        plt.title("IQ Values unsorted")
        plt.show()

        plt.plot(IQArrSquelch, 'o')
        plt.title("IQ Values unsorted SQUELCH 50%")
        plt.show()

        IQArrSquelch.sort()
        IQArr.sort()
        plt.subplot(1,2,1)
        plt.plot(IQArr, norm.pdf(IQArr, s.mean(IQArr), s.stdev(IQArr)))
        plt.hist(IQArr, bins=len(IQArr)//20000, density=True, color='r')
        plt.title("Normal IQ (Mean)")
        plt.xlabel("IQ value")
        plt.ylabel("Probability Density function")
        
        plt.subplot(1,2,2)
        plt.plot(IQArr, norm.pdf(IQArr, s.median(IQArr), s.stdev(IQArr)))
        plt.hist(IQArr, bins=len(IQArr)//20000, density=True, color='r')
        plt.title("Normal IQ (Median)")
        plt.xlabel("IQ value")
        plt.ylabel("Probability Density function")

        plt.show()

        plt.subplot(1,2,1)
        plt.plot(IQArrSquelch, norm.pdf(IQArrSquelch, s.mean(IQArrSquelch), s.stdev(IQArrSquelch)))
        plt.hist(IQArrSquelch, bins=len(IQArrSquelch)//1000, density=True, color='r')
        plt.title("Normal IQ Squelch (Mean)")
        plt.xlabel("IQ value")
        plt.ylabel("Probability Density function")

        plt.subplot(1,2,2)
        plt.plot(IQArrSquelch, norm.pdf(IQArrSquelch, s.median(IQArrSquelch), s.stdev(IQArrSquelch)))
        plt.hist(IQArrSquelch, bins=len(IQArrSquelch)//1000, density=True, color='r')
        plt.title("Normal IQ Squelch (Median)")
        plt.xlabel("IQ value")
        plt.ylabel("Probability Density function")

        plt.show()
        return [s.mean(IQArr), s.median(IQArr), s.mean(IQArrSquelch), s.median(IQArrSquelch)]

    def readIQ(self, filename):
        tempIArr = []
        tempQArr = []
        with open(self.IQFile, "rb") as f:
            lines = np.fromfile(f, dtype=np.float32)
            for i in range(0, len(lines), 2):
                tempIArr.append(lines[i])
                tempQArr.append(lines[i+1])
        return [tempIArr, tempQArr]

    def plotGraph(self):
            plt.subplot(1,2,1)
            plt.plot(self.IArr, 'o')
            plt.title("I VALUES")

            plt.subplot(1,2,2)
            plt.plot(self.QArr, 'o')
            plt.title("Q VALUES")

            plt.show()

    def initiateCalc(self):
        IQArr = self.readIQ(self.IQFile)
        self.IArr = IQArr[0]
        self.QArr = IQArr[1]
        self.plotGraph()
        return self.calcIQ(self.IArr, self.QArr)
    
def main():
    IQ = IQComplex("IQ.bin")
    result = IQ.initiateCalc()
    print(result)

if __name__=="__main__":
    main()
    