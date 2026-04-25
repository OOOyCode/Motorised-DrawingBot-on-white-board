import tkinter as tk

class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Menu")

        self.canvas = tk.Canvas(self.root, width=400, height=300)
        self.canvas.pack()

        self.selection = 0
        self.screen = "menu"

        self.mode_choice = None
        self.settings_choice = {
            "width": 5,
            "color": [255, 255, 255]
        }

        self.draw_menu()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("<Return>", self.validate)

        self.root.mainloop()

    def draw_menu(self):
        self.canvas.delete("all")

        color1 = "blue" if self.selection == 0 else "gray"
        color2 = "blue" if self.selection == 1 else "gray"

        self.canvas.create_rectangle(50, 50, 150, 150, fill=color1)
        self.canvas.create_text(100, 170, text="Mode Art")

        self.canvas.create_rectangle(250, 50, 350, 150, fill=color2)
        self.canvas.create_text(300, 170, text="Mode Trajectoire")

    def draw_settings(self):
        self.canvas.delete("all")

        labels = ["Width", "B", "G", "R", "START"]

        for i, label in enumerate(labels):
            y = 40 + i * 45
            selected = (self.selection == i)

            color = "blue" if selected else "gray"
            self.canvas.create_text(50, y, text=label, fill=color, anchor="w")

            if label != "START":
                value = (
                    self.settings_choice["width"]
                    if label == "Width"
                    else self.settings_choice["color"][i-1]
                )

                # barre
                self.canvas.create_rectangle(120, y-10, 320, y+10, outline="black")

                # remplissage
                fill_width = int((value / 255) * 200) if label != "Width" else int((value / 20) * 200)
                self.canvas.create_rectangle(120, y-10, 120 + fill_width, y+10, fill=color)

                # valeur
                self.canvas.create_text(340, y, text=str(value))

            else:
                self.canvas.create_rectangle(120, y-15, 320, y+15, fill=color)
                self.canvas.create_text(220, y, text="START")

        b, g, r = self.settings_choice["color"]
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.create_rectangle(150, 260, 250, 290, fill=hex_color)

    def move_up(self, event):
        if self.screen == "settings":
            self.selection = max(0, self.selection - 1)
            self.draw_settings()

    def move_down(self, event):
        if self.screen == "settings":
            self.selection = min(4, self.selection + 1)
            self.draw_settings()

    def move_left(self, event):
        if self.screen == "menu":
            self.selection = 0
            self.draw_menu()

        elif self.screen == "settings":
            self.adjust_value(-5)

    def move_right(self, event):
        if self.screen == "menu":
            self.selection = 1
            self.draw_menu()

        elif self.screen == "settings":
            self.adjust_value(5)

    def adjust_value(self, delta):
        if self.selection == 0:
            # width (0-20)
            self.settings_choice["width"] = max(1, min(20, self.settings_choice["width"] + delta//2))

        elif 1 <= self.selection <= 3:
            # RGB (0-255)
            i = self.selection - 1
            self.settings_choice["color"][i] = max(0, min(255, self.settings_choice["color"][i] + delta))

        self.draw_settings()

    def validate(self, event):
        if self.screen == "menu":
            if self.selection == 0:
                self.mode_choice = "Art"
                self.screen = "settings"
                self.selection = 0
                self.draw_settings()
            else:
                self.mode_choice = "Trajectoire"
                self.root.destroy()

        elif self.screen == "settings":
            if self.selection == 4:
                print("Lancement avec:", self.settings_choice)
                self.root.destroy()

    def get_mode(self):
        return self.mode_choice

    def get_settings(self):
        return self.settings_choice
