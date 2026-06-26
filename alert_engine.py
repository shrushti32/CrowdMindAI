import winsound

def play_alert():

    duration = 700
    freq = 1000

    winsound.Beep(freq, duration)