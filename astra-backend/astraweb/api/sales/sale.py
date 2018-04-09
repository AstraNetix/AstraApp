from datetime import date   
from django.contrib.auth import get_user_model
from abc import ABC, abstractmethod

User = get_user_model()

class TokenSale(ABC):
    @property
    @classmethod
    @abstractmethod
    def STARS_PER_ETHER(cls): 
        return 1000

    @property
    @classmethod
    @abstractmethod
    def CONTRIB_STRUCTURE(cls):  
        return None

    @property
    @classmethod
    @abstractmethod
    def START_DATE(cls):   
        return date.today()

    @property
    @classmethod
    @abstractmethod
    def END_DATE(cls):   
        return NotImplemented     

    @classmethod
    @abstractmethod
    def get_bonus(cls, *args, **kwargs): 
        return NotImplementedError

    @classmethod
    def add_stars(cls, user, *args, **kwargs):
        User.add_star_tokens(
            user, 
            cls.get_bonus(user.ether_part_amount) * # TODO Get conversion rate somehow
            cls.STARS_PER_ETHER * 
            user.ether_part_amount
        )
        user.save()