-- Staging: Clean lab test data
with source as (
    select * from {{ source('hospital_raw', 'raw_lab_tests') }}
),

cleaned as (
    select
        test_id,
        appointment_id,
        patient_id,
        test_type,
        test_name,
        test_date::date as test_date,
        result_value,
        result_unit,
        reference_range,
        status,
        abnormal_flag::boolean as is_abnormal,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

