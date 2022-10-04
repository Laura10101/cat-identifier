var spinnerModalId = "spinner-modal";
var errorModalId = "error-modal";

function initMaterialize() {
    //Initialise the dropdown elements of the navbar
    $(".dropdown-trigger").dropdown({ hover: true });

    //Initialise the modal plugin
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);

    //Initialise the select plugin
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
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

function getSearchResults(query) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the API request to get the search results
    let endpoint = imageSearchEndpoint + "?query=" + query;
    httpGet(endpoint, displaySearchResults, handleSearchError);
}

function displaySearchResults(data) {
    //Get the list of urls
    const urls = data["image_urls"];

    //Get the results container
    const results = document.getElementById("search-results");

    //Use this to count the number of cols already added
    //to current row
    let colCount = 0;
    let row = createRow();
    for (let i = 0; i < urls.length; i++) {
        //Create the result and add it to the current row
        const result = createSearchResult(urls[i], i);
        row.appendChild(result);

        //Check if at end of row
        colCount++;
        if (colCount == 4) {
            //Add the row to the results
            results.appendChild(row);
            //Create a new row and return to the first column
            row = createRow();
            colCount = 0;
        }
    }

    //Deactivate the spinnner
    closeModal(spinnerModalId);
}

function handleSearchError() {
    //Show error modal
    showModal(errorModalId);
}

function importTrainingImages(urlList) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = { image_urls: urlList };
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

//Use JQuery to make HTTP GET requests to the APIs
//Adapted from the httpPost method
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

//function to create a new list item from a list
function createListItem(text, classes="") {
    var item = document.createElement("li")
    item.appendChild(document.createTextNode(text))
    item.className = classes
    return item
}

//function to create a search result from a url
function createSearchResult(url, count) {
    //Create the result container
    const result = createCell();

    //Get the hidden input to hold this result's URL
    const urlElem = document.createElement("input");
    urlElem.name = "url_" + count;
    urlElem.type = "hidden";
    urlElem.value = url;
    result.appendChild(urlElem);

    //Display the image
    const img = document.createElement("img");
    img.src = url;
    img.alt = "A picture found through our search API which is currently unavailable.";
    img.className = "search-result-image";
    result.appendChild(img);

    //Add a label to the checkbox
    const label = document.createElement("label");
    result.appendChild(label);

    //Display the checkbox
    const chkBox = document.createElement("input");
    chkBox.type = "checkbox";
    chkBox.id = "include_" + count;
    chkBox.name = chkBox.id;
    label.appendChild(chkBox);

    //Create a span to include the label text
    const span = document.createElement("span")
    span.appendChild(document.createTextNode("Include?"))
    label.appendChild(span)

    return result;
}

//function to get a new Materialize row
function createRow() {
    const row = document.createElement("div");
    row.className = "row";
    return row;
}

//function to get a new Materialize cell
function createCell() {
    const cell = document.createElement("div");
    //Materialize uses a standard 12 column grid
    //https://materializecss.com/grid.html
    cell.className = "col s12 m6 l3";
    return cell;
}