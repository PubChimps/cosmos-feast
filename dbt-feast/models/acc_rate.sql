{{ config(materialized='table') }}

select 
    event_timestamp, 
    i.driver_id, 
    acc_rate, 
    (acc_rate_max-acc_rate) as acc_rate_max_diff 
from feast_driver_hourly_stats i 
join (
    select 
        driver_id, 
        max(acc_rate) as acc_rate_max 
    from feast_driver_hourly_stats 
    group by driver_id) j 
on (i.driver_id=j.driver_id) 
