<script>
const form = document.getElementById('contactForm');
const resultDiv = document.getElementById('formResult');

form.addEventListener('submit', async (e) => {
  e.preventDefault(); // отменяем стандартную отправку формы

  // Валидация Bootstrap
  if (!form.checkValidity()) {
    form.classList.add('was-validated');
    return;
  }

  const formData = new FormData(form);

  try {
    const response = await fetch('http://127.0.0.1:8000/send-message', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();

    if (data.status === 'success') {
      resultDiv.innerHTML = '<div class="alert alert-success">Сообщение отправлено!</div>';
      form.reset();
      form.classList.remove('was-validated');
    } else {
      resultDiv.innerHTML = '<div class="alert alert-danger">Ошибка при отправке сообщения.</div>';
    }
  } catch (err) {
    resultDiv.innerHTML = '<div class="alert alert-danger">Ошибка соединения с сервером.</div>';
  }
});
</script>