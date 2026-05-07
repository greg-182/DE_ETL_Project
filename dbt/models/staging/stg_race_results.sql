with source as (
    select * from {{ source('raw_data', 'race_results') }}
),

renamed as (
    select
        "DriverNumber" as driver_number,
        "BroadcastName" as driver_name,
        "Abbreviation" as driver_abbreviation,
        "TeamName" as team_name,
        "Position" as race_position,
        "GridPosition" as grid_position,
        "Points" as points,
        "Laps" as laps_completed,
        "Time" as race_time,
        "Status" as status,
        "year" as race_year,
        "race_name"
    from source
)

select * from renamed
