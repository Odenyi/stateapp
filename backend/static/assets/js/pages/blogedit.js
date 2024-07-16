// Function to get the CSRF token from the cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// edit blog code here
         // blog dropzone 
         let blogdropzoneedit= document.getElementById("blogupdate");
         if(blogdropzoneedit){
             let editblologurl = $("#blogupdate").data("url")
             // Check if a Dropzone instance is already attached to the element
         if (blogdropzoneedit.dropzone) {
             // If a Dropzone instance exists, destroy it
             blogdropzoneedit.dropzone.destroy();
         }
           // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
       var myblogdropzoneedit = new Dropzone("#blogupdate", {
         url: editblologurl, // Replace with your specific upload URL
         paramName: "blogeditimage", // The name of the form field that will contain the uploaded files
         maxFilesize: 30, // Max file size in MB (default: 256)
         acceptedFiles: 'image/*,video/*',
         maxFiles: 1,
 
         autoProcessQueue: false,
         addRemoveLinks: true, // Display remove links with preview images
         init: function() {
             // Your initialization logic here
             var dropzone = this;
 
             // Listen for the addedfile event
             dropzone.on("addedfile", function(file) {
               // Remove additional files if more than one is added
               if (dropzone.files.length > 1) {
                 dropzone.removeFile(dropzone.files[0]);
               }
             });
         }
     });
     let blogeditform = document.getElementById("updateblogfrm");
     blogeditform.addEventListener('submit', function (event) {
     
         event.preventDefault(); // Prevent the default form submission
      
         // Validate the form data
         if (!validateeditblogdata()) {
             return; // Stop form submission if validation fails
         }
 
         //get itemlist
         // Gather form data, including the uploaded files
             var blogeditformData = new FormData(blogeditform);
 
             // Add the uploaded files from Dropzone to the form data
             var dropzoneFiles2 = myblogdropzoneedit.getQueuedFiles();
             console.log(dropzoneFiles2)
 
             for (var i = 0; i < dropzoneFiles2.length; i++) {
                 
                 blogeditformData.append('blogeditimage', dropzoneFiles2[i]);
             }
             var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
             blogeditformData.append('csrfmiddlewaretoken', csrfToken);
             
             // Perform the AJAX or form submission using the modified form data
             // For example, you can use fetch or jQuery.ajax to submit the form
             fetch(editblologurl , {
                 method: 'POST',
                 
                 body: blogeditformData,
             }).then(function (response) {
                 
                 if(response.status == 200){
                     displaySuccessMessage("Blog has been Updated Sucessfully")
                 
                     // Reload the page after two seconds
                     setTimeout(function() {
                         window.location.reload();
                     }, 5000);
                     
                 }
                 return response.json(); //parse the JSON response
                 
             }).then(function(data){
                  if(data.error){
                     displayErrorMessage("Error in Updating Blog")
                 }
                 
 
             }).catch(function (error) {
                 // Handle errors, if any
             });
     
         })
 
         function validateeditblogdata(){
             let blogtitle = document.getElementById("blogtitle").value
             let blogtype = document.getElementById("blogtype").value
             let blogdescription = document.getElementById("blogdescription").value
             if(!blogtitle|| !blogtype|| !blogdescription){
                 displayErrorMessage("Please select all the required fields.")
                 return false;
             }
            
             return true;
         }
 
         }



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