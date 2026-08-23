(function () {
  var host = (location.hostname || '').toLowerCase();
  if (host !== 'cenzyk.art' && host !== 'www.cenzyk.art') return;
  var target = 'https://илай-металл.рф' + location.pathname + location.search + location.hash;
  location.replace(target);
})();
