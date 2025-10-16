-- Staging: Clean prescription data
with source as (
    select * from {{ source('hospital_raw', 'raw_prescriptions') }}
),

cleaned as (
    select
        prescription_id,
        appointment_id,
        patient_id,
        doctor_id,
        medication_id,
        dosage,
        frequency,
        duration_days,
        prescription_date::date as prescription_date,
        refills_allowed,
        status,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

