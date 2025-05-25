self.addEventListener('install', event => {
    console.log('Service Worker installing.');
  });

  self.addEventListener('activate', event => {
    console.log('Service Worker activated.');
  });

  self.addEventListener('fetch', function(event) {
    // 通常はキャッシュ対応を入れるが、今回は最低限の構成
  });
