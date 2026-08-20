# SDDP Format Catalog

Source analyzed: `docs/SddpFilEsp (1).pdf`, converted locally with Microsoft MarkItDown to `docs/sddp-manual.md`.

## Manual Findings

The manual is for SDDP file format version 17.2. It documents input families rather than one universal `.dat` schema:

- System data and execution options: `PATH.DAT`, `SISTEM.DAT`, `SDDP.DAT`, `UNIMON.DAT`, fixed/variable block duration files.
- Hydroelectric plants: `CHIDROXX.DAT`, modification, maintenance, water-use, maximum/minimum defluence, spillage, volume limits, stored energy and operational restrictions.
- Thermal plants: `CTERMIXX.DAT`, modification, block consumption, maintenance, fuel configuration/prices/availability, minimum generation, startup, combined-cycle state, emissions and fuel contracts.
- Mixed restrictions and reserves: generation restrictions, primary reserve, secondary reserve and their modifications.
- Transmission interconnection model: exchanges, aggregate exchange constraints and exchange costs.
- Power-flow network model: buses, circuits, DC links, electrical areas, flow sums, import/export limits and international circuit costs.
- Demand and energy prices: demand by bus, demand energy series and energy prices.
- Hydrology: hydro stations, historical flows, parameter files, `FORW.DAT`, `BACK.DAT`, reduced uncertainty and climate variables.
- Renewable sources and batteries: renewable configuration/scenarios and battery charge/discharge tables.
- Operational and output artifacts: reports, graph/control files, logs and simulation result files.

The manual repeatedly defines ASCII files with fixed-position fields, headers and multiple record types. It also describes dynamic files selected by the study configuration and files whose names encode stage (`ZZ`), period (`YY`), system (`XX`) or block count (`YYY`).

## Dataset Evidence: `data/UY_SDDP`

The Uruguay dataset is not limited to input ASCII files:

- `.dat`: 40 files, including readable inputs such as `sddp.dat`, `mgndur.dat`, `mtermiur.dat`, `mcirc.dat`, `pmhimeur.dat` and `pmtrmeur.dat`; some `.dat` artifacts are binary.
- `.csv`: dashboards, costs, risk, cuts, convergence and other generated reports.
- `.hdr` + `.bin`: paired binary series such as `inflow`, `losses`, `maxflw`, `qverti`, `volini`, `wdrbus` and `vergnd`.
- `.psr`: binary simulation/result series such as `vinsim.psr`, `vinpol.psr` and `userunit.psr`.
- `.log`, `.out`, `.grf`, `.all`, `.ok`, `.bak`, `.xlsx`: diagnostics, execution metadata, graph/control files and exported reports.

The initial parser therefore uses a lossless inventory strategy. It hashes and records every file, size, extension and kind. It stores line-level records for text files and preserves binary metadata without guessing an undocumented binary schema.

## Parsing Rules

1. Read bytes first; never assume UTF-8.
2. Detect and persist encoding for text files.
3. Preserve the original line, line number, section marker and tokenization.
4. Treat `$version`, `!`, `#`, `*`, `****` and `MOD:` lines as structural/comment metadata, not ordinary data.
5. Keep fixed-width parsing separate from whitespace-token parsing. The current inventory parser preserves both; family-specific schemas will be added after validating field positions against the manual.
6. Model the study identity, system identifier, stage/period, block and record type explicitly.
7. Do not convert SDDP blocks to hourly data during parsing. Temporal semantic conversion belongs to a later mapping layer.
8. Do not decode `.bin`, `.hdr` or `.psr` by heuristic. Require official format documentation or a validated reader and retain the original bytes/hash.
9. Every warning must include file path and line/record provenance.

## Initial Implementation

- Generic parser: `backend/app/services/dataset_parser.py`
- Persistent inventory: `DatasetFile`
- Lossless text records: `DatasetRecord`
- Command: `python -m app.cli data/UY_SDDP --project "UY SDDP"`
- Domain guidance: `.opencode/skills/sddp-domain/SKILL.md`
- Specialist subagent: `.opencode/agents/sddp-parser-specialist.md`

## Next Family Parsers

Implement and test in this order:

1. `SDDP.DAT`, `SISTEM.DAT`, `UNIMON.DAT` and block duration files.
2. `MGNDXX.DAT`, `CTERMIXX.DAT`, `CHIDROXX.DAT` and `MCIRC.DAT`.
3. Maintenance and dynamic modification families.
4. Demand, hydrology, transmission, reserves and restrictions.
5. Dashboard/result CSVs.
6. Official binary readers for paired `.hdr`/`.bin` and `.psr` artifacts.
