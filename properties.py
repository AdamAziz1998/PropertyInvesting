from dataclasses import dataclass, asdict

@dataclass
class Mortgage:
    deposit: int
    mortgage_principal_init: int
    interest_rate: float
    mortgage_length: int
    years_complete: int
    months_complete: int
    mortgage_principal: int

    def to_dict(self):
        return asdict(self)

class Property:
    def __init__(
            self, 
            property_value: int, 
            buy_to_let: bool, 
            mortgage_length: int, 
            is_flat: bool,
            years_complete: int = 0, 
            months_complete: int = 0,
            deposit: float = 0.1,
            interest_rate: float = 0.05
        ):
        self.property_value = property_value
        self.buy_to_let = buy_to_let
        self.is_flat = is_flat
        mortgage_principal_init = property_value - deposit
        mortgage_principal = mortgage_principal_init
        self.mortgage = Mortgage(
            deposit=deposit,
            mortgage_principal_init=mortgage_principal_init,
            interest_rate=interest_rate,
            mortgage_length=mortgage_length,
            years_complete=years_complete,
            months_complete=months_complete,
            mortgage_principal=mortgage_principal,
        )

    def to_dict(self):
        return {
            "property_value": self.property_value,
            "buy_to_let": self.buy_to_let,
            "mortgage": self.mortgage.to_dict(),
        }
    
    def convert_to_buy_to_let(self, new_mortgage_length: int):
        """Convert property to buy-to-let, update interest rate and mortgage length.
        Returns True if conversion successful, False if not eligible."""
        ltv = self.mortgage.mortgage_principal / self.property_value
        if ltv > 0.75:
            return False  # Not eligible: LTV too high
        self.buy_to_let = True
        deposit = int(self.property_value * 0.25)
        interest_rate = 0.052
        mortgage_principal_init = self.property_value - deposit
        mortgage_principal = mortgage_principal_init
        self.mortgage = Mortgage(
            deposit=deposit,
            mortgage_principal_init=mortgage_principal_init,
            interest_rate=interest_rate,
            mortgage_length=new_mortgage_length,
            years_complete=0,
            months_complete=0,
            mortgage_principal=mortgage_principal,
        )
        return True

flat = Property(
    property_value=150000,
    buy_to_let=False,
    mortgage_length=40,
    is_flat=True,
    deposit = 0.1,
)

house = Property(
    property_value=220000,
    buy_to_let=False,
    mortgage_length=40,
    is_flat=False,
    deposit = 0.1,
)

flat_buy_to_let = Property(
    property_value=150000,
    buy_to_let=True,
    mortgage_length=25,
    is_flat=True
)

house_buy_to_let = Property(
    property_value=220000,
    buy_to_let=True,
    mortgage_length=40,
    is_flat=False
)