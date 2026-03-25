import type { SupabaseClient } from "@supabase/supabase-js";
import type { Database } from "./types";

export async function submitLead(
  client: SupabaseClient<Database>,
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
  const { error } = await client.from("leads").insert({
    site_id: siteId,
    contact_type: contactType || "email",
    contact_value: contactValue.trim(),
    metadata: metadata || {},
  });

  if (error?.code === "23505") return { status: "duplicate" } as const;
  if (error) return { status: "error", message: error.message } as const;
  return { status: "ok" } as const;
}
