const spinnerModalId = "spinner-modal";
const errorModalId = "error-modal";
var trainingImagesAnalytics = null;
var predictionsAnalytics = null;
var modelsAnalytics = null;

function initMaterialize() {
    //Initialise the dropdown elements of the navbar
    $(".dropdown-trigger").dropdown({ hover: true });

    //Initialise the sidebar elements of the navbar
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);

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
    const urls_array = data["image_urls"];

    //Convert URLs from array to dictionary
    let urls = {};
    urls_array.forEach(function (item, index) { urls[index] = item; });

    //Get the results container
    const results = document.getElementById("training-images");

    displayTrainingImages(urls);

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

function getUnlabelledTrainingImages() {
    //Activate the spinner
    showModal(spinnerModalId);
    //Make the http get request
    httpGet(getUnlabelledEndpoint, displayUnlabelledTrainingImages, handleGetUnlabelledImagesError);
}

function displayUnlabelledTrainingImages(data) {
    //Get the image list out of the response data
    let images_arr = data["images"];
    //Need to convert this into a dictionary with id as key
    //and b64 data as the value
    let images = {}
    images_arr.forEach(image => images[image["id"]] = image["image"]);
    //Display the images
    displayTrainingImages(images, true);
    //Deactivate the spinnner
    closeModal(spinnerModalId);
}

function handleGetUnlabelledImagesError() {
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
        label: imageLabel,
        ids: ids
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

function startTraining() {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = { };
    httpPost(startTrainingEndpoint, data, confirmModelTrainingStarted, handleModelTrainingStartError);
}

function confirmModelTrainingStarted() {
    //Re-route the user to the check training status page
    window.location = checkTrainingStatusUrl;
}

function handleModelTrainingStartError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function updateTrainingStatus() {
    //make the get request
    httpGet(readLogEndpoint, displayTrainingLog, handleTrainingLogError);
}

function displayTrainingLog(messages) {
    //get the console div
    let console = document.getElementById("training-log-console");
    //clear the console
    console.innerHTML = "";
    //display each message
    messages["entries"].forEach(item => {
        //create the span
        let span = document.createElement("span");
        //add the message to the span
        span.appendChild(document.createTextNode(item));
        //add the span to the console
        console.appendChild(span);
    });
    //set timeout to refresh every 5 seconds
    setTimeout(updateTrainingStatus, 5000);
}

function handleTrainingLogError() {
    //Activate the error modal
    showModal(errorModalId);
    //Set a timeout to try again
    setTimeout(updateTrainingStatus, 30000);
}

function checkWarehouseUpdatedToday() {
    //Activate the spinner modal
    showModal(spinnerModalId);

    //Get confirmation as to whether today's snapshot has been posted
    httpGet(checkSnapshotPostedEndpoint, updateDataWarehouse, handleDataWarehouseUpdateError);
}

function updateDataWarehouse(posted) {
    //Begin the update process if training image snapshot not posted today
    if (!posted["snapshot_posted"]) getTrainingImagesSnapshot();
    //Otherwise jump to retrieving analytics
    else getTrainingImagesAnalytics();
}

function getTrainingImagesSnapshot() {
    //Get the training images snapshot
    httpGet(getImagesSnapshotEndpoint, postTrainingImagesSnapshot, handleDataWarehouseUpdateError);
}

function postTrainingImagesSnapshot(snapshot) {
    //Post the predictions snapshot
    httpPost(postImagesSnapshotEndpoint, snapshot, getPredictionsSnapshot, handleDataWarehouseUpdateError);
}

function getPredictionsSnapshot() {
    //Get the predictions snapshot
    httpGet(getPredictionsSnapshotEndpoint, postPredictionsSnapshot, handleDataWarehouseUpdateError);
}

function postPredictionsSnapshot(snapshot) {
    //Post the predictions snapshot
    httpPost(postPredictionsSnapshotEndpoint, snapshot, getModelsSnapshot, handleDataWarehouseUpdateError);
}

function getModelsSnapshot() {
    //Get the prediction models snapshot
    httpGet(getModelsSnapshotEndpoint, postModelsSnapshot, handleDataWarehouseUpdateError);
}

function postModelsSnapshot(snapshot) {
    //Post the prediction models snapshot
    httpPost(postModelsSnapshotEndpoint, snapshot, completeDataWarehouseUpdate, handleDataWarehouseUpdateError);
}

function completeDataWarehouseUpdate() {
    getTrainingImagesAnalytics();
}

function getTrainingImagesAnalytics() {
    httpGet(getImagesAnalyticsEndpoint, setTrainingImagesAnalytics, handleDataWarehouseUpdateError);
}

function setTrainingImagesAnalytics(data) {
    //Update global variable with training images analytics
    trainingImagesAnalytics = data["data"];
    //Get predictions analytics
    getPredictionsAnalytics();
}

function getPredictionsAnalytics() {
    httpGet(getPredictionsAnalyticsEndpoint, setPredictionsAnalytics, handleDataWarehouseUpdateError);
}

function setPredictionsAnalytics(data) {
    //Update global variable with predictions analytics data
    predictionsAnalytics = data["data"];
    //Get models analytics
    getModelsAnalytics();
}

function getModelsAnalytics() {
    httpGet(getModelsAnalyticsEndpoint, setModelsAnalytics, handleDataWarehouseUpdateError);
}

function setModelsAnalytics(data) {
    //Update the global variable with model analytics data
    modelsAnalytics = data["data"];
    renderAnalytics();
}

function renderAnalytics() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
}

function handleDataWarehouseUpdateError(error) {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
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

//function to display a grid of training images from a dictionary
//the dictionary may either be a simple array of urls or a dictionary
//of base64 images with the key as the id
function displayTrainingImages(images, isBase64=false) {
    //Get the results container
    const results = document.getElementById("training-images");

    //Use this to count the number of cols already added
    //to current row
    let colCount = 0;
    let row = createRow();
    let count = 0;
    for (var i in images) {
        //Create the result and add it to the current row
        let result = null;
        //If is base64, then the id is a guid
        if (isBase64) {
            result = createTrainingImageDisplay(images[i], count, i, true);
        } else {
            //Otherwise, the id is not set explicitly
            //the helper function will just use the image URL as id
            result = createTrainingImageDisplay(images[i], i)
        }
        row.appendChild(result);

        //Check if at end of row
        count++;
        colCount++;
        if (colCount == 4) {
            //Add the row to the results
            results.appendChild(row);
            //Create a new row and return to the first column
            row = createRow();
            colCount = 0;
        } else if (count == Object.keys(images).length) {
            results.appendChild(row);
        }
    }
}

//function to create a search result from a src and identifier
//the src may either be base64 or a url
function createTrainingImageDisplay(src, count, id=-1, isBase64=false) {
    //Use the image URL as the id for
    //non-base 64 images
    if (!isBase64) id=src;

    //Create the result container
    const result = createCell();

    //Get the hidden input to hold this result's URL
    const idElem = document.createElement("input");
    idElem.name = "id_" + count;
    idElem.type = "hidden";
    idElem.value = id;
    result.appendChild(idElem);

    //Display the image
    const img = document.createElement("img");
    if (isBase64) {
        img.src = "data:image/jpeg;base64," + src;
        img.alt = "This training image could not be displayed. It may be incorrectly formatted.";
    } else {
        img.src = src;
        img.alt = "This training image could not be displayed. Its URL may not be valid.";
    }
    img.className = "cat-image";
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