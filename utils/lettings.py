import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from overpayments import calculate_expenses
from repayment import calculate_interest_only_monthly_payment, calculate_fixed_monthly_payment

"""
This file will calculate how much profit is made when letting a property
"""

def calculate_profit(property: Property, self_manage: bool = False):
    # change the line below to a calculated values (im too lazy so will use local estimates for me)
    revenue_from_tenants = 1100 if property.is_flat else 1200

    general_expenses = calculate_expenses(property)
    print("General expenses: ", general_expenses)

    managing_expenses = revenue_from_tenants * 0.12 if not self_manage else 0
    if property.mortgage.mortgage_length == 0:
        monthly_mortgage_payment = calculate_interest_only_monthly_payment(property)
    else:
        monthly_mortgage_payment = calculate_fixed_monthly_payment(property)
    
    print("Interest: ", monthly_mortgage_payment)
    total_expenses = general_expenses + managing_expenses + monthly_mortgage_payment
    print("Total expenses: ", total_expenses)


    return revenue_from_tenants - total_expenses, monthly_mortgage_payment