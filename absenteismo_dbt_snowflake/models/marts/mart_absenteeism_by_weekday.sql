with enriched as (
    select * from {{ ref('int_absenteeism_enriched') }}
)

select
    day_of_week_name,
    count(*) as total_occurrences,
    sum(absenteeism_hours) as total_absence_hours,
    round(avg(absenteeism_hours), 2) as avg_absence_hours
from enriched
group by day_of_week_name
order by total_absence_hours desc
