from datetime import date, timedelta, datetime
from api.sales.sale import TokenSale

class TokenPreSale(TokenSale):
    STARS_PER_ETHER     =   1000  
    CONTRIB_STRUCTURE   =   {
                                timedelta(1)   :   1.50,
                                timedelta(7)   :   1.40, 
                                timedelta(14)  :   1.30, 
                                timedelta(28)  :   1.20,
                                timedelta(35)  :   1.10,
                                timedelta(42)  :   1.00,
                            }
    START_DATE          =   date(2018, 5, 5)
    END_DATE            =   date(2018, 5, 28)

    @classmethod
    def get_bonus(cls, user):
        for days, bonus in cls.CONTRIB_STRUCTURE.values():
            if user.start_time < (datetime.combine(cls.START_DATE, days)):
                return bonus