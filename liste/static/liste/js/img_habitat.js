function openImage(imgElement, habitatName) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    var title = document.getElementById("habitatTitle");

    modal.style.display = "flex";
    modalImg.src = imgElement.src;
    title.textContent = habitatName;
}

function closeImage() {
    var modal = document.getElementById("imageModal");
    modal.style.display = "none";
}
