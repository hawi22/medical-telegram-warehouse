SELECT
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} as channel_pk,
    channel_name,
    MIN(message_date) as first_post_date,
    MAX(message_date) as last_post_date,
    COUNT(message_id) as total_posts,
    AVG(view_count) as avg_views
FROM {{ ref('stg_telegram_messages') }}
GROUP BY channel_name