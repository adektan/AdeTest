with images_complex as
(
select _id, json_object_keys(images) as images_key, images->json_object_keys(images) as value
from master.complex
),
images_level as
(
select
       _id, images_key,
       case when json_typeof(value) = 'null' then 0
            when json_typeof(value) = 'array' then json_array_length(value)
       end as total
from images_complex
)
select
images_key,
       sum(case when total = 0 then 1 else 0 end) as "0",
       sum(case when total between 1 and 2 then 1 else 0 end) as "1-2",
       sum(case when total between 3 and 4 then 1 else 0 end)  as "3-4",
       sum(case when total >= 5 then 1 else 0 end) as "5 or more"
from images_level
group by 1 order by 5 desc