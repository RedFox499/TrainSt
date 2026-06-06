Y_P5 = 125
Y_P3 = 245
Y_P1 = 365
Y_P2 = 485
Y_P4 = 605


positions = {
    "before_M6": (100, Y_P2),
    "M6": (170, Y_P2),
    "H4": (460, 605),
    "H2": (460, Y_P2),
    "M8": (350, Y_P1),
    "M10": (330, Y_P3),
    "before_M10": (240, Y_P3),
    "H5": (560, 125),
    "H3": (560, Y_P3),
    "H1": (520, Y_P1),
    "1_AK": (200, Y_P1),
    "Turn_14_J": (330, Y_P2),
    "Turn_6_A": (240, Y_P2),
    "Turn_6_B": (260, Y_P2),
    "Turn_8_B": (320, Y_P1),


    "Ч1": (1100, Y_P1),
    "Ч2": (900, Y_P2),
    "Ч3": (900, Y_P3),
    "Ч4": (900, Y_P4),
    "Ч5": (900, Y_P5),

    "M1": (1660, Y_P1),
    "M3": (1690, Y_P2),
    "M5": (1380, Y_P2),
    "M7": (1380, Y_P3),

    "H": (1770, Y_P1),
    "1": (1900, Y_P1),

    "Ч2M5mid": (1210, Y_P2),
    "Ч2M5third": (1260, Y_P2),

    "beforeM7": (1300, Y_P3),

    "Ч1M1first": (1320, Y_P1),
    "Ч1M1second": (1370, Y_P1),

    "Ч1M1mid": (1450, Y_P1),
    "Ч3M7mid": (1200, Y_P3),
    "M5M3mid": (1530, Y_P2),
    "M5M3third": (1570, Y_P2),
    "beforeM5": (1280, Y_P2),

    "beforeM1": (1540, Y_P1),

    "Ч3beforeM7": (1120, Y_P3),

    "pastM7": (1600, Y_P3),

    "M3MID6": (1770, Y_P2),
    "6": (1880, Y_P2),

    "Turn12_16mid": (465, 245),
    "Turn8B_M8mid": (330, Y_P1)

    # "Ч1": (100, Y_P1),
    # "Ч2": (100, Y_P2),
    # "Ч3": (100, Y_P3),
    # "Ч4": (100, Y_P4),
    # "Ч5": (100, Y_P5),
    #
    # "M1": (860, Y_P1),
    # "M3": (890, Y_P2),
    # "M5": (580, Y_P2),
    # "M7": (580, Y_P3),
    #
    # "H": (970, Y_P1),
    # "1": (1100, Y_P1),
    #
    # "Ч2M5mid": (410, Y_P2),
    # "Ч2M5third": (460, Y_P2),
    #
    # "beforeM7": (500, Y_P3),
    #
    # "Ч1M1first": (520, Y_P1),
    # "Ч1M1second": (570, Y_P1),
    #
    # "Ч1M1mid": (650, Y_P1),
    # "Ч3M7mid": (400, Y_P3),
    # "M5M3mid": (730, Y_P2),
    # "M5M3third": (770, Y_P2),
    # "beforeM5": (480, Y_P2),
    #
    # "beforeM1": (740, Y_P1),
    #
    # "Ч3beforeM7": (320, Y_P3),
    #
    # "pastM7": (800, Y_P3),
    #
    # "M3MID6": (970, Y_P2),
    # "6": (1080, Y_P2),
}
segments = [

    ("H4", "Ч4"),
    ("H2", "Ч2"),
    ("H1", "Ч1"),
    ("H3", "Ч3"),
    ("H5", "Ч5"),
    ("Turn_14_J", "H2"),
    ("Turn_6_B", "Turn_14_J"),
    ("Turn_6_B", "Turn_6_A"),
    ("M6", "Turn_6_A"),
    ("before_M6", "M6"),
    ("Turn_8_B", "M8"),
    ("Turn_8_B", "1_AK"),
    ("before_M10", "M10"),

    ("Ч3beforeM7", "Ч3"),

    ("Ч3beforeM7", "Ч3M7mid"),

    ("beforeM7", "Ч3M7mid"),
    ("beforeM7", "M7"),

    ("Ч1M1first", "Ч1"),
    ("Ч1M1second", "Ч1M1first"),

    ("Ч1M1second", "Ч1M1mid"),

    ("beforeM1", "Ч1M1mid"),
    ("beforeM1", "M1"),

    ("M1", "H"),
    ("H", "1"),

    ("Ч2M5mid", "Ч2"),
    ("Ч2M5mid", "Ч2M5third"),

    ("beforeM5", "Ч2M5third"),
    ("beforeM5", "M5"),


    ("M5", "M5M3mid"),

    ("M5M3mid", "M5M3third"),
    ("M3", "M5M3third"),

    ("M7", "pastM7"),

    ("M3", "M3MID6"),
    ("M3MID6", "6"),

    ("M10", "Turn12_16mid"),
    ("Turn12_16mid", "H3"),
    ("Turn8B_M8mid", "H1")
]

