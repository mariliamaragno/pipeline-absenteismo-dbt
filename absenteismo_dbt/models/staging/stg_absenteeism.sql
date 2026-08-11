with source as (
    select * from {{ source('raw', 'raw_absenteeism') }}
),

renamed as (
    select
        "ID" as employee_id,
        "Reason for absence" as reason_code,
        "Month of absence" as absence_month,
        "Day of the week" as day_of_week_code,
        "Seasons" as season_code,
        "Transportation expense" as transportation_expense,
        "Distance from Residence to Work" as distance_to_work_km,
        "Service time" as service_time_years,
        "Age" as age,
        "Work load Average/day " as workload_avg_day,
        "Hit target" as hit_target,
        "Disciplinary failure" as disciplinary_failure,
        "Education" as education_level,
        "Son" as num_children,
        "Social drinker" as is_social_drinker,
        "Social smoker" as is_social_smoker,
        "Pet" as num_pets,
        "Weight" as weight_kg,
        "Height" as height_cm,
        "Body mass index" as bmi,
        "Absenteeism time in hours" as absenteeism_hours
    from source
)

select * from renamed
