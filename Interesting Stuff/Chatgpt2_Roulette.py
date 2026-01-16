import tkinter as tk
from tkinter import messagebox
import random

# =========================
# CONFIG
# =========================

WIDTH, HEIGHT = 1200, 800
BG_COLOR = "#041f1e"
FELT_COLOR = "#17653b"
WOOD_COLOR = "#4b3326"
GOLD_COLOR = "#f9c846"
TEXT_COLOR = "#ffffff"

CHIP_COLORS = {
    1: "#ffffff",   # white
    5: "#ff0000",   # red
    10: "#0000ff",  # blue
    25: "#008000",  # green
    100: "#000000", # black
}

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

# Optional sound (Windows only)
try:
    import winsound
    def play_sound(sound_type):
        if sound_type == "click":
            winsound.Beep(700, 40)
        elif sound_type == "win":
            winsound.Beep(1100, 180)
        elif sound_type == "lose":
            winsound.Beep(400, 120)
except ImportError:
    def play_sound(sound_type):
        pass

# =========================
# ENGINE
# =========================

class RouletteEngine:
    """Pure math + rules; no GUI."""
    def spin(self) -> int:
        return random.randint(0, 36)

    def get_color(self, number: int) -> str:
        if number == 0:
            return "green"
        return "red" if number in RED_NUMBERS else "black"

    def get_winning_bets(self, number: int):
        winners = []
        # Straight up
        winners.append(f"NUM_{number}")

        color = self.get_color(number)
        if color == "red":
            winners.append("OPT_RED")
        elif color == "black":
            winners.append("OPT_BLACK")

        if number != 0:
            # Even / Odd
            winners.append("OPT_EVEN" if number % 2 == 0 else "OPT_ODD")
            # Low / High
            winners.append("OPT_LOW" if number <= 18 else "OPT_HIGH")
            # Dozens
            if 1 <= number <= 12:
                winners.append("OPT_1ST12")
            elif 13 <= number <= 24:
                winners.append("OPT_2ND12")
            else:
                winners.append("OPT_3RD12")

        return winners

    def get_payout_ratio(self, bet_key: str) -> int:
        """Return the odds (35:1, 2:1, 1:1)."""
        if bet_key.startswith("NUM_"):
            return 35
        if bet_key in ("OPT_1ST12", "OPT_2ND12", "OPT_3RD12"):
            return 2
        if bet_key.startswith("OPT_"):
            return 1
        return 0

    def evaluate_bets(self, bets: dict, winning_number: int):
        """
        bets: {bet_key: amount}
        Returns: (total_payout, detail_list)
        detail_list: list of (key, amount, payout, net)
        """
        winners = set(self.get_winning_bets(winning_number))
        details = []
        total_payout = 0

        for key, amt in bets.items():
            if key in winners:
                ratio = self.get_payout_ratio(key)
                payout = amt * (ratio + 1)  # return stake + winnings
                net = payout - amt
            else:
                payout = 0
                net = -amt

            total_payout += payout
            details.append((key, amt, payout, net))

        return total_payout, details

# =========================
# GUI APP
# =========================

class RouletteApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.engine = RouletteEngine()

        self.root.title("Python Roulette – Analytics Edition")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Game/session state
        self.balance = 2000
        self.bets = {}              # bet_key -> amount
        self.visual_chips = {}      # bet_key -> list of canvas item IDs
        self.last_bets = {}         # snapshot from previous round

        # Analytics
        self.spin_count = 0
        self.total_bet_volume = 0
        self.total_return = 0       # total payout (including stake) across all spins
        self.best_win = 0
        self.worst_loss = 0

        # Drawing helpers
        self.zones = {}             # bet_key -> (x1, y1, x2, y2)
        self.current_highlight = None

        self.setup_layout()
        self.update_header()
        self.update_stats()

    # ---------- Layout ----------

    def setup_layout(self):
        # Grid: table left, info right, controls bottom
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        # Left: table canvas
        table_frame = tk.Frame(self.root, bg=BG_COLOR)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=(15, 5), pady=15)

        self.canvas = tk.Canvas(
            table_frame, width=800, height=520,
            bg=FELT_COLOR, bd=0, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_table_click)

        # Right: info + history
        right_frame = tk.Frame(self.root, bg=BG_COLOR)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 15), pady=15)

        header = tk.Frame(right_frame, bg=BG_COLOR)
        header.pack(fill="x", pady=(0, 10))

        self.lbl_balance = tk.Label(
            header, text="Balance: $0",
            font=("Helvetica", 22, "bold"),
            bg=BG_COLOR, fg=GOLD_COLOR
        )
        self.lbl_balance.pack(anchor="w")

        self.lbl_result = tk.Label(
            header, text="PLACE YOUR BETS",
            font=("Helvetica", 24, "bold"),
            bg=BG_COLOR, fg=TEXT_COLOR
        )
        self.lbl_result.pack(anchor="w", pady=(5, 0))

        # Stats panel
        stats_frame = tk.LabelFrame(
            right_frame, text="Session Stats",
            bg=BG_COLOR, fg=GOLD_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        stats_frame.pack(fill="x", pady=(0, 10))

        self.lbl_stats_spins = tk.Label(stats_frame, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w")
        self.lbl_stats_spins.pack(fill="x")
        self.lbl_stats_volume = tk.Label(stats_frame, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w")
        self.lbl_stats_volume.pack(fill="x")
        self.lbl_stats_return = tk.Label(stats_frame, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w")
        self.lbl_stats_return.pack(fill="x")
        self.lbl_stats_extremes = tk.Label(stats_frame, bg=BG_COLOR, fg=TEXT_COLOR, anchor="w")
        self.lbl_stats_extremes.pack(fill="x")

        # History panel
        history_frame = tk.LabelFrame(
            right_frame, text="Last 12 Spins",
            bg=BG_COLOR, fg=GOLD_COLOR,
            font=("Segoe UI", 11, "bold")
        )
        history_frame.pack(fill="both", expand=True)

        self.history_list = tk.Listbox(
            history_frame,
            bg="#082022", fg=TEXT_COLOR,
            font=("Consolas", 11), height=12
        )
        self.history_list.pack(fill="both", expand=True, padx=5, pady=5)

        # Bottom controls
        bottom_frame = tk.Frame(self.root, bg=WOOD_COLOR, height=80)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        bottom_frame.grid_propagate(False)

        tk.Label(
            bottom_frame, text="CHIP VALUE:",
            bg=WOOD_COLOR, fg="white",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left", padx=(20, 10))

        self.chip_var = tk.IntVar(value=10)
        for val in [1, 5, 10, 25, 100]:
            rb = tk.Radiobutton(
                bottom_frame, text=f"${val}",
                variable=self.chip_var, value=val,
                indicatoron=False, width=5,
                font=("Segoe UI", 11, "bold"),
                bg=CHIP_COLORS[val],
                fg="black" if val in (1, 5) else "white",
                selectcolor="#444444",
                command=lambda: play_sound("click")
            )
            rb.pack(side="left", padx=4, pady=10)

        btn_style = dict(
            font=("Segoe UI", 13, "bold"),
            width=11, relief="raised", bd=3
        )

        self.btn_spin = tk.Button(
            bottom_frame, text="SPIN",
            bg=GOLD_COLOR, fg="black",
            command=self.start_spin, **btn_style
        )
        self.btn_spin.pack(side="right", padx=(10, 20), pady=10)

        self.btn_clear = tk.Button(
            bottom_frame, text="CLEAR",
            bg="#8b0000", fg="white",
            command=self.clear_bets, **btn_style
        )
        self.btn_clear.pack(side="right", padx=5, pady=10)

        self.btn_undo = tk.Button(
            bottom_frame, text="UNDO BET",
            bg="#555555", fg="white",
            command=self.undo_last_bet, **btn_style
        )
        self.btn_undo.pack(side="right", padx=5, pady=10)

        self.btn_rebet = tk.Button(
            bottom_frame, text="REBET",
            bg="#1a5e63", fg="white",
            command=self.rebet_last_round, **btn_style
        )
        self.btn_rebet.pack(side="right", padx=5, pady=10)

        self.lbl_bet_summary = tk.Label(
            bottom_frame,
            text="Total Bet: $0 | Bets: 0",
            bg=WOOD_COLOR, fg="#e0e0e0",
            font=("Segoe UI", 10)
        )
        self.lbl_bet_summary.pack(side="left", padx=20)

        # Finally, draw the table
        self.draw_table()

    # ---------- Table Drawing ----------

    def draw_table(self):
        cw, ch = 60, 80
        start_x, start_y = 120, 50

        # Outer wood/gold border
        self.canvas.create_rectangle(
            start_x - 70, start_y - 20,
            start_x + 12 * cw + 10, start_y + 3 * ch + 110,
            outline=WOOD_COLOR, width=10, fill=""
        )
        self.canvas.create_rectangle(
            start_x - 60, start_y - 10,
            start_x + 12 * cw, start_y + 3 * ch + 100,
            outline=GOLD_COLOR, width=3, fill=""
        )

        # 0 slot
        x1 = start_x - cw
        y1 = start_y
        x2 = x1 + cw
        y2 = y1 + 3 * ch
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#006400", outline="white", width=2)
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="0",
                                fill="white", font=("Arial", 22, "bold"))
        self.zones["NUM_0"] = (x1, y1, x2, y2)

        # 1–36 grid
        for n in range(1, 37):
            if n % 3 == 0:
                row = 0
            elif n % 3 == 2:
                row = 1
            else:
                row = 2

            col = (n - 1) // 3
            x1 = start_x + col * cw
            y1 = start_y + row * ch
            x2 = x1 + cw
            y2 = y1 + ch

            color = "#b22222" if n in RED_NUMBERS else "black"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=2)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(n),
                                    fill="white", font=("Arial", 16, "bold"))
            self.zones[f"NUM_{n}"] = (x1, y1, x2, y2)

        # Dozens
        doz_y = start_y + 3 * ch
        doz_w = 4 * cw
        labels = ["1st 12", "2nd 12", "3rd 12"]
        keys = ["OPT_1ST12", "OPT_2ND12", "OPT_3RD12"]
        for i in range(3):
            x1 = start_x + i * doz_w
            y1 = doz_y
            x2 = x1 + doz_w
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=FELT_COLOR, outline="white", width=2)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=labels[i],
                                    fill="white", font=("Arial", 12, "bold"))
            self.zones[keys[i]] = (x1, y1, x2, y2)

        # Even money bets
        even_y = doz_y + 50
        even_w = 2 * cw
        bets = [
            ("1-18", "OPT_LOW"),
            ("EVEN", "OPT_EVEN"),
            ("RED", "OPT_RED"),
            ("BLACK", "OPT_BLACK"),
            ("ODD", "OPT_ODD"),
            ("19-36", "OPT_HIGH"),
        ]
        for i, (txt, key) in enumerate(bets):
            x1 = start_x + i * even_w
            y1 = even_y
            x2 = x1 + even_w
            y2 = y1 + 50
            fill_c = FELT_COLOR
            if txt == "RED":
                fill_c = "#b22222"
            elif txt == "BLACK":
                fill_c = "black"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_c, outline="white", width=2)
            self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=txt,
                                    fill="white", font=("Arial", 12, "bold"))
            self.zones[key] = (x1, y1, x2, y2)

    # ---------- Interaction ----------

    def on_table_click(self, event):
        x, y = event.x, event.y
        chip_val = self.chip_var.get()

        if self.balance < chip_val:
            messagebox.showwarning("Insufficient Funds", "Not enough balance for this chip.")
            return

        clicked_key = None
        center = None
        for key, (x1, y1, x2, y2) in self.zones.items():
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked_key = key
                center = ((x1 + x2) / 2, (y1 + y2) / 2)
                break

        if not clicked_key:
            return

        self.place_bet(clicked_key, chip_val, *center)
        play_sound("click")

    def place_bet(self, key: str, amount: int, cx: float, cy: float):
        self.balance -= amount
        self.bets[key] = self.bets.get(key, 0) + amount

        # Draw a chip with small random offset
        off_x = random.randint(-4, 4)
        off_y = random.randint(-4, 4)
        color = CHIP_COLORS.get(amount, "white")
        r = 15

        chip_id = self.canvas.create_oval(
            cx + off_x - r, cy + off_y - r,
            cx + off_x + r, cy + off_y + r,
            fill=color, outline="gold", width=2
        )
        text_color = "black" if color in ("#ffffff", "#ffff00") else "white"
        text_id = self.canvas.create_text(
            cx + off_x, cy + off_y,
            text=str(amount), fill=text_color,
            font=("Arial", 9, "bold")
        )
        self.visual_chips.setdefault(key, []).extend([chip_id, text_id])

        self.update_header()

    def undo_last_bet(self):
        """Remove one chip worth of bet from the last edited key."""
        if not self.bets:
            return

        # Take some key (arbitrary last from dict)
        key_to_reduce = list(self.bets.keys())[-1]
        # Choose the largest chip denomination that fits
        amount_per_chip = None
        for val in sorted(CHIP_COLORS.keys(), reverse=True):
            if self.bets[key_to_reduce] >= val:
                amount_per_chip = val
                break
        if amount_per_chip is None:
            return

        # Update logical bet
        self.bets[key_to_reduce] -= amount_per_chip
        if self.bets[key_to_reduce] <= 0:
            del self.bets[key_to_reduce]

        # Refund
        self.balance += amount_per_chip

        # Remove chip visuals
        ids = self.visual_chips.get(key_to_reduce, [])
        if ids:
            # remove last 2 ids: text, circle (reverse order we added)
            text_id = ids.pop()
            chip_id = ids.pop() if ids else None
            self.canvas.delete(text_id)
            if chip_id is not None:
                self.canvas.delete(chip_id)
        if not ids and key_to_reduce in self.visual_chips:
            del self.visual_chips[key_to_reduce]

        self.update_header()

    def clear_bets(self):
        refund = sum(self.bets.values())
        self.balance += refund
        self.bets.clear()

        # Clear all chip drawings
        for ids in self.visual_chips.values():
            for item in ids:
                self.canvas.delete(item)
        self.visual_chips.clear()

        self.update_header()

    def update_header(self):
        self.lbl_balance.config(text=f"Balance: ${self.balance}")
        total_bet = sum(self.bets.values())
        self.lbl_bet_summary.config(
            text=f"Total Bet: ${total_bet} | Bets: {len(self.bets)}"
        )

    def update_stats(self):
        self.lbl_stats_spins.config(
            text=f"Spins: {self.spin_count}"
        )
        self.lbl_stats_volume.config(
            text=f"Total Bet Volume: ${self.total_bet_volume}"
        )

        # Net = total_return - total_bet_volume
        net = self.total_return - self.total_bet_volume
        if self.total_bet_volume > 0:
            roi_pct = 100.0 * net / self.total_bet_volume
        else:
            roi_pct = 0.0

        self.lbl_stats_return.config(
            text=f"Net Result: ${net:+.0f} ({roi_pct:+.1f}% ROI)"
        )
        self.lbl_stats_extremes.config(
            text=f"Best Win: ${self.best_win:+.0f} | Worst Loss: ${self.worst_loss:+.0f}"
        )

    def rebet_last_round(self):
        if not self.last_bets:
            return

        needed = sum(self.last_bets.values())
        if self.balance < needed:
            messagebox.showinfo(
                "Rebet Failed",
                "Not enough balance to repeat last round's bets."
            )
            return

        # Recreate chips using largest denominations
        for key, amt in self.last_bets.items():
            if key not in self.zones:
                continue
            x1, y1, x2, y2 = self.zones[key]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

            remaining = amt
            for chip_val in sorted(CHIP_COLORS.keys(), reverse=True):
                while remaining >= chip_val:
                    self.place_bet(key, chip_val, cx, cy)
                    remaining -= chip_val

    # ---------- Spin logic ----------

    def start_spin(self):
        if not self.bets:
            messagebox.showinfo("No Bets", "Place at least one bet before spinning.")
            return

        self.btn_spin.config(state="disabled")
        self.btn_clear.config(state="disabled")
        self.btn_undo.config(state="disabled")
        self.btn_rebet.config(state="disabled")

        self.animate_wheel(0, 25)

    def animate_wheel(self, step, max_steps):
        # purely visual random flashes
        num = self.engine.spin()
        color = self.engine.get_color(num)
        fg = "green" if color == "green" else color
        self.lbl_result.config(text=str(num), fg=fg)

        if step < max_steps:
            delay = int(40 + step ** 1.7)  # slow down
            self.root.after(delay, lambda: self.animate_wheel(step + 1, max_steps))
        else:
            self.finish_spin()

    def finish_spin(self):
        winning_num = self.engine.spin()
        color = self.engine.get_color(winning_num)
        display_color = "#00ff00" if color == "green" else ("white" if color == "black" else "red")

        self.lbl_result.config(
            text=f"{winning_num} {color.upper()}",
            fg=display_color
        )

        self.highlight_winning_cell(winning_num)

        round_bet = sum(self.bets.values())
        self.spin_count += 1
        self.total_bet_volume += round_bet

        total_payout, details = self.engine.evaluate_bets(self.bets, winning_num)
        self.balance += total_payout
        self.total_return += total_payout

        net_round = total_payout - round_bet
        self.best_win = max(self.best_win, net_round)
        self.worst_loss = min(self.worst_loss, net_round)

        if net_round > 0:
            play_sound("win")
        elif net_round < 0:
            play_sound("lose")

        # History entry
        entry = f"#{self.spin_count:03d}  {winning_num:2d} {color[0].upper()}   net {net_round:+}"
        self.history_list.insert(0, entry)
        if self.history_list.size() > 12:
            self.history_list.delete(12, tk.END)

        # Store bets as last_bets (for rebet) before clearing
        self.last_bets = dict(self.bets)

        # Clear chips and bets from table
        self.bets.clear()
        for ids in self.visual_chips.values():
            for item in ids:
                self.canvas.delete(item)
        self.visual_chips.clear()

        self.update_header()
        self.update_stats()

        self.root.after(2500, self.enable_controls)

    def enable_controls(self):
        self.btn_spin.config(state="normal")
        self.btn_clear.config(state="normal")
        self.btn_undo.config(state="normal")
        self.btn_rebet.config(state="normal")
        self.lbl_result.config(bg=BG_COLOR)

    def highlight_winning_cell(self, number: int):
        # Remove any previous highlight
        if self.current_highlight is not None:
            self.canvas.delete(self.current_highlight)
            self.current_highlight = None

        key = f"NUM_{number}"
        if key not in self.zones:
            key = "NUM_0"
        x1, y1, x2, y2 = self.zones[key]

        self.current_highlight = self.canvas.create_rectangle(
            x1 - 2, y1 - 2, x2 + 2, y2 + 2,
            outline=GOLD_COLOR, width=4
        )

        # Simple fade-out animation
        def fade(step=0):
            if self.current_highlight is None:
                return
            if step > 6:
                self.canvas.delete(self.current_highlight)
                self.current_highlight = None
                return
            width = 4 - step * 0.5
            self.canvas.itemconfig(self.current_highlight, width=max(width, 1))
            self.root.after(200, lambda: fade(step + 1))

        fade()


if __name__ == "__main__":
    root = tk.Tk()
    app = RouletteApp(root)
    root.mainloop()
