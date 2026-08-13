export type MapCoordinates = [number, number];

export function finiteCoordinates(latitude: unknown, longitude: unknown): MapCoordinates | null {
  return typeof latitude === 'number' && Number.isFinite(latitude) && typeof longitude === 'number' && Number.isFinite(longitude)
    ? [latitude, longitude]
    : null;
}
