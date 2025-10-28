const form = document.getElementById('uploadForm');
const imageInput = document.getElementById('imageInput');
const resultDiv = document.getElementById('result');
const errorDiv = document.getElementById('error');
const previewImg = document.getElementById('preview');
const labelP = document.getElementById('label');
const confP = document.getElementById('confidence');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  errorDiv.style.display = 'none';
  resultDiv.style.display = 'none';

  if (!imageInput.files || imageInput.files.length === 0) {
    showError('Please select an image to upload.');
    return;
  }

  const file = imageInput.files[0];
  const formData = new FormData();
  formData.append('image', file);

  try {
    const res = await fetch('/upload', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const error = await res.json();
      showError(error.error || 'Upload failed');
      return;
    }

    const data = await res.json();
    previewImg.src = `/uploads/${data.filename}`;
    labelP.textContent = `Predicted: ${data.label}`;
    confP.textContent = `Confidence: ${data.confidence}`;
    resultDiv.style.display = 'block';
  } catch (err) {
    showError('Network error: ' + err.message);
  }
});

function showError(msg) {
  errorDiv.textContent = msg;
  errorDiv.style.display = 'block';
}

