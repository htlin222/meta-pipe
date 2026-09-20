import type { ProjectStatus } from "./types";

const BASE = "/api";

export async function fetchProjects(): Promise<ProjectStatus[]> {
  const res = await fetch(`${BASE}/projects`);
  if (!res.ok) throw new Error(`Failed to fetch projects: ${res.status}`);
  return res.json();
}

export async function fetchProject(name: string): Promise<ProjectStatus> {
  const res = await fetch(`${BASE}/projects/${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error(`Failed to fetch project: ${res.status}`);
  return res.json();
}
