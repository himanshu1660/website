document.addEventListener("DOMContentLoaded", function() {
    // Function to toggle popup display
    function togglePopup(popupDiv) {
        popupDiv.style.display = popupDiv.style.display === "none" ? "block" : "none";
    }

    // Followers popup
    var followersText = document.querySelector(".followers_number");
    var followersPopup = document.querySelector(".followers");
    followersText.addEventListener("click", function(event) {
        event.stopPropagation();
        togglePopup(followersPopup);
    });

    // Following popup
    var followingsText = document.querySelector(".followings_number");
    var followingPopup = document.querySelector(".following");
    followingsText.addEventListener("click", function(event) {
        event.stopPropagation();
        togglePopup(followingPopup);
    });

    // Hide popup when clicking outside of it
    window.addEventListener("click", function() {
        followersPopup.style.display = "none";
        followingPopup.style.display = "none";
    });

    // Prevent the popup from hiding when clicking inside it
    followersPopup.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    followingPopup.addEventListener("click", function(event) {
        event.stopPropagation();
    });
});
