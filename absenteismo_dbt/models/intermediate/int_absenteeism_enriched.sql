with absenteeism as (
    select * from {{ ref('stg_absenteeism') }}
),

reasons as (
    select * from {{ ref('reason_codes') }}
),

joined as (
    select
        a.employee_id,
        a.reason_code,
        r.reason_description,
        r.reason_category,
        r.reason_type,
        a.absence_month,
        a.day_of_week_code,
        case a.day_of_week_code
            when 2 then 'Segunda'
            when 3 then 'Terça'
            when 4 then 'Quarta'
            when 5 then 'Quinta'
            when 6 then 'Sexta'
            else 'Outro'
        end as day_of_week_name,
        a.season_code,
        a.transportation_expense,
        a.distance_to_work_km,
        a.service_time_years,
        a.age,
        a.workload_avg_day,
        a.hit_target,
        a.disciplinary_failure,
        a.education_level,
        a.num_children,
        a.is_social_drinker,
        a.is_social_smoker,
        a.num_pets,
        a.weight_kg,
        a.height_cm,
        a.bmi,
        a.absenteeism_hours
    from absenteeism a
    left join reasons r
        on a.reason_code = r.reason_code
)

select * from joined
