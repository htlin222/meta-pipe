interface HeaderProps {
  projectCount: number;
}

export default function Header({ projectCount }: HeaderProps) {
  return (
    <header className="flex items-center justify-between mb-8">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Meta-Pipe Dashboard
        </h1>
        <p className="text-sm text-gray-500 mt-1">
          {projectCount} project{projectCount !== 1 ? "s" : ""} tracked
        </p>
      </div>
      <div className="text-xs text-gray-600">
        Auto-refresh 30s
      </div>
    </header>
  );
}
