document.addEventListener("DOMContentLoaded", () => {
  const locationDropdown = document.getElementById("location2");
  const sqftInput = document.getElementById("square-feet");
  const bathInput = document.getElementById("bathrooms");
  const bhkInput = document.getElementById("bhks");
  const outputArea = document.getElementById("output-area");
  const checkButton = document.querySelector(".submit-btn");

  // Load Bangalore locations
  fetch("http://127.0.0.1:5000/api/get_location_names")
    .then((res) => res.json())
    .then((data) => {
      const locations = data.locations;
      locationDropdown.innerHTML = "";
      locations.forEach((loc) => {
        const option = document.createElement("option");
        option.value = loc;
        option.textContent = loc;
        locationDropdown.appendChild(option);
      });
    })
    .catch((err) => {
      console.error("Failed to load locations:", err);
      outputArea.textContent = "Failed to load locations.";
    });

  // Add increment/decrement logic
  function setupStepper(inputId, decId, incId) {
    const input = document.getElementById(inputId);
    document.getElementById(decId).addEventListener("click", () => {
      let value = parseInt(input.value) || 0;
      if (value > 0) input.value = value - 1;
    });
    document.getElementById(incId).addEventListener("click", () => {
      let value = parseInt(input.value) || 0;
      input.value = value + 1;
    });
  }

  setupStepper("square-feet", "decrement", "increment");
  setupStepper("bathrooms", "bathroom-decrement", "bathroom-increment");
  setupStepper("bhks", "bhk-decrement", "bhk-increment");

  // Submit form and fetch prediction
  checkButton.addEventListener("click", () => {
    const sqft = parseFloat(sqftInput.value);
    const bath = parseInt(bathInput.value);
    const bhk = parseInt(bhkInput.value);
    const location = locationDropdown.value;

    if (!sqft || !bath || !bhk || !location) {
      outputArea.textContent = "Please fill in all fields.";
      return;
    }

    fetch("http://127.0.0.1:5000/api/predict_home_price", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        total_sqft: sqft,
        bath: bath,
        bhk: bhk,
        location: location
      })
    })
      .then((res) => res.json())
      .then((data) => {
        const price = data.estimated_price;
        outputArea.textContent = price + " Lakh";
      })
      .catch((err) => {
        console.error("Prediction failed:", err);
        outputArea.textContent = "Error fetching price.";
      });
  });
});
