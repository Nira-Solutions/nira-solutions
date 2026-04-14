# Déployer la brochure sur GitHub Pages

## Étape 1 — Créer le repo GitHub

```bash
cd C:/Users/FlowUP/Downloads/Claude/Claude/Nira/nira-agents
git init
git add .
git commit -m "Initial Nira Solutions"
```

Sur [github.com/new](https://github.com/new) :
- Nom : `nira-solutions` (ou `nira-agents`)
- Public
- **Ne pas** ajouter README / .gitignore (on les a déjà)

Puis :
```bash
git remote add origin https://github.com/<ton-user>/nira-solutions.git
git branch -M main
git push -u origin main
```

## Étape 2 — Activer GitHub Pages

1. Sur le repo GitHub → **Settings** → **Pages**
2. Source : `Deploy from a branch`
3. Branch : `main` / dossier : `/docs`
4. **Save**

Après ~1 min, la brochure est live à :
`https://<ton-user>.github.io/nira-solutions/`

## Étape 3 — Domaine custom (optionnel)

Si tu as `nira-solutions.com` ou `nira.io` :

1. Dans `docs/`, créer un fichier `CNAME` contenant juste : `nira-solutions.com`
2. Chez ton registrar, ajouter un CNAME DNS :
   - `www` → `<ton-user>.github.io`
   - Apex `@` → IP GitHub Pages (voir [docs.github.com/pages/custom-domain](https://docs.github.com/en/pages))
3. Dans Settings → Pages → Custom domain → mettre `nira-solutions.com` + cocher HTTPS

## Mise à jour

Chaque push sur `main` déclenche un redéploiement automatique (~30s).

```bash
# modifier docs/index.html puis :
git add docs/
git commit -m "Update brochure"
git push
```

## Partage rapide

- Envoyer le lien GitHub Pages en RDV commercial
- Exporter en PDF : ouvrir dans Chrome → Imprimer → Enregistrer en PDF (mode portrait A4)
