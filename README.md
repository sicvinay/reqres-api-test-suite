# ReqRes API Test Suite

Python API automation with **Pytest, Requests, JSON Schema and requests-mock**.
Refactored from an earlier technical exercise covering the ReqRes demo Users API.

This repository focuses on client reliability and contract validation. It complements
my student workflow automation project with schemas, transport-failure checks,
credential handling, and separate offline/live execution.

## Quick start

Use Python 3.12 or newer. From the repository root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
python -m pip install -r requirements.txt
python -m pytest
python -m pytest -n 2 -m "not live" --html=reports/report.html --self-contained-html
```

Open `reports/report.html` in your browser. The default run executes 43 offline
tests and explicitly skips the 5 opt-in live tests. GitHub Actions executes the
offline tests on Linux and Windows using Python 3.12, 3.13 and 3.14.

## Two explicit verification modes

| Mode | What it proves | Network |
| --- | --- | --- |
| Default offline | Client routing, JSON encoding, schema checks, input guards, error propagation and data loading | HTTP responses are stubbed with requests-mock; unmatched requests fail |
| `--live -m live` | Actual ReqRes demo CRUD response contracts and missing-user behavior | Real requests to ReqRes |

**Offline green tests do not prove ReqRes is available or behaving correctly.**
Response fixtures are synthetic examples of the expected contract, not recordings
from a verified live run. No local replacement API is presented as ReqRes.

## Live API tests

The classic ReqRes `/api/users` endpoints return fixture data. Their POST, PUT
and DELETE responses do **not persist changes**. The suite therefore verifies
returned fields/statuses, and does not pretend to read back a newly created or
updated user. Classic demo requests can currently run anonymously with a daily
limit. An optional API key can be provided through the environment if needed.

```bash
python -m pytest --live -m live -v --html=reports/live.html --self-contained-html
```

Optional Windows PowerShell configuration:

```powershell
$env:REQRES_API_KEY = "your-own-key"
$env:REQUEST_TIMEOUT = "10"
```

Optional Bash configuration:

```bash
export REQRES_API_KEY="your-own-key"
export REQUEST_TIMEOUT="10"
```

`.env.example` documents names only; files named `.env` are not automatically
loaded. Never commit an API key. Live mode is deliberately restricted to
`https://reqres.in/api` to avoid accidentally targeting a persistent application.
Rate limits, authentication changes, service outages and network restrictions are
reported as live test failures, not silently skipped or converted into passes.

## Coverage

- Create user: payload encoding, 201, name/job, generated ID and creation timestamp field.
- Read user: 200 and nested user/support schema validation.
- Update user: 200, echoed fields and update timestamp field.
- Delete user: 204 and an empty body; no JSON decoding of an empty response.
- Negative cases: invalid input, invalid IDs, missing user, malformed response JSON,
  broken schemas, timeouts and connection errors.
- Utilities: environment configuration, credential redaction, path safety,
  missing/malformed test data and independence from the working directory.

Request schemas enforce this client's non-empty `name`/`job` convention. These
are **client-side rules**, not claims that ReqRes rejects all missing fields.
Response timestamp schemas check non-empty strings; they do not validate date
formats. The integer ID guard is also a client-side rule.

## Layout

| Directory/file | Purpose |
| --- | --- |
| `utils/config.py` | Environment configuration, finite timeout and URL validation |
| `utils/request_helper.py` | Reusable session, timeout and redacted request logging |
| `utils/users.py` | User operations and input validation |
| `utils/contracts.py` | JSON response parsing and schema validation |
| `utils/data_loader.py` | Portable UTF-8 JSON loading |
| `schemas/` | Request and response JSON Schema definitions |
| `data/` | Synthetic input data and offline response fixtures |
| `tests/test_crud_contracts.py` | Offline CRUD contracts |
| `tests/test_negative_cases.py` | Input, schema, protocol and transport negatives |
| `tests/test_utilities.py` | Configuration, loading and logging checks |
| `tests/test_live_reqres.py` | Explicitly enabled real API tests |
| `.github/workflows/tests.yml` | Six-job OS/Python CI matrix and HTML/JUnit artifacts |

Useful selections:

```bash
python -m pytest -m smoke
python -m pytest -m negative
python -m pytest tests/test_crud_contracts.py::test_delete_user_has_empty_body
```

## Improvements over the original

Eight placeholder negative tests no longer pass without assertions. Replacements
make their scope explicit rather than inventing unsupported server behavior.
The shared key, stale reports, IDE files, virtual environment, archived outputs
and unrelated scratch script are excluded. Sessions are closed after each test,
requests use a timeout, delete tests check the empty body directly, and ID fields
are kept out of update request payloads.

This is an independent portfolio project using public API documentation and
synthetic data. It contains no company application, internal endpoints or company
branding and makes no claim of employer endorsement.

## References

- [ReqRes documentation](https://reqres.in/docs)
- [Classic fake Users API behavior](https://reqres.in/fake-users-api)
- [JSON Schema validation](https://python-jsonschema.readthedocs.io/)
- [requests-mock](https://requests-mock.readthedocs.io/)
