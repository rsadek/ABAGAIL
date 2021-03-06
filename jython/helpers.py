from math import ceil

import opt.SimulatedAnnealing as SimulatedAnnealing
import shared.FixedIterationTrainer as FixedIterationTrainer
import util.linalg.DenseVector as DenseVector
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import util.ABAGAILArrays as ABAGAILArrays
import sys
import time
import opt.prob.MIMIC as MIMIC
from array import array
import MatlabWriter
# from opt.SimulatedAnnealing import SimulatedAnnealing as SimulatedAnnealing
#from shared.FixedIterationTrainer import FixedIterationTrainer as FixedIterationTrainer


__author__ = 'Ramy'


def savePath2Matlab(name, path, points, num, mat):
    xrow = 2 * (num)
    yrow = xrow + 1
    xVec = []
    yVec = []
    for i in range(0, len(path)):
        p = path[i]
        t = points[p]
        xVec.append(t[0])
        yVec.append(t[1])
    #mat.addValue(x, name,xrow )
    #mat.addValue(y, name,yrow )
    saveFit(name, xVec, xrow, mat)
    saveFit(name, yVec, yrow, mat)


def saveFit(name, vec, num, mat):
    if isinstance(vec,DenseVector):
        for i in range (vec.size()):
            val = vec.get(i)
            mat.addValue(val, name, num)
    else:
        for i in vec:
            mat.addValue(i, name, num)


def getPath(experiment):
    path = []

    if (isinstance(experiment, MIMIC)):
        path = doMIMICExtraction(experiment)
    else:
        N = experiment.getOptimal().size()
        for x in range(0, N):
            path.append(experiment.getOptimal().getDiscrete(x))
    return path


def TrainAndSave(experiment, points, fit, mat, name, runNum):
    #TODO: do we even need this function anymore? it won't help other problems. ditch it?
    # for idx, iters in enumerate(paramRange):
    start = time.time()
    f = fit.train()
    fitness = experiment.getOptimizationProblem().value(experiment.getOptimal());
    t = time.time() - start
    if not isinstance(points[0], int):
        path = getPath(experiment)
        savePath2Matlab(name, path, points, runNum, mat)
    else:
        saveFit(name,experiment.getOptimal().getData(), runNum, mat)
    # mw.addValue(iters,"RHC_iterations",idx)
    #    print fitVec
    return fitness, t


def floatRange(vec, scale, num):
    tmp = [];
    stride = int(ceil(float(len(vec)) / num))
    for x in vec[::stride]:
        tmp.append(float(x) / scale);
    return tmp


def IterRangeExperiment(name, experiment, points, paramRange, mat, row):
    totalSoFar = 0
    fitVec = []
    timeVec = []
    for idx, i in enumerate(paramRange):
        num = i - totalSoFar
        fit = FixedIterationTrainer(experiment, num)
        totalSoFar += num
        frow = row * len(paramRange) + idx
        fitness, time = TrainAndSave(experiment, points, fit, mat, name, frow)
        fitVec.append(fitness)
        timeVec.append(time)
    saveFit(name + "_fitness", fitVec, row, mat)
    saveFit(name + "_iterations", paramRange, row, mat)
    return fitVec


def CoolingRangeExperiment(name, points, problem, coolingRange, iterRange, mat):
    for idx, i in enumerate(coolingRange):
        sa = SimulatedAnnealing(1E15, i, problem)
        IterRangeExperiment(name, sa, points, iterRange, mat, idx)
    saveFit(name + "_coolingValues", coolingRange, 0, mat)

def PopulationRangeExperiment(name, gap,  points, popRange, mateRange, mutRange, iterRange, mat):
    lastRow = -1
    for idx,i in enumerate(popRange):
        for jdx, j in enumerate(mateRange):
            for kdx, k in enumerate(mutRange):
                row = idx * len(mateRange)*len(mutRange) + jdx*len(mutRange)+ kdx
                if row < lastRow:
                    print "ERROR in ROW CALC!"
                lastRow = row
                if j > i or k > i:
                    #print "skipping bad values for i,j,k "
                    continue
                ga = StandardGeneticAlgorithm(i, j, k, gap)
                IterRangeExperiment(name, ga, points, iterRange, mat, row)


