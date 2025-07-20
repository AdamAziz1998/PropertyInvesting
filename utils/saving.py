import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property, flat_first_property
import copy
import math

"""
This file will determine the amount of months it'll taketo reach a certain level of savings.
It will also take into account any upfront costs of purchasing a property.
"""

def calculate_stamp_duty(first_time_buy: bool, property: Property):
    if first_time_buy:
        return 0
    if property.property_value < 250000:
        return property.property_value * 0.03
    
    up_to250 = 250000 * 0.03
    multiplier250 = 0.05 if first_time_buy else 0.08

    if property.property_value < 925000:
        return (property.property_value - 250000) * multiplier250 + up_to250
    
    up_to925 = up_to250 + (925000 - 250000) * multiplier250 + up_to250
    multiplier925 = 0.1 if first_time_buy else 0.013

    if property.property_value < 1500000:
        return (property.property_value - 925000) * multiplier925 + up_to925
    
    up_to_1500000 = up_to925 + (1500000 - 925000) * multiplier925 + up_to925
    multiplier1500000 = 0.12 if first_time_buy else 0.15

    return (property.property_value - 1500000) * multiplier1500000 + up_to_1500000
    
# In this model will assume if it's not a first time buy then
def costs(
    property: Property,
    first_time_buy: bool,
    proffessional_moving_help: bool,
    ):
    mortgage_fees = 500	#£500 – £1,000 range
    legal_conveyancing = 1200 #£800 – £1,600 range
    survey = 500 #£400 – £600 range
    moving = 200 if proffessional_moving_help else 100 #£100 – £300 range
    stamp_duty = calculate_stamp_duty(first_time_buy, property)

    return mortgage_fees + legal_conveyancing + survey + moving + stamp_duty

def time_till_purchase(
        current_savings: int, 
        saved_per_month: int, 
        property: Property,
        first_time_buy: bool = True,
        proffessional_moving_help: bool = True,
        ):
    cost = costs(property, first_time_buy, proffessional_moving_help)
    deposit = property.mortgage.deposit

    #month is the time (in months) till the goal is reached
    months = (cost + deposit - current_savings) / saved_per_month

    return math.ceil(months)

if __name__ == "__main__":
    prop = copy.deepcopy(flat_first_property)

    current_savings = 10500
    saved_per_month = 800
    
    print(time_till_purchase(current_savings, saved_per_month, prop))