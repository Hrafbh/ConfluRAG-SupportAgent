# scripts/check_kb.py
"""
Script simple (niveau débutant) pour vérifier la KB RoutePilot.

Ce script vérifie :
1) Que les fichiers KB-001 à KB-060 existent aux chemins attendus.
2) Que chaque fichier contient un front-matter entre --- et ---.
3) Que le champ "id:" existe et correspond au numéro KB du fichier.
4) Que le champ "last_reviewed:" ressemble à une date YYYY-MM-DD.

Usage:
  python scripts/check_kb.py
"""

import os
import re
from datetime import datetime


# 1) Liste des fichiers attendus (KB-001 → KB-060)
KB_FILES = {
    1: "kb/onboarding-access/kb-001_routepilot-overview.md",
    2: "kb/onboarding-access/kb-002_onboarding-new-customer.md",
    3: "kb/onboarding-access/kb-003_create-tenant-and-admin.md",
    4: "kb/onboarding-access/kb-004_invite-users.md",
    5: "kb/onboarding-access/kb-005_roles-and-permissions.md",
    6: "kb/onboarding-access/kb-006_access-request-process.md",
    7: "kb/onboarding-access/kb-007_password-reset.md",
    8: "kb/onboarding-access/kb-008_account-locked.md",
    9: "kb/onboarding-access/kb-009_shared-mailbox-and-support-alias.md",
    10: "kb/onboarding-access/kb-010_offboarding-user.md",
    11: "kb/sso-mfa/kb-011_sso-setup-overview.md",
    12: "kb/sso-mfa/kb-012_enable-mfa.md",
    13: "kb/sso-mfa/kb-013_reset-mfa.md",
    14: "kb/sso-mfa/kb-014_backup-codes.md",
    15: "kb/sso-mfa/kb-015_common-login-errors.md",
    16: "kb/sso-mfa/kb-016_browser-session-issues.md",
    17: "kb/sso-mfa/kb-017_sso-access-denied.md",
    18: "kb/sso-mfa/kb-018_user-email-change.md",
    19: "kb/sso-mfa/kb-019_scim-user-provisioning.md",
    20: "kb/sso-mfa/kb-020_admin-console-access.md",
    21: "kb/workstation/kb-021_supported-browsers.md",
    22: "kb/workstation/kb-022_clear-cache-and-cookies.md",
    23: "kb/workstation/kb-023_enable-notifications.md",
    24: "kb/workstation/kb-024_pdf-export-issues.md",
    25: "kb/workstation/kb-025_file-upload-fail.md",
    26: "kb/workstation/kb-026_mobile-app-install.md",
    27: "kb/workstation/kb-027_mobile-login-issues.md",
    28: "kb/workstation/kb-028_gps-and-location-permissions.md",
    29: "kb/workstation/kb-029_camera-and-proof-of-delivery.md",
    30: "kb/workstation/kb-030_barcode-scan-troubleshooting.md",
    31: "kb/workstation/kb-031_printer-label-setup.md",
    32: "kb/workstation/kb-032_accessibility-and-ui-zoom.md",
    33: "kb/network-vpn/kb-033_connectivity-checklist.md",
    34: "kb/network-vpn/kb-034_wifi-issues-office.md",
    35: "kb/network-vpn/kb-035_vpn-connection.md",
    36: "kb/network-vpn/kb-036_proxy-issues.md",
    37: "kb/network-vpn/kb-037_whitelist-ip-request.md",
    38: "kb/network-vpn/kb-038_email-sms-not-received.md",
    39: "kb/network-vpn/kb-039_slow-app-performance.md",
    40: "kb/network-vpn/kb-040_mobile-sync-network.md",
    41: "kb/network-vpn/kb-041_public-status-page.md",
    42: "kb/network-vpn/kb-042_remote-warehouse-access.md",
    43: "kb/jira-tooling/kb-043_how-to-open-support-ticket.md",
    44: "kb/jira-tooling/kb-044_ticket-triage-template.md",
    45: "kb/jira-tooling/kb-045_priority-impact-urgency.md",
    46: "kb/jira-tooling/kb-046_repro-steps-and-screenshots.md",
    47: "kb/jira-tooling/kb-047_customer-communication-guidelines.md",
    48: "kb/jira-tooling/kb-048_escalation-rules.md",
    49: "kb/jira-tooling/kb-049_confluence-page-naming.md",
    50: "kb/jira-tooling/kb-050_search-in-confluence.md",
    51: "kb/jira-tooling/kb-051_labels-taxonomy.md",
    52: "kb/jira-tooling/kb-052_known-issues-log.md",
    53: "kb/incidents-runbooks/kb-053_runbook-platform-unavailable.md",
    54: "kb/incidents-runbooks/kb-054_runbook-login-spike.md",
    55: "kb/incidents-runbooks/kb-055_runbook-mobile-sync-outage.md",
    56: "kb/incidents-runbooks/kb-056_runbook-notifications-down.md",
    57: "kb/incidents-runbooks/kb-057_runbook-map-eta-issues.md",
    58: "kb/incidents-runbooks/kb-058_runbook-label-printing-issues.md",
    59: "kb/incidents-runbooks/kb-059_post-incident-review.md",
    60: "kb/incidents-runbooks/kb-060_major-incident-comms.md",
}


