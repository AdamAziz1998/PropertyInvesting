import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property

"""
This file will decide how much money if able to be overpayed to overpaying a mortgage, or saving
for a new deposit
"""

def calculate_expenses(property: Property):
    # Will assume maintenance costs of 1% of property value per year
    general_maintanence = property.property_value * 0.01 / 12
    service_charge = 2400 / 12 if property.is_flat else 0
    return general_maintanence + service_charge

def calculate_overpayment(property: Property, income: int):
    total_maintenance = calculate_expenses(property)
    overpayment = income - total_maintenance

    if overpayment < 0:
        print("overpayment is negative: increase income")
        return
    
    return overpayment

    
    


    
