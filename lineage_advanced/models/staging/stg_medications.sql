-- Staging: Clean medication catalog
with source as (
    select * from {{ source('hospital_raw', 'raw_medications') }}
),

cleaned as (
    select
        medication_id,
        medication_name,
        generic_name,
        drug_class,
        manufacturer,
        {{ cents_to_dollars('unit_cost') }} as unit_cost,  -- Using custom macro
        requires_prescription,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

