-- Staging: Clean diagnosis data
with source as (
    select * from {{ source('hospital_raw', 'raw_diagnoses') }}
),

cleaned as (
    select
        diagnosis_id,
        appointment_id,
        patient_id,
        doctor_id,
        diagnosis_code,
        diagnosis_name,
        severity,
        diagnosis_date::date as diagnosis_date,
        notes,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

