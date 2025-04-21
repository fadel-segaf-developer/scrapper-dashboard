function getValueA() {
    fetch('/api/get_a')
      .then(res => res.json())
      .then(data => {
        document.getElementById('output').textContent = 'Value A: ' + data.result;
      });
  }

  function getValueB() {
    fetch('/api/get_b')
      .then(res => res.json())
      .then(data => {
        document.getElementById('output').textContent = 'Value B: ' + data.result;
      });
  }

  function postValueC() {
    fetch('/api/post_c', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        document.getElementById('output').textContent = 'Posted: ' + data.status;
      });
  }

  function changeTheme(theme) {
    document.body.setAttribute('data-theme', theme);
  }


const ws = new WebSocket("ws://127.0.0.1:5000/ws/files");

ws.onopen = () => console.log("✅ WebSocket connected");
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log("📩 Message from server:", data);
  document.getElementById("output").textContent = data.message;
};

ws.onerror = (e) => console.error("❌ WebSocket error", e);
ws.onclose = function () {
  document.getElementById("output").textContent = "❌ Lost connection to file monitor.";
};

