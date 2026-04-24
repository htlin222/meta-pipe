import { useState } from "react";
import Header from "./components/Header";
import ProjectCard from "./components/ProjectCard";
import StageTimeline from "./components/StageTimeline";
import DependencyGraph from "./components/DependencyGraph";
import { useProjects } from "./hooks/useProjects";

export default function App() {
  const { projects, loading, error } = useProjects();
  const [selectedName, setSelectedName] = useState<string | null>(null);

  const selectedProject =
    projects.find((p) => p.project_name === selectedName) ?? null;

  if (!selectedName && projects.length > 0) {
    setSelectedName(projects[0].project_name);
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-mono">
        <p className="text-gray-400">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 max-w-7xl mx-auto font-mono">
      <Header projectCount={projects.length} />

      {loading ? (
        <p className="text-gray-500 text-sm">Loading...</p>
      ) : (
        <>
          <DependencyGraph project={selectedProject} />

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
            <div className="space-y-2">
              {projects.map((p) => (
                <ProjectCard
                  key={p.project_name}
                  project={p}
                  selected={p.project_name === selectedName}
                  onClick={() => setSelectedName(p.project_name)}
                />
              ))}
            </div>

            <div className="lg:col-span-2">
              {selectedProject && <StageTimeline project={selectedProject} />}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