SEGMENT_ORDER = [
    # Твои 6 реальных сегментов (названия строго как в ключах кортежей)
    ("M6", "beforeM6"),
    ("M2", "Ч"),
    ("M10", "H3"),
    ("M8", "H1"),
    ("M10", "H3"),
    ("M8mid", "M8"),
    ("M2", "M2H1_mid"),
    ("ALB_Sect1", "ALB_Sect1-2"),
    ("M6H2", "M6"),


    # И 18 пустых заглушек, чтобы цикл в Python не упал
    "EMPTY", "EMPTY", "EMPTY", "EMPTY",
    "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY",
    "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY", "EMPTY"
]

segment_to_block = {}
segment_to_block_type = {}


segment_groups = {
    "Ч3_до_М7": [
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3")},
        {"type": "segment", "id":  ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "M7")},
    ],
    "Ч1_до_Сер_1_Путь    ": [
        {"type": "segment", "id": ("Ч1M1first", "Ч1")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},

    ],
    "После_Сер_1_Путь": [
        {"type": "segment", "id":("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("beforeM1", "M1")},
    ],
    "Ч2_до_М5": [
        {"type": "segment", "id": ("Ч2M5mid", "Ч2")},
        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id":("beforeM5", "Ч2M5third")},
        {"type": "segment", "id":("beforeM5", "M5")},
    ],
    "ПослеМ5_До_М3": [
        {"type": "segment", "id":("M5M3mid", "M5M3third")},
        {"type": "segment", "id": ("M3", "M5M3third")},
    ],
    "M6_After6-8": [
        {"type": "segment", "id":("Turn_6_B", "Turn_14_J")},
        {"type": "segment", "id": ("Turn_6_B", "Turn_6_A")},
        {"type": "segment", "id":  ("M6", "Turn_6_A")},
    ],
    "M10_до_H3": [
        {"type": "segment", "id": ("M10", "Turn12_16mid")},
        {"type": "segment", "id": ("Turn12_16mid", "H3")}
    ],
    "M6_до_H2": [
        {"type": "segment", "id": ("M6", "Turn_14_J")},
        {"type": "segment", "id": ("Turn_14_J", "H2")},
    ],
}

split_parts_map = {
    "AKZHT_Turn5-7": {
        "partA": "AKZHT_Turn5",
        "partB": "AKZHT_Turn7"
    },
    "AKZHT_Turn13-15": {
        "partA": "AKZHT_Turn13",
        "partB": "AKZHT_Turn15"
    },
    "AKZHT_Turn9-11": {
        "partA": "AKZHT_Turn9",
        "partB": "AKZHT_Turn11"
    },
    "AKZHT_Turn1-3": {
        "partA": "AKZHT_Turn1",
        "partB": "AKZHT_Turn3"
    },
    "AKZHT_Turn6-8": {
        "partA": "AKZHT_Turn6",
        "partB": "AKZHT_Turn8"
    },
    "AKZHT_Turn10-12": {
        "partA": "AKZHT_Turn10",
        "partB": "AKZHT_Turn12"
    }
}
switch_list = ["AKZHT_Turn19", "AKZHT_Turn17", "AKZHT_Turn5-7", "AKZHT_Turn13-15", "AKZHT_Turn9-11", "AKZHT_Turn1-3", "AKZHT_Turn6-8", "AKZHT_Turn10-12",
               "AKZHT_Turn16"]

default_switch_mode = {
    "AKZHT_Turn19": "left",
    "AKZHT_Turn17": "left",
    "AKZHT_Turn5-7": "left",
    "AKZHT_Turn13-15": "left",
    "AKZHT_Turn9-11": "left",
    "AKZHT_Turn1-3": "left",
    "AKZHT_Turn6-8": "left",
    "AKZHT_Turn10-12": "left",
    "AKZHT_Turn16": "left"
}
segment_to_signal = {
    ("Ч3beforeM7", "Ч3"): "Ч3",
    ("Ч3beforeM7", "Ч3M7mid"): "Ч3",
    ("beforeM7", "Ч3M7mid"): "Ч3",

    ("beforeM7", "M7"): "M7",

    ("beforeM1", "Ч1M1mid"): "M1",
    ("beforeM1", "M1"): "M1",

    ("M1", "H"): ["H", "Ч1", "Ч2", "Ч3", "Ч4", "Ч5"],


    ("H", "1"): "1",

    ("Ч1M1first", "Ч1"): "Ч1",
    ("Ч1M1second", "Ч1M1first"): "Ч1",
    ("Ч1M1second", "Ч1M1mid"): "Ч1",


    ("Ч2M5mid", "Ч2"): "Ч2",
    ("Ч2M5mid", "Ч2M5third"): "Ч2",
    ("beforeM5", "Ч2M5third"): "Ч2",

    ("beforeM5", "M5"): "М5",

    ("M5M3mid", "M5M3third"): "М3",
    ("M3", "M5M3third"): "М3",

    ("M3", "M3MID6"): ["Ч5", "Ч4", "Ч3", "Ч2", "Ч1"],




}

diag_to_signal = {
    "AKZHT_Turn19": "Ч4",
 #   "AKZHT_Turn17": "Ч5",


}
diagonal_config = {

    "AKZHT_Turn19": {
        "left":  {"exists": True, "connected": 0,  "disconnected": 0 },
        "right": {"exists": True, "connected": -5, "disconnected": +5},
        "default": "both"
    },

    "AKZHT_Turn17": {
        "left": {"exists": True, "connected": 0, "disconnected": 0},
        "right": {"exists": True, "connected": +6, "disconnected": -6},
        "default": "both"
    },

    "AKZHT_Turn5-7": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },

    "AKZHT_Turn13-15": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "AKZHT_Turn9-11": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "AKZHT_Turn1-3": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "AKZHT_Turn6-8": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "AKZHT_Turn10-12": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },

    "AKZHT_Turn16": {
        "left": {"exists": True, "connected": 0, "disconnected": 0},
        "right": {"exists": True, "connected": +5, "disconnected": -5},
        "default": "both"
    }
}

