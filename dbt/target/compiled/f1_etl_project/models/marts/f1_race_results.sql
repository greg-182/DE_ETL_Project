with staging as (
    select * from "f1_warehouse"."staging"."stg_race_results"
),

final as (
    select
        race_year,
        race_round,
        race_name,
        is_wet_race,
        driver_name,
        driver_abbreviation,
        team_name,
        grid_position,
        race_position,
        (grid_position - race_position) as position_change,
        points,
        laps_completed,
        status,
        -- Flag to easily count retirements (Did Not Finish)
        case 
            when status not in ('Finished', '+1 Lap', '+2 Laps', '+3 Laps', '+4 Laps', '+5 Laps', '+6 Laps') 
            then 1 
            else 0 
        end as is_dnf,
        best_lap_time,
        avg_lap_time
    from staging
    where race_position is not null
    order by race_year desc, race_round asc, race_position asc
)

select * from final