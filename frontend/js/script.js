async function analyzeSkin() {

    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    // Show preview
    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/api/skin-analysis", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error || "Error occurred");
            return;
        }

        // Show result section
        document.getElementById("resultBox").style.display = "block";

        // Fill values
        document.getElementById("issue").innerText = data.issue;
        document.getElementById("skinType").innerText = data.skin_type;
        document.getElementById("tan").innerText = data.tan;
        document.getElementById("wrinkles").innerText = data.wrinkles;

        // Recommendations list
        const list = document.getElementById("recommendationList");
        list.innerHTML = "";

        data.recommendation.forEach(item => {
            const li = document.createElement("li");
            li.innerText = item;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}

async function analyzeHair() {

    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image");
        return;
    }

    // 🔥 Show preview
    const preview = document.getElementById("preview");
    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch("/api/hair-analysis", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            alert(data.error || "Error occurred");
            return;
        }

        const result = data.result;

        // Show result box
        document.getElementById("resultBox").style.display = "block";

        // Fill values
        document.getElementById("hairType").innerText = result.hair_type;
        document.getElementById("frizz").innerText = result.frizz;
        document.getElementById("damage").innerText = result.damage;
        document.getElementById("dandruff").innerText = result.dandruff;

        // 🔥 Recommendations (based on hair type)
        const list = document.getElementById("recommendationList");
        list.innerHTML = "";

        let recommendations = [];

        if (result.hair_type === "Dry") {
            recommendations = [
                "Use moisturizing shampoo",
                "Apply hair oil regularly",
                "Avoid heat styling"
            ];
        } else if (result.hair_type === "Oily") {
            recommendations = [
                "Use mild shampoo",
                "Wash hair frequently",
                "Avoid heavy oils"
            ];
        } else {
            recommendations = [
                "Maintain regular hair care routine",
                "Use balanced shampoo",
                "Apply conditioner"
            ];
        }

        recommendations.forEach(item => {
            const li = document.createElement("li");
            li.innerText = item;
            list.appendChild(li);
        });

    } catch (error) {
        console.error(error);
        alert("Server error");
    }
}