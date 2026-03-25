export async function submitLead(
  supabaseUrl: string,
  supabaseAnonKey: string,
  {
    siteId,
    contactType,
    contactValue,
    metadata,
  }: {
    siteId: string;
    contactType?: string;
    contactValue: string;
    metadata?: Record<string, unknown>;
  },
) {
  const res = await fetch(`${supabaseUrl}/rest/v1/leads`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: supabaseAnonKey,
      Authorization: `Bearer ${supabaseAnonKey}`,
      Prefer: "return=minimal",
    },
    body: JSON.stringify({
      site_id: siteId,
      contact_type: contactType ?? "email",
      contact_value: contactValue.trim(),
      metadata: metadata ?? {},
    }),
  });

  if (res.ok) return { status: "ok" } as const;

  const body = await res.json().catch(() => null);
  if (body?.code === "23505") return { status: "duplicate" } as const;
  return { status: "error", message: body?.message ?? res.statusText } as const;
}
