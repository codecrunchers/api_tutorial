# API Name: Test API

## API Root: http://88.80.185.224:5000/api/v1/
## API Content-Type: application/json

## Swagger docs available [here]([http://88.80.185.224:8080/#/default)

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

- Paginated list of all folders

```
/folders?per_page=1&page=2
```

Return all folders

#### Params
 - page: next page of paginated results, default 1
 - per_page: , optional defaults to 20
#### Request type 
GET
#### Response
All folders
- 200
```json
    {"status": [{"id": 1, "name": "dir 1"}, {"id": 2, "name": "dir 2"}]}
```

- Return a single folder
```
/folders/<folder_id>
```
#### Params
 - folder_id: id of folder to retrieve
#### Request type 
GET
#### Response
Single Folder
- 200
```json
    {"status": {"id": 1, "name": "dir 1"}}
```


### Errors

404 
Resource not found
