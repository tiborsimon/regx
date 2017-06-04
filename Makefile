.PHONY: clean dist install uninstall dev-install dev-uninstall help test

NAME := REGX
PYTHON := python3
USER := --user

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

BOLD := $(shell tput bold)
RED := $(shell tput setaf 1)
GREEN := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
RESET:= $(shell tput sgr0)

OK      := [ $(BOLD)$(GREEN)OK$(RESET) ]
WARNING := [ $(BOLD)$(YELLOW)!!$(RESET) ]
ERROR   := [$(BOLD)$(RED)FAIL$(RESET)]

STATIC_INDICATOR := .INSTALLED
DEVELOP_INDICATOR := .DEVELOP-INSTALLED

ERROR_INSTALLED := "$(ERROR) $(NAME) was already installed in static mode. Run $(BOLD)make uninstall$(RESET) first!"
ERROR_DEV_INSTALLED := "$(ERROR) $(NAME) was already installed in development mode. Run $(BOLD)make dev-uninstall$(RESET) first!"
ERROR_NOT_INSTALLED := "$(ERROR) $(NAME) was not installed yet. Run $(BOLD)make install$(RESET) first!"
ERROR_NOT_DEV_INSTALLED := "$(ERROR) $(NAME) was not installed in development mode. Run $(BOLD)make dev-install$(RESET) first!"

test:
	$(PYTHON) -m unittest discover

install:
	@if [ -f $(STATIC_INDICATOR) ]; then echo $(ERROR_INSTALLED); exit 1; fi
	@if [ -f $(DEVELOP_INDICATOR) ]; then echo $(ERROR_DEV_INSTALLED); exit 1; fi
	@$(PYTHON) setup.py install --record $(STATIC_INDICATOR) $(USER)
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) was installed."

uninstall:
	@if [ -f $(DEVELOP_INDICATOR) ]; then echo $(ERROR_DEV_INSTALLED); exit 1; fi
	@if [ ! -f $(STATIC_INDICATOR) ]; then echo $(ERROR_NOT_INSTALLED); exit 1; fi
	@cat $(STATIC_INDICATOR) | xargs -r rm -rvf
	@rm -rvf $(STATIC_INDICATOR)
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) was uninstalled."

dev-install:
	@if [ -f $(STATIC_INDICATOR) ]; then echo $(ERROR_INSTALLED); exit 1; fi
	@if [ -f $(DEVELOP_INDICATOR) ]; then echo $(ERROR_DEV_INSTALLED); exit 1; fi
	@$(PYTHON) setup.py develop $(USER)
	touch $(DEVELOP_INDICATOR)
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) development mode was installed."

dev-uninstall:
	@if [ -f $(STATIC_INDICATOR) ]; then echo $(ERROR_INSTALLED); exit 1; fi
	@if [ ! -f $(DEVELOP_INDICATOR) ]; then echo $(ERROR_NOT_DEV_INSTALLED); exit 1; fi
	$(PYTHON) setup.py develop $(USER) --uninstall
	@rm -rfv $(shell which regx) $(DEVELOP_INDICATOR)
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) development mode was uninstalled."

clean:
	@rm -rfv dist regx.egg-info build
	@find . -name "*.pyc" | xargs -r rm -fv
	@find . -name "__pycache__" | xargs -r rm -fvr
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) repo was cleaned."


build: clean
	@python2 setup.py sdist bdist_wheel
	@python3 setup.py bdist_wheel
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) was built for python2 and python3."

upload: dist
	@twine upload dist/*
	@echo "$(OK) $(BOLD)$(NAME)$(RESET) was uploaded to PyPi."

