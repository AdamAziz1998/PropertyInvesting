"""
This takes in a string nf will save up, or invest extra...
Will run the simulations and decide what is the best strategy and what will reach the goal
in the fastest possible time.
Will assume when a new property is bought the investor will move into the new property, leasing the other.
The investor won't purchase a property if LTV of current property is more than 75%.
"""

"""
I want to answer these questions:
1- If I purchase a property at a 5% deposit will I acheive my goals faster
2- Is it faster to overpay my mortgage and reach 25% 
equity and then save for another house? Or is a mix of both 
better? If so what %age of extra income goes to overpayment?
3- Should I buy a house or a flat first (or 2 flats? 2 house?)?
"""

"""
Number of tests:
Question 1 -> 5% 6% 7% 8% 9% 10%, 6 possibilities
Question 2 -> 101 posibilities, 1 for each %age from 0% to 100%
Question 3 -> 4 possibilities, (house, house), (flat, flat), (house, flat), (flat, house)
Total simulations -> 6 * 101 * 4 = 2424
"""