signals_config_simple = {
    "Ч1": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "Ч2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "Ч3": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "Ч4": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "Ч5": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "H": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["red", "white", "yellow"],
        "position_map": {
            "red": [0],
            "white": [0],
            "green": [0],
            "yellow1": [0, 1],
            "yellow2": [0, 1],
        }
    },
    "M7": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "M5": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "M3": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "M1": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "1": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "6": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "M10": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 1,
        "colors": ["red", "white"],
        "single": True
    }
}




signals_config = {
    "Ч1": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "Ч2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "Ч3": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "Ч4": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "Ч5": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "M7": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["white", "blue"],
        "type": "maneuver"
    },
    "M5": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["white", "blue"],
        "type": "maneuver"
    },
    "M3": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["white", "blue"],
        "type": "maneuver"
    },
    "M1": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["white", "blue"],
        "type": "maneuver"
    },
    "1": {
        "mount": "top",
        "pack_side": "left",
        "count": 3,
        "colors": ["yellow", "green", "red"],
        "type": "train"
    },
    "H": {
        "mount": "top",
        "pack_side": "left",
        "count": 5,
        "colors": ["yellow", "green", "red", "yellow1", "white"],
        "type": "train"
    },
    "6": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 3,
        "colors": ["red", "green", "yellow"],
        "type": "train"
    },
    "M10": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white"],
        "type": "maneuver"
    }
}
ROUTE_SIGNAL_MAP: dict[tuple[str, str], dict[str, dict[str, object]]] = {
    ("Ч5", "6"): {
        "Ч5": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },
    ("Ч3", "6"): {
        "Ч3": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },
    ("Ч2", "6"): {
        "Ч2": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },
    ("Ч1", "6"): {
        "Ч1": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },
    ("Ч4", "6"): {
        "Ч4": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },

    ("1", "Ч4"): {
        "H": {"lamps": {"yellow": {"on": True, "blink": False}, }, },
    },
    ("1", "Ч3"): {
        "H": {"lamps": {"yellow": {"on": True, "blink": False}, }, },
    },
    ("1", "Ч2"): {
        "H": {"lamps": {"yellow": {"on": True, "blink": False}, }, },
    },
    ("1", "Ч1"): {
        "H": {"lamps": {"yellow": {"on": True, "blink": False}, }, },
    },
    ("1", "Ч5"): {
        "H": {"lamps": {"yellow": {"on": True, "blink": False}, }, },
    },


}

