import tkinter as tk
from tkinter import messagebox
import random

# --- Constants & Config ---
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
BG_COLOR = "#0f3818"      # Dark Casino Green
TABLE_COLOR = "#236b36"   # Lighter Felt Green
ACCENT_COLOR = "#d4af37"  # Gold
TEXT_COLOR = "#ffffff"

# European/American hybrid definitions
# (Using European layout for simplicity but American-style visuals can be adapted)
RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}

class RouletteGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Royal Roulette")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)

        # Game State
        self.balance = 1000
        self.current_bets = {}  # Format: {'bet_type_id': amount}
        self.selected_chip_value = 10
        
        # UI Elements Container
        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        # 1. HEADER (Wheel Display & Balance)
        header_frame = tk.Frame(self.root, bg=BG_COLOR, pady=20)
        header_frame.pack(fill="x")

        self.balance_label = tk.Label(header_frame, text=f"Balance: ${self.balance}", 
                                      font=("Courier", 24, "bold"), fg=ACCENT_COLOR, bg=BG_COLOR)
        self.balance_label.pack(side="left", padx=20)

        self.result_label = tk.Label(header_frame, text="PLACE YOUR BETS", 
                                     font=("Helvetica", 32, "bold"), fg="white", bg=BG_COLOR)
        self.result_label.pack(side="right", padx=20)

        # 2. THE BETTING TABLE (Canvas for custom drawing/buttons)
        # We use frames to simulate the grid
        table_frame = tk.Frame(self.root, bg=TABLE_COLOR, bd=10, relief="ridge")
        table_frame.pack(pady=20, padx=20)

        # --- Zeros Column ---
        zero_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        zero_frame.grid(row=0, column=0, rowspan=3, padx=2)
        self.create_bet_btn(zero_frame, "0", "green", width=6, height=8, font_size=16)

        # --- Numbers Grid (1-36) ---
        # Rows in roulette table are actually 3, 6, 9... but visually we want standard layout
        # Standard layout: 3 rows. 
        # Row 1: 3, 6, 9... | Row 2: 2, 5, 8... | Row 3: 1, 4, 7...
        nums_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        nums_frame.grid(row=0, column=1, rowspan=3)

        # Generate the 3x12 grid
        for n in range(1, 37):
            # Calculate grid position
            # Visual Row 0 -> numbers divisible by 3 (3, 6, 9)
            # Visual Row 1 -> remainder 2 (2, 5, 8)
            # Visual Row 2 -> remainder 1 (1, 4, 7)
            if n % 3 == 0: row = 0
            elif n % 3 == 2: row = 1
            else: row = 2
            
            col = (n - 1) // 3
            
            color = "red" if n in RED_NUMBERS else "black"
            self.create_bet_btn(nums_frame, str(n), color, row, col)

        # --- Outside Bets (Red/Black, Even/Odd, etc) ---
        outside_frame = tk.Frame(table_frame, bg=TABLE_COLOR)
        outside_frame.grid(row=3, column=1, sticky="we", pady=10)

        # Helper to simplify outside bet button creation
        opts = [("1-18", "low"), ("EVEN", "even"), ("RED", "red"), 
                ("BLACK", "black"), ("ODD", "odd"), ("19-36", "high")]
        
        for i, (text, bet_code) in enumerate(opts):
            color = "red" if bet_code == "red" else "black" if bet_code == "black" else "#2e8b57"
            btn = tk.Button(outside_frame, text=text, bg=color, fg="white", 
                            font=("Arial", 10, "bold"), width=12, height=2,
                            command=lambda b=bet_code: self.place_bet(b))
            btn.grid(row=0, column=i, padx=2)

        # 3. CONTROLS (Chips & Actions)
        control_frame = tk.Frame(self.root, bg=BG_COLOR, pady=20)
        control_frame.pack(fill="x", side="bottom")

        # Chip Selector
        tk.Label(control_frame, text="Select Chip:", bg=BG_COLOR, fg="white").pack(side="left", padx=10)
        
        self.chip_var = tk.IntVar(value=10)
        chips = [1, 5, 10, 25, 100]
        for val in chips:
            rb = tk.Radiobutton(control_frame, text=f"${val}", variable=self.chip_var, 
                                value=val, bg=BG_COLOR, fg="white", selectcolor="black",
                                command=self.set_chip_value)
            rb.pack(side="left", padx=5)

        # Action Buttons
        self.spin_btn = tk.Button(control_frame, text="SPIN", bg=ACCENT_COLOR, fg="black", 
                                  font=("Arial", 16, "bold"), width=15, command=self.start_spin)
        self.spin_btn.pack(side="right", padx=20)
        
        tk.Button(control_frame, text="Clear Bets", bg="#8b0000", fg="white", 
                  font=("Arial", 12), command=self.clear_bets).pack(side="right", padx=10)

        # Info Box (Total Bet)
        self.bet_info_label = tk.Label(self.root, text="Total Bet: $0", 
                                       font=("Arial", 14), bg=BG_COLOR, fg="#aaaaaa")
        self.bet_info_label.pack(side="bottom", pady=5)

    def create_bet_btn(self, parent, label, color, r=None, c=None, width=6, height=3, font_size=12):
        """Creates a grid button that places a bet on a specific number"""
        btn = tk.Button(parent, text=label, bg=color, fg="white", 
                        font=("Arial", font_size, "bold"), width=width, height=height,
                        activebackground="white", activeforeground="black",
                        command=lambda: self.place_bet(label))
        if r is not None and c is not None:
            btn.grid(row=r, column=c, padx=1, pady=1)
        else:
            btn.pack() # For 0/00 which might not use grid
        return btn

    def set_chip_value(self):
        self.selected_chip_value = self.chip_var.get()

    def place_bet(self, bet_target):
        if self.balance < self.selected_chip_value:
            messagebox.showwarning("Oops", "Not enough balance!")
            return

        # Deduct balance
        self.balance -= self.selected_chip_value
        
        # Add to current bets
        if bet_target in self.current_bets:
            self.current_bets[bet_target] += self.selected_chip_value
        else:
            self.current_bets[bet_target] = self.selected_chip_value
            
        self.update_status()

    def clear_bets(self):
        # Refund current bets to balance
        total_bet = sum(self.current_bets.values())
        self.balance += total_bet
        self.current_bets.clear()
        self.update_status()

    def update_status(self):
        total_wager = sum(self.current_bets.values())
        self.balance_label.config(text=f"Balance: ${self.balance}")
        self.bet_info_label.config(text=f"Total Bet: ${total_wager} | Bets placed: {len(self.current_bets)}")

    def start_spin(self):
        if not self.current_bets:
            messagebox.showinfo("Wait", "Place a bet first!")
            return
        
        self.spin_btn.config(state="disabled")
        self.animate_wheel(0, 20) # Start animation loops

    def animate_wheel(self, count, max_counts):
        """Simulates the ball spinning by flashing random numbers"""
        temp_num = random.randint(0, 36)
        color = "red" if temp_num in RED_NUMBERS else "black" if temp_num != 0 else "green"
        
        self.result_label.config(text=str(temp_num), fg=color)
        
        if count < max_counts:
            # Slow down as we get closer to the end
            delay = 50 + (count * 10) 
            self.root.after(delay, lambda: self.animate_wheel(count + 1, max_counts))
        else:
            self.resolve_spin()

    def resolve_spin(self):
        winning_number = random.randint(0, 36)
        winning_color = "red" if winning_number in RED_NUMBERS else "black"
        if winning_number == 0: winning_color = "green"

        self.result_label.config(text=f"{winning_number}", fg=winning_color)

        # Calculate Winnings
        total_won = 0
        
        for bet_target, bet_amt in self.current_bets.items():
            multiplier = 0
            
            # 1. Single Number Bets
            if bet_target.isdigit(): 
                if int(bet_target) == winning_number:
                    multiplier = 35 # + original bet returned separately below? 
                    # Standard casino logic: payout is 35:1. 
                    # If you win, you get 35*bet + your original bet.
                    # Since we deducted the bet from balance already, we add back (35+1) * bet
                    total_won += bet_amt * 36 

            # 2. Color Bets
            elif bet_target == "red" and winning_color == "red":
                total_won += bet_amt * 2
            elif bet_target == "black" and winning_color == "black":
                total_won += bet_amt * 2
            
            # 3. Even/Odd
            elif bet_target == "even" and winning_number != 0 and winning_number % 2 == 0:
                total_won += bet_amt * 2
            elif bet_target == "odd" and winning_number % 2 != 0:
                total_won += bet_amt * 2

            # 4. Low/High
            elif bet_target == "low" and 1 <= winning_number <= 18:
                total_won += bet_amt * 2
            elif bet_target == "high" and 19 <= winning_number <= 36:
                total_won += bet_amt * 2

        # Update Balance
        self.balance += total_won
        
        # Show Result
        total_wager = sum(self.current_bets.values())
        net_change = total_won - total_wager
        
        result_msg = f"Result: {winning_number} ({winning_color.upper()})\n"
        if total_won > 0:
            result_msg += f"YOU WON ${total_won}!"
            self.balance_label.config(fg="#00ff00") # Flash Green
        else:
            result_msg += "No Wins."
            self.balance_label.config(fg="red") # Flash Red

        # Briefly flash the status label
        self.bet_info_label.config(text=result_msg, fg="yellow")
        
        # Reset for next round
        self.current_bets.clear()
        self.spin_btn.config(state="normal")
        self.root.after(2000, self.update_status) # Reset UI text after 2 sec
        self.root.after(2000, lambda: self.balance_label.config(fg=ACCENT_COLOR)) # Reset color

# --- Main Entry Point ---
if __name__ == "__main__":
    root = tk.Tk()
    game = RouletteGame(root)
    root.mainloop()