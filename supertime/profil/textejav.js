function pingAddress(address, port) {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();
    const socket = new WebSocket(`ws://${address}:${port}`);

    socket.on('open', () => {
      const pingTime = Date.now() - startTime;
      socket.close();
      resolve(pingTime);
    });

    socket.on('error', () => {
      reject(new Error('Erreur de connexion'));
    });

    setTimeout(() => {
      reject(new Error('Délai de connexion dépassé'));
    }, 5000); // Délai de connexion de 5 secondes
  });
}

function updateStatusButton(address, port) {
  const statusButton = document.getElementById('status-button');

  pingAddress(address, port)
    .then(pingTime => {
      statusButton.style.backgroundColor = 'green';
      statusButton.textContent = 'En ligne';
      console.log(`Délai de ping : ${pingTime}ms`);
    })
    .catch(error => {
      statusButton.style.backgroundColor = 'red';
      statusButton.textContent = 'Hors ligne';
      console.error(`Erreur : ${error.message}`);
    });
}

// Créer le bouton d'état
const statusButton = document.createElement('button');
statusButton.id = 'status-button';
statusButton.style.padding = '10px 20px';
statusButton.style.fontSize = '16px';
statusButton.style.border = 'none';
statusButton.style.borderRadius = '5px';
statusButton.style.cursor = 'pointer';

// Ajouter le bouton d'état à la page
document.body.appendChild(statusButton);

// Mettre à jour l'état du bouton toutes les 10 secondes
setInterval(() => {
  updateStatusButton('example.com', 80);
}, 10000);