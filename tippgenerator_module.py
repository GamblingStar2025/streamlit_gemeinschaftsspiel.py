
import random
from collections import Counter

def get_hot_numbers(history, top_n=20):
    flat = [n for row in history for n in row]
    return [num for num, _ in Counter(flat).most_common(top_n)]

def get_cyclic_numbers(history, window=20):
    repeating = []
    for i in range(len(history) - window):
        past = set(history[i:i+window])
        future = set(history[i+window:i+window+5])
        repeating.extend(set(past).intersection(future))
    return list(set(repeating))

def monte_carlo_simulation(pool, k=5, simulations=10000):
    if len(pool) < k:
        pool += random.sample(range(1, 51), k - len(pool))
    result_counter = Counter()
    for _ in range(simulations):
        draw = tuple(sorted(random.sample(pool, k)))
        result_counter[draw] += 1
    return max(result_counter, key=result_counter.get)

def generate_star_numbers(sim=5000):
    result_counter = Counter()
    for _ in range(sim):
        draw = tuple(sorted(random.sample(range(1, 13), 2)))
        result_counter[draw] += 1
    return max(result_counter, key=result_counter.get)

def generiere_tipps(anzahl, history, ki_gewichtung=100, sim=100000):
    tipps = []
    hot = get_hot_numbers(history)
    repeat = get_cyclic_numbers(history)
    pool = list(set(hot + repeat))

    for _ in range(anzahl):
        zahlen = monte_carlo_simulation(pool, 5, simulations=sim)
        sterne = generate_star_numbers(sim=sim // 2)
        tipps.append((zahlen, sterne))
    return tipps
