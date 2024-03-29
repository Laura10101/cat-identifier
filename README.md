# Cat Identifier

British Shorthair cats are the most popular breed of cat in the UK. There is a large body of hobby breeders who enjoy raising kittens. However, feline genetics is a complicated area, and because the British Shorthair is available in a broad range of colours and patterns, it can be very difficult for breeders to predict what colour of kittens they will get from different parental pairings.

To help breeders with this problem, a previous project ("kitten calculator") allowed hobby breeders to enter the traits of two parents in order to calculate the likely traits of their offspring. The calculator, however, assumed that its users already know the basic terminology for feline colours. This assumption is not always correct - particularly for more complex phenotypes. This could mean that breeders enter incorrect information into the calculator and therefore perform matings which don't produce the expected kittens.

To assist breeders with this problem, this Cat Identifier provides a web portal that breeders can use to identify the phenotype of a cat from an image of the cat. The breeder just needs to upload a picture of their cat, and the Cat Identifier's machine learning technology will predict the colour and pattern of the cat, and whether it either tabby or pointed.

The tool also has wider applications for other types of users. For example, pet owners can use the Cat Identifier to find out more information about their pets. Similarly, the tool can be used to help identify lost or stray cats so they can be returned home.

![Preview of the breeder app of the Cat Identifier](documentation/wireframesdocumentation/am-i-responsive.png)

## Relationship to Kitten Calculator

