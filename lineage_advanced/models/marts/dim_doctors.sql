-- Dimension: Doctor information with performance metrics
with doctors as (
    select * from {{ ref('stg_doctors') }}
),

hospitals as (
    select * from {{ ref('stg_hospitals') }}
),

appointments as (
    select * from {{ ref('stg_appointments') }}
),

doctor_metrics as (
    select
        doctor_id,
        count(distinct patient_id) as unique_patients_seen,
        count(*) as total_appointments,
        count(case when status = 'Completed' then 1 end) as completed_appointments,
        avg(duration_minutes) as avg_appointment_duration
    from appointments
    group by doctor_id
),

final as (
    select
        doctors.doctor_id,
        doctors.full_name,
        doctors.specialty,
        doctors.department,
        doctors.license_number,
        doctors.hire_date,
        doctors.email,
        doctors.phone,
        
        hospitals.hospital_id,
        hospitals.hospital_name,
        hospitals.city as hospital_city,
        
        coalesce(doctor_metrics.unique_patients_seen, 0) as unique_patients_seen,
        coalesce(doctor_metrics.total_appointments, 0) as total_appointments,
        coalesce(doctor_metrics.completed_appointments, 0) as completed_appointments,
        coalesce(doctor_metrics.avg_appointment_duration, 0) as avg_appointment_duration,
        
        date_diff('year', doctors.hire_date, current_date) as years_of_service
        
    from doctors
    left join hospitals on doctors.hospital_id = hospitals.hospital_id
    left join doctor_metrics on doctors.doctor_id = doctor_metrics.doctor_id
)

select * from final

