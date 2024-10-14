const myCarouselElement = document.querySelector ('#myCarousel')

const carousel = new bootstrap.Carousel(myCarouselElement, {
  interval: 2000,
  touch: false
})

function toggleMenu() {
  document.querySelector('.menu').classList.toggle('active');
}