init:
	pip install -e . '.[dev]'

lint:
	flake8 aws_assume_role_helper
	pylint --rcfile .pylintrc aws_assume_role_helper
