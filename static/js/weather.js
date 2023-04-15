fetch(`https://api.openweathermap.org/data/2.5/weather?lat=50.877&lon=-1.328&appid=deb3810bce774c36b0d3f2a13de05b2b`)
  .then((response) => response.json())
  .then((data) => {
    // Extract weather information from API response
    const city = data.name;
    const weatherDescription = data.weather[0].description;
    const temperatureInKelvin = data.main.temp;
    const humidity = data.main.humidity;
    const weatherConditionCode = data.weather[0].icon; // Get weather condition code
    const { icon } = data.weather[0];
    const weatherIconElement = document.getElementById('weather-icon');

    // Convert temperature to Celsius and round it to the nearest integer
    const temperatureInCelsius = Math.round(temperatureInKelvin - 273.15);

    // Update weather widget with weather information
    document.getElementById('city').textContent = `${city}`;
    document.getElementById('weather-description').textContent = `${weatherDescription}`;
    document.getElementById('temperature').textContent = `${temperatureInCelsius}°C`;
    document.getElementById('humidity').textContent = `Humidity: ${humidity}%`;

    // Update weather icon based on weather condition code
    weatherIconElement.className = 'weather-icon'; // Reset weather icon classes
    weatherIconElement.classList.add('wi', `wi-owm-${weatherConditionCode}`); // Add weather icon classes based on the condition
    weatherIconElement.innerHTML = `<img src="/static/assets/weather-icons/${icon}.png">`;
  })
  .catch((error) => {
    console.error('Failed to fetch weather data:', error);
  });
