# Write your code here :-)
import time
import sys

import simpletest_monooled

# print("WARNING: main.py not ready yet", file=sys.stderr)
# sys.exit(0)

screen = simpletest_monooled.screen()

while True:
    screen.drew_logo()
    time.sleep(10)
    # time.sleep(2.0)
    # screen.splash()
    # time.sleep(2.0)
    # screen.origin()
    # time.sleep(2.0)
    screen.hello()
    time.sleep(2.0)
