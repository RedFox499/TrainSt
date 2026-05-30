Y_P5 = 125
Y_P3 = 245
Y_P1 = 365
Y_P2 = 485
Y_P4 = 605


positions = {

    "Ч1": (100, Y_P1),
    "Ч2": (100, Y_P2),
    "Ч3": (100, Y_P3),
    "Ч4": (100, Y_P4),
    "Ч5": (100, Y_P5),

    "M1": (860, Y_P1),
    "M3": (890, Y_P2),
    "M5": (580, Y_P2),
    "M7": (580, Y_P3),

    "H": (970, Y_P1),
    "1": (1100, Y_P1),

    "Ч2M5mid": (410, Y_P2),
    "Ч2M5third": (460, Y_P2),

    "beforeM7": (500, Y_P3),

    "Ч1M1first": (520, Y_P1),
    "Ч1M1second": (570, Y_P1),

    "Ч1M1mid": (650, Y_P1),
    "Ч3M7mid": (400, Y_P3),
    "M5M3mid": (730, Y_P2),
    "M5M3third": (770, Y_P2),
    "beforeM5": (480, Y_P2),

    "beforeM1": (740, Y_P1),

    "Ч3beforeM7": (320, Y_P3),

    "pastM7": (800, Y_P3)
}
segments = [
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
    "block_CH3M7": [
        {"type": "segment", "id": ("Ч3beforeM7", "Ч3")},
        {"type": "segment", "id":  ("Ч3beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "Ч3M7mid")},
        {"type": "segment", "id": ("beforeM7", "M7")},
    ],
    "block_CH1M1MID": [
        {"type": "segment", "id": ("Ч1M1first", "Ч1")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1first")},
        {"type": "segment", "id": ("Ч1M1second", "Ч1M1mid")},

    ],
    "block_C1M1MID_beforeM1": [
        {"type": "segment", "id":("beforeM1", "Ч1M1mid")},
        {"type": "segment", "id": ("beforeM1", "M1")},
    ],
    "block_CH2M5": [
        {"type": "segment", "id": ("Ч2M5mid", "Ч2")},
        {"type": "segment", "id": ("Ч2M5mid", "Ч2M5third")},
        {"type": "segment", "id":("beforeM5", "Ч2M5third")},
        {"type": "segment", "id":("beforeM5", "M5")},
    ],
    "block_M5M3mid": [
        {"type": "segment", "id":("M5M3mid", "M5M3third")},
        {"type": "segment", "id": ("M3", "M5M3third")},
    ],




}

split_parts_map = {
    "ALB_Turn5-7": {
        "partA": "ALB_Turn5",
        "partB": "ALB_Turn7"
    },
    "ALB_Turn13-15": {
        "partA": "ALB_Turn13",
        "partB": "ALB_Turn15"
    },
    "ALB_Turn9-11": {
        "partA": "ALB_Turn9",
        "partB": "ALB_Turn11"
    },
    "ALB_Turn1-3": {
        "partA": "ALB_Turn1",
        "partB": "ALB_Turn3"
    },
}
switch_list = ["ALB_Turn19", "ALB_Turn17", "ALB_Turn5-7", "ALB_Turn13-15", "ALB_Turn9-11", "ALB_Turn1-3"]

default_switch_mode = {
    "ALB_Turn19": "left",
    "ALB_Turn17": "left",
    "ALB_Turn5-7": "left",
    "ALB_Turn13-15": "left",
    "ALB_Turn9-11": "left",
    "ALB_Turn1-3": "left",
}
segment_to_signal = {
    ('M8', 'M8mid'): "M8",
    ('M1', 'M8mid'): "M8",
    ("M2", "Ч"): "Ч",
    ("M2", "M2H1_mid"): "H1",
    ("M2H1_mid", "M2H1_third"): "H1",
    ("M2H1_third", "H1"): "H1",

    ('M1', 'M8mid'): "M1",
    ('M8mid', 'M8'): "M1",
    #("pastM1", "M1"): "M1",
    #("M10", "H3"): "H3",
    ("M2", "M2H1_mid"): "M2",
    ("M2H1_mid", "M2H1_third"): "M2",
    ("M2H1_third", "H1"): "M2",
    ("H2", "M6H2"): "H2",
    ("M6", "M6H2"): "M6",

}

diag_to_signal = {
    "ALB_Turn1": "M10",
    "ALB_Turn8": "H4",
    "ALB_Turn2": "H3",


}
diagonal_config = {

    "ALB_Turn19": {
        "left":  {"exists": True, "connected": 0,  "disconnected": 0 },
        "right": {"exists": True, "connected": -5, "disconnected": +5},
        "default": "both"
    },

    "ALB_Turn17": {
        "left": {"exists": True, "connected": 0, "disconnected": 0},
        "right": {"exists": True, "connected": +6, "disconnected": -6},
        "default": "both"
    },

    "ALB_Turn5-7": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },

    "ALB_Turn13-15": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "ALB_Turn9-11": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
    "ALB_Turn1-3": {
        "left": {"exists": True, "connected": 5, "disconnected": 0},
        "right": {"exists": True, "connected": 5, "disconnected": 0},
        "default": "both"
    },
}

signals_config_simple = {
    "Ч": {
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
    "M2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True,
    },

    "H1": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True,
    },
    "H2": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "H3": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "H4": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },

    "M6": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 1,
        "colors": ["grey", "white"],
        "single": True
    },
    "M8": {
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
    "ALB_Sect1-2": {
        "mount": "top",
        "pack_side": "left",
        "count": 1,
        "colors": ["grey", "white"],
    },
    "ALB_Sect1-2_2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 1,
        "colors": ["grey", "white"],
    },
    "ALB_Sect2": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["red", "white"],
    }
}




