.PHONY: clean dist install uninstall dev-install dev-uninstall help

help:
	@echo "REGX - the regular expression power tool"

install:
	@python3 setup.py install --record INSTALLED --user

uninstall:
	@cat INSTALLED | xargs rm -rvf
	@rm -rvf INSTALLED

dev-install:
	@python3 setup.py develop --user
	touch DEV-INSTALLED

dev-uninstall:
	@python3 setup.py develop --user --uninstall
	@rm -rfv $(shell which regx) DEV-INSTALLED

clean:
	@rm -rfv dist regx.egg-info build

dist: clean
	@python2 setup.py sdist bdist_wheel
	@python3 setup.py bdist_wheel
