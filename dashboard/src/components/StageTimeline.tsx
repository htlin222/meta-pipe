import type { ProjectStatus } from "../types";
import { PIPELINE_STAGES } from "../types";

interface StageTimelineProps {
  project: ProjectStatus;
}

export default function StageTimeline({ project }: StageTimelineProps) {
  return (
    <div className="border border-gray-800 rounded-lg p-5">
      <h3 className="text-sm font-mono text-gray-400 mb-4">
        {project.project_name}
      </h3>

      <div className="space-y-0">
        {PIPELINE_STAGES.map((def) => {
          const stage = project.stages[def.id];
          if (!stage) return null;

          const isCurrent = project.current_stage === def.id;

          return (
            <div
              key={def.id}
              className={`flex items-start gap-3 py-2 px-3 rounded ${
                isCurrent ? "bg-gray-900" : ""
              }`}
            >
              <div className="mt-0.5 font-mono text-xs w-4 text-center shrink-0">
                {stage.validated ? "+" : stage.exists ? "~" : "-"}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-gray-500">
                    {def.id}
                  </span>
                  <span className={`text-sm ${stage.validated ? "text-gray-200" : stage.exists ? "text-gray-400" : "text-gray-600"}`}>
                    {stage.name}
                  </span>
                  {isCurrent && (
                    <span className="text-xs text-gray-500 border border-gray-700 px-1.5 py-0 rounded font-mono">
                      current
                    </span>
                  )}
                </div>

                {stage.exists && (
                  <div className="flex gap-3 mt-0.5 text-xs text-gray-600 font-mono">
                    <span>{stage.file_count} files</span>
                    {stage.last_modified && (
                      <span>
                        {new Date(stage.last_modified).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                )}

                {stage.key_files_missing.length > 0 && (
                  <div className="mt-0.5 text-xs text-gray-500 font-mono">
                    missing: {stage.key_files_missing.join(", ")}
                  </div>
                )}

                {stage.key_files_present.length > 0 && (
                  <div className="mt-0.5 text-xs text-gray-600 font-mono">
                    {stage.key_files_present.join(", ")}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
