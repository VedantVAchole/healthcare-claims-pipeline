import random
import csv
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
random.seed(42)
Faker.seed(42)

print("Starting healthcare data generation...")

# ICD-10 Diagnosis Codes (50 common diagnoses)
ICD_CODES = [
    {'code': 'E11.9', 'name': 'Type 2 Diabetes Mellitus', 'category': 'Diabetes', 'severity': 'MODERATE', 'avg_cost': 2500},
    {'code': 'I25.10', 'name': 'Coronary Artery Disease', 'category': 'Heart Disease', 'severity': 'HIGH', 'avg_cost': 35000},
    {'code': 'J44.9', 'name': 'COPD', 'category': 'Respiratory', 'severity': 'MODERATE', 'avg_cost': 5000},
    {'code': 'I10', 'name': 'Hypertension', 'category': 'Heart Disease', 'severity': 'MODERATE', 'avg_cost': 1500},
    {'code': 'E78.5', 'name': 'Hyperlipidemia', 'category': 'Metabolic', 'severity': 'LOW', 'avg_cost': 800},
    {'code': 'M17.9', 'name': 'Osteoarthritis of Knee', 'category': 'Musculoskeletal', 'severity': 'MODERATE', 'avg_cost': 4000},
    {'code': 'F41.1', 'name': 'Generalized Anxiety Disorder', 'category': 'Mental Health', 'severity': 'MODERATE', 'avg_cost': 3000},
    {'code': 'C50.9', 'name': 'Breast Cancer', 'category': 'Cancer', 'severity': 'CRITICAL', 'avg_cost': 85000},
    {'code': 'N18.3', 'name': 'Chronic Kidney Disease', 'category': 'Kidney', 'severity': 'HIGH', 'avg_cost': 45000},
    {'code': 'J45.909', 'name': 'Asthma', 'category': 'Respiratory', 'severity': 'MODERATE', 'avg_cost': 2200},
]

print(f"Loaded {len(ICD_CODES)} diagnosis codes")

# Generate one patient
def generate_patient(patient_id_num):
    """Generate a single patient record"""
    
    age = random.randint(18, 85)
    
    # Chronic conditions - older patients more likely to have them
    chronic_conditions = []
    if age > 60:
        chronic_conditions = random.choices(
            ['Diabetes', 'Hypertension', 'Heart Disease', 'None'],
            weights=[0.3, 0.4, 0.2, 0.1],
            k=1
        )
    elif age > 40:
        chronic_conditions = random.choices(
            ['Diabetes', 'Hypertension', 'None'],
            weights=[0.2, 0.3, 0.5],
            k=1
        )
    else:
        chronic_conditions = ['None']
    
    return {
        'patient_id': f"PAT{patient_id_num:05d}",
        'age': age,
        'gender': random.choice(['M', 'F']),
        'state': fake.state_abbr(),
        'zip_code': fake.zipcode(),
        'insurance_plan': random.choice(['BRONZE', 'SILVER', 'GOLD', 'PLATINUM']),
        'chronic_conditions': chronic_conditions[0],
        'member_since_date': fake.date_between(start_date='-5y', end_date='today')
    }

print("Patient generation function defined")

# Medical specialties
SPECIALTIES = [
    'Cardiology', 'Orthopedics', 'Endocrinology', 'Pulmonology',
    'Oncology', 'Neurology', 'Gastroenterology', 'Primary Care',
    'Psychiatry', 'Dermatology'
]

# Generate one provider
def generate_provider(provider_id_num):
    """Generate a single provider (doctor/hospital) record"""
    
    provider_type = random.choice(['PHYSICIAN', 'HOSPITAL', 'PHARMACY'])
    
    if provider_type == 'PHYSICIAN':
        provider_name = f"Dr. {fake.name()}"
        specialty = random.choice(SPECIALTIES)
        years_experience = random.randint(3, 35)
        hospital_name = None
    elif provider_type == 'HOSPITAL':
        provider_name = f"{fake.city()} Medical Center"
        specialty = random.choice(SPECIALTIES)
        years_experience = random.randint(10, 50)
        hospital_name = provider_name
    else:  # PHARMACY
        provider_name = f"{fake.company()} Pharmacy"
        specialty = 'Pharmacy'
        years_experience = random.randint(5, 30)
        hospital_name = None
    
    return {
        'provider_id': f"PRV{provider_id_num:05d}",
        'provider_name': provider_name,
        'specialty': specialty,
        'provider_type': provider_type,
        'state': fake.state_abbr(),
        'city': fake.city(),
        'hospital_name': hospital_name,
        'years_experience': years_experience,
        'network_tier': random.choices(
            ['IN_NETWORK', 'OUT_OF_NETWORK'],
            weights=[0.8, 0.2],
            k=1
        )[0]
    }

print("Provider generation function defined")


# Claim types
CLAIM_TYPES = ['INPATIENT', 'OUTPATIENT', 'PHARMACY']

