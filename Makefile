
install: ./backend/requirements.txt ./E2E-tests/requirements.txt
	python -m venv env
	. ./env/bin/activate
	pip3 install -r ./backend/requirements.txt
	pip3 install -r ./E2E-tests/requirements.txt
	npm install --prefix ./frontend
	playwright install

dev-frontend:
	npm run --prefix ./frontend dev & echo $$! > temp.txt

E2E:
	pytest ./E2E-tests
	if [ -f temp.txt ]; then kill `cat temp.txt` && rm temp.txt; fi


tests:
	make install
	PYTHONPATH=./backend/ coverage run -m pytest ./backend/tests/test_main.py;
	coverage html
	make -j 2 dev-frontend E2E

dev-backend:
	fastapi dev ./backend/src/main.py

dev:
	make install
	make -j 2 dev-frontend dev-backend

clean:
	rm -f coverage.* .coverage ./backend/*.db ./backend/.coverage ./backend/tests/*.db
	rm -f -r ./env ./E2E-tests/env ./backend/env ./backend/htmlcov ./frontend/node_modules
