
import random
import numpy as np
import pandas as pd

def generate_basic_combos(number_range, n_picks, total=10):
    return [sorted(random.sample(number_range, n_picks)) for _ in range(total)]

def generate_smart_combos(df, n_picks=6, total=10, top_n=25):
    flat_numbers = df.select_dtypes(include='number').values.flatten()
    freq = pd.Series(flat_numbers).value_counts().sort_values(ascending=False)
    hot_pool = freq.head(top_n).index.tolist()

    def entropy(combo):
        sorted_c = sorted(combo)
        deltas = [sorted_c[i+1] - sorted_c[i] for i in range(len(sorted_c) - 1)]
        total = sum(deltas)
        if total == 0:
            return 0
        proportions = [d / total for d in deltas]
        return -sum(p * np.log2(p) for p in proportions if p > 0)

    smart_combos = []
    while len(smart_combos) < total:
        combo = sorted(random.sample(hot_pool, n_picks))
        e = entropy(combo)
        if e >= 1.5:
            smart_combos.append({'Combo': combo, 'Entropy': round(e, 3)})

    return pd.DataFrame(smart_combos)
