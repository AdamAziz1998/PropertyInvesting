import sys
import os
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from utils.saving import costs
from utils.repayment import step, calculate_fixed_monthly_payment
from utils.overpayments import calculate_overpayment

"""
Strategy Steps:
1. Save for a property.
2. If a property is owned:
   - Save for a new property while paying off the current one.
   - Once savings reach the required amount for the next property, switch all excess funds to mortgage overpayments.
   - If the LTV of the current property reaches 75%, prioritize saving over overpaying.
"""

def generate_property(next_property: str, deposit: float) -> Property:
    """Creates a Property object with pre-defined values based on the property type."""
    is_flat = next_property == "F"
    property_value = 150000 if is_flat else 220000
    deposit_amount = property_value * deposit
    interest_rate = 0.06 if deposit == 0.05 else 0.05  # Simulating 2025 rates

    return Property(
        property_value=property_value,
        buy_to_let=False,
        mortgage_length=40,
        is_flat=is_flat,
        deposit=deposit_amount,
        interest_rate=interest_rate,
    )

def saving_vs_overpayment_allocation(
    max_overpayment: int,
    current_property: Property,
    next_property: Property,
    current_saving: int,
    overpayment_pct: float
):
    """Determines how to allocate funds between saving and overpayment."""
    current_ltv = current_property.mortgage.mortgage_principal / current_property.property_value
    required_saving = costs(next_property, False, True) + next_property.mortgage.deposit

    if current_ltv < 0.75:
        return max_overpayment, 0
    elif current_saving > required_saving:
        return 0, max_overpayment
    else:
        overpayment_applied = math.floor(max_overpayment * overpayment_pct)
        saving = max_overpayment - overpayment_applied
        return saving, overpayment_applied

def append_history(history: list, month_number: int, current_saving: int, properties: list[Property]):
    """Stores monthly progress in the history log."""
    history.append({
        "month": month_number,
        "savings": current_saving,
        "properties": [
            {
                "value": p.property_value,
                "mortgage_principal": p.mortgage.mortgage_principal,
                "ltv": round(p.mortgage.mortgage_principal / p.property_value, 4)
            }
            for p in properties
        ]
    })

def move_forward_one_month(
    income: int,
    current_saving: int,
    overpayment_pct: float,
    next_property: Property,
    properties: list[Property],
    month_number: int,
    history: list
):
    """Simulates one month of income allocation, repayment, and savings growth."""
    current_property = properties[-1]
    max_overpayment = calculate_overpayment(current_property, income)
    saving, overpayment_applied = saving_vs_overpayment_allocation(
        max_overpayment, current_property, next_property, current_saving, overpayment_pct
    )

    current_saving += saving
    fixed_payment = calculate_fixed_monthly_payment(current_property)
    current_property = step(current_property, fixed_payment, overpayment_applied)
    properties[-1] = current_property

    append_history(history, month_number, current_saving, properties)

    return properties, current_saving

def purchase_first_property(
    next_property: str,
    current_saving: int,
    income: int,
    history: list,
    deposit: float
):
    """Simulates saving until the first property is affordable."""
    income_while_renting = income - 1000
    new_property = generate_property(next_property, deposit)
    total_cost = costs(new_property, True, True) + new_property.mortgage.deposit

    months = 0
    properties = []

    while current_saving < total_cost:
        current_saving += income_while_renting
        months += 1
        append_history(history, months, current_saving, properties)

    current_saving -= total_cost
    properties = [new_property]

    return months, properties, current_saving

def balance_after_property_purchase(next_property: Property, current_saving: int) -> float:
    """Returns the balance after purchasing a property."""
    total_cost = costs(next_property, False, True) + next_property.mortgage.deposit
    return current_saving - total_cost

def move_forward_n_months(
    income: int,
    current_saving: int,
    overpayment_pct: float,
    next_property: str,
    properties: list[Property],
    months_passed: int,
    history: list,
    deposit: float
):
    """Simulates months of progress until the next property is affordable."""
    if not properties:
        return purchase_first_property(next_property, current_saving, income, history, deposit)

    next_prop = generate_property(next_property, deposit)
    current_property = properties[-1]

    while balance_after_property_purchase(next_prop, current_saving) < 0 or \
          current_property.mortgage.mortgage_principal / current_property.property_value > 0.75:

        months_passed += 1
        properties, current_saving = move_forward_one_month(
            income,
            current_saving,
            overpayment_pct,
            next_prop,
            properties,
            months_passed,
            history,
        )
        current_property = properties[-1]

    current_saving = balance_after_property_purchase(next_prop, current_saving)
    properties.append(next_prop)

    return months_passed, properties, current_saving

def test_strategy(
    income: int,
    current_saving: int,
    overpayment_pct: float,
    strategy: str,
    deposit: float
):
    """Main simulation entry point for a 2-property strategy."""
    months_passed = 0
    properties = []
    history = []

    for prop_type in strategy:
        months_passed, properties, current_saving = move_forward_n_months(
            income,
            current_saving,
            overpayment_pct,
            prop_type,
            properties,
            months_passed,
            history,
            deposit,
        )

    total_net_assets = sum(p.property_value - p.mortgage.mortgage_principal for p in properties)
    total_net_assets += current_saving

    return months_passed, total_net_assets, history

if __name__ == "__main__":
    income = 1800
    current_saving = 5000
    overpayment_pct = 0.75
    strategy = "FF"
    deposit = 0.1

    months_passed, net_assets, history = test_strategy(
        income,
        current_saving,
        overpayment_pct,
        strategy,
        deposit,
    )

    for month in history:
        print(month)

    print(f"Total months: {months_passed}")
    print(f"Net assets: £{net_assets:,.2f}")
    # TODO: Factor in the cost of letting out the original property after moving to a new one.
