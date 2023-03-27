import enum
import math
import random
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [9, 6]
plt.rcParams["figure.autolayout"] = True
plt.rcParams['font.size'] = 16

# config
TRIALS = 1000
SHUFFLES = 10
VAL_FREQS_PER_COLOR = { 0: 1 } | {
    # numerical cards, skip, reverse, plus two occur twice
        v: 2 for v in list(range(1, 10)) + ['s', 'r', '+']
    }

def main():
    OGDECK = flatten([[col + str(val)] * freq 
                for val, freq in VAL_FREQS_PER_COLOR.items() 
                for col in ['r', 'b', 'g', 'y']])
    # adjacent compatible card counts
    adj_comp_counts = [0] * (SHUFFLES + 1)
    # adjacent same color counts
    adj_same_col_counts = [0] * (SHUFFLES + 1)
    
    # print(adj_same_col_count(OGDECK))
    
    for i in range(TRIALS):
        deck = OGDECK[:]
        adj_comp_counts[0] += adj_comp_count(deck)
        adj_same_col_counts[0] += adj_same_col_count(deck)
        for s in range(1, SHUFFLES + 1):
            deck = riffle(deck)
            adj_comp_counts[s] += adj_comp_count(deck)
            adj_same_col_counts[s] += adj_same_col_count(deck)
        
        # # plot first one as an example
        # if i == 0:
        #     plt.plot(adj_comp_counts, label='# of adjacent, compatible cards in example deck')
        #     plt.plot(adj_same_col_counts, label='# of adjacent cards of the same color in example deck') 
    
    adj_comp_counts = [x / TRIALS 
                       for x in adj_comp_counts]
    adj_same_col_counts = [x / TRIALS 
                           for x in adj_same_col_counts]
    
    print(adj_comp_counts[6])
    print(adj_same_col_counts[6])
    
    plt.title('Deck Shuffledness vs. Shuffle Attempts (1k Trials)')
    plt.plot(adj_comp_counts, label='average # of adjacent, compatible cards')
    plt.plot(adj_same_col_counts, label='average # of adjacent cards of the same color')    
    # plt.plot([30]*(SHUFFLES + 1)); plt.plot([20]*(SHUFFLES + 1))
    plt.xlabel('# of shuffles')
    plt.ylim([0, 100])
    plt.xticks(range(0, SHUFFLES + 1))
    plt.yticks(range(0, 101, 10))
    plt.legend(prop={'size': 16})
    plt.show()
                        
def flatten(l):
    """Flattens a list. Trust me, I stole this code."""
    return [item for sublist in l for item in sublist]
    
    
    plt.legend()
    plt.show()
def adj_comp_count(d):
    count = 0
    for i in range(len(d) - 1):
        if compatible(d[i], d[i + 1]): count += 1
    return count
def compatible(c1, c2):
    return c1[0] == c2[0] or c1[1] == c2[1]
def adj_same_col_count(d):
    count = 0
    for i in range(len(d) - 1):
        if d[i][0] == d[i + 1][0]: count += 1
    return count
def riffle(d):
    half1, half2 = imperfectcut(d)
    newdeck = []
    
    while half1 and half2:
        # implement GSR model
        if random.random() > len(half1)/(len(half1) + len(half2)):
            newdeck += [half1.pop()]
        if random.random() > len(half2)/(len(half1) + len(half2)):
            newdeck += [half2.pop()]
    
    return newdeck + half1 + half2
def imperfectcut(d):
    cutind = round(len(d) / 2 + random.random() * 10 - 5)
    return d[:cutind], d[cutind:]

if __name__ == '__main__':
    main()