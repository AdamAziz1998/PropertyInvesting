import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from properties import Property
from simulation import test_strategy

different_inital_ltv = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
overpayment_pct = [i/100 for i in range(0, 101)]
strategies = ['HH', 'FF', 'HF', 'FH']

def run(initial_ltvs: list[float], overpayment_pcts: list[float], strategies: list[str]):
    for i in range(initial_ltvs):
        for j in range(overpayment_pcts):
            for k in range(strategies):
                return