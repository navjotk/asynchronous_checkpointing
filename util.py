import numpy as np
from functools import reduce
from operator import mul
from timeit import default_timer
import pickle


def prod(iterable):
    return reduce(mul, iterable, 1)


class Timer(object):
    def __init__(self, tracker):
        self.timer = default_timer
        self.tracker = tracker
        
    def __enter__(self):
        self.start = self.timer()
        return self
        
    def __exit__(self, *args):
        end = self.timer()
        self.elapsed_secs = end - self.start
        self.elapsed = self.elapsed_secs * 1000  # millisecs
        self.tracker.append(self.elapsed)


def measure(rnn):
    repeats = 5
    fw_timings = []
    bw_timings = []
    for i in range(repeats):
        with Timer(fw_timings):
            rnn.forwardProp()
        with Timer(bw_timings):
            rnn.backProp()
    return fw_timings, bw_timings

def measure_fw(rnn):
    repeats = 5
    fw_timings = []
    for i in range(repeats):
        with Timer(fw_timings):
            rnn.forwardProp()
    return fw_timings


def LoadText():
    #open text and return input and output data (series of words)
    with open("big2.txt", "r") as text_file:
        data = text_file.read()
    text = list(data)
    outputSize = len(text)
    data = list(set(text))
    uniqueWords, dataSize = len(data), len(data) 
    returnData = np.zeros((uniqueWords, dataSize))
    for i in range(0, dataSize):
        returnData[i][i] = 1
    returnData = np.append(returnData, np.atleast_2d(data), axis=0)
    output = np.zeros((uniqueWords, outputSize))
    for i in range(0, outputSize):
        index = np.where(np.asarray(data) == text[i])
        output[:,i] = returnData[0:-1,index[0]].astype(float).ravel()
    return returnData, uniqueWords, output, outputSize, data

def preprocess():
    returnData, uniqueWords, output, outputSize, data = LoadText()
    pickle.dump( (returnData, uniqueWords, output, outputSize, data), open( "save.p", "wb" ) )

def loadpickled():
    returnData, uniqueWords, output, outputSize, data = pickle.load(open("save.p", "rb"))
    return returnData, uniqueWords, output, outputSize, data

#write the predicted output (series of words) to disk
def ExportText(output, data):
    finalOutput = np.zeros_like(output)
    prob = np.zeros_like(output[0])
    outputText = ""
    print(len(data))
    print(output.shape[0])
    for i in range(0, output.shape[0]):
        for j in range(0, output.shape[1]):
            prob[j] = output[i][j] / np.sum(output[i])
        outputText += np.random.choice(data, p=prob)    
    with open("output.txt", "w") as text_file:
        text_file.write(outputText)
    return
