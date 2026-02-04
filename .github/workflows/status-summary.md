---
name: Status Update Summary
on: every 12h
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, projects]
safe-outputs:
  create-project-status-update:
---

Read all recent status updates from Project #2 since the last SUMMARY update (or the last 12 hours if no prior summary exists).

Create a new project status update that:

1. Summarizes all individual status updates into a cohesive overview
2. Groups by theme (completed work, in-progress items, blockers)
3. Highlights key accomplishments and any patterns
4. Notes how many issues were closed in this period

Start the body with **SUMMARY** on the first line so it's easy to identify.
Keep it concise but comprehensive (5-8 sentences max).
