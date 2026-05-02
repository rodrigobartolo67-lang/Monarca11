const form = document.getElementById('translate-form');
const output = document.getElementById('output');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  output.textContent = 'Procesando archivo...';

  const formData = new FormData(form);

  try {
    const response = await fetch('/api/translate', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      output.textContent = data.error || 'Error desconocido.';
      return;
    }

    output.textContent = data.translatedText;
  } catch (error) {
    output.textContent = `Error de conexión: ${error.message}`;
  }
});
