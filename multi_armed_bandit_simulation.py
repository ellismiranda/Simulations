from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import random


class Bandit:

    def __init__(self, prob=None):
        self.prob = prob if prob else random.random()
        self.quality = 1.0
        self.count = 2.0
        self.successes = 1.0
        self.failures = 1.0

    def pull(self):
        result = random.random() < self.prob
        update_bandit(self, result)


def thompson_expected_value(bandit):
    return (bandit.successes + 1) / (bandit.successes + 1 + bandit.failures + 1)


def generate_bandits(num):
    return [Bandit() for i in range(num)]


def update_bandit(bandit, result):
    if result:
        bandit.successes += 1
    else:
        bandit.failures += 1
    bandit.count += 1
    bandit.quality = bandit.successes / bandit.count


def log(logs, bandits, targets):
    for target in targets:
        logs[target].append([getattr(bandit, target) for bandit in bandits])
    return logs


def graph_logs(logs):
    for target in logs:
        df = pd.DataFrame.from_dict(logs[target])
        ax = df.plot(style='-')
        ax.set_xlabel('epochs')
        ax.set_ylabel(target)
    plt.show()


def run(num_bandits, epochs, epsilon, targets):
    bandits = generate_bandits(num_bandits)
    logs = defaultdict(list)

    for epoch in range(epochs):
        if random.random() > epsilon:
            bandit_chosen = max(bandits, key=thompson_expected_value)
        else:
            bandit_chosen = random.choice(bandits)

        bandit_chosen.pull()
        log(logs, bandits, targets)

    return logs


if __name__ == '__main__':
    n_bandits = 3
    n_epochs = 1000
    epsilon = 0.2
    targets = ['successes', 'quality']

    logs = run(n_bandits, n_epochs, epsilon, targets)
    graph_logs(logs)
