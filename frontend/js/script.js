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

function getImageFile() {
  return document.getElementById('imageInput').files[0] || null;
}
 
function showPreview(file) {
  const preview = document.getElementById('preview');
  const placeholder = document.getElementById('previewPlaceholder');
  if (preview && file) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
  }
  if (placeholder) {
    placeholder.style.display = 'none';
  }
}
 
function setStatus(message, type) {
  const statusEl = document.getElementById('status');
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = '';
  statusEl.style.display = 'block';
  if (type === 'error')   statusEl.classList.add('status-error');
  if (type === 'loading') statusEl.classList.add('status-loading');
  if (type === 'success') statusEl.classList.add('status-success');
}
 
 
// ======================================
// HAIR ANALYSIS
// ======================================
 
async function analyzeHair() {
 
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
    const res = await fetch("/api/hair-analysis", {
      method: "POST",
      body: formData
    });
 
    if (!res.ok) {
      throw new Error("Server response failed");
    }
 
    const data = await res.json();
 
    console.log("✅ HAIR RESPONSE:", data);
 
    if (!data.success) {
      setStatus("❌ " + (data.error || "Analysis failed"), "error");
      return;
    }
 
    // Show success
    setStatus("✅ Hair Analysis Complete", "success");
 
    // Show result box
    const box = document.getElementById("resultBox");
    if (box) box.style.display = "block";
 
    // Show product section
    const productSection = document.getElementById("productSection");
    if (productSection) productSection.style.display = "block";
 
    // Set result values safely
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.innerText = val ?? "-";
    };
 
    setVal("hairType", data.hair_type);
    setVal("frizz",    data.frizz);
    setVal("damage",   data.damage);
    setVal("dandruff", data.dandruff);
 
    // Populate recommendations
    const list = document.getElementById("hairRecommendationList");
 
    if (!list) {
      console.error("❌ hairRecommendationList not found in HTML");
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
    console.error("❌ HAIR ERROR:", err);
    setStatus("❌ Server error", "error");
  }
}
// ======================================
// SKIN ANALYSIS ✅ (UPDATED)
// ======================================



// ======================================
// SHARED UTILITIES
// ======================================

function getImageFile() {
  return document.getElementById('imageInput').files[0] || null;
}

function showPreview(file) {
  const preview = document.getElementById('preview');
  const placeholder = document.getElementById('previewPlaceholder');
  if (preview && file) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
  }
  if (placeholder) {
    placeholder.style.display = 'none';
  }
}

function setStatus(message, type) {
  const statusEl = document.getElementById('status');
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = '';
  statusEl.style.display = 'block';
  if (type === 'error')   statusEl.classList.add('status-error');
  if (type === 'loading') statusEl.classList.add('status-loading');
  if (type === 'success') statusEl.classList.add('status-success');
}


// ======================================
// CONDITION → PRODUCT SECTION MAPPING
// ======================================

function showSkinProducts(condition) {
  // Hide all product sections first
  const allSections = [
    'products-normal',
    'products-infection',
    'products-rashes',
    'products-allergy'
  ];
  allSections.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });

  // Normalize condition string for matching
  const c = (condition || '').toLowerCase();

  let sectionId = 'products-normal'; // default fallback

  if (c.includes('infection') || c.includes('fungal') || c.includes('bacterial') || c.includes('ringworm')) {
    sectionId = 'products-infection';
  } else if (c.includes('rash') || c.includes('eczema') || c.includes('dermatitis') || c.includes('psoriasis')) {
    sectionId = 'products-rashes';
  } else if (c.includes('allerg') || c.includes('hives') || c.includes('urticaria') || c.includes('contact')) {
    sectionId = 'products-allergy';
  } else if (c.includes('normal') || c.includes('healthy') || c.includes('clear')) {
    sectionId = 'products-normal';
  }

  const targetSection = document.getElementById(sectionId);
  if (targetSection) targetSection.style.display = 'block';
}


// ======================================
// SKIN ANALYSIS
// ======================================



function getImageFile() {
  return document.getElementById('imageInput').files[0] || null;
}

function showPreview(file) {
  const preview = document.getElementById('preview');
  const placeholder = document.getElementById('previewPlaceholder');
  if (preview && file) {
    preview.src = URL.createObjectURL(file);
    preview.style.display = 'block';
  }
  if (placeholder) {
    placeholder.style.display = 'none';
  }
}

function setStatus(message, type) {
  const statusEl = document.getElementById('status');
  if (!statusEl) return;
  statusEl.textContent = message;
  statusEl.className = '';
  statusEl.style.display = 'block';
  if (type === 'error')   statusEl.classList.add('status-error');
  if (type === 'loading') statusEl.classList.add('status-loading');
  if (type === 'success') statusEl.classList.add('status-success');
}


// ======================================
// CONDITION → PRODUCT SECTION MAPPING
// ======================================

function showSkinProducts(condition) {
  // Hide all product sections first
  const allSections = [
    'products-normal',
    'products-infection',
    'products-rashes',
    'products-allergy'
  ];
  allSections.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });

  // Normalize condition string for matching
  const c = (condition || '').toLowerCase();

  let sectionId = 'products-normal'; // default fallback

  if (c.includes('infection') || c.includes('fungal') || c.includes('bacterial') || c.includes('ringworm')) {
    sectionId = 'products-infection';
  } else if (c.includes('rash') || c.includes('eczema') || c.includes('dermatitis') || c.includes('psoriasis')) {
    sectionId = 'products-rashes';
  } else if (c.includes('allerg') || c.includes('hives') || c.includes('urticaria') || c.includes('contact')) {
    sectionId = 'products-allergy';
  } else if (c.includes('normal') || c.includes('healthy') || c.includes('clear')) {
    sectionId = 'products-normal';
  }

  const targetSection = document.getElementById(sectionId);
  if (targetSection) targetSection.style.display = 'block';
}




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

    console.log("SKIN RESPONSE:", data);

    if (!data.success) {
      setStatus("❌ " + (data.error || "Analysis failed"), "error");
      return;
    }

    // Show success
    setStatus("✅ Skin Analysis Complete", "success");

    // Show result box
    const resultBox = document.getElementById("resultBox");
    if (resultBox) resultBox.style.display = "block";

    // Set result values safely
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.innerText = val ?? "-";
    };

    setVal("skinCondition",  data.condition);
    setVal("skinConfidence", data.confidence !== undefined ? data.confidence + "%" : "-");
    setVal("skinType",       data.skin_type);

    // Show the correct product section based on detected condition
    showSkinProducts(data.condition);

    // Populate recommendations
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