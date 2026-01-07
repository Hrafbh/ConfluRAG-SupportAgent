---
id: KB-003
title: "Création d’un tenant + compte admin : procédure"
category: "Onboarding & Access"
tags: ["tenant", "admin", "access", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
Procédure standard pour créer un tenant RoutePilot et provisionner un compte Admin initial.

## Prérequis
- Nom légal client + nom affiché tenant
- E-mail Admin (contact responsable)
- Fuseau horaire + pays (pour formats dates/adresses)

## Resolution steps
1) Ouvrir Console Admin (accès interne).
2) Créer le tenant :
   - Nom affiché
   - Identifiant tenant (court, sans espaces)
   - Timezone
3) Créer l’utilisateur Admin :
   - e-mail (unique)
   - rôle = Admin
   - statut = Actif
4) Envoyer invitation (lien de setup mot de passe/MFA selon politique).
5) Ajouter labels internes (ex: `tier-standard`, `region-eu`, `onboarding-YYYYMM`).

## Verification
- Admin se connecte
- Admin voit module “Administration”
- Admin peut inviter au moins 1 utilisateur

## Escalation
Si e-mail d’invitation non reçu : vérifier article “E-mail/SMS non reçus”, puis escalader si nécessaire.

## References
- (À compléter) “Inviter un utilisateur”
