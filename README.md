#pytchuka
A very simple http python mock server  

##Install
```
pip install pytchuka
```

##Run
Just type: `pytchuka 5001` to run on port 5001. In this mode every request return status code 200 and an empty body.

##Spec file format
The spec file is a JSON file with a array of "request" and "response" objects.
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
  
**--live** means live reload :'D