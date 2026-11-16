# Validation

Validated on 16 November 2026 using Python 3.12 on Linux.

- Default run: 43 passed, 5 live tests explicitly skipped.
- Parallel offline run (two workers): 43 passed.
- Delete contract test run individually: 1 passed.
- HTML and JUnit reports generated successfully.
- Source scan: no empty test placeholders or obvious credential patterns.

Offline tests use synthetic HTTP stubs; this does not establish live ReqRes
behavior or availability. Live API tests were not run during local validation.
The CI matrix covers Linux and Windows on Python 3.12, 3.13 and 3.14.
