// Helper function to update the value
function updateValue(buttonId, inputId, operation) {
    const button = document.getElementById(buttonId);
    const input = document.getElementById(inputId);
  
    button.addEventListener("click", () => {
      const currentValue = parseInt(input.value, 10) || 0;
  
      if (operation === "increment") {
        input.value = currentValue + 1;
      } else if (operation === "decrement" && currentValue > 0) {
        input.value = currentValue - 1;
      }
    });
  }
  
  // Add increment and decrement functionality for square feet
  updateValue("increment", "square-feet", "increment");
  updateValue("decrement", "square-feet", "decrement");
  
  // Add increment and decrement functionality for bathrooms
  updateValue("bathroom-increment", "bathrooms", "increment");
  updateValue("bathroom-decrement", "bathrooms", "decrement");
  
  // Add increment and decrement functionality for BHKs
  updateValue("bhk-increment", "bhks", "increment");
  updateValue("bhk-decrement", "bhks", "decrement");
  
