pep8:
	flake8 events_watcher --ignore=E501,E127,E128,E124

test:
	coverage run --branch --source=events_watcher manage.py test events_watcher
	coverage report --omit=events_watcher/test*

release:
	python setup.py sdist register upload -s
