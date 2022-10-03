function initMaterialize() {
    //Initialise the dropdown elements of the navbar
    $(".dropdown-trigger").dropdown({ hover: true });

    //Initialise the modal plugin
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
}

function uploadTrainingImages(zipFile) {

}

function confirmUpload() {

}

function importTrainingImages(zipFile) {

}

function confirmImport() {

}

function labelTrainingImages(zipFile) {

}

function confirmLabelling() {
    
}

function updateTrainingStatus() {

}

//Use JQuery to make HTTP post requests to the APIs
//Taken from StackOverflow: https://stackoverflow.com/questions/6323338/jquery-ajax-posting-json-to-webservice
function httpPost(endpoint, data, success, error) {
    $.ajax({
        type: "POST",
        url: endpoint,
        data: JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

//Use JQuery to make HTTP get requests to the APIs
//Adapted from the httpPost function above
function httpGet(endpoint, success, error) {
    $.ajax({
        type: "GET",
        url: endpoint,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    });
}

//function to open a Materialize modal based on its ID
function showModal(modalId) {
    M.Modal.getInstance(document.getElementById(modalId)).open();
}

//function to close a Materialize modal based on its ID
function closeModal(modalId) {
    M.Modal.getInstance(document.getElementById(modalId)).close();
}