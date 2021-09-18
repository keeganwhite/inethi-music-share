/**
 * Validates a users bank account details on the Registration page using an API call. Uses jQuery and must be linked to
 * the registration page of the wordpress website.
 * @param accountType the type of account the user has
 * @param branchCode the universal branch code used by the bank the user banks with
 * @param accountNumber the users bank account number
 * @param callback the function that will be run on the object sent back from freecdv.co.za
 */
function validate(accountType, branchCode, accountNumber, callback) {
  $.get('https://cors-anywhere.herokuapp.com/https://freecdv.co.za/check/'+accountType+'/'+branchCode+'/'+accountNumber, callback);
}

/**
 * Function that calls the validate function when the user clicks the submit button on the registration page and alerts the user
 * to the response
 */
$(function() {
  $("#um-submit-btn").on("click",function() {
    validate($("#acc_type-76").val(),
      $("#branch_code-76").val(),
      $("#account_number-76").val(),
      function(r) {
          const accType = $("#acc_type-76").val();
          const branchCode = $("#branch_code-76").val();
          const accNum = $("#account_number-76").val();
          console.log("API call to freecdv.co.za invoked with: " + accType + ", " + branchCode + ", " + accNum); // to see documentation on this API call see https://freecdv.co.za/swagger/index.html
          console.log("Response:" + JSON.stringify(r, null, "\t"))
          const status = JSON.parse(JSON.stringify(r, null, "\t")).status;
          switch (status) {
              case "Valid":
                  window.alert("Your bank details are valid.")
                  break;
              case "InvalidAccountLength":
                  window.alert("Your account number is an invalid length. Please check your bank details on your account page. See FAQ for more help.")
                  break;
              case "BranchNotComputerised":
                  window.alert("Your branch code does not allow online services. Please try a universal branch code. There are examples at the top of the page. Please check your bank details on your account page. See FAQ for more help.");
                  break;
              case "BranchCodeNotInvalid":
                  window.alert("Your branch code is invalid. Please check your bank details on your account page. See FAQ for more help.")
                  break;
              case "AccountTypeNotValid":
                  window.alert("Your account type was invalid. Please check your bank details on your account page. See FAQ for more help.")
                  break;
              case "AccountNumberNotValid":
                  window.alert("Your account number was invalid. Please check your bank details on your account page. See FAQ for more help.")
                  break;
              default:
                  window.alert("Your bank details were not checked by our system due to an error.")
          }
      });
  })
});
