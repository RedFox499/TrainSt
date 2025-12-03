import os
import sys
import tkinter as tk
import pygame

# ------------------ базовые настройки ------------------

WIDTH, HEIGHT = 1150, 600
BG_COLOR = (255, 255, 255)
TRACK_COLOR = (0, 0, 0)
NODE_COLOR = (120, 120, 120)
NODE_SELECTED_COLOR = (220, 0, 0)
TEXT_COLOR = (0, 0, 0)

# ------------------ Tkinter окно и рамка для Pygame ------------------

root = tk.Tk()
root.title("Tkinter + Pygame: ЖД схема")

embed = tk.Frame(root, width=WIDTH, height=HEIGHT, bg="black")
embed.pack(padx=10, pady=10)

info_label = tk.Label(root, text="Кликни начальную станцию", anchor="w")
info_label.pack(fill="x", padx=10, pady=5)

root.update_idletasks()
os.environ["SDL_WINDOWID"] = str(embed.winfo_id())
# при проблемах на Windows иногда нужно:
# os.environ["SDL_VIDEODRIVER"] = "windib"

# ------------------ инициализация Pygame ------------------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)

# ------------------ схема (те же координаты, что у тебя) ------------------

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
    "4":  (970, 130),

    "CH": (80, 330),

    "2": (970, 230),
    "pastM1": (1090, 330),
    "beforeM6": (260, 230),
}

