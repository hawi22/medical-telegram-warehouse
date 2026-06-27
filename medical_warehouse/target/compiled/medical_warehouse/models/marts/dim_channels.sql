SELECT
    md5(cast(coalesce(cast(channel_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as channel_pk,
    channel_name,
    MIN(message_date) as first_post_date,
    MAX(message_date) as last_post_date,
    COUNT(message_id) as total_posts,
    AVG(view_count) as avg_views
FROM "medical_warehouse"."public_staging"."stg_telegram_messages"
GROUP BY channel_name