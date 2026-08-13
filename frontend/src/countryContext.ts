export type CountryContext = {
  name: string;
  center: [number, number];
  bounds: [[number, number], [number, number]];
};

const contexts: Record<string, CountryContext> = {
  pe: { name: "Peru", center: [-9.2, -75.0], bounds: [[-18.5, -81.5], [0.0, -68.5]] },
  ur: { name: "Uruguay", center: [-32.9, -56.0], bounds: [[-35.2, -58.5], [-30.0, -53.0]] },
  pa: { name: "Panama", center: [8.5, -80.0], bounds: [[7.0, -83.2], [9.7, -77.0]] },
  cr: { name: "Costa Rica", center: [9.9, -84.2], bounds: [[8.0, -86.0], [11.3, -82.5]] },
};

export function getCountryContext(countryCode?: string | null): CountryContext | null {
  return countryCode ? contexts[countryCode.toLowerCase()] ?? null : null;
}