routes_dir = {
    ("M2", "H3"): "right",
    ("M2", "H1"): "right",
    ("M2", "M8"): "right",
    ("M2", "M1"): "right",
    ("M2", "M10"): "right",
    ("M2", "H2"): "right",
    ("M2", "H4"): "right",
    ("M2", "1"): "right",
    ("M2", "2"): "right",
    ("M2", "4"): "right",
    ("H2", "M6"): "left",
    ("H2", "M2"): "left",
    ("H4", "M6"): "left",
    ("H4", "M2"): "left",
    ("M6", "H4"): "right",
    ("M6", "H2"): "right",
    ("M6", "4"): "right",
    ("H1", "M2"): "left",
    ("M10", "M1"): "right",
    ("M1", "M2"): "left",
    ("M1", "M8"): "left",
    ("M1", "H3"): "left",
    ("M8", "M1"): "right",
    ("M1", "H1"): "left",
    ("M1", "M10"): "left",
    ("H3", "M2"): "left",
}
routes = {
    ("Ч5", "6"): [
        {"type": "diag", "name": "AKZHT_Turn17"},
        {"type": "segment", "id":  ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "M7")},
        {"type": "diag", "name": "AKZHT_Turn15"},
        {"type": "diag", "name": "AKZHT_Turn13"},
        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "diag", "name": "AKZHT_Turn1"},
        {"type": "diag", "name": "AKZHT_Turn3"},
        {"type": "segment", "id":("M3", "M5M3third")},
        {"type": "segment", "id": ("M3", "M3MID6")},
        {"type": "segment", "id": ("M3MID6", "6")},
    ],
    ("Ч3", "6"): [
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3")},
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "M7")},
        {"type": "diag", "name": "AKZHT_Turn15"},
        {"type": "diag", "name": "AKZHT_Turn13"},
        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "diag", "name": "AKZHT_Turn1"},
        {"type": "diag", "name": "AKZHT_Turn3"},
        {"type": "segment", "id": ("M3", "M5M3third")},
        {"type": "segment", "id": ("M3", "M3MID6")},
        {"type": "segment", "id": ("M3MID6", "6")},
    ],
    ("Ч1", "6"): [
        {"type": "segment", "id": ("Ч1M1first", "Ч1")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},

        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "diag", "name": "AKZHT_Turn1"},
        {"type": "diag", "name": "AKZHT_Turn3"},
        {"type": "segment", "id": ("M3", "M5M3third")},
        {"type": "segment", "id": ("M3", "M3MID6")},
        {"type": "segment", "id": ("M3MID6", "6")},
    ],
    ("Ч2", "6"): [
        {"type": "segment", "id": ("Ч2M5mid", "Ч2")},
        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "M5")},
        {"type": "segment", "id": ("M5M3mid", "M5M3third")},
        {"type": "segment", "id": ("M5", "M5M3mid")},
        {"type": "segment", "id": ("M3", "M5M3third")},
        {"type": "segment", "id": ("M3", "M3MID6")},
        {"type": "segment", "id": ("M3MID6", "6")},
    ],
    ("Ч4", "6"): [
        {"type": "diag", "name": "AKZHT_Turn19"},
        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "M5")},
        {"type": "segment", "id": ("M5M3mid", "M5M3third")},
        {"type": "segment", "id": ("M5", "M5M3mid")},
        {"type": "segment", "id": ("M3", "M5M3third")},
        {"type": "segment", "id": ("M3", "M3MID6")},
        {"type": "segment", "id": ("M3MID6", "6")},
    ],

    ("1", "Ч4"): [
        {"type": "segment", "id": ("H", "1")},
        {"type": "segment", "id": ("M1", "H")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "segment", "id":  ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id":  ("Ч1M1second", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},

        {"type": "diag", "name": "AKZHT_Turn5"},
        {"type": "diag", "name": "AKZHT_Turn7"},

        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "M5")},
        {"type": "diag", "name": "AKZHT_Turn19"},


    ],
    ("1", "Ч2"): [
        {"type": "segment", "id": ("M1", "H")},
        {"type": "segment", "id": ("H", "1")},
        {"type": "segment", "id":   ("beforeM1", "M1")},
        {"type": "segment", "id":  ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id":  ("Ч1M1second", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},

        {"type": "diag", "name": "AKZHT_Turn5"},
        {"type": "diag", "name": "AKZHT_Turn7"},

        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "Ч2M5third")},
        {"type": "segment", "id": ("beforeM5", "M5")},
        {"type": "segment", "id": ("Ч2M5mid", "Ч2")},

    ],

    ("1", "Ч3"): [
        {"type": "segment", "id": ("M1", "H")},
        {"type": "segment", "id": ("H", "1")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},

        {"type": "diag", "name": "AKZHT_Turn15"},
        {"type": "diag", "name": "AKZHT_Turn13"},

        {"type": "segment", "id":    ("Ч3beforeM7", "Ч3")},
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id":   ("beforeM7", "M7")},

    ],

    ("1", "Ч1"): [
        {"type": "segment", "id": ("M1", "H")},
        {"type": "segment", "id": ("H", "1")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},
        {"type": "segment", "id":  ("Ч1M1first", "Ч1")},


    ],

    ("1", "Ч5"): [
        {"type": "segment", "id": ("M1", "H")},
        {"type": "segment", "id": ("H", "1")},
        {"type": "segment", "id": ("beforeM1", "M1")},
        {"type": "segment", "id": ("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},

        {"type": "diag", "name": "AKZHT_Turn15"},
        {"type": "diag", "name": "AKZHT_Turn13"},

        {"type": "segment", "id":    ("Ч3beforeM7", "Ч3")},
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id":   ("beforeM7", "M7")},

        {"type": "diag", "name": "AKZHT_Turn17"},
    ],
}


route_switch_modes = {
    ("Ч5", "6"): {"AKZHT_Turn17":  "right", "AKZHT_Turn13-15": "right", "AKZHT_Turn1-3": "right"},
    ("Ч3", "6"): {"AKZHT_Turn17":  "left", "AKZHT_Turn13-15": "right", "AKZHT_Turn1-3": "right"},
    ("Ч1", "6"): {"AKZHT_Turn13-15": "left", "AKZHT_Turn1-3": "right", "AKZHT_Turn5-7": "left"},
    ("Ч2", "6"): {"AKZHT_Turn1-3": "left", "AKZHT_Turn5-7": "left", "AKZHT_Turn19": "left"},
    ("Ч4", "6"): {"AKZHT_Turn1-3": "left", "AKZHT_Turn5-7": "left", "AKZHT_Turn19": "right"},

    ("1", "Ч4"): {"AKZHT_Turn19": "right", "AKZHT_Turn5-7": "right",  "AKZHT_Turn1-3": "left", "AKZHT_Turn13-15": "left", "AKZHT_Turn9-11": "left"},
    ("1", "Ч2"): {"AKZHT_Turn19": "left", "AKZHT_Turn5-7": "right",  "AKZHT_Turn1-3": "left", "AKZHT_Turn13-15": "left", "AKZHT_Turn9-11": "left"},
    ("1", "Ч1"): {"AKZHT_Turn5-7": "left", "AKZHT_Turn1-3": "left", "AKZHT_Turn13-15": "left", "AKZHT_Turn9-11": "left"},
    ("1", "Ч3"): {"AKZHT_Turn1-3": "left", "AKZHT_Turn13-15": "right", "AKZHT_Turn9-11": "left", "AKZHT_Turn17": "left"},
    ("1", "Ч5"): {"AKZHT_Turn1-3": "left", "AKZHT_Turn13-15": "right", "AKZHT_Turn9-11": "left", "AKZHT_Turn17": "right"},
}
