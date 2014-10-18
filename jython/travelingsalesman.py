# traveling salesman algorithm implementation in jython
# This also prints the index of the points of the shortest route.
# To make a plot of the route, write the points at these indexes
# to a file and plot them in your favorite tool.
import sys
import os
import time

import java.io.FileReader as FileReader
import java.io.File as File
import java.lang.String as String
import java.lang.StringBuffer as StringBuffer
import java.lang.Boolean as Boolean
import java.util.Random as Random

import dist.DiscreteDependencyTree as DiscreteDependencyTree
import dist.DiscreteUniformDistribution as DiscreteUniformDistribution
import dist.Distribution as Distribution
import dist.DiscretePermutationDistribution as DiscretePermutationDistribution
import opt.DiscreteChangeOneNeighbor as DiscreteChangeOneNeighbor
import opt.EvaluationFunction as EvaluationFunction
import opt.GenericHillClimbingProblem as GenericHillClimbingProblem
import opt.HillClimbingProblem as HillClimbingProblem
import opt.NeighborFunction as NeighborFunction
import opt.RandomizedHillClimbing as RandomizedHillClimbing
import opt.SimulatedAnnealing as SimulatedAnnealing
import opt.example.FourPeaksEvaluationFunction as FourPeaksEvaluationFunction
import opt.ga.CrossoverFunction as CrossoverFunction
import opt.ga.SingleCrossOver as SingleCrossOver
import opt.ga.DiscreteChangeOneMutation as DiscreteChangeOneMutation
import opt.ga.GenericGeneticAlgorithmProblem as GenericGeneticAlgorithmProblem
import opt.ga.GeneticAlgorithmProblem as GeneticAlgorithmProblem
import opt.ga.MutationFunction as MutationFunction
import opt.ga.StandardGeneticAlgorithm as StandardGeneticAlgorithm
import opt.ga.UniformCrossOver as UniformCrossOver
import opt.prob.GenericProbabilisticOptimizationProblem as GenericProbabilisticOptimizationProblem
import opt.prob.MIMIC as MIMIC
import opt.prob.ProbabilisticOptimizationProblem as ProbabilisticOptimizationProblem
import shared.FixedIterationTrainer as FixedIterationTrainer
import opt.example.TravelingSalesmanEvaluationFunction as TravelingSalesmanEvaluationFunction
import opt.example.TravelingSalesmanRouteEvaluationFunction as TravelingSalesmanRouteEvaluationFunction
import opt.SwapNeighbor as SwapNeighbor
import opt.ga.SwapMutation as SwapMutation
import opt.example.TravelingSalesmanCrossOver as TravelingSalesmanCrossOver
import opt.example.TravelingSalesmanSortEvaluationFunction as TravelingSalesmanSortEvaluationFunction
import shared.Instance as Instance
import util.ABAGAILArrays as ABAGAILArrays
import com.jmatio.types.MLDouble as MLDouble
#import matplotlib.pyplot as plt

import MatlabWriter
from array import array




"""
Commandline parameter(s):
    none
"""

# set N value.  This is the number of points
N = 50
random = Random()

points = [[0 for x in xrange(2)] for x in xrange(N)]
for i in range(0, len(points)):
    points[i][0] = random.nextDouble()
    points[i][1] = random.nextDouble()

ef = TravelingSalesmanRouteEvaluationFunction(points)
odd = DiscretePermutationDistribution(N)
nf = SwapNeighbor()
mf = SwapMutation()
cf = TravelingSalesmanCrossOver(ef)
hcp = GenericHillClimbingProblem(ef, odd, nf)
gap = GenericGeneticAlgorithmProblem(ef, odd, mf, cf)


def savePath2Matlab(name, path, num):
    xrow =2*(num);
    yrow = xrow+1;
    for i in range(0,len(path)):
        p = path[i]
        t= points[p]
        x = points[path[i]][0]
        mw.addValue(x, name,xrow )

    for i in range(0,len(path)):
        y = points[path[i]][1]
        mw.addValue(y, name,yrow )
    mw.write();


def saveFit(name, vec, iters, num):
    for i in range(0,len(vec)):
        mw.addValue(vec[i],name,num)
        mw.addValue(iters,name+"iterations",num)

def RHCExperiment(experiment, paramRange):
    fitVec =[]
    for idx, iters in enumerate(paramRange):
        fit = FixedIterationTrainer(experiment, iters)
        fitness = fit.train()
        fitVec.append(fitness)
        path = []
        for x in range(0,N):
            path.append(rhc.getOptimal().getDiscrete(x))
        savePath2Matlab("RHC", path, idx)
    saveFit("RHC_fitness", fitVec, iters, 0)
    return path


mw = MatlabWriter("ts.mat", N, 2)
rhc = RandomizedHillClimbing(hcp)
begin = 100;
end = 2000;
numSamples = 10;
step = (end - begin) / numSamples;

path = RHCExperiment(rhc, range(begin, end, step))

print "RHC Inverse of Distance: " + str(ef.value(rhc.getOptimal()))
print "Route:"
print path
print "writing MATLAB matrix"
mw.write();

print "All Done! Bye now :)"
sys.exit();

#plt.plot(points)

SA_iters =2000;
SA_cooling = .6
sa = SimulatedAnnealing(1E11, SA_cooling, hcp)
fit = FixedIterationTrainer(sa, SA_iters)
fit.train()
print "SA Inverse of Distance: " + str(ef.value(sa.getOptimal()))
print "Route:"
path = []
for x in range(0,N):
    path.append(sa.getOptimal().getDiscrete(x))
print path

save2matlab("SA", path)

#ga = StandardGeneticAlgorithm(2000, 1500, 250, gap)
GA_population =2000
GA_toMate =1500
GA_toMutate=250
GA_iters=2000000;
ga = StandardGeneticAlgorithm(GA_population, GA_toMate, GA_toMutate, gap)
fit = FixedIterationTrainer(ga, 2000000)
fit.train()
print "GA Inverse of Distance: " + str(ef.value(ga.getOptimal()))
print "Route:"
path = []
for x in range(0,N):
    path.append(ga.getOptimal().getDiscrete(x))
print path

save2matlab("GA", path)
# for mimic we use a sort encoding
ef = TravelingSalesmanSortEvaluationFunction(points);
fill = [N] * N
ranges = array('i', fill)
odd = DiscreteUniformDistribution(ranges);
df = DiscreteDependencyTree(.1, ranges);
pop = GenericProbabilisticOptimizationProblem(ef, odd, df);

mimic = MIMIC(500, 100, pop)
fit = FixedIterationTrainer(mimic, 1000)
fit.train()
print "MIMIC Inverse of Distance: " + str(ef.value(mimic.getOptimal()))
print "Route:"
path = []
optimal = mimic.getOptimal()
fill = [0] * optimal.size()
ddata = array('d', fill)
for i in range(0,len(ddata)):
    ddata[i] = optimal.getContinuous(i)
order = ABAGAILArrays.indices(optimal.size())
ABAGAILArrays.quicksort(ddata, order)
print order
save2matlab("MIMIC", order)
mw.write();
