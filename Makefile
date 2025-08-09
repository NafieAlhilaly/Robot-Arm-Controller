BUILD_DIR := build
INSTALL_DIR := install
LOG_DIR := log

.PHONY: all
all: build

.PHONY: build
build:
	colcon build

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) $(INSTALL_DIR) $(LOG_DIR)
