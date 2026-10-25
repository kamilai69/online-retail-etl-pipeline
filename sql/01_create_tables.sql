create table if not exists product (
	stock_code text primary key,
	description text not null
);

create table if not exists customer (
	customer_id integer primary key
);

create table if not exists fact_sales (
	sale_id bigint generated always as identity primary key, 
	invoice text not null,
	stock_code text not null,
	customer_id integer not null,
	invoice_date timestamp not null, 
	country text,
	quantity integer not null, 
	price numeric(10, 3) not null,
	revenue numeric(10, 3) not null,
	line_type text not null check (line_type in ('sale', 'refund', 'error')),
	error_category text CHECK (error_category IN ('QUALITY_ERROR', 'MIXING_ERROR',
    'DAMAGE_ERROR', 'MISSING_ERROR', 'SOLD_ERROR')),
	check ((line_type = 'error') = (error_category is not null)),
	
	foreign key (stock_code) 
		references product(stock_code), 
		
	foreign key (customer_id)
		references customer(customer_id)
);