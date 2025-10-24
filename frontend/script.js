document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("btnCalcular");
  const btnHistorial = document.getElementById("btnHistorial");
  const resultado = document.getElementById("resultado");
  const historial = document.getElementById("historial");

  // 🔹 Detecta automáticamente el host del backend
  let API_URL;

  // Si estás accediendo desde la misma PC donde corre Docker
  if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
    API_URL = "http://localhost:5000";
  } else {
    // Para otras PCs en la LAN: usa la IP del host Docker
    // ⚠️ Cambia "10.7.55.17" por la IP real del host si es diferente
    API_URL = `http://${window.location.hostname}:5000`;
  }

  // 🔹 Función para calcular
  btnCalcular.addEventListener("click", async () => {
    const a = parseFloat(document.getElementById("num1").value);
    const b = parseFloat(document.getElementById("num2").value);
    const op = document.getElementById("operacion").value;

    try {
      const response = await fetch(`${API_URL}/operacion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ a, b, op })
      });

      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      resultado.innerText = data.resultado;
    } catch (err) {
      resultado.innerText = "Error al conectar con el backend";
      console.error("Fetch error:", err);
    }
  });

  // 🔹 Función para obtener historial
  btnHistorial.addEventListener("click", async () => {
    try {
      const response = await fetch(`${API_URL}/historial`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);

      const data = await response.json();
      historial.innerHTML = "";
      data.forEach(row => {
        const li = document.createElement("li");
        li.textContent = `${row.a} ${row.operacion} ${row.b} = ${row.resultado}`;
        historial.appendChild(li);
      });
    } catch (err) {
      historial.innerHTML = "<li>Error al obtener el historial</li>";
      console.error("Fetch error:", err);
    }
  });
});
