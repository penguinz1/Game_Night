// Function to make blinking text
(function() {
    var blinks = document.getElementsByTagName('blink');
    var visibility = 'hidden';
    window.setInterval(function() {
    for (var i = blinks.length - 1; i >= 0; i--) {
        blinks[i].style.visibility = visibility;
    }
    visibility = (visibility === 'visible') ? 'hidden' : 'visible';
}, 750);
})();