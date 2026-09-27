# Project agent instructions

## Mandatory context maintenance

The user requires `AI_PROJECT_CONTEXT.md` to be updated for **every user prompt concerning this project**, including questions, clarification, implementation, debugging, and documentation requests.

- Read `AI_PROJECT_CONTEXT.md` before working.
- Before the final response, update it with the current request, resulting decisions or clarification, changes made, verification performed, and any outstanding work relevant to that prompt.
- For a question-only turn, record the relevant clarification without claiming code changes or tests occurred. If no project facts changed, state that briefly in the latest-interaction entry.
- Maintain a concise `Latest interaction` section, replacing its prior contents each turn. Integrate enduring facts into the appropriate sections; do not append the entire conversation or duplicate existing material.
- Correct superseded facts and distinguish planned work from completed, tested work. Do not copy secrets or unnecessary personal information into context.
- Preserve unrelated user changes. If updating the file is blocked, report that limitation rather than claiming the context was updated.

This rule was explicitly requested by the project owner. Follow the user's current instructions if they amend it.
