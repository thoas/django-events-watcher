test:
	flake8 events_watcher --ignore=E501,E127,E128,E124
	coverage run --branch --source=events_watcher runtests.py
	coverage report --omit=events_watcher/test*

release:
	python setup.py sdist register upload -s
