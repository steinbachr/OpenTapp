from pytz import timezone

class Formatting():
    DATE_FORMAT = "%m/%d/%Y"
    TIME_FORMAT = "%I:%M %p"
    DATETIME_FORMAT = "%m/%d/%Y at %I:%M %p"
    
class API_KEYS():
    GOOGLE_API = "AIzaSyCz1c_IrgTCVFRqtc4UwYLvKi9Tb4YCBws"
    

class Enum():
    EXCLUDE = ['__module__', '__doc__']
    
    @classmethod
    def list_for_dropdown(cls):
        return sorted([v.tuple_for_dropdown for k,v in cls.__dict__.items() if k not in cls.EXCLUDE])

    @classmethod
    def for_key(cls, key):
        for k,v in cls.__dict__.items():
            if k in cls.EXCLUDE:
                continue
            elif v.for_key(key):
                return v.for_key(key)        
    
class EnumInstance():
    def __init__(self, key_val, verbose_val, metadata_val={}):
        self.key_val = key_val
        self.verbose_val = verbose_val    
        self.metadata_val = metadata_val
        
    @property
    def tuple_for_dropdown(self):
        return (self.key_val, self.verbose_val)
    
    @property
    def verbose(self):
        return self.verbose_val
    
    @property
    def key(self):
        return self.key_val
    
    @property
    def metadata(self):
        return self.metadata_val 
    
    def for_key(self, key):
        return self if self.key_val == key else False    
    
class PossibleGroupRedemptionResults(Enum):
    FAIL     = EnumInstance(0, "Not enough people")
    TIER_ONE = EnumInstance(1, "Fits tier one")
    TIER_TWO = EnumInstance(2, "Fits tier two")
    
class DealTypes(Enum):
    SINGLE       = EnumInstance(0, "Single Deal")
    GROUP        = EnumInstance(1, "Group Deal")
    
class NavigationTabs(Enum):
    DASHBOARD   = EnumInstance(0, "tab-dashboard")
    BROADCAST   = EnumInstance(1, "tab-deal")
    QUEUE       = EnumInstance(2, "tab-queue")
    PROFILE     = EnumInstance(3, "tab-profile")
    STATS       = EnumInstance(4, "tab-stats")
    PAYMENTS    = EnumInstance(5, "tab-payments")
    HELP        = EnumInstance(6, "tab-help")    
    
    

