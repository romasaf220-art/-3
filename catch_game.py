import tkinter as tk
import random

class CatchGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Поймай Квадрат!")
        self.root.geometry("600x400")
        
        self.score = 0
        self.time_left = 30
        
        # Создаем холст
        self.canvas = tk.Canvas(self.root, bg="#222", width=600, height=350)
        self.canvas.pack()
        
        # Текст счета и времени
        self.info_label = tk.Label(self.root, text=f"Счет: 0 | Время: 30", font=("Arial", 16))
        self.info_label.pack(pady=5)
        
        # Создаем "цель" (красный квадрат)
        self.target = self.canvas.create_rectangle(0, 0, 30, 30, fill="red", outline="white")
        
        # Привязываем клик мыши
        self.canvas.bind("<Button-1>", self.click_target)
        
        self.move_target()
        self.timer()
        
        self.root.mainloop()

    def move_target(self):
        x = random.randint(20, 580)
        y = random.randint(20, 330)
        self.canvas.coords(self.target, x, y, x+30, y+30)

    def click_target(self, event):
        # Проверяем, попал ли клик по квадрату
        x, y = event.x, event.y
        coords = self.canvas.coords(self.target)
        if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
            self.score += 1
            self.info_label.config(text=f"Счет: {self.score} | Время: {self.time_left}")
            self.move_target()

    def timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.info_label.config(text=f"Счет: {self.score} | Время: {self.time_left}")
            self.root.after(1000, self.timer)
        else:
            self.canvas.create_text(300, 175, text="ВРЕМЯ ВЫШЛО!", fill="white", font=("Arial", 30))

if __name__ == "__main__":
    CatchGame()