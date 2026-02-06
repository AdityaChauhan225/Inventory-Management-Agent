import scaledown
import inspect

print("ScaleDown module dir:", [x for x in dir(scaledown) if not x.startswith("_")])

if hasattr(scaledown, 'ScaleDown'):
    print("\nScaleDown class found.")
    cls = scaledown.ScaleDown
    try:
        print("Init signature:", inspect.signature(cls.__init__))
    except ValueError:
        print("Init signature: (unknown, maybe C extension or built-in)")
    
    methods = [x for x in dir(cls) if not x.startswith("_")]
    print("Public Class methods:", methods)
else:
    print("\nScaleDown class NOT found in module.")
