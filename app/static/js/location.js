// app/static/js/js/location.js

function getAndSendLocation() {
  if (navigator.geolocation) {
    console.log('Tentando obter a localização automática...')
    // getCurrentPosition: tenta obter a localização do dispositivo
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lon = position.coords.longitude
        console.log(`Localização obtida: Lat=${lat}, Lon=${lon}`)

        // Envia as coordenadas para o backend (views.py)
        sendLocationToServer(lat, lon)
      },
      (error) => {
        console.error(
          'Erro ao obter a localização (Usuário negou ou erro do sensor):',
          error.message
        )
        loadManualLocationForm()
      }
    )
  } else {
    console.warn('Geolocalização não é suportada pelo navegador.')
    loadManualLocationForm()
  }
}

function sendLocationToServer(lat, lon, regionName = null) {
  // Função unificada para enviar dados automáticos ou manuais para o Flask
  const data = {
    latitude: lat,
    longitude: lon,
    region: regionName,
  }

  fetch('/set_location', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === 'success') {
        // Atualiza a interface com a nova localização
        const display = document.getElementById('current-location-display')
        if (display) {
          display.textContent = data.current_region
        }
        // Oculta o formulário manual após o sucesso
        const manualForm = document.getElementById('manual-location-form')
        if (manualForm) {
          manualForm.style.display = 'none'
        }
      }
    })
    .catch((error) => {
      console.error('Erro ao enviar localização para o servidor:', error)
    })
}

function loadManualLocationForm() {
  // Exibe o formulário manual se a detecção automática falhar ou o usuário clicar em "Alterar"
  const manualForm = document.getElementById('manual-location-form')
  if (manualForm) {
    manualForm.style.display = 'block'
  }
}

// Inicia a detecção automática ao carregar o script
getAndSendLocation()

// Lógica para enviar localização manual quando o formulário é submetido
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('manual-location-input')
  if (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      const regionName = document.getElementById('region_name').value
      // Envia apenas o nome da região (lat/lon como null)
      sendLocationToServer(null, null, regionName)
    })
  }
})
