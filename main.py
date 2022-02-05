# Write your code here :-)
import time
import sys

import simpletest_monooled

print("WARNING: main.py not ready yet", file=sys.stderr)
sys.exit(0)

while True:
    screen = simpletest_monooled.screen()
    screen.drew_logo()
    time.sleep(2.0)
    screen.splash()
    time.sleep(2.0)
    screen.origin()
    time.sleep(2.0)
    screen.triangle()
    time.sleep(2.0)
