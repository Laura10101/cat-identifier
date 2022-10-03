var spinnerModalId = "spinner-modal";
var errorModalId = "error-modal";

function initMaterialize() {
    //Initialise the dropdown elements of the navbar
    $(".dropdown-trigger").dropdown({ hover: true });

    //Initialise the modal plugin
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
}

function uploadTrainingImages(b64ZipFile) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = { zip_file: JSON.stringify(b64ZipFile) };
    httpPost(imageUploadEndpoint, data, confirmUpload, handleUploadError);
}

function confirmUpload(data) {
    let successList = document.getElementById("upload-success");
    let ignoredList = document.getElementById("upload-ignored");
    //Deactivate the spinner
    closeModal(spinnerModalId);
    //Add successfully-imported files to the success list
    for (const name in data["training_images"]) {
        const item = createListItem(name);
        successList.appendChild(item);
    }
    //Add ignored files to the ignore list
    for (const i in data["ignored"]) {
        const item = createListItem(data["ignored"][i]);
        ignoredList.appendChild(item);
    }
}

function handleUploadError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function importTrainingImages(urlList) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = { image_urls: JSON.stringify(urlList) };
    httpPost(imageImportEndpoint, data, confirmImport, handleImportError);
}

function confirmImport() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
}

function handleImportError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function labelTrainingImages(imageLabel, ids) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = {
        label: JSON.stringify(imageLabel),
        ids: JSON.stringify(ids)
    };
    httpPost(imageLabelEndpoint, data, confirmLabelling, handleLabellingError);
}

function confirmLabelling() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
}

function handleLabellingError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
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

//function to create a new list item from a list
function createListItem(text, classes="") {
    var item = document.createElement("li")
    item.appendChild(document.createTextNode(text))
    item.className = classes
    return item
}