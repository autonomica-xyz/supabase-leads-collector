import { createClient } from "@supabase/supabase-js";
import type { Database } from "./types";

export function createLeadsClient(supabaseUrl: string, supabaseAnonKey: string) {
  return createClient<Database>(supabaseUrl, supabaseAnonKey);
}
