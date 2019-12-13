-- wagtailcore_pagerevision.content_json.content_type uses foreign keys from production data.
-- Foreign key ids inside of nested content_json field are not automatically updated during datadump.
-- So the content_type value must be updated to match the correct content_type ids used locally.
update wagtailcore_pagerevision
  set content_json = sq00.updated_content_json
from (
  select
    r.id as revision_id,
    jsonb_set(r.content_json::jsonb, '{content_type}', p.content_type_id::varchar::jsonb) as updated_content_json
  from wagtailcore_pagerevision r
  join wagtailcore_page p on r.page_id = p.id
) as sq00
where sq00.revision_id = id
;