# 2) Petite fonction pour lire un fichier texte
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# 3) Extraire le front-matter (tout ce qui est entre --- et ---)
def extract_front_matter(text):
    # Cherche un bloc au début du fichier : --- ... ---
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        return None
    return match.group(1)


# 4) Chercher une valeur "id:" dans le front-matter
def get_id(front_matter):
    match = re.search(r"^id:\s*(.+)$", front_matter, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


# 5) Chercher "last_reviewed:" et vérifier le format date
def get_last_reviewed(front_matter):
    match = re.search(r"^last_reviewed:\s*(.+)$", front_matter, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip().strip('"').strip("'")
    return value


def is_valid_date(date_str):
    # Vérifier que ça ressemble à YYYY-MM-DD
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def main():
    errors = []

    # Vérifier tous les fichiers
    for number in range(1, 61):
        expected_path = KB_FILES[number]

        # (A) existe ?
        if not os.path.exists(expected_path):
            errors.append(f"[FILE_MISSING] KB-{number:03d} -> {expected_path}")
            continue

        # (B) lire le contenu
        text = read_file(expected_path)

        # (C) front-matter
        fm = extract_front_matter(text)
        if fm is None:
            errors.append(f"[FRONT_MATTER_MISSING] {expected_path}")
            continue

        # (D) id
        kb_id = get_id(fm)
        if kb_id is None:
            errors.append(f"[ID_MISSING] {expected_path} (missing 'id:')")
        else:
            expected_id = f"KB-{number:03d}"
            if kb_id != expected_id:
                errors.append(f"[ID_MISMATCH] {expected_path} (found {kb_id}, expected {expected_id})")

        # (E) last_reviewed
        last_reviewed = get_last_reviewed(fm)
        if last_reviewed is None:
            errors.append(f"[LAST_REVIEWED_MISSING] {expected_path} (missing 'last_reviewed:')")
        else:
            if not is_valid_date(last_reviewed):
                errors.append(f"[LAST_REVIEWED_INVALID] {expected_path} (found {last_reviewed}, expected YYYY-MM-DD)")

    # Résultat
    if len(errors) == 0:
        print(" Tout est OK : KB-001 à KB-060 sont présents et le front-matter est cohérent.")
    else:
        print(f" {len(errors)} problème(s) trouvé(s) :\n")
        for e in errors:
            print("-", e)
        print("\nCorrigez les fichiers listés puis relancez : python scripts/check_kb.py")


if __name__ == "__main__":
    main()
