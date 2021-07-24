deps:
	pip3 install -r requirements.txt

test:
	nose2 -v --with-coverage --coverage-report html --coverage-report term
