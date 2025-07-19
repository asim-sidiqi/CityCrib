document.addEventListener("DOMContentLoaded", () => {
  const cityDropdown = document.getElementById("location"); // New
  const locationDropdown = document.getElementById("location2");
  const sqftInput = document.getElementById("square-feet");
  const bathInput = document.getElementById("bathrooms");
  const bhkInput = document.getElementById("bhks");
  const outputArea = document.getElementById("output-area");
  const checkButton = document.querySelector(".submit-btn");

  function loadLocations(city) {
    fetch(`https://citycrib.onrender.com/api/get_location_names?city=${city}`)
      .then((res) => res.json())
      .then((data) => {
        const locations = data.locations;
        if (!locations || !Array.isArray(locations)) {
          throw new Error("Invalid response format: locations not found");
      }
        locationDropdown.innerHTML = "";
        locations.forEach((loc) => {
          const capitalized = loc
            .split(" ")
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
          const option = document.createElement("option");
          option.value = loc;
          option.textContent = capitalized;
          locationDropdown.appendChild(option);
        });
      })
      .catch((err) => {
        console.error("Failed to load locations:", err);
        outputArea.textContent = "Failed to load locations.";
      });
  }

  // Load default city (e.g., Bangalore) on page load
  loadLocations(cityDropdown.value);

  // Reload locations when city changes
  cityDropdown.addEventListener("change", () => {
    const selectedCity = cityDropdown.value;
    loadLocations(selectedCity);
  });

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

  checkButton.addEventListener("click", () => {
    const sqft = parseFloat(sqftInput.value);
    const bath = parseInt(bathInput.value);
    const bhk = parseInt(bhkInput.value);
    const location = locationDropdown.value;
    const city = cityDropdown.value;

    if (!sqft || !bath || !bhk || !location || !city) {
      outputArea.textContent = "Please fill in all fields.";
      return;
    }

    fetch("https://citycrib.onrender.com/api/predict_home_price", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        city: city,
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
