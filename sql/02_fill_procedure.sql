CREATE OR REPLACE PROCEDURE fill_product()
LANGUAGE plpgsql AS $$
DECLARE
    n integer := 0;
    n_unknown integer := 0;
BEGIN
    insert into product (stock_code, description)
	select distinct stock_code, description
	from sales
	where line_type <> 'error';
	GET DIAGNOSTICS n = ROW_COUNT;

	insert into product (stock_code, description)
	select distinct stock_code, 'UNKNOWN PRODUCT'
	from sales
	on conflict (stock_code) do nothing;
	GET DIAGNOSTICS n_error = ROW_COUNT;

	raise notice '% product line inserted of which % were error line', n+n_unknown, n_unknown;
END;
$$;

create or replace procedure fill_customer()
LANGUAGE plpgsql AS $$
declare 
	n integer := 0;
	r record;
begin 
	for r in select distinct customer_id from sales
	loop
		insert into customer (customer_id) values (r.customer_id);
		n := n +1;
	end loop;
	raise notice '% customer line inserted ', n;
end;
$$;

create or replace procedure fill_sales()
LANGUAGE plpgsql AS $$
declare 
	n integer := 0;
begin
	insert into fact_sales (invoice, stock_code, customer_id, invoice_date, 
	country, quantity, price, revenue, line_type, error_category)
	select invoice, stock_code, customer_id, invoice_date, country, quantity, 
	price, revenue, line_type,
	CASE line_type WHEN 'error' THEN description end
	from sales;

	GET DIAGNOSTICS n = ROW_COUNT;
	RAISE NOTICE '% sale line inserted', n;
end;
$$;
