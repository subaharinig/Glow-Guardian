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
// FACE ANALYSIS ✅ (UPDATED)
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

        if (!res.ok) throw new Error("Server response failed");

        const data = await res.json();

        console.log("FACE RESPONSE:", data);

        if (!data.success) {
            setStatus("❌ " + (data.error || "Analysis failed"), "error");
            return;
        }

        setStatus("✅ Analysis Complete", "success");

        document.getElementById("resultBox").style.display = "block";
        document.getElementById("productSection").style.display = "block";

        document.getElementById("issue").innerText = data.issue || "-";
        document.getElementById("skinType").innerText = data.skin_type || "-";
        document.getElementById("tan").innerText = data.tan || "-";
        document.getElementById("wrinkles").innerText = data.wrinkles || "-";

        const list = document.getElementById("recommendationList");
        list.innerHTML = "";

        if (data.recommendation && data.recommendation.length > 0) {
            data.recommendation.forEach(item => {
                const li = document.createElement("li");
                li.innerText = item;
                list.appendChild(li);
            });
        } else {
            const li = document.createElement("li");
            li.innerText = "No recommendations available";
            list.appendChild(li);
        }

    } catch (err) {
        console.error("FACE ERROR:", err);
        setStatus("❌ Server error", "error");
    }
}

// ======================================
// HAIR ANALYSIS ✅ (UPDATED)
// ======================================

async function analyzeHair() {

    const file = getImageFile();

    if (!file) {
        setStatus("❌ Please select an image", "error");
        return;
    }

    // Preview
    showPreview(file);

    // Status
    setStatus("⏳ Analyzing...", "loading");

    const formData = new FormData();
    formData.append("image", file);

    try {
        const res = await fetch("/api/hair-analysis", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            throw new Error("Server response failed");
        }

        const data = await res.json();

        console.log("✅ HAIR RESPONSE:", data); // DEBUG

        if (!data.success) {
            setStatus("❌ " + (data.error || "Analysis failed"), "error");
            return;
        }

        // ✅ Show success
        setStatus("✅ Hair Analysis Complete", "success");

        // ✅ Show result box
        const box = document.getElementById("resultBox");
        if (box) box.style.display = "block";

        // ✅ Set values safely
        document.getElementById("hairType").innerText = data.hair_type ?? "-";
        document.getElementById("frizz").innerText = data.frizz ?? "-";
        document.getElementById("damage").innerText = data.damage ?? "-";
        document.getElementById("dandruff").innerText = data.dandruff ?? "-";

        // ✅ IMPORTANT: Use UNIQUE ID (fix your HTML also)
        const list = document.getElementById("hairRecommendationList");

        if (!list) {
            console.error("❌ hairRecommendationList not found in HTML");
            return;
        }

        list.innerHTML = "";

        // ✅ Add recommendations
        if (Array.isArray(data.recommendation) && data.recommendation.length > 0) {

            data.recommendation.forEach(item => {
                const li = document.createElement("li");
                li.innerText = item;
                list.appendChild(li);
            });

        } else {

            const li = document.createElement("li");
            li.innerText = "No recommendations available";
            list.appendChild(li);
        }

    } catch (err) {
        console.error("❌ HAIR ERROR:", err);
        setStatus("❌ Server error", "error");
    }
}

// ======================================
// SKIN ANALYSIS ✅ (UPDATED)
// ======================================



async function analyzeSkin() {

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
        const res = await fetch("/api/skin-analysis", {
            method: "POST",
            body: formData
        });

        if (!res.ok) throw new Error("Server error");

        const data = await res.json();

        console.log("SKIN RESPONSE:", data); // 🔍 DEBUG

        if (!data.success) {
            setStatus("❌ " + data.error, "error");
            return;
        }

        setStatus("✅ Skin Analysis Complete", "success");

        const resultBox = document.getElementById("result");
        resultBox.style.display = "block";

        // =========================
        // Set basic values
        // =========================
        document.getElementById("skinCondition").innerText = data.condition || "-";
        document.getElementById("skinConfidence").innerText = data.confidence || "-";
        document.getElementById("skinType").innerText = data.skin_type || "-";

        // =========================
        // Recommendations (LIKE HAIR)
        // =========================
        const list = document.getElementById("skinRecommendationList");

        if (!list) {
            console.error("❌ skinRecommendationList not found in HTML");
            return;
        }

        list.innerHTML = "";

        if (Array.isArray(data.recommendation) && data.recommendation.length > 0) {

            data.recommendation.forEach(item => {
                const li = document.createElement("li");
                li.innerText = item;
                list.appendChild(li);
            });

        } else {

            const li = document.createElement("li");
            li.innerText = "No recommendations available";
            list.appendChild(li);
        }

    } catch (err) {
        console.error("SKIN ERROR:", err);
        setStatus("❌ Server error", "error");
    }
}