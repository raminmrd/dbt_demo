-- Staging: Clean hospital data
with source as (
    select * from {{ source('hospital_raw', 'raw_hospitals') }}
),

cleaned as (
    select
        hospital_id,
        hospital_name,
        address,
        city,
        state,
        zip_code,
        phone,
        bed_capacity,
        trauma_level,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

