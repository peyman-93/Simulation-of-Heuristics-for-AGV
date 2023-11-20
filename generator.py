#!/usr/bin/env python3

import random
import statistics

def generate_task_list(m, r, t):
    cost = 10

    # Generate homogeneous machine costs
    hm_costs = []
    variance = 0.2 * cost
    min_cost = round(cost - variance)
    max_cost = round(cost + variance)
    for _ in range(m):
        cost = random.randint(min_cost, max_cost)
        hm_costs.append(cost)

    # Generate heterogeneous machine costs
    ht_costs = []
    variance = 0.8 * cost
    min_cost = round(cost - variance)
    max_cost = round(cost + variance)
    for _ in range(m):
        cost = random.randint(min_cost, max_cost)
        ht_costs.append(cost)

    # Assign tasks to resources
    min_variance = None
    max_variance = None
    hm_resources = None
    ht_resources = None
    for _ in range(10):
        a = sorted(random.sample(range(1, t), r - 1) + [0, t])
        resources = [a[i+1] - a[i] for i in range(len(a) - 1)]
        variance = statistics.variance(resources)
        if min_variance is None or variance < min_variance:
            min_variance = variance
            hm_resources = resources
        if max_variance is None or variance > max_variance:
            max_variance = variance
            ht_resources = resources

    # Assign machines to resources homogeneously
    hm_tasks = []
    for resource in range(1, r + 1):
        for _ in range(hm_resources[resource - 1]):
            machine = random.randint(1, m)
            hm_tasks.append((machine, resource))

    # Assign machines to resources heterogeneously
    ht_tasks = []
    for resource in range(1, r + 1):
        for _ in range(ht_resources[resource - 1]):
            machine = random.randint(1, m)
            ht_tasks.append((machine, resource))

    # Randomize tasks order
    random.shuffle(hm_tasks)
    random.shuffle(ht_tasks)

    for i in range(1, 5):
        # Determine the filename based on the parameters and cost type
        filename = f"m{m}r{r}t{t}_{i:02d}"

        with open("inputs/" + filename + ".txt", 'w') as f:
            # Write the machine, resource, and task count to the file
            f.write(f"{m},{r},{t}\n")

            # Assign machine costs
            costs = hm_costs if i % 2 == 1 else ht_costs
            for cost in costs:
                f.write(f"{cost}\n")

            # Assign machines to resources
            tasks = hm_tasks if i < 3 else ht_tasks
            for (machine, resource) in tasks:
                f.write(f"{machine},{resource}\n")

if __name__ == "__main__":
    # Assign seed to the random number generator
    random.seed(42)

    # Generate instances for combinations of machines, resources and tasks
    generate_task_list(5, 3, 10)
    generate_task_list(5, 3, 20)
    generate_task_list(10, 5, 30)
    generate_task_list(10, 5, 60)
    generate_task_list(20, 10, 120)
    generate_task_list(20, 10, 240)

