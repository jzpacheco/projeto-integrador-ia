from enum import Enum

class TaxTypes(Enum):
    pre_fixed = 'pre_fixed'
    variable_rate = 'variable_rate'
    
class CorrectionTypes(str, Enum):
    nan = 'nan'
    tr = 'tr'
    ipca = 'ipca'
    selic = 'selic'
    igpm = 'igpm'
    cdi = 'cdi'
