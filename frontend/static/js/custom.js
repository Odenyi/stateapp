$(document).ready(function() {

    // work on show interest model to sents sms
        $(".contact_form").on("submit",function(e) {
            e.preventDefault()
           
            let duburl = $(this).data("type")
            let url = $(this).data("url")
            let name = $("#customername").val()
            let email = $("#customeremail").val()
            let number = $("#customernumber").val()
            let message = $("#customermessage").val()
            let formData = new FormData();
           
             // Check if email and name have values
            if(duburl != "blogcontact"){
             
            if (!email || !name || !number) {
                displayErrorMessage("Please provide name,phone and email.");
                return; // Exit the function without submitting
            }
    
            // Check if number has between 10 to 13 characters and starts with 0, +254, or 254
            if (!(number.length >= 10 && number.length <= 13) ||
                !(number.startsWith("0") || number.startsWith("+254") || number.startsWith("254"))) {
                    displayErrorMessage("Please provide a valid phone number starting with 0, +254, or 254, and having 10 to 13 characters.");
                return; // Exit the function without submitting
            }
              // Create a FormData object and append the collected data
              
              formData.append("name", name);
              formData.append("email", email);
              formData.append("number", number);
              formData.append("message", message);
              formData.append("url", duburl);
             
               // Send the FormData using an AJAX request
            }
            else{
                let blogid = $(this).data("blogid")
                if (!name) {
                    console.log("passed here")
                    displayErrorMessage("Please provide  name.");
                    return; // Exit the function without submitting
                }
                
                if(email){
                    // Regular expression for a basic email pattern
                    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
                    
                    // Use the test() method to check if the email matches the pattern
                    isvalid = emailPattern.test(email);
                    if(!isvalid){
                        displayErrorMessage("Please provide use the correct email format.");
                        return
                    }
                }
                if(!message){
                    displayErrorMessage("Please write a comment.");
                    return; // Exit the function without submitting
                }
                formData.append("name", name);
                formData.append("email", email);
                formData.append("blogid",blogid)
              
                formData.append("message", message);
                formData.append("url", duburl);

            }

            // Add the CSRF token to the headers
            let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    
              
        $.ajax({
            url: url,
           
            method:"POST",
            data: formData,
            headers: { "X-CSRFToken": csrfToken },
            processData: false,
            contentType: false,
            success: function(response) {
                if(duburl == "blogcontact"){
                    displaySuccessMessage("Comment added succesfully")
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                }
                else{
                displaySuccessMessage("Your request has been submitted succesfully one of our representatives will contact you")
                }
            },
            error: function(xhr, textStatus, errorThrown) {
                // Display error message
                displayErrorMessage("Please try again later System is under maintenace call +254792126894 ")
            }
        });
    
        })

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
       
        
        
       
     
        
        
        
    })