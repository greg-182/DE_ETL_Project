# Superset SQL Snippets (Formula 1)

This file collects copy-paste SQL snippets for common chart customizations in Superset based on the Formula 1 datasets.

Datasets to add in Superset (**Data -> Datasets -> + Dataset**):
- `mart.f1_race_results`
- `mart.f1_driver_standings`
- `mart.f1_constructor_standings`

Dataset used in examples:
- mart.f1_race_results

How to use these:
- Add expressions in **Dataset -> Edit dataset -> Columns -> + COLUMN** for calculated columns.
- Add expressions in **Dataset -> Edit dataset -> Metrics -> + METRIC** for custom metrics.
- Use the output alias as chart dimension/metric fields.

## Custom Metrics (`mart.f1_race_results`)

### Total Retirements (DNFs)
Count the number of times a driver did not finish.
```sql
SUM(is_dnf)
```
Suggested metric name: `dnf_count`

### Total Positions Gained
Sum of positions gained during the race (grid position - finish position).
```sql
SUM(position_change)
```
Suggested metric name: `total_positions_gained`

### Fastest Lap Time
Find the single fastest lap across all selected data.
```sql
MIN(best_lap_time)
```
Suggested metric name: `overall_best_lap`

### Average Race Lap Time
Calculate the average lap time.
```sql
AVG(avg_lap_time)
```
Suggested metric name: `overall_avg_lap`

### Podium Finishes
Count the number of times a driver finished in 1st, 2nd, or 3rd place.
```sql
SUM(CASE WHEN race_position <= 3 THEN 1 ELSE 0 END)
```
Suggested metric name: podium_count

### Race Wins
Count the number of 1st place finishes.
```sql
SUM(CASE WHEN race_position = 1 THEN 1 ELSE 0 END)
```
Suggested metric name: win_count

### Total Points
Calculate the total points scored.
```sql
SUM(points)
```
Suggested metric name: total_points

## Calculated Columns

### Top 10 Finisher Flag
Categorize whether the result was in the top 10.
```sql
CASE 
  WHEN race_position <= 10 THEN 'Top 10'
  ELSE 'Outside Top 10'
END
```

### Podium Category
Label the specific podium step or 'Off Podium'.
```sql
CASE
  WHEN race_position = 1 THEN '1st Place'
  WHEN race_position = 2 THEN '2nd Place'
  WHEN race_position = 3 THEN '3rd Place'
  ELSE 'Off Podium'
END
```

## Simple Filters

Use these as chart-level SQL filters when needed:

### Filter for Recent Seasons
Keep rows from the year 2020 onwards:
```sql
race_year >= 2020
```

### Filter for Wet Races Only
```sql
is_wet_race = true
```

### Filter for Winners Only
Keep only rows where the driver won the race:
```sql
race_position = 1
```
