# Cat Identifier

Blah

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
- As a model administrator, I want to see reporting about the performance of the machine learning model, so that I can identify areas to improve accuracy

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

The wireframe for a breeder or owner to see their results being calculated is shown below:

The wireframe for a breeder or owner to see the phenotype of their cat is shown below:

__Features for Model Administrators__
The wireframes below show how a breeder or owner can provide the model administrator with feedback on their results:

The wireframe below shows how a model administrator can upload a Zip file containing training images:

The wireframe below shows how the application will confirm to the model administrator that images are being uploaded:

The wireframe below shows how the model administrator can search Google Images from within the application:

The wireframe below shows how the model administrator can select training images to import from the Google Images search results:

The wireframe below shows how the application will confirm to the model administrator that images are being imported:

The wireframe below shows how the model administrator can apply training labels to training images in bulk:

The wireframe below shows how the application will confirm to the model administrator that image labels are being applied:

The wireframe below shows how the model administrator will see summary reports about the model's performance:

## Features

### Existing Features
Blah


### Features Left to Implement

In the future, the following additional features would add value to the site for users:

- Blah

## Testing 

For all testing, please refer to the [TESTING.md](TESTING.md) file.

## Deployment

The site was deployed to GitHub pages. The steps to deploy are as follows: 
  - In the [GitHub repository](https://github.com/Laura10101/volanto-launchpad), navigate to the Settings tab 
  - From the source section drop-down menu, select the **Main** Branch, then click "Save".
  - The page will be automatically refreshed with a detailed ribbon display to indicate the successful deployment.

The live link can be found [here](https://laura10101.github.io/volanto-launchpad)

### Local Deployment

In order to make a local copy of this project, you can clone it. In your IDE Terminal, type the following command to clone my repository:

- `git clone https://github.com/Laura10101/volanto-launchpad.git`

Alternatively, if using Gitpod, you can click below to create your own workspace using this repository.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Laura10101/volanto-launchpad)

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
- I personally created all other content on the site specifically for the Volanto Launchpad project.

### Media

The following tools and sources were used to create the images on the site:

- I created the Header image specifically for the site using Canva.
- Testimonial portrait images were sourced from Snappa's stock images.
- I also used Colorzilla's Ultimate CSS Gradient Generator to create the background for the image.
- The glowing effect on links and buttons was adapted from an Instagram post by the [developers_community account](https://www.instagram.com/p/CXqjOWsARwC/?utm_medium=copy_link).

## Acknowledgements
I would like to thank the following people for their support in implementing this project:

- My mentor, Tim Nelson, for his help and guidance throughout.
- The Code Institute community on Slack for their helpful guidance.