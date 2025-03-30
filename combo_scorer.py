
import pandas as pd
import numpy as np

def score_combo(combo, recent_draws):
    combo_set = set(combo)
    numbers = recent_draws.values.flatten()
    number_freq = pd.Series(numbers).value_counts()

    hotness = sum([number_freq.get(n, 0) for n in combo]) / len(combo)

    sorted_c = sorted(combo)
    deltas = [sorted_c[i+1] - sorted_c[i] for i in range(len(sorted_c) - 1)]
    total_gap = sum(deltas)
    proportions = [d / total_gap for d in deltas] if total_gap > 0 else [0]
    entropy = -sum(p * np.log2(p) for p in proportions if p > 0)

    avg_gap = total_gap / len(deltas)
    gap_score = max(0, 1 - abs(avg_gap - 8) / 8)

    recent_sums = recent_draws.sum(axis=1)
    combo_sum = sum(combo)
    avg_sum = recent_sums.mean()
    sum_score = max(0, 1 - abs(combo_sum - avg_sum) / avg_sum)

    total_score = round((hotness * 0.4 + entropy * 10 * 0.3 + gap_score * 10 * 0.2 + sum_score * 10 * 0.1), 2)

    return {
        'Combo': combo,
        'Hotness': round(hotness, 2),
        'Entropy': round(entropy, 3),
        'Gap Score': round(gap_score, 3),
        'Sum Score': round(sum_score, 3),
        'Total Score': total_score
    }
