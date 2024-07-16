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

// edit video code here
         // video dropzone 
         let videodropzoneedit= document.getElementById("videoupdate");
         if(videodropzoneedit){
             let editvideourl = $("#videoupdate").data("url")
             // Check if a Dropzone instance is already attached to the element
         if (videodropzoneedit.dropzone) {
             // If a Dropzone instance exists, destroy it
             videodropzoneedit.dropzone.destroy();
         }
           // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
       var myvideodropzoneedit = new Dropzone("#videoupdate", {
         url: editvideourl, // Replace with your specific upload URL
         paramName: "videoeditimage", // The name of the form field that will contain the uploaded files
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
     let videoeditform = document.getElementById("updatevideofrm");
     videoeditform.addEventListener('submit', function (event) {
     
         event.preventDefault(); // Prevent the default form submission
      
         // Validate the form data
         if (!validateeditvideodata()) {
             return; // Stop form submission if validation fails
         }
 
         //get itemlist
         // Gather form data, including the uploaded files
             var videoeditformData = new FormData(videoeditform);
 
             // Add the uploaded files from Dropzone to the form data
             var dropzoneFiles2 = myvideodropzoneedit.getQueuedFiles();
             
 
             for (var i = 0; i < dropzoneFiles2.length; i++) {
                 
                 videoeditformData.append('videoedit', dropzoneFiles2[i]);
             }
             var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
             videoeditformData.append('csrfmiddlewaretoken', csrfToken);
             
             // Perform the AJAX or form submission using the modified form data
             // For example, you can use fetch or jQuery.ajax to submit the form
             fetch(editvideourl , {
                 method: 'POST',
                 
                 body: videoeditformData,
             }).then(function (response) {
                 
                 if(response.status == 200){
                     displaySuccessMessage("video has been Updated Sucessfully")
                 
                     // Reload the page after two seconds
                     setTimeout(function() {
                         window.location.reload();
                     }, 5000);
                     
                 }
                 return response.json(); //parse the JSON response
                 
             }).then(function(data){
                  if(data.error){
                     displayErrorMessage("Error in Updating video")
                 }
                 
 
             }).catch(function (error) {
                 // Handle errors, if any
             });
     
         })
 
         function validateeditvideodata(){
             let videotitle = document.getElementById("videotitle").value
             let videotype = document.getElementById("videotype").value
             
             if(!videotitle|| !videotype){
                 displayErrorMessage("Please select all the required fields.")
                 return false;
             }
             var dropzoneFiles2 = myvideodropzoneedit.getQueuedFiles();
             if (dropzoneFiles2.length !=0){
             for (let i = 0; i < dropzoneFiles2.length; i++) {
                if (!isVideo(dropzoneFiles2[i])) {
                    displayErrorMessage("Please upload only video files.");
                    return false;
                }
            }
            }
            
             return true;
         }
         function isVideo(file) {
            // Define an array of allowed video MIME types
            const allowedVideoTypes = ["video/mp4", "video/mpeg", /* Add more video types here */];
        
            // Check if the file type is in the allowed video types array
            return allowedVideoTypes.includes(file.type);
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