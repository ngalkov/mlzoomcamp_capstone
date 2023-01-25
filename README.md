# Quality Prediction in a Mining Process
## Overview

This project is a part of the [Machine Learning Zoomcamp course](https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp) held by [DataTalks.Club](https://datatalks.club/).

This project covers some areas of machine learning and building web services. Тhe following were conducted:
- data exploration, 
- development of a regression model 
- building of a web service
- containerization
- cloud deployment

⚠️❗ **This project is for educational purposes only and cannot be used in practice** ❗⚠️

## Problem description

One of the most important parts of a mining process is a flotation.

In the extraction of metals from their ores, the process of mineral flotation plays a most important role. Flotation provides the means of separating and concentrating the valuable components of an ore to produce a grade of mineral concentrate suitable for feeding to efficient pyrometallurgical or hydrometallurgical operations. 

The flotation process involves crushing the ore to liberate separate grains of the various valuable minerals and gangue components, pulping the ore particles with water, and then selectively rendering hydrophobic the surface of the mineral of interest. A stream of air bubbles is then passed through the pulp; the bubbles attach to and levitate the hydrophobic particles, which collect in a froth layer which flows over the weir of the flotation cell.

The main goal of the project is to predict how much impurity is in the ore concentrate. If we can predict how much silica (impurity) is in the ore concentrate, we can help the engineers, giving them early information to take actions (empowering!). Hence, they will be able to take corrective actions in advance (reduce impurity, if it is the case) and also help the environment (reducing the amount of ore that goes to tailings as you reduce silica in the ore concentrate).

## Data
Dataset from:  
[Quality Prediction in a Mining Process](https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process)

The first column shows time and date range.

The second and third columns are quality measures of the iron ore pulp right before it is fed into the flotation plant. Column 4 until column 8 are the most important variables that impact in the ore quality in the end of the process. From column 9 until column 22, we can see process data (level and air flow inside the flotation columns, which also impact in ore quality. 

The last two columns are the final iron ore pulp quality measurement from the lab.

Target is to predict the last column, which is the % of silica in the iron ore concentrate.

## Project structure
The project structure loosely follows [Cookiecutter Data Science project template](https://drivendata.github.io/cookiecutter-data-science/).

    |---data
    |   |---archive.zip         <- dataset
    |
    |---models
    |   |---model.bin           <- model, saved as Python object
    |
    |---notebooks
    |   |---notebook.ipynb      <- EDA, model selection
    |
    |---tests
    |   |---test_service.py     <- test files
    |   |---sample.json 
    |
    |---train.py                <- training final model
    |
    |---service.py              <- application code
    |
    |---bentofile.yaml          <- BentoML configuration file
    |
    |---README.md               <- project description
    |
    |---Pipfile                 <- pipenv files
    |---Pipfile.lock

## Setup
All of the following instructions apply to the Windows system (without WSL). There may be some differences on other systems.

The project can be used in two ways:
- development - if you want to reproduce all exploration steps (EDA, feature selection, etc...)
- production - if you want to use it as a service.

### Setup Prerequisites
 - Python 3.9 or above
 - Pipenv
 - Docker (in case you want to run service as a Docker container)

 If you do not have any of these, please follow the respective guides:
  - [Python Installation](https://docs.python.org/3/using/index.html)
  - [Popenv Installation](https://github.com/pypa/pipenv#installation)
  - [Docker Installation](https://docs.docker.com/engine/install/)

### Set up local environment

To install this project locally, follow the steps below:
 - Create a new folder and navigate to it.
 - Clone the project repository  
     ```
    git clone https://github.com/ngalkov/mlzoomcamp_capstone
    ```
 - Create the new virtual environment:  
   for development (this will install both development and production dependencies)
     ```
    pipenv install --dev
    ```
   for production (this will install production dependencies only)
     ```
    pipenv install --ignore-pipfile
    ```
  - Downliad the [dataset](https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process/download?datasetVersionNumber=1) and put it into `./data` folder. It should have a name`./data/archive.zip.`
 - Activate virtual environment
      ```
    pipenv shell
    ```
    Alternatively you can run a command in the virtual environment without launching a shell:
    ```
    pipenv run <insert command here>
    ```

That's all! Now you can easily run the scripts and notebooks.

## Usage

### Data processing, EDA, models (development environment only)

Run `./noteboks/notebook.ipynb`

### Training the model (development environment only)

The project already contains a trained model, saved as Python object - `./models/model.bin`.

The model can be retrained. Run the training script
```
pipenv run python train.py
```
There should be a dataset `./data/archive.zip`.  
Script retrain the model with this dataset and saves the model as Python object into `./models/model.bin` and BentoML model into your BentoML folder (probably `~/bentoml`) under the name `ore_impurity_model`.

### Run as a service
To run the service locally, do the following:
 - Navigate to the project directory.
 - Start virtual environment
    ```
    pipenv shell
    ```
 - Build a Bento.
    ```
    bentoml build
    ```
 - Run the service locally
    ```
    bentoml serve ore_impurity_predictor:latest --production
    ```

The service should start on port 3000.  
BentoML API will be available at this address: http://127.0.0.1:3000

You can send a POST request to the address  
`127.0.0.1:3000/predict`  
The body of the request must contain a json of the form  
```[17.81, 4953.84, 558.973, 379.3315, 9.01614, 1.72614, 301.588, 302.132, 298.6339053905, 299.9169904186, 364.879, 305.5358, 599.92, 592.876, 605.694, 342.334, 350.036, 507.038, 354.79]```  
An example of such a json is in `./tests/sample.json`

Service returns a json of the form   
`{"impurity": 1.5428869724273682}`

You can use a testing script to make sure the service is working. See [Testing](##Testing) section.

To exit virtual environment run:  
```
exit
```

## Containerization
Alternatively you can run service as a Docker container. A docker image can be automatically generated from a Bento for production deployment.

To build an image and run a container on your local machine do the following:
 - Navigate to the project directory.
 - Build docker image
    ```
    bentoml containerize ore_impurity_predictor:latest
    ```
 - run a Docker container with your app
    ```
    docker run -it --rm -p 3000:3000 ngalkov/ore_impurity_predictor:latest serve --production
    ```
Instead of building an image by yourself, you can pull it out an already built from Dockerhub. Use the command 
```
docker pull ngalkov/ore_impurity_predictor
```

## Testing
The service can be tested with a testing script. Run
```
pipenv run python ./tests/test_service.py http://127.0.0.1:3000/predict
```
The script sends a request to the service and prints the response to the console.

Alternatively you can use BentoML API at http://127.0.0.1:3000

## Cloud deployment 
We will use [Yandex Cloud](https://cloud.yandex.com) for cloud deployment.

Do the following:  
1. log in to Yandex Cloud
2. Create a virtual machine: **All services - Compute Cloud - Create VM**.  
   Leave all parameters at their defaults. Fill **Login** field with your username. Put your public SSH key into **SSH key** field.
3. Log in with ssh into VM.
4. Install Docker into VM.  
   ([Docker Installation](https://docs.docker.com/engine/install/))
5. run a Docker container with the app
    ```
    docker run -it --rm -p 3000:3000 ngalkov/ore_impurity_predictor:latest serve --production
    ```
The service should start on port 3000.

## Production service
There is a working service deployed in the Yandex Cloud.  
You can access BentoML API at http://51.250.109.233:3000

To use the service send POST request to http://51.250.109.233:3000/predict 
(as in [Run as a service](###Runasaservice) section)

The service can be tested with a testing script. Run
```
pipenv run python ./tests/test_service.py http://51.250.109.233:3000/predict
```
The script sends a request to the service and prints the response to the console.
