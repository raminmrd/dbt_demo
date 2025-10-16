-- Intermediate: Combine appointments with patient and doctor details
with appointments as (
    select * from {{ ref('stg_appointments') }}
),

patients as (
    select * from {{ ref('stg_patients') }}
),

doctors as (
    select * from {{ ref('stg_doctors') }}
),

hospitals as (
    select * from {{ ref('stg_hospitals') }}
),

combined as (
    select
        appointments.appointment_id,
        appointments.appointment_date,
        appointments.appointment_time,
        appointments.appointment_type,
        appointments.status,
        appointments.duration_minutes,
        
        -- Patient details
        patients.patient_id,
        patients.full_name as patient_name,
        patients.age as patient_age,
        patients.gender,
        patients.insurance_provider,
        
        -- Doctor details
        doctors.doctor_id,
        doctors.full_name as doctor_name,
        doctors.specialty,
        doctors.department,
        
        -- Hospital details
        hospitals.hospital_id,
        hospitals.hospital_name
        
    from appointments
    left join patients on appointments.patient_id = patients.patient_id
    left join doctors on appointments.doctor_id = doctors.doctor_id
    left join hospitals on appointments.hospital_id = hospitals.hospital_id
)

select * from combined

