#!/bin/bash

set -e

PROJECT_ROOT="$(dirname "$(readlink -e "$0")")/../../.."
CONTRIB="$PROJECT_ROOT/contrib"
CONTRIB_SDIST="$CONTRIB/build-linux/sdist"
DISTDIR="$PROJECT_ROOT/dist"

. "$CONTRIB"/build_tools_util.sh

# note that at least py3.7 is needed, to have https://bugs.python.org/issue30693
python3 --version || fail "python interpreter not found"

break_legacy_easy_install

# upgrade to modern pip so that it knows the flags we need.
# we will then install a pinned version of pip as part of requirements-build-sdist
python3 -m pip install --upgrade pip

info "Installing pinned requirements."
python3 -m pip install --no-dependencies --no-warn-script-location -r "$CONTRIB"/deterministic-build/requirements-build-sdist.txt

chmod +x "$CONTRIB"/make_packages 

"$CONTRIB"/make_packages || fail "make_packages failed"

chmod +x "$CONTRIB_SDIST"/make_tgz

"$CONTRIB_SDIST"/make_tgz || fail "make_tgz failed"


info "done."
ls -la "$DISTDIR"
sha256sum "$DISTDIR"/*
