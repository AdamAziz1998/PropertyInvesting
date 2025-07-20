import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from utils.saving import time_till_purchase, costs
from utils.repayment import step, calculate_fixed_monthly_payment
from utils.overpayments import calculate_overpayment
import math

def generate_property(next_property: str):
    return Property(
        property_value=220000,
        buy_to_let=False,
        mortgage_length=40,
        is_flat=True if next_property == "H" else False,
    )

def saving_vs_overpayment_allocation(max_overpayment, next_property, current_saving, overpayment_pct):
    if property.mortgage.mortgage_principal / property.property_value < 0.75:
        saving = max_overpayment
        overpayment_applied = 0
    elif current_saving > costs(next_property, True, True):
        saving = 0
        overpayment_applied = max_overpayment
    else:
        overpayment_applied = math.floor(max_overpayment * overpayment_pct)
        saving = max_overpayment - overpayment_applied
    return saving, overpayment_applied

# This gets called if a property is owned
def move_forward_one_month(        
        income: int, 
        current_saving: int,
        overpayment_pct: float,
        next_property: Property,
        property: Property,  #This will have the most recently purchased property, which is currently occupied
    ):
    max_overpayment = calculate_overpayment(property, income)
    # Allocate to either overpayment, or saving, or both
    saving, overpayment_applied = saving_vs_overpayment_allocation(
        max_overpayment, next_property, current_saving, overpayment_pct
    )

    current_saving += saving
    fixed_monthly_payment = calculate_fixed_monthly_payment(property)
    current_property = step(property, fixed_monthly_payment, overpayment_applied)

    return current_property, current_saving

def purchase_first_property(next_property, current_saving, income):
    new_property = generate_property(next_property)
    months = time_till_purchase(current_saving, income, new_property)
    cost = costs(new_property, True, True)
    new_cash_balance = (months * income) - cost - new_property.mortgage.deposit
    return months, [new_property], new_cash_balance

# This will move forward n months until the second property is bought
# Returning the properties and the money saved at the time and the number of months
def move_forward_n_months(
        income: int, 
        current_saving: int,
        overpayment_pct: float,
        next_property: str,
        properties: list,
        months_passed: int,
):
    l = len(properties)
    if l != 0:
        next_prop = generate_property(next_property)
        prop = properties[-1]
        while l != len(properties):
            current_property, current_saving = move_forward_one_month(
                income, 
                current_saving,
                overpayment_pct,
                next_prop,
                prop
                )
            months_passed +=1
        properties[len(properties) - 1] = current_property
        properties.append(next_prop)
        return months_passed, properties, current_saving
    else:
        return purchase_first_property(next_property, current_saving, income)


# Income will be the amount of money that can be used for property purposes
# For more information about strategy see ../../strategies/notes.py
# Overpayment will be the amount of extra money that can be contributed to 
# overpayment vs saving for a new property (e.gs 1.0 -> 100% of extra income towards overpayment,
# 0.6 -> 60% of extra income towards overpayment and 40% towards saving for a new property)
def test_strategy(
        income: int, 
        current_saving: int,
        overpayment_pct: float,
        strategy: str,
        ):
    months_passed = 0
    properties: list[Property] = []

    # Buy first property
    months_passed, properties, new_cash_bal = move_forward_n_months(
        income, 
        current_saving,
        overpayment_pct,
        strategy[0],
        properties,
        months_passed,

    )

    # Buy second property
    months_passed, properties, new_cash_bal = move_forward_n_months(
        income, 
        new_cash_bal, 
        overpayment_pct,
        strategy[1], 
        properties, 
        months_passed,
    )

    total_net_assets = 0
    for property in properties:
        total_net_assets += property.property_value - property.mortgage.mortgage_principal
    total_net_assets += new_cash_bal

    return months_passed, total_net_assets

"""
Step 1: save for a property
Step 2: if there is a property:
    - Save for a new property whilst paying off current property
    - If the savings required for a new property is acheived, put all extra cash into paying off new property
    - If the property reaches a 75% LTV before saving for a new property then only save for new property.
"""