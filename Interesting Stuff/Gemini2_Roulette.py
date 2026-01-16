import tkinter as tk
from tkinter import messagebox
import random
import math
import time

# ==========================================
# CONFIGURATION & ASSETS
# ==========================================

WIDTH, HEIGHT = 1200, 800
BG_COLOR = "#0f2618"        # Deep Casino Green
FELT_COLOR = "#2e8b57"      # Table Felt Green
WOOD_COLOR = "#5c4033"      # Wood trim
GOLD_COLOR = "#ffd700"      # Gold accents
TEXT_COLOR = "#ffffff"

# Chip Colors for different values
CHIP_COLORS = {
    1: "#ffffff",    # White
    5: "#ff0000",    # Red
    10: "#0000ff",   # Blue
    25: "#008000",   # Green
    100: "#000000"   # Black
}

RED_NUMBERS = {
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
}

# Try to import sound, ignore if not on Windows
try:
    import winsound
    def play_sound(sound_type):
        if sound_type == "click":
            winsound.Beep(600, 50)
        elif sound_type == "win":
            winsound.Beep(1000, 200)
except ImportError:
    def play_sound(sound_type):
        pass

# ==========================================
# LOGIC ENGINE
# ==========================================

class RouletteEngine:
    """Handles the math and rules."""
    def spin(self):
        return random.randint(0, 36)

    def get_color(self, number):
        if number == 0: return "green"
        return "red" if number in RED_NUMBERS else "black"

    def get_winning_bets(self, number):
        """Returns a list of all bet keys that win for a given number."""
        winners = []
        
        # Single Number
        winners.append(f"NUM_{number}")
        
        # Colors
        color = self.get_color(number)
        if color == "red": winners.append("OPT_RED")
        if color == "black": winners.append("OPT_BLACK")
        
        if number != 0:
            # Even/Odd
            winners.append("OPT_EVEN" if number % 2 == 0 else "OPT_ODD")
            # Low/High
            winners.append("OPT_LOW" if number <= 18 else "OPT_HIGH")
            # Dozens
            if 1 <= number <= 12: winners.append("OPT_1ST12")
            elif 13 <= number <= 24: winners.append("OPT_2ND12")
            elif 25 <= number <= 36: winners.append("OPT_3RD12")
            
        return winners

    def get_payout_ratio(self, bet_key):
        """Returns payout ratio (e.g., 35 for single number, 1 for red/black)."""
        if bet_key.startswith("NUM_"): return 35
        if bet_key.startswith("OPT_"):
            if "1ST12" in bet_key or "2ND12" in bet_key or "3RD12" in bet_key:
                return 2
            return 1
        return 0

# ==========================================
# GUI APPLICATION
# ==========================================

