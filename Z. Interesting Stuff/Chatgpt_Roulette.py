import random
import tkinter as tk
from tkinter import messagebox

# ---------- Constants & Colors ----------

WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 800
BG_COLOR = "#042326"      # Dark teal
TABLE_COLOR = "#125b50"   # Table green
ACCENT_COLOR = "#f4c95d"  # Gold
TEXT_COLOR = "#f9f9f9"

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

# ---------- Pure Game Engine (no GUI) ----------

class RouletteEngine:
    def __init__(self):
        self.red_numbers = RED_NUMBERS

    def spin(self) -> int:
        """Return a random winning number between 0 and 36."""
        return random.randint(0, 36)

    def get_color(self, number: int) -> str:
        """Return 'red', 'black', or 'green'."""
        if number == 0:
            return "green"
        return "red" if number in self.red_numbers else "black"

    def evaluate_bets(self, bets: dict, winning_number: int) -> int:
        """
        Evaluate all bets and return total amount won (including stake).
        bets: dict[bet_target -> amount]
        """
        total_won = 0
        winning_color = self.get_color(winning_number)

        for bet_target, bet_amt in bets.items():
            # 1. Straight-up number bet (0–36)
            if bet_target.isdigit():
                if int(bet_target) == winning_number:
                    # 35:1 payout + original stake
                    total_won += bet_amt * 36

            # 2. Color bets
            elif bet_target == "red" and winning_color == "red":
                total_won += bet_amt * 2
            elif bet_target == "black" and winning_color == "black":
                total_won += bet_amt * 2

            # 3. Even / Odd (excluding zero)
            elif bet_target == "even" and winning_number != 0 and winning_number % 2 == 0:
                total_won += bet_amt * 2
            elif bet_target == "odd" and winning_number % 2 == 1:
                total_won += bet_amt * 2

            # 4. Low / High
            elif bet_target == "low" and 1 <= winning_number <= 18:
                total_won += bet_amt * 2
            elif bet_target == "high" and 19 <= winning_number <= 36:
                total_won += bet_amt * 2

        return total_won

# ---------- GUI Class ----------

class RouletteGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = RouletteEngine()

        # State
        self.balance = 1000
        self.current_bets = {}   # bet_target -> amount
        self.selected_chip_value = 10
        self.history = []        # list of strings
        self.num_buttons = {}    # "number" -> Button widget

        # Window
        self.root.title("Python Royal Roulette – Enhanced")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Layout
        self.build_layout()
        self.update_status()

    # ----- UI Construction -----

    def build_layout(self):
        # main grid: table (col 0) and side panel (col 1)
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        table_container = tk.Frame(self.root, bg=BG_COLOR)
        table_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        side_panel = tk.Frame(self.root, bg=BG_COLOR)
        side_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 20), pady=20)

        # ----- TABLE AREA -----
        border = tk.Frame(table_container, bg=ACCENT_COLOR, bd=3, relief="ridge")
        border.pack(fill="both", expand=True)

        table_frame = tk.Frame(border, bg=TABLE_COLOR, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        # Zero column
        zero_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        zero_frame.grid(row=0, column=0, rowspan=3, padx=(0, 10))

        self.create_number_button(
            zero_frame, "0", "green",
            width=6, height=8, font_size=16
        )

        # Grid 1–36
        nums_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        nums_frame.grid(row=0, column=1, rowspan=3)

        for n in range(1, 37):
            if n % 3 == 0:
                row = 0
            elif n % 3 == 2:
                row = 1
            else:
                row = 2
            col = (n - 1) // 3

            color = "red" if n in RED_NUMBERS else "black"
            self.create_number_button(nums_frame, str(n), color, row, col)

        # Outside bets row
        outside_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        outside_frame.grid(row=3, column=1, pady=(15, 0), sticky="we")

        outside_bets = [
            ("1-18", "low"),
            ("EVEN", "even"),
            ("RED", "red"),
            ("BLACK", "black"),
            ("ODD", "odd"),
            ("19-36", "high"),
        ]

        for i, (text, code) in enumerate(outside_bets):
            base_color = {
                "red": "#b22222",
                "black": "#000000"
            }.get(code, "#1f6f78")  # default teal

            btn = tk.Button(
                outside_frame,
                text=text,
                bg=base_color,
                fg="white",
                font=("Segoe UI", 11, "bold"),
                relief="raised",
                bd=3,
                width=12,
                height=2,
                command=lambda b=code: self.place_bet(b),
            )
            btn.grid(row=0, column=i, padx=2)

        # ----- SIDE PANEL -----

        # Balance + last result
        top_panel = tk.Frame(side_panel, bg=BG_COLOR)
        top_panel.pack(fill="x", pady=(0, 15))

        self.balance_label = tk.Label(
            top_panel,
            text="Balance: $0",
            font=("Consolas", 20, "bold"),
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
        )
        self.balance_label.pack(anchor="w")

        self.result_display = tk.Label(
            top_panel,
            text="PLACE YOUR BETS",
            font=("Segoe UI", 24, "bold"),
            fg=TEXT_COLOR,
            bg=BG_COLOR,
        )
        self.result_display.pack(anchor="w", pady=(10, 0))

        # Current bets summary
        bet_panel = tk.LabelFrame(
            side_panel,
            text="Current Bets",
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=("Segoe UI", 11, "bold"),
        )
        bet_panel.pack(fill="x", pady=(0, 15))

        self.bet_summary = tk.Label(
            bet_panel,
            text="No bets placed.",
            font=("Segoe UI", 10),
            fg="#d0d0d0",
            bg=BG_COLOR,
            justify="left",
            wraplength=300,
        )
        self.bet_summary.pack(fill="x", padx=8, pady=8)

        # History
        history_panel = tk.LabelFrame(
            side_panel,
            text="Last 10 Spins",
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=("Segoe UI", 11, "bold"),
        )
        history_panel.pack(fill="both", expand=True, pady=(0, 15))

        self.history_list = tk.Listbox(
            history_panel,
            bg="#0b1f24",
            fg=TEXT_COLOR,
            font=("Consolas", 11),
            height=8,
        )
        self.history_list.pack(fill="both", expand=True, padx=8, pady=8)

        # Chip selection
        chip_panel = tk.LabelFrame(
            side_panel,
            text="Chip Value",
            fg=ACCENT_COLOR,
            bg=BG_COLOR,
            font=("Segoe UI", 11, "bold"),
        )
        chip_panel.pack(fill="x", pady=(0, 10))

        self.chip_var = tk.IntVar(value=10)
        for val in [1, 5, 10, 25, 100]:
            rb = tk.Radiobutton(
                chip_panel,
                text=f"${val}",
                variable=self.chip_var,
                value=val,
                indicatoron=False,
                font=("Segoe UI", 11, "bold"),
                width=5,
                bg="#0b1f24",
                fg=TEXT_COLOR,
                selectcolor="#1f6f78",
                command=self.set_chip_value,
            )
            rb.pack(side="left", padx=4, pady=6)

        # Action buttons
        button_panel = tk.Frame(side_panel, bg=BG_COLOR)
        button_panel.pack(fill="x", pady=(5, 0))

        self.spin_btn = tk.Button(
            button_panel,
            text="SPIN",
            font=("Segoe UI", 16, "bold"),
            bg=ACCENT_COLOR,
            fg="black",
            width=10,
            command=self.start_spin,
        )
        self.spin_btn.pack(side="left", padx=(0, 10), pady=5)

        clear_btn = tk.Button(
            button_panel,
            text="Clear Bets",
            font=("Segoe UI", 11, "bold"),
            bg="#b22222",
            fg="white",
            width=10,
            command=self.clear_bets,
        )
        clear_btn.pack(side="left", padx=(0, 10), pady=5)

        self.bet_info_label = tk.Label(
            side_panel,
            text="Total Bet: $0 | Bets: 0",
            font=("Segoe UI", 10),
            fg="#d0d0d0",
            bg=BG_COLOR,
        )
        self.bet_info_label.pack(anchor="w", pady=(5, 0))

    def create_number_button(
        self,
        parent,
        label: str,
        color: str,
        row: int = None,
        col: int = None,
        width: int = 4,
        height: int = 2,
        font_size: int = 14,
    ):
        btn = tk.Button(
            parent,
            text=label,
            bg=color,
            fg="white",
            font=("Segoe UI", font_size, "bold"),
            width=width,
            height=height,
            relief="raised",
            bd=3,
            activebackground="#f0f0f0",
            activeforeground="black",
            command=lambda l=label: self.place_bet(l),
        )

        # store for later highlight
        self.num_buttons[label] = btn

        if row is not None and col is not None:
            btn.grid(row=row, column=col, padx=2, pady=2)
        else:
            btn.pack()

        return btn

    # ----- Game Logic Wrappers -----

    def set_chip_value(self):
        self.selected_chip_value = self.chip_var.get()

    def place_bet(self, bet_target: str):
        if self.balance < self.selected_chip_value:
            messagebox.showwarning(
                "Insufficient Balance",
                "Not enough balance for this chip."
            )
            return

        self.balance -= self.selected_chip_value
        self.current_bets[bet_target] = (
            self.current_bets.get(bet_target, 0) + self.selected_chip_value
        )
        self.update_status()

    def clear_bets(self):
        refund = sum(self.current_bets.values())
        self.balance += refund
        self.current_bets.clear()
        self.update_status()

    def update_status(self):
        total_bet = sum(self.current_bets.values())

        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_info_label.config(
            text=f"Total Bet: ${total_bet} | Bets: {len(self.current_bets)}"
        )

        if self.current_bets:
            parts = [
                f"{k}: ${v}"
                for k, v in sorted(self.current_bets.items(), key=lambda x: str(x[0]))
            ]
            text = ", ".join(parts)
        else:
            text = "No bets placed."

        self.bet_summary.config(text=text)

    def start_spin(self):
        if not self.current_bets:
            messagebox.showinfo("No Bets", "Place at least one bet before spinning.")
            return

        self.spin_btn.config(state="disabled")
        self.animate_wheel(0, 18)

    def animate_wheel(self, count: int, max_counts: int):
        temp_num = self.engine.spin()
        temp_color = self.engine.get_color(temp_num)

        color_map = {
            "red": "#ff4b3e",
            "black": "#111111",
            "green": "#2aa10f",
        }

        self.result_display.config(
            text=str(temp_num),
            fg="white",
            bg=color_map.get(temp_color, BG_COLOR),
        )

        if count < max_counts:
            delay = 40 + count * 15
            self.root.after(delay, lambda: self.animate_wheel(count + 1, max_counts))
        else:
            self.resolve_spin()

    def resolve_spin(self):
        winning_number = self.engine.spin()
        winning_color = self.engine.get_color(winning_number)

        color_map = {
            "red": "#ff4b3e",
            "black": "#111111",
            "green": "#2aa10f",
        }

        self.result_display.config(
            text=f"{winning_number}",
            fg="white",
            bg=color_map.get(winning_color, BG_COLOR),
        )

        # highlight winning number on the table
        self.highlight_winning_number(str(winning_number))

        total_won = self.engine.evaluate_bets(self.current_bets, winning_number)
        total_bet = sum(self.current_bets.values())
        net = total_won - total_bet

        # update balance
        self.balance += total_won

        # add to history
        self.add_to_history(winning_number, winning_color, net)

        if total_won > 0:
            self.balance_label.config(fg="#00ff88")
            message = (
                f"Result: {winning_number} ({winning_color.upper()}) – "
                f"YOU WON ${total_won} (net {net:+})"
            )
        else:
            self.balance_label.config(fg="#ff5555")
            message = (
                f"Result: {winning_number} ({winning_color.upper()}) – "
                f"No wins this round (net {net:+})"
            )

        self.bet_info_label.config(text=message)

        # reset for next round
        self.current_bets.clear()
        self.spin_btn.config(state="normal")
        self.root.after(2000, lambda: self.balance_label.config(fg=ACCENT_COLOR))
        self.root.after(2000, self.update_status)

    def highlight_winning_number(self, label: str):
        # reset all buttons
        for text, btn in self.num_buttons.items():
            if text == "0":
                bg = "green"
            else:
                n = int(text)
                bg = "red" if n in RED_NUMBERS else "black"
            btn.config(bg=bg, fg="white", relief="raised")

        # highlight winner
        btn = self.num_buttons.get(label)
        if btn:
            btn.config(bg=ACCENT_COLOR, fg="black", relief="sunken")

    def add_to_history(self, number: int, color: str, net: int):
        entry = f"{number:>2} ({color[0].upper()})   net {net:+}"
        self.history.insert(0, entry)
        self.history = self.history[:10]

        self.history_list.delete(0, tk.END)
        for item in self.history:
            self.history_list.insert(tk.END, item)


if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteGUI(root)
    root.mainloop()
