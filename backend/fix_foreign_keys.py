#!/usr/bin/env python3
"""Fix foreign key references in models.py"""

with open('models.py', 'r') as f:
    content = f.read()

content = content.replace("ForeignKey('user.id')", "ForeignKey('clinical_users.id')")

with open('models.py', 'w') as f:
    f.write(content)

print('✓ Fixed all foreign key references')
