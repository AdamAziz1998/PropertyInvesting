import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategies.simulation import test_strategy


def find_optimal_strategy(deposit_rates: list[float], overpayment_rates: list[float], strategy_codes: list[str]):
    monthly_income = 1800
    initial_savings = 5000

    best_months = float('inf')
    best_strategy = None
    best_overpayment = None
    best_deposit = None
    highest_assets = float('-inf')

    for deposit in deposit_rates:
        for strategy in strategy_codes:
            for overpayment in overpayment_rates:
                months, net_assets, _ = test_strategy(
                    income=monthly_income,
                    current_saving=initial_savings,
                    overpayment_pct=overpayment,
                    strategy=strategy,
                    deposit=deposit
                )

                print(f"Tested - Strategy: {strategy}, Overpayment: {overpayment:.2f}, Months: {months}, Deposit: {deposit * 100}%")

                is_better = (
                    months < best_months or
                    (months == best_months and net_assets > highest_assets)
                )

                if is_better:
                    best_months = months
                    best_strategy = strategy
                    best_overpayment = overpayment
                    best_deposit = deposit
                    highest_assets = net_assets

    return best_months, best_strategy, best_overpayment, best_deposit, highest_assets


if __name__ == "__main__":
    deposit_options = [0.05, 0.10]
    overpayment_options = [i / 100 for i in range(0, 101)]
    strategy_options = ['HH', 'FF', 'HF', 'FH']

    result = find_optimal_strategy(deposit_options, overpayment_options, strategy_options)

    print("\nOptimal Strategy Found:")
    print(f"  Strategy:            {result[1]}")
    print(f"  Overpayment Rate:    {result[2]:.2f}")
    print(f"  Deposit Rate:        {result[3]:.2f}")
    print(f"  Months to Complete:  {result[0]}")
    print(f"  Net Assets Achieved: {result[4]:,.2f}")
