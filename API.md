# API Name: Test API

## API Root: http://88.80.185.224:5000
## API Content-Type: application/json

### CREATE 
Create a new folder
#### Request type 
POST
#### Params
 - folder_name: 256 char string
#### Response
Newly created folder
- 200
```json
    {"status": {"id": 2, "name": "alan021939024"}}
```



### UPDATE
Updated folder details
#### Request type 
PUT
#### Params
 - folder_name: 256 char string
 - id: id of folder to update
#### Response
Updated folder
- 200
```json
    {"status": {"id": 2, "name": "new_name"}}
```

### DELETE
Remove a folder
#### Request type 
DELETE
#### Params
 - id: id of folder to update
#### Response
Deleted folder
- 200
```json
    {"status": {"id": 2, "name": "new_name"}}
```

### QUERY
Return all folders
#### Request type 
GET
#### Response
All folders
- 200
```json
    {"status": [{"id": 1, "name": "dir 1"}, {"id": 2, "name": "dir 2"}]}
```
