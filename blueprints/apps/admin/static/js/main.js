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

    initSelects();
}

function initSelects() {
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

function clearTrainingImages(filter) {
    //Activate the spinner
    showModal(spinnerModalId);

    httpDelete(deleteTrainingImageEndpoint, displayClearTrainingImagesResult, handleClearTrainingImagesError, filter);
}

function handleClearTrainingImagesError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function displayClearTrainingImagesResult() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
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

function selectAllCatImages() {
    changeCatImageSelectionState(true);
}

function unselectAllCatImages() {
    changeCatImageSelectionState(false);
}

function importTrainingImages(urlList, query) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = { image_urls: urlList, query: query };
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

function getUnlabelledTrainingImages(query=null) {
    //Activate the spinner
    showModal(spinnerModalId);
    //Make the http get request
    if (query == null || query == "") {
        httpGet(getUnlabelledEndpoint, displayUnlabelledTrainingImages, handleGetUnlabelledImagesError);
    } else {
        httpGet(getUnlabelledEndpoint + "?query=" + query, displayUnlabelledTrainingImages, handleGetUnlabelledImagesError);
    }
}

function displayUnlabelledTrainingImages(data) {
    //Get the image list out of the response data
    let images_arr = data["images"];
    //Need to convert this into a dictionary with id as key
    //and b64 data as the value
    let images = {}
    let queries = []
    images_arr.forEach(image => {
        images[image["id"]] = image["image"];
        if (image["source_query"] != null) {
            if (!queries.includes(image["source_query"])) {
                queries.push(image["source_query"]);
            }
        }
    });
    //Display the queries in the select box
    queries.sort();
    //update the query filter select
    //this will only update first time around
    updateQueryFilterSelect(queries);
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

function getUnreviewedPredictions() {
    //Activate the spinner
    showModal(spinnerModalId);
    //Make the http get request
    httpGet(getUnreviewedPredictionsEndpoint, displayUnreviewedPredictions, handleGetUnreviewedPredictionsError);
}

function displayUnreviewedPredictions(data) {
    //Get the image list out of the response data
    let images_arr = data["predictions"];
    //Need to convert this into a dictionary with id as key
    //and b64 data as the value
    let images = {};
    let labels = {};
    images_arr.forEach(image => {
        images[image["id"]] = image["image"];
        labels[image["id"]] = image["label"];
    });
    //Display the images
    displayTrainingImages(images, true, labels);
    //Deactivate the spinnner
    closeModal(spinnerModalId);
}

function handleGetUnreviewedPredictionsError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function patchAdminPredictionReview(label, ids) {
    //Activate the spinner
    showModal(spinnerModalId);

    //Make the post request
    data = {
        admin_feedback: label["is_correct"],
        ids: ids
    };
    let successHandler = function() {
        importPredictionsAsTrainingImages(label, ids);
    }
    httpPost(postPredictionReviewEndpoint, data, successHandler, handleReviewError);
}

function importPredictionsAsTrainingImages(label, ids) {

}

function confirmPredictionImport() {
    //Deactivate the spinner
    closeModal(spinnerModalId);
}

function handleReviewError() {
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
        let pre = document.createElement("pre");
        //add the message to the span
        pre.appendChild(document.createTextNode(item));
        //add the span to the console
        console.appendChild(pre);
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
    renderTrainingSetByDateChart(trainingImagesAnalytics);
    renderTrainingSetByLabelChart(trainingImagesAnalytics);
    renderModelPerformanceByDateChart(modelsAnalytics);
    renderPredictionQualityByDateChart(predictionsAnalytics);
    //Deactivate the spinnner
    closeModal(spinnerModalId);
}

function handleDataWarehouseUpdateError(error) {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function clearTrainingImageAnalytics() {
    if (mustClearTrainingImageAnalytics) {
        httpDelete(postImagesSnapshotEndpoint, clearPredictionAnalytics, handleAnalyticsClearanceError);
    } else {
        clearPredictionAnalytics();
    }
}

function clearPredictionAnalytics() {
    if (mustClearPredictionAnalytics) {
        httpDelete(postPredictionsSnapshotEndpoint, clearModelAnalytics, handleAnalyticsClearanceError);
    } else {
        clearModelAnalytics();
    }
}

function clearModelAnalytics() {
    if (mustClearModelAnalytics) {
        httpDelete(postModelsSnapshotEndpoint, displayAnalyticsClearanceResult, handleAnalyticsClearanceError);
    } else {
        displayAnalyticsClearanceResult();
    }
}

function handleAnalyticsClearanceError() {
    //Deactivate the spinnner
    closeModal(spinnerModalId);
    //Activate the error modal
    showModal(errorModalId);
}

function displayAnalyticsClearanceResult() {
    closeModal(spinnerModalId);
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

//Use JQuery to make HTTP DELETE requests to the APIs
//Adapted from the httpPost method
function httpDelete(endpoint, success, error, data=null) {
    request = {
        type: "DELETE",
        url: endpoint,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: success,
        error: error
    };

    if (data != null) {
        request["data"] = JSON.stringify(data);
    }
    $.ajax(request);
}

//Use JQuery to make HTTP PATCH requests to the APIs
//Adapted from the httpPost method
function httpPatch(endpoint, data, success, error) {
    request = {
        type: "PATCH",
        url: endpoint,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        data: JSON.stringify(data),
        success: success,
        error: error
    };
    $.ajax(request);
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
    var item = document.createElement("li");
    item.appendChild(document.createTextNode(text));
    if (classes.length > 0) classes += " ";
    classes += "defaultlist";
    item.className = classes;
    return item;
}

//function to display a grid of training images from a dictionary
//the dictionary may either be a simple array of urls or a dictionary
//of base64 images with the key as the id
function displayTrainingImages(images, isBase64=false, labels=null) {
    //Get the results container
    const results = document.getElementById("training-images");
    results.innerHTML = "";
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
            if (labels != null) {
                result = createTrainingImageDisplay(images[i], count, i, true, labels[i]);
            } else {
                result = createTrainingImageDisplay(images[i], count, i, true);
            }
        } else {
            //Otherwise, the id is not set explicitly
            //the helper function will just use the image URL as id
            if (labels != null) {
                result = createTrainingImageDisplay(images[i], i, images[i], false, labels[i]);
            } else {
                result = createTrainingImageDisplay(images[i], i);
            }
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
function createTrainingImageDisplay(src, count, id=-1, isBase64=false, label=null) {
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

    const imgDiv = document.createElement("div");
    result.appendChild(imgDiv);

    //Display the prediction or label, if it is provided
    if (label != null) {
        let labelDiv = document.createElement("div");
        result.appendChild(labelDiv);

        let labelText = "This is " + determinePhenotype(label);
        let labelP = document.createElement("p");
        labelP.innerText = labelText;
        labelDiv.appendChild(labelP);
    }

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
    imgDiv.appendChild(img);

    const inputDiv = document.createElement("div");
    result.appendChild(inputDiv);

    //Add a label to the checkbox
    const labelElem = document.createElement("label");
    inputDiv.appendChild(labelElem);

    //Display the checkbox
    const chkBox = document.createElement("input");
    chkBox.type = "checkbox";
    chkBox.id = "include_" + count;
    chkBox.className = "include-image-chkbox";
    chkBox.name = chkBox.id;
    labelElem.appendChild(chkBox);

    //Create a span to include the label text
    const span = document.createElement("span")
    span.appendChild(document.createTextNode("Include?"))
    labelElem.appendChild(span)

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

//function to change the selection state of images
//in a cat image grid
function changeCatImageSelectionState(targetState) {
    let boxes = document.getElementsByClassName("include-image-chkbox");
    for (let box of boxes) {
        box.checked = targetState;
    }
}

//function to update the filter select box with queries
function updateQueryFilterSelect(queries) {
    //get the select box
    const queryList = document.getElementById("query-filter");
    //only populate once per page load
    if (queryList.options.length == 0) {
        //add the default filter which shows everything
        let option = document.createElement("option");
        option.text = "Show all";
        option.value = "unfiltered";
        queryList.add(option);

        //add each query to the list
        queries.forEach(query => {
            option = document.createElement("option");
            option.text = query;
            option.value = query;
            queryList.add(option);
        })
        //re-initialise the select box
        initSelects();
    }
}

/* CHART SETUP */
//set up chart to show training set size by date
function renderTrainingSetByDateChart(data) {
    let analysedData = analyseTrainingSetByDate(data);
    const trainingSetByDateChart = new Chart(trainingSetByDateCanvas, {
        type: "line",
        data: {
            labels: analysedData.dates,
            datasets: [{
                label: "# of training images",
                data: analysedData.metrics,
                backgroundColor: backgroundColours[0],
                borderColor: borderColours[0]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Training set size by date"
                }
            }
        }
    });
}

function analyseTrainingSetByDate(data) {
    return getMetricByDate(data, metric="count", method="sum");
}

//set up chart to show training set size by label attributes
function renderTrainingSetByLabelChart(data) {
    let isCatMetrics = getLatestFilteredMetric(data, "is_cat", "count", "sum", "date");
    let colourMetrics = getLatestFilteredMetric(data, "colour", "count", "sum", "date");
    let isTabbyMetrics = getLatestFilteredMetric(data, "is_tabby", "count", "sum", "date");
    let patternMetrics = getLatestFilteredMetric(data, "pattern", "count", "sum", "date");
    let isPointedMetrics = getLatestFilteredMetric(data, "is_pointed", "count", "sum", "date");

    isCatMetrics = pivotTrainingSetByLabelMetricsObject(isCatMetrics, { false: "Not a cat", true: "Is a cat"});
    colourMetrics = pivotTrainingSetByLabelMetricsObject(colourMetrics, { null: "Not Labelled" });
    isTabbyMetrics = pivotTrainingSetByLabelMetricsObject(isTabbyMetrics, { false: "Not a tabby", true: "Is a tabby" });
    patternMetrics = pivotTrainingSetByLabelMetricsObject(patternMetrics, { null: "Not Labelled" });
    isPointedMetrics = pivotTrainingSetByLabelMetricsObject(isPointedMetrics, { false: "Not pointed", true: "Is pointed" });

    const trainingSetByLabelChart = new Chart(trainingSetByLabelCanvas, {
        type: "pie",
        data: {
            labels: [],
            datasets: []
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Size of training image set by label attributes"
                }
            }
        }
    });
    updateTrainingSetByLabelChart(isCatMetrics, trainingSetByLabelChart, "# of training images by cat or not cat");

    document.getElementById("show-is-cat-label-data-btn").onclick = function() {
        updateTrainingSetByLabelChart(
            isCatMetrics,
            trainingSetByLabelChart,
            "# of training images by cat or not cat"
        );
    }

    document.getElementById("show-colour-label-data-btn").onclick = function() {
        updateTrainingSetByLabelChart(
            colourMetrics,
            trainingSetByLabelChart,
            "# of training images by colour"
        );
    }

    document.getElementById("show-is-tabby-label-data-btn").onclick = function() {
        updateTrainingSetByLabelChart(
            isTabbyMetrics,
            trainingSetByLabelChart,
            "# of training images by tabby or not tabby"
        );
    }

    document.getElementById("show-pattern-label-data-btn").onclick = function() {
        updateTrainingSetByLabelChart(
            patternMetrics,
            trainingSetByLabelChart,
            "# of training images by pattern"
        );
    }

    document.getElementById("show-is-pointed-label-data-btn").onclick = function() {
        updateTrainingSetByLabelChart(
            isPointedMetrics,
            trainingSetByLabelChart,
            "# of training images by pointed or not pointed"
        );
    }
}

function updateTrainingSetByLabelChart(data, chart, label) {
    chart.data.labels = data.labels;
    chart.data.datasets = [];
    chart.data.datasets.push({
        label: label,
        data: data.metrics,
        backgroundColor: backgroundColours,
        borderColor: borderColours
    });
    chart.update();
}

function pivotTrainingSetByLabelMetricsObject(data, categoryMapping={}) {
    let labels = [];
    let metrics = []
    for (category in data) {
        if (category in categoryMapping) labels.push(categoryMapping[category]);
        else labels.push(category);
        metrics.push(data[category]);
    }
    return {
        labels: labels,
        metrics: metrics
    }
}

//set up chart to show model performance by date
function renderModelPerformanceByDateChart(data) {
    let minAccuracyMetrics = getMetricByDate(data, "min_accuracy", "min", "snapshot_date");
    let avgAccuracyMetrics = getMetricByDate(data, "avg_accuracy", "avg", "snapshot_date");
    let maxAccuracyMetrics = getMetricByDate(data, "max_accuracy", "max", "snapshot_date");
    const modelPerformanceByDateChart = new Chart(modelPerformanceByDateCanvas, {
        type: "line",
        data: {
            labels: minAccuracyMetrics.dates,
            datasets: [{
                label: "Min",
                data: minAccuracyMetrics.metrics,
                backgroundColor: backgroundColours[0],
                borderColor: borderColours[0]
            },
            {
                label: "Average",
                data: avgAccuracyMetrics.metrics,
                backgroundColor: backgroundColours[1],
                borderColor: borderColours[1]
            },
            {
                label: "Max",
                data: maxAccuracyMetrics.metrics,
                backgroundColor: backgroundColours[2],
                borderColor: borderColours[2]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Min, average and max performance during training over time"
                }
            }
        }
    });
}

//set up chart to show prediction quality by date
function renderPredictionQualityByDateChart(data) {
    let metrics = analysePredictionQualityByDate(data);
    const predictionQualityByDateChart = new Chart(predictionQualityByDateCanvas, {
        type: "line",
        data: {
            labels: metrics.dates,
            datasets: [{
                label: "User Accepted",
                data: metrics.userAcceptedPredictions,
                backgroundColor: backgroundColours[0],
                borderColor: borderColours[0]
            },
            {
                label: "Admin Accepted",
                data: metrics.adminAcceptedPredictions,
                backgroundColor: backgroundColours[1],
                borderColor: borderColours[1]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "User acceptance versus admin acceptance of predictions (%)"
                }
            }
        }
    });
}

function analysePredictionQualityByDate(data) {
    let totalPredictionsByDate = getMetricByDate(data);
    let userAcceptedPredictionsByDate = getMetricByDate(
            data, "count", "sum", "date", "user_review_status", "Accepted"
        );
    let adminAcceptedPredictionsByDate = getMetricByDate(
            data, "count", "sum", "date", "admin_review_status", "Accepted"
        );
    let userAcceptedPredictions = [];
    let adminAcceptedPredictions = [];
    for (let i = 0; i < totalPredictionsByDate.metrics.length; i++) {
        let total = totalPredictionsByDate.metrics[i];
        let userAccepted = userAcceptedPredictionsByDate.metrics[i];
        let adminAccepted = adminAcceptedPredictionsByDate.metrics[i];
        userAcceptedPredictions.push(Math.round((userAccepted / total) * 100));
        adminAcceptedPredictions.push(Math.round((adminAccepted / total) * 100));
    }
    return {
        dates: totalPredictionsByDate.dates,
        userAcceptedPredictions: userAcceptedPredictions,
        adminAcceptedPredictions: adminAcceptedPredictions
    }
}

//get the most recent value for a given metric broken down by values of a given category field
function getLatestFilteredMetric(data, categoryField, metric="count", method="sum", dateField="date") {
    //Find the most recent date in the data set
    let groupedData = groupByDate(data);
    let max = maxDate(Object.keys(groupedData));
    //List out all categories refered to in the snapshots for most recent date
    let categories = [];
    data.forEach(snapshot => {
        if (new Date(snapshot[dateField]).getTime().toString() == max) {
            let category = snapshot[categoryField];
            if (!(category in categories)) {
                categories.push(category);
            }
        }
    });
    //Add the metric for each category
    let metricByCategory = {};
    categories.forEach(category => {
        let metricByDate = getMetricByDate(data, metric, method, dateField, categoryField, category);
        metricByCategory[category] = metricByDate.metrics[metricByDate.metrics.length - 1];
    });
    return metricByCategory;
}

//get a given metric by date for a given data set using given method
function getMetricByDate(data, metric="count", method="sum", dateField="date", filterField=null, filterValue=null) {
    // first, group the data into an object with key = date and
    // value = an array of the metric values for all snapshots matching that date
    let groupedData = groupByDate(data, metric, dateField, filterField, filterValue);
    // next, apply the aggregation function to the array of metric values for each date
    // to produce an object with a single aggregated value for each date
    let aggregatedData = aggregateByDate(groupedData, metric, method);
    // then fill in any missing values so that all dates between the min and max date range
    // have a value. if a date is missing its value, use the previous day's value
    let filledData = fillMetricAggregation(aggregatedData);
    //finally, pivot the object to get a dates array and a metrics array
    return pivotToDateMetricArrays(filledData);
}

//group data into an array of the given metric by date
function groupByDate(data, metric, dateField="date", filterField=null, filterValue=null) {
    let metricByDate = {};
    data.forEach(snapshot => {
        let date = new Date(snapshot[dateField]).getTime();
        if (!(date in metricByDate)) {
            metricByDate[date] = [];
        }
        if (filterField != null) {
            if (snapshot[filterField] == filterValue) metricByDate[date].push(snapshot[metric]);
        } else {
            metricByDate[date].push(snapshot[metric]);
        }
    });
    return metricByDate;
}

//create a dictionary which gives the aggregated
//metric for each date in the data based on the
//specified aggregation method
function aggregateByDate(metricsByDate, metric="count", method="sum") {
    let aggregatedMetricsByDate = {};
    for (let date in metricsByDate) {
        let metrics = metricsByDate[date];
        switch(method) {
            case "sum":
                aggregatedMetricsByDate[date] = metrics.reduce((a, b) => a + b, 0);
                break;

            case "min":
                aggregatedMetricsByDate[date] = metrics.reduce((a, b) => {
                    if (b < a) return b;
                    else return a;
                }, 99999999);
                break;

            case "max":
                aggregatedMetricsByDate[date] = metrics.reduce((a, b) => {
                    if (b > a) return b;
                    else return a;
                }, -99999999);
                break;

            case "avg":
                let sum = metrics.reduce((a, b) => a + b, 0);
                aggregatedMetricsByDate[date] = sum / metrics.length;
                break;

            case "count":
                aggregatedMetricsByDate[date] = metrics.length;
                break;
        }
    }
    return aggregatedMetricsByDate;
}

//function to fill in missing dates in an aggregated data object
function fillMetricAggregation(aggregatedMetrics) {
    let dates = Object.keys(aggregatedMetrics);
    let min = minDate(dates);
    let max = maxDate(dates);
    let currentDate = new Date();
    currentDate.setTime(min);
    while (currentDate.getTime().toString() <= max) {
        if (!(currentDate.getTime().toString() in aggregatedMetrics)) {
            let previousDate = subtractDays(currentDate);
            aggregatedMetrics[currentDate.getTime()] = aggregatedMetrics[previousDate.getTime()];
        }
        currentDate = addDays(currentDate);
    }
    return aggregatedMetrics;
}

//pivot an object into two dates and metrics arrays, rather than date, value pairs
function pivotToDateMetricArrays(data) {
    let min = minDate(Object.keys(data))
    let max = maxDate(Object.keys(data))
    let currentDate = new Date();
    currentDate.setTime(min);
    let dates = [];
    let metrics = []
    while (currentDate.getTime().toString() <= max) {
        dates.push(toShortFormat(currentDate));
        metrics.push(data[currentDate.getTime().toString()]);
        currentDate = addDays(currentDate);
    }
    return {
        dates: dates,
        metrics: metrics
    }
}

/* Date analytics */
function addDays(date, numberOfDays=1) {
    date = new Date(date);
    date.setDate(date.getDate() + numberOfDays);
    return date;
}

function subtractDays(date, numberOfDays=1) {
    date = new Date(date);
    date.setDate(date.getDate() - numberOfDays);
    return date;
}

function minDate(dates) {
    let min = null;
    dates.forEach(date => {
        if (min == null) {
            min = date;
        } else {
            if (date < min) min = date;
        }
    });
    return min;
}

function maxDate(dates) {
    let max = null;
    dates.forEach(date => {
        if (max == null) {
            max = date;
        } else {
            if (date > max) max = date;
        }
    });
    return max;
}


//converts a date to a short format string
//taken from StackOverflow: https://stackoverflow.com/questions/27480262/get-current-date-in-dd-mon-yyy-format-in-javascript-jquery
function toShortFormat(date) {
    const monthNames = ["Jan", "Feb", "Mar", "Apr",
                        "May", "Jun", "Jul", "Aug",
                        "Sep", "Oct", "Nov", "Dec"];
    
    const day = date.getDate();
    
    const monthIndex = date.getMonth();
    const monthName = monthNames[monthIndex];
    
    const year = date.getFullYear();
    
    return "" + day + " " + monthName + " " + year;
}
/* End date analytics */

//From a JSON object containing cat traits,
//calculate a string describing the cat's phenotype
function determinePhenotype(traits) {
    //Firstly, check if the prediction indicates this is a cat
    if (!traits["is_cat"]) return "not a cat";

    //Next, get the colour and pattern
    let colour = traits["colour"].toLowerCase();
    
    //Next, put the phenotype text together
    let phenotype = "a " + colour;

    //If it is tabby or pointed, state this explicitly
    //otherwise don't state it
    if (traits["is_tabby"]) phenotype += " tabby";
    if (traits["is_pointed"]) phenotype += " point";

    //Finally, add the pattern if it isn't self
    let pattern = traits["pattern"].toLowerCase();
    if (pattern != "self") phenotype += " " + pattern;
    else {
        if (!traits["is_tabby"] && !traits["is_pointed"]) phenotype += " " + pattern;
    }
    return phenotype;
}