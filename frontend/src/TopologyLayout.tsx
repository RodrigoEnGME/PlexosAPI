import { useMemo, useState } from "react";
import {
  Battery,
  Droplets,
  Flame,
  House,
  Leaf,
  Sun,
  Wind,
  Zap,
} from "lucide-react";
import type { Entity } from "./visualizerTypes";

type Circuit = {
  source_code: string;
  from_bus: string;
  to_bus: string;
  is_interconnection?: boolean;
};
type Bus = {
  source_code: string;
  name?: string;
  system_code?: string | null;
  demand_mw?: number;
  primary_source?: { name: string; capacity_mw: number | null };
};
const icons = {
  hydro: Droplets,
  thermal: Flame,
  wind: Wind,
  solar: Sun,
  biomass: Leaf,
  unknown: Zap,
  battery: Battery,
};

export function TopologyLayout({
  buses,
  circuits,
  entities,
  onSelectBus,
  selectedBus,
  showDemandReferences,
}: {
  buses: Bus[];
  circuits: Circuit[];
  entities: Entity[];
  onSelectBus: (busCode: string) => void;
  selectedBus: string;
  showDemandReferences: boolean;
}) {
  const [zoom, setZoom] = useState(1);
  const maxRows = 6;
  const nodes = useMemo(
    () =>
      buses.map((bus, index) => {
        const column = Math.floor(index / maxRows);
        const row = index % maxRows;
        const assets = entities.filter(
          (entity) =>
            entity.bus?.toString() === bus.source_code && entity.is_active,
        );
        return { bus, x: 44 + column * 104, y: 42 + row * 76, assets };
      }),
    [buses, entities],
  );
  const nodeByCode = new Map(nodes.map((node) => [node.bus.source_code, node]));
  const width = Math.max(
    760,
    88 + Math.max(1, Math.ceil(nodes.length / maxRows)) * 104,
  );
  const height = Math.max(180, 84 + Math.min(maxRows, nodes.length) * 76);
  return (
    <div
      className="topology-layout"
      role="region"
      aria-label="Derived electrical topology layout, not geographic"
    >
      <div className="topology-toolbar">
        <span className="topology-label">
          DERIVED TOPOLOGY · NOT GEOGRAPHIC
        </span>
        <div>
          <button
            aria-label="Zoom out topology"
            onClick={() => setZoom((value) => Math.max(0.5, value - 0.25))}
          >
            -
          </button>
          <button aria-label="Reset topology zoom" onClick={() => setZoom(1)}>
            {Math.round(zoom * 100)}%
          </button>
          <button
            aria-label="Zoom in topology"
            onClick={() => setZoom((value) => Math.min(3, value + 0.25))}
          >
            +
          </button>
        </div>
      </div>
      <div className="topology-viewport">
        <svg
          style={{
            width: `${zoom * width}px`,
            height: `${zoom * height}px`,
          }}
          viewBox={`0 0 ${width} ${height}`}
          preserveAspectRatio="xMinYMin meet"
        >
          <g className="topology-circuits">
            {circuits.map((circuit) => {
              const from = nodeByCode.get(circuit.from_bus);
              const to = nodeByCode.get(circuit.to_bus);
              return from && to ? (
                <line
                  className={
                    circuit.is_interconnection ? "interconnection" : ""
                  }
                  key={circuit.source_code}
                  x1={from.x}
                  y1={from.y}
                  x2={to.x}
                  y2={to.y}
                />
              ) : null;
            })}
          </g>
          <g className="topology-nodes">
            {nodes.map((node) => (
              <g
                key={node.bus.source_code}
                className={selectedBus === node.bus.source_code ? "selected" : ""}
                transform={`translate(${node.x} ${node.y})`}
                role="button"
                tabIndex={0}
                aria-label={`Select bus ${node.bus.source_code}${node.bus.name ? `, ${node.bus.name}` : ""}, ${node.assets.length} active generator${node.assets.length === 1 ? "" : "s"}${node.bus.demand_mw ? `, demand ${Math.round(node.bus.demand_mw)} megawatts` : ""}`}
                onClick={() => onSelectBus(node.bus.source_code)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    onSelectBus(node.bus.source_code);
                  }
                }}
              >
                <circle className="topology-hit-target" r="22" />
                <circle
                  className={node.bus.demand_mw ? "demand-node" : ""}
                  r={Math.min(18, 9 + node.assets.length * 2)}
                />
                {node.bus.demand_mw &&
                (!node.bus.primary_source || showDemandReferences) ? (
                  <text className="demand-label" y="-22">
                    {Math.round(node.bus.demand_mw)} MW
                  </text>
                ) : null}
                {node.bus.demand_mw &&
                (!node.bus.primary_source || showDemandReferences) ? (
                  <foreignObject x="-8" y="-8" width="16" height="16">
                    <span className="topology-demand-icon">
                      <House size={12} />
                    </span>
                  </foreignObject>
                ) : null}
                <text y="30">{node.bus.source_code}</text>
                {node.assets.slice(0, 3).map((asset, index) => {
                  const Icon =
                    icons[asset.technology as keyof typeof icons] ??
                    icons.unknown;
                  return (
                    <foreignObject
                      key={asset.id}
                      x={-8 + index * 10}
                      y={-8}
                      width="16"
                      height="16"
                    >
                       <span className="topology-asset" aria-hidden="true" title={asset.name}>
                         <Icon size={12} />
                       </span>
                    </foreignObject>
                  );
                })}
              </g>
            ))}
          </g>
        </svg>
      </div>
      <div className="topology-source">
        Derived from tenant-scoped bus and circuit input records. Geographic
        coordinates were not provided; source provenance remains in the inspector.
      </div>
    </div>
  );
}
