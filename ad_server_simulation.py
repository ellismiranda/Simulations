from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import random
import sys

BID_FLOOR = 0.50
TARGETS = [
    'gaming',
    'whatssnoo',
    'funny',
    'leagueoflegends',
    'boottoobig',
    'pics',
    'photography',
    'catsstandingup',
]


class Ad:
    def __init__(self, name):
        self.name = str(name)
        self.targets = gen_targets()
        self.bid = gen_bid()
        self.budget = gen_budget()
        self.rate = gen_rate()
        self.clicks = 0
        self.impressions = 0
        self.ctr = 0.5

    def __str__(self):
        return " ".join([self.name, str(self.bid), str(self.rate), str(self.clicks), str(self.impressions), str(self.targets)])


class Slot:
    def __init__(self):
        self.target = random.choice(TARGETS)


def gen_bid():
    return round(random.randint(0, BID_FLOOR*10) + random.random() + BID_FLOOR, 2)


def gen_budget():
    return round(random.randint(0, BID_FLOOR*1000) + random.random(), 2)


def gen_targets():
    return random.sample(TARGETS, random.randint(1, int(len(TARGETS)/2)))


def gen_rate():
    return random.random()


def gen_ads(num):
    return [Ad(i) for i in range(0, num)]


def gen_slots(num):
    return [Slot() for i in range(0, num)]


def ctr(ad):
    return (ad.clicks + 1.0) / (ad.impressions + 2.0)


def match_target(ad, target):
    return target in ad.targets


def serve_ad(ad):
    if random.random() < ad.rate:
        ad.clicks += 1
    ad.impressions += 1
    ad.ctr = ctr(ad)


def pay(ad, price):
    ad.budget -= price
    if ad.budget < ad.bid:
        ad.bid = ad.budget


def log(logs, ads, targets):
    for target in targets:
        logs[target].append([getattr(ad, target) for ad in ads])
    return logs


def graph_logs(logs):
    for log in logs:
        df = pd.DataFrame.from_dict(logs[log])
        ax = df.plot(style="-")
        ax.set_xlabel('epochs')
        ax.set_ylabel(log)
    plt.show()


def quality_score(ad):
    return ad.bid * ad.ctr


def auction(slot, ads):
    viable_ads = [ad for ad in ads if slot.target in ad.targets and ad.budget > 0]
    sorted_ads = sorted(viable_ads, key=quality_score, reverse=True)
    if len(sorted_ads) > 0:
        if len(sorted_ads) == 1:
            return sorted_ads[0], sorted_ads[0].bid
        elif sorted_ads[0].bid > sorted_ads[1].bid:
            return sorted_ads[0], sorted_ads[1].bid
        else:
            return sorted_ads[0], sorted_ads[1].bid * (sorted_ads[1].rate / sorted_ads[0].rate)
    else:
        return None, None


def run_auction(num_ads, num_epoch, targets):
    ads = gen_ads(num_ads)
    logs = defaultdict(list)
    for i in range(0, num_epoch):
        slot = Slot()
        winner, price = auction(slot, ads)
        if winner:
            print winner.name, "wins with a bid of", winner.bid, "and a score of", quality_score(winner), "for a price of", price
            pay(winner, price)
            serve_ad(winner)
            log(logs, ads, targets)
    return logs


if __name__ == '__main__':
    try:
        num_advertisers = int(sys.argv[1])
        num_ads = int(sys.argv[2])
        print num_advertisers, num_ads
        targets = ['budget', 'bid', 'ctr', 'impressions']
        logs = run_auction(num_advertisers, num_ads, targets)
        graph_logs(logs)
    except IndexError:
        print "Please ensure correct usage:  python ad_server_simulation.py [number of advertisers] [number of ads to auction]"
