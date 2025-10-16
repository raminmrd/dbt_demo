-- INCREMENTAL MODEL: Financial metrics aggregated by day
-- This demonstrates dbt's incremental materialization for large, growing datasets

{{ config(
    materialized='incremental',
    unique_key='metric_date'
) }}

with claims as (
    select * from {{ ref('int_claim_analysis') }}
    {% if is_incremental() %}
        -- Only process new records when running incrementally
        where claim_date > (select max(metric_date) from {{ this }})
    {% endif %}
),

daily_metrics as (
    select
        claim_date as metric_date,
        count(*) as total_claims,
        count(case when claim_status = 'Approved' then 1 end) as approved_claims,
        count(case when claim_status = 'Denied' then 1 end) as denied_claims,
        count(case when claim_status = 'Pending' then 1 end) as pending_claims,
        
        sum(total_charged) as total_revenue,
        sum(insurance_paid) as total_insurance_paid,
        sum(patient_paid) as total_patient_paid,
        sum(outstanding_balance) as total_outstanding,
        
        avg(insurance_coverage_percent) as avg_coverage_percent,
        avg(days_to_claim) as avg_days_to_claim,
        
        count(distinct patient_id) as unique_patients,
        count(distinct insurance_provider) as unique_insurers
        
    from claims
    group by claim_date
)

select * from daily_metrics

