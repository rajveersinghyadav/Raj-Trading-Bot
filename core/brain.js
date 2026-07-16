// core/brain.js - Updated for Multi-Asset
const config = require('../config');

async function analyze(marketData, asset) {
    console.log(`Brain: ${asset} ka data analyse ho raha hai...`);
    
    // Yahan hum har asset ke liye alag logic set karenge
    if (asset === 'XAUUSD') {
        // Gold ke liye logic: thoda zyada conservative rahenge
        if (marketData.price > 2000) return { action: 'BUY', confidence: 0.8 };
    } else {
        // Baki assets ke liye normal logic
        if (marketData.volume > 100) return { action: 'BUY', confidence: 0.7 };
    }
    
    return { action: 'HOLD', confidence: 0 };
}

module.exports = { analyze };
