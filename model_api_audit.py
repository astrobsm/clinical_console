#!/usr/bin/env python3
"""
Model-API Compatibility Audit for Clinical Console
"""
import os
import re

def audit_model_api_compatibility():
    """Audit all models and their corresponding APIs for field mismatches"""
    
    print("🔍 MODEL-API COMPATIBILITY AUDIT")
    print("=" * 80)
    
    # Define model fields based on models.py analysis
    model_fields = {
        'Patient': {
            'fields': ['id', 'name', 'dob', 'gender', 'inpatient', 'created_at', 'consultant_id'],
            'table_name': 'patient'
        },
        'Appointment': {
            'fields': ['id', 'patient_id', 'scheduled_by', 'appointment_date', 'appointment_type', 'status', 'notes', 'created_at'],
            'table_name': 'appointment'
        },
        'ClinicalEvaluation': {
            'fields': ['id', 'patient_id', 'summary', 'date'],
            'table_name': 'clinicalevaluation'
        },
        'Diagnosis': {
            'fields': ['id', 'patient_id', 'diagnosis', 'date'],
            'table_name': 'diagnosis'
        },
        'TreatmentPlan': {
            'fields': ['id', 'patient_id', 'treatment', 'date'],
            'table_name': 'treatment'
        },
        'LabInvestigation': {
            'fields': ['id', 'patient_id', 'investigation', 'result', 'date'],
            'table_name': 'labinvestigation'
        },
        'ImagingInvestigation': {
            'fields': ['id', 'patient_id', 'investigation', 'finding', 'date'],
            'table_name': 'imaginginvestigation'
        },
        'WoundCarePlan': {
            'fields': ['id', 'patient_id', 'care_given', 'date'],
            'table_name': 'wound_care'
        },
        'SurgeryBooking': {
            'fields': ['id', 'patient_id', 'surgery_type', 'date', 'purpose'],
            'table_name': 'surgerybooking'
        },
        'Notification': {
            'fields': ['id', 'user_id', 'message', 'is_read', 'created_at'],
            'table_name': 'notification'
        },
        'AcademicEvent': {
            'fields': ['id', 'title', 'description', 'event_date', 'moderator_id', 'presenter_id', 'created_at'],
            'table_name': 'academicevent'
        },
        'Assessment': {
            'fields': ['id', 'user_id', 'assessment_type', 'score', 'responses', 'created_at'],
            'table_name': 'assessment'
        },
        'CBTQuestion': {
            'fields': ['id', 'diagnosis', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'option_e', 'correct_option'],
            'table_name': 'cbtquestion'
        },
        'Discharge': {
            'fields': ['id', 'patient_id', 'discharge_date', 'follow_up_date', 'discharge_summary', 'created_at'],
            'table_name': 'discharge'
        },
        'DischargeSummary': {
            'fields': ['id', 'patient_id', 'summary_text', 'created_at'],
            'table_name': 'dischargesummary'
        },
        'Score': {
            'fields': ['id', 'user_id', 'assessment_id', 'value', 'percentage', 'recommendation', 'advice', 'created_at'],
            'table_name': 'score'
        }
    }
    
    # API files to check
    api_files = [
        'patients.py',
        'appointment.py', 
        'clinical.py',
        'diagnosis.py',
        'treatment.py',
        'lab_investigation.py',
        'imaging_investigation.py',
        'wound_care.py',
        'surgery_booking.py',
        'assessments.py',
        'academic_event.py',
        'cbt_question.py'
    ]
    
    issues_found = []
    
    for api_file in api_files:
        api_path = f"backend/api/{api_file}"
        if os.path.exists(api_path):
            print(f"\n📁 Checking: {api_file}")
            
            with open(api_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract field references from the API file
            # Look for patterns like 'p.field_name' or 'obj.field_name'
            field_references = re.findall(r'[a-zA-Z_]\w*\.([a-zA-Z_]\w*)', content)
            field_references = list(set(field_references))  # Remove duplicates
            
            # Extract JSON field names from return statements
            json_fields = re.findall(r"'([a-zA-Z_]\w*)'\s*:", content)
            json_fields = list(set(json_fields))
            
            all_fields = list(set(field_references + json_fields))
            
            print(f"   Fields referenced: {sorted(all_fields)}")
            
            # Try to match with models
            for model_name, model_info in model_fields.items():
                model_fields_set = set(model_info['fields'])
                api_fields_set = set([f for f in all_fields if f not in ['get', 'query', 'all', 'isoformat', 'json', 'session']])
                
                # Check for mismatches
                missing_in_model = api_fields_set - model_fields_set
                if missing_in_model and len(missing_in_model) > 0:
                    # Check if this API might be for this model
                    common_fields = api_fields_set & model_fields_set
                    if len(common_fields) > 2:  # If more than 2 fields match, likely the same model
                        print(f"   ⚠️  Potential {model_name} API - Missing fields in model: {sorted(missing_in_model)}")
                        issues_found.append({
                            'api_file': api_file,
                            'model': model_name,
                            'missing_fields': sorted(missing_in_model),
                            'type': 'missing_in_model'
                        })
        else:
            print(f"\n❌ API file not found: {api_path}")
    
    # Check for common problematic patterns
    print(f"\n🔍 Checking for common problematic patterns...")
    
    problematic_patterns = [
        ('date_registered', 'Should be created_at'),
        ('senior_registrar_id', 'Field does not exist in Patient model'),
        ('registrar_id', 'Field does not exist in Patient model'),
        ('house_officer_id', 'Field does not exist in Patient model'),
        ('purpose', 'Check if field exists in model'),
        ('date', 'Check if should be appointment_date, event_date, etc.')
    ]
    
    for api_file in api_files:
        api_path = f"backend/api/{api_file}"
        if os.path.exists(api_path):
            with open(api_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            for pattern, issue in problematic_patterns:
                if pattern in content:
                    print(f"   ⚠️  {api_file}: Found '{pattern}' - {issue}")
                    issues_found.append({
                        'api_file': api_file,
                        'pattern': pattern,
                        'issue': issue,
                        'type': 'problematic_pattern'
                    })
    
    print(f"\n" + "=" * 80)
    print(f"🎯 AUDIT SUMMARY")
    print(f"Files checked: {len(api_files)}")
    print(f"Issues found: {len(issues_found)}")
    
    if issues_found:
        print(f"\n📋 ISSUES TO FIX:")
        for i, issue in enumerate(issues_found, 1):
            if issue['type'] == 'missing_in_model':
                print(f"{i}. {issue['api_file']} (Model: {issue['model']})")
                print(f"   Missing fields: {', '.join(issue['missing_fields'])}")
            elif issue['type'] == 'problematic_pattern':
                print(f"{i}. {issue['api_file']}")
                print(f"   Pattern: {issue['pattern']} - {issue['issue']}")
    else:
        print(f"\n✅ No obvious compatibility issues found!")
    
    print(f"=" * 80)
    
    return issues_found

if __name__ == "__main__":
    audit_model_api_compatibility()
