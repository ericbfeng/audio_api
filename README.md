# deepgram
Simple Flask API to support the following methods:

1. POST raw audio data and store it. 

Eg: $ curl -X POST --data-binary @myfile.wav 

http://localhost/post 

2. GET a list of stored files, GET the content of stored files, and GET metadata of stored files, such as the duration of the audio. The GET endpoint(s) should accept a query parameter that allows the user to filter results. Results should be returned as JSON. 

Eg: $ curl http://localhost/download?name=myfile.wav 

Eg: $ curl http://localhost/list?maxduration=300 

Eg: $ curl http://localhost/info?name=myfile.wav 

