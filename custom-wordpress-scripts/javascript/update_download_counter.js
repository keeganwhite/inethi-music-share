/**
 * When a product page is loaded this script updates the download counter
 */

$( document ).ready(function() {
    console.log("button pressed")
    const dataType = 'json';
    let couponGenerator = "http://0.0.0.0:5000/api/updatedownloads"
    const song_name = document.getElementsByClassName("product_title entry-title")[0].textContent.trim();
    // User name is found in short description which takes the following form:
    // Check out my profile by searching for *username* in the musician directory
    const username = document.getElementsByClassName("woocommerce-product-details__short-description")[0].textContent.trim();
    console.log(song_name)

    const data = {
        "username": username,
        "songname": song_name
    }
    console.log("About to send")
    $.ajax({
        type: "POST",
        url: couponGenerator,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data, status) {
            const json_obj = data.message;
            const message = JSON.stringify(json_obj);
            alert("Downloads: "+ message);
        },
        error: function (errMsg) {
            console.log("could not load download counter");
        }
    })
});