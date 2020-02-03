# Project

This project demonstrates how to import and manage member data via a Django Rest Framework API.

Project is based on Docker containers and is equipped with build scripts that make the whole set up easy:

1. Build the docker images:
    ```
    make build
    ```
2. Start docker containers and start outputting the logs:
    ```
    make && make logs
    ```

3. The application will be available under:
    ```
    http://127.0.0.1:8000/
    ```
4. You can stop the whole app with:
    ```
    make stop
    ```
    You can also remove all containers/images/vendor assets with:
    ```
    make purge-all
    ```
---
# API Endpoints

API can be accessed via `http://localhost:8000/api/v1/` URL, available endpoints:

## /api/v1/members/list/

Creates Member, related Account is automatically created for integrity purposes
```
curl -X POST \
  http://127.0.0.1:8000/api/v1/members/list/ \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 124,
    "first_name": "Bob",
    "last_name": "Dylan",
    "phone_number": "+48 100 000 000",
    "client_member_id": 11,
    "account_id": 2
}'
```

Response:
```json
{
  "id": 124,
  "first_name": "Bob",
  "last_name": "Dylan",
  "phone_number": "+48 100 000 000",
  "account_id": 2,
  "client_member_id": 11
}
```
  
## /api/v1/members/list/

Fetch all Members
```
curl -X GET \
  http://127.0.0.1:8000/api/v1/members/list/
```

Response:
```json
[
  {
    "id": 50,
    "first_name": "Thedric",
    "last_name": "O'Daly",
    "phone_number": "6671953131",
    "account_id": 9,
    "client_member_id": 5098379
  },
  {
    "id": 123,
    "first_name": "Bob",
    "last_name": "Dylan",
    "phone_number": "+48 100 000 000",
    "account_id": 2,
    "client_member_id": 11
  }
]
```
  
## /api/v1/members/by-phone/<PHONE_NUMBER>/

Get Member by phone number
```
curl -X GET \
  'http://127.0.0.1:8000/api/v1/members/by-phone/+48%20100%20000%20000/'
```

Reponse:
```json
{
  "id": 123,
  "first_name": "Bob",
  "last_name": "Dylan",
  "phone_number": "+48 100 000 000",
  "account_id": 122,
  "client_member_id": 11
}
```
  
## /api/v1/members/by-id/<ID>/

Get Member by ID
```
curl -X GET \
  'http://127.0.0.1:8000/api/v1/members/by-id/123/'
```

Reponse:
```json
{
  "id": 123,
  "first_name": "Bob",
  "last_name": "Dylan",
  "phone_number": "+48 100 000 000",
  "account_id": 122,
  "client_member_id": 11
}
```
  
## /api/v1/members/by-mrn/<MRN>/

Get Member by Medical Record Number (MRN)
```
curl -X GET \
  'http://127.0.0.1:8000/api/v1/members/by-mrn/11/'
```

Reponse:
```json
{
  "id": 123,
  "first_name": "Bob",
  "last_name": "Dylan",
  "phone_number": "+48 100 000 000",
  "account_id": 122,
  "client_member_id": 11
}
```
  
## /api/v1/members/bulk-create/

Upload members via CSV file, This is volume-optimized endpoint, Member creation is done in batches, 
failures are listed as `failed_ids` and `failed` entries.

Note: **This endpoint has some bugs, it's a demo of the concept.**

More can be found in `mpulsedemo/members/serializers.py` and `mpulsedemo/members/views.py`.

The idea is that the uniqueness is enforced on DB level, inserts are done via chunks in transactions to speed up 
the process and reduce amount of queries. Transactions are not broken on insert failures via `INSERT IGNORE` 
statement. Failed entries are discovered post-hoc, to be presented in `failed_ids` and `failed`. 
This can be heavily fine-tuned but requires some work on `bulk_insert` method.
```
curl -X POST \
  http://127.0.0.1:8000/api/v1/members/bulk-create/ \
  -H 'Content-Length: 2281' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F 'csv_file=@/Users/rootx/Dropbox/Projects/mPulse Mobile/member_data_with_duplicate_records.csv'
```

Reponse:
```json
[
  [
    "success",
    [
      {
        "id": 1,
        "first_name": "Yank",
        "last_name": "Deboo",
        "phone_number": "1284628753",
        "account_id": "12",
        "client_member_id": 7228138
      },
      {
        "id": 2,
        "first_name": "Gennie",
        "last_name": "O'Heffernan",
        "phone_number": "2642745297",
        "account_id": "5",
        "client_member_id": 7228138
      },
      [...]
    ]
  ],
  [
    "failed_ids",
    [
      1,
      2,
      [...]
    ]
  ],
  [
    "failed",
    [
      {
        "first_name": "Yank",
        "last_name": "Deboo",
        "phone_number": "1284628753",
        "client_member_id": "7228138",
        "account_id": "12",
        "id": "1"
      },
      {
        "first_name": "Gennie",
        "last_name": "O'Heffernan",
        "phone_number": "2642745297",
        "client_member_id": "7228138",
        "account_id": "5",
        "id": "2"
      },
      [...],
    ]
  ]
]
```
  

## /api/v1/accounts/<ACCOUNT_ID>/member-list/

Get list of members for given account
```
curl -X GET \
  'http://127.0.0.1:8000/api/v1/accounts/1/member-list/'
```

Reponse:
```json
[
  {
    "id": 25,
    "first_name": "Jae",
    "last_name": "Everill",
    "phone_number": "6671953131",
    "account_id": 1,
    "client_member_id": 5300438
  },
  {
    "id": 40,
    "first_name": "Kala",
    "last_name": "Kensley",
    "phone_number": "6043528866",
    "account_id": 1,
    "client_member_id": 3762881
  },
  [...]
]
```


## /api/v1/accounts/list/

Get list of accounts
```
curl -X GET \
  'http://127.0.0.1:8000/api/v1/accounts/list/'
```

Reponse:
```json
[
  {
    "id": 12,
    "date_added": "2020-02-02T01:32:10.829176Z",
    "date_updated": "2020-02-02T01:32:10.829215Z"
  },
  {
    "id": 5,
    "date_added": "2020-02-02T01:32:10.829241Z",
    "date_updated": "2020-02-02T01:32:10.829258Z"
  },
  [...]
]
```
    
