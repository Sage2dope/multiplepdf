// Array of words
var words = ["Text 1", "Text 2", "Text 3"];

// Function to update text
function updateText() {
  var wordIndex = 0;
  var wordsCount = words.length;
  
  return function() {
    $('.word').text(words[wordIndex]);
    wordIndex = (wordIndex + 1) % wordsCount;
  }
}

// Update text on each animation iteration
$('.word-swipe').on('animationiteration', updateText());
