try:
    from scaledown import ScaleDown
    print("SUCCESS: Imported ScaleDown")
    sd = ScaleDown(api_key="test")
    print(f"Instance created: {sd}")
except ImportError as e:
    print(f"FAILED: {e}")
except Exception as e:
    print(f"ERROR during init: {e}")
