pipeline {
    agent any

    // ── Variables globales ───────────────────────────────────
    environment {
        DOCKERHUB_USER  = "adillabiad"
        IMAGE_NAME      = "mon-app"
        APP_VERSION     = sh(script: "cat VERSION", returnStdout: true).trim()
        IMAGE_TAG       = "${APP_VERSION}-${GIT_COMMIT[0..6]}"         // ex: 0.1.0-a3f5c12
        DOCKERHUB_CREDS = credentials("dockerhub-secret")
    }

    stages {

        // ── 1. CHECKOUT ──────────────────────────────────────
        stage("Checkout") {
            steps {
                checkout scm
            }
        }

        // ── 2. TEST ──────────────────────────────────────────
        stage("Test") {
            steps {
                sh """
                    docker run --rm \
                        -v \$(pwd):/app \
                        -w /app \
                        python:3.12-slim \
                        sh -c "pip install --quiet -r requirements.txt && pytest tests/ -v --tb=short"
                """
            }
        }

        // ── 3. BUILD IMAGE ───────────────────────────────────
        stage("Build") {
            steps {
                sh """
                    docker build \
                        --platform linux/amd64 \
                        -t ${DOCKERHUB_USER}/${IMAGE_NAME}:latest \
                        -t ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG} \
                        .
                """
            }
        }

        // ── 4. PUSH DOCKERHUB ────────────────────────────────
        stage("Push") {
            steps {
                sh """
                    echo ${DOCKERHUB_CREDS_PSW} | docker login -u ${DOCKERHUB_CREDS_USR} --password-stdin
                    docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:latest
                    docker push ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}
                """
            }
        }

        // ── 5. DEPLOY ────────────────────────────────────────
        stage("Deploy") {
            steps {
                sh """
                    kubectl set image deployment/mon-app \
                        mon-app=${DOCKERHUB_USER}/${IMAGE_NAME}:latest \
                        -n mon-app
                """
            }
        }
    }

    // ── POST : notifications ─────────────────────────────────
    post {
        success {
            echo "Pipeline réussi — image: ${DOCKERHUB_USER}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo "Pipeline échoué"
        }
    }
}
