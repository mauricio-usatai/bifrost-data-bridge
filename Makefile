app:
	python main.py

pylint:
	git ls-files '*.py' | xargs pylint --disable=duplicate-code --fail-under=10

black:
	git ls-files '*.py' | black --check .

pytest:
	pytest