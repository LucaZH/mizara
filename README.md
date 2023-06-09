# Mizara
- [x] [Get] [Post] api/users/

  ```json
  {
      "username": "",
      "email": "",
      "password":"",
  }
  ```

- [x] [Get] [Put] [Delete] api/users/<int:pk>/

    ```json
    {
        "username": "",
        "email": ""
    }
    ```

- [x] [Post] api/token/

    ```json
        {
            "username": "",
            "password": ""
        }
    ```

- [x] [Post] api/upload/ 

    ```json
    {
        "name": "file_name",
        "size": "file_size",
        "file_type ": "file_type",
    }
    ```

    

- [x]   [Get] api/directories/

    Parameters : 

    -   dir 
    -   filter

    Filter:

    -   name
        
    -   ext

    Example:
        api/directories/?dir=/home/rimuru/&?filter=ext
    
    Response :
    ```json
    {
        "directories": [],
        "files": [   
            {
            "file_name": "file_name",
            "file_size": "0.0 MB"
            },
        ]
    }
    ```

- [x] [Get] api/download/

    `header : "token": "ed53d1211ee261bbb1209530c69b5f4c19232c33" `

    `Parameters : file_path`

- [x] [Get] api/streaming/

    `header : "token": "ed53d1211ee261bbb1209530c69b5f4c19232c33" `

    `Parameters : file_path`

- [x] [Get] api/disk

    Response :
    ```json
    [   
        {
            "Device": "/dev/sda5",
            "Mountpoint": "/",
            "File systeme type": "ext4",
            "Total size": "113.99 GB",
            "Used": "71.17 GB",
            "Free": "36.99 GB",
            "Percentage Used": 65.8
        },
    ]
    ```

- [x] [Get] api/transfer/

    `header : "token": "ed53d1211ee261bbb1209530c69b5f4c19232c33" `

    Response :

    ```json
        [
            {
                "id": "id",
                "date": "date_now",
                "file_path": "file_path",
                "downloader": "user_id"
            },
        ]
    ```
- [x] [Get] api/sysinfo/

    ```json
        {
        "OS": "Linux-5.10.0-21-amd64-x86_64-with-glibc2.31",
        "Processor": "",
        "Pc-name": "dev",
        "machine": "x86_64"
        }
    ```