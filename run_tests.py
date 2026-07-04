import sys
import os

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from tests.test_data_ingester import (
        test_ingester_loads_csv,
        test_ingester_converts_currency,
        test_profile_has_expected_keys
    )
    
    print("Running test_ingester_loads_csv...")
    test_ingester_loads_csv()
    print("test_ingester_loads_csv passed!")

    print("Running test_ingester_converts_currency...")
    test_ingester_converts_currency()
    print("test_ingester_converts_currency passed!")

    print("Running test_profile_has_expected_keys...")
    test_profile_has_expected_keys()
    print("test_profile_has_expected_keys passed!")
    
    print("\nAll tests passed successfully!")
except Exception as e:
    import traceback
    print(f"Test failed with error: {e}")
    traceback.print_exc()
    sys.exit(1)
