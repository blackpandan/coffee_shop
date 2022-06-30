# **COFFEE API**

## **Introduction**
---

this is an api that was created during udacity nano degreee for the purpose of managing drinks with users, authentication is done using auth0. it was created with python flask following [pep8 guideline](https://peps.python.org/pep-0008/) 

---
## **Getting Started**
---

### **Base Url**

Due to the fact the API is still in development the base url is:
```bash
localhost:5000/
```

### **Api Keys / Authentication**

authentication is done using bearer method with jwt tokens from auth0 sent in the header 

---
## **Error**
---

this project handles errors and success by using the traditional http response codes

1.   ```2xx``` codes indicates successful responses

2. ```4xx``` codes indicates errors from client

below are the list of the codes return and their meaning

- ```200``` : this indicates that the request was succesful sample response provided below


- ```400```: this error occurs when the server will not process the request due to missing headers or data 

    

- ```404```: this error is returned when the question, category or route requested was not found

- ```405```: errors with this code occurs when the method used in the request was not accepted.

- ```406```: This error happens when a request is rejected due to missing or incorrect parameters.


 sample responses for success and errors

- sucess 
    ```json
    {
      "drinks": [
          {
              "id": 2,
              "recipe": [
                  {
                      "color": "blue",
                      "parts": 1
                  }
              ],
              "title": "Water0"
          }
      ],
      "success": true
    }
    ```

- error
    ```json
    {
        "error":404,
        "sucess":false,
        "message":"Not Found",
    }
    ```

---
## **Resource Endpoint Library**
---

## Drinks - ```{baseUrl}/drinks```

this enpoint handles all processes for reading, creating, deleting and updating drinks.

- **Retrieve all Drinks**: in order to retrieve drinks a get request is sent to this endpoint with the authentication ```token``` and a ```page``` number, ```page``` size is 10 drinks per page, default is 1.

    ```
    GET {baseUrl}/drinks
    ```

    sample response:

    ```json
    {
        "drinks": [
            {
            "id": 2,
            "recipe": [
                {
                "color": "blue",
                "parts": 1
                }
            ],
            "title": "Water0"
            }
        ],
        "success": true
    }
    ```

    an ```array``` of ```drinks``` and a ```status``` attribute containing a ```boolean``` which represent the state of sucess is returned. 


- **Retrieving Individual Drink Detail**: in order to retrive the details of a specific drink, a get request is sent to this endpoint with the ```id``` of the drink as a url parameter

    ```
    GET {baseUrl}/drinks/{id}
    ```

    it return a ```drink``` ```array``` and a ```success``` property.


- **Retrieving All Drinks With More Details**: in order to retrieve the full version of all drinks, a get request is sent to this endpoint with a ```page``` parameter in the url.

    ```
    GET {baseUrl}/drinks-detail
    ```

    on successful execution it return a reponse containing an ```array``` of drinks, and a ```success``` boolean attribute.


- **Deleting Drinks**: this endpoint is provided to delete drinks by ```id```, it accepts a get request and the ```id``` of the drink in the url.

    ```
    GET {baseUrl}/drinks/{id} 
    ```

    it returns a json response that contains the ```id``` of the deleted drink


-  **Creating Drinks**: the api provides this enpoint which accepts certain paramters and adds a new ```drink``` to the database, the mothod used is POST.

    parameters:

    - title - ```required```: this is a ```String``` that represents the title of the drink.

    - recipe - ```required```: this is an ```array``` of ```objects``` that represent the recipe to make the ```drink```, each object in the array must contain ```color, name, parts```

    ```
    POST {baseUrl}/drinks
    ```

