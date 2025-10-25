async function uploadImage() {
    const input = document.getElementById('imageUpload');
    const file = input.files[0];
    if (!file) {
        alert("Please choose an image!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    if (data.error) {
        alert(data.error);
        return;
    }

    document.getElementById("result").innerHTML = `
        <h3>Prediction: ${data.prediction}</h3>
        <p>Care Suggestion: ${data.advice}</p>
        <img src="${data.file_url}" width="250" style="margin-top:10px;border-radius:10px;">
    `;
}
