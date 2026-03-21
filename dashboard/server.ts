import express from "express";
import { execFile } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join, resolve } from "node:path";
import { promisify } from "node:util";

const execFileAsync = promisify(execFile);

const app = express();
const PORT = 6666;

const REPO_ROOT = resolve(import.meta.dirname, "..");
const PROJECTS_DIR = join(REPO_ROOT, "projects");
const STATUS_SCRIPT = join(REPO_ROOT, "tooling", "python", "project_status.py");

app.use(express.static(join(import.meta.dirname, "dist")));

async function listProjectNames(): Promise<string[]> {
  const entries = await readdir(PROJECTS_DIR, { withFileTypes: true });
  return entries
    .filter((e) => e.isDirectory() && e.name !== "legacy" && !e.name.startsWith("."))
    .map((e) => e.name)
    .sort();
}

async function getProjectStatus(name: string) {
  const projectPath = join(PROJECTS_DIR, name);
  const { stdout } = await execFileAsync(
    "uv",
    ["run", STATUS_SCRIPT, "--project", projectPath, "--json", "/dev/stdout"],
    {
      cwd: join(REPO_ROOT, "tooling", "python"),
      timeout: 15000,
    }
  );

  const jsonEnd = stdout.lastIndexOf("}");
  const jsonStr = stdout.slice(0, jsonEnd + 1);
  return JSON.parse(jsonStr);
}

app.get("/api/projects", async (_req, res) => {
  try {
    const names = await listProjectNames();
    const statuses = await Promise.all(
      names.map(async (name) => {
        try {
          return await getProjectStatus(name);
        } catch {
          return { project_name: name, error: true, completion_percentage: 0, stages: {} };
        }
      })
    );
    res.json(statuses);
  } catch (err) {
    res.status(500).json({ error: String(err) });
  }
});

app.get("/api/projects/:name", async (req, res) => {
  try {
    const status = await getProjectStatus(req.params.name);
    res.json(status);
  } catch (err) {
    res.status(500).json({ error: String(err) });
  }
});

app.get("/api/pipeline", (_req, res) => {
  res.json({
    stages: [
      { id: "01_protocol", name: "Protocol Development", depends_on: [] },
      { id: "02_search", name: "Literature Search", depends_on: ["01_protocol"] },
      { id: "03_screening", name: "Title/Abstract Screening", depends_on: ["02_search"] },
      { id: "04_fulltext", name: "Full-text Retrieval", depends_on: ["03_screening"] },
      { id: "05_extraction", name: "Data Extraction", depends_on: ["04_fulltext"] },
      { id: "06_analysis", name: "Meta-Analysis", depends_on: ["05_extraction"] },
      { id: "07_manuscript", name: "Manuscript Assembly", depends_on: ["06_analysis"] },
      { id: "08_reviews", name: "GRADE Assessment", depends_on: ["07_manuscript"] },
      { id: "09_qa", name: "Quality Assurance", depends_on: ["08_reviews"] },
    ],
  });
});

app.get("/{*path}", (_req, res) => {
  res.sendFile(join(import.meta.dirname, "dist", "index.html"));
});

app.listen(PORT, () => {
  console.log(`Meta-Pipe Dashboard running at http://localhost:${PORT}`);
});
