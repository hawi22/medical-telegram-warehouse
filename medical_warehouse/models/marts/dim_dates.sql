SELECT
    DISTINCT 
    CAST(message_date AS DATE) as date_pk,
    EXTRACT(DAY FROM message_date) as day,
    EXTRACT(DOW FROM message_date) as day_of_week,
    EXTRACT(MONTH FROM message_date) as month,
    EXTRACT(YEAR FROM message_date) as year,
    CASE WHEN EXTRACT(DOW FROM message_date) IN (0, 6) THEN TRUE ELSE FALSE END as is_weekend
FROM {{ ref('stg_telegram_messages') }}