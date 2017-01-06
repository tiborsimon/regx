.PHONY: clean dist install uninstall dev-install dev-uninstall help test

NAME := REGX

BOLD := $(shell tput bold)
YELLOW := $(shell tput setaf 3)
RESET:= $(shell tput sgr0)

help:
	@echo ""
	@echo "$(BOLD)$(NAME)$(RESET) - the $(BOLD)REG$(RESET)ular e$(BOLD)X$(RESET)pression power tool $(BOLD)make interface$(RESET)"
	@echo "────────────────────────────────────────────────────────"
	@echo "$(BOLD)help$(RESET)           Prints out this help message."
	@echo "$(BOLD)test$(RESET)           Runs the test suite."
	@echo "$(BOLD)install$(RESET)        Installs $(NAME) in the regular static way."
	@echo "$(BOLD)uninstall$(RESET)      Uninstalls the static installation of $(NAME)."
	@echo "$(BOLD)dev-install$(RESET)    Installs $(NAME) in developer mode."
	@echo "$(BOLD)dev-uninstall$(RESET)  Uninstalls the development mode."
	@echo "$(BOLD)build$(RESET)          Builds $(NAME) for distribution."
	@echo "$(BOLD)upload$(RESET)         Upload $(NAME) to PyPi with twine."
	@echo "$(BOLD)clean$(RESET)          Cleans up all generated artifacts."
	@echo ""

test:
	python2 -m unittest discover & python3 -m unittest discover

install:
	@python setup.py install --record INSTALLED --user
	@echo "$(BOLD)$(YELLOW)$(NAME)$(RESET) was $(BOLD)$(YELLOW)installed$(RESET)."

uninstall:
	@cat INSTALLED | xargs rm -rvf
	@rm -rvf INSTALLED
	@echo "$(BOLD)$(YELLOW)$(NAME)$(RESET) was $(BOLD)$(YELLOW)uninstalled$(RESET)."

dev-install:
	@python setup.py develop --user
	touch DEV-INSTALLED
	@echo "$(BOLD)$(YELLOW)$(NAME)$(RESET) development mode was $(BOLD)$(YELLOW)installed$(RESET)."

dev-uninstall:
	@python setup.py develop --user --uninstall
	@rm -rfv $(shell which regx) DEV-INSTALLED
	@echo "$(BOLD)$(YELLOW)$(NAME)$(RESET) development mode was $(BOLD)$(YELLOW)uninstalled$(RESET)."

clean:
	@rm -rfv dist regx.egg-info build
	@find . -name "*.pyc" | xargs rm -fv
	@find . -name "__pycache__" | xargs rm -fvr

build: clean
	@python2 setup.py sdist bdist_wheel
	@python3 setup.py bdist_wheel

upload: dist
	@twine upload dist/*

