import scaledown
import inspect

print("ScaleDown module dir:", dir(scaledown))

if hasattr(scaledown, 'ScaleDown'):
    print("\nScaleDown class found.")
    cls = scaledown.ScaleDown
    print("Init signature:", inspect.signature(cls.__init__))
    print("Class methods:", dir(cls))
else:
    print("\nScaleDown class NOT found in module.")
