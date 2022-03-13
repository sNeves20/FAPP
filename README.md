# Financial Application

## Backend

The backend of this project is a Python API that is build uppon the [FastAPI](https://fastapi.tiangolo.com/). I chose this framework, instead of the traditional Flask or Django frameworks,  because of it's integration with the Pydantic module which allows for datatype validation.

### __<ins>ToDo</ins>__

 - [ ] Fix the *__stocks/brokers/addAccount__*. This currently adds a broker account in the database. This should be changed to be always needed the username and password to the broker each time we needed to account.

 -  


## Database

For storing data, I decided on using MongoDB. This is because the data that will be used will vary from user to user, one user may have only savings data, another one might have both savings and stock broker information

### Running the Application

To run the application we are using Docker and DockerCompose. 
In order to run the API, you can simply run the following command:
`docker-compose up app`
This will also run the __mongo__ container which is the database container that is being used for storing and accessing data.
