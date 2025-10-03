document.addEventListener("DOMContentLoaded", () => {
  const btnCalcular = document.getElementById("btnCalcular");
  const btnHistorial = document.getElementById("btnHistorial");
  const resultado = document.getElementById("resultado");
  const historial = document.getElementById("historial");

  // 🔹 API_URL apunta a la IP de tu host Docker
  const API_URL = "http://10.7.55.226:5000";

  // 🔹 Calcular
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
      console.error(err);
    }
  });

  // 🔹 Historial
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
      console.error(err);
    }
  });
});
