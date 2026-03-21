import type { ProjectStatus } from "../types";
import { PIPELINE_STAGES } from "../types";

interface DependencyGraphProps {
  project: ProjectStatus | null;
}

function nodeStyle(project: ProjectStatus | null, stageId: string) {
  if (!project) return "border-gray-800 text-gray-600";
  const stage = project.stages[stageId];
  if (!stage) return "border-gray-800 text-gray-600";
  if (stage.validated) return "border-gray-400 text-gray-200";
  if (stage.exists) return "border-gray-600 text-gray-400";
  return "border-gray-800 text-gray-600";
}

export default function DependencyGraph({ project }: DependencyGraphProps) {
  return (
    <div className="border border-gray-800 rounded-lg p-4 mb-6">
      <div className="flex items-center gap-3 mb-3">
        <h3 className="text-xs font-mono text-gray-500 uppercase tracking-wider">
          Pipeline
        </h3>
        {project && (
          <span className="text-xs font-mono text-gray-600">
            {project.project_name}
          </span>
        )}
      </div>
      <div className="flex items-center gap-1 overflow-x-auto pb-1">
        {PIPELINE_STAGES.map((stage, i) => (
          <div key={stage.id} className="flex items-center shrink-0">
            <div
              className={`px-2 py-1 rounded border text-xs font-mono ${nodeStyle(project, stage.id)}`}
              title={stage.name}
            >
              {stage.id.replace("_", " ")}
            </div>
            {i < PIPELINE_STAGES.length - 1 && (
              <span className="text-gray-700 mx-0.5 text-xs">&rarr;</span>
            )}
          </div>
        ))}
      </div>
      <div className="flex gap-4 mt-2 text-xs text-gray-600 font-mono">
        <span>+ complete</span>
        <span>~ in progress</span>
        <span>- not started</span>
      </div>
    </div>
  );
}
