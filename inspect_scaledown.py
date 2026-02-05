import scaledown
import inspect

print("Attributes in scaledown module:")
for item in dir(scaledown):
    print(f"- {item}")

print("\nDetailed inspection of available classes:")
for name, obj in inspect.getmembers(scaledown):
    if inspect.isclass(obj):
        print(f"Class: {name}")
