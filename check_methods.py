from scaledown import ScaleDown
import sys

with open("methods.txt", "w") as f:
    f.write(str(dir(ScaleDown)))
