SHELL = /bin/bash

MD5 := md5
BUILD_DIR := build
MD5_DIR := $(BUILD_DIR)/md5
DATA_DIR := data
DATA_CLEAN_DIR := $(DATA_DIR)/clean
DATA_MATCH_DIR := $(DATA_DIR)/match
DATA_FUSE_DIR := $(DATA_DIR)/fuse
SCRIPT_DIRS := clean match fuse
DATA_DEP_FILES := $(patsubst %,%/data.d,$(SCRIPT_DIRS))
EXCLUDED_SCRIPTS := fuse/all.py match/cross_agency.py match/harahan_pd.py

.DEFAULT_GOAL := all

export PYTHONPATH := $(shell pwd):$(PYTHONPATH)

.SUFFIXES:
.SECONDARY:
.PHONY: all clean

clean:
	rm -f $(DATA_DEP_FILES)
	rm -rf $(BUILD_DIR)

# calculate md5
$(MD5_DIR)/%.md5: % | $(MD5_DIR)
	@-mkdir -p $(dir $@) 2>/dev/null
	$(if $(filter-out $(shell cat $@ 2>/dev/null),$(shell $(MD5) $<)),$(MD5) $< > $@)

%/data.d: %/*.py
	scripts/write_deps.py $* $(if $(findstring fuse,$*),--all ,)$(patsubst %,-e %,$(EXCLUDED_SCRIPTS))

$(BUILD_DIR) $(DATA_DIR): ; @-mkdir $@ 2>/dev/null
$(MD5_DIR): | $(BUILD_DIR) ; @-mkdir $@ 2>/dev/null
$(DATA_CLEAN_DIR) $(DATA_MATCH_DIR) $(DATA_FUSE_DIR): | $(DATA_DIR) ; @-mkdir $@ 2>/dev/null

include $(DATA_DEP_FILES)
