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
import {
  Area,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ComposedChart,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip as ChartTooltip,
  XAxis,
  YAxis,
} from "recharts";
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
  family?: string;
  frequency?: string;
  system_code?: string | null;
  interpretation_status?: string;
};
type MaintenanceSettings = { project_id: number; revision_id?: number | null; availability_basis: "short_term" | "long_term"; review_status: string; override: Record<string, unknown> };
type MaintenanceReview = {
  project_id: number;
  revision_id: number;
  review_status: string;
  availability_basis: "short_term" | "long_term";
  tables: { source_file: string; family: string; frequency: string; system_code?: string | null; review_status: "pending" | "confirmed" | "overridden"; examples: { source_code: string; asset_name: string; source_line: number; measure_type: number; unit_type: number; values: number[]; warnings: string[]; header_evidence: Record<string, unknown>; interpretation_status: string }[] }[];
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
    availability_basis?: "short_term" | "long_term";
    warnings: string[];
    block_durations_hours?: Record<string, number[]>;
    systems: { code: string; name: string; country_code?: string }[];
    layout: string;
  };
  entities: Entity[];
  buses: {
    source_code: string;
    name: string;
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
  fuels?: { source_code: string; name: string; unit_name?: string | null; base_cost?: number | null; co2_factor?: number | null; source_file: string; source_line: number }[];
  fuel_prices?: { fuel_code: string; year: number; month: number; price: number; source_file: string; source_line: number }[];
  currencies?: { code: string; conversion_to_reference: number; is_reference: boolean; source_file: string; source_line: number }[];
  provenance: string;
};
type HistoryEvent = { kind: string; source_file: string; source_line: number; effective_date: string; value?: number; measure_type?: number; unit_type?: number; fields?: Record<string, unknown> };
type EntityHistory = { stage: number; as_of: string; year?: number; month?: number; label?: string; lifecycle_status: string; is_active: boolean; capacity_installed_mw?: number; capacity_maximum_mw?: number; capacity_available_mw?: number | null; availability_source?: string; availability_basis?: "short_term" | "long_term" | null; availability_warning?: string | null; has_maintenance_plan?: boolean; maintenance_value?: number | null; maintenance_type?: number | null; maintenance_unit?: number | null; events?: HistoryEvent[] };
type HistoryFrequency = "monthly" | "weekly";
type HistoryScale = "absolute" | "detail";
type SummaryStats = { mean: number; p10: number; p25: number; p75: number; p90: number; min: number; max: number; stddev: number; valid_count: number };
type ProfilePoint = { mean: number; p10: number; p25: number; p75: number; p90: number; min: number; max: number; stddev: number; valid_count: number; hour?: number; month?: number; warning?: string | null };
type ProfileStats = { asset_id?: number; status?: "pending" | "running" | "ready" | "failed" | "not-applicable"; progress?: number; processed_assets?: number; total_assets?: number; source_code?: string; unit?: string; grouping?: string; statistics?: SummaryStats; series?: ProfilePoint[]; warnings?: string[]; missing_count?: number; filters?: { month?: number | null; scenario?: number | null; stage?: number | null; block?: number | null }; provenance?: string; error?: string; message?: string };
type AnalyticsStatus = { status: "not-started" | "pending" | "running" | "ready" | "failed"; phase?: string; progress: number; processed_assets: number; total_assets: number; error?: string | null };
type DemandProfile = {
  bus_code: string;
  bus_name: string;
  authority: "DBF" | "DBUS" | null;
  selected_date: string | null;
  curve_date: string | null;
  available_dates: string[];
  available_blocks: number[];
  demand_codes: string[];
  records: { block: number; demand_mw: number | null; demand_code: string | null; effective_date: string | null; source_file: string; source_line: number; value_kind: "input" }[];
  summary: { total_mw: number; peak_mw: number; block_count: number };
  warnings: string[];
  provenance: string;
  hourly_series?: { period: number; source_hour: number; load_level: number; demand_mw: number; value_kind: "derived" }[];
  hourly_formula?: string | null;
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

function StatValue({ label, value, unit = "" }: { label: string; value: number | undefined; unit?: string }) {
  return <span className="stat-value"><b>{value === undefined ? "—" : value.toFixed(2)}</b><small>{label}{unit ? ` · ${unit}` : ""}</small></span>;
}

function formatHistoryEvent(event: HistoryEvent): string {
  if (event.kind === "modification") {
    const capacity = event.fields?.capacity;
    if (capacity !== undefined) return `Potencia instalada: ${String(capacity)} MW`;
    const factor = event.fields?.factor;
    if (factor !== undefined) return `Factor operativo: ${String(factor)}`;
    return "Modificación de parámetros";
  }
  if (event.kind === "maintenance") {
    const unit = event.unit_type === 1 ? "unidades" : event.unit_type === 2 ? "%" : event.unit_type === 3 ? "MW" : "unidades";
    const mode = event.measure_type === 2 ? "disponibilidad" : "reducción";
    return `Mantenimiento: ${mode} ${event.value ?? "—"} ${unit}`;
  }
  return "Cambio de entrada";
}

function CapacityHistoryChart({ history, fullHistory, frequency, scale }: { history: EntityHistory[]; fullHistory: EntityHistory[]; frequency: HistoryFrequency; scale: HistoryScale }) {
  if (!history.length) return <p className="muted-copy">No capacity history is available for this generator.</p>;
  const data = history.map((point) => ({
    ...point,
     label: new Intl.DateTimeFormat("es-AR", { month: "short", year: "2-digit", timeZone: "UTC" }).format(new Date(`${point.as_of}T00:00:00Z`)),
    available: Number(point.capacity_available_mw ?? 0),
  }));
  const fullValues = fullHistory.map((point) => Number(point.capacity_available_mw ?? 0));
  const minimum = Math.min(...fullValues);
  const maximum = Math.max(...fullValues);
  const padding = maximum === minimum ? Math.max(1, maximum * 0.1) : (maximum - minimum) * 0.1;
  const scaleMagnitude = 10 ** Math.floor(Math.log10(Math.max(1, maximum)));
  const scaleStep = scaleMagnitude / 2;
  const absoluteMaximum = Math.max(scaleStep, Math.ceil(maximum / scaleStep) * scaleStep);
  const domain = scale === "absolute"
    ? [0, absoluteMaximum]
    : [Math.max(0, minimum - padding), maximum + padding];
  return <div className="capacity-history-chart" role="img" aria-label="Capacity availability by stage">
    <ResponsiveContainer width="100%" height={190}>
      <BarChart data={data} margin={{ top: 8, right: 12, bottom: 8, left: 0 }}>
        <CartesianGrid stroke="var(--chart-grid)" strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="label" tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={{ stroke: "var(--line)" }} interval={Math.max(0, Math.ceil(data.length / 6) - 1)} />
        <YAxis domain={domain} allowDataOverflow={false} tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={false} width={50} tickFormatter={(value: number) => `${value.toFixed(1)}`} />
         <ChartTooltip contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", color: "var(--text)", fontFamily: "DM Mono", fontSize: 11 }} labelFormatter={(_, payload) => { const point = payload?.[0]?.payload as EntityHistory | undefined; return point ? `${point.label ?? point.as_of} · Month ${point.stage}` : "Capacity"; }} formatter={(value) => [`${typeof value === "number" ? value.toFixed(3) : "—"} MW`, "Available Power"]} />
        <Bar dataKey="available" name="available" maxBarSize={18}>
          {data.map((point) => <Cell key={point.stage} fill={point.events?.length ? "var(--chart-p90)" : "var(--accent)"} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
      <div className="profile-chart-caption"><span>Available Power · {frequency === "weekly" ? "calendar week" : "calendar month"}</span><span>{scale === "absolute" ? "Absolute scale · 0 MW baseline" : "Detail scale · cropped axis"} · {minimum.toFixed(3)}–{maximum.toFixed(3)} MW</span></div>
   </div>;
}

function ProfileChart({ profile, theme }: { profile: ProfileStats; theme: "dark" | "light" }) {
  const points = profile.series ?? [];
  const monthLabels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const bandColor = theme === "dark" ? "#49a7e0" : "#2587c8";
  if (!points.length) return null;
  const chartData = points.map((point) => ({
    ...point,
    label: point.month ? monthLabels[point.month - 1] : String(point.hour).padStart(2, "0"),
    bandBase: point.p25,
    bandWidth: Math.max(0, point.p75 - point.p25),
  }));
  return <div className="profile-chart" role="img" aria-label={`${profile.grouping ?? "profile"} statistics`}>
    <ResponsiveContainer width="100%" height={240}>
      <ComposedChart data={chartData} margin={{ top: 8, right: 14, bottom: 4, left: 0 }}>
        <CartesianGrid stroke="var(--chart-grid)" strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="label" tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={{ stroke: "var(--line)" }} interval={points.length > 12 ? 3 : 0} />
        <YAxis tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={false} width={42} tickFormatter={(value: number) => value.toFixed(1)} />
        <ChartTooltip contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", color: "var(--text)", fontFamily: "DM Mono", fontSize: 11 }} labelFormatter={(_, payload) => { const point = payload?.[0]?.payload as (typeof chartData)[number] | undefined; return point ? `${point.label} · n=${point.valid_count}${point.warning ? " · skew/outlier warning" : ""}` : "Profile"; }} formatter={(value, name) => [typeof value === "number" ? value.toFixed(2) : String(value ?? "—"), String(name)]} />
        <Legend wrapperStyle={{ color: "var(--muted)", fontFamily: "DM Mono", fontSize: 10 }} />
        <Area dataKey="bandBase" stackId="quartile-band" stroke="none" fill="#000000" fillOpacity={0} isAnimationActive={false} legendType="none" tooltipType="none" />
        <Area className="profile-band-area" dataKey="bandWidth" stackId="quartile-band" stroke="none" fill={bandColor} fillOpacity={0.32} isAnimationActive={false} legendType="none" name="P25-P75" />
        <Line type="monotone" dataKey="p10" name="P10" stroke="var(--chart-p10)" strokeDasharray="5 4" strokeWidth={1.5} dot={false} />
        <Line type="monotone" dataKey="mean" name="Mean" stroke="var(--accent)" strokeWidth={2.5} dot={false} activeDot={{ r: 4 }} />
        <Line type="monotone" dataKey="p90" name="P90" stroke="var(--chart-p90)" strokeDasharray="5 4" strokeWidth={1.5} dot={false} />
      </ComposedChart>
    </ResponsiveContainer>
      <div className="profile-chart-caption"><span>{profile.grouping === "month-of-year" ? "month" : profile.grouping}</span><span>P25-P75 interquartile band</span></div>
  </div>;
}

function ProfileStatsPanel({ profile, status, technology, theme }: { profile: ProfileStats | null; status: "idle" | "loading" | "ready" | "empty" | "error"; technology: string; theme: "dark" | "light" }) {
  return <section className="profile-panel" aria-live="polite">
    <div className="panel-section-head"><span className="eyebrow">INPUT PROFILE</span><strong>{technology === "hydro" ? "Typical hydrograph" : "Typical renewable profile"}</strong></div>
    {status === "loading" && <p className="muted-copy">Gráficas aún no disponibles. Se están generando en segundo plano{profile?.progress !== undefined ? ` · ${profile.progress}%` : ""}.</p>}
    {status === "empty" && <p className="muted-copy">{profile?.message ?? "No compatible input series is linked to this generator."}</p>}
    {status === "error" && <p className="error-copy">Statistics could not be loaded. The source may be unavailable or the request failed.</p>}
     {profile?.statistics && <div className="stats-grid"><StatValue label="mean" value={profile.statistics.mean} unit={profile.unit} /><StatValue label="P10" value={profile.statistics.p10} /><StatValue label="P90" value={profile.statistics.p90} /><StatValue label="min" value={profile.statistics.min} /><StatValue label="max" value={profile.statistics.max} /><StatValue label="buckets" value={profile.statistics.valid_count} /></div>}
     {profile?.series && <ProfileChart profile={profile} theme={theme} />}
     {profile?.warnings?.map((warning) => <small className="profile-warning" key={warning}>{warning}</small>)}
    {profile && <small className="provenance-line">{profile.provenance ?? "Statistics are precalculated for this revision."}{profile.missing_count ? ` · ${profile.missing_count} missing` : ""}</small>}
  </section>;
}

function DemandCurveChart({ profile }: { profile: DemandProfile }) {
  if (profile.hourly_series?.length) {
    return <div className="demand-chart" role="img" aria-label={`Hourly demand curve for bus ${profile.bus_code}`}><ResponsiveContainer width="100%" height={190}><LineChart data={profile.hourly_series} margin={{ top: 8, right: 8, bottom: 4, left: 0 }}><CartesianGrid stroke="var(--chart-grid)" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="period" tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={{ stroke: "var(--line)" }} /><YAxis tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={false} width={42} /><ChartTooltip contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", color: "var(--text)", fontFamily: "DM Mono", fontSize: 11 }} formatter={(value) => [typeof value === "number" ? `${value.toFixed(2)} MW` : String(value ?? "—"), "Demand"]} /><Line type="monotone" dataKey="demand_mw" name="Demand MW" stroke="var(--accent)" strokeWidth={2.5} dot={false} activeDot={{ r: 4 }} /></LineChart></ResponsiveContainer></div>;
  }
  return <div className="demand-chart" role="img" aria-label={`Block demand curve for bus ${profile.bus_code}`}><ResponsiveContainer width="100%" height={190}><BarChart data={profile.records} margin={{ top: 8, right: 8, bottom: 4, left: 0 }}><CartesianGrid stroke="var(--chart-grid)" strokeDasharray="3 3" vertical={false} /><XAxis dataKey="block" tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={{ stroke: "var(--line)" }} /><YAxis tick={{ fill: "var(--muted)", fontSize: 10, fontFamily: "DM Mono" }} tickLine={false} axisLine={false} width={42} /><ChartTooltip contentStyle={{ background: "var(--surface)", border: "1px solid var(--line)", color: "var(--text)", fontFamily: "DM Mono", fontSize: 11 }} formatter={(value) => [typeof value === "number" ? `${value.toFixed(2)} MW` : String(value ?? "—"), "Demand"]} /><Bar dataKey="demand_mw" name="Demand MW" fill="var(--accent)" radius={[2, 2, 0, 0]} /></BarChart></ResponsiveContainer></div>;
}

function DemandProfilePanel({ profile, status, date, block, demandCode, onDateChange, onBlockChange, onDemandCodeChange }: { profile: DemandProfile | null; status: "idle" | "loading" | "ready" | "empty" | "error"; date: string; block: string; demandCode: string; onDateChange: (value: string) => void; onBlockChange: (value: string) => void; onDemandCodeChange: (value: string) => void }) {
  return <section className="demand-profile-panel" aria-live="polite">
    <div className="panel-section-head"><span className="eyebrow">NODE DEMAND</span><strong>{profile?.hourly_series?.length ? "HOURLY / HRBMAP" : profile?.authority ?? "—"}</strong></div>
    <div className="demand-profile-controls">
      <label htmlFor="demand-date">AS OF <input id="demand-date" type="date" value={date} onChange={(event) => onDateChange(event.target.value)} /></label>
      <label htmlFor="demand-block">BLOCK <select id="demand-block" value={block} onChange={(event) => onBlockChange(event.target.value)}><option value="all">All</option>{(profile?.available_blocks ?? []).map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
      <label htmlFor="demand-code">LOAD <select id="demand-code" value={demandCode} onChange={(event) => onDemandCodeChange(event.target.value)}><option value="all">All</option>{(profile?.demand_codes ?? []).map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
      {profile?.curve_date && <span>Curve date <b>{profile.curve_date}</b></span>}
    </div>
    {status === "loading" && <p className="muted-copy">Loading block demand curve...</p>}
    {status === "empty" && <p className="muted-copy">No demand record is available for this node and date.</p>}
    {status === "error" && <p className="error-copy">Demand curve could not be loaded.</p>}
    {profile && profile.records.length > 0 && <>
      <div className="demand-summary"><span><b>{profile.summary.peak_mw.toFixed(2)}</b><small>peak MW</small></span><span><b>{profile.summary.total_mw.toFixed(2)}</b><small>sum of blocks</small></span><span><b>{profile.summary.block_count}</b><small>blocks</small></span></div>
      <DemandCurveChart profile={profile} />
      <small className="provenance-line">{profile.hourly_formula ? `${profile.hourly_formula}. ` : ""}{profile.provenance}{profile.warnings.length ? ` · ${profile.warnings.join(" ")}` : ""}</small>
    </>}
  </section>;
}
type NodeGroup = {
  key: string;
  busCode: string | null;
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
const apiBase = import.meta.env.VITE_API_BASE_URL ?? (import.meta.env.DEV ? "" : "http://127.0.0.1:8000");
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
    iconSize: [44, 44],
    iconAnchor: [22, 22],
  });
}

function demandMarkerIcon() {
  const icon = renderToStaticMarkup(<House size={16} strokeWidth={2} />);
  return divIcon({
    className: "demand-marker-wrapper",
    html: `<span class="demand-marker" aria-hidden="true">${icon}</span>`,
    iconSize: [44, 44],
    iconAnchor: [22, 22],
  });
}

function MaintenanceReviewPanel({ review, onConfirm }: { review: MaintenanceReview; onConfirm: (sourceFile: string, measureType: number, unitType: number, overridden: boolean) => Promise<void> }) {
  const [choices, setChoices] = useState<Record<string, { measureType: number; unitType: number }>>({});
  const [saving, setSaving] = useState<string | null>(null);
  const [error, setError] = useState("");
  const hasPendingTables = review.tables.some((table) => table.review_status === "pending");
  if (!review.tables.length || !hasPendingTables) return null;
  return <section className="maintenance-review" aria-labelledby="maintenance-review-title">
    <div className="maintenance-review-head">
      <div><span className="eyebrow">MAINTENANCE INTERPRETATION</span><h2 id="maintenance-review-title">Review PM table settings</h2><p>Defaults are active. Confirm or override the detected interpretation before relying on the schedule.</p></div>
      <span className="status-chip warning">REVIEW REQUIRED</span>
    </div>
    <div className="maintenance-review-tables">
      {review.tables.map((table) => {
        const first = table.examples[0];
        const choice = choices[table.source_file] ?? { measureType: first?.measure_type ?? 1, unitType: first?.unit_type ?? 2 };
        return <div className="maintenance-review-table" key={table.source_file}>
          <div className="maintenance-review-table-head"><strong>{table.source_file}</strong><span>{table.family} · {table.frequency} · system {table.system_code ?? "—"}</span></div>
          <div className="maintenance-review-controls">
            <label>TYPE INFO<select aria-label={`Tipo Info ${table.source_file}`} value={choice.measureType} onChange={(event) => setChoices((current) => ({ ...current, [table.source_file]: { ...choice, measureType: Number(event.target.value) } }))}><option value={1}>Reduction</option><option value={2}>Absolute</option></select></label>
            <label>UNITS<select aria-label={`Units ${table.source_file}`} value={choice.unitType} onChange={(event) => setChoices((current) => ({ ...current, [table.source_file]: { ...choice, unitType: Number(event.target.value) } }))}><option value={1}>Number of units</option><option value={2}>Percentage</option><option value={3}>MW</option><option value={4}>m3/s (unresolved)</option></select></label>
            <button className="upload-button" disabled={saving === table.source_file || table.review_status !== "pending"} onClick={async () => { setSaving(table.source_file); setError(""); try { await onConfirm(table.source_file, choice.measureType, choice.unitType, choice.measureType !== first?.measure_type || choice.unitType !== first?.unit_type); } catch (reason) { setError(reason instanceof Error ? reason.message : "Maintenance confirmation failed."); } finally { setSaving(null); } }}>{saving === table.source_file ? "Saving..." : table.review_status === "confirmed" ? "Confirmed" : table.review_status === "overridden" ? "Overridden" : "Confirm table"}</button>
            {table.review_status !== "pending" && <span className={`review-result ${table.review_status}`}>{table.review_status}</span>}
          </div>
          {table.examples.map((example) => <div className="maintenance-review-example" key={`${table.source_file}-${example.source_line}`}><code>{table.source_file}:{example.source_line}</code><strong>{example.source_code} {example.asset_name}</strong><span>sample: {example.values.join(", ")}</span><small>{example.warnings.length ? example.warnings.join(" · ") : `Detected ${example.measure_type === 1 ? "reduction" : "absolute"} / ${example.unit_type === 2 ? "percentage" : `unit ${example.unit_type}`}`}</small></div>)}
        </div>;
      })}
    </div>
    {error && <p className="error-copy" role="alert">{error}</p>}
  </section>;
}

function App() {
  const [projectId, setProjectId] = useState<number | undefined>(
    configuredProjectId,
  );
  const [projects, setProjects] = useState<Project[]>([]);
  const [revisions, setRevisions] = useState<Revision[]>([]);
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null);
  const [selectedId, setSelectedId] = useState("");
  const [selectedNodeBus, setSelectedNodeBus] = useState("");
  const [nodeQuery, setNodeQuery] = useState("");
  const [nodeSearchOpen, setNodeSearchOpen] = useState(false);
  const [activeNodeOption, setActiveNodeOption] = useState(0);
  const [entityHistory, setEntityHistory] = useState<EntityHistory[]>([]);
  const [historyError, setHistoryError] = useState("");
  const [historyFrequency, setHistoryFrequency] = useState<HistoryFrequency>("monthly");
  const [historyWindowSize, setHistoryWindowSize] = useState<60 | 120>(60);
  const [historyScale, setHistoryScale] = useState<HistoryScale>("absolute");
  const [historyWindowStart, setHistoryWindowStart] = useState(0);
  const [profileStats, setProfileStats] = useState<ProfileStats | null>(null);
  const [profileStatus, setProfileStatus] = useState<"idle" | "loading" | "ready" | "empty" | "error">("idle");
  const [demandProfile, setDemandProfile] = useState<DemandProfile | null>(null);
  const [demandProfileStatus, setDemandProfileStatus] = useState<"idle" | "loading" | "ready" | "empty" | "error">("idle");
  const [demandDate, setDemandDate] = useState("");
  const [demandBlockFilter, setDemandBlockFilter] = useState("all");
  const [demandCodeFilter, setDemandCodeFilter] = useState("all");
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
  const [importRun, setImportRun] = useState<ImportRun | null>(null);
  const [revisionRefreshKey, setRevisionRefreshKey] = useState(0);
  const [revisionRefreshPending, setRevisionRefreshPending] = useState(false);
  const [lastRefreshedImportId, setLastRefreshedImportId] = useState<number | null>(null);
  const [pipelineHydrating, setPipelineHydrating] = useState(false);
  const [analyticsStatus, setAnalyticsStatus] = useState<AnalyticsStatus | null>(null);
  const [analyticsError, setAnalyticsError] = useState("");
  const [maintenanceSettings, setMaintenanceSettings] = useState<MaintenanceSettings | null>(null);
  const [maintenanceReview, setMaintenanceReview] = useState<MaintenanceReview | null>(null);
  const [newProjectName, setNewProjectName] = useState("");
  const [creatingProject, setCreatingProject] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);
  const importActive = Boolean(importRun && !["completed", "failed"].includes(importRun.status));
  const pipelineBusy = importActive || revisionRefreshPending || pipelineHydrating;

  useEffect(() => {
    localStorage.setItem("gme-theme", theme);
  }, [theme]);
  useEffect(() => {
    api<Project[]>("/api/projects")
      .then((items) => {
        setProjects(items);
        setProjectId((current) => current ?? items[0]?.id);
      })
      .catch((reason: Error) => {
        setStatus("error");
        setError(reason.message);
      });
  }, []);
  useEffect(() => {
    if (!projectId) return;
    api<Revision[]>(`/api/projects/${projectId}/revisions`)
      .then(setRevisions)
      .catch(() => setRevisions([]));
  }, [projectId]);
  useEffect(() => {
    if (!projectId) {
      setMaintenanceSettings(null);
      setMaintenanceReview(null);
      return;
    }
    api<MaintenanceSettings>(`/api/projects/${projectId}/maintenance-settings`)
      .then(setMaintenanceSettings)
      .catch(() => setMaintenanceSettings(null));
    api<MaintenanceReview>(`/api/projects/${projectId}/maintenance-review`)
      .then(setMaintenanceReview)
      .catch(() => setMaintenanceReview(null));
  }, [projectId, revisionRefreshKey]);
  useEffect(() => {
    if (!projectId) {
      setImportRun(null);
      setPipelineHydrating(false);
      return;
    }
    setImportRun(null);
    setPipelineHydrating(true);
    api<ImportRun[]>(`/api/projects/${projectId}/imports`)
      .then((runs) => {
        const active = runs.find((run) => !["completed", "failed"].includes(run.status));
        if (active) setImportRun(active);
      })
      .catch(() => undefined)
      .finally(() => setPipelineHydrating(false));
  }, [projectId]);
  useEffect(() => {
    if (!projectId || importActive || pipelineHydrating) {
      setAnalyticsStatus(null);
      setAnalyticsError("");
      return;
    }
    const controller = new AbortController();
    let timer: number | undefined;
    setAnalyticsStatus(null);
    setAnalyticsError("");
    const load = () => api<AnalyticsStatus>(`/api/projects/${projectId}/analytics/status`, { signal: controller.signal })
      .then((result) => {
        if (controller.signal.aborted) return;
        setAnalyticsStatus(result);
        setAnalyticsError("");
        if (result.status === "pending" || result.status === "running") timer = window.setTimeout(load, 1500);
      })
      .catch((reason: Error) => {
        if (controller.signal.aborted) return;
        setAnalyticsError(reason.message || "Analytics status unavailable.");
      });
    load();
    return () => {
      controller.abort();
      if (timer) window.clearTimeout(timer);
    };
  }, [projectId, importActive, pipelineHydrating]);
  useEffect(() => {
    if (!projectId) return;
    const controller = new AbortController();
    setStatus("loading");
    api<Snapshot>(`/api/projects/${projectId}/snapshot?stage=${stage}&block=${block}`, { signal: controller.signal })
      .then((nextSnapshot) => {
        setSnapshot(nextSnapshot);
        setRevisionRefreshPending(false);
        setDemandDate(nextSnapshot.as_of);
        setStatus("connected");
        setError("");
        setSelectedSystem((current) =>
          current === "all" ||
          nextSnapshot.study.systems.some((system) => system.code === current)
            ? current
            : "all",
        );
        setSelectedId((current) => nextSnapshot.entities.some((item) => item.id === current) ? current : "");
        setSelectedNodeBus((current) => {
          if (current && nextSnapshot.buses.some((bus) => bus.source_code === current)) return current;
          const byCapacity = nextSnapshot.entities.filter((item) => item.is_active && item.bus).reduce<{ bus_code: string; capacity: number } | null>((best, item) => {
            const capacity = item.capacity_available_mw ?? item.capacity_mw ?? 0;
            if (!best || capacity > best.capacity) return { bus_code: String(item.bus), capacity };
            return best;
          }, null);
          return byCapacity?.bus_code ?? nextSnapshot.buses[0]?.source_code ?? "";
        });
      })
      .catch((reason: Error) => {
        if (controller.signal.aborted) return;
        setStatus("error");
        setError(reason.message);
      });
    return () => controller.abort();
  }, [projectId, stage, block, revisionRefreshKey]);
  const updateMaintenanceBasis = (basis: "short_term" | "long_term") => {
    if (!projectId) return;
    api<MaintenanceSettings>(`/api/projects/${projectId}/maintenance-settings`, { method: "PUT", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ availability_basis: basis }) })
      .then((result) => {
        setMaintenanceSettings(result);
        setRevisionRefreshKey((current) => current + 1);
      })
      .catch((reason: Error) => setError(reason.message));
  };
  const confirmMaintenanceTable = async (sourceFile: string, measureType: number, unitType: number, overridden: boolean) => {
    if (!projectId || !maintenanceReview) return;
    const result = await api<MaintenanceSettings>(`/api/projects/${projectId}/revisions/${maintenanceReview.revision_id}/maintenance-settings/confirm`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ availability_basis: maintenanceSettings?.availability_basis ?? "short_term", review_status: overridden ? "overridden" : "confirmed", override: { source_file: sourceFile, measure_type: measureType, unit_type: unitType } }) });
    setMaintenanceSettings(result);
    const nextReview = await api<MaintenanceReview>(`/api/projects/${projectId}/maintenance-review`);
    setMaintenanceReview(nextReview);
    setRevisionRefreshKey((current) => current + 1);
  };
  const selectedEntity = snapshot?.entities.find((item) => item.id === selectedId);
  const selectedEntityId = selectedEntity?.id;
  const selectedEntityAssetType = selectedEntity?.asset_type;
  const selectedEntityTechnology = selectedEntity?.technology;
  useEffect(() => {
    if (pipelineBusy || !projectId || !selectedId) {
      setEntityHistory([]);
      setHistoryError("");
      setHistoryFrequency("monthly");
      setHistoryWindowStart(0);
      return;
    }
    setHistoryWindowStart(0);
    setHistoryError("");
    const historyPath = `/api/projects/${projectId}/assets/${selectedId}/history?block=${block}`;
    api<{ series: EntityHistory[]; frequency?: HistoryFrequency }>(historyPath)
      .then((result) => {
        setEntityHistory(result.series);
        setHistoryError("");
        setHistoryFrequency(result.frequency ?? "monthly");
      })
      .catch((reason: Error) => {
        setEntityHistory([]);
        setHistoryError(reason.message || "Capacity history request failed.");
        setHistoryFrequency("monthly");
      });
  }, [pipelineBusy, projectId, selectedId, block]);
  const historyWindowEnd = Math.min(historyWindowStart + historyWindowSize, entityHistory.length);
  const visibleHistory = entityHistory.slice(historyWindowStart, historyWindowEnd);
  const historyEvents = visibleHistory.flatMap((point) => (point.events ?? []).map((event) => ({ ...event, stage: point.stage, as_of: point.as_of })));
  const historyPeriodLabel = historyFrequency === "weekly" ? "Weeks" : "Months";
  useEffect(() => {
    if (pipelineBusy || !projectId || !selectedEntityId || !selectedEntityAssetType) {
      setProfileStats(null);
      setProfileStatus("idle");
      return;
    }
    setProfileStats(null);
    setProfileStatus("loading");
    const controller = new AbortController();
    const isRenewable = selectedEntityAssetType === "renewable" || ["wind", "solar", "biomass"].includes(normalizeTechnology(selectedEntityAssetType, selectedEntityTechnology ?? ""));
    const isHydro = selectedEntityAssetType === "hydro";
    const endpoint = (isHydro || isRenewable)
      ? `/api/projects/${projectId}/assets/${selectedEntityId}/profile-statistics`
      : null;
    if (!endpoint) {
      setProfileStatus("empty");
      return () => controller.abort();
    }
    let retryTimer: number | undefined;
    const load = () => api<ProfileStats>(endpoint, { signal: controller.signal })
      .then((result) => {
        if (controller.signal.aborted) return;
        setProfileStats(result);
        if (result.status === "pending" || result.status === "running") {
          setProfileStatus("loading");
          retryTimer = window.setTimeout(load, 1500);
        } else if (result.status === "failed") setProfileStatus("error");
        else if (result.status === "not-applicable") setProfileStatus("empty");
        else setProfileStatus("ready");
      })
      .catch((reason: Error) => {
        if (controller.signal.aborted) return;
        setProfileStatus(reason.message.startsWith("404") ? "empty" : "error");
      });
    load();
    return () => {
      controller.abort();
      if (retryTimer) window.clearTimeout(retryTimer);
    };
  }, [pipelineBusy, projectId, selectedEntityId, selectedEntityAssetType, selectedEntityTechnology]);
  useEffect(() => {
    if (pipelineBusy || !projectId || !selectedNodeBus || !demandDate) {
      setDemandProfile(null);
      setDemandProfileStatus("idle");
      return;
    }
    const controller = new AbortController();
    setDemandProfileStatus("loading");
    const params = new URLSearchParams({ date: demandDate });
    if (demandBlockFilter !== "all") params.set("block", demandBlockFilter);
    if (demandCodeFilter !== "all") params.set("demand_code", demandCodeFilter);
    api<DemandProfile>(`/api/projects/${projectId}/buses/${encodeURIComponent(selectedNodeBus)}/demand?${params}`, { signal: controller.signal })
      .then((result) => {
        if (controller.signal.aborted) return;
        setDemandProfile(result);
        setDemandProfileStatus(result.records.length ? "ready" : "empty");
      })
      .catch((reason: Error) => {
        if (controller.signal.aborted) return;
        setDemandProfileStatus(reason.message.startsWith("404") ? "empty" : "error");
      });
    return () => controller.abort();
  }, [pipelineBusy, projectId, selectedNodeBus, demandDate, demandBlockFilter, demandCodeFilter]);
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
  useEffect(() => {
    if (importRun?.status !== "completed" || importRun.id === lastRefreshedImportId) return;
    setLastRefreshedImportId(importRun.id);
    setRevisionRefreshPending(true);
    setRevisionRefreshKey((value) => value + 1);
    setSelectedId("");
    setSelectedNodeBus("");
    setEntityHistory([]);
    setProfileStats(null);
    setDemandProfile(null);
  }, [importRun?.id, importRun?.status, lastRefreshedImportId]);

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
              busCode: item.entity.bus !== undefined ? String(item.entity.bus) : null,
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
  const selected = systemEntities.find((entity) => entity.id === selectedId);
  const availabilityBasisDisabled = !selected || selected.has_maintenance_plan || !["thermal", "hydro"].includes(selected.asset_type);
  const availabilityBasisNote = selected?.has_maintenance_plan
    ? "PM schedule controls this machine"
    : selected && !["thermal", "hydro"].includes(selected.asset_type)
      ? "Outage index is not applicable to this asset type"
      : "Used for machines without a PM plan";
  const nodeAssets = selectedNodeBus ? systemEntities.filter((entity) => String(entity.bus) === selectedNodeBus && entity.is_active) : [];
  const selectedNode = systemBuses.find((bus) => bus.source_code === selectedNodeBus);
  const searchableNodes = systemBuses.filter((bus) => {
    const query = nodeQuery.trim().toLowerCase();
    if (!query) return true;
    return `${bus.source_code} ${bus.name} ${systemEntities.filter((entity) => String(entity.bus) === bus.source_code).map((entity) => `${entity.name} ${entity.source_code}`).join(" ")}`.toLowerCase().includes(query);
  });
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
  const topologySection = !geographicLayout && snapshot ? (
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
        selectedBus={selectedNodeBus}
        showDemandReferences={showDemandReferences}
        onSelectBus={selectNode}
      />
    </section>
  ) : null;

  function selectNode(busCode: string, generatorId?: string) {
    const nodeEntities = systemEntities.filter(
      (entity) => String(entity.bus) === busCode && entity.is_active,
    );
    setSelectedNodeBus(busCode);
    setSelectedId(
      generatorId ?? (nodeEntities.length === 1 ? nodeEntities[0].id : ""),
    );
    setDemandBlockFilter("all");
    setDemandCodeFilter("all");
    setNodeQuery("");
    setNodeSearchOpen(false);
    setActiveNodeOption(0);
  }

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
  const analyticsActive = analyticsStatus?.status === "pending" || analyticsStatus?.status === "running";
  const processingActive = pipelineHydrating || importActive || revisionRefreshPending || analyticsActive || analyticsStatus?.status === "failed";
  const processingProgress = importActive ? importDetails.progress ?? 0 : analyticsStatus?.progress ?? 0;
  const processingPhase = pipelineHydrating ? "checking active revision" : importActive ? importDetails.phase ?? "importing source" : revisionRefreshPending ? "activating new revision" : analyticsStatus?.phase ?? "profile statistics";

  return (
    <main className={`workspace theme-${theme}`}>
      <aside className="rail" aria-label="Application navigation">
        <div className="rail-logo">
          GME<span>·</span>PX
        </div>
        <nav aria-label="Workspace navigation">
          <button
            className={view === "map" ? "nav-active" : ""}
            onClick={() => setView("map")}
            aria-label="01 Map workspace"
            aria-current={view === "map" ? "page" : undefined}
          >
            01 <span>System map</span>
          </button>
          <button
            className={view === "files" ? "nav-active" : ""}
            onClick={() => setView("files")}
            aria-label="02 Files"
            aria-current={view === "files" ? "page" : undefined}
          >
            02 <span>Files</span>
          </button>
          <button aria-label="03 Mappings, unavailable" disabled>
            03 <span>Mappings</span>
          </button>
          <button aria-label="04 Exports, unavailable" disabled>
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
        {processingActive && (
          <section className={`processing-banner processing-${analyticsStatus?.status === "failed" ? "failed" : importActive ? "importing" : "running"}`} aria-live="polite" aria-label="Historical data processing status">
            <div className="processing-banner-head">
              <div>
                <span className="eyebrow">DATA PIPELINE</span>
                <strong>{importActive ? "Importing source and building model" : analyticsStatus?.status === "failed" ? "Historical profile processing failed" : "Calculating historical profiles"}</strong>
              </div>
              <span className="processing-percent">{processingProgress}%</span>
            </div>
            <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={processingProgress} aria-label="Historical data processing progress">
              <span style={{ width: `${Math.min(100, Math.max(0, processingProgress))}%` }} />
            </div>
            <div className="processing-banner-meta">
              <span>{processingPhase}</span>
              {importActive ? <span>{importRun?.files_processed ?? 0} / {importRun?.files_total || "—"} files</span> : <span>{analyticsStatus?.processed_assets ?? 0} / {analyticsStatus?.total_assets ?? 0} assets</span>}
              {analyticsStatus?.status === "failed" && <span className="processing-error">{analyticsStatus.error ?? "Check analytics status for details."}</span>}
              {analyticsError && <span className="processing-error">{analyticsError}</span>}
            </div>
          </section>
        )}
        {snapshot && (snapshot.study.warnings.length > 0 || systemDemands.length > 0) && (
          <details className="diagnostics-summary">
            <summary><span><b>DIAGNOSTICS</b> · {snapshot.study.warnings.length} known limitations{systemDemands.length ? ` · ${systemDemands.length} demand records` : ""}</span><small>Open details</small></summary>
            <div className="diagnostics-detail">
              {systemDemands.length > 0 && <div className="diagnostic-item demand-diagnostic"><House size={16} aria-hidden="true" /><span><b>DEMAND</b>{demandTotalGwh.toFixed(1)} GWh · {systemDemands.length} source records for stage {stage}, block {block}</span><label className="demand-toggle"><input type="checkbox" checked={showDemandReferences} onChange={(event) => setShowDemandReferences(event.target.checked)} /> Show references</label></div>}
              {snapshot.study.warnings.map((warning) => <div className="diagnostic-item warning-diagnostic" key={warning}><span><b>KNOWN LIMITATION</b>{warning}</span></div>)}
            </div>
          </details>
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
            <div className={`visual-grid${pipelineBusy ? " pipeline-busy" : ""}`} aria-busy={pipelineBusy}>
              {pipelineBusy && (
                <div className="pipeline-overlay" role="status" aria-live="polite">
                  <div className="pipeline-overlay-card">
                    <span className="eyebrow">ACTIVE REVISION UPDATE</span>
                    <strong>{pipelineHydrating ? "Checking active revision" : revisionRefreshPending ? "Refreshing model and temporal series" : "Processing source data in background"}</strong>
                    <span>{pipelineHydrating ? "Waiting for the import status before requesting temporal data." : revisionRefreshPending ? "The map will refresh when the new revision is ready." : `${processingPhase} · ${processingProgress}%`}</span>
                    <div className="progress-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={processingProgress} aria-label="Active revision update progress"><span style={{ width: `${Math.min(100, Math.max(0, processingProgress))}%` }} /></div>
                    <small>Historical capacity, maintenance and input profiles will be reloaded automatically.</small>
                  </div>
                </div>
              )}
                <section className={`map-panel ${geographicLayout ? "geographic-layout" : "topology-first"}`}>
                <div className="panel-head">
                  <div>
                    <span className="eyebrow">{geographicLayout ? "01 / GEOGRAPHIC CONTEXT" : "01 / NETWORK TOPOLOGY"}</span>
                    <h2>{projectName} input network</h2>
                  </div>
                  <div className="node-search">
                    <label htmlFor="node-search-input"><span className="eyebrow">FIND NODE</span><input id="node-search-input" role="combobox" aria-autocomplete="list" aria-controls="node-search-results" aria-expanded={nodeSearchOpen} aria-activedescendant={nodeSearchOpen && searchableNodes.length ? `node-option-${searchableNodes[Math.min(activeNodeOption, searchableNodes.length - 1)].source_code}` : undefined} value={nodeQuery} onFocus={() => { setNodeSearchOpen(true); setActiveNodeOption(0); }} onBlur={() => window.setTimeout(() => setNodeSearchOpen(false), 120)} onChange={(event) => { setNodeQuery(event.target.value); setNodeSearchOpen(true); setActiveNodeOption(0); }} onKeyDown={(event) => {
                      if (event.key === "ArrowDown") { event.preventDefault(); setNodeSearchOpen(true); setActiveNodeOption((current) => Math.min(searchableNodes.length - 1, current + 1)); }
                      if (event.key === "ArrowUp") { event.preventDefault(); setActiveNodeOption((current) => Math.max(0, current - 1)); }
                      if (event.key === "Enter" && nodeSearchOpen && searchableNodes.length) { event.preventDefault(); selectNode(searchableNodes[Math.min(activeNodeOption, searchableNodes.length - 1)].source_code); }
                      if (event.key === "Escape") { event.preventDefault(); setNodeSearchOpen(false); }
                    }} placeholder="Bus code, name or generator" /></label>
                    {nodeSearchOpen && <div id="node-search-results" className="node-search-results" role="listbox" aria-label="Network nodes">
                      {searchableNodes.length ? searchableNodes.map((bus) => {
                        const count = systemEntities.filter((entity) => String(entity.bus) === bus.source_code && entity.is_active).length;
                        const optionIndex = searchableNodes.indexOf(bus);
                        return <button id={`node-option-${bus.source_code}`} key={bus.source_code} className={`${selectedNodeBus === bus.source_code ? "selected " : ""}${activeNodeOption === optionIndex ? "active" : ""}`.trim()} onMouseEnter={() => setActiveNodeOption(optionIndex)} onMouseDown={(event) => event.preventDefault()} onClick={() => selectNode(bus.source_code)} role="option" aria-selected={selectedNodeBus === bus.source_code}><strong>BUS {bus.source_code}</strong><span>{bus.name} · {count} generators</span></button>;
                      }) : <p className="node-search-empty">No matching node.</p>}
                    </div>}
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
                {topologySection}
                <div
                  className="map-canvas"
                  role="region"
                  aria-label={geographicLayout ? "Geographic map of input assets" : `${countryContext?.name ?? "Study"} reference geography`}
                >
                  {snapshot && geographicLayout ? (
                    <MapContainer
                      center={[-32.9, -56]}
                      zoom={6}
                      scrollWheelZoom={false}
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
                            alt={`Select node ${group.busCode ?? group.key}: ${group.items.length} generator${group.items.length === 1 ? "" : "s"}`}
                            title={`Node ${group.busCode ?? group.key}: ${preview.name}`}
                            eventHandlers={{
                              click: () => {
                                setSelectedNodeBus(group.busCode ?? "");
                                setSelectedId(group.items.length === 1 ? preview.id : "");
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
                                  alt={`Select demand node ${bus.source_code}`}
                                  title={`Demand at node ${bus.source_code}`}
                                  eventHandlers={{ click: () => selectNode(bus.source_code) }}
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
                      scrollWheelZoom={false}
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
                        : "Country context is secondary reference geography; assets use the derived topology."}
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
                <div className="node-selection-note">Select a node on the map or use Find Node. Generator details appear in the inspector.</div>
              </section>
              <section className="timeline-panel">
                <div className="timeline-title">
                  <span className="eyebrow">03 / TIME CONTEXT</span>
                  <h2>Input horizon</h2>
                  <p>Stage changes reload the intermediate database snapshot.</p>
                </div>
                <div className="timeline-scroll" tabIndex={0} aria-label="Scrollable study timeline">
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
                      <span className="timeline-family">FAMILY <b>INPUT MODEL</b></span>
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
                </div>
              </section>
              <aside className="inspector">
                <div className="node-context-card">
                  <span className="eyebrow">NODE INSPECTOR</span>
                  <h2>BUS {selectedNodeBus || "—"}</h2>
                  <p>{selectedNode?.name ?? "Select a node on the map"} · {nodeAssets.length} active generators</p>
                  <span>{selectedNode?.demand_mw ? `Demand ${selectedNode.demand_mw.toFixed(1)} MW` : "No demand value"}</span>
                </div>
                <div className="generator-selector">
                  <div className="panel-section-head"><span className="eyebrow">GENERATORS AT THIS NODE</span><strong>{nodeAssets.length}</strong></div>
                  {nodeAssets.length === 0 ? <p className="muted-copy">Select a node with active generators to inspect its assets.</p> : <div className="generator-selector-grid">{nodeAssets.map((entity) => <button key={entity.id} className={entity.id === selected?.id ? "selected" : ""} onClick={() => setSelectedId(entity.id)} aria-pressed={entity.id === selected?.id}><TechnologyIcon technology={entity.technology} size={16} /><span><strong>{entity.name}</strong><small>{technologyMeta[entity.technology].label} · {entity.capacity_available_mw ?? entity.capacity_mw ?? "—"} MW</small></span></button>)}</div>}
                </div>
                {selectedNodeBus && <DemandProfilePanel profile={demandProfile} status={demandProfileStatus} date={demandDate} block={demandBlockFilter} demandCode={demandCodeFilter} onDateChange={setDemandDate} onBlockChange={setDemandBlockFilter} onDemandCodeChange={setDemandCodeFilter} />}
                <div className="inspector-empty-copy"><strong>{selected ? `${selected.name} selected` : "Choose a generator from the node selector."}</strong><span>{selected ? "Its technical inputs and profile are shown below the network." : "Technical details, capacity history and cached P10/mean/P90 profiles will appear below."}</span></div>
              </aside>
             </div>
              {selected && <section className="generator-details-panel">
                <div className="generator-details-head panel-head">
                  <div>
                    <span className="eyebrow">02 / GENERATOR DETAIL</span>
                    <h2>{selected.name}</h2>
                  </div>
                  <span className={`type-mark ${selected.technology}`}>{technologyMeta[selected.technology].label}</span>
                </div>
                <div className="generator-details-body">
                  <div className="generator-overview">
                     <div className="entity-summary"><span className="big-value">{selected.capacity_available_mw ?? "—"}</span><span className="unit">MW<br /><small>available power</small></span></div>
                      <div className="availability-strip"><span><b>{selected.capacity_installed_mw ?? selected.capacity_mw ?? "—"}</b><small>installed power</small></span></div>
                     {selected.availability_warning && <p className="warning-copy">{selected.availability_warning}</p>}
                    <dl className="facts">
                      <div><dt>Bus</dt><dd>{selected.bus ?? "not linked"}</dd></div>
                      <div><dt>Stage</dt><dd>{stage} / {maxStage}</dd></div>
                      <div><dt>Coordinates</dt><dd className={selected.coordinate_status === "bus-reference" ? "verified" : "warning"}>{selected.coordinate_status === "bus-reference" ? "bus reference" : "missing"}</dd></div>
                      <div><dt>Input state</dt><dd className={inputState === "base" ? "verified" : "warning"}>{inputState}</dd></div>
                      <div><dt>Lifecycle</dt><dd>{selected.lifecycle_status}</dd></div>
                    </dl>
                  </div>
                  <div className="generator-inputs">
                    {selected.technical_details ? <div className="technical-details"><span className="eyebrow">TECHNICAL INPUTS</span>{Object.entries(selected.technical_details).filter(([key]) => !["kind", "source_file", "source_line", "production_curve", "level_volume_curve", "consumption_segments", "alternative_fuels"].includes(key)).slice(0, 8).map(([key, value]) => <div className="technical-row" key={key}><span>{key.replaceAll("_", " ")}</span><strong>{String(value ?? "—")}</strong></div>)}</div> : null}
                      <div className="history-strip">
                        <div className="history-strip-head"><span className="eyebrow">CAPACITY AVAILABILITY · {entityHistory.length} {historyPeriodLabel.toLowerCase()}</span><div className="history-window-controls" aria-label="Capacity history range"><button type="button" onClick={() => setHistoryWindowStart(Math.max(0, historyWindowStart - historyWindowSize))} disabled={historyWindowStart === 0} aria-label={`Previous capacity history ${historyPeriodLabel.toLowerCase()}`}>←</button><span>{historyPeriodLabel} {entityHistory.length ? historyWindowStart + 1 : 0}-{historyWindowEnd} / {entityHistory.length}</span><button type="button" onClick={() => setHistoryWindowStart(Math.min(Math.max(0, entityHistory.length - historyWindowSize), historyWindowStart + historyWindowSize))} disabled={historyWindowEnd >= entityHistory.length} aria-label={`Next capacity history ${historyPeriodLabel.toLowerCase()}`}>→</button><select value={historyWindowSize} onChange={(event) => { const nextSize = Number(event.target.value) as 60 | 120; setHistoryWindowSize(nextSize); setHistoryWindowStart(0); }} aria-label={`${historyPeriodLabel} shown in capacity history`}><option value="60">60 {historyPeriodLabel.toLowerCase()}</option><option value="120">120 {historyPeriodLabel.toLowerCase()}</option></select></div></div>
                     {historyError ? <p className="error-copy">Capacity history could not be loaded: {historyError}</p> : <CapacityHistoryChart history={visibleHistory} fullHistory={entityHistory} frequency={historyFrequency} scale={historyScale} />}
                         <div className="history-scale-control"><label htmlFor="availability-basis">Outage basis</label><select id="availability-basis" aria-label="Availability basis" disabled={availabilityBasisDisabled} value={maintenanceSettings?.availability_basis ?? "short_term"} onChange={(event) => updateMaintenanceBasis(event.target.value as "short_term" | "long_term")}><option value="short_term">Short-term index</option><option value="long_term">Historical index</option></select><small>{availabilityBasisNote}</small><label htmlFor="history-scale">Y scale</label><select id="history-scale" value={historyScale} onChange={(event) => setHistoryScale(event.target.value as HistoryScale)}><option value="absolute">Absolute · 0 MW baseline</option><option value="detail">Detail · cropped axis</option></select></div>
                        <div className="history-events" aria-label="Capacity and maintenance events">
                          {historyEvents.length === 0 ? <small className="history-event muted-copy">No hay cambios de potencia o mantenimiento en este rango.</small> : historyEvents.slice(0, 7).map((event) => <div className="history-event" key={`${event.kind}-${event.stage}-${event.source_file}-${event.source_line}`}><strong>{historyPeriodLabel.slice(0, -1).toUpperCase()} {event.stage} · {event.as_of}</strong><span>{formatHistoryEvent(event)}</span><small>{event.source_file}:{event.source_line}</small></div>)}
                        </div>
                      </div>
                    {selected.technical_details?.kind === "thermal" && (() => { const fuelCode = String(selected.technical_details.fuel_code ?? ""); const fuel = snapshot?.fuels?.find((item) => item.source_code === fuelCode); const price = snapshot?.fuel_prices?.find((item) => item.fuel_code === fuelCode); return <div className="fuel-panel"><span className="eyebrow">FUEL / COST</span><div className="fuel-grid"><span><b>{fuel?.name ?? (fuelCode || "—")}</b><small>fuel</small></span><span><b>{price?.price ?? fuel?.base_cost ?? "—"}</b><small>{fuel?.unit_name ?? "source price"}</small></span><span><b>{String(selected.technical_details.variable_om_cost ?? "—")}</b><small>O&M $/MWh</small></span></div><small className="provenance-line">Source: {fuel?.source_file ?? selected.source_file} · values remain source inputs</small></div>; })()}
                  </div>
                  <div className="generator-analytics">
                    {(selected.asset_type === "hydro" || ["wind", "solar", "biomass"].includes(selected.technology)) && <ProfileStatsPanel profile={profileStats} status={profileStatus} technology={selected.technology} theme={theme} />}
                    <div className="provenance"><span className="eyebrow">SOURCE PROVENANCE</span><strong>{selected.source_file} · line {selected.source_line}</strong><p>{selected.modifications.length} dated modifications applied before {snapshot?.as_of ?? "this stage"}.</p></div>
                  </div>
                </div>
              </section>}
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
        {maintenanceReview && <MaintenanceReviewPanel review={maintenanceReview} onConfirm={confirmMaintenanceTable} />}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
