-- Fact: Appointment-level facts with all related data
with patient_visits as (
    select * from {{ ref('int_patient_visits') }}
),

diagnoses as (
    select * from {{ ref('stg_diagnoses') }}
),

prescriptions as (
    select * from {{ ref('int_prescriptions_with_costs') }}
),

lab_tests as (
    select * from {{ ref('stg_lab_tests') }}
),

claims as (
    select * from {{ ref('stg_insurance_claims') }}
),

-- Aggregate data per appointment
diagnosis_agg as (
    select
        appointment_id,
        count(*) as diagnosis_count,
        string_agg(diagnosis_name, ', ') as diagnoses_list
    from diagnoses
    group by appointment_id
),

prescription_agg as (
    select
        appointment_id,
        count(*) as prescription_count,
        sum(estimated_cost) as total_medication_cost
    from prescriptions
    group by appointment_id
),

lab_test_agg as (
    select
        appointment_id,
        count(*) as lab_test_count,
        count(case when is_abnormal then 1 end) as abnormal_test_count
    from lab_tests
    group by appointment_id
),

final as (
    select
        patient_visits.appointment_id,
        patient_visits.appointment_date,
        patient_visits.appointment_type,
        patient_visits.status,
        patient_visits.duration_minutes,
        
        -- Keys
        patient_visits.patient_id,
        patient_visits.doctor_id,
        patient_visits.hospital_id,
        
        -- Patient info
        patient_visits.patient_name,
        patient_visits.patient_age,
        patient_visits.gender,
        patient_visits.insurance_provider,
        
        -- Doctor info
        patient_visits.doctor_name,
        patient_visits.specialty,
        patient_visits.department,
        
        -- Hospital info
        patient_visits.hospital_name,
        
        -- Aggregated metrics
        coalesce(diagnosis_agg.diagnosis_count, 0) as diagnosis_count,
        diagnosis_agg.diagnoses_list,
        coalesce(prescription_agg.prescription_count, 0) as prescription_count,
        coalesce(prescription_agg.total_medication_cost, 0) as total_medication_cost,
        coalesce(lab_test_agg.lab_test_count, 0) as lab_test_count,
        coalesce(lab_test_agg.abnormal_test_count, 0) as abnormal_test_count,
        
        -- Financial
        coalesce(claims.total_charged, 0) as total_charged,
        coalesce(claims.insurance_paid, 0) as insurance_paid,
        coalesce(claims.patient_paid, 0) as patient_paid,
        claims.claim_status
        
    from patient_visits
    left join diagnosis_agg on patient_visits.appointment_id = diagnosis_agg.appointment_id
    left join prescription_agg on patient_visits.appointment_id = prescription_agg.appointment_id
    left join lab_test_agg on patient_visits.appointment_id = lab_test_agg.appointment_id
    left join claims on patient_visits.appointment_id = claims.appointment_id
)

select * from final

