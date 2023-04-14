run:
	python -m uvicorn server_app:app --reload --proxy-headers --host 0.0.0.0 --port 8000
setup: requirements.txt
	python -m pip install -r requirements.txt
clean:
	rm -rf __pycache__
build:
	docker build --rm --tag cloudml .
deploy:
	docker run -d -p 8000:8000 --name cloudml-container cloudml
remove:
	docker rm cloudml-container
start:
	docker start cloudml-container
stop:
	docker stop cloudml-container