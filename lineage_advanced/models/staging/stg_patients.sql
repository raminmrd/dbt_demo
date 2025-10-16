-- Staging: Clean and enrich patient data
with source as (
    select * from {{ source('hospital_raw', 'raw_patients') }}
),

cleaned as (
    select
        patient_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as full_name,
        date_of_birth::date as date_of_birth,
        {{ calculate_age('date_of_birth') }} as age,  -- Using custom macro
        gender,
        email,
        phone,
        address,
        city,
        state,
        zip_code,
        insurance_provider,
        registration_date::date as registration_date,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

