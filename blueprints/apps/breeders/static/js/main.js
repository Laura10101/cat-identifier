//Initialize Materialize framework
function initMaterialize() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
}

//Display a preview of the image selected by the breeder
//before they upload it
//Adapted from code at: https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
function previewSelectedCatImage() {
    //Get the file input and the image
    let [imageInput] = document.getElementById("image-input").files;
    let reader = new FileReader();
    reader.onload = function() {
        //Display the result from the FileReader in the preview image
        let imagePreview = document.getElementById("image-preview");
        imagePreview.src = reader.result;
        //Now close the selection modal
        M.Modal.getInstance(document.getElementById("image-selection-modal")).close();
    };
    reader.readAsDataURL(imageInput);
}

//Submit the upload form when the upload button is clicked
function submitUploadForm() {
    $("#upload-form").submit();
}

//Use the Prediction API to determine the cat's
//phenotype based on the image uploaded by the user
function getCatPhenotype(b64Image) {
    //Show the spinner modal
    M.Modal.getInstance(document.getElementById("spinner-modal")).open()
    //Create the JSON object to pass to the prediction API
    const data = {
        "image": b64Image
    };
    //Post the HTTP request using JQuery
    httpPost(postPredictionEndpoint, data, displayCatPhenotype, function() { 
        M.Modal.getInstance(document.getElementById("error-modal")).open();
    });
}

//Function to handle the callback from the Prediction API after
//posting a new prediction
function displayCatPhenotype(data) {
    //Get references to the relevant DOM elements
    let spinner = M.Modal.getInstance(document.getElementById("spinner-modal"));
    let sourceImage = $("#source-image");
    let phenotypeImage = $("#phenotype-image");
    let phenotypeText = $("#phenotype-text");
    let predictionIdField = $("#prediction-id");

    //Extract data from the response
    let predictionId = data["id"];
    let traits = data["label"];

    //Calculate the phenotype
    let phenotype = determinePhenotype(traits);
    //Calculate the phenotype Id by replacing spaces with hyphens - HTML friendly
    let phenotypeId = phenotype.replace(new RegExp(" ", "g"), "-");

    //Update DOM elements
    phenotypeImage.attr("src", baseStaticUrl + "/" + phenotypeId + ".jpg");
    phenotypeText.text(phenotype);
    predictionIdField.attr("value", predictionId);
    
    //Close the spinner
    spinner.close();
}

//From a JSON object containing cat traits,
//calculate a string describing the cat's phenotype
function determinePhenotype(traits) {
    //Firstly, check if the prediction indicates this is a cat
    if (!traits["is_cat"]) return "not a cat";

    //Next, get the colour and pattern
    let colour = traits["colour"].toLowerCase();
    let pattern = traits["pattern"].toLowerCase();

    //Next, put the phenotype text together
    let phenotype = colour;

    //If it is tabby or pointed, state this explicitly
    //otherwise don't state it
    if (traits["is_tabby"]) phenotype += " tabby";
    if (traits["is_pointed"]) phenotype += " pointed";

    //Finally, add the pattern if it isn't self
    if (pattern != "self") phenotype += pattern;
    return phenotype;
}

//Function to redirect users back to the initial page when they have acknowledge an error
function resultsErrorAcknowledged() {
    window.location.href = startAgainUrl;
}

function acceptPrediction() {
    document.getElementById("feedback-value").value = true;
    submitFeedbackForm();
}

function rejectPrediction() {
    document.getElementById("feedback-value").value = false;
    submitFeedbackForm();
}

function submitFeedbackForm() {
    $("#feedback-form").submit();
}

function postFeedback(accepted) {
    //Show the spinner modal
    M.Modal.getInstance(document.getElementById("spinner-modal")).open()
    let data = { "user_feedback": accepted };
    httpPost(feedbackEndpoint, data, confirmFeedbackPosted, handleFeedbackError);
}

function confirmFeedbackPosted() {
    //Show the spinner modal
    M.Modal.getInstance(document.getElementById("spinner-modal")).close()
}

function handleFeedbackError() {
    //Show the error modal
    M.Modal.getInstance(document.getElementById("error-modal")).open()
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