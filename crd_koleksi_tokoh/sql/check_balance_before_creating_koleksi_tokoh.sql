create or replace function the_cims.check_balance_before_creating_koleksi_tokoh() returns trigger as
$$
declare
koin int4;
harga int4;
begin
if (TG_OP = 'INSERT' or TG_OP = 'UPDATE') then
  koin := (
    select koin from pemain
    where username = new.username_pengguna
    limit 1
  );
  harga := (
    select harga from koleksi
    where id = new.id_koleksi
    limit 1
  );
  if (koin < harga) then
    raise exception 'Jumlah koin yang dimiliki tidak mencukupi';
  end if;
end if; end;
$$
language plpgsql;

create trigger check_balance_before_creating_koleksi_tokoh before insert or update on KOLEKSI_TOKOH
for each row execute procedure check_balance_before_creating_koleksi_tokoh();

-- drop trigger check_balance_before_creating_koleksi_tokoh on KOLEKSI_TOKOH;
