#!/usr/bin/env python3
"""
Fix Critical Model-API Mismatches
"""
import os
import re

def fix_critical_mismatches():
    """Fix the most critical field mismatches that cause 500 errors"""
    
    print("🔧 FIXING CRITICAL MODEL-API MISMATCHES")
    print("=" * 60)
    
    fixes = []
    
    # Fix 1: date_registered -> created_at in Patient references
    api_files = [
        'backend/api/patients.py',
        'backend/api/imaging_investigation.py'
    ]
    
    for file_path in api_files:
        if os.path.exists(file_path):
            print(f"📝 Fixing {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Replace date_registered with created_at
            original_content = content
            content = content.replace('date_registered', 'created_at')
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ Fixed date_registered -> created_at")
                fixes.append(f"{file_path}: date_registered -> created_at")
            else:
                print(f"   ℹ️  No date_registered found")
    
    # Fix 2: Check for 'date' field in appointment.py (should use appointment_date)
    appointment_file = 'backend/api/appointment.py'
    if os.path.exists(appointment_file):
        print(f"📝 Checking {appointment_file}")
        
        with open(appointment_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if it's using 'a.date' instead of 'a.appointment_date'
        if 'a.date' in content and 'a.appointment_date' in content:
            print(f"   ✅ Already using correct appointment_date field")
        elif 'a.date' in content:
            print(f"   ⚠️  Found 'a.date' - may need manual review")
            # Don't auto-fix this as it might be correct
    
    # Fix 3: Check specific problematic patterns
    problematic_files = {
        'backend/api/wound_care.py': {
            'model_field': 'care_given',
            'check_pattern': r'care_given'
        },
        'backend/api/surgery_booking.py': {
            'model_field': 'surgery_type',
            'check_pattern': r'surgery_type'
        },
        'backend/api/lab_investigation.py': {
            'model_field': 'investigation',
            'check_pattern': r'investigation'
        }
    }
    
    for file_path, info in problematic_files.items():
        if os.path.exists(file_path):
            print(f"📝 Checking {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if re.search(info['check_pattern'], content):
                print(f"   ✅ Found expected field '{info['model_field']}'")
            else:
                print(f"   ⚠️  Missing expected field '{info['model_field']}'")
    
    print(f"\n" + "=" * 60)
    print(f"🎯 CRITICAL FIXES APPLIED: {len(fixes)}")
    
    for fix in fixes:
        print(f"   ✅ {fix}")
    
    if not fixes:
        print("   ℹ️  No critical fixes needed or already applied")
    
    print(f"\nNext steps:")
    print(f"1. Test the fixed APIs")
    print(f"2. Commit the changes")
    print(f"3. Deploy to production")
    print(f"=" * 60)
    
    return fixes

if __name__ == "__main__":
    fix_critical_mismatches()
