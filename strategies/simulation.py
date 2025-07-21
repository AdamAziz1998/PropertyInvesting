import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from utils.saving import time_till_purchase, costs
from utils.repayment import step, calculate_fixed_monthly_payment
from utils.overpayments import calculate_overpayment
import math

"""
Step 1: save for a property
Step 2: if there is a property:
    - Save for a new property whilst paying off current property
    - If the savings required for a new property is acheived, put all extra cash into paying off new property
    - If the property reaches a 75% LTV before saving for a new property then only save for new property.
"""

def generate_property(next_property: str):
    return Property(
        property_value=150000 if next_property == "F" else 220000,
        buy_to_let=False,
        mortgage_length=40,
        is_flat=True if next_property == "F" else False,
    )

def saving_vs_overpayment_allocation(
        max_overpayment: int, 
        current_property: Property, 
        next_property: Property,
        current_saving: int, 
        overpayment_pct: float,
        ):
    if current_property.mortgage.mortgage_principal / current_property.property_value < 0.75:
        saving = max_overpayment
        overpayment_applied = 0
    elif current_saving > costs(next_property, True, True) + next_property.mortgage.deposit:
        saving = 0
        overpayment_applied = max_overpayment
    else:
        overpayment_applied = math.floor(max_overpayment * overpayment_pct)
        saving = max_overpayment - overpayment_applied
    return saving, overpayment_applied

def append_history(history: list, month_number: int, current_saving: int, properties: list[Property]):
        history.append({
        "month": month_number,
        "savings": current_saving,
        "properties": [
            {
                "value": p.property_value,
                "mortgage_principal": p.mortgage.mortgage_principal,
                "ltv": round(p.mortgage.mortgage_principal / p.property_value, 4)
            } for p in properties
        ]
    })


# This gets called if a property is owned
def move_forward_one_month(        
        income: int, 
        current_saving: int,
        overpayment_pct: float,
        next_property: Property,
        properties: list[Property],  #This will have the most recently purchased property, which is currently occupied
        month_number: int,
        history: list,
    ):
    current_property = properties[-1]
    max_overpayment = calculate_overpayment(current_property, income)
    # Allocate to either overpayment, or saving, or both
    saving, overpayment_applied = saving_vs_overpayment_allocation(
        max_overpayment, current_property, next_property, current_saving, overpayment_pct
    )

    current_saving += saving
    fixed_monthly_payment = calculate_fixed_monthly_payment(current_property)
    current_property = step(current_property, fixed_monthly_payment, overpayment_applied)
    properties[-1] = current_property

    append_history(history, month_number, current_saving, properties)

    return properties, current_saving

def purchase_first_property(next_property: str, current_saving: int, income: int, history: list):
    # assuming before the purchase of the new property the person rents for 1000 a month
    income_while_renting = income - 1000
    properties = []
    new_property = generate_property(next_property)
    property_bought = False
    cost = costs(new_property, True, True) + new_property.mortgage.deposit
    months = 0
    while not property_bought:
        current_saving += income_while_renting
        months += 1
        
        if cost < current_saving:
            property_bought = True
            current_saving -= cost
            properties = [new_property]

        append_history(history, months, current_saving, properties)
        
    return months, [new_property], current_saving

def balance_after_property_purchase(next_property: Property, current_saving):
    cost = costs(next_property, False, True)
    new_cash_balance = current_saving - cost - next_property.mortgage.deposit
    return  new_cash_balance

# This will move forward n months until the second property is bought
# Returning the properties and the money saved at the time and the number of months
def move_forward_n_months(
        income: int, 
        current_saving: int,
        overpayment_pct: float,
        next_property: str,
        properties: list[Property],
        months_passed: int,
        history: list,
):
    l = len(properties)
    if l != 0:
        next_prop = generate_property(next_property)
        focal_property = properties[-1]
        focal_property_LTV = focal_property.mortgage.mortgage_principal / focal_property.property_value
        #while loop depends on if the property can be purchased and the most recent property reaches a 75% or less LTV
        while balance_after_property_purchase(next_prop, current_saving) < 0 or focal_property_LTV > 0.75:
            months_passed +=1
            properties, current_saving = move_forward_one_month( #change this to return properties
                income, 
                current_saving,
                overpayment_pct,
                next_prop,
                properties,
                months_passed,
                history,
                )
            
            focal_property = properties[-1]
            focal_property_LTV = focal_property.mortgage.mortgage_principal / focal_property.property_value

        current_saving = balance_after_property_purchase(next_prop, current_saving)
        properties.append(next_prop)
        
        # The code above is wrong, the while loop needs to stop when I can afford the next property, and then the savings need to be adjust as something was bought.
        return months_passed, properties, current_saving
    else:
        return purchase_first_property(next_property, current_saving, income, history)


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
    history = []

    # Buy first property
    months_passed, properties, new_cash_bal = move_forward_n_months(
        income, 
        current_saving,
        overpayment_pct,
        strategy[0],
        properties,
        months_passed,
        history,
    )

    # Buy second property
    months_passed, properties, new_cash_bal = move_forward_n_months(
        income, 
        new_cash_bal, 
        overpayment_pct,
        strategy[1], 
        properties, 
        months_passed,
        history,
    )

    total_net_assets = 0
    for property in properties:
        total_net_assets += property.property_value - property.mortgage.mortgage_principal
    total_net_assets += new_cash_bal

    return months_passed, total_net_assets, history

if __name__ == "__main__":
    income = 1800
    current_saving = 10000
    overpayment_pct = 0.75
    strategy = "FF"

    months_passed, total_net_assets, history = test_strategy(
        income,
        current_saving,
        overpayment_pct,
        strategy,
    )

    print(f"Total months: {months_passed}")
    print(f"Net assets: £{total_net_assets:,.2f}")
    for month in history:
        print(month)

    # problem: the cost of moving into a new place if considered, but not the cost of letting off a property initally