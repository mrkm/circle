# -*- coding: utf-8 -*-
# coding: utf-8
import datetime

# booking state
EAST = "EAST"
WEST = "WEST"
EAST_CANCELED = "EAST_CANCELED"
WEST_CANCELED = "WEST_CANCELED"

AVAILABLE_EAST = {
    0: (datetime.time(17), datetime.time(21)),
    1: (datetime.time(17), datetime.time(21)),
    2: (datetime.time(0), datetime.time(0)),
    3: (datetime.time(17), datetime.time(21)),
    4: (datetime.time(17), datetime.time(21)),
    5: (datetime.time(0), datetime.time(0)),
    6: (datetime.time(9), datetime.time(21)),
    }

AVAILABLE_WEST = {
    0: (datetime.time(7, 30), datetime.time(22)),
    1: (datetime.time(7, 30), datetime.time(22)),
    2: (datetime.time(7, 30), datetime.time(22)),
    3: (datetime.time(7, 30), datetime.time(22)),
    4: (datetime.time(7, 30), datetime.time(22)),
    5: (datetime.time(7, 30), datetime.time(22)),
    6: (datetime.time(7, 30), datetime.time(22)),
    }
