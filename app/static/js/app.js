function getToken() {
  return localStorage.getItem('token');
}

function showAlert(selector, message, type = 'danger') {
  $(selector).html(`<div class="alert alert-${type}">${message}</div>`);
}

async function apiRequest(url, method = 'GET', body = null, auth = true) {
  const headers = { 'Content-Type': 'application/json' };
  if (auth) {
    const token = getToken();
    if (!token) {
      window.location.href = '/';
      throw new Error('Session expired');
    }
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || 'Request failed');
  }

  return data;
}

function requireAuth() {
  if (!getToken()) {
    window.location.href = '/';
  }
}

function bindLogout() {
  $('#logoutBtn').on('click', function () {
    localStorage.removeItem('token');
    window.location.href = '/';
  });
}

async function hydrateCurrentOperator(nameSelector, welcomeSelector = null) {
  try {
    const current = await apiRequest('/api/auth/me', 'GET', null, true);
    const currentName = current.full_name || 'Operator';
    $(nameSelector).text(currentName);
    if (welcomeSelector) {
      $(welcomeSelector).text(`Welcome, ${currentName}`);
    }
  } catch (_) {
    // noop
  }
}
