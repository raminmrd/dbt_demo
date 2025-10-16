{% snapshot snap_patient_insurance %}

-- SNAPSHOT: Track changes to patient insurance over time
-- Snapshots implement Slowly Changing Dimension (SCD) Type 2 logic
-- This tracks historical changes to patient insurance providers

{{
    config(
      target_schema='snapshots',
      unique_key='patient_id',
      strategy='check',
      check_cols=['insurance_provider'],
    )
}}

select
    patient_id,
    full_name,
    insurance_provider,
    current_timestamp as snapshot_timestamp
from {{ ref('stg_patients') }}

{% endsnapshot %}

