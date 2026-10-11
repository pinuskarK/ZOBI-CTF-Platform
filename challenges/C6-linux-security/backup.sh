#!/usr/bin/env bash
# INTENTIONALLY VULNERABLE CTF SCRIPT. Install only in the isolated ZOBI C6 guest.
# The command name "tar" is intentionally unresolved by absolute path for the
# PATH-lookup lesson. Never reuse this privileged script on a real system.
set -eu

SOURCE_DIR="/home/researcher/research"
BACKUP_DIR="/var/backups/zobi-c6"
BACKUP_FILE="${BACKUP_DIR}/research.tar.gz"

/usr/bin/mkdir -p "$BACKUP_DIR"
if [[ ! -d "$SOURCE_DIR" ]]; then
    /usr/bin/printf 'Source directory is missing: %s\n' "$SOURCE_DIR" >&2
    exit 1
fi

# INTENTIONAL CTF WEAKNESS: privileged execution resolves "tar" via PATH.
tar -czf "$BACKUP_FILE" -C "$SOURCE_DIR" .

/usr/bin/chown root:root "$BACKUP_FILE"
/usr/bin/chmod 0600 "$BACKUP_FILE"
/usr/bin/printf 'Research backup complete.\n'
