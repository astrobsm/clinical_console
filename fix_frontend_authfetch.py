#!/usr/bin/env python3
"""
Comprehensive Frontend authFetch Fix Script
Fixes all instances where components treat authFetch as raw fetch response
"""
import os
import re

def fix_file(filepath, content):
    """Fix authFetch usage patterns in a file"""
    original_content = content
    
    # Pattern 1: const res = await authFetch(...); const data = await res.json();
    pattern1 = re.compile(
        r'(\s*)(const\s+res\s*=\s*await\s+authFetch\([^)]+\);)\s*\n\s*(const\s+data\s*=\s*await\s+res\.json\(\);)',
        re.MULTILINE
    )
    content = pattern1.sub(r'\1const data = await authFetch\(\2', content)
    
    # Pattern 2: if (res.ok) setItems(data); -> if (data) setItems(data);
    pattern2 = re.compile(r'if\s*\(\s*res\.ok\s*\)', re.MULTILINE)
    content = pattern2.sub('if (data)', content)
    
    # Pattern 3: else setError(data.msg || 'message'); -> else setError('message');
    pattern3 = re.compile(r'else\s+setError\(data\.msg\s*\|\|\s*([^)]+)\);', re.MULTILINE)
    content = pattern3.sub(r'else setError(\1);', content)
    
    return content, content != original_content

def main():
    """Fix all frontend files with authFetch issues"""
    
    files_to_fix = [
        'frontend/src/pages/SurgeryBooking.js',
        'frontend/src/pages/Score.js', 
        'frontend/src/pages/Notifications.js',
        'frontend/src/pages/DischargeSummary.js',
        'frontend/src/pages/Discharge.js',
        'frontend/src/pages/CBTQuestion.js'
    ]
    
    base_path = r'c:\Users\USER\Documents\Medical practice\BPRS UNTH\plasticunth'
    
    print("🔧 FIXING FRONTEND authFetch USAGE")
    print("=" * 50)
    
    for file_path in files_to_fix:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content, changed = fix_file(file_path, content)
            
            if changed:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Fixed: {file_path}")
            else:
                print(f"ℹ️  No changes needed: {file_path}")
        else:
            print(f"❌ File not found: {file_path}")
    
    print("\n🎯 SUMMARY:")
    print("- Fixed authFetch patterns in all affected files")
    print("- Changed 'const res = await authFetch(); const data = await res.json();'")
    print("- To 'const data = await authFetch();'")
    print("- Updated error handling patterns")
    
    print("\n🔍 NEXT STEPS:")
    print("1. Test Clinical Evaluations patient dropdown")
    print("2. Verify other forms load data correctly")
    print("3. Check for any remaining console errors")

if __name__ == "__main__":
    main()
