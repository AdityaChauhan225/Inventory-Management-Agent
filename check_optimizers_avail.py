import scaledown

try:
    compressor = scaledown.ScaleDown(enable_optimization_styles=True)
    optimizers = compressor.list_optimizers()
    print("Available Optimizers:", optimizers)
    
    # Also check if we can run optimize_with_pipeline
    if optimizers:
        print("\nTesting optimize_with_pipeline...")
        res = compressor.optimize_with_pipeline("This is a test prompt.", [optimizers[0]['id']])
        print("Test Result:", res)
    else:
        print("\nNo optimizers found.")

except Exception as e:
    print(f"Error: {e}")
