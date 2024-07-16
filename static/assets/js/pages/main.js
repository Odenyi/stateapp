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


$(document).ready(function() {

   
    // Handle click event on remove button of other images on update
    $(".remove-image").on("click", function(e) {
        e.preventDefault()
        var imageId = $(this).data("image-id");
        var imageContainer = $(this).closest('.image-containermore');
        var deleteUrl = $(this).data("url");

        var csrfToken = getCookie("csrftoken");
        // Display Bootbox confirmation dialog
        bootbox.confirm("Are you sure you want to remove this image ?", function(result) {
            if (result) {
                // User confirmed, initiate AJAX call to delete the image
                $.ajax({
                    url: deleteUrl,
                    type: "DELETE",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    success: function (data) {
                        if (data.success) {
                            displaySuccessMessage("The image has been deleted")
                            imageContainer.css('background', 'tomato');
                            imageContainer.fadeOut(800, function () {
                            imageContainer.remove();
                                })
                        } else {
                            displayErrorMessage("Error while deleting Image")
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("AJAX error:", error);
                        displayErrorMessage("Error while deleting Image")
                    }
                });
                
            }
        });
    });


  

    //delete property
     // Handle click event on remove button
     $(".remove-property").on("click", function(e) {
        e.preventDefault()
        var propertyId = $(this).data("id");
        var property = $(this).data("name");
        var deletecontainer = $(this).closest('.view_property');
        var deleteUrl = $(this).data("url");
        console.log(deleteUrl)

        var csrfToken = getCookie("csrftoken");
        // Display Bootbox confirmation dialog
        bootbox.confirm(`Are you sure you want to remove this image for ${property} ?`, function(result) {
            if (result) {
                // User confirmed, initiate AJAX call to delete the image
                $.ajax({
                    url: deleteUrl,
                    type: "DELETE",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    success: function (data) {
                        if (data.success) {
                          if(propertyId == "deleteview2"){
                            displayErrorMessage("Property Successfully deleted")
                            // Reload the page after two seconds to route admin_property
                            let reloadurl = $(".remove-property").data("reloadurl")
                            setTimeout(function() {
                                window.location.href = reloadurl;
                            }, 3000);


                          }
                          else{
                            deletecontainer.css('background', 'tomato');
                            deletecontainer.fadeOut(800, function () {
                            deletecontainer.remove();
                            displayErrorMessage("Property Successfully deleted")
                            // Reload the page after two seconds
                            setTimeout(function() {
                                window.location.reload();
                            }, 3000);
                         })
                        }
                        } else {
                            displayErrorMessage("Property not deleted Try again Later")
                            console.error("Error deleting image.");
                        }
                    },
                    error: function (xhr, status, error) {
                        console.error("AJAX error:", error);
                        displayErrorMessage("Error while deleting property")
                    }
                });
                
            }
        });
    });

        // blog dropzone 
        let blogdropzone = document.getElementById("blogupload");
        if(blogdropzone){
            let addblogurl = $("#blogupload").data("url")
            // Check if a Dropzone instance is already attached to the element
        if (blogdropzone.dropzone) {
            // If a Dropzone instance exists, destroy it
            blogdropzone.dropzone.destroy();
        }
          // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
      var myblogdropzone = new Dropzone("#blogupload", {
        url: addblogurl, // Replace with your specific upload URL
        paramName: "mainblogimage", // The name of the form field that will contain the uploaded files
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
    blogaddform = document.getElementById("addblogfrm");
    blogaddform.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission
     
        // Validate the form data
        if (!validateblogdata()) {
            return; // Stop form submission if validation fails
        }

        //get itemlist
        // Gather form data, including the uploaded files
            var blogformData = new FormData(blogaddform);

            // Add the uploaded files from Dropzone to the form data
            var dropzoneFiles2 = myblogdropzone.getQueuedFiles();

            for (var i = 0; i < dropzoneFiles2.length; i++) {
                
                blogformData.append('blogimage', dropzoneFiles2[i]);
            }
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            blogformData.append('csrfmiddlewaretoken', csrfToken);
            
            // Perform the AJAX or form submission using the modified form data
            // For example, you can use fetch or jQuery.ajax to submit the form
            fetch(addblogurl , {
                method: 'POST',
                
                body: blogformData,
            }).then(function (response) {
                var successMessage = document.createElement('p');
                if(response.status == 200){
                    displaySuccessMessage("Blog has been added Sucessfully")
                
                    // Reload the page after two seconds
                    setTimeout(function() {
                        window.location.reload();
                    }, 5000);
                    
                }
                return response.json(); //parse the JSON response
                
            }).then(function(data){
                 if(data.error){
                    displayErrorMessage("Error in adding Blog")
                }
                

            }).catch(function (error) {
                // Handle errors, if any
            });
    
        })

        function validateblogdata(){
            let blogtitle = document.getElementById("blogtitle").value
            let blogtype = document.getElementById("blogtype").value
            let blogdescription = document.getElementById("blogdescription").value
            if(!blogtitle|| !blogtype|| !blogdescription){
                displayErrorMessage("Please select all the required fields.")
                return false;
            }
            var dropzoneFiles2 = myblogdropzone.getQueuedFiles();

                if(dropzoneFiles2.length==0){
                        // No files are queued, show an error message
                displayErrorMessage("Please upload at least one image.")
    
                return false;
                }
            return true;
        }

        }


         // blog dropzone 
         let videodropzone = document.getElementById("videoupload");
         if(videodropzone){
             let addvideourl = $("#videoupload").data("url")
             // Check if a Dropzone instance is already attached to the element
         if (videodropzone.dropzone) {
             // If a Dropzone instance exists, destroy it
             videodropzone.dropzone.destroy();
         }
           // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
       var myvideodropzone = new Dropzone("#videoupload", {
         url: addvideourl, // Replace with your specific upload URL
         paramName: "mainvideo", // The name of the form field that will contain the uploaded files
         maxFilesize: 200, // Max file size in MB (default: 256)
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
     vedioaddform = document.getElementById("addvediofrm");
     vedioaddform.addEventListener('submit', function (event) {
         event.preventDefault(); // Prevent the default form submission
      
         // Validate the form data
         if (!validatevediodata()) {
             return; // Stop form submission if validation fails
         }
 
         //get itemlist
         // Gather form data, including the uploaded files
             var vedioformData = new FormData(vedioaddform);
 
             // Add the uploaded files from Dropzone to the form data
             var dropzoneFiles2 = myvideodropzone.getQueuedFiles();
 
             for (var i = 0; i < dropzoneFiles2.length; i++) {
                 
                 vedioformData.append('mainvideo', dropzoneFiles2[i]);
             }
             var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
             vedioformData.append('csrfmiddlewaretoken', csrfToken);
             
             // Perform the AJAX or form submission using the modified form data
             // For example, you can use fetch or jQuery.ajax to submit the form
             fetch(addvideourl, {
                 method: 'POST',
                 
                 body: vedioformData,
             }).then(function (response) {
                 var successMessage = document.createElement('p');
                 if(response.status == 200){
                     displaySuccessMessage("Video has been added Sucessfully")
                 
                     // Reload the page after two seconds
                     setTimeout(function() {
                         window.location.reload();
                     }, 5000);
                     
                 }
                 return response.json(); //parse the JSON response
                 
             }).then(function(data){
                  if(data.error){
                     displayErrorMessage("Error in adding Video")
                 }
                 
 
             }).catch(function (error) {
                 // Handle errors, if any
             });
     
         })
 
         function validatevediodata(){
             let videotitle = document.getElementById("videotitle").value
             let videotype = document.getElementById("videotype").value
             
             if(!videotitle|| !videotype){
                 displayErrorMessage("Please select all the required fields.")
                 return false;
             }
             var dropzoneFiles2 = myvideodropzone.getQueuedFiles();
 
                 if(dropzoneFiles2.length==0){
                         // No files are queued, show an error message
                 displayErrorMessage("Please upload at least one video.")
     
                 return false;
                 }
            
                 for (let i = 0; i < dropzoneFiles2.length; i++) {
                    if (!isVideo(dropzoneFiles2[i])) {
                        displayErrorMessage("Please upload only video files.");
                        return false;
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
 

        
 


        // Get the element containing the Dropzone
        var dropzoneElement2 = document.getElementById("mainimageupdate");
        if (dropzoneElement2) {
            let editurl2 = $("#mainimageupdate").data("url")
          

        // Check if a Dropzone instance is already attached to the element
        if (dropzoneElement2.dropzone) {
            // If a Dropzone instance exists, destroy it
            dropzoneElement2.dropzone.destroy();
        }

      // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
      var myDropzone2 = new Dropzone("#mainimageupdate", {
        url: editurl2, // Replace with your specific upload URL
        paramName: "mainimage", // The name of the form field that will contain the uploaded files
        // maxFilesize: 3, // Max file size in MB (default: 256)
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

    //  form submission to save data 
}

//for other moreimage on update url
  // Get the element containing the Dropzone
  var dropzoneElement3 = document.getElementById("moreimagesupload");
  if (dropzoneElement3) {
    let editurl = $("#moreimagesupload").data("url")

  // Check if a Dropzone instance is already attached to the element
  if (dropzoneElement3.dropzone) {
      // If a Dropzone instance exists, destroy it
      dropzoneElement3.dropzone.destroy();
  }

// Initialize Dropzone programmatically on the div with ID "frmFileUpload"
var myDropzone3 = new Dropzone("#moreimagesupload", {
  url: editurl, // Replace with your specific upload URL
  paramName: "moreimages", // The name of the form field that will contain the uploaded files
//   maxFilesize: 3, // Max file size in MB (default: 256)
  autoProcessQueue: false,
  addRemoveLinks: true, // Display remove links with preview images
  acceptedFiles: 'image/*,video/*',
  init: function() {
      // Your initialization logic here
  }
});
}

//update property
var myForm2 = document.getElementById('property_update');
if(myForm2){ 
let mydropzone = myDropzone2;
let mydropzone1 = myDropzone3;

myForm2.addEventListener('submit', function (event) {
   event.preventDefault(); // Prevent the default form submission

   // Validate the form data
   if (!validateFormData()) {
       return; // Stop form submission if validation fails
   }

   // Gather form data, including the uploaded files
   var formData = new FormData(myForm2);

   // Add the uploaded files from Dropzone to the form data
   var dropzoneFiles = mydropzone.getQueuedFiles();

   for (var i = 0; i < dropzoneFiles.length; i++) {
       
       formData.append('mainimage', dropzoneFiles[i]);
   }
    
    // Add the uploaded files from Dropzone to the form data
   var dropzoneFiles1 = mydropzone1.getQueuedFiles();   
  
    for (var i = 0; i < dropzoneFiles1.length; i++) {
        
        formData.append('moreimages', dropzoneFiles1[i]);
    }
    // Function to validate the form data
   function validateFormData() {
        // returns true or false

       // Gather form fields for validation
       var title = document.getElementById('propertyname').value;
       var property_description = document.getElementById('propertydescription').value;
       
       var property_location = document.getElementById('propertylocation').value;
       var propertydescription = document.getElementById('propertydescription').value;
       var property_offertype = document.querySelector('input[name=radio1]:checked');
       var property_price = document.getElementById('propertyprice').value;
       var property_type = document.getElementById('propertytype').value;
       var property_bedrooms= document.getElementById('propertybedrooms').value;
       var property_bathrooms= document.getElementById('propertybathrooms').value;
       var checkboxes = document.querySelectorAll('[name="propertyamenities"]');
       var propertysize =document.getElementById('propertysize').value;
       
      
       var checked = Array.from(checkboxes).some(function(checkbox) {
           return checkbox.checked;
       });

       if (!checked) {
           displayErrorMessage("Please select at least one amenity.")
           return false;
       }
    
       
       
       // Perform your validation checks here
       // For example, check if any required fields are empty
       if (!title || !property_description || !property_location || !property_offertype || !property_price || !property_type || !property_bathrooms || !property_bedrooms || !propertysize) {
           // Create an error message element
           displayErrorMessage("Please fill in all the required fields.")

           return false; // Validation failed
       }

       // Validation successful
       return true;
                 
   }
   var propertyidurl = document.getElementById('propertyid').value;
   // Manually add the CSRF token to the form data
   var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
   formData.append('csrfmiddlewaretoken', csrfToken);
  
   // Perform the AJAX or form submission using the modified form data
   // For example, you can use fetch or jQuery.ajax to submit the form
   fetch(propertyidurl , {
       method: 'POST',
     
       body: formData,
   }).then(function (response) {
    var successMessage = document.createElement('p');
    if(response.status == 200){
        displaySuccessMessage("Property has been Updated Sucessfully")
    
        // Reload the page after two seconds
        setTimeout(function() {
            window.location.reload();
        }, 5000);
        
    }
    return response.json(); //parse the JSON response
       
   }).then(function(data){
       // Handle the response from the server
       var successMessage = document.createElement('p');
   
       if(response.succes){
        displaySuccessMessage("Property has been Updated Sucessfully")
           // Reload the page after two seconds
            setTimeout(function() {
                window.location.reload();
            }, 5000);
       }else if(data.error){
        displayErrorMessage("Error in Updating Property")
       }
      

   }).catch(function (error) {
       // Handle errors, if any
   });
});
}



//adding property dropzone
 // Initialize Dropzone programmatically on the div with ID "frmFileUpload"
 var dropzoneElement = document.getElementById("frmFileUpload");

 if(dropzoneElement){
    if (dropzoneElement.dropzone) {
        // If a Dropzone instance exists, destroy it
        dropzoneElement.dropzone.destroy();
    }
 var myDropzone = new Dropzone("#frmFileUpload", {
    url: $("#frmFileUpload").data("url"), // Replace with your specific upload URL
    paramName: "propertyimages", // The name of the form field that will contain the uploaded files
    maxFilesize: 30, // Max file size in MB (default: 256)
    autoProcessQueue:false,
    addRemoveLinks: true, // Display remove links with preview images
    init:function(){
         var myForm = document.getElementById('property_addform');
         let addurl = $("#frmFileUpload").data("url")
         let mydropzone = this;
         
        myForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent the default form submission

            // Validate the form data
            if (!validateFormData()) {
                return; // Stop form submission if validation fails
            }

            // Gather form data, including the uploaded files
            var formData = new FormData(myForm);

            // Add the uploaded files from Dropzone to the form data
            var dropzoneFiles = mydropzone.getQueuedFiles();
            
            for (var i = 0; i < dropzoneFiles.length; i++) {
                
                formData.append('propertyimages', dropzoneFiles[i]);
            }
             // Function to validate the form data
            function validateFormData() {
                // Gather form fields for validation
                var title = document.getElementById('propertyname').value;
                var property_description = document.getElementById('propertydescription').value;
                
                var property_location = document.getElementById('propertylocation').value;
                var propertydescription = document.getElementById('propertydescription').value;
                var property_offertype = document.querySelector('input[name=radio1]:checked');
                var property_price = document.getElementById('propertyprice').value;
                var property_type = document.getElementById('propertytype').value;
                var property_bedrooms= document.getElementById('propertybedrooms').value;
                var property_bathrooms= document.getElementById('propertybathrooms').value;
                var checkboxes = document.querySelectorAll('[name="propertyamenities"]');
                var propertysize =document.getElementById('propertysize').value;
               
                var checked = Array.from(checkboxes).some(function(checkbox) {
                    return checkbox.checked;
                });

                if (!checked) {
                    displayErrorMessage("Please select at least one amenity.")
                    return false;
                }
             
                // Get queued files from Dropzone
                var dropzoneFiles = myDropzone.getQueuedFiles();

                if(dropzoneFiles.length==0){
                        // No files are queued, show an error message
                displayErrorMessage("Please upload at least one image.")
    
                return false;
                }
                
                // Perform your validation checks here
                // For example, check if any required fields are empty
                if (!title || !property_description || !property_location || !property_offertype || !property_price || !property_type || !property_bathrooms || !property_bedrooms || !propertysize) {
                    // Create an error message element

                    
                    displayErrorMessage("Please fill in all the required fields.")
                    return false; // Validation failed
                }

                // Validation successful
                return true;
                          
            }
            // Manually add the CSRF token to the form data
            var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
            formData.append('csrfmiddlewaretoken', csrfToken);

            // Perform the AJAX or form submission using the modified form data
            // For example, you can use fetch or jQuery.ajax to submit the form
            fetch(addurl, {
                method: 'POST',
              
                body: formData,
            }).then(function (response) {
                var successMessage = document.createElement('p');
                if(response.status == 200){

                    displaySuccessMessage('Property has been uploaded Sucessfully')
                   
                    // Reload the page after two seconds
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                }
                return response.json(); //parse the JSON response
            }).then(function(data){
               
            
                if(response.succes){

                    displaySuccessMessage('Data has been uploaded Sucessfully')

                    // Reload the page after two seconds
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                }else if(data.error){
                    displayErrorMessage("Error while Uploading Property Try again Later")
                }
                

            }).catch(function (error) {
                // Handle errors, if any
                // displayErrorMessage("Error while Uploading Property")
            });
        });

    }
});

 }

//  edi user 
usereditform = document.getElementById("edituserfrm");
usereditform.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    edituserurl = $(this).data("usrurl");
    // Validate the form data
    if (!validateuserdata()) {
        return; // Stop form submission if validation fails
    }

    //get itemlist
    // Gather form data, including the uploaded files
        var usereditData = new FormData(usereditform);

      
        var csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        usereditData.append('csrfmiddlewaretoken', csrfToken);
        
        // Perform the AJAX or form submission using the modified form data
        // For example, you can use fetch or jQuery.ajax to submit the form
        fetch(edituserurl , {
            method: 'POST',
            
            body: usereditData,
        }).then(function (response) {
            var successMessage = document.createElement('p');
            if(response.status == 200){
                displaySuccessMessage("User info has been added Sucessfully")
            
                // Reload the page after two seconds
                setTimeout(function() {
                    window.location.reload();
                }, 5000);
                
            }
            return response.json(); //parse the JSON response
            
        }).then(function(data){
             if(data.error){
                displayErrorMessage("Error in adding Blog")
            }
            

        }).catch(function (error) {
            // Handle errors, if any
        });

    })

    function validateuserdata(){
        let username = document.getElementById("username").value
        let useremail = document.getElementById("useremail").value
        let user_type = document.getElementById("user_type").value
        if(!username|| !useremail || !user_type){
            displayErrorMessage("Please Enter all the required fields.")
            return false;
        }
       
        return true;
    }

// delete user from the system

// Your JavaScript file (e.g., custom.js)

$('.deleteUsr').on("click", function(e) {
    e.preventDefault();

    // Store a reference to the clicked "Delete" button
    var deleteButton = $(this);
    console.log("deleting data")

    // Get the URL for deleting the user
    var deleteUrl = deleteButton.data("delusr");

    var csrfToken = getCookie("csrftoken");
    
    // Display Bootbox confirmation dialog
    bootbox.confirm("Are you sure you want to delete this user?", function(result) {
        if (result) {
            // User confirmed, initiate AJAX call to delete the user
            $.ajax({
                url: deleteUrl,
                type: "DELETE",
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

//delete video
$('.deletevideo').on("click", function(e) {
    e.preventDefault();

    // Store a reference to the clicked "Delete" button
    var deleteButton = $(this);
    

    // Get the URL for deleting the user
    var deleteUrl = deleteButton.data("delvideo");

    var csrfToken = getCookie("csrftoken");
    
    // Display Bootbox confirmation dialog
    bootbox.confirm("Are you sure you want to delete this Video?", function(result) {
        if (result) {
            // User confirmed, initiate AJAX call to delete the user
            $.ajax({
                url: deleteUrl,
                type: "DELETE",
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
});
