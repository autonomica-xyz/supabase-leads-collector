#!/usr/bin/env python3
"""
Set Supabase env vars across Vercel projects.
Usage: VERCEL_TOKEN=xxx python3 scripts/set_vercel_env.py
"""

import json
import os
import sys
import urllib.request
import urllib.error

VERCEL_TOKEN = os.environ.get("VERCEL_TOKEN")
if not VERCEL_TOKEN:
    print("Error: VERCEL_TOKEN env var is required")
    sys.exit(1)

API_BASE = "https://api.vercel.com"
HEADERS = {
    "Authorization": f"Bearer {VERCEL_TOKEN}",
    "Content-Type": "application/json",
}

SUPABASE_URL = "https://vksgbaecppvkhmvlphfg.supabase.co"
SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZrc2diYWVjcHB2a2htdmxwaGZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NDA3MjksImV4cCI6MjA4OTIxNjcyOX0"
    ".epRL09jxk9NFjoMbHD5XaosFwiB9C56YbFPRE5w0UGw"
)

# Project name -> env vars to set
PROJECTS = {
    "autonomica-landing-page-2": {
        "LEADS_SUPABASE_URL": SUPABASE_URL,
        "LEADS_SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
    },
    "enclava": {
        "VITE_LEADS_SUPABASE_URL": SUPABASE_URL,
        "VITE_LEADS_SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
    },
    "freedom-cash": {
        "VITE_LEADS_SUPABASE_URL": SUPABASE_URL,
        "VITE_LEADS_SUPABASE_ANON_KEY": SUPABASE_ANON_KEY,
    },
}

TARGETS = ["production", "preview", "development"]


def api(method, path, body=None):
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def get_projects():
    result = api("GET", "/v9/projects?limit=100")
    return {p["name"]: p["id"] for p in result.get("projects", [])}


def get_existing_env(project_id):
    result = api("GET", f"/v9/projects/{project_id}/env")
    return {e["key"]: e["id"] for e in result.get("envs", [])}


def set_env(project_id, key, value, existing_ids):
    if key in existing_ids:
        env_id = existing_ids[key]
        api("PATCH", f"/v9/projects/{project_id}/env/{env_id}", {
            "value": value,
            "target": TARGETS,
        })
        return "updated"
    else:
        api("POST", f"/v9/projects/{project_id}/env", {
            "key": key,
            "value": value,
            "target": TARGETS,
            "type": "plain",
        })
        return "created"


def main():
    print("Fetching Vercel projects...")
    all_projects = get_projects()

    for project_name, env_vars in PROJECTS.items():
        if project_name not in all_projects:
            print(f"\n⚠  Project '{project_name}' not found — skipping")
            print(f"   Available: {', '.join(sorted(all_projects))}")
            continue

        project_id = all_projects[project_name]
        print(f"\n{project_name} ({project_id})")

        existing = get_existing_env(project_id)

        for key, value in env_vars.items():
            action = set_env(project_id, key, value, existing)
            print(f"  {action:8s} {key}")

    print("\nDone.")


if __name__ == "__main__":
    main()
