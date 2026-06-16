SELECT
    city,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(wind_speed), 2) AS avg_wind_speed,

    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature

FROM {{ ref('clean_syntheticweather') }}

WHERE valid_location
    AND valid_weather
    AND valid_wind

GROUP BY city