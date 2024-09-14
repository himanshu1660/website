document.addEventListener("DOMContentLoaded", function() {
    // Function to toggle popup display
    function togglePopup(popupDiv) {
      popupDiv.style.display = popupDiv.style.display === "none" ? "block" : "none";
      var overlay = document.querySelector(".overlay");
      overlay.style.display = popupDiv.style.display === "none" ? "none" : "block";
      if (popupDiv.style.display === "block") {
        document.body.style.overflow = "hidden"; // Prevent body scrolling when popup is open
      } else {
        document.body.style.overflow = "auto"; // Restore body scrolling when popup is closed
      }
    }
  
    var postphoto = document.querySelector(".create");
    var followersPopup = document.querySelector(".post-photo");
    postphoto.addEventListener("click", function(event) {
      event.stopPropagation();
      togglePopup(followersPopup);
    });
  
    var story = document.querySelector(".post-your-story");
    var followingPopup = document.querySelector(".post-story");
    story.addEventListener("click", function(event) {
      event.stopPropagation();
      togglePopup(followingPopup);
    });
  
    var del_posts = document.querySelectorAll(".del");
    var popup = document.querySelectorAll(".delete-post");
    del_posts.forEach(function(del_post, index) {
      del_post.addEventListener("click", function(event) {
        event.stopPropagation();
        togglePopup(popup[index]);
      });
    });
  
    // Hide popup and overlay when clicking outside of them
    window.addEventListener("click", function(event) {
      var overlayElement = document.querySelector(".overlay");
      if (event.target === overlayElement || !event.target.closest(".post-photo") && !event.target.closest(".post-story") && !event.target.closest(".delete-post")) {
        followersPopup.style.display = "none";
        followingPopup.style.display = "none";
        popup.forEach(function(popupDiv) {
          popupDiv.style.display = "none";
        });
        overlayElement.style.display = "none";
        document.body.style.overflow = "auto"; // Restore body scrolling when all popups are closed
      }
    });
  
    // Prevent the popup from hiding when clicking inside it
    followersPopup.addEventListener("click", function(event) {
      event.stopPropagation();
    });
    followingPopup.addEventListener("click", function(event) {
      event.stopPropagation();
    });
    popup.forEach(function(popupDiv) {
      popupDiv.addEventListener("click", function(event) {
        event.stopPropagation();
      });
    });
  });








var button = document.getElementById('right');
var back = document.getElementById('left');
var container = document.getElementById('box');

// Initially hide both buttons
back.style.display = container.scrollLeft > 0 ? 'block' : 'none';
button.style.display = container.scrollWidth > container.clientWidth ? 'block' : 'none';

button.onclick = function () {
    sideScroll(container, 'right', 25, 200, 10);
}

back.onclick = function () {
    sideScroll(container, 'left', 25, 200, 10);
}

function sideScroll(element, direction, speed, distance, step) {
    var scrollAmount = 0;
    var slideTimer = setInterval(function () {
        if (direction == 'left') {
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        
        // Show or hide the left button based on scroll position
        back.style.display = element.scrollLeft > 0 ? 'block' : 'none';
        
        // Show or hide the right button based on scroll position
        button.style.display = element.scrollLeft + element.offsetWidth >= element.scrollWidth ? 'none' : 'block';
        
        if (scrollAmount >= distance) {
            window.clearInterval(slideTimer);
        }
    }, speed);
}








