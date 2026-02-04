---
name: Issue Closed Status Update
on:
  issues:
    types: [closed]
permissions:
  contents: read
  issues: read
  pull-requests: read
tools:
  github:
    toolsets: [default, projects]
safe-outputs:
  create-project-status-update:
  add-comment:
    max: 1
---

An issue was just closed. Do two things:

1. **Project status update** for Project #2:
   - What was completed (issue title + brief summary)
   - Who did the work (closer + assignees)
   - Resolution (completed, won't fix, or duplicate)
   - Keep it concise (2-3 sentences max)
   - **Status logic**: Check the remaining open issues in the project backlog. Only set status to COMPLETE if there are zero open issues remaining. Otherwise use ON_TRACK (or AT_RISK if there are blockers).

2. **Post a comment on the issue** with a Slack-ready message formatted like:
   ✅ **[Issue title]** — completed by @user
   > One sentence summary of what was done.
   Format it so I can copy/paste directly into Slack.
