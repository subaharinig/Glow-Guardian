// ======================================
// COMMON
// ======================================
function getImageFile() {
    return document.getElementById("imageInput").files[0];
}

function showPreview(file) {
    const preview = document.getElementById("preview");
    if (preview) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
    }
}

function setStatus(msg, type = "") {
    const status = document.getElementById("status");
    if (!status) return;

    status.innerText = msg;
    status.className = "status " + type;
}


// ======================================
// FACE ANALYSIS ✅
// ======================================
async function analyzeFace() {

    const file = getImageFile();

    if (!file) {
        setStatus("❌ Please select an image", "error");
        return;
    }

    showPreview(file);
    setStatus("⏳ Analyzing...", "loading");

    const formData = new FormData();
    formData.append("image", file);

    try {
        const res = await fetch("/api/face-analysis", {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (!data.success) {
            setStatus("❌ " + data.error, "error");
            return;
        }

        setStatus("✅ Analysis Complete", "success");

        document.getElementById("resultBox").style.display = "block";

        document.getElementById("issue").innerText = data.issue;
        document.getElementById("skinType").innerText = data.skin_type;
        document.getElementById("tan").innerText = data.tan;
        document.getElementById("wrinkles").innerText = data.wrinkles;

        const list = document.getElementById("recommendationList");
        list.innerHTML = "";

        data.recommendation.forEach(item => {
            const li = document.createElement("li");
            li.innerText = item;
            list.appendChild(li);
        });

    } catch (err) {
        console.error(err);
        setStatus("❌ Server error", "error");
    }
}


// ======================================
// HAIR ANALYSIS
// ======================================
async function analyzeHair() {

    const file = getImageFile();

    if (!file) {
        alert("Select image");
        return;
    }

    showPreview(file);

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch("/api/hair-analysis", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (!data.success) return alert(data.error);

    const r = data.result;

    document.getElementById("resultBox").style.display = "block";

    document.getElementById("hairType").innerText = r.hair_type;
    document.getElementById("frizz").innerText = r.frizz;
    document.getElementById("damage").innerText = r.damage;
    document.getElementById("dandruff").innerText = r.dandruff;
}


// ======================================
// SKIN ANALYSIS
// ======================================
async function analyzeSkin() {

    const file = getImageFile();

    if (!file) {
        alert("Select image");
        return;
    }

    showPreview(file);

    const formData = new FormData();
    formData.append("image", file);

    const res = await fetch("/api/skin-analysis", {
        method: "POST",
        body: formData
    });

    const data = await res.json();

    if (!data.success) return alert(data.error);

    document.getElementById("result").innerHTML = `
        <h3>🧠 Skin Analysis</h3>
        <p><b>Condition:</b> ${data.condition}</p>
        <p><b>Confidence:</b> ${data.confidence}%</p>
        <p><b>Skin Type:</b> ${data.skin_type}</p>

        <h4>💡 Recommendations:</h4>
        <ul>
            ${data.recommendation.map(r => `<li>${r}</li>`).join("")}
        </ul>
    `;
}