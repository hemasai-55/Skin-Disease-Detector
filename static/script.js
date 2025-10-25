async function uploadImage() {
  const fileInput = document.getElementById('imageUpload');
  const file = fileInput.files[0];
  if (!file) {
    alert("Please choose an image file!");
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch('/upload', {
    method: 'POST',
    body: formData
  });

  const result = await response.json();
  document.getElementById('result').innerHTML = `
    <h3>Prediction: ${result.prediction}</h3>
    <p><strong>Care Suggestion:</strong> ${result.suggestion}</p>
    <img src="${result.image_url}" width="200" style="margin-top:10px;border-radius:10px;">
  `;
}
