# docker-aws-ecr-project

A small Flask web app, packaged as a Docker image and stored in a private Amazon ECR repository. I built this project to practise containerising an application and working with AWS container tooling.

## What it does

The app runs on port `5004` and has two routes:

| Route | Response |
|---|---|
| `/` | `Hello, World! This is practice` |
| `/health` | `Health check OK` |

The `/health` route gives a simple way to check that the app is up, which is useful for container platforms and load balancers.

## Tech used

- **Python 3.12** and **Flask**: the web app
- **Docker**: packages the app and its dependencies into an image
- **Docker Compose**: runs the container with its port mapping and restart policy
- **Amazon ECR**: private registry that stores the image
- **AWS CLI**: authenticates Docker with ECR
- **Git and GitHub**: version control

## Project structure

```text
docker-aws-ecr-project/
├── health.py            # Flask app with / and /health routes
├── requirements.txt     # Python dependencies (Flask)
├── Dockerfile           # Instructions for building the image
├── .dockerignore        # Files kept out of the image (.venv, .git)
├── docker-compose.yml   # Runs the image from ECR on port 5004
├── .gitignore           # Files kept out of Git (.venv)
└── README.md
```

## How it was built

### 1. The Flask app
`health.py` defines the two routes. It listens on `0.0.0.0` rather than `127.0.0.1` so it accepts connections from outside the container.

### 2. The Dockerfile
- Starts from the lightweight `python:3.12-slim` base image.
- Copies `requirements.txt` and installs dependencies **before** copying the rest of the code. Docker caches the dependency layer, so code changes don't trigger a reinstall.
- Exposes port `5004` and starts the app with an exec-form `CMD`.

### 3. Keeping unwanted files out
- `.dockerignore` stops `COPY . .` from copying the local virtual environment and Git history into the image. That keeps the image smaller and avoids putting macOS-built packages into a Linux container.
- `.gitignore` keeps the virtual environment out of the GitHub repository.

### 4. Pushing to Amazon ECR
1. Created a private ECR repository with image scanning turned on.
2. Authenticated Docker with ECR using the AWS CLI.
3. Tagged the image with the repository URI and a version tag.
4. Pushed the image and reviewed the scan results in the ECR console.
5. Set `docker-compose.yml` to pull the image from ECR.

## Running it locally

Install Python dependencies and run the app directly:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python health.py
```

Or build and run it with Docker:

```bash
docker build -t docker-aws-ecr-project .
docker run -p 5004:5004 docker-aws-ecr-project
```

Then open <http://localhost:5004> and <http://localhost:5004/health>.

## What I learned

- **Duplicate Flask function names break routing.** Flask names each route after its function, so two routes that both used `hello_world` caused an `AssertionError`. Giving each route its own function fixed it.
- **`CMD` syntax matters.** The exec form uses square brackets and needs the exact filename, including `.py`.
- **`.dockerignore` and `.gitignore` do different jobs.** One controls what goes into the image; the other controls what goes into Git.
- **Managing two GitHub accounts over SSH.** I used an SSH host alias with `IdentitiesOnly yes` so pushes to this repo use my personal key.
- **Merging unrelated histories.** The GitHub repo was created with a README, so its history didn't share a commit with my local repo. I merged them with `--allow-unrelated-histories` instead of force-pushing.

## Next steps

- Run the container as a non-root user.
- Deploy the image from ECR to **Amazon ECS on Fargate**.
- Build and push the image automatically with **GitHub Actions**, using OIDC instead of stored AWS keys.
- Add an ECR lifecycle policy to delete old images.
