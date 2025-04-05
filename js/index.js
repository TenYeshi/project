document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll("#imageCarousel .carousel-item");
    const indicators = document.querySelectorAll("#imageCarousel .carousel-indicators button");
    const total = items.length;
    const randomIndex = Math.floor(Math.random() * total);

    items[randomIndex].classList.add("active");
    indicators[randomIndex].classList.add("active");
  });