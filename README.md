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

## Environnement

| Branche Git | Namespace k8s | Image Docker | Port local |
|---|---|---|---|
| `main` | `app-prod` | `mon-app:latest` | `31001` |

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

Le `Jenkinsfile` exécute à chaque push sur `main` :
1. Checkout du code
2. Tests pytest
3. Build image Docker
4. Push vers DockerHub
5. Deploy dans le namespace `app-prod`
