-- Staging: Clean doctor/provider data
with source as (
    select * from {{ source('hospital_raw', 'raw_doctors') }}
),

cleaned as (
    select
        doctor_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as full_name,
        specialty,
        license_number,
        hire_date::date as hire_date,
        department,
        hospital_id,
        phone,
        email,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

