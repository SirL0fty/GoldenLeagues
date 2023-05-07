const apiKey = 'deb3810bce774c36b0d3f2a13de05b2b';
const url = `https://api.openweathermap.org/data/2.5/weather?units=metric&q=`;

const searchBox = document.querySelector('.search input');
const searchBtn = document.querySelector('.search button');
const weatherIcon = document.querySelector('.weather-icon');

async function checkWeather(city = 'Southampton') {
  const response = await fetch(`${url}${city}&appid=${apiKey}`);
  const data = await response.json();

  if (data.cod === '404') {
    alert('Location not found. Please try again.');
    return;
  }

  console.log(data);

  document.querySelector('.weather-city').innerHTML = data.name;
  document.querySelector('.weather-temp').innerHTML = Math.round(data.main.temp) + '°C';
  document.querySelector('.weather-humidity').innerHTML = data.main.humidity + '%';
  document.querySelector('.weather-wind').innerHTML = data.wind.speed + 'km/h';

  if (data.weather[0].main == 'Clouds') {
    weatherIcon.src = 'static/assets/weather-icons/clouds.png';
  } else if (data.weather[0].main == 'Rain') {
    weatherIcon.src = 'static/assets/weather-icons/rain.png';
  } else if (data.weather[0].main == 'Snow') {
    weatherIcon.src = 'static/assets/weather-icons/snow.png';
  } else if (data.weather[0].main == 'Clear') {
    weatherIcon.src = 'static/assets/weather-icons/clear.png';
  } else if (data.weather[0].main == 'Drizzle') {
    weatherIcon.src = 'static/assets/weather-icons/drizzle.png';
  }

  localStorage.setItem('defaultCity', city);
}

searchBtn.addEventListener('click', () => {
  checkWeather(searchBox.value);
});

searchBox.addEventListener('keydown', (event) => {
  if (event.keyCode === 13) {
    checkWeather(searchBox.value);
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const defaultCity = localStorage.getItem('defaultCity');
  if (defaultCity) {
    checkWeather(defaultCity);
    searchBox.value = defaultCity;
  } else {
    checkWeather();
  }
});
