# Mizara
- [x] [Get] [Post] api/users/

  ```json
  {
      "first_name": "",
      "last_name": "",
      "username": "",
      "email": ""
  }
  ```

  


- [x] [Get] [Put] [Delete] api/users/<int:pk>/

    ```json
    {
        "first_name": "",
        "last_name": "",
        "username": "",
        "email": ""
    }
    ```

    

- [x] [Get] api/token/

- [x] [Post] api/upload/

    ```json
    {
        "nom": "file_name",
        "taille": os.path.getsize(file_path),
        "type_fichier": mime.from_file(file_path),
    }
    ```

    

- [x]   [Get] api/directories/<path:directory>/
        
        for filter the result , user api/directories/<path:directory>/?filter=name
        
        filter:
            -   name
            -   ext

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

- [x] [Get] api/download/<path:file_path>/,

- [x] [Get] api/disk
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