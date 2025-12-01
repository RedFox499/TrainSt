import tkinter as tk
import time
root = tk.Tk()
canvas = tk.Canvas(root, width=1150, height=600, bg="white")
canvas.pack()

#########################################        ФУНКЦИЯ ТУПИКОВ                ##############################################
def drawDeadEnd(name, direction, offset):
    x = positions[name][0]
    y = positions[name][1]
    direction = direction
    if direction == "right":
        canvas.create_line(x, y, x + offset, y, width=4, fill="black")
        canvas.create_line(x + offset, y - 15, x + offset, y + 15, width=6)
    elif direction == "left":
        canvas.create_line(x, y, x - offset, y, width=4, fill="black")
        canvas.create_line(x - offset, y - 15, x - offset, y + 15, width=6, fill="black")


#{'M2H3': [11, 12, 13], 'M1M10': [14, 15, 16], 'H42': [17, 18, 19], '2T1': [20, 21, 22]}
#
#
#
#
#
#
#
#
#
#########################################        ПОЗИЦИОНИРОВАНИЕ                ##############################################

positions = {
    "M1": (1000, 330),
    "M8": (850, 330),
    "H1": (500, 330),
    "1STR": (380, 330),
    "M2": (150, 330),
    "M6H2": (445,230),
    "M10": (850, 430),
    "H3": (390, 430),

    "M6": (300, 230),
    "H2": (620, 230),

    "1": (760, 330),
    "2": (760, 230),
    "3": (760, 430),
    "4": (760, 130),

    "H4": (620, 130),
    "past4":  (970, 130),
    "CH": (80, 330),
    "past2": (970, 230),
    "pastM1": (1090,330),
    "beforeM6": (260, 230),
}

segments = [
    ("M1", "pastM1"),
    ("M1", "M8"),
    ("M8", "H1"),
    ("H1", "M2"),
    ("M2", "CH"),

    ("past2", "H2"),
    ("H2", "M6H2"),
    ("M6H2", "M6"),

    ("M10", "H3"),

    ("past4", "H4"),

    ("M6", "beforeM6"),

]
#########################################        МАССИВЫ ЭЛЕМЕНТОВ               ##############################################
selected_nodes = []
MAX_SELECTED = 2
node_ids = {}
segment_ids = {}
diag_ids = {}
diagonal_config = {
    "M1M10": {
        "left":  {"exists": True,  "connected": 0,  "disconnected": 0},
        "right": {"exists": True,  "connected": -5,  "disconnected": +5},
        "default": "both"
    },
    "M2H3": {
        "left":  {"exists": True,  "connected": 0,  "disconnected": 0},
        "right": {"exists": True,  "connected": -5,  "disconnected": +5},
        "default": "both"
    },

    "H42": {
        "left":  {"exists": True,  "connected": -5,  "disconnected": +5},
        "right": {"exists": True,  "connected": 0,  "disconnected": 0},
        "default": "both"
    },

    "2T1": {
        "left":  {"exists": True,  "connected": -5,  "disconnected": +5},
        "right": {"exists": True, "connected": -5,  "disconnected": +5},
        "default": "both"
    }
}

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


