# ArduinoCode.py
from __future__ import annotations
from typing import Dict, Tuple, List, Any
from configs import SEGMENT_ORDER, segment_groups, segment_to_block

# ---------------------------------------------------------------------
# SERIAL handle
# ---------------------------------------------------------------------
ser = None  # Ожидается объект serial.Serial из основного скрипта

# ---------------------------------------------------------------------
# ЖЕЛЕЗНАЯ КАРТА СВЕТОФОРОВ
# Формат: ("Имя_Светофора", "Цвет"): (Индекс_Байта, Индекс_Бита)
# Индексы байтов: 0 (reg5), 1 (reg4), 2 (reg3), 3 (reg2), 4 (reg1)
# ---------------------------------------------------------------------
HW_MAP_40: Dict[Tuple[str, str], Tuple[int, int]] = {
    # Первый байт (reg5)
    ("H", "red"): (0, 0),  # Верхний
    ("H", "yellow"): (0, 1),
    ("H", "yellow1"): (0, 2),

    ("H_fake", "red"): (1, 5),

    ("Ч1", "red"): (0, 3),  # Нижний
    ("Ч1", "green"): (0, 4),
    ("Ч2", "red"): (0, 5),
    ("Ч2", "green"): (0, 6),
    ("Ч3", "red"): (0, 7),

    # Второй байт (reg4)
    ("Ч3", "green"): (1, 0),
    ("Ч4", "red"): (1, 1),
    ("Ч4", "green"): (1, 2),
    ("Ч5", "red"): (1, 3),
    ("Ч5", "green"): (1, 4),

}

# ---------------------------------------------------------------------
# ПРИЕМ ДАННЫХ ОТ ARDUINO (Переключение стрелок)
# ---------------------------------------------------------------------
# Карта соответствия имен в GUI и каналов сервоприводов (0-8) на плате PCA9685
# Убедись, что индексы соответствуют твоей раскладке!
SWITCH_HW_MAP = {
    "Перегон_03": 1,
    "AKZHT_Turn5-7": 4,
    "AKZHT_Turn1-3": 6,
    "AKZHT_Turn19": 7,
    "AKZHT_Turn13-15": 8,
}


def send_switch_command_to_hardware(switch_name: str, mode: str):
    global ser
    if ser is None or not ser.is_open:
        return

    if switch_name in SWITCH_HW_MAP:
        servo_id = SWITCH_HW_MAP[switch_name]
        pos_val = 1 if mode == "left" else 2

        try:
            # Если это спаренная стрелка, шлем команды для 4 и для 6 каналов
            if switch_name == "AKZHT_Turn1-3":
                command_str = f"W 6 {pos_val}\nW 3 {pos_val}\n"
            elif switch_name == "AKZHT_Turn5-7":
                command_str = f"W 4 {pos_val}\nW 5 {pos_val}\n"
            elif switch_name == "AKZHT_Turn13-15":
                command_str = f"W 8 {pos_val}\nW 15 {pos_val}\n"
            else:
                command_str = f"W {servo_id} {pos_val}\n"



            ser.write(command_str.encode('ascii'))
            print(f"[HW_SWITCH] Отправлено на макет для: {switch_name} -> {mode}")
        except Exception as e:
            print(f"[HW_SWITCH] Ошибка отправки: {e}")



# ---------------------------------------------------------------------
# ПРИЕМ ДАННЫХ ОТ ARDUINO (Датчики занятости)
# ---------------------------------------------------------------------
def parse_arduino_string(line, seg_occ_dict, diag_occ_dict):
    # Очищаем строку от префиксов, если они летят из Ардуино
    bin_str = line.replace("Data: ", "").strip()

    # Проверяем, что прилетел пакет именно из 3 датчиков
    if len(bin_str) != 3:
        return

    # Идем по 3 символам пакета
    for idx, char in enumerate(bin_str):
        if idx >= len(SEGMENT_ORDER):
            break

        seg = SEGMENT_ORDER[idx]
        if seg == "EMPTY":
            continue

        # 0 = Поезд на рельсах (Занят), 1 = Свободен
        is_occupied = (char == '0')

        if is_occupied:
            print(f"[Occupancy] Поезд на секции! Датчик №{idx} -> {seg}")

        # Если это стандартный сегмент-путь (кортеж нод)
        if isinstance(seg, tuple):
            block = segment_to_block.get(seg)
            # Если сегмент привязан к блоку, красим весь блок
            if block:
                for s in segment_groups[block]:
                    if s['type'] == "segment":
                        seg_occ_dict[s['id']] = 0 if is_occupied else 1
                    elif s["type"] == "diag":
                        diag_occ_dict[s['name']] = 0 if is_occupied else 1
            else:
                # Иначе красим только этот конкретный сегмент
                seg_occ_dict[seg] = 0 if is_occupied else 1

        # Если привязал к стрелке-диагонали (строка)
        elif isinstance(seg, str):
            diag_occ_dict[seg] = 0 if is_occupied else 1

# ---------------------------------------------------------------------
# ОТПРАВКА ДАННЫХ НА ARDUINO (Светофоры)
# ---------------------------------------------------------------------
def build_hw_frame(signals_state: Dict[str, Any], blink_phase: bool) -> List[int]:
    """Собирает 5 байт (40 бит). 1 = ВЫКЛ, 0 = ВКЛ (Active-Low)."""
    frame = [0xFF, 0xFF]

    for sig_name, st in signals_state.items():
        lamps = st.get("lamps", {})
        for lamp_name, cfg in lamps.items():
            if not cfg.get("on", False):
                continue

            if cfg.get("blink", False) and not blink_phase:
                continue

            pos = HW_MAP_40.get((sig_name, lamp_name))
            if pos:
                byte_idx, bit_idx = pos
                frame[byte_idx] &= ~(1 << bit_idx)

    return frame


def send_lights_to_arduino(frame: List[int]):
    """Запаковывает 5 байт в пакет 'L' и шлет в Serial."""
    if ser is None or not ser.is_open: return
    try:
        packet = bytearray([ord('L')]) + bytearray(frame)
        ser.write(packet)
        # Отладочный вывод для контроля
        #print(f"DEBUG [{time.strftime('%H:%M:%S')}]: {' '.join(f'{b:08b}' for b in frame)}")
    except Exception as e:
        print(f"[AC] Serial Error: {e}")



def all_off():
    """Гасит все светофоры (все биты в 1)."""
    send_lights_to_arduino([0xFF] * 2)