import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property, flat
import numpy as np
from typing import Tuple

def calculate_fixed_monthly_payment(property: Property) -> float:
    """Calculate fixed monthly payment using standard amortization formula."""
    r = property.mortgage.interest_rate / 12
    n = property.mortgage.mortgage_length * 12
    P = property.mortgage.mortgage_principal

    return P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def calculate_interest_only_monthly_payment(property: Property) -> float:
    """Calculate monthly payment for interest-only mortgage."""
    return property.mortgage.mortgage_principal * (property.mortgage.interest_rate / 12)

def calculate_interest(property: Property): 
    """Calculate monthly interest payment (rounded up)."""
    epsilon = 0.00001
    monthly_interest_rate = property.mortgage.interest_rate / 12

    # epsilon applied to consistently round up when using number ending in 0.5
    return int(np.round(property.mortgage.mortgage_principal * monthly_interest_rate + epsilon))

def step(property: Property, fixed_monthly_payment: float, overpay: int = 0) -> Property:
    """
    Simulate one month of mortgage repayment using a fixed monthly payment plus optional overpayment.
    Returns interest and principal paid for the month.
    """
    if property.mortgage.mortgage_principal <= 0:
        return property

    interest = calculate_interest(property)
    total_payment = fixed_monthly_payment + overpay
    principal_payment = total_payment - interest

    # Clamp to remaining balance
    principal_payment = min(principal_payment, property.mortgage.mortgage_principal)

    remaining_balance = property.mortgage.mortgage_principal - principal_payment
    remaining_balance = max(0, remaining_balance)

    # Update mortgage state
    property.mortgage.mortgage_principal = remaining_balance
    if property.mortgage.months_complete == 11:
        property.mortgage.years_complete += 1
        property.mortgage.months_complete = 0
    else:
        property.mortgage.months_complete += 1
    return property

def multistep(property: Property, months: int, fixed_monthly_payment: float, overpay: int = 0):
    """Simulate multiple months of repayment."""
    for _ in range(months):
        if property.mortgage.mortgage_principal <= 0:
            break
        step(property, fixed_monthly_payment, overpay)
    


def time_to_loan_to_value(property: Property, target_ltv: float, fixed_monthly_payment: float, overpay: int = 0) -> int:
    """
    Calculate how many months it takes to reach a given LTV (e.g., 0.75 = 75% loan-to-value).
    Returns the number of months needed.
    """
    months = 0

    while (property.mortgage.mortgage_principal / property.property_value) > target_ltv:
        if property.mortgage.mortgage_principal <= 0:
            break
        step(property, fixed_monthly_payment, overpay)
        months += 1

        if months > 1000:  # safety cap (~83 years)
            print("Aborted after 1000 months.")
            break

    return months

if __name__ == "__main__":
    import copy

    # Clone the property to avoid modifying global
    prop = copy.deepcopy(flat)

    fixed_payment = calculate_fixed_monthly_payment(prop)
    maintenance = prop.property_value * 0.01 / 12
    overpay_amount = 1400 - fixed_payment - maintenance

    months = time_to_loan_to_value(prop, 0.75, fixed_payment, overpay_amount)
    print(f"Months to reach 75% LTV: {months}")
