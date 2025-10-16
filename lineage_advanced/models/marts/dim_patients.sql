-- Dimension: Patient information with visit history
with patients as (
    select * from {{ ref('stg_patients') }}
),

appointments as (
    select * from {{ ref('stg_appointments') }}
),

patient_metrics as (
    select
        patient_id,
        count(*) as total_visits,
        count(case when status = 'Completed' then 1 end) as completed_visits,
        count(case when status = 'No-show' then 1 end) as no_show_count,
        min(appointment_date) as first_visit_date,
        max(appointment_date) as last_visit_date
    from appointments
    group by patient_id
),

final as (
    select
        patients.patient_id,
        patients.full_name,
        patients.date_of_birth,
        patients.age,
        patients.gender,
        patients.email,
        patients.phone,
        patients.city,
        patients.state,
        patients.insurance_provider,
        patients.registration_date,
        
        coalesce(patient_metrics.total_visits, 0) as total_visits,
        coalesce(patient_metrics.completed_visits, 0) as completed_visits,
        coalesce(patient_metrics.no_show_count, 0) as no_show_count,
        patient_metrics.first_visit_date,
        patient_metrics.last_visit_date,
        
        case
            when coalesce(patient_metrics.total_visits, 0) >= 5 then 'Frequent'
            when coalesce(patient_metrics.total_visits, 0) >= 2 then 'Regular'
            when coalesce(patient_metrics.total_visits, 0) = 1 then 'New'
            else 'Registered'
        end as patient_category
        
    from patients
    left join patient_metrics on patients.patient_id = patient_metrics.patient_id
)

select * from final

