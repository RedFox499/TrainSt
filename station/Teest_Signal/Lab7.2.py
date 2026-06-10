import tkinter as tk
import serial
import time

# --- НАСТРОЙКИ ПОРТА ---
PORT = 'COM6'
BAUD = 9600

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print("Arduino на связи!")
except:
    print("ОШИБКА: Проверь COM-порт!")
    ser = None

root = tk.Tk()
root.title("Инженерный отладчик + Бит-монитор")
root.configure(bg="#1a1a1a")

# Состояния: 5 байт по 8 бит (1 = ВЫКЛ, 0 = ВКЛ для Active Low)
bits = [[1 for _ in range(8)] for _ in range(5)]


# --- Функция обновления текстового табло ---
def update_bit_display():
    display_text = ""
    for b_idx in range(5):
        # Инвертируем для монитора: если в битах 0 (ВКЛ), показываем "1"
        line = "".join(["1" if bits[b_idx][i] == 0 else "0" for i in range(8)])
        display_text += f"Байт {b_idx}:  {line}\n"

    monitor_label.config(text=display_text)


def send_to_arduino():
    if ser and ser.is_open:
        packet = [ord('L')]
        for b_idx in range(5):
            byte_val = 0
            for i in range(8):
                # Младший бит (i=0) идет в (1 << 0)
                if bits[b_idx][i]:
                    byte_val |= (1 << i)
            packet.append(byte_val)

        ser.write(bytes(packet))
        update_bit_display()  # Обновляем текст при каждой отправке
        print(f"Отправлено (Hex): {' '.join([format(b, '02X') for b in packet[1:]])}")


def toggle_bit(b_idx, bit_idx, btn):
    bits[b_idx][bit_idx] = 1 if bits[b_idx][bit_idx] == 0 else 0
    if bits[b_idx][bit_idx] == 0:
        btn.config(bg="#2ecc71", fg="black", text=f"BIT {bit_idx}\n[ON]")
    else:
        btn.config(bg="#34495e", fg="white", text=f"BIT {bit_idx}\n[off]")
    send_to_arduino()


# --- Интерфейс ---
for b in range(5):
    frame = tk.LabelFrame(root, text=f" РЕГИСТР {b + 1} (Байт {b}) ", bg="#2c3e50", fg="#ecf0f1")
    frame.pack(fill="x", padx=10, pady=5)
    for bit in range(7, -1, -1):
        btn = tk.Button(frame, text=f"BIT {bit}\n[off]", width=8, height=2, bg="#34495e", fg="white")
        # Используем default value для лямбды, чтобы сохранить b и bit
        btn.config(command=lambda b=b, bit=bit, btn=btn: toggle_bit(b, bit, btn))
        btn.pack(side="left", padx=2, pady=5)

# --- Бит-монитор (Текстовое табло) ---
monitor_frame = tk.Frame(root, bg="#000000", bd=2, relief="sunken")
monitor_frame.pack(fill="x", padx=10, pady=10)

monitor_label = tk.Label(
    monitor_frame,
    text="00000000\n00000000\n00000000\n00000000\n00000000",
    font=("Courier New", 16, "bold"),
    fg="#00FF00",  # Зеленый "хакерский" цвет
    bg="#000000",
    justify="left",
    padx=10,
    pady=10
)
monitor_label.pack()


def all_off():
    for b in range(5):
        for bit in range(8): bits[b][bit] = 1
    send_to_arduino()
    # Сброс визуализации кнопок (упрощенно)
    for frame in root.winfo_children():
        if isinstance(frame, tk.LabelFrame):
            for btn in frame.winfo_children():
                btn.config(bg="#34495e", fg="white")
                txt = btn.cget("text").split("\n")[0]
                btn.config(text=f"{txt}\n[off]")


tk.Button(root, text="ГАСИТЬ ВСЁ", command=all_off, bg="#e74c3c", fg="white", font="bold").pack(fill="x", padx=10,
                                                                                                pady=10)

update_bit_display()  # Показать начальное состояние
root.mainloop()