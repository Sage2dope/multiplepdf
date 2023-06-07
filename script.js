const words = ['Word 1', 'Word 2', 'Word 3'];
let currentIndex = 0;

function animateWordSwipe() {
  const wordElement = document.querySelector('.word');
  const currentWord = words[currentIndex];

  wordElement.textContent = currentWord;
  wordElement.classList.add('swipe-animation');

  currentIndex = (currentIndex + 1) % words.length;

  setTimeout(() => {
    wordElement.classList.remove('swipe-animation');
    setTimeout(animateWordSwipe, 1000); // Change the delay between swipes if desired
  }, 5000); // Change the duration of each word if desired
}

animateWordSwipe();
