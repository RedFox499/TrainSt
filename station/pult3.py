import tkinter
import tkinter as tk
import time
from tkinter.messagebox import showinfo

root = tk.Tk()
canvas = tk.Canvas(root, width=1150, height=600, bg="white")
canvas.pack()


def showInfo(title, msg):
    showinfo(title=title, message=msg)
#########################################        ФУНКЦИЯ ТУПИКОВ                ##############################################
def drawDeadEnd(name, direction, offset):
    x = positions[name][0]
    y = positions[name][1]
    if direction == "right":
        canvas.create_line(x, y, x + offset, y, width=4, fill="black")
        canvas.create_line(x + offset, y - 15, x + offset, y + 15, width=6)
    elif direction == "left":
        canvas.create_line(x, y, x - offset, y, width=4, fill="black")
        canvas.create_line(x - offset, y - 15, x - offset, y + 15, width=6, fill="black")

#########################################        ПОЗИЦИОНИРОВАНИЕ                ##############################################
positions = {
    "M1": (1000, 330),
    "M8": (850, 330),
    "H1": (500, 330),
    "1STR": (380, 330),
    "M2": (150, 330),
    "M6H2": (445, 230),
    "M10": (850, 430),
    "H3": (390, 430),

    "M6": (300, 230),
    "H2": (620, 230),

    "1": (760, 330),
    "2": (760, 230),
    "3": (760, 430),
    "4": (760, 130),

    "H4": (620, 130),
    "past4": (970, 130),
    "CH": (80, 330),
    "past2": (970, 230),
    "pastM1": (1090, 330),
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
signal_ids = {}

active_routes = {}  # route_id -> {"start": a, "end": b, "segments": [...]}
route_counter = 1   # уникальные номера маршрутов

occupied_segments = set()
occupied_diagonals = set()
# текущее положение каждой диагонали: name -> "left"/"right"/"both"/"none"
diagonal_modes = {}

switch_indicator_ids = {}          # name -> id прямоугольника
switch_list = ["M1M10", "M2H3", "H42", "2T1"]

# нормальное (плюсовое) положение стрелок
default_switch_mode = {
    "M1M10": "left",
    "M2H3": "left",
    "H42":  "left",
    "2T1":  "left",
}

last_switch_check = {}

seg_occ_train = {
    ("M1", "pastM1"): 1,
    ("M1", "M8"): 1,
    ("M8", "H1"): 1,
    ("H1", "M2"): 1,
    ("M2", "CH"): 1,
    ("past2", "H2"): 1,
    ("H2", "M6H2"): 1,
    ("M6H2", "M6"): 1,
    ("M10", "H3"): 1,
    ("past4", "H4"): 1,
    ("M6", "beforeM6"): 1,
}
diag_occ_train = {
    "M1M10": 1,
    "M2H3": 1,
    "H42": 1,
    "2T1": 1,
}


#########################################        КОНФИГ ДИАГОНАЛЕЙ               ##############################################
diagonal_config = {
    "M1M10": {
        "left":  {"exists": True, "connected": 0,  "disconnected": 0},
        "right": {"exists": True, "connected": -5, "disconnected": +5},
        "default": "both"
    },
    "M2H3": {
        "left":  {"exists": True, "connected": 0,  "disconnected": 0},
        "right": {"exists": True, "connected": -5, "disconnected": +5},
        "default": "both"
    },

    "H42": {
        "left":  {"exists": True, "connected": -5, "disconnected": +5},
        "right": {"exists": True, "connected": 0,  "disconnected": 0},
        "default": "both"
    },

    "2T1": {
        "left":  {"exists": True, "connected": -5, "disconnected": +5},
        "right": {"exists": True, "connected": -5, "disconnected": +5},
        "default": "both"
    }
}

#########################################        КОНФИГ СВЕТОФОРОВ               ##############################################
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
        "colors": ["blue", "white"],
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
# ВАЖНО: id сегмента – кортеж, как в segment_ids
routes = {
    # МАНЕВРОВЫЕ
    ("H2", "M6"): [
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "segment", "id": ("M6H2", "M6")},
    ],
    ("H4", "M6"): [
        {"type": "diag", "name": "H42"},
        {"type": "segment", "id": ("M6H2", "M6")},
    ],
    ("M2", "H3"): [
        {"type": "segment", "id": ("M2", "H1")},
        {"type": "diag", "name": "M2H3"},
    ],
    ("M2", "H1"): [
        {"type": "segment", "id": ("M2", "H1")},
    ],
    ("M2", "M8"): [
        {"type": "segment", "id": ("M2", "H1")},
        {"type": "segment", "id": ("H1", "M8")},
    ],
    ("M2", "M1"): [
        {"type": "segment", "id": ("M2", "H1")},
        {"type": "segment", "id": ("H1", "M8")},
        {"type": "segment", "id": ("M8", "M1")},
    ],
    ("H3", "M10"): [
        {"type": "segment", "id": ("H3", "M10")},
    ],
    ("H3", "M1"): [
        {"type": "segment", "id": ("H3", "M10")},
        {"type": "diag", "name": "M1M10"},
        {"type": "segment", "id": ("M8", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M2", "M10"): [
        {"type": "segment", "id": ("M2", "H1")},
        {"type": "diag", "name": "M2H3"},
        {"type": "segment", "id": ("H3", "M10")},
    ],
    ("M10", "M1"): [
        {"type": "diag", "name": "M1M10"},
        {"type": "segment", "id": ("M8", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M1", "M8"): [
        {"type": "segment", "id": ("M1", "pastM1")},
        {"type": "segment", "id": ("M8", "M1")},
    ],
    ("M8", "M1"): [
        {"type": "segment", "id": ("M8", "M1")},
        {"type": "segment", "id": ("M1", "pastM1")},
    ],
    ("M1", "H1"): [
        {"type": "segment", "id": ("M1", "pastM1")},
        {"type": "segment", "id": ("M1", "M8")},
        {"type": "segment", "id": ("M8", "H1")},
    ],
    ("M2", "H2"): [
        {"type": "segment", "id": ("M2", "H1")},
        {"type": "diag", "name": "2T1"},
        {"type": "segment", "id": ("H2", "M6H2")},
        {"type": "segment", "id": ("M6", "M6H2")},
    ],
    ("H1", "M8"): [
        {"type": "segment", "id": ("H1", "M8")},
    ],
}

# какие положения стрелок нужны для маршрута (можно подправить под реальную схему)
route_switch_modes = {
    ("H2", "M6"): {
        "H42":  "left",
        "2T1":  "left",
    },
    ("H4", "M6"): {
        "H42":  "right",
        "2T1":  "left",
    },
    ("M2", "H3"): {
        "M2H3": "right",
    },
    ("M2", "M10"): {
        "M2H3": "right",
    },
    ("H3", "M1"): {
        "M1M10": "right",
    },
    ("H3","M10"):{},
    ("M10", "M1"): {
        "M1M10": "right",
    },
    ("M2", "H1"): {
        "M2H3": "left",
        "2T1":  "left",
    },
    ("M2", "M8"): {
        "M2H3": "left",
    },
    ("M2", "M1"): {
        "M1M10": "left",   # идём по прямому, стрелка на M1M10 не на бок
        "M2H3": "left",
        "2T1":  "left",
    },
    ("M1", "M8"): {
        "M1M10": "left",
    },
    ("M1", "H1"): {
        "M1M10": "left",
    },
    ("M2", "H2"): {
        "2T1": "right",
        "H42":  "left",
        "M1M10": "right",
    },
    ("H1", "M8"): {
    }
}




#########################################       ОТРИСОВКА СВЕТОФОРОВ                ##############################################
def drawSignal(name, mount="bottom", pack_side="right", count=3, colors=None):
    x, y = positions[name]

    r = 4
    gap = 2 * r + 2
    stand_len = 15
    bar_len = 10

    dy_sign = -1 if mount == "top" else 1
    sx, sy = x, y + dy_sign * stand_len

    canvas.create_line(x, y, sx, sy, width=2, fill="black")

    hx_sign = 1 if pack_side == "right" else -1

    hx0, hy0 = sx, sy
    hx1, hy1 = sx + hx_sign * bar_len, sy
    canvas.create_line(hx0, hy0, hx1, hy1, width=2, fill="black")

    ids = []
    start_cx = hx1 + hx_sign * (r + 1)

    for i in range(count):
        cx = start_cx + hx_sign * i * gap
        cy = sy

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

#########################################        ФУНКЦИИ МАРШРУТОВ                ##############################################
def paint_diagonal(name, color):
    for l in range(len(diag_ids[(name)])):
        canvas.itemconfig(diag_ids[name][l], fill=color)

def paint_segment(key, color):
    seg_id = segment_ids.get(key)
    if seg_id is None:
        return
    canvas.itemconfig(seg_id, fill=color)

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
            paint_diagonal(step["name"], color)
        else:
            print("Неизвестный тип шага:", step)

#########################################        ФУНКЦИИ ВКЛ/ОТКЛ СТРЕЛОК               ##############################################
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
    cfg = diagonal_config.get(nameDiag)
    if cfg is None:
        print(f"No config for {nameDiag}")
        return

    left_cfg = cfg["left"]
    if left_cfg["exists"]:
        if mode in ("left", "both"):
            setBranchLeft(nameDiag, left_cfg["connected"])
        else:
            setBranchLeft(nameDiag, left_cfg["disconnected"])

    right_cfg = cfg["right"]
    if right_cfg["exists"]:
        if mode in ("right", "both"):
            setBranchRight(nameDiag, right_cfg["connected"])
        else:
            setBranchRight(nameDiag, right_cfg["disconnected"])

def get_switch_state_color(name):
    mode = diagonal_modes.get(name)
    normal = default_switch_mode.get(name, "left")
    if mode is None:
        return "grey"
    if mode == normal:
        return "green"    # плюс, нормальное положение
    else:
        return "yellow"   # переведена

def update_switch_indicator(name):
    rect = switch_indicator_ids.get(name)
    if rect is None:
        return
    color = get_switch_state_color(name)
    canvas.itemconfig(rect, fill=color)

def set_diagonal_mode(nameDiag, mode):
    apply_diagonal_mode(nameDiag, mode)
    diagonal_modes[nameDiag] = mode
    update_switch_indicator(nameDiag)

#########################################  МИНИ-Таблица стрелок (правый нижний угол)  #########################################
def create_switch_table():
    w = int(canvas["width"])
    h = int(canvas["height"])

    dy = 25
    total_height = dy * len(switch_list)
    y_start = h - total_height - 20

    x_text = w - 220
    x_rect = w - 60

    for i, name in enumerate(switch_list, start=1):
        y = y_start + (i - 1) * dy
        canvas.create_text(x_text, y, text=f"{i}. {name}", anchor="w")
        rect = canvas.create_rectangle(
            x_rect - 8, y - 8, x_rect + 8, y + 8,
            outline="black", fill="grey"
        )
        switch_indicator_ids[name] = rect
        update_switch_indicator(name)

def blink_switches(diags, duration_ms=2000, interval_ms=200):
    if not diags:
        return

    end_time = time.time() + duration_ms / 1000.0
    final_colors = {d: get_switch_state_color(d) for d in diags}

    def _step(state=True):
        if time.time() >= end_time:
            for d in diags:
                rect = switch_indicator_ids.get(d)
                if rect is not None:
                    canvas.itemconfig(rect, fill=final_colors[d])
            return

        for d in diags:
            rect = switch_indicator_ids.get(d)
            if rect is not None:
                canvas.itemconfig(rect, fill="cyan" if state else final_colors[d])

        root.after(interval_ms, _step, not state)

    _step(True)
#########################################        СТРЕЛКИ/ДИАГОНАЛИ               ##############################################
def AddDiagonal(x1, y1, x2, y2, offsetleft, offsetright, nameDiag):
    l1 = canvas.create_line(x1, y1, x1 - offsetleft, y1, width=4, fill="black")
    l2 = canvas.create_line(x2, y2, x2 + offsetright, y2, width=4, fill="black")
    l3 = canvas.create_line(x1, y1, x2, y2, width=4, fill="black")
    diag_ids[(nameDiag)] = [l1, l2, l3]

#########################################       ЛИНИИ              ##############################################
for a, b in segments:
    x1, y1 = positions[a]
    x2, y2 = positions[b]
    seg = canvas.create_line(x1 - 5, y1, x2 + 5, y2, width=4, fill="black")
    segment_ids[(a, b)] = seg
    segment_ids[(b, a)] = seg

#########################################        ДИАГОНАЛИ/СТРЕЛКИ               ##############################################
AddDiagonal(260, 330, 350, 430, 20, 38, "M2H3")
AddDiagonal(965, 330, 890, 430, -22, -37, "M1M10")
AddDiagonal(560, 130, 470, 230, -57, -20, "H42")
AddDiagonal(420, 230, 350, 330, -20, -20, "2T1")

# начальное положение стрелок
set_diagonal_mode("M1M10", "left")
set_diagonal_mode("M2H3", "left")
set_diagonal_mode("H42", "left")
set_diagonal_mode("2T1", "left")

def check_if_route_finished(seg, rev):
    for rid in list(active_routes.keys()):
        data = active_routes[rid]
        segs = data["segments"]
        real_segs = [step["id"] for step in segs if step.get("type") == "segment"]
        last_seg = real_segs[-1]
        if seg == last_seg or rev == last_seg:
            release_route(rid)



def update_all_occupancy():

    # --- 1) сегменты ---
    for (a, b), seg_id in segment_ids.items():
        for seg in seg_occ_train:
            rev = (seg[1], seg[0])
            if seg_occ_train.get(seg, 1) == 0:
                occupied_segments.discard(seg)
                occupied_segments.discard(rev)
                check_if_route_finished(seg, rev)

        # 1) поезд занимает -> красный
        if seg_occ_train.get((a, b), 1) == 0 or seg_occ_train.get((b, a), 1) == 0 :
            paint_segment((a,b), "red")
            continue
        # 2) маршрут занимает -> жёлтый
        if (a, b) in occupied_segments or (b, a) in occupied_segments:
            paint_segment((a,b), "yellow")
            continue
        # 3) свободный -> чёрный
        paint_segment((a,b), "black")

    # --- 2) диагонали ---
    for diag_name, lines in diag_ids.items():
        # 1) поезд на диагонали -> красный
        if diag_occ_train.get(diag_name, 1) == 0:
            paint_diagonal(diag_name, "red")
            continue
        # 2) маршрут использует диагональ -> жёлтый
        if diag_name in occupied_diagonals:
            paint_diagonal(diag_name, "yellow")
            continue
        # 3) свободна -> чёрная
        paint_diagonal(diag_name, "black")
    root.after(1500, update_all_occupancy)

#########################################        ПОДСВЕТКА МАРШРУТОВ               ##############################################
def highlight_possible_targets(start):

    possible = set()

    for (a, b) in routes.keys():
        if a == start:
            possible.add(b)

    for name, item_id in node_ids.items():
        if name == start:
            canvas.itemconfig(item_id, fill="yellow")
            continue

        if name in possible:
            canvas.itemconfig(item_id, fill="green")
            canvas.itemconfig(item_id, state="normal")
        else:
            canvas.itemconfig(item_id, fill="grey")
            canvas.itemconfig(item_id, state="disabled")

    for name in possible:
        canvas.itemconfig(f"node_{name}", state="normal")

def reset_node_selection():
    for name, item_id in node_ids.items():
        canvas.itemconfig(item_id, fill="black", state="normal")
    selected_nodes.clear()

def disable_all_except_selected():
    for name, item in node_ids.items():
        if name in selected_nodes:
            canvas.itemconfig(item, state="normal")
        else:
            canvas.itemconfig(item, fill="grey", state="disabled")

#########################################        ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ УЗЛОВ      ##############################################
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

#########################################        КОНФЛИКТЫ МАРШРУТОВ ПОСТРОЕНИЕ НОВЫХ               ##############################################
def next_route_id():
    global route_counter
    rid = route_counter
    route_counter += 1
    return rid

def get_route(start, end):
    key = (start, end)
    if key in routes:
        return routes[key]
    return None

def check_route_conflict(start, end):
    for step in routes.get((start,end)):
        print(step)
        if step["type"] == "segment":
            a, b = step["id"]
            if step["id"] in occupied_segments or seg_occ_train.get((a, b), 1) == 0 or seg_occ_train.get((b, a), 1) == 0:
                return True
        elif step["type"] == "diag":
            print(diag_occ_train.get(step["type"],1))
            if step["name"] in occupied_diagonals or diag_occ_train.get(step["name"],1) == 0:
                return True
    return False

def register_route(start, end):
    global route_counter
    rid = route_counter
    route_counter += 1
    for step in routes.get((start,end)):
        if step["type"] == "segment":
            a, b = step["id"]
            occupied_segments.add((a,b))
            occupied_segments.add((b,a))
        elif step["type"] == "diag":
            occupied_diagonals.add(step["name"])

    active_routes[rid] = {
        "start": start,
        "end": end,
        "segments": routes.get((start,end)),
    }
    print(active_routes)
    return rid

def release_route(route_id):
    global route_counter
    if route_id not in active_routes:
        return
    data = active_routes[route_id]
    for step in data["segments"]:
        if step["type"] == "segment":
            a, b = step["id"]
            paint_segment((a,b), "black")
            occupied_segments.discard((a,b))
            occupied_segments.discard((b, a))
        elif step["type"] == "diag":
            paint_diagonal(step["name"], "black")
            occupied_diagonals.discard(step["name"])
    del active_routes[route_id]
    route_counter -= 1

#########################################        МИГАНИЕ МАРШРУТА               ##############################################
def blink_route(start, end, duration_ms=2000, interval_ms=200):

    end_time = time.time() + duration_ms / 1000.0

    def _step(state=True):
        if time.time() >= end_time:
            paint_route(start, end, "black")
            return

        color = "cyan" if state else "black"
        paint_route(start, end, color)
        root.after(interval_ms, _step, not state)

    _step(True)
#########################################        ОБРАБОТКА КЛИКА ПО УЗЛУ          ##############################################
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
    print("Выбрано узлов:", len(selected_nodes), "->", selected_nodes)

    if len(selected_nodes) == 1:
        highlight_possible_targets(name)

    if len(selected_nodes) == 2:
        first = selected_nodes[0]
        second = selected_nodes[1]
        disable_all_except_selected()
        on_two_nodes_selected(first, second)

#########################################        ФУНКЦИЯ ПРИ ВЫБОРЕ ДВУХ ТОЧЕК   ##############################################
def on_two_nodes_selected(a, b):
    global last_switch_check
    print("Выбраны точки маршрута:", a, "->", b)

    # 1. Проверка конфликтов по занятым сегментам/стрелкам
    if check_route_conflict(a, b):
        print("Маршрут конфликтует с уже установленными!")
        reset_node_selection()
        return

    # 2. Ищем настройки стрелок для этого маршрута
    key = (a, b)
    if key not in route_switch_modes:
        key = (b, a)

    if key not in route_switch_modes:
        print("Для этого маршрута нет настроек стрелок")
        reset_node_selection()
        return

    route_cfg = route_switch_modes[key]   # только нужные стрелки для ЭТОГО маршрута

    last_switch_check = {}
    changed = []
    main_diag = None  # какая стрелка будет мигать в табличке

    # 3. Применяем нужные положения стрелок (ТОЛЬКО из route_cfg)
    if not route_cfg:
        print("Для этого маршрута стрелки не задействованы.")
    else:
        for diag_name, need_mode in route_cfg.items():
            current_mode = diagonal_modes.get(diag_name)
            ok = (current_mode == need_mode)

            last_switch_check[diag_name] = {
                "needed": need_mode,
                "current": current_mode,
                "ok": ok,
            }

            if not ok:
                if main_diag is None:
                    main_diag = diag_name
                set_diagonal_mode(diag_name, need_mode)
                changed.append(f"{diag_name}: {current_mode} -> {need_mode}")

        if main_diag is None and route_cfg:
            main_diag = next(iter(route_cfg.keys()))

    print("Устанавливаем маршрут")
    paint_route(a, b, "cyan")
    blink_route(a, b, duration_ms=2000, interval_ms=200)

    if main_diag is not None:
        blink_switches([main_diag], duration_ms=2000, interval_ms=200)

    if changed:
        print("Изменены стрелки:")
        for line in changed:
            print("  ", line)
    else:
        if route_cfg:
            print("Стрелки уже стояли как нужно.")
        else:
            print("Маршрут без задействования стрелок.")

    reset_node_selection()

    def finalize():
        rid = register_route(a, b)
        paint_route(a, b, "yellow")
        print("Активные маршруты:", active_routes)

    root.after(2050, finalize)

def snos():
    for active in list(active_routes.keys()):
        release_route(active)

def check():
    check_if_route_finished()
#########################################        ТУПИКИ               ##############################################
drawDeadEnd("pastM1", "right", 0)
drawDeadEnd("past2", "right", 0)
drawDeadEnd("past4", "right", 0)
drawDeadEnd("beforeM6", "left", 0)

#########################################        СТАНЦИИ(КРУГИ/ТЕКСТ)             ##############################################
bannedNames = ["pastM1", "beforeM6", "past2", "1STR", "past4", "M6H2"]
for name, (x, y) in positions.items():
    if name in bannedNames:
        continue
    node = canvas.create_text(x, y - 25, text=name, tags=(f"node_{name}", "node"))
    node_ids[name] = node

#########################################        РИСУЕМ ВСЕ СВЕТОФОРЫ            ##############################################
for name, cfg in signals_config.items():
    drawSignal(
        name,
        cfg["mount"],
        cfg["pack_side"],
        cfg["count"],
        cfg.get("colors")
    )

#########################################        БИНДЫ И НАЧАЛЬНАЯ ОКРАСКА        ##############################################
canvas.tag_bind("node", "<Button-1>", on_node_click)
canvas.tag_bind("node", "<Enter>", on_enter)
canvas.tag_bind("node", "<Leave>", on_leave)
create_switch_table()

button = tkinter.Button(root, text="Снести", command=snos)
button.place(x=1, y=1)
button = tkinter.Button(root, text="Проверка", command=check)
button.place(x=50, y=1)

def do():
    if seg_occ_train[("H1", "M2")] == 0:
        seg_occ_train[("H1", "M2")] = 1
    else:
        seg_occ_train[("H1", "M2")] = 0
def do2():
    if seg_occ_train[("M8", "H1")] == 0:
        seg_occ_train[("M8", "H1")] = 1
    else:
        seg_occ_train[("M8", "H1")] = 0
button69 = tkinter.Button(root, text="prost", command=do)
button69.place(x=100, y=2)
button6969 = tkinter.Button(root, text="prost2", command=do2)
button6969.place(x=150, y=2)

update_all_occupancy()
root.mainloop()
