from scaledown import ScaleDown
import inspect

print("Please show full output:")
try:
    sig = inspect.signature(ScaleDown.__init__)
    print(f"Signature: {sig}")
except Exception as e:
    print(f"Could not get signature: {e}")

print("\nDocstring:")
print(ScaleDown.__doc__)
print("\nInit Docstring:")
print(ScaleDown.__init__.__doc__)
