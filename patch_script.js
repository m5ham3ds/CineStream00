if (!isCloudflare && document.readyState === 'complete') {
    window._failCount = (window._failCount || 0) + 1;
    var maxFails = (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=')) ? 2 : 4;
    if (window._failCount >= maxFails) { 
        clearInterval(intervalId);
        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
    }
}
