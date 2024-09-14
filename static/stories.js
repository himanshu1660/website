var storyRight = document.getElementById('story-right');
var storyLeft = document.getElementById('story-left');
var container = document.getElementById('story-box');

storyRight.onclick = function () {
    sideScroll(container, 'right', 5, 500, 500);
};

storyLeft.onclick = function () {
    sideScroll(container, 'left', 5, 500, 500);
};

function sideScroll(element, direction, speed, distance, step) {
    var scrollAmount = 0;
    var slideTimer = setInterval(function () {
        if (direction === 'left') {
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        
        if (scrollAmount >= distance) {
            clearInterval(slideTimer); // Clear the interval when the distance is reached
        }
    }, speed);
}