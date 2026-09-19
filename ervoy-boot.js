// Loads the GRUPO ERVOY design system. React is already provided by the DC
// runtime, so only the stylesheets and the bundle are appended here.
(() => {
  const me = document.currentScript && document.currentScript.src;
  const root = me ? me.slice(0, me.lastIndexOf('/') + 1) : '';
  const base = root + '_ds/grupo-ervoy-882293a9-b810-450d-b354-defe5c9b541d';
  for (const p of ['_ds_bundle.css', 'styles.css']) {
    const l = document.createElement('link');
    l.rel = 'stylesheet';
    l.href = base + '/' + p;
    document.head.appendChild(l);
  }
  const load = () => {
    const s = document.createElement('script');
    s.src = base + '/_ds_bundle.js';
    s.async = false;
    s.onerror = () => console.error('ervoy-boot.js: failed to load ' + s.src);
    document.head.appendChild(s);
  };
  const wait = () => (window.React ? load() : setTimeout(wait, 20));
  wait();
})();
