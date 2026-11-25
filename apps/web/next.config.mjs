/** The normal Next.js server remains the default; the free demo exports the same client UI. */
export default {
  ...(process.env.FINCORE_STATIC_EXPORT === 'true' ? {output: 'export'} : {}),
};
