
import pandas as pd

def backtest_combos(generated_combos, historical_draws):
    historical_sets = historical_draws.apply(lambda row: set(row.dropna().astype(int).values), axis=1)
    results = []

    for combo in generated_combos:
        combo_set = set(combo)
        match_counts = [len(combo_set & past_draw) for past_draw in historical_sets]

        results.append({
            'Combo': combo,
            'Hits (3 numbers)': match_counts.count(3),
            'Hits (4 numbers)': match_counts.count(4),
            'Hits (5 numbers)': match_counts.count(5),
            'Hits (6 numbers)': match_counts.count(6),
            'Max Match in Single Draw': max(match_counts)
        })

    return pd.DataFrame(results)
