---
id: KB-014
title: "Codes de secours : génération et récupération"
category: "SSO/MFA"
tags: ["backup-codes", "mfa", "support-l1"]
last_reviewed: "2026-01-07"
---
## Summary
Les codes de secours permettent de se connecter si le second facteur est indisponible.

## Resolution steps
1) Aller dans “Profil / Sécurité”.
2) Section “Codes de secours”.
3) Générer un nouveau lot (invalidate l’ancien).
4) Stocker en lieu sûr (gestionnaire de mots de passe recommandé).

## Symptômes
- “Je n’ai plus mes codes” : régénérer (si login possible).
- “Code invalide” : vérifier qu’il n’a pas déjà été utilisé.

## Verification
Tester un code une fois (puis le considérer consommé).

## Escalation
Si login impossible et pas de codes : utiliser KB-013 (reset MFA).

## References
- (À compléter) “Reset MFA”
