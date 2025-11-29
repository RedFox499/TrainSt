import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=1150, height=600, bg="white")
canvas.pack()


def drawDeadEnd(name, direction, offset):
    x, y = positions[name]
    if direction == "right":
        canvas.create_line(x, y, x + offset, y, width=4, fill="black")
        canvas.create_line(x + offset, y - 15, x + offset, y + 15, width=6)
    elif direction == "left":
        canvas.create_line(x, y, x - offset, y, width=4, fill="black")
        canvas.create_line(x - offset, y - 15, x - offset, y + 15, width=6, fill="black")


positions = {
    "M1": (1000, 330),
    "M8": (850, 330),
    "H1": (500, 330),
    "M2": (150, 330),

    "M10": (850, 430),
    "H3": (390, 430),

    "M6": (300, 230),
    "H2": (620, 230),

    "H4": (620, 130),
    "4": (970, 130),

    "CH": (80, 330),

    "2": (970, 230),
    "pastM1": (1090, 330),
    "beforeM6": (260, 230),
}

segments = [
    ("M1", "M8"),
    ("M8", "H1"),
    ("H1", "M2"),
    ("M2", "CH"),

    ("M10", "H3"),

    ("H2", "M6"),

    ("H2", "2"),
    ("H4", "4"),
    ("M1", "pastM1"),
    ("M6", "beforeM6"),
]

node_ids = {}
segment_ids = {}
diag_ids = {}
signal_ids = {}

# =======================
#  КОНФИГ СВЕТОФОРОВ
#  mount:    'top' / 'bottom'  – стойка от пути вверх/вниз
#  pack_side:'left' / 'right'  – лампы слева/справа от стойки
#  count:    сколько ламп
#  colors:   список цветов по порядку ламп
#            (имена на английском: "white","yellow","red","green","blue")
# =======================
signals_config = {
    "CH": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 5,
        "colors": ["white", "yellow", "red", "green", "yellow"],
    },
    "M2": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["blue", "white"],        # пример
    },

    "H1": {
        "mount": "bottom",
        "pack_side": "left",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "H2": {
        "mount": "bottom",
        "pack_side": "left",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "H3": {
        "mount": "bottom",
        "pack_side": "left",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },
    "H4": {
        "mount": "top",
        "pack_side": "left",
        "count": 4,
        "colors": ["white", "red", "green", "yellow"],
    },

    "M6": {
        "mount": "top",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white"],
    },
    "M8": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white"],
    },
    "M10": {
        "mount": "bottom",
        "pack_side": "right",
        "count": 2,
        "colors": ["red", "white"],
    },
    "M1": {
        "mount": "top",
        "pack_side": "left",
        "count": 2,
        "colors": ["white", "red"],
    },
}


#def on_signal_click(name, index):
  #  print(f"Нажат светофор {name}, лампа {index}")


def drawSignal(name, mount="bottom", pack_side="right", count=3, colors=None):
    """
    Стойка от пути вверх/вниз + палка + лампы слева/справа.
    colors: список цветов для ламп (может быть None)
    """
    x, y = positions[name]

    r = 4              # радиус лампы
    gap = 2 * r + 2    # расстояние между лампами
    stand_len = 15     # длина стойки
    bar_len = 10       # длина палки от стойки до первой лампы

    # направление стойки (вверх/вниз от линии)
    dy_sign = -1 if mount == "top" else 1

    # точка конца стойки
    sx, sy = x, y + dy_sign * stand_len

    # вертикальная стойка
    canvas.create_line(x, y, sx, sy, width=2, fill="black")

    # направление, куда пойдут палка и лампы
    hx_sign = 1 if pack_side == "right" else -1

    # горизонтальная палка
    hx0, hy0 = sx, sy
    hx1, hy1 = sx + hx_sign * bar_len, sy
    canvas.create_line(hx0, hy0, hx1, hy1, width=2, fill="black")

    ids = []
    start_cx = hx1 + hx_sign * (r + 1)  # первая лампа после палки

    for i in range(count):
        cx = start_cx + hx_sign * i * gap
        cy = sy

        # цвет для текущей лампы
        fill_color = ""
        if colors is not None and i < len(colors):
            fill_color = colors[i]

        oid = canvas.create_oval(
            cx - r, cy - r,
            cx + r, cy + r,
            outline="black", width=1, fill=fill_color
        )
        ids.append(oid)
        canvas.tag_bind(oid, "<Button-1>",
                        lambda e, n=name, idx=i: on_signal_click(n, idx))

    signal_ids[name] = ids

    # подпись
    label_y = y + dy_sign * (stand_len + 10)
    canvas.create_text(x, label_y, text=name)


def AddDiagonal(x1, y1, x2, y2, offsetleft, offsetright, nameDiag):
    l1 = canvas.create_line(x1, y1, x1 - offsetleft, y1, width=4, fill="black")
    l2 = canvas.create_line(x2, y2, x2 + offsetright, y2, width=4, fill="black")
    l3 = canvas.create_line(x1, y1, x2, y2, width=4, fill="black")
    diag_ids[nameDiag] = [l1, l2, l3]


# ЛИНИИ ПУТЕЙ
for a, b in segments:
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    seg = canvas.create_line(x1 - 5, y1, x2 + 5, y2, width=4, fill="black")
    segment_ids[(a, b)] = seg
    segment_ids[(b, a)] = seg

# ДИАГОНАЛИ
AddDiagonal(260, 330, 350, 430, 20, 38, "M2H3")
AddDiagonal(965, 330, 890, 430, -22, -37, "M1M10")
AddDiagonal(560, 130, 470, 230, -57, -20, "H42")
AddDiagonal(420, 230, 310, 330, -20, -20, "2T1")

# ТУПИКИ
drawDeadEnd("pastM1", "right", 0)
drawDeadEnd("2", "right", 0)
drawDeadEnd("4", "right", 0)
drawDeadEnd("beforeM6", "left", 0)

# СТАНЦИИ (без светофоров)
for name, (x, y) in positions.items():
    if name in ("2", "4", "pastM1", "beforeM6"):
        continue
    if name in signals_config:
        continue  # тут рисуем светофор

    node = canvas.create_line(x, y - 13, x, y + 13, width=4, fill="grey")
    node_ids[name] = node
    canvas.create_text(x, y - 25, text=name)

# РИСУЕМ ВСЕ СВЕТОФОРЫ
for name, cfg in signals_config.items():
    drawSignal(
        name,
        cfg["mount"],
        cfg["pack_side"],
        cfg["count"],
        cfg.get("colors")
    )

root.mainloop()