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

- [x] [Post] api/upload/ (file path in a file content in )

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

    `Parameters : file_path`

- [x] [Get] api/streaming/

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