from scaledown import ScaleDown
import inspect

with open("inspect_optimize.txt", "w") as f:
    try:
        sig = inspect.signature(ScaleDown.optimize_with_pipeline)
        f.write(f"Signature: {sig}\n")
        f.write(f"Doc: {ScaleDown.optimize_with_pipeline.__doc__}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