#########################################        МАРШРУТЫ                ##############################################
routes = {
    #МАНЕВРОВЫЕ
    ("H2", "M6"): [
        {"type": "segment", "id": "(H2', 'M6H2)"},
        {"type": "segment", "id": "('M6H2', 'M6')"}
    ],
    ("H4", "M6"): [
        {"type": "diag", "name": "H42"},
        {"type": "segment", "id": "('M6H2', 'M6')"}
    ],
    ("M2", "H3"): [
        {"type": "segment", "id": "('M2', 'H1')"},
        {"type": "diag", "name": "M2H3"},
    ],
    ("M2", "H1"): [
        {"type": "segment", "id": "('M2', 'H1')"},
    ],
    ("M2", "M8"): [
        {"type": "segment", "id": "('M2', 'H1')"},
        {"type": "segment", "id": "('H1', 'M8')"},
    ],
    ("M2", "M1"): [
        {"type": "segment", "id": "('M2', 'H1')"},
        {"type": "segment", "id": "('H1', 'M8')"},
        {"type": "segment", "id": "('M8', 'M1')"},
    ],
    ("H3", "M10"): [
        {"type": "segment", "id": "('H3', 'M10')"},
    ],
    ("H3", "M1"): [
        {"type": "segment", "id": "('H3', 'M10')"},
        {"type": "diag", "name": "M1M10"},
        {"type": "segment", "id": "('M8', 'M1')"},
        {"type": "segment", "id": "('M1', 'pastM1')"},
    ],
    ("M2", "M10"): [
        {"type": "segment", "id": "('M2', 'H1')"},
        {"type": "diag", "name": "M2H3"},
        {"type": "segment", "id": "('H3', 'M10')"},
        {"two_way": True}
    ],
    ("M10", "M1"): [
        {"type": "diag", "name": "M1M10"},
        {"type": "segment", "id": "('M8', 'M1')"},
        {"type": "segment", "id": "('M1', 'pastM1')"},
    ],
    ("M1", "M8"): [
        {"type": "segment", "id": "('M1', 'pastM1')"},
        {"type": "segment", "id": "('M8', 'M1')"},
    ],
    ("M8", "M1"): [
        {"type": "segment", "id": "('M8', 'M1')"},
        {"type": "segment", "id": "('M1', 'pastM1')"},
    ],
    ("M1", "H1"): [
        {"type": "segment", "id": "('M1', 'pastM1')"},
        {"type": "segment", "id": "('M1', 'M8')"},
        {"type": "segment", "id": "('M8', 'H1')"},
    ],
}
#########################################       ОТРИСОВКА СВЕТОФОРОВ                ##############################################
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


    signal_ids[name] = ids

    # подпись
    #label_y = y + dy_sign * (stand_len + 10)
    #canvas.create_text(x, label_y, text=name)

#########################################        ФУНКЦИИ МАРШРУТОВ                ##############################################
def paint_diagonal(name, color):
    for l in range(len(diag_ids[(name)])):
        canvas.itemconfig(diag_ids[name][l], fill=color)
def paint_segment(name, color):
    canvas.itemconfig(segment_ids[name], fill=color)

def paint_route(start, end, color="yellow"):
    key = (start, end)
    if key not in routes:
        key = (end, start)
        if key not in routes:
            print("Маршрут не найден")
            return

    for step in routes[key]:
        if step["type"] == "segment":
            paint_segment(step["id"], color)

        elif step["type"] == "diag":
            paint_diagonal(step["name"], "yellow")

        else:
            print("Неизвестный тип:", step)

#########################################        ФУНКЦИИ ВКЛ/ОТКЛ СТРЕЛОК/ДИАГОНАЛЕЙ               ##############################################
def setBranchRight(nameDiag, offset):
    x1, y1, x2, y2 = canvas.coords(diag_ids[nameDiag][0])
    canvas.coords(diag_ids[nameDiag][0], x1, y1 + offset, x2, y2 + offset)
    x1, y1, x2, y2 = canvas.coords(diag_ids[nameDiag][2])
    canvas.coords(diag_ids[nameDiag][2], x1, y1 + offset, x2, y2)

def setBranchLeft(nameDiag, offset):
    x1, y1, x2, y2 = canvas.coords(diag_ids[nameDiag][1])
    canvas.coords(diag_ids[nameDiag][1], x1, y1 + offset, x2, y2 + offset)
    x1, y1, x2, y2 = canvas.coords(diag_ids[nameDiag][2])
    canvas.coords(diag_ids[nameDiag][2], x1, y1, x2, y2 + offset)

