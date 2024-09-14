// ---------------------START LIKE COUNT-----------------------
document.addEventListener('DOMContentLoaded', function() {
    var likeButtons = document.querySelectorAll('#likeButton');
    likeButtons.forEach(function(likeButton) {
        likeButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            // Get the like count element for this post
            var postElement = likeButton.closest('.post');
            var likeCountElement = postElement.querySelector('.likes p');

            // Make an AJAX request to the Django view
            var xhr = new XMLHttpRequest();
            xhr.open('GET', this.href, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    var response = xhr.responseText;
                    if (response === 'liked') {
                        // Replace the SVG with the filled heart icon
                        var svgElement = this.querySelector('svg');
                        svgElement.classList.add('liked');

                        // Update the like count
                        var currentLikeCount = parseInt(likeCountElement.textContent.split(' ')[0]);
                        likeCountElement.textContent = (currentLikeCount + 1) + ' Likes';
                    } else {
                        // Replace the SVG with the outlined heart icon
                        var svgElement = this.querySelector('svg');
                        svgElement.classList.remove('liked');

                        // Update the like count
                        var currentLikeCount = parseInt(likeCountElement.textContent.split(' ')[0]);
                        likeCountElement.textContent = (currentLikeCount - 1) + ' Likes';
                    }
                }
            }.bind(this);
            xhr.send();
        });
    });
});
// -----------------------------END LIKE COUNT---------------------

// ------------------------------START BOOKMARKS------------------------
document.addEventListener('DOMContentLoaded', function() {
    var bookmarkButtons = document.querySelectorAll('#bookmarkButton');
    bookmarkButtons.forEach(function(bookmarkButton) {
        bookmarkButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent the default link behavior

            // Make an AJAX request to the Django view
            var xhr = new XMLHttpRequest();
            xhr.open('GET', this.href, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                    var response = xhr.responseText;
                    if (response === 'bookmarked') {
                        // Replace the SVG with the filled bookmark icon
                        var svgElement = this.querySelector('svg');
                        svgElement.classList.add('bookmarked');

                    } else {
                        // Replace the SVG with the outlined bookmark icon
                        var svgElement = this.querySelector('svg');
                        svgElement.classList.remove('bookmarked');
                    }
                }
            }.bind(this);
            xhr.send();
        });
    });
});
// ------------------------------END BOOKMAKRS-----------------------
