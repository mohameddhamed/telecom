# input_timeout.py
#
# NOTE TO STUDENTS: This is a helper file for reading keyboard input without
# blocking the program. It is specific to Windows (`msvcrt`). You do not
# need to modify this file. It is provided so the client can check for
# server messages and keyboard input at the same time.
#

import msvcrt
import time
import sys


def readInput(timeout=1):
    start_time = time.time()
    input_str = ""
    while True:
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
            if ord(byte_arr) == 13:  # enter_key
                break
            elif ord(byte_arr) >= 32:  # space_char
                input_str += byte_arr.decode()
            elif ord(byte_arr) == 8:  # backspace_char
                input_str = input_str[:-1]
                # The following lines are for updating the console display
                # correctly after a backspace.
                sys.stdout.write("\r")
                sys.stdout.write(" " * (len(input_str) + 20))
                sys.stdout.write("\r")
                sys.stdout.write(input_str)
                sys.stdout.flush()

        if len(input_str) == 0 and (time.time() - start_time) > timeout:
            break

    if len(input_str) > 0:
        return input_str
    else:
        return ""
