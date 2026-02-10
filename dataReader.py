import matplotlib.pyplot as plt
import numpy as np

def showImage(values):
    image = plt.imshow(values)
    plt.show()

def readFiles():
    rgbs = [] 
    for i in range(9):
        with open(f"Reading{i}.txt", "r") as f:
            val = f.read()
            rgbs.append(eval(val))
    showImage(np.array(rgbs).reshape(3, 3, 3))

def main():
    readFiles()

if __name__=="__main__":
    main()