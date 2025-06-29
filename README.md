# fastapi-crud-file-demo
FastAPI Demo of a workshop I facilitated to teach my learners RESTful API using FastAPI for CRUD operations, forms, file uploads and downloads. 

## Contacts
- `Adedoyin Simeon Adeyemi` | [LinkedIn](https://www.linkedin.com/in/adedoyin-adeyemi-a7827b160/)

## Concepts

- CRUD operations
- Posting and Accepting Form data
- File Uploading and saving
- File Downloading
- Simple basic Authentication (Password hashing not implemented for simplicity)

## Tools

- FastAPI - Backend Framework.
- uvicorn - Dev Server for FastAPI
- Python-mulitpart - File upload/download

## Setup

- Install uv package manager
```bash
$ make install-uv
```

- Create virtual environment
```bash
$ make venv
```

- Activate the virtual environment
    - MacOs / Unix Systems (terminal)
    ```bash
    $ source .venv/bin/activate
    ```

    - Windows (Command Prompt)
    ```bash
    $ source .venv/Scripts/activate.bat
    ```
    
    - Windows (Powershel)
    ```bash
    $ source .venv/Scripts/activate.ps1
    ```

- Install dependencies
```bash
(.venv) $ make install
```

- Run app
```bash
(.venv) $ make run
```
