from datetime import date   
from api.sales.sale import TokenSale

class TokenPreSale(TokenSale):
    STARS_PER_ETHER     =   2000    
    CONTRIB_STRUCTURE   =   {
                                500000     :   1.50,
                                250000     :   1.25, 
                                100000     :   1.25, 
                                50000      :   1.25,
                                0          :   0.00,
                            }
    START_DATE          =   date(2018, 4, 24)
    END_DATE            =   date(2018, 5, 18)

    @classmethod
    def get_bonus(cls, usd):
        for min_val, bonus in cls.CONTRIB_STRUCTURE.values():
            if usd > min_val:
                return bonus
    

    