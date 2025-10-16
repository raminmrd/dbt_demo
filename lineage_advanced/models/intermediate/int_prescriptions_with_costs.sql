-- Intermediate: Enrich prescriptions with medication costs
with prescriptions as (
    select * from {{ ref('stg_prescriptions') }}
),

medications as (
    select * from {{ ref('stg_medications') }}
),

enriched as (
    select
        prescriptions.prescription_id,
        prescriptions.appointment_id,
        prescriptions.patient_id,
        prescriptions.doctor_id,
        prescriptions.medication_id,
        prescriptions.dosage,
        prescriptions.frequency,
        prescriptions.duration_days,
        prescriptions.prescription_date,
        prescriptions.refills_allowed,
        prescriptions.status,
        
        -- Medication details
        medications.medication_name,
        medications.generic_name,
        medications.drug_class,
        medications.manufacturer,
        medications.unit_cost,
        medications.requires_prescription,
        
        -- Cost calculations
        medications.unit_cost * prescriptions.duration_days as estimated_cost
        
    from prescriptions
    left join medications on prescriptions.medication_id = medications.medication_id
)

select * from enriched

