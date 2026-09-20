export interface StageStatus {
  stage: string;
  name: string;
  exists: boolean;
  validated: boolean;
  key_files_present: string[];
  key_files_missing: string[];
  file_count: number;
  last_modified: string | null;
}

export interface ProjectStatus {
  project_name: string;
  project_root: string;
  timestamp: string;
  stages: Record<string, StageStatus>;
  current_stage: string | null;
  completion_percentage: number;
  next_action: string;
}

export interface PipelineStage {
  id: string;
  name: string;
  depends_on: string[];
}

export const PIPELINE_STAGES: PipelineStage[] = [
  { id: "01_protocol", name: "Protocol", depends_on: [] },
  { id: "02_search", name: "Search", depends_on: ["01_protocol"] },
  { id: "03_screening", name: "Screening", depends_on: ["02_search"] },
  { id: "04_fulltext", name: "Full-text", depends_on: ["03_screening"] },
  { id: "05_extraction", name: "Extraction", depends_on: ["04_fulltext"] },
  { id: "06_analysis", name: "Analysis", depends_on: ["05_extraction"] },
  { id: "07_manuscript", name: "Manuscript", depends_on: ["06_analysis"] },
  { id: "08_reviews", name: "Reviews", depends_on: ["07_manuscript"] },
  { id: "09_qa", name: "QA", depends_on: ["08_reviews"] },
];
