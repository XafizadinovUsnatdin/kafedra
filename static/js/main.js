document.addEventListener('DOMContentLoaded', function () {

  // ── Dark mode ─────────────────────────────────────────
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  const toggleBtn = document.getElementById('darkToggle');
  if (toggleBtn) {
    updateToggleIcon(savedTheme);
    toggleBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('theme', next);
      updateToggleIcon(next);
    });
  }

  function updateToggleIcon(theme) {
    const icon = document.getElementById('darkToggleIcon');
    if (icon) {
      icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
  }

  // ── Auto-dismiss alerts ────────────────────────────────
  setTimeout(function () {
    document.querySelectorAll('.alert-auto').forEach(function (el) {
      new bootstrap.Alert(el).close();
    });
  }, 4000);

  // ── Confirm delete ─────────────────────────────────────
  document.querySelectorAll('.btn-delete-confirm').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      if (!confirm("Haqiqatan ham o'chirmoqchimisiz?")) e.preventDefault();
    });
  });

  // ── Sidebar toggle (mobile) ───────────────────────────
  const sidebarToggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggleBtn && sidebar) {
    sidebarToggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });
  }

  // ── Highlight active sidebar link ─────────────────────
  const path = window.location.pathname;
  document.querySelectorAll('.sidebar .nav-link').forEach(function (link) {
    const href = link.getAttribute('href');
    if (href && href !== '/' && path.startsWith(href)) {
      link.classList.add('active');
    } else if (href === '/' && path === '/') {
      link.classList.add('active');
    }
  });

  // ── Chart.js dark mode defaults ───────────────────────
  if (typeof Chart !== 'undefined') {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    Chart.defaults.color = isDark ? '#95a5a6' : '#666';
    Chart.defaults.borderColor = isDark ? '#3a3f4b' : '#e0e0e0';
  }
});
