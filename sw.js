// 漫畫圖片優先從這台裝置的快取讀（index.html 會在背景把每一頁存進 "pages-v1"）。
// 只處理 books/ 底下的 .jpg；網頁本身（index.html）照常走網路，更新不受影響。
const PAGE_CACHE = "pages-v1";

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(self.clients.claim()));

self.addEventListener("fetch", e => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (!/\/books\/.+\.jpg$/.test(url.pathname)) return;
  if (url.searchParams.has("r")) return; // 載入失敗後的重試：直接走網路
  e.respondWith((async () => {
    const cache = await caches.open(PAGE_CACHE);
    const hit = await cache.match(req, { ignoreVary: true });
    if (hit) return hit;
    const res = await fetch(req);
    if (res.ok) cache.put(req, res.clone()).catch(() => {});
    return res;
  })());
});
