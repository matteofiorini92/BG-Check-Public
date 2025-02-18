import os
from decimal import Decimal
from datetime import datetime

TIMES = {
    'DAY': {
        'FROM': datetime.strptime("08:00", '%H:%M').time(),
        'TO': datetime.strptime("23:00", '%H:%M').time()
    },
    'NIGHT': {
        'FROM': datetime.strptime("23:00", '%H:%M').time(),
        'TO': datetime.strptime("08:00", '%H:%M').time()
    },
    'PEAK': {
        'FROM': datetime.strptime("17:00", '%H:%M').time(),
        'TO': datetime.strptime("19:00", '%H:%M').time()
    },
    'EV': {
        'FROM': datetime.strptime("02:00", '%H:%M').time(),
        'TO': datetime.strptime("05:00", '%H:%M').time()
    }
}

VAT = Decimal("0.09")

DISCOUNT = Decimal(os.environ.get("DISCOUNT"))

STANDING_CHARGE_EXCL_VAT = Decimal(os.environ.get("STANDING_CHARGE"))

PSO_LEVY = Decimal(os.environ.get("PSO_LEVY"))

BASE_RATES_EXCL_VAT = {
    'DAY': Decimal(os.environ.get("BASE_RATE_EXCL_VAT_DAY")),
    'NIGHT': Decimal(os.environ.get("BASE_RATE_EXCL_VAT_NIGHT")),
    'PEAK': Decimal(os.environ.get("BASE_RATE_EXCL_VAT_PEAK")),
    'EV': Decimal(os.environ.get("BASE_RATE_EXCL_VAT_EV"))
}

RATES = {
    'DAY': Decimal(os.environ.get("RATE_DAY")),
    'NIGHT': Decimal(os.environ.get("RATE_NIGHT")),
    'PEAK': Decimal(os.environ.get("RATE_PEAK")),
    'EV': Decimal(os.environ.get("RATE_EV"))
}

DAYS_OF_THE_WEEK = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}