import RendererRegistry, { UnsupportedRendererState } from './RendererRegistry';

describe('RendererRegistry Hardened Tests', () => {
  test('getIntrospection returns registered items', () => {
    const introspection = RendererRegistry.getIntrospection();
    expect(introspection.length).toBeGreaterThan(0);
    expect(introspection.some(i => i.key === '7:mathematics:maths_i:part1:overview')).toBe(true);
    expect(introspection.some(i => i.key === '7:mathematics:maths_ii:part2:overview')).toBe(true);
  });

  test('Exact resolution for Class 5 English', () => {
    const comp = RendererRegistry.get('5:english:english:main:overview');
    expect(comp).toBeDefined();
  });

  test('Exact resolution for Class 6 Mathematics', () => {
    const comp = RendererRegistry.get('6:mathematics:mathematics:main:master');
    expect(comp).toBeDefined();
  });

  test('Exact resolution for Class 7 Maths I and Maths II', () => {
    const mathsI = RendererRegistry.get('7:mathematics:maths_i:part1:notes');
    const mathsII = RendererRegistry.get('7:mathematics:maths_ii:part2:notes');
    expect(mathsI).toBeDefined();
    expect(mathsII).toBeDefined();
    expect(mathsI).not.toBe(mathsII); // Distinct renderers/components or configs
  });

  test('Negative tests: strict isolation and no fallback', () => {
    // Unknown book or wrong part must not resolve via fallback
    const wrongResolution = RendererRegistry.get('7:mathematics:maths_i:part2:overview');
    expect(wrongResolution).toBeUndefined();

    const unknownBook = RendererRegistry.get('5:english:unknown_book:main:overview');
    expect(unknownBook).toBeUndefined();
  });
});
