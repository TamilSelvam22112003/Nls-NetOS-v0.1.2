#!/usr/bin/env bash
set -Eeuo pipefail

# Install FRRouting and deploy the repository-managed configuration.
# This script enables the service but deliberately does not start routing.

readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly REPO_ROOT="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
readonly FRR_CONFIG_SOURCE="${REPO_ROOT}/etc/frr"
readonly FRR_CONFIG_DEST="/etc/frr"
readonly FRR_DAEMONS=(zebra ospfd ospf6d staticd)
readonly FRR_CONFIG_FILES=(daemons frr.conf vtysh.conf nls-routing.conf)

log() {
    printf '[NLS-FRR] %s\n' "$*"
}

die() {
    printf '[NLS-FRR] ERROR: %s\n' "$*" >&2
    exit 1
}

if [[ "${EUID}" -ne 0 ]]; then
    die "Run as root: sudo $0"
fi

if [[ ! -r /etc/os-release ]]; then
    die "Cannot identify the operating system (/etc/os-release is missing)."
fi

# shellcheck disable=SC1091
. /etc/os-release
[[ "${ID:-}" == "ubuntu" ]] || die "Ubuntu is required; detected: ${ID:-unknown}."

case "${VERSION_ID:-}" in
    20.04|22.04|24.04)
        ;;
    *)
        die "Unsupported Ubuntu release: ${VERSION_ID:-unknown}. Supported releases: 20.04, 22.04 and 24.04."
        ;;
esac

[[ -d "${FRR_CONFIG_SOURCE}" ]] || die "Repository FRR configuration directory not found: ${FRR_CONFIG_SOURCE}"

for file in "${FRR_CONFIG_FILES[@]}"; do
    [[ -s "${FRR_CONFIG_SOURCE}/${file}" ]] || die "Required repository configuration is missing or empty: ${FRR_CONFIG_SOURCE}/${file}"
done

export DEBIAN_FRONTEND=noninteractive
log "Installing FRRouting and its Python management tools."
apt-get update
apt-get install -y frr frr-pythontools

getent passwd frr >/dev/null || die "The FRR package did not create the 'frr' service account."
getent group frr >/dev/null || die "The FRR package did not create the 'frr' group."

install -d -o frr -g frr -m 0750 "${FRR_CONFIG_DEST}"

# Preserve any existing administrator/package configuration before deploying
# repository-managed files. The backup is created only when a target exists.
backup_dir=""
for file in "${FRR_CONFIG_FILES[@]}"; do
    if [[ -e "${FRR_CONFIG_DEST}/${file}" ]]; then
        if [[ -z "${backup_dir}" ]]; then
            backup_dir="${FRR_CONFIG_DEST}/nls-backup-$(date +%Y%m%d%H%M%S)"
            install -d -o root -g root -m 0700 "${backup_dir}"
        fi
        cp -a "${FRR_CONFIG_DEST}/${file}" "${backup_dir}/${file}"
    fi
done

log "Deploying repository FRR configuration to ${FRR_CONFIG_DEST}."
for file in "${FRR_CONFIG_FILES[@]}"; do
    install -o frr -g frr -m 0640 "${FRR_CONFIG_SOURCE}/${file}" "${FRR_CONFIG_DEST}/${file}"
done

# Verify that the required routing daemons are enabled in the deployed file.
for daemon in "${FRR_DAEMONS[@]}"; do
    grep -Eq "^[[:space:]]*${daemon}=yes([[:space:]]*(#.*)?)?$" "${FRR_CONFIG_DEST}/daemons" \
        || die "Required daemon is not enabled in /etc/frr/daemons: ${daemon}"
done

log "Checking installed FRR executables."
command -v vtysh >/dev/null 2>&1 || die "vtysh was not found in PATH."

for daemon in "${FRR_DAEMONS[@]}"; do
    [[ -x "/usr/lib/frr/${daemon}" ]] || die "FRR daemon executable is missing: /usr/lib/frr/${daemon}"
done

dpkg-query -W -f='${Status}' frr 2>/dev/null | grep -q "install ok installed" \
    || die "The FRR package is not reported as installed by dpkg."
dpkg-query -W -f='${Status}' frr-pythontools 2>/dev/null | grep -q "install ok installed" \
    || die "The frr-pythontools package is not reported as installed by dpkg."

log "Enabling the FRR service without starting it."
systemctl enable frr

systemctl is-enabled --quiet frr || die "FRR service could not be enabled."

log "Installation and configuration deployment completed."
log "vtysh: $(command -v vtysh)"
for daemon in "${FRR_DAEMONS[@]}"; do
    log "${daemon}: /usr/lib/frr/${daemon}"
done
log "Configuration: ${FRR_CONFIG_DEST}"
log "Service enabled: yes"
log "Service active: $(systemctl is-active frr 2>/dev/null || true)"
log "Routing daemons were NOT started by this script."

if [[ -n "${backup_dir}" ]]; then
    log "Previous configuration backup: ${backup_dir}"
fi

log "The NLS-specific nls-routing.conf file is deployed as a managed template; it is not automatically included in frr.conf."
