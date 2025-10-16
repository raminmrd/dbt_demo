-- Staging: Clean appointment data
with source as (
    select * from {{ source('hospital_raw', 'raw_appointments') }}
),

cleaned as (
    select
        appointment_id,
        patient_id,
        doctor_id,
        appointment_date::date as appointment_date,
        appointment_time::time as appointment_time,
        appointment_type,
        status,
        duration_minutes,
        hospital_id,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

