# Supabase leads collector

A shared Supabase backend for collecting leads across multiple landing pages. Instead of each site managing its own database, they all write to one place.

## How it works

Two tables:

- `sites` — a registry of known sites (e.g. `autonomica`, `enclava`)
- `leads` — contact submissions tagged with which site they came from

Each lead has a `site_id`, a `contact_type` (defaults to `email`), and a `contact_value`. Duplicate submissions are silently ignored.

Row-level security is on: anonymous users can insert leads, but cannot read, update, or delete anything.

## Database setup

Apply the migration to your Supabase project:

```bash
supabase db push
```

Or run the SQL directly from `supabase/migrations/001_create_leads.sql`.

Add your sites to the `sites` table before accepting leads.

## Usage

```ts
import { createLeadsClient, submitLead } from "@leads/supabase-backend";

const client = createLeadsClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const result = await submitLead(client, {
  siteId: "my-site",
  contactValue: "user@example.com",
});

// result.status: "ok" | "duplicate" | "error"
```

`contactType` defaults to `email` but can be anything — `phone`, `twitter`, `discord`, etc. There's no enforced list; just be consistent across your sites.

```ts
await submitLead(client, {
  siteId: "my-site",
  contactType: "phone",
  contactValue: "+1 555 000 0000",
});
```

`submitLead` returns one of three statuses:

| Status | Meaning |
|--------|---------|
| `ok` | Lead saved |
| `duplicate` | Already exists, no action taken |
| `error` | Something went wrong (check `result.message`) |

## Structure

```
src/
  client.ts    — typed Supabase client
  submit.ts    — submitLead()
  types.ts     — generated database types
supabase/
  migrations/  — SQL schema
```
