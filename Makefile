# install uv
install-uv:
	pip install uv

# create a virtual environment
venv:
	uv venv

# install dependencies
install:
	uv add -r requirements.txt


# run the server in DEV app
run-dev:
	uvicorn server:app --reload

# run the server in PROD app
run:
	uvicorn server:app --host 0.0.0.0
