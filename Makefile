test develop install dist bdist_egg sdist upload:
	@python setup.py $@

docs::
	@make -C docs html
