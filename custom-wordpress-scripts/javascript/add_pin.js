/**
 * When the user submits their create permission pin form this code runs to send the data to the API with a post request
 * returns the result of the process
 */

document.addEventListener( 'wpcf7submit', function( event ) {
    console.log("button pressed")
    const dataType = 'json';
    let couponGenerator = "http://0.0.0.0:5000/api/newuser"
    var inputs = event.detail.inputs;
    const username = inputs[0].value;
    const pin = inputs[1].value;
    console.log(username)
    console.log(pin)
    const data = {
        "username": username,
        "password": pin,
    }
    console.log("About to send")
    $.ajax({
        type: "POST",
        url: couponGenerator,
        // The key needs to match your method's input parameter (case-sensitive).
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data, status) {
            const json_obj = data.message;
            const message = JSON.stringify(json_obj);
            alert("Your coupon code is: "+ message);
        },
        error: function (errMsg) {
            alert("You have already created a pin or you left the pin field blank");
        }
    })
});
