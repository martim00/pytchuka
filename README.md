# pytchuka #
A very simple http python mock server  

## Install ##
```
pip install pytchuka
```

## Run ##
Just type: `pytchuka 5001` to run on port 5001. In this mode, every request returns status code 200 and an empty body.

## Spec file format ##
The spec file is a JSON file with a array of objects { "request", "response" }.
```json
[
    {
        "request": {
            "url": "/test/sub-path",
            "method": "POST"
        },
        "response": {
            "status": 201,
            "body": {
                "hello": "world"
            }
        }
    }
]
```
Using pytchuka with a spec file:  
`pytchuka --spec ./data.json --live true 5001`  

**--live** means "live reload" :'D
## Request Data ##
The request is defined by **url**, **method**, **body**, **query_string** and **file_upload**.  
The url is the path of the endpoint.  
`/api/v1/endpoint` or using python regex (match) `api/v1/endpoint/*`  

The method is the HTTP method: `GET, POST, PUT, DELETE...`

The body is when you have cases with different returns based on body data (POST, PUT...) with the same url.
```json
[
    {
        "request": {
            "url": "/test/sub-path",
            "method": "POST",
            "body" : {
                "name": "Name1",
                "city": "Kansas"
            }
        },
        "response": {
            "status": 201,
            "body": {
                "greetings": "Hi Name1"
            }
        }
    },
    {
        "request": {
            "url": "/test/sub-path",
            "method": "POST",
            "body" : {
                "name": "Name2",
                "city": "*"
            }
        },
        "response": {
            "status": 201,
            "body": {
                "greetings": "Hi Name2"
            }
        }
    }
]
```
It's possible to accept any value for a field using "\*" as the value.
  
The query_string is the same idea of the body.

```json
[
    {
        "request": {
            "url": "/test/sub-path",
            "method": "GET",
            "query_string" : "name=Name1"
        },
        "response": {
            "status": 200,
            "body": {
                "greetings": "Hi Name1"
            }
        }
    },
    {
        "request": {
            "url": "/test/sub-path",
            "method": "GET",
            "query_string" : "name=Name2"
        },
        "response": {
            "status": 200,
            "body": {
                "greetings": "Hi Name2"
            }
        }
    }
]
```

The file_upload is a way to simulate the file upload :)  
**key** is the form-data key and the filename is the key data.    
```json
[
    {
        "request": {
            "url": "/test/sub-path",
            "method": "POST",
            "file_upload": {
                "key": "key name",
                "filename": "my personal file_tabajara"
            }
        },
        "response": {
            "status": 200,
            "body": {
                "greetings": "Hi Name1"
            }
        }
    }
]
```
## Response Data ##
The response data is defined only for the status code and the body data.
## Sample ##
Run pytchuka with the spec file in the sample folder. The `run.bat` is a example of calls for it using curl.