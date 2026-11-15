| # | Area | The question to answer | Evidence | Finding | Disposition |
|---|---|---|---|---|---|
| 1 | **Secrets** | Is any credential in the repository, in its history, in a log, or in a screenshot? | | | |
| 2 | **Input** | Does every externally supplied value get validated and safely parameterized before it reaches a query, a shell, a path, or a template? | | | |
| 3 | **Authentication** | Can a request act as a user without proving it is that user? Are sessions and password storage handled by a maintained library rather than by you? | | | |
| 4 | **Authorization** | For every object a user can name, is ownership checked *server-side* on every request — not just hidden in the UI? | | | |
| 5 | **Transport & storage** | Is traffic HTTPS end to end? Is anything sensitive stored that you do not actually need? | | | |
| 6 | **Dependencies** | Does any direct or transitive dependency carry a published advisory? Which, and what did you do? | | | |
| 7 | **Errors & logging** | Do error responses leak stack traces, queries, paths, or tokens? Do logs contain secrets or personal data? | | | |
