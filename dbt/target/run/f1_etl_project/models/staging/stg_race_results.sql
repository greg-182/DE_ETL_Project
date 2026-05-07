
  create view "f1_warehouse"."staging"."stg_race_results__dbt_tmp"
    
    
  as (
    with source as (
    select * from "f1_warehouse"."raw"."race_results"
),

renamed as (
    select
        "DriverNumber" as driver_number,
        "BroadcastName" as driver_name,
        "Abbreviation" as driver_abbreviation,
        "TeamName" as team_name,
        cast("Position" as numeric) as race_position,
        cast("GridPosition" as numeric) as grid_position,
        cast("Points" as numeric) as points,
        cast("Laps" as integer) as laps_completed,
        "Time" as race_time,
        "Status" as status,
        cast("best_lap_time" as numeric) as best_lap_time,
        cast("avg_lap_time" as numeric) as avg_lap_time,
        "year" as race_year,
        "round" as race_round,
        "race_name",
        "is_wet_race"
    from source
)

select * from renamed
  );