query_view = """
create or replace view master.v_analytic_property as
with factilty_lvl as (
    select _id, string_agg(facilities,', ') as facilities from (
    select _id, json_object_keys(facilities) as facilities, facilities->>json_object_keys(facilities) as flag  from master.complex) a
    where flag = 'true'
    group by 1
),
    parkir_lvl as (
    select _id
     , string_agg((descs || ' : ' || car), ', ') as car_parking
     , string_agg((descs || ' : ' || motor), ', ') as motor_parking
    from (
    select
    _id,
    json_object_keys(parking->0) as descs,
    parking->0->>json_object_keys(parking->0) as car,
    parking->1->>json_object_keys(parking->0) as motor
    from master.unit
    ) a where descs not in ('type', 'name')
    group by 1
),
     lift_lvl as (
    select _id,
       sum((lift->0->>'count')::int) as total_lift_passenger,
       sum((lift->1->>'count')::int) as total_lift_service
    from master.unit group by 1
),
     internet_lvl as (
    select _id, string_agg(internet, ', ') as internet from (
    select _id,
           json_object_keys(internet) as internet,
           internet->>json_object_keys(internet) as flag
    from master.unit where json_typeof(internet) = 'object'
    ) a
    where flag = 'true' group by 1
)

select
t1._id as complex_id,
t2._id as tower_id,
t1.category,
t1.name as complex_name,
t2.name as name_of_tower,
coalesce(t3.land_size,0) as land_size,
t1.address_street as street,
t1.address_zip as zip_code,
t1.address_subdistrict as subdistrict,
t1.address_urban as urban,
t1.address_city as city,
t1.address_province as province,
t1.address_country as country,
trim(t1.developer_name) as developer_name,
t3.unit_total,
t3.floor_count,
t2.year_completion as tower_year_completion,
t2.service_charge as tower_service_charge,
t2.promo,
t3.unit_rent_total,
t3.unit_sell_total,
t3.rent_commission,
t3.sell_commission,
trim(replace(replace(replace(t1.service_types::text, '"', ''),'[',''),']', '')) as service_types,
fl.facilities,
pl.car_parking,
pl.motor_parking,
ll.total_lift_passenger,
ll.total_lift_service,
il.internet,
trim(replace(replace(replace(t3.building_type::text, '"', ''),'[',''),']', '')) as building_type,
t1.last_update_at as last_update_complex,
t2.last_update_at as last_update_tower_unit,
t1.isactive as is_active_complex,
t2.isactive as is_active_tower
from master.complex t1
left join master.tower t2 on t1._id = t2.complex_id
left join master.unit t3 on t2._id = t3._id
left join parkir_lvl pl on t2._id = pl._id
left join lift_lvl ll on t2._id = ll._id
left join internet_lvl il on t2._id = il._id
left join factilty_lvl fl on t1._id = fl._id;
"""

insert_query = """
insert into master.analytic_property
select t1.complex_id,
       t1.tower_id,
       t1.category,
       t1.complex_name,
       t1.name_of_tower,
       t1.land_size,
       t1.street,
       t1.zip_code,
       t1.subdistrict,
       t1.urban,
       t1.city,
       t1.province,
       t1.country,
       t1.developer_name,
       t1.unit_total,
       t1.floor_count,
       t1.tower_year_completion,
       t1.tower_service_charge,
       t1.promo,
       t1.unit_rent_total,
       t1.unit_sell_total,
       t1.rent_commission,
       t1.sell_commission,
       t1.service_types,
       t1.facilities,
       t1.car_parking,
       t1.motor_parking,
       t1.total_lift_passenger,
       t1.total_lift_service,
       t1.internet,
       t1.building_type,
       t1.last_update_complex,
       t1.last_update_tower_unit,
       t1.is_active_complex,
       t1.is_active_tower
from master.v_analytic_property t1
    left join master.analytic_property t2 on t1.complex_id = t2.complex_id and coalesce(t2.tower_id,'null') = coalesce(t1.tower_id,'null')
where t2.complex_id is null and t2.tower_id is null;
"""

update_query = """
update master.analytic_property t1
set
    complex_id = t2.complex_id,
tower_id = t2.tower_id,
category = t2.category,
complex_name = t2.complex_name,
name_of_tower = t2.name_of_tower,
land_size = t2.land_size,
street = t2.street,
zip_code = t2.zip_code,
subdistrict = t2.subdistrict,
urban = t2.urban,
city = t2.city,
province = t2.province,
country = t2.country,
developer_name = t2.developer_name,
unit_total = t2.unit_total,
floor_count = t2.floor_count,
tower_year_completion = t2.tower_year_completion,
tower_service_charge = t2.tower_service_charge,
promo = t2.promo,
unit_rent_total = t2.unit_rent_total,
unit_sell_total = t2.unit_sell_total,
rent_commission = t2.rent_commission,
sell_commission = t2.sell_commission,
service_types = t2.service_types,
facilities = t2.facilities,
car_parking = t2.car_parking,
motor_parking = t2.motor_parking,
total_lift_passenger = t2.total_lift_passenger,
total_lift_service = t2.total_lift_service,
internet = t2.internet,
building_type = t2.building_type,
last_update_complex = t2.last_update_complex,
last_update_tower_unit = t2.last_update_tower_unit,
is_active_complex = t2.is_active_complex,
is_active_tower = t2.is_active_tower,
update_timestamp = now()
from master.v_analytic_property t2 where t1.complex_id = t2.complex_id and coalesce(t2.tower_id,'null') = coalesce(t1.tower_id,'null');
"""