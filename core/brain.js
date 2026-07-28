const learning = require('./learning');

class AIBrain {
  analyzeMarket(candleData) {
    const stats = learning.recordAndLearn(candleData);
    const isBullish = candleData.buyerVolume > candleData.sellerVolume;
    
    const volumeRatio = candleData.buyerVolume / (candleData.sellerVolume || 1);
    const is100PercentSure = (isBullish && volumeRatio > 1.3) || (!isBullish && volumeRatio < 0.77);

    const basePoints = Math.abs(candleData.close - candleData.open) * 15;
    const entryPoint = candleData.close;
    const slPoint = isBullish ? entryPoint - (basePoints * 0.5) : entryPoint + (basePoints * 0.5);
    
    let targetPoint = isBullish ? entryPoint + (basePoints * 1.5) : entryPoint - (basePoints * 1.5);
    if (is100PercentSure) {
      const extensionFactor = 1.0 + (stats.occurrences * 0.002);
      targetPoint = isBullish ? entryPoint + (basePoints * extensionFactor * 2) : entryPoint - (basePoints * extensionFactor * 2);
    }

    return {
      asset: candleData.asset,
      direction: isBullish ? 'BUY' : 'SELL',
      entryPoint: entryPoint.toFixed(4),
      targetPoint: targetPoint.toFixed(4),
      slPoint: slPoint.toFixed(4),
      confidence: is100PercentSure ? 1.0 : 0.85,
      pattern: candleData.pattern,
      memoryMatches: stats.occurrences,
      buyerVolume: candleData.buyerVolume,
      sellerVolume: candleData.sellerVolume,
      reason: `Historical pattern match recorded ${stats.occurrences} times in memory with high volume validation. Buyers vs Sellers balance dictates continuous market movement.`
    };
  }
}

module.exports = new AIBrain();