# Generate one claim
def generate_claim(claim_id_num, patient_ids, provider_ids):
    """Generate a single insurance claim record"""
    
    # Random patient and provider
    patient_id = random.choice(patient_ids)
    provider_id = random.choice(provider_ids)
    
    # Random diagnosis
    diagnosis = random.choice(ICD_CODES)
    
    # Service date (within last 3 months)
    service_date = fake.date_between(start_date='-3M', end_date='today')
    
    # Claim date (1-10 days after service)
    days_to_file = random.randint(1, 10)
    claim_date = service_date + timedelta(days=days_to_file)
    
    # Claim amount based on diagnosis severity
    base_cost = diagnosis['avg_cost']
    variation = random.uniform(0.7, 1.3)  # +/- 30% variation
    claim_amount = round(base_cost * variation, 2)
    
    # Allowed amount (insurance negotiated rate - usually 90-95% of billed)
    allowed_amount = round(claim_amount * random.uniform(0.90, 0.95), 2)
    
    # Patient responsibility (deductible + copay - usually 10-30% of allowed)
    patient_responsibility = round(allowed_amount * random.uniform(0.10, 0.30), 2)
    
    # Claim status (most approved, some denied, few pending)
    claim_status = random.choices(
        ['APPROVED', 'DENIED', 'PENDING'],
        weights=[0.85, 0.10, 0.05],
        k=1
    )[0]
    
    # Procedure code (simplified - using diagnosis code as proxy)
    procedure_code = f"CPT{random.randint(10000, 99999)}"
    
    # Claim type
    claim_type = random.choice(CLAIM_TYPES)
    
    return {
        'claim_id': f"CLM{claim_id_num:06d}",
        'patient_id': patient_id,
        'provider_id': provider_id,
        'diagnosis_code': diagnosis['code'],
        'service_date': service_date.strftime('%Y-%m-%d'),
        'claim_date': claim_date.strftime('%Y-%m-%d'),
        'claim_amount': claim_amount,
        'allowed_amount': allowed_amount,
        'patient_responsibility': patient_responsibility,
        'claim_status': claim_status,
        'procedure_code': procedure_code,
        'claim_type': claim_type
    }

print("Claim generation function defined")

# Main execution
def main():
    """Generate all healthcare data and save to CSV files"""
    
    print("\n" + "="*50)
    print("HEALTHCARE DATA GENERATION STARTED")
    print("="*50 + "\n")
    
    # Step 1: Generate ICD codes CSV
    print("Step 1/4: Generating diagnosis codes...")
    with open('../data/icd_codes.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['code', 'name', 'category', 'severity', 'avg_cost'])
        writer.writeheader()
        writer.writerows(ICD_CODES)
    print(f"✓ Generated {len(ICD_CODES)} diagnosis codes\n")
    
    # Step 2: Generate patients
    print("Step 2/4: Generating patients...")
    patients = []
    for i in range(1, 1001):  # 1000 patients
        patients.append(generate_patient(i))
        if i % 200 == 0:  # Progress update every 200
            print(f"  Generated {i} patients...")
    
    with open('../data/patients.csv', 'w', newline='') as f:
        fieldnames = ['patient_id', 'age', 'gender', 'state', 'zip_code', 
                     'insurance_plan', 'chronic_conditions', 'member_since_date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(patients)
    print(f"✓ Generated {len(patients)} patients\n")
    
    # Step 3: Generate providers
    print("Step 3/4: Generating providers...")
    providers = []
    for i in range(1, 201):  # 200 providers
        providers.append(generate_provider(i))
        if i % 50 == 0:
            print(f"  Generated {i} providers...")
    
    with open('../data/providers.csv', 'w', newline='') as f:
        fieldnames = ['provider_id', 'provider_name', 'specialty', 'provider_type',
                     'state', 'city', 'hospital_name', 'years_experience', 'network_tier']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(providers)
    print(f"✓ Generated {len(providers)} providers\n")
    
    # Step 4: Generate claims
    print("Step 4/4: Generating claims...")
    patient_ids = [p['patient_id'] for p in patients]
    provider_ids = [p['provider_id'] for p in providers]
    
    claims = []
    for i in range(1, 10001):  # 10,000 claims
        claims.append(generate_claim(i, patient_ids, provider_ids))
        if i % 2000 == 0:
            print(f"  Generated {i} claims...")
    
    with open('../data/claims.csv', 'w', newline='') as f:
        fieldnames = ['claim_id', 'patient_id', 'provider_id', 'diagnosis_code',
                     'service_date', 'claim_date', 'claim_amount', 'allowed_amount',
                     'patient_responsibility', 'claim_status', 'procedure_code', 'claim_type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(claims)
    print(f"✓ Generated {len(claims)} claims\n")
    
    # Summary
    print("="*50)
    print("DATA GENERATION COMPLETE!")
    print("="*50)
    print(f"Files created in ../data/ folder:")
    print(f"  - icd_codes.csv ({len(ICD_CODES)} rows)")
    print(f"  - patients.csv ({len(patients)} rows)")
    print(f"  - providers.csv ({len(providers)} rows)")
    print(f"  - claims.csv ({len(claims)} rows)")
    print("\nReady to upload to S3!")

# Run the main function
if __name__ == "__main__":
    main()


