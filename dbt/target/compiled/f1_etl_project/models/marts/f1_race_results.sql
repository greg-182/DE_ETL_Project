with staging as (
    select * from "f1_warehouse"."staging"."stg_race_results"
),

final as (
    select
        race_year,
        race_name,
        driver_name,
        team_name,
        race_position,
        points,
        laps_completed,
        status
    from staging
    where race_position is not null
    order by race_year desc, race_position asc
)

select * from final