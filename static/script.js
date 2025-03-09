
document.addEventListener("DOMContentLoaded", () => {
    const map = L.map('map').setView([49.8175, 15.4729], 7);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

    // Přenos souřadnic do formuláře při kliknutí na mapu
    map.on('click', (event) => {
        document.getElementById('lat').value = event.latlng.lat;
        document.getElementById('lng').value = event.latlng.lng;
    });

    fetch('/get_places')
        .then(response => response.json())
        .then(data => {
            data.forEach(place => {
                const marker = L.marker([place.lat, place.lng], {
                    icon: L.icon({
                        iconUrl: '/static/heart.png',
                        iconSize: [30, 30],
                        iconAnchor: [15, 30],
                        popupAnchor: [0, -30]
                    })
                }).addTo(map).bindTooltip(`${place.name}`).openTooltip();

                marker.on('click', () => {
                    marker.bindPopup(`
                        <b>${place.name}</b><br>${place.timestamp}
                        <form action="/delete_place/${place.id}" method="post">
                            <button class="popup-button">❌ Smazat</button>
                        </form>
                        <form action="/update_place/${place.id}" method="post">
                            <input type="text" name="name" value="${place.name}" required />
                            <input type="datetime-local" name="date" required />
                            <button class="popup-button">✏️ Upravit</button>
                        </form>
                    `).openPopup();
                });
            });
        });
});
