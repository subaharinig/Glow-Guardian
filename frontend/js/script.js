async function analyzeSkin() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/api/skin-analysis", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById("result").innerText = data.error;
            return;
        }

        document.getElementById("result").innerText =
            `Skin Type: ${data.skin_type}
Acne: ${data.acne}
Recommendation: ${data.recommendation}`;

    } catch (error) {
        console.error(error);
        alert("Error connecting to server");
    }
}