
  
    

  create  table "medical_warehouse"."public_marts"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    SELECT
    md5(cast(coalesce(cast(message_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(channel_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as message_pk,
    CAST(message_date AS DATE) as date_fk,
    md5(cast(coalesce(cast(channel_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as channel_fk,
    message_text,
    view_count,
    forward_count,
    has_image,
    message_length
FROM "medical_warehouse"."public_staging"."stg_telegram_messages"
  );
  