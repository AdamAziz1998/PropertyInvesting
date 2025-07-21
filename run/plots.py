import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strategies.simulation import test_strategy
import matplotlib.pyplot as plt

# Note: many parts of this page was ChatGPT generated.

def plot_savings_over_time(history):
    months = [entry["month"] for entry in history]
    savings = [entry["savings"] for entry in history]

    plt.figure(figsize=(10, 5))
    plt.plot(months, savings, label='Savings', color='green')
    plt.title("Savings Over Time")
    plt.xlabel("Month")
    plt.ylabel("Savings (£)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_property_value_vs_mortgage(history):
    plt.figure(figsize=(12, 6))

    property_data = {}

    # Build per-property time series only when the property appears
    for entry in history:
        month = entry["month"]
        for i, prop in enumerate(entry["properties"]):
            if i not in property_data:
                property_data[i] = {
                    "months": [],
                    "values": [],
                    "mortgages": [],
                }
            property_data[i]["months"].append(month)
            property_data[i]["values"].append(prop["value"])
            property_data[i]["mortgages"].append(prop["mortgage_principal"])

    # Plot each property's value and mortgage over time
    for i, data in property_data.items():
        plt.plot(data["months"], data["values"], label=f'Property {i+1} Value')
        plt.plot(data["months"], data["mortgages"], label=f'Property {i+1} Mortgage', linestyle='--')

    plt.title("Property Value vs Mortgage Over Time")
    plt.xlabel("Month")
    plt.ylabel("£")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_ltv_ratios(history):
    plt.figure(figsize=(10, 5))

    property_data = {}

    for entry in history:
        month = entry["month"]
        for i, prop in enumerate(entry["properties"]):
            if i not in property_data:
                property_data[i] = {
                    "months": [],
                    "ltvs": [],
                }
            property_data[i]["months"].append(month)
            property_data[i]["ltvs"].append(prop["ltv"])

    for i, data in property_data.items():
        plt.plot(data["months"], data["ltvs"], label=f'Property {i+1} LTV')

    plt.title("LTV Ratios Over Time")
    plt.xlabel("Month")
    plt.ylabel("Loan-to-Value Ratio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_net_worth(history):
    months = []
    net_worths = []

    for entry in history:
        month = entry["month"]
        savings = entry["savings"]
        equity = sum([p["value"] - p["mortgage_principal"] for p in entry["properties"]])
        total = savings + equity

        months.append(month)
        net_worths.append(total)

    plt.figure(figsize=(10, 5))
    plt.plot(months, net_worths, label="Net Worth", color="blue")
    plt.title("Net Worth Over Time")
    plt.xlabel("Month")
    plt.ylabel("Net Worth (£)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_equity_per_property(history):
    plt.figure(figsize=(10, 5))

    property_data = {}

    for entry in history:
        month = entry["month"]
        for i, prop in enumerate(entry["properties"]):
            if i not in property_data:
                property_data[i] = {
                    "months": [],
                    "equity": [],
                }
            equity = prop["value"] - prop["mortgage_principal"]
            property_data[i]["months"].append(month)
            property_data[i]["equity"].append(equity)

    for i, data in property_data.items():
        plt.plot(data["months"], data["equity"], label=f'Property {i+1} Equity')

    plt.title("Equity per Property Over Time")
    plt.xlabel("Month")
    plt.ylabel("Equity (£)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    income = 1800
    current_saving = 5000
    overpayment_pct = 0.75
    strategy = "FF"
    deposit = 0.05

    months_passed, net_assets, history = test_strategy(
        income,
        current_saving,
        overpayment_pct,
        strategy,
        deposit,
    )

    # Run plots
    plot_savings_over_time(history)
    plot_property_value_vs_mortgage(history)
    plot_ltv_ratios(history)
    plot_net_worth(history)
    plot_equity_per_property(history)