
async function uploadImage() {
  const imageInput = document.getElementById("imageUpload");
  const file = imageInput.files[0];
  if (!file) return alert("Please upload an image first!");

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("/predict", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  document.getElementById("result").innerHTML = `
    <h2>Prediction: ${data.prediction}</h2>
    <p>Care Suggestion: ${data.advice}</p>
  `;
}