# геометрия участков (линий), как было в Tkinter
segments_geom = [
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

# конфиг диагоналей (стрелочных соединений)
diagonal_config = {
    "M1M10": {
        "left":  {"exists": True,  "connected": 0,  "disconnected": 0},
        "right": {"exists": True,  "connected": -5, "disconnected": +5},
        "default": "both"
    },
    "M2H3": {
        "left":  {"exists": True,  "connected": 0,  "disconnected": 0},
        "right": {"exists": True,  "connected": -5, "disconnected": +5},
        "default": "both"
    },
    "H42": {
        "left":  {"exists": True,  "connected": -5, "disconnected": +5},
        "right": {"exists": True,  "connected": 0,  "disconnected": 0},
        "default": "both"
    },
    "2T1": {
        "left":  {"exists": True,  "connected": -5, "disconnected": +5},
        "right": {"exists": True,  "connected": -5, "disconnected": +5},
        "default": "both"
    }
}

# ------------------ состояния инфраструктуры ------------------


class SegmentState:
    """Участок пути между двумя узлами: занятость и блокировка маршрутом."""
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.occupied = False
        self.locked_by = None  # id маршрута, который держит этот участок


class SwitchState:
    """Стрелка (диагональ): режим и блокировка."""
    def __init__(self, name, default_mode):
        self.name = name
        self.mode = default_mode
        self.locked_by = None  # id маршрута


class Route:
    """
    Маршрут:
    - id, имя
    - начальный и конечный узел (для выбора мышкой)
    - segments: список участков (a, b) по порядку прохождения
    - diag_modes: для каких диагоналей какой режим (left/right/both/none)
    """
    def __init__(self, rid, name, start, end, segments, diag_modes=None):
        self.id = rid
        self.name = name
        self.start = start
        self.end = end
        self.segments = segments
        self.diag_modes = diag_modes or {}
        self.active = False


class Train:
    """
    Поезд едет по списку участков маршрута:
    - плавно от точки A к B;
    - занимает участок, когда вошёл на него;
    - освобождает, когда ушёл;
    - в конце освобождает маршрут.
    """
    def __init__(self, route, speed=0.4):
        self.route = route
        self.speed = speed      # "доля участка в секунду"
        self.index = 0          # номер текущего участка
        self.progress = 0.0     # 0..1 по текущему участку
        self.finished = False

        if self.route.segments:
            a, b = self.route.segments[0]
            key = tuple(sorted((a, b)))
            seg = segments_state.setdefault(key, SegmentState(a, b))
            seg.occupied = True

    def update(self, dt):
        if self.finished or not self.route.segments:
            return

        self.progress += self.speed * dt

        # если прошли участок – переходим на следующий
        while self.progress >= 1.0 and not self.finished:
            # освободить предыдущий участок
            a_prev, b_prev = self.route.segments[self.index]
            key_prev = tuple(sorted((a_prev, b_prev)))
            seg_prev = segments_state[key_prev]
            seg_prev.occupied = False

            self.index += 1
            self.progress -= 1.0

            # маршрут закончен
            if self.index >= len(self.route.segments):
                self.finished = True
                release_route(self.route)
                return

            # занять следующий участок
            a, b = self.route.segments[self.index]
            key = tuple(sorted((a, b)))
            seg = segments_state.setdefault(key, SegmentState(a, b))
            seg.occupied = True


# словарь участков (логика)
segments_state = {}
for a, b in segments_geom:
    key = tuple(sorted((a, b)))
    if key not in segments_state:
        segments_state[key] = SegmentState(a, b)

# стрелки (диагонали)
switches = {}
for name, cfg in diagonal_config.items():
    switches[name] = SwitchState(name, cfg["default"])

# диагонали для отрисовки
diag_data = {}


def add_diagonal(x1, y1, x2, y2, offsetleft, offsetright, nameDiag):
    """
    Аналог AddDiagonal из Tkinter, только сохраняем данные,
    а рисуем потом.
    """
    diag_data[nameDiag] = {
        "l1_base": (x1, y1, x1 - offsetleft, y1),
        "l2_base": (x2, y2, x2 + offsetright, y2),
        "l3_base": (x1, y1, x2, y2),
        "offset_left_branch": 0,
        "offset_right_branch": 0,
        "offset_start": 0,
        "offset_end": 0,
    }


def setBranchRight(nameDiag, offset):
    d = diag_data[nameDiag]
    d["offset_left_branch"] = offset
    d["offset_start"] = offset


def setBranchLeft(nameDiag, offset):
    d = diag_data[nameDiag]
    d["offset_right_branch"] = offset
    d["offset_end"] = offset


def apply_diagonal_mode(nameDiag, mode):
    cfg = diagonal_config.get(nameDiag)
    if cfg is None:
        return

    sw = switches[nameDiag]
    sw.mode = mode

    # левая ветка
    left_cfg = cfg["left"]
    if left_cfg["exists"]:
        if mode in ("left", "both"):
            setBranchLeft(nameDiag, left_cfg["connected"])
        else:
            setBranchLeft(nameDiag, left_cfg["disconnected"])

    # правая ветка
    right_cfg = cfg["right"]
    if right_cfg["exists"]:
        if mode in ("right", "both"):
            setBranchRight(nameDiag, right_cfg["connected"])
        else:
            setBranchRight(nameDiag, right_cfg["disconnected"])


# координаты диагоналей (как были в Tkinter)
add_diagonal(260, 330, 350, 430, 20, 38, "M2H3")
add_diagonal(965, 330, 890, 430, -22, -37, "M1M10")
add_diagonal(560, 130, 470, 230, -57, -20, "H42")
add_diagonal(420, 230, 310, 330, -20, -20, "2T1")

# ставим стрелки в дефолтное положение
for name, cfg in diagonal_config.items():
    apply_diagonal_mode(name, cfg["default"])

# ------------------ узлы (станции) для кликов ------------------

nodes = {}
node_selected = {}

for name, (x, y) in positions.items():
    if name in ("2", "4", "pastM1", "beforeM6"):
        continue  # тупики, по ним не кликаем
    nodes[name] = (x, y)
    node_selected[name] = False

# ------------------ отрисовка ------------------


def draw_segments():
    for a, b in segments_geom:
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        key = tuple(sorted((a, b)))
        seg = segments_state[key]
        if seg.occupied:
            color = (255, 0, 0)      # занят поездом
        elif seg.locked_by:
            color = (255, 255, 0)    # залочен маршрутом
        else:
            color = TRACK_COLOR
        pygame.draw.line(screen, color, (x1 - 5, y1), (x2 + 5, y2), 4)


def draw_diagonals():
    for name, d in diag_data.items():
        sw = switches[name]
        base_color = (0, 0, 0) if not sw.locked_by else (255, 255, 0)

        # левая ветка
        x1, y1, x2, y2 = d["l1_base"]
        y1o = y1 + d["offset_left_branch"]
        y2o = y2 + d["offset_left_branch"]
        pygame.draw.line(screen, base_color, (x1, y1o), (x2, y2o), 4)

        # правая ветка
        x1, y1, x2, y2 = d["l2_base"]
        y1o = y1 + d["offset_right_branch"]
        y2o = y2 + d["offset_right_branch"]
        pygame.draw.line(screen, base_color, (x1, y1o), (x2, y2o), 4)

        # диагональ
        x1, y1, x2, y2 = d["l3_base"]
        y1o = y1 + d["offset_start"]
        y2o = y2 + d["offset_end"]
        pygame.draw.line(screen, base_color, (x1, y1o), (x2, y2o), 4)


def draw_dead_ends():
    def de(name, direction, offset):
        x, y = positions[name]
        if direction == "right":
            pygame.draw.line(screen, TRACK_COLOR, (x, y), (x + offset, y), 4)
            pygame.draw.line(screen, TRACK_COLOR,
                             (x + offset, y - 15), (x + offset, y + 15), 6)
        else:
            pygame.draw.line(screen, TRACK_COLOR, (x, y), (x - offset, y), 4)
            pygame.draw.line(screen, TRACK_COLOR,
                             (x - offset, y - 15), (x - offset, y + 15), 6)

    de("pastM1", "right", 0)
    de("2", "right", 0)
    de("4", "right", 0)
    de("beforeM6", "left", 0)


def draw_nodes():
    for name, (x, y) in nodes.items():
        color = NODE_SELECTED_COLOR if node_selected[name] else NODE_COLOR
        pygame.draw.line(screen, color, (x, y - 13), (x, y + 13), 4)
        text_surface = font.render(name, True, TEXT_COLOR)
        rect = text_surface.get_rect(center=(x, y - 25))
        screen.blit(text_surface, rect)


def draw_trains():
    for tr in trains:
        if tr.finished or not tr.route.segments:
            continue
        idx = tr.index
        if idx >= len(tr.route.segments):
            continue
        a, b = tr.route.segments[idx]
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        t = tr.progress
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), 8)


