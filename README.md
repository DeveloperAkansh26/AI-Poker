AI Poker is a Python-based poker game that simulates a full poker environment enhanced by AI-driven decision-making. The project includes essential poker functionalities such as card management, hand evaluation, game logic, and a dynamic AI model that adapts its strategy based on the current game state.
Features

    Game Logic: Implements standard poker rules and game flow.

    Hand Evaluation: Determines winning hands using robust evaluation logic.

    AI Players: Utilizes AI techniques, including Monte Carlo simulations, to simulate intelligent decision-making during gameplay.

How It Works

The core AI logic is implemented in the model.py file and revolves around an AI player class (MyPlayer) that makes decisions by analyzing the game state and simulating outcomes. Here's a breakdown:
Dynamic Decision-Making

    Game State Analysis:
    The AI evaluates the community cards at different stages (flop, turn) to determine hand strength using a hand evaluator. If the hand rank is high (value ≥ 4), it switches to an "aggressive" mode, opting for larger raises.

    Action Selection:
    Depending on its evaluation, the AI decides whether to:

        Fold: When the hand is weak.

        Call: Especially if multiple opponents have raised during the same phase.

        Raise/All-In: Based on its current stack and a dynamic threshold that adjusts between "normal" and "aggressive" states.

Monte Carlo Simulation for Win Estimation

    Simulating Unknown Cards:
    The AI performs Monte Carlo simulations to estimate its chance of winning. It does this by:

        Constructing a Partial Deck: Excluding known cards from a full deck.

        Completing the Board: Randomly selecting cards to fill in missing community cards.

        Dealing Opponents’ Hands: Randomly assigning hole cards to simulate the opponents’ hands.

    Outcome Evaluation:
    Each simulation compares the AI’s hand against the simulated opponents’ best hands. By averaging the results over many simulations, the AI computes an estimated win rate to guide its betting strategy.
