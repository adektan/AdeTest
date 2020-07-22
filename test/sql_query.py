insert_master_complex = """
insert into master.complex
(_id, category, name, developer_name, address_street, address_city, address_subdistrict, address_urban, address_province, address_zip, address_coordinate, create_by_uid, facilities, images, tower_total, branches, unit_rent_total, unit_sell_total, developer_legal_name, land_size, last_update_at, last_update_by_uid, address_country, surrounding_area, address_area, create_at, status, code, service_types, premium_listing_available, isactive)
select
       t1._id,
       t1.category,
       t1.name,
       t1.developer_name,
       t1.address_street,
       t1.address_city,
       t1.address_subdistrict,
       t1.address_urban,
       t1.address_province,
       t1.address_zip,
       t1.address_coordinate,
       replace(t1.create_by_uid, '', null) as create_by_uid,
       t1.facilities,
       t1.images,
       t1.tower_total,
       t1.branches,
       t1.unit_rent_total,
       t1.unit_sell_total,
       replace(t1.developer_legal_name, '', null) as developer_legal_name,
       t1.land_size,
       t1.last_update_at,
       t1.last_update_by_uid,
       t1.address_country,
       t1.surrounding_area,
       t1.address_area,
       t1.create_at,
       t1.status,
       t1.code,
       t1.service_types,
       t1.premium_listing_available,
       t1.isactive
from complex t1 left join master.complex t2 on t1._id = t2._id
where t1.insert_date = (select max(insert_date) from complex) and t2._id is null;
"""

update_master_complex = """
update master.complex t1
    set
       category = t2.category,
       name = t2.name,
       developer_name = t2.developer_name,
       address_street = t2.address_street,
       address_city = t2.address_city,
       address_subdistrict = t2.address_subdistrict,
       address_urban = t2.address_urban,
       address_province = t2.address_province,
       address_zip = t2.address_zip,
       address_coordinate = t2.address_coordinate,
       create_by_uid = replace(t2.create_by_uid, '', null),
       facilities = t2.facilities,
       images = t2.images,
       tower_total = t2.tower_total,
       branches = t2.branches,
       unit_rent_total = t2.unit_rent_total,
       unit_sell_total = t2.unit_sell_total,
       developer_legal_name = replace(t2.developer_legal_name, '', null),
       land_size = t2.land_size,
       last_update_at = t2.last_update_at,
       last_update_by_uid = t2.last_update_by_uid,
       address_country = t2.address_country,
       surrounding_area = t2.surrounding_area,
       address_area = t2.address_area,
       create_at = t2.create_at,
       status = t2.status,
       code = t2.code,
       service_types = t2.service_types,
       premium_listing_available = t2.premium_listing_available,
       isactive = t2.isactive,
       update_timestamp = now()
from complex t2 where t1._id = t2._id and t2.insert_date = (select max(insert_date) from complex);
"""

insert_master_tower = """
insert into master.tower
select t1._id,
       t1.name,
       t1.category,
       t1.complex_id,
       case when
           length(t1.year_completion::text) > 4
           then to_char(to_timestamp(t1.year_completion), 'yyyy')::int
           else t1.year_completion::int
       end as year_completion,
       case when
           length(t1.year_completed_estimation::text) > 4
           then to_char(to_timestamp(t1.year_completed_estimation), 'yyyy')::int
           else t1.year_completed_estimation::int
       end as year_completed_estimation,
       t1.year_construction,
       t1.year_renovation,
       replace(t1.architect, '', null) as architect,
       replace(t1.contractor, '', null) as contractor,
       replace(t1.certificate, '', null) as certificate,
       coalesce(t1.service_charge,0) as service_charge,
       coalesce(t1.sinking_fund,0) as sinking_fund,
       replace(t1.promo, '', null) as promo,
       t1.last_update_by_uid,
       t1.last_update_at,
       t1.isactive
from tower t1 left join master.tower t2 on t1._id = t2._id
where t1.insert_date = (select max(insert_date) from tower) and t2._id is null;
"""

update_master_tower = """
update master.tower t1
    set
       name = t2.name,
       category = t2.category,
       complex_id = t2.complex_id,
       year_completion = case when
           length(t2.year_completion::text) > 4
           then to_char(to_timestamp(t2.year_completion), 'yyyy')::int
           else t2.year_completion::int
       end,
       year_completed_estimation = case when
           length(t2.year_completed_estimation::text) > 4
           then to_char(to_timestamp(t2.year_completed_estimation), 'yyyy')::int
           else t2.year_completed_estimation::int
       end,
       year_construction = t2.year_construction,
       year_renovation = t2.year_renovation,
       architect = replace(t2.architect, '', null),
       contractor = replace(t2.contractor, '', null),
       certificate = replace(t2.certificate, '', null),
       service_charge = coalesce(t2.service_charge,0),
       sinking_fund = coalesce(t2.sinking_fund,0),
       promo = replace(t2.promo, '', null),
       last_update_by_uid = t2.last_update_by_uid,
       last_update_at = t2.last_update_at,
       isactive = t2.isactive,
       update_timestamp = now()
from tower t2 where t1._id = t2._id and t2.insert_date = (select max(insert_date) from tower);
"""

insert_master_unit = """
insert into master.unit
select t1._id,
       t1.complex_id,
       t1.category,
       coalesce(t1.land_size,0),
       t1.unit_total,
       t1.floor_count,
       coalesce(t1.max_zone_per_floor,0),
       t1.unit_rent_total,
       t1.unit_sell_total,
       t1.rent_commission,
       t1.sell_commission,
       t1.parking,
       t1.lift,
       t1.building_type,
       t1.internet,
       t1.total_unit_primary,
       t1.isactive
from tower t1 left join master.unit t2 on t1._id = t2._id
where t1.insert_date = (select max(insert_date) from tower) and t2._id is null;
"""

update_master_unit = """
update master.unit t1
    set
       complex_id = t2.complex_id,
       category = t2.category,
       land_size = t2.land_size,
       unit_total = t2.unit_total,
       floor_count = t2.floor_count,
       max_zone_pe_floor = coalesce(t2.max_zone_per_floor,0),
       unit_rent_total = t2.unit_rent_total,
       unit_sell_total = t2.unit_sell_total,
       rent_commission = t2.rent_commission,
       sell_commission = t2.sell_commission,
       parking = t2.parking,
       lift = t2.lift,
       building_type = t2.building_type,
       internet = t2.internet,
       total_unit_primary = t2.total_unit_primary,
       isactive = t2.isactive,
       update_timestamp = now()
from tower t2 where t1._id = t2._id and t2.insert_date = (select max(insert_date) from tower);
"""