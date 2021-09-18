/**
 * When the user submits their form, the form data is sent  to the API and the result of the post request is displayed to the user
 */

document.addEventListener( 'wpcf7submit', function( event ) {
    console.log("button pressed")
    const dataType = 'json';
    let couponGenerator = "http://0.0.0.0:5000/api/create"
    var inputs = event.detail.inputs;
    const username = inputs[0].value;
    const songname = inputs[2].value;
    const password = inputs[3].value;
    console.log(username)
    console.log(songname)
    console.log(password)
    const data = {
        "username": username,
        "password": password,
        "songname": songname
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
            alert("Song name or pin incorrect");
        }
    })
});