class RoulettePro:
    def __init__(self, root):
        self.root = root
        self.engine = RouletteEngine()
        self.root.title("Python Roulette Professional")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        
        # Game State
        self.balance = 2000
        self.current_chip_value = 10
        self.bets = {} # key: amount
        self.visual_chips = [] # list of canvas ids
        
        self.setup_ui()
        self.update_header()

    def setup_ui(self):
        # --- Top Header (Info) ---
        self.header_frame = tk.Frame(self.root, bg=BG_COLOR)
        self.header_frame.pack(fill="x", pady=10, padx=20)
        
        self.lbl_balance = tk.Label(self.header_frame, text="Balance: $2000", font=("Helvetica", 24, "bold"), bg=BG_COLOR, fg=GOLD_COLOR)
        self.lbl_balance.pack(side="left")
        
        self.lbl_result = tk.Label(self.header_frame, text="READY TO SPIN", font=("Helvetica", 28, "bold"), bg=BG_COLOR, fg="white")
        self.lbl_result.pack(side="right")

        # --- Main Table Area (Canvas) ---
        # We use a Canvas for the table so we can draw custom shapes and stack chips visuals
        self.canvas = tk.Canvas(self.root, width=1100, height=500, bg=FELT_COLOR, bd=0, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        # Bind clicks
        self.canvas.bind("<Button-1>", self.on_table_click)
        
        self.draw_table()

        # --- Bottom Controls ---
        self.controls_frame = tk.Frame(self.root, bg=WOOD_COLOR, pady=15)
        self.controls_frame.pack(fill="x", side="bottom")

        # Chip Selectors
        tk.Label(self.controls_frame, text="CHIP VALUE:", bg=WOOD_COLOR, fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=20)
        
        self.chip_var = tk.IntVar(value=10)
        for val in [1, 5, 10, 25, 100]:
            # Custom styled radio buttons using Frame/Label trick or standard Radiobutton
            rb = tk.Radiobutton(self.controls_frame, text=f"${val}", variable=self.chip_var, value=val, 
                                bg=CHIP_COLORS[val], fg="black" if val!=100 and val!=10 and val!=25 else "white",
                                font=("Arial", 12, "bold"), indicatoron=0, width=5, 
                                command=lambda: play_sound("click"))
            rb.pack(side="left", padx=5)

        # Action Buttons
        btn_style = {"font":("Arial", 14, "bold"), "width": 12, "relief": "raised", "bd": 4}
        
        self.btn_spin = tk.Button(self.controls_frame, text="SPIN WHEEL", bg=GOLD_COLOR, fg="black", command=self.start_spin, **btn_style)
        self.btn_spin.pack(side="right", padx=20)
        
        self.btn_clear = tk.Button(self.controls_frame, text="CLEAR BETS", bg="#8b0000", fg="white", command=self.clear_bets, **btn_style)
        self.btn_clear.pack(side="right", padx=10)

    # -------------------------------------------------------------------------
    # DRAWING THE TABLE
    # -------------------------------------------------------------------------
    def draw_table(self):
        """Draws the betting grid on the canvas."""
        self.zones = {} # Map coordinates to bet keys for click detection
        
        # Dimensions
        cw, ch = 60, 80 # Cell width/height
        start_x, start_y = 100, 50
        
        # 1. Draw "0"
        self.canvas.create_rectangle(start_x - cw, start_y, start_x, start_y + 3*ch, fill="#006400", outline="white", width=2)
        self.canvas.create_text(start_x - cw/2, start_y + 1.5*ch, text="0", fill="white", font=("Arial", 20, "bold"))
        self.register_zone(start_x - cw, start_y, start_x, start_y + 3*ch, "NUM_0")

        # 2. Draw 1-36 Numbers
        for n in range(1, 37):
            # Math to place them in 3 rows
            # Row 0 (top) are 3, 6, 9...
            # Row 1 (mid) are 2, 5, 8...
            # Row 2 (bot) are 1, 4, 7...
            if n % 3 == 0: row = 0
            elif n % 3 == 2: row = 1
            else: row = 2
            
            col = (n - 1) // 3
            
            x1 = start_x + col * cw
            y1 = start_y + row * ch
            x2 = x1 + cw
            y2 = y1 + ch
            
            color = "#b22222" if n in RED_NUMBERS else "black"
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="white", width=2)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(n), fill="white", font=("Arial", 16, "bold"))
            self.register_zone(x1, y1, x2, y2, f"NUM_{n}")

        # 3. Draw Outside Bets (Dozens)
        doz_y = start_y + 3*ch
        doz_w = 4 * cw
        labels = ["1st 12", "2nd 12", "3rd 12"]
        keys = ["OPT_1ST12", "OPT_2ND12", "OPT_3RD12"]
        
        for i in range(3):
            x1 = start_x + i * doz_w
            y1 = doz_y
            x2 = x1 + doz_w
            y2 = y1 + 50
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=FELT_COLOR, outline="white", width=2)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=labels[i], fill="white", font=("Arial", 12, "bold"))
            self.register_zone(x1, y1, x2, y2, keys[i])

        # 4. Draw Outside Bets (Even Money)
        even_y = doz_y + 50
        even_w = 2 * cw
        bets = [
            ("1-18", "OPT_LOW"), ("EVEN", "OPT_EVEN"), 
            ("RED", "OPT_RED"), ("BLACK", "OPT_BLACK"), 
            ("ODD", "OPT_ODD"), ("19-36", "OPT_HIGH")
        ]
        
        for i, (txt, key) in enumerate(bets):
            x1 = start_x + i * even_w
            y1 = even_y
            x2 = x1 + even_w
            y2 = y1 + 50
            
            fill_c = FELT_COLOR
            if txt == "RED": fill_c = "#b22222"
            elif txt == "BLACK": fill_c = "black"
            
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_c, outline="white", width=2)
            self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=txt, fill="white", font=("Arial", 12, "bold"))
            self.register_zone(x1, y1, x2, y2, key)

    def register_zone(self, x1, y1, x2, y2, bet_key):
        """Stores the clickable area."""
        self.zones[bet_key] = (x1, y1, x2, y2)

    # -------------------------------------------------------------------------
    # INTERACTION
    # -------------------------------------------------------------------------
    def on_table_click(self, event):
        x, y = event.x, event.y
        chip_val = self.chip_var.get()
        
        if self.balance < chip_val:
            messagebox.showwarning("Bankrupt", "Insufficient funds!")
            return

        # Check which zone was clicked
        clicked_key = None
        cx, cy = 0, 0
        
        for key, coords in self.zones.items():
            x1, y1, x2, y2 = coords
            if x1 <= x <= x2 and y1 <= y <= y2:
                clicked_key = key
                cx, cy = (x1+x2)/2, (y1+y2)/2
                break
        
        if clicked_key:
            self.place_bet(clicked_key, chip_val, cx, cy)
            play_sound("click")

    def place_bet(self, key, amount, x, y):
        self.balance -= amount
        self.bets[key] = self.bets.get(key, 0) + amount
        self.update_header()
        
        # Draw Chip Visual
        # Add a slight random offset so chips stack "messily" like real life
        off_x = random.randint(-5, 5)
        off_y = random.randint(-5, 5)
        
        color = CHIP_COLORS.get(amount, "white")
        
        # Draw chip circle
        r = 15 # radius
        chip_id = self.canvas.create_oval(x+off_x-r, y+off_y-r, x+off_x+r, y+off_y+r, fill=color, outline="gold", width=2)
        # Draw chip text
        text_id = self.canvas.create_text(x+off_x, y+off_y, text=str(amount), fill="black" if color=="white" else "white", font=("Arial", 8, "bold"))
        
        self.visual_chips.append(chip_id)
        self.visual_chips.append(text_id)

    def clear_bets(self):
        refund = sum(self.bets.values())
        self.balance += refund
        self.bets.clear()
        
        # Remove visuals
        for item in self.visual_chips:
            self.canvas.delete(item)
        self.visual_chips.clear()
        
        self.update_header()

    def update_header(self):
        self.lbl_balance.config(text=f"Balance: ${self.balance}")

    # -------------------------------------------------------------------------
    # GAMEPLAY
    # -------------------------------------------------------------------------
    def start_spin(self):
        if not self.bets:
            messagebox.showinfo("Wait", "Please place a bet first!")
            return
            
        self.btn_spin.config(state="disabled")
        self.btn_clear.config(state="disabled")
        
        # Wheel Animation Logic
        # We'll flash the result label rapidly to simulate spinning
        self.animate_wheel(0, 30) 

    def animate_wheel(self, step, max_steps):
        # Generate random number for visual
        num = self.engine.spin()
        color = self.engine.get_color(num)
        fg_c = "green" if color == "green" else color
        
        self.lbl_result.config(text=str(num), fg=fg_c)
        
        if step < max_steps:
            # Exponential decay for delay (starts fast, slows down)
            delay = int(50 + (step ** 1.8)) 
            self.root.after(delay, lambda: self.animate_wheel(step+1, max_steps))
        else:
            self.finish_spin()

    def finish_spin(self):
        winning_num = self.engine.spin()
        winning_color = self.engine.get_color(winning_num)
        
        # Visual Update
        self.lbl_result.config(text=f"{winning_num} {winning_color.upper()}", fg="white" if winning_color=="black" else winning_color)
        
        if winning_color == "green": 
            self.lbl_result.config(fg="#00ff00")

        # Calculate Winnings
        total_payout = 0
        winning_keys = self.engine.get_winning_bets(winning_num)
        
        for bet_key, bet_amount in self.bets.items():
            if bet_key in winning_keys:
                ratio = self.engine.get_payout_ratio(bet_key)
                # Payout = Bet + (Bet * Ratio)
                winnings = bet_amount + (bet_amount * ratio)
                total_payout += winnings
        
        self.balance += total_payout
        
        # Show Result Summary
        net_result = total_payout - sum(self.bets.values())
        
        if total_payout > 0:
            play_sound("win")
            msg = f"You won ${total_payout}!"
            self.lbl_result.config(text=f"WINNER: {winning_num}", fg=GOLD_COLOR)
        else:
            msg = "No wins this time."
        
        # Clean up
        self.update_header()
        
        # After 2 seconds, clear chips (casino style: house takes losing chips)
        # For simplicity in this game, we just clear everything for next round
        self.root.after(3000, self.reset_table)

    def reset_table(self):
        self.bets.clear()
        for item in self.visual_chips:
            self.canvas.delete(item)
        self.visual_chips.clear()
        
        self.lbl_result.config(text="PLACE BETS", fg="white")
        self.btn_spin.config(state="normal")
        self.btn_clear.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    app = RoulettePro(root)
    root.mainloop()