-- Split the Enclava brand into enclava.ai and enclava.dev.
-- Historical leads stay on site_id = 'enclava'.
insert into sites (id, name, url) values
  ('enclava-ai', 'Enclava AI', 'https://enclava.ai'),
  ('enclava-dev', 'Enclava Dev', 'https://enclava.dev')
on conflict (id) do update
  set name = excluded.name,
      url = excluded.url;
