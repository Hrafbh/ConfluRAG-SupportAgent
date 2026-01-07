---
id: KB-013
title: "Reset MFA : perte/changement téléphone"
category: "SSO/MFA"
tags: ["mfa-reset", "support-l2", "security"]
last_reviewed: "2026-01-07"
---
## Summary
Procédure L2 pour réinitialiser la MFA quand l’utilisateur a perdu/changé de téléphone.

## Informations à collecter
- Tenant + e-mail utilisateur
- Contexte : perte / vol / changement
- Confirmation identité (selon politique interne)

## Resolution steps
1) Vérifier statut compte (actif).
2) Réinitialiser MFA depuis console admin (action “Reset MFA” si disponible).
3) Envoyer consignes à l’utilisateur :
   - se reconnecter
   - ré-enrôler MFA (KB-012)
   - régénérer codes de secours (KB-015)

## Verification
Login OK + MFA configurée sur nouveau device.

## Escalation
Si utilisateur en SSO strict : reset MFA peut dépendre de l’IdP → rediriger IAM.

## References
- (À compléter) “Activation MFA”
