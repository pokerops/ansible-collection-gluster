.PHONY: ${MAKECMDGOALS}

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
MAKEFILE_DIR := $(dir $(MAKEFILE_PATH))

HOST_DISTRO = $$(grep ^ID /etc/os-release | cut -d '=' -f 2)
PKGMAN = $$(if [ "$(HOST_DISTRO)" = "fedora" ]; then echo "dnf" ; else echo "apt-get"; fi)
MOLECULE_SCENARIO ?= install
MOLECULE_DOCKER_IMAGE ?= ubuntu2204
MOLECULE_DOCKER_COMMAND ?= /lib/systemd/systemd
MOLECULE_KVM_IMAGE ?= https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img
GALAXY_API_KEY ?=
GITHUB_REPOSITORY ?= $$(git config --get remote.origin.url | cut -d':' -f 2 | cut -d. -f 1)
GITHUB_ORG = $$(echo ${GITHUB_REPOSITORY} | cut -d/ -f 1)
GITHUB_REPO = $$(echo ${GITHUB_REPOSITORY} | cut -d/ -f 2)
REQUIREMENTS = requirements.yml
ROLE_DIR = roles
ROLE_FILE = roles.yml
COLLECTION_NAMESPACE = $$(yq -r '.namespace' < galaxy.yml)
COLLECTION_NAME = $$(yq -r '.name' < galaxy.yml)
COLLECTION_VERSION = $$(yq -r '.version' < galaxy.yml)

LOGIN_ARGS ?=

all: install version lint test

test: requirements
	MOLECULE_KVM_IMAGE=${MOLECULE_KVM_IMAGE} \
	MOLECULE_DOCKER_COMMAND=${MOLECULE_DOCKER_COMMAND} \
	MOLECULE_DOCKER_IMAGE=${MOLECULE_DOCKER_IMAGE} \
	uv run molecule $@ -s ${MOLECULE_SCENARIO}

install:
	@uv sync

lint: requirements
	uv run yamllint .
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	uv run ansible-lint playbooks/

requirements: install
	@yq '.roles[].name' -r < roles.yml | xargs -I {} rm -rf roles/{}
	@python --version
	@uv run ansible-galaxy role install \
		--force --no-deps \
		--roles-path ${ROLE_DIR} \
		--role-file ${ROLE_FILE}
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	uv run ansible-galaxy collection install \
		--force-with-deps .
	@\find ./ -name "*.ymle*" -delete

build: requirements
	@uv run ansible-galaxy collection build --force

ifeq (login,$(firstword $(MAKECMDGOALS)))
    LOGIN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
    $(eval $(subst $(space),,$(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))):;@:)
endif

dependency create prepare converge idempotence side-effect verify destroy cleanup reset list login:
	ANSIBLE_COLLECTIONS_PATH=$(MAKEFILE_DIR) \
	MOLECULE_KVM_IMAGE=${MOLECULE_KVM_IMAGE} \
	MOLECULE_DOCKER_COMMAND=${MOLECULE_DOCKER_COMMAND} \
	MOLECULE_DOCKER_IMAGE=${MOLECULE_DOCKER_IMAGE} \
	uv run molecule $@ -s ${MOLECULE_SCENARIO} ${LOGIN_ARGS}

ignore:
	@uv run ansible-lint --generate-ignore

clean: destroy reset
	@uv env remove $$(which python) >/dev/null 2>&1 || exit 0

publish: build
	uv run ansible-galaxy collection publish --api-key ${GALAXY_API_KEY} \
		"${COLLECTION_NAMESPACE}-${COLLECTION_NAME}-${COLLECTION_VERSION}.tar.gz"

version:
	@uv run molecule --version
