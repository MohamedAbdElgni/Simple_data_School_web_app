// // Wait for the DOM to be fully loaded
// document.addEventListener("DOMContentLoaded", function () {
//   // Get the alert div element by its ID
//   const alertDiv = document.getElementById("alertMessage");

//   // Show the message with the fadeIn animation
//   alertDiv.style.display = "block";
//   alertDiv.style.animation = "fadeIn 1s ease-in-out";

//   // Set a timeout function to trigger the fade-out animation after 4 seconds
//   setTimeout(function () {
//     alertDiv.style.animation = "fadeOut 1s ease-in-out";
//     // Remove the message from the DOM after the fade-out animation finishes
//     setTimeout(function () {
//       alertDiv.remove();
//     }, 1000); // 1000 milliseconds = 1 second (duration of the fadeOut animation)
//   }, 4000); // 4000 milliseconds = 4 seconds
// });
function passfunc() {
    var x = document.getElementById("password");
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
  }


