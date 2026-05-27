# mon-app

Application FastAPI minimaliste — fil conducteur pour apprendre le pipeline CI/CD local avec Jenkins et Kubernetes.

## Stack

- **Python 3.12** + FastAPI
- **Docker** (multi-stage, ARM/M1 compatible)
- **Jenkins** sur k8s local (Rancher Desktop)
- **DockerHub** comme registry

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/` | Message de bienvenue + environnement |
| GET | `/health` | Health check |
| GET | `/version` | Version de l'app (lue depuis `VERSION`) |

## Lancer en local (sans Docker)

```bash
pip install -r requirements.txt
uvicorn app.app:app --reload
```

## Lancer les tests

```bash
pytest tests/ -v
```

## Pipeline Jenkins

Le `Jenkinsfile` exécute manuellement (ou automatiquement via webhook) sur la branche `main` :

| Stage | Description | Statut |
|---|---|---|
| Checkout | Clone le repo GitHub | ✅ Actif |
| Test | `pytest` — 4 tests | ✅ Actif |
| Build | `docker build` — image taguée `VERSION-SHA` | ✅ Actif |
| Push | Push vers DockerHub (`adillabiad/mon-app`) | ✅ Actif |
| Deploy | `kubectl set image` dans le namespace `mon-app` | ⏸ Désactivé |

## Images Docker produites

Chaque build produit deux tags sur DockerHub :

```
adillabiad/mon-app:latest          ← toujours le plus récent
adillabiad/mon-app:0.1.0-a3f5c12  ← version sémantique + SHA git
```

## Infrastructure locale

| Composant | Namespace k8s | Accès |
|---|---|---|
| Jenkins | `jenkins` | `http://localhost:30080` |
| mon-app (futur) | `mon-app` | `http://localhost:31001` |

## Prochaines étapes

- [ ] Activer le stage Deploy (`k8s/deployment.yaml`)
- [ ] Configurer le webhook GitHub → Jenkins (via ngrok)
- [ ] Ajouter l'environnement `develop`
