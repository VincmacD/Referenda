var currentDate = new Date();
var voteButtons = document.querySelectorAll('#vote-button');
voteButtons.forEach(function(button) {
    var startDate = new Date(button.getAttribute('data-start-date'));
    var expiryDate = new Date(button.getAttribute('data-expiry-date'));
    
    if (currentDate >= startDate && currentDate <= expiryDate) {
        // Show the vote button
        button.style.display = "visible"; 
    } else {
        // Hide the vote button
        button.style.display = "none";
    }
});