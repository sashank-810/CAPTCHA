import time
import matplotlib.pyplot as plt
import sys
import readline

def record_key_times():
    print("Type a 6-letter word and press Enter:")
    key_times = []
    word = ""

    def on_key_pressed(char):
        nonlocal word
        if len(word) < 6:
            key_times.append(time.time())
            word += char
        if len(word) == 6:
            return False  # Stop recording after 6 letters

    # Enable raw input mode
    sys.stdin = open('/dev/tty')
    for _ in range(6):
        char = sys.stdin.read(1)  # Read a single character
        on_key_pressed(char)
    
    return key_times, word

def compute_delays(key_times):
    return [key_times[i] - key_times[i - 1] for i in range(1, len(key_times))]

def plot_delays(delays, word):
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(delays) + 1), delays, marker='o', linestyle='-', color='b')
    plt.xlabel("Key Press Index")
    plt.ylabel("Time Delay (seconds)")
    plt.title(f"Time Delay Between Successive Key Presses for '{word}'")
    plt.grid(True)
    plt.show()

def main():
    key_times, word = record_key_times()
    if len(word) != 6:
        print("Invalid input. Please type exactly 6 letters.")
        return
    
    delays = compute_delays(key_times)
    plot_delays(delays, word)

if __name__ == "__main__":
    main()