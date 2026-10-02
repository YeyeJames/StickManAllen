// 已停用：舊版曾用 Service Worker 讀取裝置上的圖片。
// 留著這個檔案，讓已經裝過的瀏覽器更新後把它自己移除，並清掉舊快取。
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k !== "pages-v2") await caches.delete(k);
  await self.registration.unregister();
})()));
