@echo off

echo curl -X GET http://localhost:5001/test/chris
REM ----------------------------------------
curl -X GET http://localhost:5001/test/chris
REM ----------------------------------------
echo.
echo.
echo curl -X GET http://localhost:5001/test/friend
REM -----------------------------------------
curl -X GET http://localhost:5001/test/friend
REM -----------------------------------------
echo.
echo.
echo curl -X GET http://localhost:5001/test?name=Nemo
REM --------------------------------------------
curl -X GET http://localhost:5001/test?name=Nemo
REM --------------------------------------------
echo.
echo.
echo curl -X GET http://localhost:5001/test?name=Goku
REM --------------------------------------------
curl -X GET http://localhost:5001/test?name=Goku
REM --------------------------------------------
echo.
echo.
echo curl -X POST http://localhost:5001/test
REM -----------------------------------
curl -X POST http://localhost:5001/test
REM -----------------------------------
echo.
echo.
echo curl -X POST http://localhost:5001/test -H "Content-Type: application/json" -d "{ \"name\": \"Lightning McQueen\" }"
REM ----------------------------------------------------------------------------------------------------------------
curl -X POST http://localhost:5001/test -H "Content-Type: application/json" -d "{ \"name\": \"Lightning McQueen\" }"
REM ----------------------------------------------------------------------------------------------------------------
echo.
echo.
echo curl -X POST http://localhost:5001/test -H "Content-Type: application/json" -d "{ \"name\": \"Emmanuelle\" }"
REM ---------------------------------------------------------------------------------------------------------
curl -X POST http://localhost:5001/test -H "Content-Type: application/json" -d "{ \"name\": \"Emmanuelle\" }"
REM ---------------------------------------------------------------------------------------------------------
echo.
echo.
echo curl -X POST http://localhost:5001/test -H "content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "myfile=@.\fake_file.txt"
REM -------------------------------------------------------------------------------------------------------------------------------------------------------
curl -X POST http://localhost:5001/test -H "content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "myfile=@.\fake_file.txt"
REM -------------------------------------------------------------------------------------------------------------------------------------------------------
echo.
echo.
REM -----
pause