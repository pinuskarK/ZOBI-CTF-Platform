#!/usr/bin/env bash
# ZOBI C6 challenge artefact — install only inside the disposable, isolated VM.
# INTENTIONAL LAB WEAKNESS: tar is invoked by command name while the sudo policy
# permits the caller to preserve PATH. Do not use this script on real systems.
set -eu

BACKUP_DIR="/var/backups/zobi"
SOURCE_DIR="/home/researcher/research-data"
/usr/bin/mkdir -p "$BACKUP_DIR"
ARCHIVE="$BACKUP_DIR/research-$(/usr/bin/date +%Y%m%d%H%M%S).tar.gz"

# Intentionally unsafe for the challenge: command lookup uses PATH.
tar -czf "$ARCHIVE" -C "$SOURCE_DIR" .
printf 'Backup created: %s\n' "$ARCHIVE"
