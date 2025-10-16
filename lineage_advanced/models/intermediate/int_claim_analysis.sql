-- Intermediate: Claims with calculated metrics
with claims as (
    select * from {{ ref('stg_insurance_claims') }}
),

appointments as (
    select * from {{ ref('stg_appointments') }}
),

patients as (
    select * from {{ ref('stg_patients') }}
),

enriched as (
    select
        claims.claim_id,
        claims.appointment_id,
        claims.patient_id,
        claims.insurance_provider,
        claims.claim_date,
        claims.service_date,
        claims.total_charged,
        claims.insurance_paid,
        claims.patient_paid,
        claims.claim_status,
        claims.denial_reason,
        
        -- Patient details
        patients.full_name as patient_name,
        patients.age as patient_age,
        
        -- Appointment details
        appointments.appointment_type,
        appointments.status as appointment_status,
        
        -- Calculated fields
        claims.total_charged - claims.insurance_paid - claims.patient_paid as outstanding_balance,
        case 
            when claims.total_charged > 0 
            then (claims.insurance_paid / claims.total_charged) * 100 
            else 0 
        end as insurance_coverage_percent,
        date_diff('day', claims.service_date, claims.claim_date) as days_to_claim
        
    from claims
    left join patients on claims.patient_id = patients.patient_id
    left join appointments on claims.appointment_id = appointments.appointment_id
)

select * from enriched

