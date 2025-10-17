# input_timeout.py (macOS/Linux version)
#
# Replaces the Windows-specific msvcrt with termios/tty/select
# to achieve non-blocking keyboard input with a timeout.

import sys
import time
import select
import tty
import termios


def readInput(timeout=1):
    start_time = time.time()
    input_str = ""

    # Get the file descriptor for standard input (the keyboard)
    fd = sys.stdin.fileno()
    # Save the current terminal settings so we can restore them later
    old_settings = termios.tcgetattr(fd)

    try:
        # Set the terminal to 'cbreak' mode.
        # This allows us to read characters immediately without waiting for Enter,
        # and disables local echo (we must echo characters manually).
        tty.setcbreak(fd)

        while True:
            # Use select to check if there is data on stdin (kbhit equivalent).
            # We use a 0 timeout to poll instantly.
            rlist, _, _ = select.select([sys.stdin], [], [], 0)

            if rlist:
                # Read exactly one character
                char = sys.stdin.read(1)

                # Check for Enter (newline or carriage return)
                if char == "\n" or char == "\r":
                    break
                # Check for Backspace (often DEL / \x7f on macOS)
                elif char == "\x7f" or char == "\b":
                    if len(input_str) > 0:
                        input_str = input_str[:-1]
                        # Move cursor back, print a space to erase, move back again
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                else:
                    # Add the character to our string
                    input_str += char
                    # Manually echo the character to the screen
                    sys.stdout.write(char)
                    sys.stdout.flush()

            # Check if the timeout has expired AND the user hasn't started typing yet.
            if len(input_str) == 0 and (time.time() - start_time) > timeout:
                break

            # Small sleep to prevent this loop from using 100% CPU while waiting
            time.sleep(0.01)

    finally:
        # CRITICAL: Restore the original terminal settings.
        # If this doesn't run, the user's terminal will be broken.
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    # Print a newline because pressing Enter in cbreak mode doesn't produce one on screen
    print("")

    if len(input_str) > 0:
        return input_str
    else:
        return ""
