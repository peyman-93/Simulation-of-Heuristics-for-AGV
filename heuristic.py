#!/usr/bin/env python3

import csv
import random
import datetime
import itertools

from inputs import readTests, readInputs

"""
FIFO (First In First Out) heuristic
"""
def calculate_fifo(inputs, rng):
    sequence = inputs.tasks.copy()
    return sequence

"""
Random uniform heuristic
"""
def calculate_random(inputs, rng):
    sequence = inputs.tasks.copy()
    rng.shuffle(sequence)
    return sequence

"""
Heuristic inspired in the NEH algorithm
    1. order resources by amount of work (see maxResource param)
    2. order machines by cost (see maxMachine param)
    3. assign resources to machines in sequence (round-robin for both resources and machines)
       maxResource = True : sort resources in descending order
       maxMachine =  True : sort machines in descending order
"""
def calculate_sequence(inputs, maxResource, maxMachine, rng): 
    sequence = []
    task_list = inputs.tasks.copy()

    # Calculate cost per resource
    cost_per_resource = [0 for _ in inputs.resources]
    for task in inputs.tasks:
        machine_index = task[0]
        resource_index = task[1]
        cost_per_resource[resource_index - 1] += inputs.machines[machine_index]

    # Sort resources by cost
    resource_indices = sorted(range(len(cost_per_resource)), key=lambda index: cost_per_resource[index], reverse = maxResource)
    resource_indices = [x + 1 for x in resource_indices]

    # Sort machines by cost
    machine_indices = sorted(inputs.machines, key=inputs.machines.get, reverse = maxMachine)

    # Round-robin selection of task based on cost per resource and machine cost
    resources_round_robin = itertools.cycle(resource_indices)
    machines_round_robin = itertools.cycle(machine_indices)
    machine = next(machines_round_robin)
    while task_list:
        resource = next(resources_round_robin)
        task = [machine, resource]
        if task in task_list:
            task_list.pop(task_list.index(task))
            sequence.append(task)
            machine = next(machines_round_robin)
            continue
        # Assign next resource to a valid machine
        for _ in range(len(machine_indices)):
            machine = next(machines_round_robin)
            task = [machine, resource]
            if task in task_list:
                task_list.pop(task_list.index(task))
                sequence.append(task)
                break

    return sequence

"""
Function to write out the sequence in Simul8 format
JFL20231026: add a sequence column
"""
def output_sequence(file_name, list_seq):
    with open("outputs/" + file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "", ""])
        writer.writerow(["", "time", "lbl_seq", "lbl_loc", "lbl_resource"])
        for i, task in enumerate(list_seq):
            writer.writerow(["", 0, i, task[0], task[1]])

def output_sequence2(file_name, list_seq):
    return
    # with open("outputs_simul8/" + file_name, 'w', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), "", ""])
    #     writer.writerow(["", "time", "lbl_seq", "lbl_loc", "lbl_resource"])
    #     for i, task in enumerate(list_seq):
    #         writer.writerow(["", 0, i, task[0], task[1]])

if __name__ == "__main__":
    # Read tests from the file
    tests = readTests("test2run.txt")

    for test in tests:
        # Read inputs for the test instance
        inputs = readInputs(test.instanceName)
        rng = random.Random(test.seed)

        # Skip instance if file was not found
        if inputs == None:
            continue

        if test.execType == 0:
            # Compute sequence using a FIFO approach
            sol_fifo = calculate_fifo(inputs, rng)
            out_fifo = f"{test.instanceName}_input_fifo.csv"
            output_sequence(out_fifo, sol_fifo)
            out_fifo2 = f"{test.instanceName}_output_fifo.csv"
            output_sequence2(out_fifo2, sol_fifo)
        elif test.execType == 1:
            # Compute sequence using a random approach
            sol_rand = calculate_random(inputs, rng)
            out_rand = f"{test.instanceName}_input_rand.csv"
            output_sequence(out_rand, sol_rand)
            out_rand2 = f"{test.instanceName}_output_rand.csv"
            output_sequence2(out_rand2, sol_rand)
        elif test.execType == 2:
            # Compute sequence minimizing resource and machine costs
            sol_min = calculate_sequence(inputs, False, False, rng)
            out_min = f"{test.instanceName}_input_min.csv"
            output_sequence(out_min, sol_min)
            out_min2 = f"{test.instanceName}_output_min.csv"
            output_sequence2(out_min2, sol_min)
        elif test.execType == 3:
            # Compute sequence maximizing resource and machine costs
            sol_max = calculate_sequence(inputs, True, True, rng)
            out_max = f"{test.instanceName}_input_max.csv"
            output_sequence(out_max, sol_max)
            out_max2 = f"{test.instanceName}_output_max.csv"
            output_sequence2(out_max2, sol_max)
        elif test.execType == 4:
            # Compute sequence minimizing resource and maximizing machine costs
            sol_min_max = calculate_sequence(inputs, False, True, rng)
            out_min_max = f"{test.instanceName}_input_min_max.csv"
            output_sequence(out_min_max, sol_min_max)
            out_min_max2 = f"{test.instanceName}_output_min_max.csv"
            output_sequence2(out_min_max2, sol_min_max)
        else:
            # Compute sequence maximizing resource and minimizing machine costs
            sol_max_min = calculate_sequence(inputs, True, False, rng)
            out_max_min = f"{test.instanceName}_input_max_min.csv"
            output_sequence(out_max_min, sol_max_min)
            out_max_min2 = f"{test.instanceName}_output_max_min.csv"
            output_sequence2(out_max_min2, sol_max_min)
