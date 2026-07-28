module.exports = {
  PORT: process.env.PORT || 3000,
  SUPPORTED_ASSETS: ["BTCUSDT", "ETHUSDT", "EURUSD", "GBPUSD", "XAUUSD"],
  UPDATE_INTERVAL_MS: 1000,
  CONFIDENCE_THRESHOLD: 1.0, // Requires 100% certainty for dynamic target expansion
  INITIAL_TARGET_MULTIPLIER: 1.5,
  DYNAMIC_STEP_MULTIPLIER: 0.5
};
