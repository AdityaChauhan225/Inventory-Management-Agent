from scaledown import ScaleDown
import inspect

try:
    print(f"Signature: {inspect.signature(ScaleDown.__init__)}")
except Exception as e:
    print(f"Error: {e}")
