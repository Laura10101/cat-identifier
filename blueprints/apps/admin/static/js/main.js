var spinnerModalId = "spinner-modal";

function initMaterialize() {
    //Initialise the dropdown elements of the navbar
    $(".dropdown-trigger").dropdown({ hover: true });

    //Initialise the modal plugin
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
}

function uploadTrainingImages(b64ZipFile) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
}

function confirmUpload() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
}

function importTrainingImages(urlList) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
}

function confirmImport() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
}

function labelTrainingImages(imageLabels) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
}

function confirmLabelling() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
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

//function to open a Materialize modal based on its ID
function showModal(modalId) {
    M.Modal.getInstance(document.getElementById(modalId)).open();
}

//function to close a Materialize modal based on its ID
function closeModal(modalId) {
    M.Modal.getInstance(document.getElementById(modalId)).close();
}