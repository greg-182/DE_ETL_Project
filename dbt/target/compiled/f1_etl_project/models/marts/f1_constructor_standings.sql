with race_results as (
    select * from "f1_warehouse"."mart"."f1_race_results"
),

constructor_race_points as (
    select
        race_year,
        race_round,
        race_name,
        team_name,
        sum(points) as team_race_points
    from race_results
    group by 1, 2, 3, 4
),

standings as (
    select
        race_year,
        race_round,
        race_name,
        team_name,
        team_race_points,
        sum(team_race_points) over (
            partition by race_year, team_name 
            order by race_round
            rows between unbounded preceding and current row
        ) as cumulative_points
    from constructor_race_points
)

select * 
from standings
order by race_year desc, race_round asc, cumulative_points desc