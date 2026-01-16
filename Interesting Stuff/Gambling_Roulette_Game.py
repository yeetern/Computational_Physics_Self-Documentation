import random
import math

# ============================================================
# 1. Roulette Game Definitions
# ============================================================

# Standard roulette red numbers (European & American same colors)
RED_NUMBERS = {
    1, 3, 5, 7, 9,
    12, 14, 16, 18,
    19, 21, 23, 25, 27,
    30, 32, 34, 36
}
# Black numbers are all 2–36 that are not red; 0 and 00 are green

class FairRoulette:
    """
    Idealized fair roulette:
    - Pockets 1–36
    - If you hit the exact pocket, you win 35× your bet (net +35)
    - Otherwise you lose your bet (net -1)
    """
    def __init__(self):
        self.pockets = [i for i in range(1, 37)]
        self.ball = None
        self.pocketOdds = len(self.pockets) - 1  # 35:1

    # ---------- Core mechanics ----------
    def spin(self):
        self.ball = random.choice(self.pockets)

    def betPocket(self, pocket, amt):
        """
        Simple single-number bet (for compatibility with old code).
        """
        if str(pocket) == str(self.ball):
            return amt * self.pocketOdds
        else:
            return -amt

    # ---------- General bet evaluator ----------
    def bet_general(self, bet_type, selection, amt):
        """
        Evaluate arbitrary bets.

        Parameters
        ----------
        bet_type : str
            One of:
              'single', 'double', 'triple', 'quad',
              'five', 'six',
              'dozen', 'column',
              'low', 'high',
              'red', 'black',
              'odd', 'even'
        selection : varies
            - single: int (e.g. 17)
            - double/triple/quad/six: iterable of ints (numbers)
            - five: ignored here (only meaningful in American); we handle
              it in subclass but keep interface consistent
            - dozen: 1, 2, or 3 (1–12, 13–24, 25–36)
            - column: 1, 2, or 3 (first/second/third column)
            - low/high/red/black/odd/even: selection ignored
        amt : float
            Bet size

        Returns
        -------
        net_win : float
            +amt * odds if win, else -amt
        """
        # Odds table from your image
        odds_table = {
            "single": 35,
            "double": 17,
            "triple": 11,
            "quad":   8,
            "five":   6,
            "six":    5,
            "dozen":  2,
            "column": 2,
            "low":    1,
            "high":   1,
            "red":    1,
            "black":  1,
            "odd":    1,
            "even":   1,
        }

        if bet_type not in odds_table:
            raise ValueError(f"Unknown bet_type: {bet_type}")

        odds = odds_table[bet_type]

        # Convert ball to int when possible; 0 or 00 stay as strings
        ball = self.ball
        ball_int = None
        if isinstance(ball, int):
            ball_int = ball
        else:
            try:
                ball_int = int(ball)
            except (TypeError, ValueError):
                ball_int = None  # '00' will end up here

        win = False

        # ---------- Map bet types to winning sets ----------
        if bet_type == "single":
            win = (ball_int == selection)

        elif bet_type in ("double", "triple", "quad", "six"):
            # selection should be an iterable of ints
            winning_numbers = set(selection)
            win = (ball_int in winning_numbers)

        elif bet_type == "five":
            # Only real for American roulette -> override there.
            # Here, we just say it never wins.
            win = False

        elif bet_type == "dozen":
            # selection = 1 (1–12), 2 (13–24), 3 (25–36)
            if selection == 1:
                winning_numbers = set(range(1, 13))
            elif selection == 2:
                winning_numbers = set(range(13, 25))
            elif selection == 3:
                winning_numbers = set(range(25, 37))
            else:
                raise ValueError("dozen selection must be 1, 2, or 3")
            win = (ball_int in winning_numbers)

        elif bet_type == "column":
            # selection = 1,2,3 for 1st, 2nd, 3rd column
            if ball_int is None:
                win = False
            else:
                col = (ball_int - 1) % 3 + 1  # 1..3
                win = (col == selection)

        elif bet_type == "low":
            # 1–18
            win = (ball_int is not None and 1 <= ball_int <= 18)

        elif bet_type == "high":
            # 19–36
            win = (ball_int is not None and 19 <= ball_int <= 36)

        elif bet_type == "red":
            win = (ball_int in RED_NUMBERS)

        elif bet_type == "black":
            win = (ball_int is not None and
                   1 <= ball_int <= 36 and
                   ball_int not in RED_NUMBERS)

        elif bet_type == "odd":
            win = (ball_int is not None and ball_int % 2 == 1)

        elif bet_type == "even":
            win = (ball_int is not None and ball_int % 2 == 0 and ball_int != 0)

        # Note: 0 or 00 automatically lose for all even-money bets,
        # which is exactly how casinos earn their edge.

        return amt * odds if win else -amt

    def __str__(self):
        return "Fair Roulette"


