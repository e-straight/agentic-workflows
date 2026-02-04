---
name: Issue Closed Status Update
on:
  issues:
    types: [closed]
permissions:
  contents: read
  issues: read
  pull-requests: read
safe-outputs:
  create-project-status-update:
---

An issue was just closed. Create a project status update for Project #2 that includes:

1. **What was completed**: The issue title and a brief summary of what it addressed
2. **Who did the work**: The user who closed the issue and any assignees
3. **Resolution**: Whether it was completed, won't fix, or duplicate

Keep the update concise (2-3 sentences max).
