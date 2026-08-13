import { describe, expect, it } from 'vitest';
import { finiteCoordinates } from './mapGeometry';

describe('development environment', () => {
  it('identifies the converter product', () => {
    expect('SDDP -> PLEXOS 9').toContain('PLEXOS');
  });

  it('rejects null, undefined and non-finite map coordinates', () => {
    expect(finiteCoordinates(null, null)).toBeNull();
    expect(finiteCoordinates(undefined, -56)).toBeNull();
    expect(finiteCoordinates(Number.NaN, -56)).toBeNull();
    expect(finiteCoordinates(-32.9, -56)).toEqual([-32.9, -56]);
  });
});
