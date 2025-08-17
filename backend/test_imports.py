#!/usr/bin/env python3
"""
Comprehensive API Import Test
"""
import sys
sys.path.append('.')

def test_critical_apis():
    print("🔍 TESTING CRITICAL API IMPORTS")
    print("=" * 40)
    
    tests = [
        ("Models", "from models import db, Patient, WoundCarePlan, SurgeryBooking, User, ImagingInvestigation"),
        ("Patients API", "from api.patients import bp"),
        ("Wound Care API", "from api.wound_care import bp"),
        ("Surgery Booking API", "from api.surgery_booking import bp"),
        ("Imaging Investigation API", "from api.imaging_investigation import bp"),
    ]
    
    results = []
    
    for name, import_cmd in tests:
        try:
            exec(import_cmd)
            print(f"✅ {name}: SUCCESS")
            results.append(True)
        except Exception as e:
            print(f"❌ {name}: FAILED - {str(e)}")
            results.append(False)
    
    print("\n" + "=" * 40)
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print(f"🎉 ALL TESTS PASSED! ({success_count}/{total_count})")
        print("✅ Ready for deployment!")
        return True
    else:
        print(f"⚠️  {success_count}/{total_count} tests passed")
        print("❌ Need to fix remaining issues")
        return False

if __name__ == "__main__":
    test_critical_apis()
