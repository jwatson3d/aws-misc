# Data Catalog / Finding Stuff

# Schema holding a specific table / column

```
select  distinct ns.nspname
from    pg_class t,
        pg_attribute a,
        pg_namespace ns
where   t.relname = 'TBL'
and     a.attname = 'COL'
and     a.attrelid = t.oid
and     ns.oid = t.relnamespace;
```


# List of tables and columns, with distribution and sort keys

This is an alternative to `PG_TABLE_DEF`, which is limited to the current search path,
and `SVV_TABLE_INFO`, which shows a "user friendly" distribution key and only the first
column of the sort key.

Variant 1: useful for a CTE.

```
select  pgn.nspname as schema_name,
        pgc.relname as table_name,
        pga.attname as column_name,
        pga.attnum  as column_order,
        pga.attisdistkey as is_distkey,
        pga.attsortkeyord as sortkey_order
from    pg_attribute pga
join    pg_class pgc on pgc.oid = pga.attrelid
join    pg_namespace pgn on pgn.oid = pgc.relnamespace
where   pgc.relkind = 'r'
and     pga.attnum > 0
```

Variant 2: for when you know the schema and/or table name.

```
select  pgn.nspname as schema_name,
        pgc.relname as table_name,
        pga.attname as column_name,
        pga.attisdistkey as is_distkey,
        pga.attsortkeyord as sortkey_order
from    pg_attribute pga
join    pg_class pgc on pgc.oid = pga.attrelid
join    pg_namespace pgn on pgn.oid = pgc.relnamespace
where   pgc.relkind = 'r'
and     pga.attnum > 0
and     schema_name like '%X%'
and     table_name like '%X%'
order   by pgn.nspname, pgc.relname, pga.attnum
```


# Dependencies of a view

```
select  *
from    information_schema.view_table_usage
where   view_name like '%SOMETHING%';
```

```
select  *
from    information_schema.view_table_usage
where   table_name like '%SOMETHING%';
```


# Identify user

```
select  *
from    pg_user
where   usesysid = 103;
```
