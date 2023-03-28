import enum
import math
import random
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [9, 6]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 16

# config
# TRIALS = 3000
# SHUFFLES = 7
VAL_FREQS_PER_COLOR = { 0: 1 } | {
    # numerical cards, skip, reverse, plus two occur twice
        v: 2 for v in list(range(1, 10)) + ['s', 'r', '+']
    }

"""Findings:
Around 3 shuffles is reasonable for both metrics.

There are 96 adjacent, compatible cards in a completely unshuffled deck, reduced to ~29.88 after 7 shuffles.

There are 96 adjacent cards of the same color in a completely unshuffled deck, reduced to ~24.29 after 7 shuffles.
"""

def shuffletrials(trials, shuffles, fignum):
    OGDECK = flatten([[col + str(val)] * freq 
                for col in ['r', 'b', 'g', 'y']
                for val, freq in VAL_FREQS_PER_COLOR.items()])
    
    # print(OGDECK)
    
    # adjacent compatible card counts
    adj_comp_counts = [0] * (shuffles + 1)
    # adjacent same color counts
    adj_same_col_counts = [0] * (shuffles + 1)
    
    # print(adj_same_col_count(OGDECK))
    
    for i in range(trials):
        deck = OGDECK[:]
        adj_comp_counts[0] += adj_comp_count(deck)
        adj_same_col_counts[0] += adj_same_col_count(deck)
        for s in range(1, shuffles + 1):
            deck = riffle(deck)
            adj_comp_counts[s] += adj_comp_count(deck)
            adj_same_col_counts[s] += adj_same_col_count(deck)
        
        # # plot first one as an example
        # if i == 0:
        #     plt.plot(adj_comp_counts, label='# of adjacent, compatible cards in example deck')
        #     plt.plot(adj_same_col_counts, label='# of adjacent cards of the same color in example deck') 
    
    adj_comp_counts = [x / trials 
                       for x in adj_comp_counts]
    adj_same_col_counts = [x / trials 
                           for x in adj_same_col_counts]
    
    print(f'{adj_comp_counts[0]} -> {adj_comp_counts[39]}')
    print(f'{adj_same_col_counts[0]} -> {adj_same_col_counts[39]}')
    
    plt.title(f'Deck Shuffledness vs. Shuffle Attempts ({trials} Trials)')
    plt.plot(adj_comp_counts, label='average # of adjacent, compatible cards')
    plt.plot(adj_same_col_counts, label='average # of adjacent cards of the same color')    
    # plt.plot([30]*(shuffles + 1)); plt.plot([20]*(shuffles + 1))
    plt.xlabel('# of shuffles')
    plt.ylim([0, 100])
    plt.xticks(range(0, shuffles + 1))
    plt.yticks(range(0, 101, 10))
    plt.grid()
    plt.legend(prop={'size': 16})
    # plt.show()
    plt.savefig(f'Figure_{fignum}.png', dpi=300)
    plt.clf()
                        
def flatten(l):
    """Flattens a list. Trust me, I stole this code."""
    return [item for sublist in l for item in sublist]
    
    
    plt.legend()
    plt.show()
def adj_comp_count(d):
    count = 0
    for i in range(len(d)):
        if compatible(d[i], d[(i + 1) % len(d)]):
            # if i == len(d) - 2:
            #     count += 2
            # else:
                count += 1
    return count
def compatible(c1, c2):
    return c1[0] == c2[0] or c1[1] == c2[1]
def adj_same_col_count(d):
    count = 0
    for i in range(len(d)):
        if d[i][0] == d[(i + 1) % len(d)][0]: 
            # if i == len(d) - 2:
            #     count += 2
            # else:
                count += 1
    return count
def riffle(d):
    half1, half2 = imperfectcut(d)
    newdeck = []
    
    while half1 and half2:
        # implement GSR model
        r = random.randint(0, len(half1) + len(half2) - 1)
        if r < len(half1):
            newdeck += [half1.pop()]
        else:
            newdeck += [half2.pop()]
        
        # if random.random() > len(half1)/(len(half1) + len(half2)):
        #     newdeck += [half1.pop()]
        # if random.random() > len(half2)/(len(half1) + len(half2)):
        #     newdeck += [half2.pop()]
    
    return half1 + half2 + newdeck
def imperfectcut(d):
    cutind = round(len(d) / 2 + random.random() * 10 - 5)
    return d[:cutind], d[cutind:]

if __name__ == '__main__':
    # shuffletrials(1,    7,   1) # all good!
    # shuffletrials(1,    100, 2)
    # shuffletrials(10000, 15,  3) # increase trials
    # shuffletrials(10000, 7,   4) # increase trials
    
    # test
    shuffletrials(10000, 40, 99)