def apply_diagonal_mode(nameDiag, mode):
    """
    mode: "left", "right", "both", "none"
    - left  -> подключить left, отключить right (если exists)
    - right -> подключить right, отключить left (если exists)
    - both  -> подключить обе (если существуют)
    - none  -> отключить обе (если существуют)
    """
    cfg = diagonal_config.get(nameDiag)
    if cfg is None:
        print(f"No config for {nameDiag}")
        return
    # LEFT
    left_cfg = cfg["left"]
    if left_cfg["exists"]:
        if mode == "left" or mode == "both":
            # подключаем левую — используем значение connected
            setBranchLeft(nameDiag, left_cfg["connected"])
        else:
            # отключаем левую
            setBranchLeft(nameDiag, left_cfg["disconnected"])
    # если left не существует — ничего не делаем

    # RIGHT
    right_cfg = cfg["right"]
    if right_cfg["exists"]:
        if mode == "right" or mode == "both":
            setBranchRight(nameDiag, right_cfg["connected"])
        else:
            setBranchRight(nameDiag, right_cfg["disconnected"])

#########################################        СТРЕЛКИ/ДИАГОНАЛИ               ##############################################

def AddDiagonal(x1,y1, x2,y2, offsetleft, offsetright, nameDiag):
    l1 = canvas.create_line(x1, y1, x1 - offsetleft, y1, width=4, fill="black")
    l2 = canvas.create_line(x2, y2, x2 + offsetright, y2, width=4, fill="black")
    l3 = canvas.create_line(x1, y1, x2, y2, width=4, fill="black")
    diag_ids[(nameDiag)] = [l1, l2, l3]


def ChangeDir():
    pass

#########################################       ЛИНИИ              ##############################################
for a, b in segments:
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    seg = canvas.create_line(x1-5, y1, x2+5, y2, width=4, fill="black")
    segment_ids[(a, b)] = seg
    segment_ids[(b, a)] = seg

#########################################        ДИАГОНАЛИ/СТРЕЛКИ               ##############################################
AddDiagonal(260, 330, 350, 430, 20, 38, "M2H3")
AddDiagonal(965, 330, 890, 430, -22, -37, "M1M10")
AddDiagonal(560,130, 470, 230, -57, -20, "H42")
AddDiagonal(420,230, 350, 330, -20, -20, "2T1")


#########################################        ПОДСВЕТКА МАРШРУТОВ               ##############################################
def highlight_possible_targets(start):
    """
    start — имя выбранной точки.
    Подсвечивает зелёным возможные цели.
    Остальные — серым.
    """

    possible = set()

    for (a, b), data in routes.items():
        if a == start:
            possible.add(b)

        if data["two_way"] and b == start:
            possible.add(a)
    # 2. Обходим все точки
    for name, item_id in node_ids.items():

        # если это выбранная точка — оставляем цвет выделения
        if name == start:
            canvas.itemconfig(item_id, fill="yellow")
            continue

        # если точка достижима — зелёная
        if name in possible:
            canvas.itemconfig(item_id, fill="green")
            canvas.itemconfig(item_id, state="normal")  # кликабельная
        else:
            # недостижимая → серым + отключить клики
            canvas.itemconfig(item_id, fill="grey")
            canvas.itemconfig(item_id, state="disabled")

    # 3. Чтобы текст тоже реагировал, если надо
    # (если у текста такие же теги node_<name>, "node")
    for name in possible:
        canvas.itemconfig(f"node_{name}", state="normal")


def reset_node_selection():
    for name, item_id in node_ids.items():
        canvas.itemconfig(item_id, fill="black", state="normal")
    selected_nodes.clear()
def disable_all_except_selected():
    for name, item in node_ids.items():
        if name in selected_nodes:
            canvas.itemconfig(item, state="normal")     # 2 выбранные — оставляем кликабельными (если надо)
        else:
            canvas.itemconfig(item, fill = "grey", state="disabled")   # все остальные выключаем

#########################################        ФУНКЦИЯ НАЖАТИЕ ДВУХ ТОЧЕК               ##############################################
def get_node_name_from_event(event):
    items = canvas.find_withtag("current")
    if not items:
        return None

    item = items[0]
    tags = canvas.gettags(item)

    for t in tags:
        if t.startswith("node_"):
            return t.replace("node_", "")
    return None

