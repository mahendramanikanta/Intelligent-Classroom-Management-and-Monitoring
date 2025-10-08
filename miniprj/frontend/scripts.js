async function fetchData() {
  try {
    const response = await fetch("http://localhost:5000/latest");
    const data = await response.json();

    if (data.length > 0) {
      const latest = data[0];

      document.getElementById("temp").textContent = `🌡️ Temp: ${latest.temperature}°C`;
      document.getElementById("humid").textContent = `💧 Humidity: ${latest.humidity}%`;
      document.getElementById("light").textContent = `💡 Light Level: ${latest.light_level}`;
      document.getElementById("sound").textContent = `🔊 Sound: ${latest.sound_level}`;
      document.getElementById("air").textContent = `🌫️ Air Quality: ${latest.air_quality}`;
      document.getElementById("motion").textContent = `🏃‍♂️ Motion: ${latest.motion ? "Yes" : "No"}`;

      document.getElementById("fanStatus").textContent = `Fan: ${latest.fan ? "🟢 ON" : "🔴 OFF"}`;
      document.getElementById("lightStatus").textContent = `Light: ${latest.light ? "🟡 ON" : "⚫ OFF"}`;
    } else {
      alert("No data available from backend.");
    }
  } catch (error) {
    alert("Failed to fetch data from backend.");
    console.error(error);
  }
}

// Fetch immediately on load
window.onload = fetchData;
