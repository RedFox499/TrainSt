import tkinter as tk
import serial
import time

# --- НАСТРОЙКИ СВЯЗИ ---
SERIAL_PORT = 'COM6'  # Проверь порт!
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Подключено к {SERIAL_PORT}")
    CHIP_CONNECTED = True
except Exception as e:
    print(f"Ошибка подключения: {e}. Работа в ДЕМО-режиме.")
    CHIP_CONNECTED = False


def send_command(channel, position):
    command = f"W{channel} {position}\n"
    if CHIP_CONNECTED:
        try:
            ser.write(command.encode('utf-8'))
            print(f"Отправлено: {command.strip()}")
        except Exception as e:
            print(f"Ошибка записи: {e}")
    else:
        print(f"[ДЕМО] Команда: {command.strip()}")

    # Красим кнопки
    if position == 1:
        buttons[channel]['plus'].config(bg='#2ecc71', fg='white')
        buttons[channel]['minus'].config(bg='SystemButtonFace', fg='black')
    elif position == 2:
        buttons[channel]['plus'].config(bg='SystemButtonFace', fg='black')
        buttons[channel]['minus'].config(bg='#e74c3c', fg='white')
    elif position == 3:
        buttons[channel]['plus'].config(bg='SystemButtonFace', fg='black')
        buttons[channel]['minus'].config(bg='SystemButtonFace', fg='black')


def trigger_express_test():
    """Отправляет команду 'T' для быстрого поочередного теста всех 16 серв"""
    print("Запуск экспресс-теста всех 16 каналов платы...")
    if CHIP_CONNECTED:
        try:
            ser.write(b"T\n")
        except Exception as e:
            print(f"Ошибка связи при тесте: {e}")
    else:
        print("[ДЕМО] Отправлена команда T (Экспресс-тест 16 каналов)")

    for ch in channels:
        buttons[ch]['plus'].config(bg='SystemButtonFace', fg='black')
        buttons[ch]['minus'].config(bg='SystemButtonFace', fg='black')


def toggle_test_mode(channel):
    if test_states[channel]['running']:
        test_states[channel]['running'] = False
        buttons[channel]['test'].config(bg='SystemButtonFace', fg='black', text="🔄 ТЕСТ")
    else:
        test_states[channel]['running'] = True
        buttons[channel]['test'].config(bg='#f39c12', fg='white', text="🛑 СТОП", activebackground='#d35400')
        run_test_cycle(channel, 1)


def run_test_cycle(channel, next_position):
    if not test_states[channel]['running']:
        return
    send_command(channel, next_position)
    flipped_position = 2 if next_position == 1 else 1
    root.after(1000, lambda: run_test_cycle(channel, flipped_position))


def align_all_to_neutral():
    print("Ручной сброс всех 16 стрелок в нейтраль...")
    for ch in channels:
        if test_states[ch]['running']:
            toggle_test_mode(ch)
        send_command(ch, 3)
        time.sleep(0.04)


# --- ИНТЕРФЕЙС ТКINTER ---
root = tk.Tk()
root.title("Пульт АКЖТ: Максимальная панель 16 каналов (0-15)")
root.geometry("580x710")  # Слегка увеличили высоту под 16 строк
root.configure(bg='#f5f6fa')

buttons = {}
test_states = {}
channels = list(range(16))  # Авто-генерация списка от 0 до 15

title_label = tk.Label(
    root, text="СТАНЦИЯ: ПОЛНАЯ КОНФИГУРАЦИЯ ШИЛДА (16 СТРЕЛОК)",
    font=("Arial", 11, "bold"), bg='#f5f6fa', fg='#2c3e50'
)
title_label.pack(pady=6)

btn_express = tk.Button(
    root, text="⚡ ЗАПУСТИТЬ ПОЛНЫЙ ТЕСТ ПЛАТЫ (ПРОГОН СТРЕЛОК 0-15)", font=("Arial", 10, "bold"),
    bg='#9b59b6', fg='white', activebackground='#8e44ad', bd=3, relief="raised",
    command=trigger_express_test
)
btn_express.pack(pady=4, fill="x", padx=50)

grid_frame = tk.Frame(root, bg='#f5f6fa')
grid_frame.pack(pady=2)

for index, ch in enumerate(channels):
    test_states[ch] = {'running': False}

    lbl = tk.Label(
        grid_frame, text=f"Стрелка {ch:02d}:", font=("Arial", 10, "bold"),
        bg='#f5f6fa', fg='#34495e'
    )
    lbl.grid(row=index, column=0, padx=15, pady=2, sticky="w")

    btn_plus = tk.Button(
        grid_frame, text="ПЛЮС", font=("Arial", 8, "bold"), width=12, bd=2, relief="groove",
        command=lambda c=ch: send_command(c, 1)
    )
    btn_plus.grid(row=index, column=1, padx=4, pady=2)

    btn_minus = tk.Button(
        grid_frame, text="МИНУС", font=("Arial", 8, "bold"), width=12, bd=2, relief="groove",
        command=lambda c=ch: send_command(c, 2)
    )
    btn_minus.grid(row=index, column=2, padx=4, pady=2)

    btn_test = tk.Button(
        grid_frame, text="🔄 ТЕСТ", font=("Arial", 8, "bold"), width=12, bd=2, relief="raised",
        command=lambda c=ch: toggle_test_mode(c)
    )
    btn_test.grid(row=index, column=3, padx=10, pady=2)

    buttons[ch] = {'plus': btn_plus, 'minus': btn_minus, 'test': btn_test}

btn_reset = tk.Button(
    root, text="⚙️ ВЫСТАВИТЬ ВСЕ 16 СТРЕЛОК В НЕЙТРАЛЬ", font=("Arial", 10, "bold"),
    bg='#3498db', fg='white', activebackground='#2980b9', bd=3, relief="raised",
    command=align_all_to_neutral
)
btn_reset.pack(pady=10, fill="x", padx=50)

def on_closing():
    for ch in channels:
        test_states[ch]['running'] = False
    if CHIP_CONNECTED:
        ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()