import type { ProjectStatus } from "../types";

interface ProjectCardProps {
  project: ProjectStatus;
  selected: boolean;
  onClick: () => void;
}

function stageBrightness(validated: boolean, exists: boolean) {
  if (validated) return "bg-gray-300";
  if (exists) return "bg-gray-500";
  return "bg-gray-800";
}

export default function ProjectCard({ project, selected, onClick }: ProjectCardProps) {
  const stages = Object.values(project.stages);

  return (
    <button
      onClick={onClick}
      className={`w-full text-left rounded-lg p-4 transition-colors cursor-pointer border ${
        selected
          ? "bg-gray-900 border-gray-500"
          : "bg-gray-950 border-gray-800 hover:border-gray-600"
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <h2 className="font-mono text-sm truncate">{project.project_name}</h2>
        <span className="font-mono text-sm tabular-nums text-gray-400">
          {project.completion_percentage}%
        </span>
      </div>

      <div className="w-full bg-gray-800 rounded-full h-1.5 mb-2">
        <div
          className="bg-gray-400 h-1.5 rounded-full transition-all duration-500"
          style={{ width: `${project.completion_percentage}%` }}
        />
      </div>

      <div className="flex gap-0.5">
        {stages.map((s) => (
          <div
            key={s.stage}
            className={`h-1.5 flex-1 rounded-sm ${stageBrightness(s.validated, s.exists)}`}
            title={`${s.stage}: ${s.name}`}
          />
        ))}
      </div>

      {project.current_stage && (
        <p className="text-xs text-gray-600 mt-2 truncate font-mono">
          {project.next_action}
        </p>
      )}
    </button>
  );
}
