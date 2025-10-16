-- Intermediate: Diagnoses with patient and appointment context
with diagnoses as (
    select * from {{ ref('stg_diagnoses') }}
),

patient_visits as (
    select * from {{ ref('int_patient_visits') }}
),

enriched as (
    select
        diagnoses.diagnosis_id,
        diagnoses.diagnosis_code,
        diagnoses.diagnosis_name,
        diagnoses.severity,
        diagnoses.diagnosis_date,
        diagnoses.notes,
        
        -- From patient visits
        patient_visits.appointment_id,
        patient_visits.patient_id,
        patient_visits.patient_name,
        patient_visits.patient_age,
        patient_visits.gender,
        patient_visits.doctor_id,
        patient_visits.doctor_name,
        patient_visits.specialty,
        patient_visits.hospital_name
        
    from diagnoses
    left join patient_visits on diagnoses.appointment_id = patient_visits.appointment_id
)

select * from enriched

