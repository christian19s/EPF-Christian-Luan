lint:
	pylint --disable=all --enable=trailing-whitespace,line-too-long,missing-final-newline .

run:
	python3 main.py

install-requirements:
	pip3 install -r requirements.txt

make-docker: 
	docker buildx build -t docker-test .
run-docker:
	docker run -p 8080:8080 --rm docker-test
