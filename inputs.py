#!/usr/bin/env python3

class Test:

    def __init__(self, instanceName, maxTime, nIter, distCrit, betaMin, betaMax, distCand, betaMin2, betaMax2, seed, shortSim, longSim, variance, execType):
        self.instanceName = instanceName
        self.maxTime = int(maxTime)
        self.nIter = int(nIter)
        self.distCrit = distCrit
        self.betaMin = float(betaMin)
        self.betaMax = float(betaMax)
        self.distCand = distCand
        self.betaMin2 = float(betaMin2)
        self.betaMax2 = float(betaMax2)
        self.seed = int(seed)
        self.shortSim = int(shortSim)
        self.longSim = int(longSim)
        self.variance = float(variance)
        self.execType = int(execType)
        self.TYPE_CRITERIA = 0
        self.TYPE_CANDIDATE = 1

class Inputs:

    def __init__(self, name, n_machines, n_resources, n_tasks, machines, resources, tasks):
        self.name = name
        self.n_machines = n_machines
        self.n_resources = n_resources
        self.n_tasks = n_tasks
        self.machines = machines
        self.resources = resources
        self.tasks = tasks

def readTests(fileName):
    tests = []
    with open("tests/" + fileName) as f:
        for line in f:
            tokens = line.split("\t")
            if '#' not in tokens[0]:
                test = Test(*tokens)
                tests.append(test)
    return tests

def readInputs(instanceName):
    try:
        with open("inputs/" + instanceName + ".txt") as f:
            data = f.readlines()

            # Extract info from the first line
            first_line_data = data[0].split(",")
            n_machines = int(first_line_data[0])
            n_resources = int(first_line_data[1])
            n_tasks = int(first_line_data[2])

            # Extract machines
            machines = {} 
            for i in range(1, n_machines + 1):
                machines[i] = int(data[i])

            # Extract resources
            resources = []
            for i in range(1, n_resources + 1):
                resources.append(i)

            # Extract tasks
            tasks = []
            for i in range(1, n_tasks + 1):
                task_line = data[n_machines + i].split(",")
                tasks.append([int(task_line[0]), int(task_line[1])])

            inputs = Inputs(instanceName, n_machines, n_resources, n_tasks, machines, resources, tasks)
            return inputs

    except FileNotFoundError:
        print("[ERROR]: File not found.")
        return None
