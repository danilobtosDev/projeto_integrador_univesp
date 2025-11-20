// app/static/js/location.js

function getAndSendLocation() {
  if (navigator.geolocation) {
    console.log('Tentando obter a localização...')
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lon = position.coords.longitude
        console.log(`Localização obtida: Lat=${lat}, Lon=${lon}`)

        // Enviar as coordenadas para o backend para processamento/armazenamento
        sendLocationToServer(lat, lon)
      },
      (error) => {
        console.error('Erro ao obter a localização:', error.message)
        // Se falhar (usuário negou), carregue a localização padrão/manual
        loadManualLocationForm()
      }
    )
  } else {
    alert('Geolocalização não é suportada pelo seu navegador.')
    loadManualLocationForm()
  }
}

function sendLocationToServer(lat, lon, regionName = null) {
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
        console.log('Localização atualizada no servidor:', data.message)
        // Atualizar a interface para refletir a nova localização
        document.getElementById('current-location-display').textContent =
          data.current_region
      }
    })
    .catch((error) => {
      console.error('Erro ao enviar localização:', error)
    })
}

function loadManualLocationForm() {
  // Exibe o formulário manual se a detecção automática falhar
  const manualForm = document.getElementById('manual-location-form')
  if (manualForm) {
    manualForm.style.display = 'block'
  }
}

// Inicia a detecção automática ao carregar a página
getAndSendLocation()
