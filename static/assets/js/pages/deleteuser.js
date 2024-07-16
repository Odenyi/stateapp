// Capture the form submission event
// delete user from the system

// Your JavaScript file (e.g., custom.js)

$('.deleteUsr').on("click", function(e) {
e.preventDefault();

// Store a reference to the clicked "Delete" button
var deleteButton = $(this);


// Get the URL for deleting the user
var deleteUrl = deleteButton.data("delusr");
// Get the ID of the user being deleted
var userId = $(this).data("userid");
logeduser = $(this).data("loguser");

// Check if the user being deleted is the currently logged-in user
if (userId === logeduser) {
    // Display a message indicating that the user cannot delete their own account
    displayErrorMessage("You cannot delete your own account.");
    return;
}

var csrfToken = getCookie("csrftoken");

// Display Bootbox confirmation dialog
bootbox.confirm("Are you sure you want to delete this user?", function(result) {
if (result) {
    // User confirmed, initiate AJAX call to delete the user
    $.ajax({
        url: deleteUrl,
        type: "POST",
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function (data) {
            if (data.success) {
                // Remove the deleted user row from the table
                deleteButton.closest('tr').remove();
                
                displaySuccessMessage("User has been deleted.");
            } else {
                displayErrorMessage("Error while deleting user.");
            }
        },
        error: function (xhr, status, error) {
            console.error("AJAX error:", error);
            displayErrorMessage("Error while deleting user.");
        }
    });
}
});
});


// display success and error functions
function displayErrorMessage(message) {
let errorMessage = $('<div>').addClass('popup error').text(message);
$('body').append(errorMessage);
setTimeout(function() {
errorMessage.fadeOut(500, function() {
    errorMessage.remove();
});
}, 10000); // Display error message for 10 seconds
}

function displaySuccessMessage(message) {
let successMessage = $('<div>').addClass('popup success').text(message);
$('body').append(successMessage);
setTimeout(function() {
successMessage.fadeOut(500, function() {
    successMessage.remove();
});
}, 10000); // Display success message for 10 seconds
}
