USE e2edaProject;

-- Creating an empty table first to make sure the dataype is correct and then append it from python script

-- create table df_orders (
-- order_id int primary key,
-- order_date date,
-- ship_mode varchar(20),
-- segment varchar(20),
-- country varchar(20),
-- city varchar(20),
-- state varchar(20),
-- postal_code varchar(20),
-- region varchar(20),
-- category varchar(20),
-- sub_category varchar(20),
-- product_id varchar(20),
-- quantity int,
-- discount decimal(7,2),
-- sales_price decimal(7,2),
-- profit decimal(7,2))
-- ;

-- Checking the appended table

-- select * from df_orders;





-- Find the top highest revenue generating products

-- Select product_id, sum(sales_price) as sales
-- from df_orders
-- group by product_id
-- order by sales desc





-- Find the highest selling products in each region

-- With cte as(
-- Select region, product_id, sum(sales_price) as sales
-- from df_orders
-- group by region, product_id)
-- select * from (
-- select *,
-- row_number() over(partition by region order by sales desc) as rn
-- from cte) A 
-- where rn<=5






-- Find month over month growth comparison for 2022 and 2023 sales eg: jan 2022 vs jan 2023

-- select distinct year(order_date) from df_orders

-- with cte as (

-- select year(order_date) as order_year, month(order_date) as order_month,
-- sum(sales_price) as sales
-- from df_orders
-- group by year(order_date), month(order_date)
-- order by year(order_date), month(order_date)
-- )
-- select order_month,
-- sum(case when order_year = 2022 then sales else 0 end) as sales_2022,
-- sum(case when order_year = 2023 then sales else 0 end) as sales_2023

-- from cte
-- group by order_month
-- order by order_month





-- For each category, which month had the highest sales?

-- with cte as (
-- Select category, date_format(order_date,'%Y%m') as order_year_month,
-- sum(sales_price) as sales
-- from df_orders
-- group by category, date_format(order_date,'%Y%m')
-- order by category, date_format(order_date,'%Y%m')
-- )
-- select * from (
-- select *,
-- row_number() over(partition by category order by sales desc) as rn
-- from cte
-- ) a

-- where rn = 1







-- Which sub-category had the highest growth by profit in 2023 compared to 2022?

with cte as (

select sub_category, year(order_date) as order_year,
sum(sales_price) as sales
from df_orders
group by sub_category, year(order_date)
order by year(order_date), month(order_date)
 )

, cte2 as (
select sub_category,
sum(case when order_year = 2022 then sales else 0 end) as sales_2022,
sum(case when order_year = 2023 then sales else 0 end) as sales_2023

from cte
group by sub_category
-- order by order_month
)

select *
, (sales_2023 - sales_2022)*100 / sales_2022
from cte2
order by (sales_2023 - sales_2022)*100 / sales_2022 desc