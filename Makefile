check:
	python setup.py check

build:
	python setup.py sdist

clean:
	@rm -rf ./dist
	@rm -rf ./tinylimit.egg-info
	@rm -rf ./cache

upload:
	twine upload ./dist/*
