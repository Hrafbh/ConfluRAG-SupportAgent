---
id: KB-011
title: "SSO RoutePilot : principes (SAML/OIDC) & prérequis"
category: "SSO/MFA"
tags: ["sso", "saml", "oidc", "iam", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
Le SSO permet aux utilisateurs de se connecter via l’identité entreprise. Cette page cadre les prérequis et les points de vigilance support.

## Prérequis
- Domaine e-mail de l’entreprise
- Contact IAM (owner technique)
- Choix : SAML ou OIDC (selon politique interne)
- Règles de mapping : groupes → rôles RoutePilot

## Points de vigilance (support)
- Un SSO mal configuré crée des “Access denied” même si le compte existe.
- Le provisioning (SCIM) change qui gère les comptes (IdP vs RoutePilot).
- Toujours tester avec un compte pilote avant déploiement global.

## Verification
- 1 utilisateur pilote login OK
- Rôle correct attribué
- Déconnexion/reconnexion OK

## Escalation
Si erreurs SSO persistantes : collecter message exact + heure + tenant + e-mail test.

## References
- (À compléter) “Access denied”
