SELECT
    city,
    DATE(event_time) AS weather_date,

    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(feels_like), 2) AS avg_feels_like,
    ROUND(AVG(humidity), 2) AS avg_humidity,
    ROUND(AVG(pressure), 2) AS avg_pressure,
    ROUND(AVG(wind_speed), 2) AS avg_wind_speed,
    ROUND(AVG(cloud_coverage), 2) AS avg_cloud_coverage

FROM {{ ref('clean_syntheticweather') }}

WHERE
    valid_location
    AND valid_weather
    AND valid_wind
    AND valid_pressure
    AND valid_clouds

GROUP BY
    city,
    DATE(event_time)