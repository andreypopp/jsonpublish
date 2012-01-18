test develop install dist bdist_egg sdist upload register:
	@python setup.py $@

docs::
	@make -C docs html
