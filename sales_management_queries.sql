use sales_management_sys;
select
sum(gross_sales) as
total_sales,
sum(received_amount)as
total_received,
sum(pendind_amount)as
total_pending
from customer_sales;


select * from branches;

select * from payment_splits;

select * from customer_sales
where status = 'open';

select
branch_id,
count(*) as
total_sales_count
from customer_sales
group by branch_id
order by branch_id;

select
c.sale_id,
c.name,
b.branch_name,
c.gross_sales,
c.received_amount,
c.pendind_amount
from customer_sales c
join branches b 
on c.branch_id =
b.branch_id;


select
c.sale_id,
c.name,
c.gross_sales,
coalesce(sum(p.amount_paid),0) as total_payment_received
from customer_sales c
left join payment_splits p
on c.sale_id = p.sale_id
group by
c.sale_id,
c.name,
c.gross_sales;


select
b.branch_name,
sum(c.gross_sales)as total_gross_sales
from customer_sales c
join branches b
on c.branch_id=b.branch_id
group by b.branch_name
order by total_gross_sales
desc;

select
c.sale_id,
c.name,
c.gross_sales,
p.amount_paid,
p.payment_method
from customer_sales c
join payment_splits p
on c.sale_id=p.sale_id;


select
sale_id,
name,
gross_sales,
received_amount,
pendind_amount
from customer_sales
where pendind_amount>5000
order by pendind_amount
desc;


select
sale_id,
name,
gross_sales
from customer_sales
order by gross_sales 
desc
limit 3;


select
b.branch_name,
sum(c.gross_sales)as total_gross_sales
from customer_sales c
join branches b
on c.branch_id =b.branch_id
group by b.branch_id,b.branch_name
order by total_gross_sales
desc
limit 1;
