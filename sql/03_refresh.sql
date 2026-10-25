create or replace procedure refresh()
language plpgsql as $$
begin
    truncate fact_sales, product, customer restart identity;
    call fill_product();
    call fill_customer();
    call fill_sales();
end;
$$;