function openModal(id) {
    const modal = document.getElementById("modal-" + id);
    if (modal) {
        modal.style.display = "block";
    }
}

function closeModal(id) {
    const modal = document.getElementById("modal-" + id);
    if (modal) {
        modal.style.display = "none";
    }
}
