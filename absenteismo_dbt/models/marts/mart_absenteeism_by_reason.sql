with enriched as (
    select * from {{ ref('int_absenteeism_enriched') }}
)

select
    reason_code,
    reason_description,
    reason_category,
    reason_type,
    count(*) as total_occurrences,
    sum(absenteeism_hours) as total_absence_hours,
    round(avg(absenteeism_hours), 2) as avg_absence_hours
from enriched
group by reason_code, reason_description, reason_category, reason_type
order by total_absence_hours desc
