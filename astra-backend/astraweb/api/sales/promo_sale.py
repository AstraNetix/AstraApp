from datetime import date, timedelta, datetime
from api.sales.sale import TokenSale
from django.contrib.auth import get_user_model

User = get_user_model()

class PromoSale(TokenSale):
    END_DATE        =   date.today() + timedelta(days=365.25/2)

    TOTAL_STARS     =   500000

    REFERRAL        =   5
    JOINING         =   10
    TELEGRAM        =   10
    MEME            =   10
    PROOF_OF_LOVE   =   10
    WHITELIST       =   25

    @classmethod
    def add_stars(cls, user, amount):
        if date.today() <= cls.END_DATE:
            User.add_promo_star_tokens(user, amount)
            cls.TOTAL_STARS -= amount

    @classmethod
    def registered(cls, user):
        cls.add_stars(user, cls.JOINING)

    @classmethod
    def make_referee(cls, user, referral_code):
        referrer = user.add_referral(referral_code)
        if referrer:
            cls.add_stars(user, cls.REFERRAL)
            cls.add_stars(referrer, cls.REFERRAL)

    @classmethod
    def join_telegram(cls, user):
        cls.add_stars(user, cls.TELEGRAM)
    
    @classmethod
    def add_proof_of_love(cls, user):
        cls.add_stars(user, cls.PROOF_OF_LOVE)

    @classmethod
    def complete_whitelist(cls, user):
        if user.ico_complete():
            user.add(cls.WHITELIST)