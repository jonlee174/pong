from datetime import datetime
import os
import pygame

def record_history(winning_score, losing_score):
    now_date = datetime.now().strftime("%m/%d/%Y")
    now_time = datetime.now().strftime("%I:%M%p")
    with open(os.path.join("data", "history.txt"), "a") as f:
        f.write(f"The score was {winning_score}-{losing_score} on {now_date} at {now_time}\n")
