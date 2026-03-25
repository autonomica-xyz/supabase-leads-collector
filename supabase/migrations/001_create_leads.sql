-- Sites registry
create table sites (
  id text primary key,
  name text not null,
  url text,
  created_at timestamptz default now()
);

-- Seed known sites
insert into sites (id, name, url) values
  ('autonomica', 'Autonomica', 'https://autonomica.xyz'),
  ('enclava', 'Enclava', null),
  ('freedom-cash', 'Freedom Cash', null);

-- Leads table
create table leads (
  id uuid primary key default gen_random_uuid(),
  site_id text not null references sites(id),
  contact_type text not null default 'email',
  contact_value text not null,
  metadata jsonb default '{}',
  created_at timestamptz default now(),
  unique (site_id, contact_type, contact_value)
);

create index idx_leads_site on leads(site_id);
create index idx_leads_created on leads(created_at desc);

-- RLS: anon can only INSERT
alter table leads enable row level security;

create policy "anon_insert_leads"
  on leads for insert
  to anon
  with check (true);
