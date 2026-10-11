# C3 — The Abandoned Lab

## Purpose

C3 is the Stage 3, Moderate-difficulty Web Security challenge. It deliberately demonstrates SQL injection in a controlled lab. It is not safe to expose this service to the public Internet.

## Verified source layout

- `app.py`: Flask routes, login handling, archive page, session checks, and health endpoint.
- `init_db.py`: creates the SQLite `users` table and seeds a lab account.
- `requirements.txt`: Flask and Gunicorn dependencies.
- `Dockerfile`: builds a small Python image and runs the service as the non-root `c3user`.
- `compose.yaml`: defines the container, persistent SQLite volume, required secret variables, port binding, and health check.
- Container name: `zobi-c3-web-security`.
- Container port: `5003`; host port: `5003`.
- Database file: `/app/data/research.db` in the container.

## Security boundary

The unsafe SQL string concatenation is intentional for this challenge. Run it only in the authorised CTF lab. The application now requires `C3_FLAG` and `FLASK_SECRET_KEY` from the local environment rather than embedding the challenge flag or a default session key in source code.

The Compose default binds to `127.0.0.1:5003`. If participants must reach it from another machine, set `C3_BIND_ADDRESS` to the intended lab interface address in the local `.env` file and restrict access with the host firewall to the authorised participant network. Do not use `0.0.0.0` on a public or shared server without a reviewed firewall rule.

The Compose file refers to an external Docker network named `zobi_challenges`; create and inspect that network before starting the service. The network's existence alone does not prove isolation.

## First-time setup

Run on the authorised Ubuntu lab host from this directory:

```bash
cp .env.example .env
nano .env
```

Replace the placeholder values with the exact CTFd flag, a long random session secret, and a private C3_DEMO_PASSWORD for the seeded lab account. Do not commit `.env` or show its contents in screenshots.

Create the network if it does not already exist:

```bash
docker network inspect zobi_challenges >/dev/null 2>&1 || \
  docker network create --driver bridge --subnet 172.20.0.0/24 --gateway 172.20.0.1 zobi_challenges
```

Before using the network, inspect its configuration and confirm it matches the approved isolation design:

```bash
docker network inspect zobi_challenges
```

Build and start the service:

```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail=100 c3-web-security
curl -i http://127.0.0.1:5003/health
```

Expected health response:

```json
{"service":"The Abandoned Lab","status":"running"}
```

## Intended participant workflow

1. Open the Research Portal from the authorised lab network.
2. Test ordinary invalid credentials and observe the rejection.
3. Investigate how the login form's input is incorporated into the database query.
4. Demonstrate the deliberately vulnerable SQL query using the intended challenge method.
5. Access the protected archive, recover the configured flag, and submit it to CTFd.
6. Confirm a correct submission is accepted and an incorrect submission is rejected.

The archive also contains the clue about Dr. Alex's computer. Ensure that clue is consistent with the next challenge in the deployed CTFd event.

## Local automated tests

The repository includes `tests/test_app.py`. Run tests with the Python environment and Flask dependencies installed:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

These tests check application routes and the intended lab-only SQL injection behaviour using a temporary database. They do not test Docker networking, CTFd configuration, flag submission, or host firewall isolation.

## Operations and recovery

Restart without deleting persistent data:

```bash
docker compose restart c3-web-security
docker compose ps
curl -i http://127.0.0.1:5003/health
```

To rebuild the image while preserving the database volume:

```bash
docker compose up -d --build
```

Do not run `docker compose down -v` unless the team explicitly intends to erase the C3 database. Back up the approved volume before any destructive reset.

## Acceptance evidence to capture

- `docker compose ps` showing the running/healthy container.
- `/health` response.
- Normal invalid login rejected.
- Intended SQL injection path succeeds in the lab.
- Correct C3 flag accepted and wrong flag rejected in CTFd.
- Firewall and binding checks showing only the intended network can reach the service.
- Reset/recovery followed by a successful health check.

Do not label a test passed until it has been executed and evidence saved.