class EuRoulette(FairRoulette):
    """
    European roulette:
    - Pockets 1–36 + single '0'
    - Pays 35:1 on single-number -> negative expectation.
    """
    def __init__(self):
        super().__init__()
        self.pockets.append('0')  # now 37 pockets
        self.pocketOdds = 35

    def __str__(self):
        return "European Roulette"


class AmRoulette(FairRoulette):
    """
    American roulette:
    - Pockets 1–36 + '0' + '00'
    - Pays 35:1 on single-number -> even worse odds.
    """
    def __init__(self):
        super().__init__()
        self.pockets.append('0')
        self.pockets.append('00')  # now 38 pockets
        self.pocketOdds = 35

    # Override general bet to implement real five-number bet: 0-00-1-2-3
    def bet_general(self, bet_type, selection, amt):
        if bet_type == "five":
            odds = 6  # 6:1 from your table
            # Success if ball is 0, 00, 1, 2, or 3
            ball_str = str(self.ball)
            win = ball_str in {"0", "00", "1", "2", "3"}
            return amt * odds if win else -amt
        # Everything else same as parent
        return super().bet_general(bet_type, selection, amt)

    def __str__(self):
        return "American Roulette"


# ============================================================
# 2. Core Monte Carlo Helpers (Existing Data Scientist Part)
# ============================================================

def playRoulette(game, numSpins, pocket, bet, toPrint=False):
    """
    Original helper: single-number bet on 'pocket'.
    """
    totReturn = 0.0
    for _ in range(numSpins):
        game.spin()
        totReturn += game.betPocket(pocket, bet)
    meanReturn = totReturn / numSpins

    if toPrint:
        print(f"{numSpins} spins of", game)
        print("Average return per spin:", meanReturn)
    return meanReturn


def playRoulette_general(game, numSpins, bet_type, selection, bet, toPrint=False):
    """
    NEW helper for arbitrary bet types using bet_general().
    Returns average net return per spin.
    """
    totReturn = 0.0
    for _ in range(numSpins):
        game.spin()
        totReturn += game.bet_general(bet_type, selection, bet)
    meanReturn = totReturn / numSpins

    if toPrint:
        print(f"{numSpins} spins of", game,
              "| bet_type:", bet_type, "| selection:", selection)
        print("Average return per spin:", meanReturn)
    return meanReturn


def findPocketReturn(game, numTrials, numSpins, toPrint=False,
                     pocket=2, bet=1):
    """
    OLD: many experiments for single-pocket bet.
    """
    returns = []
    for _ in range(numTrials):
        mean_ret = playRoulette(game, numSpins, pocket, bet, toPrint=False)
        returns.append(mean_ret)
    if toPrint:
        print(f"Finished {numTrials} trials of {numSpins} spins each.")
        print("Example returns:", returns[:5], "...\n")
    return returns


def getMeanAndStd(values):
    """
    Compute sample mean and sample standard deviation.
    """
    n = len(values)
    mean = sum(values) / n
    var = sum((x - mean) ** 2 for x in values) / (n - 1)
    std = math.sqrt(var)
    return mean, std


# ============================================================
# 3. Example Empirical-Rule Experiment with General Bets
# ============================================================

if __name__ == "__main__":

    numTrials = 20
    spin_options = (100, 1000)   # keep short for demo
    games = (FairRoulette, EuRoulette, AmRoulette)

    # Choose a bet to study: change this for experiments
    bet_type = "red"        # e.g. 'single', 'double', 'dozen', 'column', 'odd', ...
    selection = None        # None for red/black/low/high/odd/even
    bet_size = 1

    print(f"\n=== Studying bet_type='{bet_type}', selection={selection}, bet={bet_size} ===")

    for numSpins in spin_options:
        print("\nSimulate", numTrials, "trials of", numSpins,
              "spins each for this bet type")

        for G in games:
            game_instance = G()
            returns = []
            for _ in range(numTrials):
                mean_ret = playRoulette_general(
                    game_instance,
                    numSpins=numSpins,
                    bet_type=bet_type,
                    selection=selection,
                    bet=bet_size,
                    toPrint=False
                )
                returns.append(mean_ret)

            mean, std = getMeanAndStd(returns)
            ci_half = 1.96 * std

            print(
                "Exp. return for", game_instance, "≈",
                str(round(100 * mean, 3)) + "%,",
                "+/-", str(round(100 * ci_half, 3)) + "%  (95% CI)"
            )
