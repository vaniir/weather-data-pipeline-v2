SELECT
    city,
    DATE_TRUNC('week', event_time) AS weather_week,

    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(wind_speed), 2) AS avg_wind_speed

FROM {{ ref('clean_openweather') }}

WHERE valid_location
    AND valid_weather
    AND valid_wind

GROUP BY
    city,
    DATE_TRUNC('week', event_time)