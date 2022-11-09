# Cat Identifier

British Shorthair cats are the most popular breed of cat in the UK. There is a large body of hobby breeders who enjoy raising kittens. However, feline genetics is a complicated area, and because the British Shorthair is available in a broad range of colours and patterns, it can be very difficult for breeders to predict what colour of kittens they will get from different parental pairings.

To help breeders with this problem, a previous project ("kitten calculator") allowed hobby breeders to enter the traits of two parents in order to calculate the likely traits of their offspring. The calculator, however, assumed that its users already know the basic terminology for feline colours. This assumption is not always correct - particularly for more complex phenotypes. This could mean that breeders enter incorrect information into the calculator and therefore perform matings which don't produce the expected kittens.

To assist breeders with this problem, this Cat Identifier provides a web portal that breeders can use to identify the phenotype of a cat from an image of the cat. The breeder just needs to upload a picture of their cat, and the Cat Identifier's machine learning technology will predict the colour and pattern of the cat, and whether it either tabby or pointed.

The tool also has wider applications for other types of users. For example, pet owners can use the Cat Identifier to find out more information about their pets. Similarly, the tool can be used to help identify lost or stray cats so they can be returned home.

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

Blah

### Typography

Blah

### Imagery
Blah

### Wireframes

__Features for Cat Breeders or Owners__

The wireframes for a breeder or owner to upload a photo of their cat is shown below:

![Uploading a photo of my cat](https://laura10101.github.io/cat-identifier/assets/img/wireframes/landing-page.png)

![Selecting a photo of my cat](https://laura10101.github.io/cat-identifier/assets/img/wireframes/upload-box.png)

The wireframe for a breeder or owner to see their results being calculated is shown below:

![Results being calculated](https://laura10101.github.io/cat-identifier/assets/img/wireframes/calculating-result.png)

The wireframe for a breeder or owner to see the phenotype of their cat is shown below:

![Displaying predicted phenotype](https://laura10101.github.io/cat-identifier/assets/img/wireframes/display-result.png)

__Features for Model Administrators__

The wireframes below show how a breeder or owner can provide the model administrator with feedback on their results:

![Asking breeder for feedback on their results](https://laura10101.github.io/cat-identifier/assets/img/wireframes/display-result.png)

![Thanking user for their feedback](https://laura10101.github.io/cat-identifier/assets/img/wireframes/feedback-thankyou.png)

The wireframe below shows how a model administrator can upload a Zip file containing training images:

![Selecting training images to upload](https://laura10101.github.io/cat-identifier/assets/img/wireframes/upload-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that images are being uploaded:

![Uploading training images](https://laura10101.github.io/cat-identifier/assets/img/wireframes/uploading-training-data.png)

The wireframe below shows how the model administrator can search Google Images from within the application:

![Searching Google Images for training data](https://laura10101.github.io/cat-identifier/assets/img/wireframes/find-training-data.png)

The wireframe below shows how the model administrator can select training images to import from the Google Images search results:

![Selecting training images to import](https://laura10101.github.io/cat-identifier/assets/img/wireframes/import-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that images are being imported:

![Importing training images](https://laura10101.github.io/cat-identifier/assets/img/wireframes/import-training-images.png)

The wireframe below shows how the model administrator can apply training labels to training images in bulk:

![Setting labels for training images](https://laura10101.github.io/cat-identifier/assets/img/wireframes/label-training-data.png)

The wireframe below shows how the application will confirm to the model administrator that image labels are being applied:

![Applying labels to training images](https://laura10101.github.io/cat-identifier/assets/img/wireframes/labelling-training-data.png)

The wireframe below shows how the model administrator will see summary reports about the model's performance:

![Reports on model performance](https://laura10101.github.io/cat-identifier/assets/img/wireframes/model-reporting.png)

## Features

### Existing Features
Blah


### Features Left to Implement

In the future, the following additional features would add value to the site for users:

- Blah

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
- CSS Tricks
- [HTML Living Standard](https://html.spec.whatwg.org/)

Additionally, assistance was provided by my Code Institute tutor, and by the Code Institute Slack community.

### Code

Code libraries or snippets were used in whole or in part from the following sources:

- [W3 Schools Responsive TopNav Example](https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_topnav)
- [W3 Schools How To - Glowing Text](https://www.w3schools.com/howto/howto_css_glowing_text.asp)
- [CSS Tricks - Sticky Footer, Five Ways](https://css-tricks.com/couple-takes-sticky-footer/)

### Content

- The icons for the Home Page features section, in the Footer, and for the responsive hamburger menu were taken from [Font Awesome](https://fontawesome.com/)
- I personally created all other content on the site specifically for my Code Insitute projects.

### Media

The following tools and sources were used to create the images on the site:

-

## Acknowledgements
I would like to thank the following people for their support in implementing this project:

- My mentor, Tim Nelson, for his help and guidance throughout.
- The Code Institute community on Slack for their helpful guidance.