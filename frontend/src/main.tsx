import { StrictMode, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Marker,
  MapContainer,
  Polyline,
  TileLayer,
  Tooltip,
  useMap,
} from "react-leaflet";
import { divIcon } from "leaflet";
import {
  Droplets,
  Battery,
  Flame,
  House,
  Leaf,
  Moon,
  Sun,
  Wind,
  Zap,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { renderToStaticMarkup } from "react-dom/server";
import "leaflet/dist/leaflet.css";
import "./styles.css";
import { finiteCoordinates, type MapCoordinates } from "./mapGeometry";
import { getCountryContext } from "./countryContext";
import { TopologyLayout } from "./TopologyLayout";
import type { Entity } from "./visualizerTypes";

/*
type Entity = {
  id: string;
  source_code: string;
  name: string;
  technology: string;
  asset_type: string;
  system_code?: string | null;
  bus?: number;
  capacity_mw: number | null;
  operating_factor?: number;
  source_file: string;
  source_line: number;
  latitude?: number | null;
  longitude?: number | null;
  coordinate_status?: string;
  lifecycle_status: string;
  is_active: boolean;
  modifications: {
    source_file: string;
    source_line: number;
    effective_date: string;
  }[];
}; */
type Circuit = {
  source_code: string;
  from_bus: string;
  to_bus: string;
  system_code?: string | null;
  from_system_code?: string | null;
  to_system_code?: string | null;
  is_interconnection?: boolean;
  from_latitude?: number | null;
  from_longitude?: number | null;
  to_latitude?: number | null;
  to_longitude?: number | null;
  nominal_voltage_kv?: number | null;
  name: string;
  normal_limit_mw?: number;
  status: string;
};
type Maintenance = {
  asset_type: string;
  source_code: string;
  value: number | null;
  measure_type: number;
  unit_type: number;
  warnings: string[];
};
type Snapshot = {
  stage: number;
  block: number;
  as_of: string;
  study: {
    initial_year: number;
    stages: number;
    blocks: number;
    frequency: string;
    warnings: string[];
    block_durations_hours?: Record<string, number[]>;
    systems: { code: string; name: string; country_code?: string }[];
    layout: string;
  };
  entities: Entity[];
  buses: {
    source_code: string;
    system_code?: string | null;
    nominal_voltage_kv?: number | null;
    demand_mw?: number;
    primary_source?: {
      source_code: string;
      name: string;
      technology?: string;
      capacity_mw: number | null;
    };
    latitude?: number | null;
    longitude?: number | null;
  }[];
  circuits: Circuit[];
  maintenance: Maintenance[];
  demands: {
    source_code: string;
    segment: number;
    system_code?: string | null;
    value_gwh: number | null;
  }[];
  provenance: string;
};
type Project = { id: number; name: string };
type Revision = {
  id: number;
  revision_number: number;
  status: string;
  is_active: boolean;
};
type ImportRun = {
  id: number;
  project_id: number;
  source_path: string;
  status: string;
  files_total: number;
  files_processed: number;
  files_binary: number;
  errors: number;
  message: string | null;
};
type Placed = { entity: Entity; coordinates: MapCoordinates };
type NodeGroup = {
  key: string;
  coordinates: [number, number];
  items: Placed[];
};

function MapViewport({ coordinates }: { coordinates: MapCoordinates[] }) {
  const map = useMap();
  useEffect(() => {
    if (coordinates.length === 1) map.setView(coordinates[0], 8);
    else if (coordinates.length > 1)
      map.fitBounds(coordinates, { padding: [28, 28] });
  }, [coordinates, map]);
  return null;
}

function CountryViewport({
  bounds,
}: {
  bounds: [[number, number], [number, number]];
}) {
  const map = useMap();
  useEffect(() => {
    map.fitBounds(bounds, { padding: [24, 24] });
  }, [bounds, map]);
  return null;
}

const technologyMeta: Record<
  string,
  { label: string; color: string; Icon: LucideIcon }
> = {
  hydro: { label: "Hydro", color: "#2E9BB3", Icon: Droplets },
  thermal: { label: "Thermal", color: "#D8794A", Icon: Flame },
  wind: { label: "Wind", color: "#6F8FE8", Icon: Wind },
  solar: { label: "Solar", color: "#D6A72E", Icon: Sun },
  biomass: { label: "Biomass", color: "#62A66F", Icon: Leaf },
  unknown: { label: "Generator", color: "#7D919E", Icon: Zap },
  battery: { label: "Battery", color: "#C58B35", Icon: Battery },
};
const apiBase = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";
const tenantId = import.meta.env.VITE_TENANT_ID ?? "1";
const configuredProjectId = import.meta.env.VITE_PROJECT_ID
  ? Number(import.meta.env.VITE_PROJECT_ID)
  : undefined;

async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiBase}${path}`, {
    ...init,
    headers: { "X-Tenant-ID": tenantId, ...(init?.headers ?? {}) },
  });
  if (!response.ok)
    throw new Error(`${response.status}: ${await response.text()}`);
  return response.json() as Promise<T>;
}

function normalizeTechnology(assetType: string, technology: string) {
  const value = `${assetType} ${technology}`.toUpperCase();
  if (assetType === "battery") return "battery";
  if (assetType === "hydro") return "hydro";
  if (value.includes("EOL") || value.includes("WIND")) return "wind";
  if (value.includes("SOL") || value.includes("PV")) return "solar";
  if (value.includes("BIC") || value.includes("BIOM")) return "biomass";
  if (
    assetType === "thermal" ||
    value.includes("TERM") ||
    value.includes("LNG") ||
    value.includes("TGD")
  )
    return "thermal";
  return "unknown";
}

function TechnologyIcon({
  technology,
  size = 16,
}: {
  technology: string;
  size?: number;
}) {
  const Icon = (technologyMeta[technology] ?? technologyMeta.unknown).Icon;
  return <Icon size={size} strokeWidth={2} aria-hidden="true" />;
}

function markerIcon(technology: string, count: number) {
  const meta = technologyMeta[technology] ?? technologyMeta.unknown;
  const icon = renderToStaticMarkup(
    <TechnologyIcon technology={technology} size={18} />,
  );
  return divIcon({
    className: "generator-marker-wrapper",
    html: `<span class="generator-marker" style="--marker-color:${meta.color}">${icon}${count > 1 ? `<b>${count}</b>` : ""}</span>`,
    iconSize: [34, 34],
    iconAnchor: [17, 17],
  });
}

function demandMarkerIcon() {
  const icon = renderToStaticMarkup(<House size={16} strokeWidth={2} />);
  return divIcon({
    className: "demand-marker-wrapper",
    html: `<span class="demand-marker" aria-hidden="true">${icon}</span>`,
    iconSize: [28, 28],
    iconAnchor: [14, 14],
  });
}

function App() {
  const [projectId, setProjectId] = useState<number | undefined>(
    configuredProjectId,
  );
  const [projects, setProjects] = useState<Project[]>([]);
  const [revisions, setRevisions] = useState<Revision[]>([]);
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [selectedId, setSelectedId] = useState("");
  const [selectedSystem, setSelectedSystem] = useState("all");
  const [selectedVoltage, setSelectedVoltage] = useState("all");
  const [showDemandReferences, setShowDemandReferences] = useState(false);
  const [countryMapOpen, setCountryMapOpen] = useState(
    () => localStorage.getItem("gme-country-map") !== "hidden",
  );
  const [stage, setStage] = useState(1);
  const [block, setBlock] = useState(1);
  const [theme, setTheme] = useState<"dark" | "light">(
    () =>
      (localStorage.getItem("gme-theme") as "dark" | "light" | null) ??
      (window.matchMedia("(prefers-color-scheme: light)").matches
        ? "light"
        : "dark"),
  );
  const [view, setView] = useState<"map" | "files">("map");
  const [status, setStatus] = useState<"loading" | "connected" | "error">(
    "loading",
  );
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  const [openNode, setOpenNode] = useState<string | null>(null);
  const [importRun, setImportRun] = useState<ImportRun | null>(null);
  const [newProjectName, setNewProjectName] = useState("");
  const [creatingProject, setCreatingProject] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    localStorage.setItem("gme-theme", theme);
  }, [theme]);
  useEffect(() => {
    api<Project[]>("/api/projects")
      .then((items) => {
        setProjects(items);
        if (!projectId && items[0]) setProjectId(items[0].id);
      })
      .catch((reason: Error) => {
        setStatus("error");
        setError(reason.message);
      });
  }, []);
  useEffect(() => {
    if (!projectId) return;
    setStatus("loading");
    Promise.all([
      api<Snapshot>(
        `/api/projects/${projectId}/snapshot?stage=${stage}&block=${block}`,
      ),
      api<Revision[]>(`/api/projects/${projectId}/revisions`),
    ])
      .then(([nextSnapshot, nextRevisions]) => {
        setSnapshot(nextSnapshot);
        setRevisions(nextRevisions);
        setStatus("connected");
        setError("");
        setSelectedSystem((current) =>
          current === "all" ||
          nextSnapshot.study.systems.some((system) => system.code === current)
            ? current
            : "all",
        );
        if (!nextSnapshot.entities.some((item) => item.id === selectedId))
          setSelectedId(nextSnapshot.entities[0]?.id ?? "");
      })
      .catch((reason: Error) => {
        setStatus("error");
        setError(reason.message);
        setSnapshot(null);
      });
  }, [projectId, stage, block]);
  useEffect(() => {
    if (!importRun || ["completed", "failed"].includes(importRun.status))
      return;
    const timer = window.setInterval(() => {
      api<ImportRun>(
        `/api/projects/${importRun.project_id}/imports/${importRun.id}`,
      )
        .then(setImportRun)
        .catch(() => undefined);
    }, 1000);
    return () => window.clearInterval(timer);
  }, [importRun]);

  const normalizedEntities = useMemo(
    () =>
      (snapshot?.entities ?? []).map((entity) => ({
        ...entity,
        technology: normalizeTechnology(entity.asset_type, entity.technology),
      })),
    [snapshot],
  );
  const systemEntities = normalizedEntities.filter(
    (entity) =>
      selectedSystem === "all" || entity.system_code === selectedSystem,
  );
  const systemBuses = (snapshot?.buses ?? []).filter(
    (bus) => selectedSystem === "all" || bus.system_code === selectedSystem,
  );
  const voltageOptions = Array.from(
    new Set(
      systemBuses
        .map((bus) => bus.nominal_voltage_kv)
        .filter(
          (value): value is number => value !== null && value !== undefined,
        ),
    ),
  ).sort((a, b) => b - a);
  const voltageMatches = (value?: number | null) =>
    selectedVoltage === "all" ||
    (selectedVoltage === "unknown"
      ? value == null
      : value === Number(selectedVoltage));
  const visibleBuses = systemBuses.filter((bus) =>
    voltageMatches(bus.nominal_voltage_kv),
  );
  const demandBuses = visibleBuses.filter((bus) => (bus.demand_mw ?? 0) > 0);
  const systemDemands = (snapshot?.demands ?? []).filter(
    (demand) =>
      selectedSystem === "all" || demand.system_code === selectedSystem,
  );
  const demandTotalGwh = systemDemands.reduce(
    (total, demand) => total + (demand.value_gwh ?? 0),
    0,
  );
  const systemCircuits = (snapshot?.circuits ?? []).filter(
    (circuit) =>
      selectedSystem === "all" ||
      circuit.from_system_code === selectedSystem ||
      circuit.to_system_code === selectedSystem,
  );
  const visibleCircuits = systemCircuits.filter(
    (circuit) =>
      voltageMatches(circuit.nominal_voltage_kv) || circuit.is_interconnection,
  );
  const placed = systemEntities.flatMap((entity) => {
    const coordinates = finiteCoordinates(entity.latitude, entity.longitude);
    return coordinates ? [{ entity, coordinates }] : [];
  });
  const located = placed.filter((item) => item.entity.is_active);
  const unlocated = systemEntities.filter(
    (entity) =>
      !entity.is_active ||
      !finiteCoordinates(entity.latitude, entity.longitude),
  );
  const nodeGroups = useMemo(
    () =>
      Array.from(
        located
          .reduce((groups, item) => {
            const key =
              item.entity.bus?.toString() ?? item.coordinates.join(",");
            const group = groups.get(key) ?? {
              key,
              coordinates: item.coordinates,
              items: [] as Placed[],
            };
            group.items.push(item);
            groups.set(key, group);
            return groups;
          }, new Map<string, NodeGroup>())
          .values(),
      ),
    [located],
  );
  const selected =
    systemEntities.find((entity) => entity.id === selectedId) ??
    systemEntities[0];
  const systemCoordinates = visibleBuses.flatMap((bus) => {
    const coordinates = finiteCoordinates(bus.latitude, bus.longitude);
    return coordinates ? [coordinates] : [];
  });
  const projectName =
    projects.find((item) => item.id === projectId)?.name ??
    "No project selected";
  const maxStage = snapshot?.study.stages || 1;
  const maxBlock = snapshot?.study.blocks || 1;
  const geographicLayout = snapshot?.study.layout !== "topology layout";
  const selectedSystemInfo = snapshot?.study.systems.find(
    (system) => system.code === selectedSystem,
  );
  const countryContext = getCountryContext(selectedSystemInfo?.country_code);
  const selectedMaintenance =
    selected &&
    snapshot?.maintenance.find(
      (item) =>
        item.source_code === selected.source_code &&
        item.asset_type === selected.asset_type,
    );
  const blockDuration =
    snapshot?.study.block_durations_hours?.[String(stage)]?.[block - 1];
  const inputState =
    selectedMaintenance?.value && selectedMaintenance.value > 0
      ? "maintenance"
      : selected?.modifications.length
        ? "modified"
        : selected?.is_active
          ? "base"
          : "future";

  async function upload(file: File) {
    if (!projectId) return;
    setUploading(true);
    setError("");
    const form = new FormData();
    form.append("file", file);
    try {
      const run = await api<ImportRun>(`/api/projects/${projectId}/imports`, {
        method: "POST",
        body: form,
      });
      setImportRun(run);
      setView("files");
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }

  async function createProject() {
    if (!newProjectName.trim()) return;
    setCreatingProject(true);
    try {
      const project = await api<Project>("/api/projects", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newProjectName.trim() }),
      });
      setProjects((items) => [...items, project]);
      setProjectId(project.id);
      setNewProjectName("");
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : "Project creation failed",
      );
    } finally {
      setCreatingProject(false);
    }
  }

  const importDetails = (() => {
    try {
      return JSON.parse(importRun?.message ?? "{}") as {
        phase?: string;
        progress?: number;
        logs?: string[];
      };
    } catch {
      return {};
    }
  })();

  return (
    <main className={`workspace theme-${theme}`}>
      <aside className="rail">
        <div className="rail-logo">
          GME<span>·</span>PX
        </div>
        <nav aria-label="Workspace navigation">
          <button
            className={view === "map" ? "nav-active" : ""}
            onClick={() => setView("map")}
          >
            01 <span>System map</span>
          </button>
          <button
            className={view === "files" ? "nav-active" : ""}
            onClick={() => setView("files")}
          >
            02 <span>Files</span>
          </button>
          <button>
            03 <span>Mappings</span>
          </button>
          <button>
            04 <span>Exports</span>
          </button>
        </nav>
        <div className="rail-foot">
          SDDP
          <br />
          <span>WORKSPACE</span>
        </div>
      </aside>
      <section className="content">
        <header className="topbar">
          <div>
            <span className="eyebrow">GME / MODEL WORKSPACE</span>
            <h1>
              {projectName} <em>system view</em>
            </h1>
          </div>
          <div className="top-actions">
            <span className={`status-dot ${status}`} />{" "}
            {status === "connected"
              ? "LIVE INPUT"
              : status === "loading"
                ? "LOADING"
                : "API ERROR"}
            <button
              className="theme-toggle"
              onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
              aria-label={
                theme === "dark"
                  ? "Switch to light theme"
                  : "Switch to dark theme"
              }
              aria-pressed={theme === "dark"}
            >
              {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
            </button>
          </div>
        </header>
        <div className="context">
          <label>
            PROJECT{" "}
            <select
              aria-label="Project"
              value={projectId ?? ""}
              onChange={(event) => setProjectId(Number(event.target.value))}
            >
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            SYSTEM{" "}
            <select
              aria-label="System"
              value={selectedSystem}
              onChange={(event) => {
                setSelectedSystem(event.target.value);
                setSelectedId("");
              }}
            >
              <option value="all">All systems</option>
              {(snapshot?.study.systems ?? []).map((system) => (
                <option key={system.code} value={system.code}>
                  {system.name}
                </option>
              ))}
            </select>
          </label>
          <label>
            VOLTAGE{" "}
            <select
              aria-label="Voltage level"
              value={selectedVoltage}
              onChange={(event) => setSelectedVoltage(event.target.value)}
            >
              <option value="all">All voltage levels</option>
              {voltageOptions.map((voltage) => (
                <option key={voltage} value={voltage}>
                  {voltage} kV
                </option>
              ))}
              <option value="unknown">Unknown</option>
            </select>
          </label>
          <span>
            AS OF <strong>{snapshot?.as_of ?? "—"}</strong>
          </span>
          <span>
            HORIZON{" "}
            <strong>
              {snapshot ? `${maxStage} ${snapshot.study.frequency}` : "—"}
            </strong>
          </span>
          <span>
            BLOCK{" "}
            <strong>
              {block} / {maxBlock}
              {blockDuration !== undefined ? ` · ${blockDuration}h` : ""}
            </strong>
          </span>
          <span>
            LAYOUT <strong>{snapshot?.study.layout ?? "—"}</strong>
          </span>
          <span className="context-note">
            {snapshot
              ? `${located.length} / ${snapshot.entities.length} active assets located`
              : "Connect to backend to load a revision"}
          </span>
        </div>
        {snapshot &&
          (snapshot.study.warnings.length > 0 || systemDemands.length > 0) && (
            <section
              className="diagnostics-strip"
              aria-label="Study diagnostics"
            >
              {systemDemands.length > 0 && (
                <div className="diagnostic-item demand-diagnostic">
                  <House size={16} aria-hidden="true" />
                  <span>
                    <b>DEMAND</b>
                    {demandTotalGwh.toFixed(1)} GWh · {systemDemands.length}{" "}
                    source records for stage {stage}, block {block}
                  </span>
                  <label className="demand-toggle">
                    <input
                      type="checkbox"
                      checked={showDemandReferences}
                      onChange={(event) =>
                        setShowDemandReferences(event.target.checked)
                      }
                    />{" "}
                    Show references
                  </label>
                </div>
              )}
              {snapshot.study.warnings.map((warning) => (
                <div
                  className="diagnostic-item warning-diagnostic"
                  key={warning}
                >
                  <span>
                    <b>WARNING</b>
                    {warning}
                  </span>
                </div>
              ))}
            </section>
          )}
        {error && (
          <div className="api-error" role="alert">
            <strong>Backend unavailable</strong>
            <span>{error}</span>
            <button onClick={() => window.location.reload()}>Retry</button>
          </div>
        )}
        {view === "files" ? (
          <section className="files-view">
            <div className="panel-head">
              <div>
                <span className="eyebrow">02 / SOURCE CONTROL</span>
                <h2>Study imports</h2>
                <p>
                  Target project: <strong>{projectName}</strong>. Imports create
                  an immutable revision inside this project.
                </p>
              </div>
              <button
                className="upload-button"
                onClick={() => fileInput.current?.click()}
                disabled={
                  !projectId ||
                  uploading ||
                  Boolean(
                    importRun &&
                    !["completed", "failed"].includes(importRun.status),
                  )
                }
              >
                {uploading ? "UPLOADING..." : "IMPORT ZIP"}
              </button>
              <input
                ref={fileInput}
                type="file"
                accept=".zip"
                hidden
                onChange={(event) =>
                  event.target.files?.[0] && upload(event.target.files[0])
                }
              />
            </div>
            <div className="project-create">
              <label>
                NEW PROJECT{" "}
                <input
                  aria-label="New project name"
                  value={newProjectName}
                  onChange={(event) => setNewProjectName(event.target.value)}
                  placeholder="e.g. CRIE"
                />
              </label>
              <button
                className="upload-button"
                onClick={createProject}
                disabled={creatingProject || !newProjectName.trim()}
              >
                {creatingProject ? "CREATING..." : "CREATE PROJECT"}
              </button>
            </div>
            {importRun && (
              <div className={`import-console import-${importRun.status}`}>
                <div className="import-console-head">
                  <strong>IMPORT RUN #{importRun.id}</strong>
                  <span>
                    {importDetails.phase ?? importRun.status} ·{" "}
                    {importDetails.progress ?? 0}%
                  </span>
                </div>
                <div className="progress-track">
                  <span style={{ width: `${importDetails.progress ?? 0}%` }} />
                </div>
                <div className="import-stats">
                  <span>
                    {importRun.files_processed} / {importRun.files_total || "—"}{" "}
                    files
                  </span>
                  <span>{importRun.files_binary} binary artifacts</span>
                  <span>{importRun.errors} errors</span>
                </div>
                <div className="import-logs" aria-live="polite">
                  {(importDetails.logs ?? []).map((log, index) => (
                    <div key={`${index}-${log}`}>
                      <b>{String(index + 1).padStart(2, "0")}</b>
                      {log}
                    </div>
                  ))}
                </div>
              </div>
            )}
            <div className="revision-list">
              {revisions.map((revision) => (
                <div className="revision-row" key={revision.id}>
                  <span>REVISION {revision.revision_number}</span>
                  <strong>{revision.status}</strong>
                  <span>{revision.is_active ? "ACTIVE" : "ARCHIVED"}</span>
                </div>
              ))}
              {!revisions.length && (
                <p className="empty-state">
                  No revisions found for this project.
                </p>
              )}
            </div>
          </section>
        ) : (
          <>
            <div className="visual-grid">
              <section className="map-panel">
                <div className="panel-head">
                  <div>
                    <span className="eyebrow">01 / GEOGRAPHIC CONTEXT</span>
                    <h2>{projectName} input network</h2>
                  </div>
                  <div className="legend">
                    {[
                      "hydro",
                      "thermal",
                      "wind",
                      "solar",
                      "biomass",
                      "battery",
                    ].map((type) => (
                      <span key={type}>
                        <i className={`legend-icon ${type}`}>
                          <TechnologyIcon technology={type} size={12} />
                        </i>
                        {technologyMeta[type].label}
                      </span>
                    ))}
                    <span>
                      <i className="legend-icon demand">
                        <House size={12} />
                      </i>
                      Demand ({systemDemands.length || demandBuses.length})
                    </span>
                  </div>
                </div>
                <div className="map-canvas">
                  {snapshot && geographicLayout ? (
                    <MapContainer
                      center={[-32.9, -56]}
                      zoom={6}
                      scrollWheelZoom
                      className="leaflet-map"
                      aria-label="Geographic map of input assets"
                    >
                      <TileLayer
                        attribution="&copy; OpenStreetMap contributors"
                        url={
                          theme === "dark"
                            ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                        }
                      />
                      <MapViewport coordinates={systemCoordinates} />
                      {visibleCircuits.map((circuit) => {
                        const from = finiteCoordinates(
                          circuit.from_latitude,
                          circuit.from_longitude,
                        );
                        const to = finiteCoordinates(
                          circuit.to_latitude,
                          circuit.to_longitude,
                        );
                        return from && to ? (
                          <Polyline
                            key={circuit.source_code}
                            positions={[from, to]}
                            pathOptions={{
                              color: circuit.is_interconnection
                                ? "#d6a72e"
                                : "#5E7B90",
                              weight: circuit.is_interconnection ? 2 : 1,
                              opacity: 0.7,
                            }}
                          />
                        ) : null;
                      })}
                      {nodeGroups.map((group) => {
                        const preview = group.items[0].entity;
                        return (
                          <Marker
                            key={group.key}
                            position={group.coordinates}
                            icon={markerIcon(
                              preview.technology,
                              group.items.length,
                            )}
                            eventHandlers={{
                              click: () => {
                                setSelectedId(preview.id);
                                setOpenNode(
                                  group.items.length > 1 ? group.key : null,
                                );
                              },
                            }}
                          >
                            <Tooltip>
                              <span className="map-tooltip">
                                <TechnologyIcon
                                  technology={preview.technology}
                                  size={13}
                                />
                                {group.items.length > 1
                                  ? `${group.items.length} generators · `
                                  : ""}
                                {preview.name}
                              </span>
                            </Tooltip>
                          </Marker>
                        );
                      })}
                      {visibleBuses
                        .filter(
                          (bus) =>
                            (bus.demand_mw ?? 0) > 0 &&
                            (!bus.primary_source || showDemandReferences),
                        )
                        .flatMap((bus) => {
                          const position = finiteCoordinates(
                            bus.latitude,
                            bus.longitude,
                          );
                          return position
                            ? [
                                <Marker
                                  key={`demand-${bus.source_code}`}
                                  position={position}
                                  icon={demandMarkerIcon()}
                                >
                                  <Tooltip>
                                    <span className="map-tooltip">
                                      <House size={13} />
                                      Demand {bus.demand_mw?.toFixed(1)} MW ·
                                      BUS {bus.source_code}
                                      {bus.primary_source
                                        ? ` · Main source: ${bus.primary_source.name} (${bus.primary_source.capacity_mw ?? "—"} MW)`
                                        : ""}
                                    </span>
                                  </Tooltip>
                                </Marker>,
                              ]
                            : [];
                        })}
                    </MapContainer>
                  ) : snapshot && countryContext && countryMapOpen ? (
                    <MapContainer
                      center={countryContext.center}
                      zoom={5}
                      scrollWheelZoom
                      className="leaflet-map"
                      aria-label={`${countryContext.name} country context map`}
                    >
                      <TileLayer
                        attribution="&copy; OpenStreetMap contributors"
                        url={
                          theme === "dark"
                            ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
                            : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
                        }
                      />
                      <CountryViewport bounds={countryContext.bounds} />
                    </MapContainer>
                  ) : snapshot ? (
                    <div className="map-empty">
                      <strong>Country context unavailable</strong>
                      <span>
                        No reference bounds are registered for this system. The
                        derived topology remains available below.
                      </span>
                    </div>
                  ) : (
                    <div className="map-empty">
                      Waiting for an active study revision.
                    </div>
                  )}
                  <div className="map-overlay">
                    <span className="eyebrow">
                      {geographicLayout
                        ? "CARTOGRAPHIC BASE"
                        : "COUNTRY CONTEXT"}
                    </span>
                    <strong>
                      {geographicLayout
                        ? "Source coordinates from SDDP buses"
                        : countryContext
                          ? `${countryContext.name} reference bounds`
                          : "Geographic context unavailable"}
                    </strong>
                    <small>
                      {geographicLayout
                        ? "Shared nodes are grouped without shifting official coordinates."
                        : "Country context is reference geography only; assets use the derived topology below."}
                    </small>
                    {!geographicLayout && countryContext && (
                      <button
                        className="map-collapse"
                        onClick={() => {
                          setCountryMapOpen(false);
                          localStorage.setItem("gme-country-map", "hidden");
                        }}
                      >
                        {countryMapOpen
                          ? "Hide country map"
                          : "Show country map"}
                      </button>
                    )}
                  </div>
                </div>
                {!geographicLayout && countryContext && !countryMapOpen && (
                  <button
                    className="map-reopen"
                    onClick={() => {
                      setCountryMapOpen(true);
                      localStorage.removeItem("gme-country-map");
                    }}
                  >
                    Show country context map
                  </button>
                )}
                {!geographicLayout && snapshot && (
                  <section className="topology-panel">
                    <div className="panel-head">
                      <div>
                        <span className="eyebrow">DERIVED NETWORK VIEW</span>
                        <h2>{selectedSystemInfo?.name ?? "Study"} topology</h2>
                      </div>
                      <span className="topology-status">NOT GEOGRAPHIC</span>
                    </div>
                    <TopologyLayout
                      buses={visibleBuses}
                      circuits={visibleCircuits}
                      entities={systemEntities}
                      showDemandReferences={showDemandReferences}
                      onSelect={(entity) => setSelectedId(entity.id)}
                    />
                  </section>
                )}
                <div
                  className="node-grid"
                  aria-label="Generators by shared node"
                >
                  {nodeGroups
                    .filter(
                      (group) =>
                        group.items.length > 1 &&
                        (openNode === null || openNode === group.key),
                    )
                    .map((group) => (
                      <div className="node-cluster" key={group.key}>
                        <div className="node-cluster-head">
                          <strong>BUS {group.key}</strong>
                          <span>{group.items.length} generators</span>
                          <button
                            onClick={() =>
                              setOpenNode(
                                openNode === group.key ? null : group.key,
                              )
                            }
                            aria-label={`Toggle generators at bus ${group.key}`}
                          >
                            {openNode === group.key ? "CLOSE" : "OPEN"}
                          </button>
                        </div>
                        {(openNode === group.key || openNode === null) && (
                          <div className="cluster-items">
                            {group.items.map(({ entity }) => (
                              <button
                                key={entity.id}
                                className={`cluster-item ${entity.id === selected?.id ? "selected" : ""}`}
                                onClick={() => setSelectedId(entity.id)}
                                aria-label={`Select ${entity.name}`}
                              >
                                <span
                                  className="technology-icon"
                                  style={{
                                    color:
                                      technologyMeta[entity.technology].color,
                                  }}
                                >
                                  <TechnologyIcon
                                    technology={entity.technology}
                                  />
                                </span>
                                <span>
                                  <strong>{entity.name}</strong>
                                  <small>
                                    {technologyMeta[entity.technology].label} ·{" "}
                                    {entity.capacity_mw ?? "—"} MW
                                  </small>
                                </span>
                              </button>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                </div>
                <div className="asset-roster">
                  {normalizedEntities.map((entity) => (
                    <button
                      key={entity.id}
                      className={`asset-chip ${entity.id === selected?.id ? "selected" : ""}`}
                      onClick={() => setSelectedId(entity.id)}
                      aria-label={`Select ${entity.name}`}
                    >
                      <span
                        className="technology-icon"
                        style={{
                          color: technologyMeta[entity.technology].color,
                        }}
                      >
                        <TechnologyIcon
                          technology={entity.technology}
                          size={13}
                        />
                      </span>
                      {entity.name}
                    </button>
                  ))}
                </div>
              </section>
              {selected ? (
                <aside className="inspector">
                  <div className="panel-head">
                    <div>
                      <span className="eyebrow">02 / INSPECTOR</span>
                      <h2>{selected.name}</h2>
                    </div>
                    <span className={`type-mark ${selected.technology}`}>
                      {technologyMeta[selected.technology].label}
                    </span>
                  </div>
                  <div className="entity-summary">
                    <span className="big-value">
                      {selected.capacity_mw ?? "—"}
                    </span>
                    <span className="unit">
                      MW
                      <br />
                      <small>installed capacity</small>
                    </span>
                  </div>
                  <dl className="facts">
                    <div>
                      <dt>Bus</dt>
                      <dd>{selected.bus ?? "not linked"}</dd>
                    </div>
                    <div>
                      <dt>Stage</dt>
                      <dd>
                        {stage} / {maxStage}
                      </dd>
                    </div>
                    <div>
                      <dt>Coordinates</dt>
                      <dd
                        className={
                          selected.coordinate_status === "bus-reference"
                            ? "verified"
                            : "warning"
                        }
                      >
                        {selected.coordinate_status === "bus-reference"
                          ? "bus reference"
                          : "missing"}
                      </dd>
                    </div>
                    <div>
                      <dt>Input state</dt>
                      <dd
                        className={
                          inputState === "base" ? "verified" : "warning"
                        }
                      >
                        {inputState}
                      </dd>
                    </div>
                    <div>
                      <dt>Lifecycle</dt>
                      <dd>{selected.lifecycle_status}</dd>
                    </div>
                  </dl>
                  <div className="provenance">
                    <span className="eyebrow">SOURCE PROVENANCE</span>
                    <strong>
                      {selected.source_file} · line {selected.source_line}
                    </strong>
                    <p>
                      {selected.modifications.length} dated modifications
                      applied before {snapshot?.as_of ?? "this stage"}.
                    </p>
                  </div>
                </aside>
              ) : (
                <aside className="inspector empty-state">
                  Select an input asset from the roster.
                </aside>
              )}
            </div>
            <section className="timeline-panel">
              <div className="timeline-title">
                <span className="eyebrow">03 / TIME CONTEXT</span>
                <h2>Input horizon</h2>
                <p>Stage changes reload the intermediate database snapshot.</p>
              </div>
              <div className="timeline-control">
                <div className="timeline-meta">
                  <span>
                    STAGE <b>{stage}</b>
                  </span>
                  <span>{snapshot?.as_of ?? "—"}</span>
                  <label>
                    BLOCK{" "}
                    <select
                      aria-label="Study block"
                      value={block}
                      onChange={(event) => setBlock(Number(event.target.value))}
                    >
                      {Array.from({ length: maxBlock }, (_, index) => (
                        <option key={index + 1} value={index + 1}>
                          {index + 1}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
                <input
                  aria-label="Study stage"
                  type="range"
                  min="1"
                  max={maxStage}
                  value={Math.min(stage, maxStage)}
                  onChange={(event) => setStage(Number(event.target.value))}
                />
                <div className="ticks">
                  <span>01</span>
                  <span>{Math.round(maxStage / 4)}</span>
                  <span>{Math.round(maxStage / 2)}</span>
                  <span>{Math.round((maxStage * 3) / 4)}</span>
                  <span>{maxStage}</span>
                </div>
              </div>
            </section>
            {unlocated.length > 0 && (
              <section className="unlocated-strip">
                <span className="eyebrow">LOCATION DATA GAP</span>
                <strong>
                  {unlocated.length} assets are not active or have no linked
                  coordinates.
                </strong>
                <p>
                  They remain selectable through the source roster and are not
                  assigned fabricated locations.
                </p>
              </section>
            )}
          </>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
