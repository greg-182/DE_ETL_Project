with race_results as (
    select * from {{ ref('f1_race_results') }}
),

driver_points as (
    select
        race_year,
        race_round,
        race_name,
        driver_name,
        team_name,
        points as race_points
    from race_results
),

standings as (
    select
        race_year,
        race_round,
        race_name,
        driver_name,
        team_name,
        race_points,
        sum(race_points) over (
            partition by race_year, driver_name 
            order by race_round
            rows between unbounded preceding and current row
        ) as cumulative_points
    from driver_points
)

select * 
from standings
order by race_year desc, race_round asc, cumulative_points desc