def find_node_by_pos(mx, my, radius=12):
    for name, (x, y) in nodes.items():
        if abs(mx - x) <= radius and (y - 18) <= my <= (y + 18):
            return name
    return None

# ------------------ логика маршрутов и блокировок ------------------


def can_set_route(route):
    """Проверка: участки свободны, стрелки свободны, как на нормальной ЖД."""
    for a, b in route.segments:
        key = tuple(sorted((a, b)))
        seg = segments_state.setdefault(key, SegmentState(a, b))
        if seg.occupied:
            return False, f"Участок {a}-{b} занят поездом"
        if seg.locked_by and seg.locked_by != route.id:
            return False, f"Участок {a}-{b} уже в маршруте {seg.locked_by}"

    for dname in route.diag_modes.keys():
        sw = switches[dname]
        if sw.locked_by and sw.locked_by != route.id:
            return False, f"Стрелка {dname} занята маршрутом {sw.locked_by}"

    return True, "OK"


def set_route(route):
    """Установить маршрут: залочить участки и стрелки, перевести стрелки."""
    ok, msg = can_set_route(route)
    if not ok:
        return False, msg

    # блокируем участки
    for a, b in route.segments:
        key = tuple(sorted((a, b)))
        seg = segments_state.setdefault(key, SegmentState(a, b))
        seg.locked_by = route.id

    # блокируем стрелки и переводим в нужный режим
    for dname, mode in route.diag_modes.items():
        sw = switches[dname]
        sw.locked_by = route.id
        apply_diagonal_mode(dname, mode)

    route.active = True
    return True, "Маршрут установлен"


def release_route(route):
    """Снимем маршрут: освобождаем участки (если не заняты поездом) и стрелки."""
    for a, b in route.segments:
        key = tuple(sorted((a, b)))
        seg = segments_state.get(key)
        if seg and seg.locked_by == route.id and not seg.occupied:
            seg.locked_by = None

    for dname in route.diag_modes.keys():
        sw = switches[dname]
        if sw.locked_by == route.id:
            sw.locked_by = None
            # стрелку возвращаем в дефолтное положение
            apply_diagonal_mode(dname, diagonal_config[dname]["default"])

    route.active = False

# ------------------ описание маршрутов ------------------

routes = []
routes_by_nodes = {}

# 1) Главный путь CH -> pastM1: CH - M2 - H1 - M8 - M1 - pastM1
routes.append(Route(
    "R_CH_PASTM1",
    "Главный путь CH -> M1",
    "CH", "pastM1",
    [("CH", "M2"), ("M2", "H1"), ("H1", "M8"), ("M8", "M1"), ("M1", "pastM1")],
    diag_modes={}  # пока без стрелок
))

# 2) Обратный главный pastM1 -> CH
routes.append(Route(
    "R_PASTM1_CH",
    "Главный путь M1 -> CH",
    "M1", "CH",
    [("pastM1", "M1"), ("M1", "M8"), ("M8", "H1"), ("H1", "M2"), ("M2", "CH")],
    diag_modes={}
))

for r in routes:
    routes_by_nodes[(r.start, r.end)] = r

# ------------------ основной цикл Pygame внутри Tkinter ------------------

trains = []
selected_start = None
last_clicked = None
running = True


def game_loop():
    global running, last_clicked, selected_start

    if not running:
        return

    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            root.destroy()
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            name = find_node_by_pos(mx, my)
            if name is None:
                continue  # клик не по узлу

            # первый клик — выбираем начало маршрута
            if selected_start is None:
                selected_start = name
                for n in node_selected:
                    node_selected[n] = False
                node_selected[name] = True
                last_clicked = name
                info_label.config(
                    text=f"Начало маршрута: {name}. Теперь выбери конечную станцию."
                )
            else:
                # второй клик — конец маршрута
                start = selected_start
                end = name
                selected_start = None
                node_selected[name] = True
                last_clicked = name

                route = routes_by_nodes.get((start, end))
                if not route:
                    info_label.config(
                        text=f"Маршрут {start} -> {end} не описан."
                    )
                else:
                    ok, msg = set_route(route)
                    if not ok:
                        info_label.config(
                            text=f"Не могу установить маршрут {route.name}: {msg}"
                        )
                    else:
                        info_label.config(
                            text=f"{route.name} установлен, поезд отправлен."
                        )
                        trains.append(Train(route, speed=0.6))

    # обновляем поезда
    for tr in trains:
        tr.update(dt)

    # отрисовка
    screen.fill(BG_COLOR)
    draw_segments()
    draw_diagonals()
    draw_dead_ends()
    draw_nodes()
    draw_trains()

    info = f"Выделен узел: {last_clicked}" if last_clicked else "Маршрут не выбран"
    txt_surf = font.render(info, True, TEXT_COLOR)
    screen.blit(txt_surf, (10, HEIGHT - 25))

    pygame.display.flip()

    # планируем следующий кадр
    root.after(16, game_loop)


game_loop()
root.mainloop()
pygame.quit()
sys.exit()
