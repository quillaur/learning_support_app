# Available studies

In this repository, you can find the different study contents available in this app.

## Directory organisation
* The first level of subdirectories indicates the language in which the study has been written.
* The second level of subdirectories indicates the category in which each study belong.
* The third level contains the names of each available study for that category.

## Study composition
Inside each third level directory, there must be 2 files:
* content.json
* ressources.zip

The content.json file indicates the elements to display on each study pages.

The ressources.zip file contains all images referenced in the content.json file.

### Here is an exemple of what is inside the content.json file:
![alt text](content_example.png "Title")

If you wish to add an image to a page, simply put the name of that image in the proper field in the content.json file (not show in the above exemple). You do not need to specify the path to the ressources.zip file as it is implied by the architecture (and must followed as is).