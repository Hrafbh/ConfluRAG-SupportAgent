---
id: KB-010
title: "Offboarding : désactivation, transfert, audit"
category: "Onboarding & Access"
tags: ["offboarding", "security", "process", "support-l2"]
last_reviewed: "2026-01-07"
---
## Summary
Procédure pour retirer les accès d’un utilisateur (départ, changement d’équipe, prestataire).

## Resolution steps
1) Identifier le compte (e-mail) + tenant.
2) Désactiver l’utilisateur (ne pas supprimer si audit requis).
3) Si rôle critique (Admin/Dispatcher) :
   - transférer responsabilités (inviter nouvel Admin)
   - vérifier qu’au moins 1 Admin reste actif
4) Révoquer sessions actives si option disponible.
5) Noter la demande (ticket interne + date).

## Verification
- L’utilisateur ne peut plus se connecter
- Les comptes clés (Admin) restent opérationnels

## Escalation
Si compte lié à SCIM : désactiver côté IdP + attendre sync.

## References
- (À compléter) “Process demande d’accès”
