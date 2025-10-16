-- Staging: Clean insurance claims data
with source as (
    select * from {{ source('hospital_raw', 'raw_insurance_claims') }}
),

cleaned as (
    select
        claim_id,
        appointment_id,
        patient_id,
        insurance_provider,
        claim_date::date as claim_date,
        service_date::date as service_date,
        {{ cents_to_dollars('total_charged') }} as total_charged,
        {{ cents_to_dollars('insurance_paid') }} as insurance_paid,
        {{ cents_to_dollars('patient_paid') }} as patient_paid,
        claim_status,
        denial_reason,
        current_timestamp as _loaded_at
    from source
)

select * from cleaned

