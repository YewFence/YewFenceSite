/* Simple front-end only auth utils (no backend). */
(function (global) {
  const STORAGE_KEY = 'mysite-auth';
  // For demo: store a SHA-256 hash of the password (still local, not secure for real use)

  async function sha256(text) {
    const enc = new TextEncoder();
    const data = enc.encode(text);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  }

  async function savePassword(password) {
    const hash = await sha256(password);
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ hash }));
  }

  async function checkPassword(password) {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return false;
    try {
      const { hash } = JSON.parse(raw);
      const candidate = await sha256(password);
      return candidate === hash;
    } catch {
      return false;
    }
  }

  function isAuthenticated() {
    // A very naive auth flag: set when login succeeded for this session
    return sessionStorage.getItem(STORAGE_KEY + ':session') === '1';
  }

  function setAuthenticated(flag) {
    if (flag) sessionStorage.setItem(STORAGE_KEY + ':session', '1');
    else sessionStorage.removeItem(STORAGE_KEY + ':session');
  }

  async function ensurePasswordInitialized(defaultPassword) {
    // If no password saved, initialize with default
    if (!localStorage.getItem(STORAGE_KEY)) {
      await savePassword(defaultPassword);
    }
  }

  global.Auth = { savePassword, checkPassword, isAuthenticated, setAuthenticated, ensurePasswordInitialized };
})(window);
