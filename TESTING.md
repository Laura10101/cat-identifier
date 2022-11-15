# Testing

## Browser Compatibility

### Admin Navigation

__On Edge__

__On FireFox__

__On Chrome__

### The Breeder Upload Journey

__On Edge__

__On FireFox__

__On Chrome__

### Importing Training Images

__On Edge__

__On FireFox__

__On Chrome__

### Labelling Training Images

__On Edge__

__On FireFox__

__On Chrome__

### Checking Training Status

__On Edge__

__On FireFox__

__On Chrome__

### Dashboards

__On Edge__

__On FireFox__

__On Chrome__

## Code Validation

### HTML Validation
All validation errors identified during the development of the application were resolved.

One warning remains indicating that the sections that are used for the different parts of the application have no headers. I decided to ignore these warnings as adding headers would have undermined the layout of the application.

The index.html file was validated using the W3C official validator as shown below:
![HTML validation on the index.html file](https://laura10101.github.io/kitten-calculator/documentation/testing/html-validation-index.png)

Furthermore, the questions and results section of the application each generate HTML dynamically through JavaScript, so a sample of the HTML generated at each stage was also validated.

The following screenshot shows the validation results of HTML generated during the question stage of the application:

![HTML validation on the questions section](https://laura10101.github.io/kitten-calculator/documentation/testing/html-validation-questions.png)

The following screenshot shows the validation results of HTML generated during the results stage of the application:

![HTML validation on the results section](https://laura10101.github.io/kitten-calculator/documentation/testing/html-validation-results.png)

[Click here](https://validator.w3.org/nu/?doc=https%3A%2F%2Flaura10101.github.io%2Fkitten-calculator%2F) for a link to the official W3C validator for the application.

### CSS Validation
The CSS was validated through W3C's jigsaw validator and no errors were found in the CSS for the breeder app:

![CSS validation for the Breeder app](documentation/validation/js/breeder-css-validation.png)


No errors were found in the CSS for the admin app:

![CSS validation for the Breeder app](documentation/validation/js/admin-css-validation.png)

### JavaScript Validation

JSHint was used to validate the JavaScript for both the breeder and admin apps.

No validation errors were found for the breeder app:

![JSHint validation for the Breeder app](documentation/validation/js/breeder-js-validation.png)

No validation errors were found for the admin app:

![JSHint validation for the Breeder app](documentation/validation/js/admin-js-validation.png)

In both applications, JSHint highlighted identifiers which are referenced but not declared. In all cases, these were actual declared either in the
Flask template of the file or in one of the three JavaScript frameworks used by the application (Materialize, JQuery, Charts.js). Where identifiers
are declared in Flask templates, this is typically because the identifier is a constant whose value is set using a Jinja expression.

In both applications, JSHint highlighted identifiers that are unused. In all cases, these identifiers are functions that are used outside of the
JavaScript file.

### Python Validation



## Responsiveness

### Navigation
Blah

### Labelling Form
Blah

## User Story Tests

### Cat Breeder or Owner Stories

**As a cat breeder or owner, I want to be able to upload a photo of my cat, so that I can find out what phenotype my cat is**

**As a cat breeder or owner, I want to see that my results are being calculated, so that I know the application is still working**


**As a cat breeder or owner, I want to see how the application has classified my cat's photo, so that I can identify what phenotype my cat has**

### Model Administrator Stories

**As a model administrator, I want to get feedback from the cat breeder or owner as to whether the predicted phenotype was correct or not, so that I can identify opportunities to improve the accuracy of the model**

**As a model administrator, I want to be able to easily upload a large number of training images, so that I have a set of relevant training data for the machine learning model**

**As a model administrator, I want to see that my training images are being uploaded, so that I know the application is still working correctly**

**As a model administrator, I want to be able to search Google images for relevant training data from within the application, so that I can find images with which to train the machine learning model**

**As a model administrator, I want to be able to select images to import as training data from the results returned by Google, so that I can import relevant images to my training data repository**

**As a model administrator, I want to see that my selected training images are being imported, so that I know the application is still working correctly**

**As a model administrator, I want to be able to apply labels to training images in bulk, so that I can quickly and easily prepare clean data with which to train the machine learning model**

**As a model administrator, I want to see that my labels are being applied to my training data, so that I know the application is still working correctly**

**As a model administrator, I want to be able to start the training process for new models, so that I can make trained models available for breeders and pet owners to use**

**As a model administrator, I want to be able to check the current status of the training process, so that I can make sure the training process is working and review any errors that arise**

**As a model administrator, I want to be able to delete training images, so that I can rebalance the training dataset if needed**

**As a model administrator, I want to see reporting about the performance of the machine learning model, so that I can identify areas to improve accuracy**

**As a model administrator, I want to see reporting about the size and contents of the training set, so that I can identify gaps or imbalances and correct these**

**As a model administrator, I want to be able to delete reporting data, so that I can reset the statistics if needed**

## Bugs

### Fixed Bugs
The following bugs were fixed during the development process:
- 

### Unresolved Bugs
The following bugs were identified during testing but not resolved:

- 