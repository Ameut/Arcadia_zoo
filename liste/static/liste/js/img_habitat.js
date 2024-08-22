console.log("img_habitat.js is loaded");

function openImage(imgElement, habitatName) {
    console.log("openImage called with:", imgElement, habitatName);
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    var title = document.getElementById("habitatTitle");

    if (modal && modalImg && title) {
        modal.style.display = "flex";
        modalImg.src = imgElement.src;
        title.textContent = habitatName;
    } else {
        console.log("Modal elements are not found");
    }
}

function closeImage() {
    var modal = document.getElementById("imageModal");
    if (modal) {
        modal.style.display = "none";
    }
}

document.querySelectorAll('.image-container').forEach(function(container) {
    container.addEventListener('mouseover', function() {
        var img = container.querySelector('.clickable-image');
        var title = container.querySelector('.habitat-title');

        img.style.transform = 'scale(1.1)';
        title.style.opacity = '1';
    });

    container.addEventListener('mouseout', function() {
        var img = container.querySelector('.clickable-image');
        var title = container.querySelector('.habitat-title');

        img.style.transform = 'scale(1)';
        title.style.opacity = '0';
    });
});