def on_enter(event):
    name = get_node_name_from_event(event)
    if name is None:
        return

    if name not in selected_nodes:
        canvas.itemconfig(node_ids[name], fill="cyan")


def on_leave(event):
    name = get_node_name_from_event(event)
    if name is None:
        return

    if name not in selected_nodes:
        canvas.itemconfig(node_ids[name], fill="black")


def on_node_click(event):
    name = get_node_name_from_event(event)
    if name is None:
        return

    if name in selected_nodes:
        selected_nodes.remove(name)
        canvas.itemconfig(node_ids[name], fill="black")
        if len(selected_nodes) == 0:
            reset_node_selection()
        if len(selected_nodes) == 1:
            highlight_possible_targets(selected_nodes[0])
        return

    if len(selected_nodes) >= MAX_SELECTED:
        return

    selected_nodes.append(name)
    canvas.itemconfig(node_ids[name], fill="cyan")
    print(len(selected_nodes))

    if len(selected_nodes) == 1:
        highlight_possible_targets(name)


    if len(selected_nodes) == 2:
        first = selected_nodes[0]
        second = selected_nodes[1]
        disable_all_except_selected()

        on_two_nodes_selected(first, second)


#########################################        ФУНКЦИЯ ПРИ НАЖАТИИ ДВУХ КНОПОК (ПОСТРОЕНИЕ МАРШРУТА И Т.Д.)           ##############################################
def on_two_nodes_selected(a, b):
    print("Выбраны точки:", a, b)



    # Вставь сюда свою логику
#Подключить М1М10
#apply_diagonal_mode("M1M10", "right")
#Отключить М1М10
apply_diagonal_mode("M1M10", "left")


#Подключить дорогу М2H3
#apply_diagonal_mode("M2H3", "right")
#Отключить дорогу М2H3
apply_diagonal_mode("M2H3", "left")


#Отключить Н42
apply_diagonal_mode("H42", "left")
#Подключить Н42
#apply_diagonal_mode("H42", "right")


#Отключить 2Т1
apply_diagonal_mode("2T1", "left")
#Подключить Н42
#apply_diagonal_mode("2T1", "right")


#########################################        ТУПИКИ               ##############################################
drawDeadEnd("pastM1", "right", 0)
drawDeadEnd("past2", "right", 0)
drawDeadEnd("past4", "right", 0)
drawDeadEnd("beforeM6", "left", 0)

#########################################        СТАНЦИИ(КРУГИ)               ##############################################
bannedNames = [ "pastM1", "beforeM6", "past2", "1STR", "past4", "M6H2"]
for name, (x, y) in positions.items():
    if name in bannedNames:
        continue
    #node = canvas.create_line(x,y-13, x,y+13, width=4, fill="grey",tags=(f"node_{name}", "node"))
    node = canvas.create_text(x, y - 25, text=name, tags=(f"node_{name}", "node"))
    node_ids[name] = node

# РИСУЕМ ВСЕ СВЕТОФОРЫ
for name, cfg in signals_config.items():
    drawSignal(
        name,
        cfg["mount"],
        cfg["pack_side"],
        cfg["count"],
        cfg.get("colors")
    )
#paint_diagonal("M1M10")
print(segment_ids)

#print(diag_ids)
#(node_ids)
canvas.tag_bind("node", "<Button-1>", on_node_click)
canvas.tag_bind("node", "<Enter>", on_enter)
canvas.tag_bind("node", "<Leave>", on_leave)

for id in node_ids:
    canvas.itemconfig(node_ids[id], fill="black")
for id in segment_ids:
    canvas.itemconfig(segment_ids[id], fill="grey")
for id in segment_ids:
    paint_segment(id, "green")

for id in diag_ids:
   paint_diagonal(id, "lime")

root.mainloop()