Although this project can be seen as an extension of my [Kitten Calculator project](https://github.com/Laura10101/kitten-calculator) for the Code Institute, this Cat Identifier project is entirely new work. None of the functionality from that project has been reused for this project.

Other than this project offering entirely different functionality, the following technical differences are noted:

- The functionality for the Kitten Calculator was implemented entirely in JavaScript whereas the majority of the functionality for this project is implemeented in Python/Flask.
- The front-ends for this project use Materialize CSS for responsive layouts, whereas the Kitten Calculator used custom CSS and media queries.
- The Kitten Calculator was implemented as a single-page application with JavaScript and CSS used to change between views, whereas this project uses multiple pages.

To ensure some consistency in the look and feel of the two projects, the following imagery and styling was reused for this project:

- Cartoon images of cats to illustrate different phenotypes.
- CSS spinner used to indicate to users that work is happening in the background.
- Text effects on the Header.

These are a small part of this project and the vast majority of the JavaScript and CSS for this project is new work.

## Users
The primary purpose of this site is to enable people who aren't sure exactly what their British shorthair cat's phenotype is and need assistance identifying these traits. Users of this site will fall into two main groups:

- British shorthair breeders who need to know what traits their cat has so they can use this information to calculate kitten genetics.
- British shorthair cat owners who are curious to know what traits their cat has.

These users will want to be able to upload an image of their cat and have the site predict the traits the cat displays.

Because the site is powered by image recognition AI, I have targeted the site specifically at people with British shorthair cats older than 8 weeks old. This is to achieve reasonable accuracy. The AI models which power the site may be less accurate for younger kittens or other breeds.

Furthermore, a Model Administrator user will be responsible for using the site's administrative interfaces to train the machine learning model. I will assume that the Model Administrator is a trusted user and understands how to the train the model. I also assume they have an in-depth understanding of feline genetics. This user will need tools to allow them to provide training data to the model and to see reporting on the accuracy of the model.

## User Stories

### Cat Breeder or Owner Goals

- As a cat breeder or owner, I want to be able to upload a photo of my cat, so that I can find out what phenotype my cat is 
- As a cat breeder or owner, I want to see that my results are being calculated, so that I know the application is still working 
- As a cat breeder or owner, I want to see how the application has classified my cat's photo, so that I can identify what phenotype my cat has 

### Model Administrator Goals

- As a model administrator, I want to get feedback from the cat breeder or owner as to whether the predicted phenotype was correct or not, so that I can identify opportunities to improve the accuracy of the model 
- As a model administrator, I want to be able to easily upload a large number of training images, so that I have a set of relevant training data for the machine learning model 
- As a model administrator, I want to see that my training images are being uploaded, so that I know the application is still working correctly 
- As a model administrator, I want to be able to search Google images for relevant training data from within the application, so that I can find images with which to train the machine learning model 
- As a model administrator, I want to be able to select images to import as training data from the results returned by Google, so that I can import relevant images to my training data repository
- As a model administrator, I want to see that my selected training images are being imported, so that I know the application is still working correctly 
- As a model administrator, I want to be able to apply labels to training images in bulk, so that I can quickly and easily prepare clean data with which to train the machine learning model 
- As a model administrator, I want to see that my labels are being applied to my training data, so that I know the application is still working correctly
- As a model administrator, I want to be able to start the training process for new models, so that I can make trained models available for breeders and pet owners to use
- As a model administrator, I want to be able to check the current status of the training process, so that I can make sure the training process is working and review any errors that arise
- As a model administrator, I want to be able to delete training images, so that I can rebalance the training dataset if needed
- As a model administrator, I want to see reporting about the performance of the machine learning model, so that I can identify areas to improve accuracy
- As a model administrator, I want to see reporting about the size and contents of the training set, so that I can identify gaps or imbalances and correct these
- As a model administrator, I want to be able to delete reporting data, so that I can reset the statistics if needed

## UX

### Colour Scheme

To tie this project visually to the Kitten Calculator, the spinner from the Kitten Calculator was reused for this project. The colours from this spinner were used as the theme for this project to retain the desired consistency. However, the colours from this spinner did not allow for sufficient contrast to allow good accessibility when used as background colours. I therefore used a colour chooser to darken the shade.

### Typography

Ease of use was the primary consideration for the typography. For this reason, text was kept black, save for the header which is white with shading to make sure it is properly visible (the white header was more aesthetically pleasing on the header background). Arial was used as the primary font, with Helvetica as the web-safe font and Sans-sarif as a fallback font. This ensured that the typography was simple, familiar and easy to read so that users could navigate the application easily.

### Imagery
As this project has been developed as a potential extension of the Kitten Calculator, it was important for the imagery to remain consistent. The [Kitten Calculator README](https://github.com/Laura10101/kitten-calculator) aimed to provide ``users with a visual representation of the different cat traits...to make the application more intuitive for the target users``. The Cat Identifier replicates this feature by displaying a cartoon image to the user, alongside their prediction, to illustrate the predicted phenotype. These images are reused from the Kitten Calculator project to retain consistency.

Any other images displayed on the website is provided by the user as part of the functionality of this project. Given this, I decided to minimise the use of imagery in the design of the interface to allow users to focus fully on the application's functionality.

### Wireframes

__Features for Cat Breeders or Owners__

The wireframes for a breeder or owner to upload a photo of their cat is shown below:

![Uploading a photo of my cat](documentation/wireframes/landing-page.png)

![Selecting a photo of my cat](documentation/wireframes/upload-box.png)

The wireframe for a breeder or owner to see their results being calculated is shown below:

![Results being calculated](documentation/wireframes/calculating-result.png)

The wireframe for a breeder or owner to see the phenotype of their cat is shown below:

![Displaying predicted phenotype](documentation/wireframes/display-result.png)

__Features for Model Administrators__

The wireframes below show how a breeder or owner can provide the model administrator with feedback on their results:

![Asking breeder for feedback on their results](documentation/wireframes/display-result.png)

![Thanking user for their feedback](documentation/wireframes/feedback-thankyou.png)

The wireframe below shows how a model administrator can upload a Zip file containing training images:

![Selecting training images to upload](documentation/wireframes/upload-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that images are being uploaded:

![Uploading training images](documentation/wireframes/uploading-training-data.png)

The wireframe below shows how the model administrator can search Google Images from within the application:

![Searching Google Images for training data](documentation/wireframes/find-training-data.png)

The wireframe below shows how the model administrator can select training images to import from the Google Images search results:

![Selecting training images to import](documentation/wireframes/import-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that images are being imported:

![Importing training images](documentation/wireframes/importing-training-data.png)

The wireframe below shows how the model administrator can apply training labels to training images in bulk:

![Setting labels for training images](documentation/wireframes/label-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that image labels are being applied:

![Applying labels to training images](documentation/wireframes/labelling-training-data.png)

The wireframe below shows how the model administrator will see summary reports about the model's performance:

![Reports on model performance](documentation/wireframes/model-reporting.png)

## Data Model

### Choice of Database Technologies

The Cat Identifier fundamentally supports four main processes:

- Building and labelling a database of training images.
- Training machine learning models using the collated training data.
- Predicting information about unseen images provided by breeders or pet owners.
- Analytical processes on training and prediction data.

To enable these processes, the Cat Identifier stores the following sets of data:

- Images (both training images and those provided by breeder or pet owner users).
- Metadata about images (labels and review statuses).
- Trained models (including model architecture and weights).
- Statistical snapshots for the data warehouse.

These datasets include a mix of structured and unstructured data and, as such, the Cat Identifier uses both relational and non-relational
databases to store its data. As discussed in the Code Institute's Masterclass on `Combining databases`, relational databases are a good
fit for structured data whereas non-relational databases work well for unstructured data.

Images comprise unstructured data because they vary in size and format. Similarly, models exported from Keras (the Python library used to build the Cat Identifier's machine learning model) are also unstructured. This is because the model data consists of a model architecture component represented as Json data, and of a set of weights represented as an n-dimensional array of weight values whose shape depends on the architecture of the neural network.

While it would be achievable to represent both images and models in a relational format, this would not be a good fit for the data for two reasons:

- Field of a table in a relational database are typically stored in a fixed size (e.g., small int, big int, or a given number of characters), so the field size needs to be set in line with the largest expected value. Where actual values can vary significantly in size, this leads to significant wasted storage capacity. Non-relational databases do not restrict the shape or size of data in this way so reduce wasted storage.
- In the case of model configuration in particular, the format in which the data is required for processing by the Keras library is very different to the relational format, so expensive data transformations would be required to write model data to or read it from a relational database. By contrast, n-dimensional arrays can easily be converted to Json documents for storage in non-relational databases.

The metadata held by the application about images (both training images and user-provided images) is relational in its form. It would be relatively simple, therefore, to store the images in a non-relational database and the metadata in a relational database. However, this would require two database connections to be opened when accessing image data which is less efficient, so it is preferable to store the metadata as part of the image object. For this reason, the Cat Identifier also stores the metadata as part of the non-relational image schema.

By contrast, the statistical snapshots that make up the reporting database for the Cat Identifier are highly structured. Each snapshot consists of a set of pre-calculated metrics which are associated with a given set of reporting dimensions. This reduces the wait time for users when accessing reports. Because there is a finite number of snapshot types, and each snapshot type has a fixed set of statistics and filters which it contains, it can easily be stored in a structured relational form.

For these reasons, the Cat Identifier stores images, image metadata, and models in MongoDB, whereas it stores reporting data in Postgres.

### Non-relational Data Schema
The following diagram shows the schema for the MongoDB database collections.

![The MongoDB schema for the non-relational database](documentation/data-model/non-relational-schema.png)

The schema uses GridFS to store both images and also trained prediction models. GridFS is MongoDB's mechanism for storing large documents or binary data. Both image data and the trained models exceed MongoDB's limits for conventional objects and so GridFS was selected out of necessity.

GridFS system stores document data in chunks contained within the fs.chunks collection. Chunks are grouped together by file documents in the fs.files collection. This design is provided out-of-the-box when using GridFS.

Documents in the ``predictions`` collection represent images which have been uploaded by breeders or pet owners, and the labels that were predicted by the trained machine learning model for that image. These documents have the following attributes:

  - **image** is a foreign key to the GridFS file which holds the data for the uploaded image.
  - **label** is a nested document whose schema matches the predictions.label entity in the diagram above. These objects hold the values that were predicted for the uploaded image by the machine learning model.
  - **user_has_reviewed** indicates whether the user has so far provided feedback on the prediction.
  - **user_feedback** stores the feedback provided by the user (if any). It will be ``True`` if the user has accepted the prediction made by the Cat Identifier, and false otherwise (including if no feedback was provided).
  - **admin_has_reviewed** indicates whether the admin has provided any feedback on the prediction.
  - **admin_feedback** indicates whether the admin accepted or rejected the prediction made by the model.

Documents in the ``training_images`` collection represent images which have been uploaded or imported by model admins for the purpose of training the machine learning model. Although there are similarities between the schema of this collection and of the ``predictions`` collection, the two datasets serve very different purposes in the application so are stored separately. ``training_images`` attributes are:

  - **image** is a foreign key to the GridFS file which holds the data for the uploaded image.
  - **label** is a nested document whose schema matches the training_images.label entity in the diagram above. These objects hold the values that were manually selected for the associated training image by the model administrator. These values are used when training the machine learning model as the target output for the associated image.
  - **source** indicates where the training image comes from. Training images are created via a number of different features: by uploading a Zip file; by importing images from Google; or when the model administrator reviews the labels of previously-made predictions.
  - **is_labelled** is a flag to indicate whether the provided label is a default label, or whether it has been explicitly set by the model administrator. This is needed because the application will create a default label when storing training images. The default values for a label, however, may also be chosen by the model admin so it is not possible to tell from the label values alone whether the administrator has explicitly set the label.

Labels for both training images and predictions have the same schema. This is to be expected because they both represent outputs of the same machine learning model. The difference is that training image labels are fed to the machine learning model during training to indicate what the expected output for a training image should be. By contrast, the machine learning model is expected to predict the labels for prediction images without guidance, based on the training it has previously received. As such, labels for both predictions and training images have the following attributes:

  - **is_cat** indicates whether the image is of a cat or not. This is needed because it is not possible, without image recognition technology, to prevent breeders or pet owners from uploading images which are not of cats. The model, therefore, attempts to predict whether an image is or is not a cat. For training images, no other values should be set if this attribute is ``False``.
  - **colour** indicates the colour of the cat.
  - **is_tabby** indicates whether or not the cat is a tabby.
  - **pattern** indicates whether the cat is a self, bicolour, or van.
  - **is_pointed** indicates whether the cat is a colourpoint.

  The machine learning model is trained to predict these label attributes independently of one another, since these traits are not linked genetically.

Documents in the ``prediction_models`` collection contain the weights and configuration for trained machine learning models, allowing models to be stored and reloaded by the application. Attributes in this collection are:

  - **model** is a foreign key to the GridFS file containing the model configuration that was exported from Keras.
  - **weights** is a foreign key to the GridFS file containing the weights that were settled on during training for the model.
  - **loss** is the average loss value that was observed during training for this model.
  - **accuracy** is the average accuracy value that was observed during training for this model.
  - **training_started** is a timestamp indicating the date and time on which training for this model started.
  - **training_ended** is a timestamp indicating the date and time on which training for this model ended.
  - **is_active** indicates whether this is the currently-active model. Only one model can be active at any given time, and this is the model that will be used in the breeders' app to predict labels for user-uploaded images.

Documents in the ``users`` collection represent registered users of the admin app. Since the breeders' app is intended to be open for public use, users of this app do not need to sign in. However, administrators have significant control over the accuracy of trained models (based on their control over the training data). Therefore, admin app users do not to sign in. Attributes of a user are:

  - **username** is the name the user will use to login.
  - **password** is the password the user will use to login. This is hashed using the Werkzeug library.
  - **current_token** is a nested object holding the most recent authorisation token that was generated for that user. This feature is explained in the ``Security Features`` section of this README.

The attributes of a security token are:

  - **token** is the token string that the admin app will user to authorise users.
  - **expiry_time** is a timestamp indicating the point in time at which the token will cease to be valid.

Documents in the ``training_log_entries`` document represent log messages that are generated during the training process. Because training is a lengthy process which runs in the background, it is not possible to immediately confirm the final outcome of the process to administrators. The training log therefore holds messages generated during the training process giving insight into current progress and any errors that occurred. Attributes of training log entries are:

  - **timestamp** indicating the date and time at which the log entry was created.
  - **message** holds the contents of the log entry.

### Relational Data Schema

The following diagram shows the schema for the relational reporting database. This schema aims to store statistical information about the performance of trained machine learning models, the quality of predictions, and the contents of the training data. It is designed following the [Star schema approach](https://www.geeksforgeeks.org/designing-the-star-schema-in-data-warehousing/) which allows interesting statistics to be pre-calculated and grouped based on interesting dimensions which can be used to filter reporting in interesting ways.

![The MongoDB schema for the non-relational database](documentation/data-model/relational-schema.png)

The Star schema holds interesting metrics in Fact tables, while Dimensions describe what the metric relates to.

__Dimensional Tables__
For this project, the reporting database contains four dimensional tables. All dimensional tables have an autoincremented integer ``id`` field which is the primary key.

``dim_date`` is a date table which can be used to filter metrics based on various timestamps. Each date record has the following attributes:

  - ``date`` is the date that the date record corresponds to.
  - ``day_of_month`` is the integer value representing the day portion of the date.
  - ``month`` is the integer value representing the month portion of the date.
  - ``month_name`` is the string value representing the name of the month portion of the date.
  - ``year`` is the integer value representing the year portion of the date.

``dim_label`` is a dimensional table containing a list of all possible labels. Its attributes correspond to those of the training image and prediction labels in the non-relational schema, as follows:

    - ``is_unlabelled`` indicates whether a label has not yet been applied to a training image.
    - ``is_cat`` indicates whether the label is for a cat or not.
    - ``colour`` indicates the colour associated with this label.
    - ``is_tabby`` indicates whether the label is for a tabby cat or not.
    - ``pattern`` indicates the pattern associated with this label.
    - ``is_pointed`` indicates whether the label is for a colourpoint cat or not.

``dim_training_image_source`` is a dimensional table containing a list of all possible training image sources which indicate how the training image was obtained. The ``source`` field contains the string description of each image source.

``dim_prediction_review_status`` is a dimensional table containing a list of all possible review statuses for a prediction. These are the same for both admin reviews and user reviews. This dimensional table also combines the review status flags and the review value attributes from the non-relational schema. The ``status`` field contains the string description of each review status.

__Fact Tables__

The schema also contains three fact tables. Fact tables group interesting metrics by combinations of metrics, allowing an efficient process for filtering the metrics based on the available dimensions. The fact tables are intended to be updated daily (although at present they are updated at most once a day when an admin user accesses the dashboard page). Each update calculates the metrics for each fact table and for each permutation of available dimensions.

``fact_training_images_daily_snapshot`` contains metrics about the training images in the Mongo database. These snapshots are grouped by the snapshot date, the label applied to the training image, and the source of the training image. The metric is the number of training images in each dimensional grouping. This design allows the admin to evaluate the number of training images over time and by label. This is important tot he model admin since to maximise model accuracy it is important to have both a sizeable training set, and a balanced training set (i.e., approximately the same number of samples for each label). Attributes in this fact table are:

  - ``date_id`` is a foreign key to the ``dim_date`` table representing the date on which the snapshot was generated. This allows the admin to track trends over time.
  - ``label_id`` is a foreign key to the ``dim_label`` table representing the label for which the metric was calculated. This allows the admin to evaluate the number of images available for a given label.
  - ``source_id`` is a foreign key to the ``dim_training_image_source`` table, representing the source for which the metric was calculated.
  - ``count`` is the metric. This is the number of training images in the database matching the given label and source, on the given date.

``fact_models_daily_snapshot`` contains metrics about the trained models which allow the model admin to evaluate the performance **during training** of the models. This allows the model admin to determine whether the evolution of the training data set is improving or reducing model performance. Attributes are:

  - ``date_id`` is a foreign key to the ``dim_date`` table representing the date on which the snapshot was generated. This allows the admin to track trends over time.
  - ``training_started_date_id`` and ``training_ended_date_id`` are also foreign keys to the ``dim_date`` table, representing the date on which training for models in this group started or ended respectively. This allows alternative date dimensions that the model admin can use to track trends over time.
  - ``min_accuracy``, ``max_accuracy``, and ``avg_accuracy`` are metrics representing the minimum, maximum, and average accuracy of the models in the given date, training started date, and training ended date group. Accuracy is a metric which is captured during the training process and is used to evaluate performance. It indicates the proportion of false positives and false negatives predicted by the model as it undergoes training.
  - ``min_loss``, ``max_loss``, and ``avg_loss`` are metrics representing the minimum, maximum, and average loss of the model in the dimensional grouping. Loss is also captured during training of each model, and represents the gap during training between expected outputs and actual outputs of the model for a given sample.


``fact_predictions_daily_snapshot`` contains metrics about the predictions made by trained models and thus provide an alternative measure of model performance. Whereas the metrics in ``fact_models_daily_snapshot`` measure performance during training, the ``fact_predictions_daily_snapshot`` represents metrics about actual predictions made by trained models on user-provided images. This allows the admin to evaluate the actual performance of the model in the real-world. Attributes are:

  - ``date_id`` is a foreign key to the ``dim_date`` table representing the date on which the snapshot was generated. This allows the admin to track trends over time.
  - ``label_id`` is a foreign key to the ``dim_label`` table representing the label for which the metric was calculated. This allows the admin to evaluate the performance of the model on different labels.
  - ``user_review_status`` and ``admin_review_statis`` group the metric by the admin and user review statuses respectively. This allows the admin to filter by whether predictions were accepted, rejected, or not yet reviewed by either user group.
  - ``count`` is the metric representing the number of predictions in the dimensional grouping.

## Technical Design

### High-level Design

The following diagram provides a high-level overview of the structure of the Cat Identifier.

![High-level design of the Cat Identifier](documentation/architecture/high-level-design.png)

The project consists of three applications and four APIs. The APIs provide the functionality for the Cat Identifier, while the apps provide the user interfaces. The apps are implemented using HTML, CSS, JavaScript and Flask and communicate with the APIs via HTTP requests.

The apps are:

- The **Home app** is a simple landing page which allows users to choose whether they want to use the admin or breeder apps.
- The **Breeder app** is a public-facing app which allows pet owners or breeders to upload images of their cat and have the Cat Identifier predict the phenotype of their cat.
- The **Admin app** is a secure app which allows model administrators to build the training data set, label training images and manage the training process.

Each API manages a specific dataset as follows:

- The **Training Image API** manages the training data and the training process. It provides functionality to search Google for training images, import images from Google, upload images from a Zip file, label training images, and train models.
- The **Prediction API** manages the prediction data and process. It provides functionality to generate predictions based on images uploaded by users, and to allow both admins and users to review predictions.
- The **Analytics API** manages analytics data and provides functionality to analyse data resulting in snapshots, and to query snapshot data.
- The **User API** manages all user data and provides functionality for registering, authenticating, and authorising users.

### API Design

The APIs provide a significant amount of complex functionality and so structuring the code in line with good software design principles was important to ensure a clean codebase. In line with the [SOLID principles](https://en.wikipedia.org/wiki/SOLID), the code for each API has been separated into layers as follows:

- The **API Layer** handles validation of requests and determines which service function should be used to handle each request.
- The **Service Layer** orchestrates the end-to-end functionality for each operation provided by the API.
- The **Model Layer** provides the Python classes that represent the data for each API, and provide the key operations associated with that data.
- The **Data Layer** provides access to the underlying database, allowing model objects to be stored in or retrieved from the database underpinning the API.

### Technologies and Frameworks

The following libraries were used during development of this project.

__Front-end Technologies__

- HTML5
- CSS3
- JavaScript
- Materialize CSS is used as the main responsive layout framework for the application, as well as for providing a number of UI components (such as modals)
- Charts.JS is a JavaScript framework for building charts. This is used to implement the admin dashboards.

__Core Backend Technologies__

- Python 3
- Flask
- JSON is used for serialising and deserialising Python objects from and to JSON
- Base64 is used to convert image data into strings so it can be transmitted via HTTP requests
- Celery is used to allow the training process to run in a separate worker process, rather than in the API process  

__Security Features__

 - Werkzeug is used to handle password hashing
 - UUID is used to generate security tokens

__Data Access__

- Flask-SQLAlchemy is used to provide data access for the Postgres relational database
- PyMongo is used to provide data access for the MongoDB

__Data Preprocessing__

- Sklearn is used to split training data into training and testing input-output sets
- Numpy is used to manipulate the shape of training and test data
- Pillow is used to preprocess image data, ensuring a standard size and image format
- Keras Image Generators are used to apply normalisation to image data. This is a process which is important in machine learning. It ensures that numeric data falls within a normal range so that it can be consistently processed by the neural network.

__Machine Learning__

- Keras Sequential API is the high-level TensorFlow library for implementing neural networks

### Security Features

This project consists of two applications with different user groups. The ``Breeder app`` is targeted at breeders or pet owners and allows them to use trained machine learning models to find out the phenotype of their cat. The ``Admin app`` is targeted at administrators who are responsible for collating training data with which to train high-quality models.

The Breeder app is not secured because it is intended to be open to any public user.

The Admin app has the following security features:

  - Users must be added by an existing model admin.
  - Users are required to login using a username and password.
  - Passwords are hashed using the Werkzeug library both when the user is added to the database, and during the login process.
  - When a user logs in, a unique token is generated which the user can use thereafter to access features within the admin app. This is more seucre than simply using their username as a token, since the username can be guessed by attackers.
  - Tokens are regenerated each time the user accesses a feature, and expire after a fixed period of inactivity.

Both applications use bespoke APIs in the backend. API security has not yet been implemented which is a security gap that future development would address.

### The Training Process

Training a machine learning process is time consuming and may take several minutes to complete. In an initial version of this project, the training process was implemented directly inside the Training Images API. Howvever, testing resulted in timeouts occurring when using this approach.

After some research, I therefore decided to move the training process into a separate Celery task so that it can run in a separate process without the API having to wait for this process to complete.

This works as follows:

1. The admin app sends a request to the Training Image API to start the training process.
2. The Training Image API starts the training task in Celery. This posts a message onto a Redis queue for the Celery worker to handle.
3. The Training Image API then returns a response to the admin app to confirm training has started.
4. The Celery worker collects the message from Redis and runs the training process in response.
5. The training process posts updates on progress into the training_log_entries collection in the non-relational database.
6. The admin can check the status of training through the admin app which uses the Training Image API to access these log entries.

### The Machine Learning Model

The Machine Learning model used in this project was adapted from two articles on the [Towards Data Science](https://towardsdatascience.com/multi-label-image-classification-with-neural-network-keras-ddc1ab1afede) and [Machine Learning Mastery](https://machinelearningmastery.com/multi-label-classification-with-deep-learning/) websites respectively.

These articles use a popular form of neural network called a ``Convolutional Neural Network`` (CNN) which mimics the way in which the human eye scans images in phases, rather than observing an entire image at once. The input to a CNN is a 3-dimensional array, in which the first two dimensions represent the X and Y axes of the image respectively, and the third dimension is the Red-Green-Blue colour channel.

The architecture of the model is as follows:

- A simple convolutional input layer whose shape matches that of the input images. All images are resized to a standard shape during preprocessing.
- Three convolutional hidden layers. Hidden layers 1 and 3 both inlcude a max pooling layer, and add dropout. Dropout is a mechanism that is used to reduce overfitting by randomly switching a percentage of neurons off during each training batch. Max pooling is a mechanism for reducing the number of features contained within a data set, allowing the machine learning model to focus on features which are really important to the output.
- A prediction layer is needed before the output layer. This is because the input data is 3-dimensional as described above, whereas the output value is a 1-dimensional array representing the predicted value for each label attribute. The prediction layer firstly flattens the data, which reduces the 3-dimensional array into a 1-dimensional array. It then passes the flattened data through a fully-connected layer comprising 512 neurons. This is used to extract the most interesting information for predicting the output labels.
- Finally, the output layer consists of 1 neuron for each label attribute. Each neuron in this label will predict one of the corresponding output label attributes based on the output from the prediction layer.
- The activation function used through all input and hidden layers is ReLU which is a popular choice in most machine learning models. The activation function used for the output layer is sigmoid, which is ideal for multi-label classification problems (the type of machine learning problem that the Cat Identifier deals with).

## Features

### Existing Features

__Breeders can upload a cat photo__

To upload a cat photo, the breeder first selects the "Choose Image" button:

![Breeder journey to upload a cat image](documentation/screenshots/desktop/breeder-upload-1.png)

From here, the breeder now chooses the "Choose an Image File" button to bring up the file chooser:

![Breeder journey to upload a cat image](documentation/screenshots/desktop/breeder-upload-2.png)

Once selected, the breeder can preview their chosen image. They can either choose another image by repeating the process, or choose to upload the
image:

![Breeder journey to upload a cat image](documentation/screenshots/desktop/breeder-upload-3.png)

__Breeders can see their results are being calculated__

While the breeder's image is being uploaded, they will see a spinner dialog:

![Breeder journey to upload a cat image](documentation/screenshots/desktop/breeder-upload-4.png)

__Breeders can see the predicted phenotype for their image__

Once the prediction has been generated, the breeder can view their result. This consists of the predicted phenotype and a display showing their
original image and a cartoon image showing what the phenotype should look like:

![Breeder views their prediction](documentation/screenshots/desktop/breeder-results.png)

__Breeders can provide feedback on predictions for model administrators__

From this screen, the breeder can also choose to provide feedback on the prediction to indicate whether it is accurate or not:

![Breeder provides feedback](documentation/screenshots/desktop/breeder-feedback-1.png)

If the breeder provides feedback, they will see a ``thank you`` message:

![Breeder provides feedback](documentation/screenshots/desktop/breeder-feedback-2.png)

__Model admins can upload Zip files containing training images__

Admins can choose to upload Zip files containing training images. To do this, they first click the ``Choose a Zip File`` button as shown below:

![Admin uploads Zip file](documentation/screenshots/desktop/admin-upload-1.png)

Once they have chosen a file using the file chooser, they can then choose to upload that Zip file:

![Admin uploads Zip file](documentation/screenshots/desktop/admin-upload-3.png)

__Model admins can see when their Zip files are being uploaded__

The model admin will see a spinner to indicate that their file is being uploaded:

![Admin uploads Zip file](documentation/screenshots/desktop/admin-upload-4.png)

Once the upload is complete, they will see a display showing which files were successfully uploaded and which were ignored:

![Admin uploads Zip file](documentation/screenshots/desktop/admin-upload-5.png)

__Model admins can search Google images for relevant training images__

Model admins can also import training images from a Google search. To start this process, the admin enters a query string into the
search box and clicks the button:

![Admin imports training images](documentation/screenshots/desktop/admin-import-1.png)

The admin will see a spinner while the Cat Identifier searches Google Images:

![Admin imports training images](documentation/screenshots/desktop/admin-import-2.png)

Once the search is completed, the search results will be displayed to the admin:

![Admin imports training images](documentation/screenshots/desktop/admin-import-3.png)

__Model admins can select which images to import from Google__

The admin can then tick the check boxes under each image to choose which images they would like to import as training images. There is also a
checkbox to select all retrieved images:

![Admin imports training images](documentation/screenshots/desktop/admin-import-4.png)

__Model admins can see when their selected images are being imported__

The model admin will see a spinner while their chosen images are added to the training set:

![Admin imports training images](documentation/screenshots/desktop/admin-import-5.png)

The admin will see a confirmation screen once the import is complete:

![Admin imports training images](documentation/screenshots/desktop/admin-import-6.png)

__Model admins can apply labels to training images in bulk__

When the admin opts to label training images, they will see a page showing all unlabelled training images.

The admin specifies the label by indicating whether or not the images to label are of cats and if so whether the cats are tabby, are colourpoint,
and the colour and pattern of the cat.

The admin can also filter this screen based on the search term that was used to import the training images. This can make it easier to label images
in bulk since the source query acts as an informal label on the image.

![Admin labels training images](documentation/screenshots/desktop/label-images-1.png)

Once the label has been set, the admin chooses which images to apply the label to:

![Admin labels training images](documentation/screenshots/desktop/label-images-2.png)

Next, the admin clicks the ``Apply`` button.

![Admin labels training images](documentation/screenshots/desktop/label-images-3.png)

__Model admins can see when their labels are being applied to training images__

The admin will see a spinner while the images are being labelled:

![Admin labels training images](documentation/screenshots/desktop/label-images-4.png)

Once the label has been applied, the admin will see a confirmation screen:

![Admin labels training images](documentation/screenshots/desktop/label-images-5.png)

__Model admins can start the training process for new models__

To start the training process, the admin just needs to press the ``Start`` button from the ``Start model training`` page:

![Admin starts training](documentation/screenshots/desktop/start-training-1.png)

The admin will then be taken to the ``Check training status`` page automatically, which should confirm that training is underway:

![Admin starts training](documentation/screenshots/desktop/start-training-2.png)

__Model admins can check the current status of the training process__

The admin does not need to remain on the ``Check training status`` page for the training process to complete, since training runs as a background
task. However, the admin can return to this page at any point to check the current status of training:

![Admin checks training status](documentation/screenshots/desktop/check-training-status.png)

__Model admins can delete training images__

Sometimes, the admin may decide that some or all of the remaining training images are not required. The admin therefore has a tool to bulk delete
images matching a specific label query. To do this, the admin selects the label attributes which images to be deleted should match:

![Admin deletes images](documentation/screenshots/desktop/delete-images-1.png)

The Cat Identifier will confirm the result of the delete to the admin once complete:

![Admin deletes images](documentation/screenshots/desktop/delete-images-2.png)


__Model admins can view reporting on the performance of the machine learning model__

On the ``Dashboards`` page, the admin can view reporting about the performance of trained models:

![Model performance reports](documentation/screenshots/desktop/model-performance-report.png)

Two charts are available:

- The first chart shows the performance of models during training and how this has changed over time.
- The second chart shows the acceptance rate for predictions based on admin and user feedback over time.

These charts collectively allow the admin to evaluate how effective the machine learning model is.

__Model admins can view reporting about the training set__

Model admins can also view reporting about the training set:

![Training image reports](documentation/screenshots/desktop/training-image-reporting.png)

Two charts are available:

- The first chart simply shows the number of training images in the training set over time.
- The second chart can be filtered by label attributes and shows the ratio of training images matching the different values for each label attribute.
For example, in the image above, the admin can see that the majority of training images are labelled but are for the ``self`` pattern. No training images for ``bicolours`` have yet been imported, and very few ``van`` images have been imported. The training set is therefore not balanced for this
attribute.

__Model admins can delete reporting data__

Finally, admins can delete reporting data. This may be desirable if, for example, the admin decides to have a complete reset of the training process.

The admin first chooses which dashboards to clear:

![Admin clears dashboards](documentation/screenshots/desktop/clear-dashboards-1.png)

The admin will then see a confirmation page indicating the outcome of the process:

![Admin clears dashboards](documentation/screenshots/desktop/clear-dashboards-2.png)

### Features Left to Implement

In the future, the following additional features would add value to the site for users:

- Access to the application's APIs is not currently secured so any user can read or write to or from any API. Future work would add authentication and authorisation to the APIs.
- Currently, the reporting database is only refreshed when an admin user accesses the dashboard page (if the refresh hasn't already happened that day). Future work would move this update process into a Celery task which runs on a schedule.
- The machine learning model requires that all images are the same shape and size (both when training and when making predictions). Currently, the application achieves this by resizing all training images to the same size which can lead to the images being stretched. The application also displays the stretched version of the image to users. Future work would look at approaches to resizing the image without stretching (for example, by cropping or padding the image with a border to maintain the original aspect ratio).
- The Cat Identifier currently only accepts .png or .jpeg images. Future work would add support for additional image types.
- Future work would also add filters to the dashboards, allowing users to explore data in more detail.
- The reporting data on training images currently includes unlabelled images. Since image labels default boolean label attributes (`is cat`, `is tabby`, `is pointed`) to False when generating the snapshots, the inclusion of unlabelled images skews the statistics and gives the impression of imbalances. Further work would therefore exclude unlabelled images from the reporting.
- Although users are able to provide feedback on predictions, the tools available to model admins in the current version of the Cat Identifier do not make much use of this feedback. Future work would, for example, allow model admins to filter predictions based on the user feedback provided when they review these predictions.
- Currently, the image search feature only returns a limited number of results from Google. Future work would add pagination to this page to allow the admin to browse through more search results for each term.
- Currently, the admin can only bulk delete training images based on label queries. Future work would offer a tool that allows admins to select
specific images to delete.

## Testing 

For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The live deployed application can be found at [Cat Identifier](https://cat-identifier.herokuapp.com/).

### Heroku

This project uses [Heroku](https://www.heroku.com), a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Deployment steps are as follows, after account setup:

- Select *New* in the top-right corner of your Heroku Dashboard, and select *Create new app* from the dropdown menu.
- Your app name must be unique, and then choose a region closest to you (EU or USA), and finally, select *Create App*.
- From the new app *Settings*, click *Reveal Config Vars*, and set the following key/value pairs:
  - `IP` 0.0.0.0
  - `PORT` 5000
  - `MONGO_URI` mongodb+srv://service:MpWP0OA5n4AMQbop@catidentifier.1ncucur.mongodb.net/?retryWrites=true&w=majority. To get the `MONGO_URI`, follow the steps outlined in the `MongoDB` section below.
  - `API_BASE_URL` https://cat-identifier.herokuapp.com/api
  - `CONFIG_FILE` ./config/config.production.json
  - `DATABASE_URL` postgres://ckqznidqkqgwsd:ee305d223a8b55f882c85661ee97a51edebf35f2dbbe67e69f3ee945a0dcfd17@ec2-46-51-187-237.eu-west-1.compute.amazonaws.com:5432/decv568a62lsdl. To get the `DATABASE_URL`, follow the steps outlined in the `Postgres DB` section below.
  - `DEBUG` False
  - `MONGO_DB` cat_identifier_db
  - `MONGO_PREDICTION_MODELS` prediction_models
  - `MONGO_PREDICTIONS` predictions
  - `MONGO_TRAINING_IMAGES` training_images
  - `MONGO_TRAINING_LOG` training_log_entries
  - `MONGO_USERS` users
  - `REDIS_URL` redis://:p8c4e2560b7ef8b787c0ff47764b61e7bf661c867be93323b0a1b98c36f775ace@ec2-52-19-136-205.eu-west-1.compute.amazonaws.com:10839. To get the `REDIS_URL`, follow the steps outlined in the `Redis` section below.
  - `SECRET_KEY` AYdrcRATjKGYa3LGGxvcm2nZ913DNTyC

Heroku needs two additional files in order to deploy properly.
- requirements.txt
- Procfile

You can install this project's requirements (where applicable) using: `pip3 install -r requirements.txt`. If you have your own packages that have been installed, then the requirements file needs updated using: `pip3 freeze --local > requirements.txt`

The Procfile can be created with the following command: `echo -e web: python app.py\nworker: celery -A worker.celery worker > Procfile`

For Heroku deployment, follow these steps to connect your GitHub repository to the newly created app:

Either:
- Connect Heroku and GitHub.
- Then select "Automatic Deployment" from the Heroku app.
- Click the _Deploy Branch_ button.

Or:
- In the Terminal/CLI, connect to Heroku using this command: `heroku login -i`
- Set the remote for Heroku: `heroku git:remote -a cat-identifier`
- After performing the standard Git `add`, `commit`, and `push` to GitHub, you can now type: `git push heroku main`

The frontend terminal should now be connected and deployed to Heroku.

### MongoDB

You will need to sign-up for a [MongoDB](https://www.mongodb.com/) account.

The name of the database on Mongo should be `cat_identifier_db`.

The collections needed for this project are called:

  - predictions
  - prediction_models
  - training_images
  - training_log_entries
  - users

Click on the cluster created for the project.

Click on the _Connect_ button.

Click _Connect Your Application_.

Copy the connection string and ensure to replace `<password>` with your own password.

Paste this string into the env.py file and also Heroku config var as the value for the `MONGO_URI` key.

### Postgres DB

This project uses Postgres DB as the relational database for the application's data warehouse.

Deployment steps to create the Postgres DB in Heroku are as follows:

- From your Heroku dashboard, select the `cat-identifier` app.
- Select the *Resources* tab at the top.
- Under the *Add-ons* section, search for `Postgres` and select *Heroku Postgres* from the drop-down box.
- Leave the *Plan name* as `Hobby Dev - Free` and click *Submit Order Form*.
- Heroku will automatically create the `DATABASE_URL` key and value in the config settings.

### Redis

Training machine learning models can be a lengthy process and doing this inside an HTTP request could cause timeout errors for users. 

Therefore, this project deploys the training process inside a Celery worker task. The start training API endpoint starts a Celery task
which performs the training process and writes the trained model to the database once complete.

The task runs inside a separate Celery worker dyno in Heroku. For the web process which hosts the API to communicate with the Celery task, a Redis database is used as the transport layer. A Redis database therefore needs to be created in Heroku.

Deployment steps to create the Redis DB in Heroku are as follows:

- From your Heroku dashboard, select the `cat-identifier` app.
- Select the *Resources* tab at the top.
- Under the *Add-ons* section, search for `Redis` and select *Heroku Data for Redis* from the drop-down box.
- Leave the *Plan name* as `Hobby Dev - Free` and click *Submit Order Form*.
- Heroku will automatically create the `REDIS_URL` key and value in the config settings.

### Local Deployment

*Gitpod* IDE was used to write the code for this project.

To make a local copy of this repository, you can clone the project by typing the follow into your IDE terminal:
- `git clone https://github.com/Laura10101/cat-identifier.git`

You can install this project's requirements (where applicable) using: `pip3 install -r requirements.txt`.

Create an `env.py` file, and add the following environment variables:

```python
import os

os.environ.setdefault("IP", "0.0.0.0")
os.environ.setdefault("PORT", "5000")
os.environ.setdefault("DEBUG", "True")
os.environ.setdefault("SECRET_KEY", "this can be any random secret key")
os.environ.setdefault("MONGO_URI", "insert your own MongoDB URI key here")
os.environ.setdefault("MONGO_DB", "insert your own MongoDB DB Name key here")
os.environ.setdefault("MONGO_PREDICTIONS", "predictions")
os.environ.setdefault("MONGO_PREDICTION_MODELS", "prediction_models")
os.environ.setdefault("MONGO_TRAINING_IMAGES", "training_images")
os.environ.setdefault("MONGO_TRAINING_LOG", "training_log_entries")
os.environ.setdefault("MONGO_USERS", "users")
os.environ.setdefault("DATABASE_URL", "insert your own Postgres DB URL key here")
os.environ.setdefault("REDIS_URL", "insert your own Redis URL key here")
os.environ.setdefault("API_BASE_URL", "insert your local API URL here")
os.environ.setdefault("CONFIG_FILE", "./config/config.development.json")
```

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Laura10101/cat-identifier)

## Credits

### Educational Resources

The following educational and community resources were used during the implementation of this site:

- W3 Schools
- Stack Overflow
- [Geeks fopr Geeks](https://www.geeksforgeeks.org/)
- [Data Science Mastery](https://www.datasciencemastery.org/)
- [Medium](https://medium.com/)
- [Towards Data Science](https://towardsdatascience.com/)
- [Hackers and Slackers on Flask Blueprints](https://hackersandslackers.com/flask-blueprints/)
- [JavaScript Tutorials](https://www.javascripttutorial.net)

Additionally, assistance was provided by my Code Institute tutor, and by the Code Institute Slack community.

### Code

Code libraries or snippets were used in whole or in part from the following sources:

- [Towards Data Science](https://towardsdatascience.com/multi-label-image-classification-with-neural-network-keras-ddc1ab1afede)
- [Machine Learning Mastery](https://machinelearningmastery.com/multi-label-classification-with-deep-learning/)
- [Avoiding circular references when declaring SQL Alchemy databases](https://stackoverflow.com/questions/22929839/circular-import-of-db-reference-using-flask-sqlalchemy-and-blueprints)
- [Resizing Base64 image using Pillow](https://stackoverflow.com/questions/61574724/how-to-resize-base64-encoded-image-in-python)
- [Converting images into numpy array](https://stackoverflow.com/questions/57318892/convert-base64-encoded-image-to-a-numpy-array)
- [Check that an image is valid](https://stackoverflow.com/questions/60186924/python-is-base64-data-a-valid-image)
- [Scape images from Google Images using Beautiful Soup](https://python.plainenglish.io/how-to-scrape-images-using-beautifulsoup4-in-python-e7a4ddb904b8)
- Tim Nelson's user authentication and login videos at CodeInstitute.com
- [Tutorial on Windows Onload Event](https://www.javascripttutorial.net/javascript-dom/javascript-onload/)
- [Check if a JavaScript function exists](https://bobbyhadz.com/blog/javascript-check-if-function-is-defined#:~:text=Use%20the%20typeof%20operator%20to,doesn%27t%20throw%20an%20error.)
- [Using Celery in Flask blueprints](https://stackoverflow.com/questions/59632556/importing-celery-in-flask-blueprints)
- [Fixing the "Relative imports require the package argument" issue](https://stackoverflow.com/questions/22172915/relative-imports-require-the-package-argument)
- [Factory pattern for Celery and Flask](https://flask.palletsprojects.com/en/2.2.x/patterns/celery/)
- [Adaptation of the Factory Pattern](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
- [Styling file inputs using Materialize](https://fireflysemantics.medium.com/styling-a-file-input-button-with-materialize-ad9dd5326038)
- [Patch the Materialize Select issue](https://github.com/Dogfalo/materialize/blob/v1-dev/js/select.js)


### Content

- The icons for the Home Page features section, in the Footer, and for the responsive hamburger menu were taken from [Font Awesome](https://fontawesome.com/)
- I personally created all other content on the site specifically for my Code Insitute projects.

### Media

The following resources were used during the creation of this application:

- Feraichi on Fiver, who I commissioned to produce the cat images for this project (they were bought with all rights, including rights for commercial use and I am the legal owner of them)
- Paint 3D, which I used to create some additional images that I had inadvertently missed off the original list

## Acknowledgements
I would like to thank the following people for their support in implementing this project:

- My mentor, Tim Nelson, for his help and guidance throughout.
- The Code Institute community on Slack for their helpful guidance.