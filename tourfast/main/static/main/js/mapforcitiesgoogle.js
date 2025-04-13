function initMap(cityName) {
    // Убедитесь, что в вашем back-end передаются координаты города.
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({'address': cityName}, function(results, status) {
        if (status === 'OK') {
            const map = new google.maps.Map(document.getElementById('map'), {
                zoom: 10,
                center: results[0].geometry.location
            });
            const marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        } else {
            document.getElementById('cityInfo').textContent = "Не удалось найти город.";
        }
    });
}

function openDetailsModal(cityName) {
    // Ожидаем, что город будет передан сюда
    document.getElementById('cityInfo').textContent = `Город проведения тура: ${cityName}`;
    document.getElementById('detailsModal').style.display = 'block';

    // Инициализируем карту с городом
    initMap(cityName);
}

function closeDetailsModal() {
    document.getElementById('detailsModal').style.display = 'none';
}

// Закрытие модалки "Подробно" при клике вне
window.addEventListener('click', function(event) {
    const detailsModal = document.getElementById('detailsModal');
    if (event.target == detailsModal) {
        closeDetailsModal();
    }
});
