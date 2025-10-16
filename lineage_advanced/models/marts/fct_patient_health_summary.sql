-- Fact: Patient health summary and treatment history
with diagnoses as (
    select * from {{ ref('int_diagnoses_with_context') }}
),

prescriptions as (
    select * from {{ ref('int_prescriptions_with_costs') }}
),

lab_tests as (
    select * from {{ ref('stg_lab_tests') }}
),

patient_diagnosis_summary as (
    select
        patient_id,
        count(distinct diagnosis_code) as unique_diagnoses,
        count(*) as total_diagnoses,
        count(case when severity = 'Severe' then 1 end) as severe_diagnoses_count,
        max(diagnosis_date) as last_diagnosis_date,
        string_agg(distinct diagnosis_name, '; ') as all_diagnoses
    from diagnoses
    group by patient_id
),

patient_prescription_summary as (
    select
        patient_id,
        count(*) as total_prescriptions,
        count(distinct medication_id) as unique_medications,
        sum(estimated_cost) as total_medication_cost,
        max(prescription_date) as last_prescription_date
    from prescriptions
    group by patient_id
),

patient_lab_summary as (
    select
        patient_id,
        count(*) as total_lab_tests,
        count(case when is_abnormal then 1 end) as abnormal_results_count,
        max(test_date) as last_test_date
    from lab_tests
    group by patient_id
),

final as (
    select
        coalesce(
            patient_diagnosis_summary.patient_id,
            patient_prescription_summary.patient_id,
            patient_lab_summary.patient_id
        ) as patient_id,
        
        -- Diagnosis metrics
        coalesce(patient_diagnosis_summary.unique_diagnoses, 0) as unique_diagnoses,
        coalesce(patient_diagnosis_summary.total_diagnoses, 0) as total_diagnoses,
        coalesce(patient_diagnosis_summary.severe_diagnoses_count, 0) as severe_diagnoses_count,
        patient_diagnosis_summary.last_diagnosis_date,
        patient_diagnosis_summary.all_diagnoses,
        
        -- Prescription metrics
        coalesce(patient_prescription_summary.total_prescriptions, 0) as total_prescriptions,
        coalesce(patient_prescription_summary.unique_medications, 0) as unique_medications,
        coalesce(patient_prescription_summary.total_medication_cost, 0) as total_medication_cost,
        patient_prescription_summary.last_prescription_date,
        
        -- Lab test metrics
        coalesce(patient_lab_summary.total_lab_tests, 0) as total_lab_tests,
        coalesce(patient_lab_summary.abnormal_results_count, 0) as abnormal_results_count,
        patient_lab_summary.last_test_date,
        
        -- Risk assessment
        case
            when coalesce(patient_diagnosis_summary.severe_diagnoses_count, 0) > 0 then 'High Risk'
            when coalesce(patient_lab_summary.abnormal_results_count, 0) >= 2 then 'Moderate Risk'
            when coalesce(patient_diagnosis_summary.unique_diagnoses, 0) >= 3 then 'Moderate Risk'
            else 'Low Risk'
        end as risk_category
        
    from patient_diagnosis_summary
    full outer join patient_prescription_summary 
        on patient_diagnosis_summary.patient_id = patient_prescription_summary.patient_id
    full outer join patient_lab_summary 
        on coalesce(patient_diagnosis_summary.patient_id, patient_prescription_summary.patient_id) = patient_lab_summary.patient_id
)

select * from final

