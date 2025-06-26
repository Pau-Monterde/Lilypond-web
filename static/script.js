const editor = document.getElementById("editor");
const visor = document.getElementById("visor");
let timeout = null;

// Función para compilar código LilyPond
function compilarLilypond() {
  const formData = new FormData();
  formData.append("code", editor.value);

  fetch("https://TUBACKEND.com/compile", { // ← CAMBIA esta URL por la tuya
    method: "POST",
    body: formData
  })
    .then(res => res.blob())
    .then(blob => {
      const url = URL.createObjectURL(blob);
      visor.src = url;
    })
    .catch(err => console.error("Error al compilar:", err));
}

// Compilación automática con debounce (espera 1s después de teclear)
editor.addEventListener("input", () => {
  clearTimeout(timeout);
  timeout = setTimeout(compilarLilypond, 1000);
});

// Compilar al abrir la página
window.onload = compilarLilypond;
    

