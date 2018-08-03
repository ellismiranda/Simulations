from multi_armed_bandit_simulation import generate_bandits, thompson_expected_value, update_bandit
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import math

"""
# No longer being used

def generate_actions(num):
    actions = []
    for i in range(num):
        actions.extend(
            np.random.choice([action_bandit, action_delete, action_pass], 1, p=[0.025, 0.025, 0.95]))
    return actions


def action_bandit(counts, bandits):
    counts.append(count_list())
    bandits.append(Bandit())
    return 1


def action_pass(counts, bandits):
    return 0


def action_delete(counts, bandits):
    if len(bandits) > 1:
        counts.pop()
        bandits.pop()
        return -1
    return 0
"""


def graph_allocations(allocations):
    df = pd.DataFrame.from_dict(allocations)
    df.plot(style='.')
    plt.show()


def allocate_serves(remaining_serves, expected_values, e):
    best = np.argmax(expected_values)
    allocations = []
    if len(set(expected_values)) == 1:
        allocations = [remaining_serves / len(expected_values) for i in range(len(expected_values))]
    else:
        remainder = remaining_serves % len(expected_values)
        for i in range(len(expected_values)):
            if i == best:
                allocations.append(int(math.floor(remaining_serves * (1-e)) + remainder))
            else:
                # no need to account for divide by zero because if there's a singleton list, it will not reach this
                allocations.append(int(math.floor(remaining_serves * e / (len(expected_values) - 1))))

    print allocations
    return allocations


def run(num_bandits, epochs, epsilon, allocated_serves):
    bandits = generate_bandits(num_bandits)
    allocation_log = []
    remaining_serves = allocated_serves
    e = epsilon
    for epoch in range(epochs):

        expected_values = [thompson_expected_value(bandit) for bandit in bandits]
        allocated_serves = allocate_serves(remaining_serves, expected_values, e)
        allocation_log.append(allocated_serves)

        e = .995 * e

        num_served = 0
        for b in range(num_bandits):
            for i in range(int(math.ceil(allocated_serves[b] * random.uniform(0, 0.1)))):
                result = bandits[b].pull()
                update_bandit(bandits[b], result)
                num_served += 1

        remaining_serves -= num_served

        print remaining_serves

        if remaining_serves <= 0:
            print epochs - epoch - 1, "epochs remaining"
            break

    return allocation_log


if __name__ == '__main__':

    num_bandits = 3
    num_epochs = 100
    epsilon = 0.2
    serves = 10000

    allocations = run(num_bandits, num_epochs, epsilon, serves)
    graph_allocations(allocations)



