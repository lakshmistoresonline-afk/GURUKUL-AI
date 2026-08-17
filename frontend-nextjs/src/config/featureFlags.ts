export const featureFlags = {
  adaptiveMastery: {
    knowledgeGraph: process.env.NEXT_PUBLIC_FLAG_KG === 'true' || true,
    diagnostic: process.env.NEXT_PUBLIC_FLAG_DIAGNOSTIC === 'true' || true,
    conceptSRS: (process.env.NEXT_PUBLIC_FLAG_SRS as 'OFF' | 'SHADOW' | 'ACTIVE') || 'ACTIVE',
    errorAnalysis: (process.env.NEXT_PUBLIC_FLAG_ERROR as 'OFF' | 'SHADOW' | 'ACTIVE') || 'ACTIVE',
    interleaving: (process.env.NEXT_PUBLIC_FLAG_INTERLEAVING as 'OFF' | 'SHADOW' | 'ACTIVE') || 'ACTIVE',
    reviewCoordination: (process.env.NEXT_PUBLIC_FLAG_COORD as 'OFF' | 'SHADOW' | 'ACTIVE') || 'ACTIVE',
  }
};
