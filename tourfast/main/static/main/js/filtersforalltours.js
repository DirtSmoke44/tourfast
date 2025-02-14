document.querySelector('.apply-filters-btn').addEventListener('click', function() {
    const minPrice = parseFloat(document.getElementById('price-min').value);
    const maxPrice = parseFloat(document.getElementById('price-max').value);

    document.querySelectorAll('.tour-card').forEach(card => {
        const price = parseFloat(card.querySelector('.text-body strong').textContent.replace(' ₽', '').replace(/\s/g, ''));
        if (price >= minPrice && price <= maxPrice) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});