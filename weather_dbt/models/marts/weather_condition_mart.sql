SELECT
    city,
    DATE(event_time) AS weather_date,
    weather_main,
    COUNT(*) AS occurrences

FROM {{ ref('clean_syntheticweather') }}

WHERE valid_location

GROUP BY
    city,
    DATE(event_time),
    weather_main