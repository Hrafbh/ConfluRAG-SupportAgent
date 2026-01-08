# ConfluRAG-SupportAgent (RoutePilot)

Agent support interne (L1/L2) basé sur une base de connaissances **Confluence**, avec une source “as-code” dans GitHub (Markdown), pour démontrer des compétences en **NLP / RAG / Agent orchestration** dans un contexte réaliste de SaaS B2B.

> **Contexte métier (fictif, portfolio)**  
> **RoutePilot** est un SaaS B2B lié au monde physique (logistique / livraison) : planification de tournées, exécution terrain, preuve de livraison (POD), reporting, administration des accès.  
> Cet agent aide les collaborateurs (Support, Ops, Customer Success) à résoudre les demandes récurrentes sans remplacer l’équipe support.

---

## Objectifs du projet

- Centraliser et structurer une **base de connaissances** (KB) réaliste pour un SaaS B2B.
- Connecter la KB à Confluence (source “live”) tout en gardant une version **versionnée sur GitHub** (source “as-code”).
- Construire un **agent support interne** capable de :
  - répondre avec **citations** (liens/pages Confluence),
  - détecter les cas “je ne sais pas” / manque de preuve,
  - **router** vers L2/L3 (escalation) quand nécessaire,
  - générer des brouillons de réponse et/ou tickets (optionnel).

---

## Périmètre Support (L1/L2)

### Couvre
- Accès au SaaS : comptes, rôles, permissions, onboarding, offboarding.
- Authentification : SSO/MFA, erreurs de session, “access denied”.
- Usage produit : exports, notifications, mobile (GPS/caméra), POD, scan, impression étiquettes.
- Connectivité “non technique” : Wi-Fi/VPN/Proxy (diagnostic simple), e-mail/SMS non reçus.
- Process support : triage, communication client, escalation, templates.

### Hors scope
- Débug profond DevOps/SRE (logs infra détaillés, tuning complexe).
- Support poste utilisateur générique hors contexte RoutePilot.

---

## Base de connaissances (KB)

La base de connaissances est maintenue “as-code” dans le dossier `kb/` (Markdown), puis publiée dans Confluence pour reproduire un contexte entreprise et faciliter l’usage côté support.

- **1 page = 1 fichier** `.md`
- **Nommage** : `KB-###_<slug>.md` (ID stable pour citations, mapping Confluence, évaluation)
- **Organisation** : pages classées par thématiques (onboarding, SSO/MFA, usage web/mobile, connectivité simple, support ops, runbooks)
- **Objectif** : couvrir les demandes récurrentes **L1/L2** (accès, erreurs de connexion, usage produit, exports, mobile, notifications, connectivité, process support)
- **Qualité** : chaque page suit un template (sections standard + métadonnées) pour améliorer la recherche et le RAG

Exemples :
- `kb/onboarding-access/kb-002_onboarding-new-customer.md`
- `kb/sso-mfa/kb-013_reset-mfa.md`

---

## Architecture cible (RAG + Agent)

1) **KB source (GitHub)**  
   Pages en Markdown (`kb/`) avec métadonnées : `id`, `title`, `category`, `tags`, `last_reviewed`.

2) **Sync Confluence (publish)**  
   Publication des pages vers Confluence (pour navigation, collaboration, et démo réaliste).

3) **Ingestion Confluence (pull)**  
   Extraction via API : contenu + métadonnées (titre, labels, url, dates). Normalisation du texte.

4) **Chunking + métadonnées**  
   Découpage par sections (overlap léger) et ajout de métadonnées par chunk : `page_id`, `title`, `tags`, `category`, `updated_at`, `source_url`.

5) **Indexation (vector store)**  
   Embeddings des chunks + stockage dans une base vectorielle pour la recherche sémantique.

6) **Retrieval + citations**  
   Top-k retrieval + filtrage (catégorie/tags). Réponses **avec citations** (titre + lien Confluence / id page).

7) **Agent support (tools + routing + guardrails)**  
   Outils typiques :
   - `search_kb(query, filters)`
   - `open_page(page_id)`
   - `draft_reply(context, question)`
   - `escalate(summary)` *(optionnel : brouillon d’escalade L2/L3)*

   Guardrails :
   - mode “je ne sais pas” si preuves insuffisantes
   - réponses factuelles basées sur les sources
   - format actionnable (étapes L1/L2)

8) **UI + évaluation**  
   UI chat + sources citées, et un jeu de tests (questions answerable/unanswerable) pour mesurer retrieval, couverture citations et robustesse anti-hallucination.