signals_config = {
    "Ч1": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["red", "green", "white", "yellow"],
    },
    "Ч2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["red", "green", "white", "yellow"],
    },
    "Ч3": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["red", "green", "white", "yellow"],
    },
    "Ч4": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["red", "green", "white", "yellow"],
    },
    "Ч5": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 4,
        "colors": ["red", "green", "white", "yellow"],
    },
    "M7": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["blue", "white"],
        "type": "maneuver"
    },
    "M5": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["blue", "white"],
        "type": "maneuver"
    },
    "M3": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["blue", "white"],
        "type": "maneuver"
    },
    "M1": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["blue", "white"],
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
    }
}
ROUTE_SIGNAL_MAP: dict[tuple[str, str], dict[str, dict[str, object]]] = {
    ("M1", "M8"): {
        "M1": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M1", "H1"): {
        "M1": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M1", "M10"): {
        "M1": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M1", "M2"): {
        "M1": {"lamps": {"white": {"on": True, "blink": False}, }, },
        "H1": { "lamps": { "green": {"on": True, "blink": False},} },
    },
    ("M2", "H3"): {
        "M2": { "lamps": { "white": {"on": True, "blink": False}, } },
    },
    ("M2", "M10"): {
        "M2": {"lamps": { "white": {"on": True, "blink": False},} },
    },
    ("M2", "H1"):{
        "M2": {"lamps": { "white": {"on": True, "blink": False}, } },
    },
    ("M2", "M8"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }}, },
    ("M2", "M1"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
        "M8": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M2", "H2"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M2", "H1"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }},
    },
    ("M2", "H4"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }},
    },
    ("H4", "M2"): {
        "H4": {"lamps": { "green": {"on": False, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("M2", "2"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }},
    },
    ("M2", "4"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }},
    },
    ("M2", "1"): {
        "M2": {"lamps": {"white": {"on": True, "blink": False}, }},
    },
    ("M6", "H2"): {
        "M6": {"lamps": {"white": {"on": True, "blink": False},} },},
    ("M6", "H4"): {
        "M6": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M8", "M1"): {
        "M8": { "lamps": { "white": {"on": True, "blink": False}, "red": {"on": False, "blink": False},} },
    },

    ("M10", "M1"): {
        "M10": {"lamps": {"white": {"on": True, "blink": False}, "red": {"on": False, "blink": False}, }}, },
    ("M1", "H3"): {
        "M1": {"lamps": {"white": {"on": True, "blink": False}, "red": {"on": False, "blink": False}, }}, },

    ("H1", "M2"): {
        "H1": {"lamps": {"green": {"on": True, "blink": False}, }, },
    },
    ("H2", "M2"):{
        "H2": {"lamps": { "green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H2", "M6"):{
        "H2": {"lamps": { "green": {"on": True, "blink": False} }, },
    },
    ("H4", "M6"):{
        "H4": {"lamps": { "green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H3", "M2"): {
        "H3": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H3", "M10"): {
        "M10": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("M6", "4"): {
        "M6": {"lamps": {"white": {"on": True, "blink": False} }, },
    },

    ("Ч", "1"): {
        "Ч": {"lamps": {"yellow1": {"on": True, "blink": False}, } },
        #"M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("Ч", "2"): {
        "Ч": {"lamps": {"yellow": {"on": True, "blink": False}, "yellow1": {"on": True, "blink": False}, } },
       # "M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("Ч", "3"): {
        "Ч": {"lamps": {"yellow": {"on": True, "blink": False}, "yellow1": {"on": True, "blink": False}, }   },
        #"M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("Ч", "4"): {
        "Ч": {"lamps": {"yellow": {"on": True, "blink": False}, "yellow1": {"on": True, "blink": False}, }},
       # "M2": {"lamps": {"white": {"on": True, "blink": False}, }, },
    },
    ("Ч", "M1"):{
        "Ч": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H3", "Ч"):{
        "H3": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H1", "Ч"): {
        "H1": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H2", "Ч"): {
        "H2": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
    },
    ("H4", "Ч"): {
        "H4": {"lamps": {"green": {"on": True, "blink": False}, "yellow": {"on": True, "blink": False}, }, },
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
    # МАНЕВРОВЫЕ
    ("M2", "H3"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "diag", "name": "ALB_Turn2"},
    ],
    ("M2", "H1"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2H1_third", "H1")},
    ],
    ("M2", "M8"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2H1_third", "H1")},
        {"type": "segment", "id": ("H1", "M8")},
    ],
    ("M2", "M1"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2H1_third", "H1")},
        {"type": "segment", "id": ("H1", "M8")},
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M2", "M10"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "diag", "name": "ALB_Turn2"},
        {"type": "segment", "id": ("H3", "M10")},
    ],
    ("M2", "H2"): [
        {"type": "segment", "id": ("M2","M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "segment", "id": ("H2", "M6H2")},
    ],
    ("M2", "H4"): [
        {"type": "segment", "id": ("M2","M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "diag", "name": "ALB_Turn8"},

    ],
    ("M2", "1"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("H1", "M2H1_third")},
        {"type": "segment", "id": ("H1", "M8")},
    ],
    ("M2", "2"): [
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "segment", "id": ("H2", "past2")},
    ],
    ("M2", "4"): [
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2", "M2H1_mid")},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "diag", "name": "ALB_Turn8"},
        {"type": "segment", "id": ("M8", "M1")},
        {"type": "segment", "id": ("past4", "H4")},
    ],
    ("H2", "M6"): [
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "segment", "id": ("M6H2", "M6")},
        {"type": "segment", "id": ("M6", "beforeM6")},
    ],
    ("H2", "M2"): [
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2","M2H1_mid")}
    ],
    ("H4", "M6"): [
        {"type": "diag", "name": "ALB_Turn8"},
        {"type": "segment", "id": ("M6H2", "M6")},
        {"type": "segment", "id": ("M6", "beforeM6")},
    ],
    ("H4", "M2"): [
        {"type": "diag", "name": "ALB_Turn8"},
        {"type": "diag", "name": "ALB_Turn4"},
        {"type": "diag", "name": "ALB_Turn6"},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2", "M2H1_mid")},
    ],
    ("M6", "H4"):[
        {"type": "segment", "id": ("M6H2", "M6")},
        {"type": "diag", "name": "ALB_Turn8"},
    ],
    ("M6", "H2"):[
        {"type": "segment", "id": ("M6H2", "M6")},
        {"type": "segment", "id": ("M6H2", "H2")},
    ],
    ("M6", "4"): [
        {"type": "segment", "id": ("M6H2", "M6")},
        {"type": "diag", "name": "ALB_Turn8"},
        {"type": "segment", "id": ("past4", "H4")},
    ],
    # ("H3", "M10"): [
    #     {"type": "segment", "id": ("H3", "M10")},
    #     {"type": "diag", "name": "ALB_Turn1"},
    #
    # ],
    ("H1", "M2"): [
        {"type": "segment", "id": ("M2H1_third", "H1")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2", "M2H1_mid")},
    ],
    #
    # ("H3", "M1"): [
    #     {"type": "segment", "id": ("H3", "M10")},
    #     {"type": "diag", "name": "ALB_Turn1"},
    #     {"type": "segment", "id": ("M8", "M1")},
    #     {"type": "segment", "id": ("M8mid", "M1")},
    #     {"type": "segment", "id": ("M1", "pastM1")},
    # ],
    ("M10", "M1"): [
        {"type": "diag", "name": "ALB_Turn1"},
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M1", "M2"): [
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "segment", "id": ("M8", "H1")},
        {"type": "segment", "id": ("M2H1_third", "H1")},
        {"type": "segment", "id": ("M2H1_mid", "M2H1_third")},
        {"type": "segment", "id": ("M2", "M2H1_mid")},
    ],
    ("M1", "M8"): [
        {"type": "segment", "id": ("M1", "pastM1")},
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M8mid", "M8")},
    ],
    ("M1", "H3"): [
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "diag", "name": "ALB_Turn1"},
        {"type": "segment", "id": ("H3", "M10")},
    ],
    ("M8", "M1"): [
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M1", "H1"): [
        {"type": "segment", "id": ("M1", "pastM1")},
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "segment", "id": ("M8", "H1")},
    ],
    ("M1", "M10"): [
        {"type": "segment", "id": ("M8mid", "M1")},
        {"type": "segment", "id": ("M8mid", "M8")},
        {"type": "diag", "name": "ALB_Turn1"},
    ],
    ("H3", "M2"): [
        {"type": "diag", "name": "ALB_Turn2"},
        {"type": "segment", "id": ("M2", "M2H1_mid")},
    ]
}


route_switch_modes = {
    ("H2", "M6"): {"ALB_Turn8":  "left","ALB_Turn4-6":  "left"},
    ("H4", "M6"): {"ALB_Turn8":  "right","ALB_Turn4-6":  "left"},
    ("M2", "H3"): {"ALB_Turn2": "right"},
    ("M2", "M10"): {"ALB_Turn2": "right"},
    ("H3", "M1"): {"ALB_Turn1": "right"},
    ("H3","M10"):{},
    ("M10", "M1"): {"ALB_Turn1": "right"},
    ("M2", "H1"): {"ALB_Turn2": "left","ALB_Turn4-6":  "left"},
    ("M2", "M8"): {"ALB_Turn2": "left", "ALB_Turn4-6":  "left"},
    ("M2", "M1"): {"ALB_Turn1": "left","ALB_Turn2": "left","ALB_Turn4-6":  "left"},
    ("M2", "1"):  {"ALB_Turn4-6": "left", "ALB_Turn2": "left"},
    ("M2", "2"): {"ALB_Turn2": "left", "ALB_Turn4-6": "right", "ALB_Turn8": "left"},
    ("M2", "4"): {"ALB_Turn2": "left","ALB_Turn4-6": "right", "ALB_Turn8": "right"},
    ("M1", "M2"): {"ALB_Turn1": "left", "ALB_Turn2": "left", "ALB_Turn4-6": "left"},
    ("M1", "M8"): {"ALB_Turn1": "left"},
    ("M1", "H1"): {"ALB_Turn1": "left"},
    ("M2", "H2"): {"ALB_Turn4-6": "right", "ALB_Turn8":  "left", "ALB_Turn2": "left"},
    ("H1", "M8"): {},
    ("Ч", "4"): {"ALB_Turn2": "left","ALB_Turn4-6": "right", "ALB_Turn8": "right"},
    ("Ч", "3"): {"ALB_Turn2": "right"},
    ("Ч", "2"): {"ALB_Turn2": "left", "ALB_Turn4-6": "right", "ALB_Turn8": "left"},
    ("Ч", "1"): {"ALB_Turn4-6": "left", "ALB_Turn2": "left"},
    ("Ч", "M1"): {"ALB_Turn4-6": "left", "ALB_Turn2": "left", "ALB_Turn1": "left"},
    ("M2", "H4"): {"ALB_Turn2": "left", "ALB_Turn4-6": "right", "ALB_Turn8": "right"},
    ("H2", "M2"): {"ALB_Turn8": "left", "ALB_Turn4-6": "right", "ALB_Turn2": "left"},
    ("M6", "4"): {"ALB_Turn4-6": "left", "ALB_Turn8": "right"},
    ("H3", "Ч"): {"ALB_Turn2": "right"},
    ("H1", "Ч"): {"ALB_Turn2": "left", "ALB_Turn4-6": "left"},
    ("H2", "Ч"): {"ALB_Turn4-6": "right", "ALB_Turn2": "left",},
    ("H4", "Ч"): {"ALB_Turn4-6": "right", "ALB_Turn2": "left", "ALB_Turn8": "right"},

}
