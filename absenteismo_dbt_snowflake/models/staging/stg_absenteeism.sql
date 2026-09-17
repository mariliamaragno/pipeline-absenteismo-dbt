with source as (
    select * from {{ source('raw', 'raw_absenteeism') }}
),

renamed as (
    select
        ID as employee_id,
        REASON_FOR_ABSENCE as reason_code,
        MONTH_OF_ABSENCE as absence_month,
        DAY_OF_THE_WEEK as day_of_week_code,
        SEASONS as season_code,
        TRANSPORTATION_EXPENSE as transportation_expense,
        DISTANCE_FROM_RESIDENCE_TO_WORK as distance_to_work_km,
        SERVICE_TIME as service_time_years,
        AGE as age,
        WORK_LOAD_AVERAGE_DAY as workload_avg_day,
        HIT_TARGET as hit_target,
        DISCIPLINARY_FAILURE as disciplinary_failure,
        EDUCATION as education_level,
        SON as num_children,
        SOCIAL_DRINKER as is_social_drinker,
        SOCIAL_SMOKER as is_social_smoker,
        PET as num_pets,
        WEIGHT as weight_kg,
        HEIGHT as height_cm,
        BODY_MASS_INDEX as bmi,
        ABSENTEEISM_TIME_IN_HOURS as absenteeism_hours
    from source
)

select * from renamed
