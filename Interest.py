import time

SECOND_IN_DAY = 86400

def calc_catch_up(balance, rate, last_time):
    now = time.time()
    elapsed_seconds = now - last_time

    elapsed_days = elapsed_seconds // SECOND_IN_DAY

    if elapsed_days > 0:
        new_balance =  balance * (1 + rate) ** elapsed_days

        new_time = last_time + (elapsed_days * SECOND_IN_DAY)

        return new_balance, new_time, elapsed_days
    return balance, last_time, 0