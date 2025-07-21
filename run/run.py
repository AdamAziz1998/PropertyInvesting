import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from strategies.simulation import test_strategy

def run(initial_ltvs: list[float], overpayment_pcts: list[float], strategies: list[str]):
    income = 1800
    current_saving = 5000

    optimal_time = 1000000
    best_strategy = ""
    best_overpayment_pcts = []

    # for initial_ltv in range(initial_ltvs):   TODO: Test buying with different LTVs
    for strategy in strategies:
        for overpayment_pct in overpayment_pcts:
            months_passed, total_net_assets, history = test_strategy(income, current_saving, overpayment_pct, strategy)
            print(overpayment_pct, strategy, months_passed)

            if months_passed < optimal_time:
                optimal_time = months_passed
                best_strategy = strategy
                best_overpayment_pcts = [overpayment_pct]
            if months_passed == optimal_time and strategy == best_strategy:
                best_overpayment_pcts.append(overpayment_pct)
    
    return optimal_time, best_strategy, best_overpayment_pcts


if __name__ == "__main__":
    initial_ltvs = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    overpayment_pcts = [i/100 for i in range(0, 101)]
    strategies = ['HH', 'FF', 'HF', 'FH']
    optimal_time, best_strategy, best_overpayment_pct = run(initial_ltvs, overpayment_pcts, strategies)

    print(best_overpayment_pct, best_strategy, optimal_time)