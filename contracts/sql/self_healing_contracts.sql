create or replace procedure repair_null_spike(target_table string)
returns string
language sql
as
$$
  begin
    return 'placeholder remediation for ' || target_table;
  end;
$$;

