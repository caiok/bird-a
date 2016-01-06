# ================================ #

BASE_DIR := $(PWD)

# Set VENV if not already set
ifndef VENV
	VENV := /usr
	SUDO := sudo
else:
	SUDO :=
endif


# Ask the user if prod or devel
reply := $(shell read -p 'Production or Development? (p/D) ' reply; echo $$reply)
PROD := $(shell echo "$(reply)" | grep "^[pP]$$" | tr '[:lower:]' '[:upper:]')

# Variables setting
ifeq ($(PROD), "P")
	BE_SETUP_TARGET := install
	BE_CONF := $(PWD)/config/production.ini
else
	BE_SETUP_TARGET := develop
	BE_CONF := $(PWD)/config/development.ini
endif


.PHONY: all make-be make-fe run-be run-fe

# -------------------------------- #

all:
	#@echo "Prod: \"$(PROD)\" (reply: \"$(reply)\")"
	@echo
	@echo "make make-be"
	@echo "     Install the backend"
	@echo
	@echo "make make-fe"
	@echo "     Make the frontend"
	@echo
	@echo "make run-be"
	@echo "     Run the backend"
	@echo
	@echo "make run-fe"
	@echo "     Run the frontend"
	@echo

# ================================ #

# Make Backend
make-be:
	cd $(BASE_DIR)/backend; $(SUDO) $(VENV)/bin/python setup.py $(BE_SETUP_TARGET)

# -------------------------------- #

# Run Backend
run-be:
	cd $(BASE_DIR)/backend ; $(VENV)/bin/pserve ../config/development.ini --reload

# -------------------------------- #

# Make Frontend
make-fe:
	cd $(BASE_DIR)/frontend; grunt

# -------------------------------- #

# Run Frontend
run-fe:
	cd $(BASE_DIR)/frontend ; grunt serve

# ================================ #

clean-be:
	cd $(BASE_DIR)/backend;  $(SUDO) rm -rvf backend.egg-info
	cd $(BASE_DIR)/backend;  find . -name "*.pyc" -exec rm -vf '{}' \;

# -------------------------------- #

clean-fe:
	cd $(BASE_DIR)/frontend; grunt clean

# -------------------------------- #

clean: clean-be clean-fe

# ================================ #