def MIMICSampleRangeExperiment(name, points, problem, sampleRange, iterRange, mat):
    for idx, i in enumerate(sampleRange):
        mimic = MIMIC(i, 20, problem)
        IterRangeExperiment(name, mimic, points, iterRange, mat, idx)
    saveFit(name + "_numSamples", sampleRange, 0, mat)


def MIMICKeepRangeExperiment(name, points, problem, keepRange, iterRange, mat):
    for idx, i in enumerate(keepRange):
        mimic = MIMIC(1000, i, problem)
        fitVec = IterRangeExperiment(name, mimic, points, iterRange, mat, idx * len(iterRange))
        row = idx;
        saveFit(name + "_fitness", fitVec, idx, mat)
        saveFit(name + "_iterations", iterRange, idx, mat)
    saveFit(name + "_numSamples", keepRange, 0, mat)


def MIMICAllRangeExperiment(name, points, problem, sampleRange, keepRange, iterRange, mat):
    currmax =-1
    bestSampleSize = -1
    bestKeep = -1
    bestPath =[]
    lastRow = -1;
    for jdx, j in enumerate(sampleRange):
        iVec =[]
        jVec =[]
        for idx, i in enumerate(keepRange):    #percentage to keep
            fitVec = []
            row = idx * len(sampleRange) + jdx
            keep = int(ceil(j*i)) #i is the percentage
            print "samples " + str(j) + " keep " + str(keep)
            if keep < j:  #TODO: no longer needed now that using % keep isntead of absolute
                mimic = MIMIC(j, keep, problem)

                if( row == lastRow):
                    print "Error! lastRow == row! "
                else:
                    lastRow = row
                fitVec= IterRangeExperiment(name, mimic, points, iterRange, mat, row)
            else:
                print "i <= j, skipping row " + str(row)
            iVec.append(i)
            jVec.append(j)
            saveFit(name + "_keep", iVec, idx*len(sampleRange)+jdx, mat)
            saveFit(name + "_sampleSize", jVec, idx*len(sampleRange)+jdx, mat)
    #         if len(fitVec) >0 and  max(fitVec) > currmax:
    #             currmax = max(fitVec)
    #             bestSampleSize = jdx
    #             bestKeep = idx
    #             bestPath = getPath(mimic)
    # print "MIMIC: best Sample Size found at index " + str(bestSampleSize) + " value " + str(sampleRange[bestSampleSize])
    # print "MIMIC: best Keep found at " + str(bestKeep) + " value " + str(keepRange[bestKeep])
    # print "peak fitness " + str(currmax)
    # savePath2Matlab(name + "_best", bestPath,points, 0, mat)



def doMIMICExtraction(mimic):
    optimal = mimic.getOptimal()
    fill = [0] * optimal.size()
    ddata = array('d', fill)
    for i in range(0, len(ddata)):
        ddata[i] = optimal.getContinuous(i)
    order = ABAGAILArrays.indices(optimal.size())
    ABAGAILArrays.quicksort(ddata, order)
    print order
    return order


#
# def getArgs():
#     try:
#         opts, args = getopt.getopt(sys.argv[1:], 'rsgmo:', ['rhc','sa','ga','MIMIC','output='])
#     except getopt.GetoptError, err:
#         print str(err)
#         sys.exit(2)
#     output = None
#     verbose = False
#     for o, a in opts:
#         if o == "-r":
#             DO_RHC = True
#         elif o == "s":
#             DO_SA = True
#         elif o == "g":
#             DO_GA = True
#         elif o == "m":
#             DO_MIMIC = True
#         elif o in ("-o","--output"):
#             output = a
#         else:
#             assert False,"unhandled option"
#
# getArgs()
