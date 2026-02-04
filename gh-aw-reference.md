# GitHub Agentic Workflows (gh-aw) Reference

A quick reference for triggers, events, and safe-outputs in GitHub Agentic Workflows.

---

## 1. Triggers and Events

### Core GitHub Event Triggers

| Trigger | Description | Common Event Types |
|---------|-------------|-------------------|
| `issues` | React to issue events | `opened`, `edited`, `labeled`, `unlabeled`, `assigned`, `closed`, `reopened`, `deleted` |
| `pull_request` | React to PR events | `opened`, `synchronize`, `labeled`, `closed`, `review_requested`, `ready_for_review` |
| `issue_comment` | React to issue/PR comments | `created`, `edited`, `deleted` |
| `pull_request_review_comment` | React to PR review comments | `created`, `edited`, `deleted` |
| `discussion` | React to discussion events | `created`, `edited`, `labeled`, `answered` |
| `discussion_comment` | React to discussion comments | `created`, `edited`, `deleted` |
| `workflow_run` | Chain after other workflows | `completed`, `requested` |
| `workflow_dispatch` | Manual trigger from UI/API | Supports custom `inputs` |
| `push` | Commits pushed to branches | Filter by `branches`, `paths` |
| `schedule` | Cron-based recurring runs | Standard cron or human-friendly syntax |

### gh-aw Special Triggers

| Trigger | Description | Example |
|---------|-------------|---------|
| `slash_command` | Responds to `/command` in issues/PRs/comments | `on: /review-bot` |
| `on: daily` | Human-friendly daily schedule (scattered time) | `on: daily around 14:00` |
| `on: hourly` | Human-friendly hourly schedule | `on: every 6h` |
| `on: weekly` | Human-friendly weekly schedule | `on: weekly on monday` |
| `on: issue labeled X` | Shorthand for label-based triggers | `on: issue labeled bug, critical` |

### Schedule Formats

| Format | Example | Description |
|--------|---------|-------------|
| Fuzzy daily | `daily` | Compiler assigns scattered time |
| Fuzzy hourly | `hourly` | Compiler assigns scattered minute |
| Fuzzy weekly | `weekly on monday` | Scattered time on specific day |
| Around time | `daily around 14:00` | Scattered within ±1 hour |
| Between times | `daily between 9:00 and 17:00` | Scattered within range |
| With timezone | `daily around 3pm utc-5` | Supports UTC offsets |
| Interval | `every 6h` | Run at regular intervals |
| Standard cron | `cron: "30 6 * * 1"` | Fixed time (Monday 06:30 UTC) |

### Trigger Modifiers

| Modifier | Description | Example |
|----------|-------------|---------|
| `reaction` | Add emoji reaction on trigger | `reaction: "rocket"` |
| `stop-after` | Auto-disable after deadline | `stop-after: "+7d"` |
| `manual-approval` | Require approval via GitHub environments | `manual-approval: production` |
| `skip-if-match` | Skip if search query has matches | `skip-if-match: 'is:issue is:open label:bot'` |
| `skip-if-no-match` | Skip if search query has NO matches | `skip-if-no-match: 'is:pr label:ready'` |
| `lock-for-agent` | Lock issue during processing | `lock-for-agent: true` |
| `names` | Filter by label names | `names: [bug, critical]` |
| `forks` | Allow PRs from specific forks | `forks: ["trusted-org/*"]` |

### Available Reactions

| Value | Emoji |
|-------|-------|
| `+1` | 👍 |
| `-1` | 👎 |
| `laugh` | 😄 |
| `confused` | 😕 |
| `heart` | ❤️ |
| `hooray` | 🎉 |
| `rocket` | 🚀 |
| `eyes` | 👀 |

---

## 2. Things the AI Can Do (Safe-Outputs)

Safe-outputs define what write operations the AI agent can request. The AI runs with read-only permissions; write operations execute in separate jobs with minimal permissions.

### Issues & Discussions

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `create-issue` | Create new GitHub issues | 1 | `issues: write` |
| `update-issue` | Modify issue title, body, or status | 1 | `issues: write` |
| `close-issue` | Close issues with optional comment | 1 | `issues: write` |
| `link-sub-issue` | Create parent-child issue relationships | 1 | `issues: write` |
| `create-discussion` | Create repository discussions | 1 | `discussions: write` |
| `update-discussion` | Modify discussion title, body, or labels | 1 | `discussions: write` |
| `close-discussion` | Close discussions with resolution | 1 | `discussions: write` |

### Pull Requests

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `create-pull-request` | Create PRs with code changes | 1 | `contents: write`, `pull-requests: write` |
| `update-pull-request` | Modify PR title or body | 1 | `pull-requests: write` |
| `close-pull-request` | Close PRs without merging | 10 | `pull-requests: write` |
| `push-to-pull-request-branch` | Push commits to existing PR branch | 1 | `contents: write` |
| `create-pull-request-review-comment` | Add line-specific review comments | 10 | `pull-requests: write` |

### Comments & Labels

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `add-comment` | Post comments on issues, PRs, or discussions | 1 | `issues: write` or `pull-requests: write` |
| `hide-comment` | Minimize comments in GitHub UI | 5 | `issues: write` or `pull-requests: write` |
| `add-labels` | Add labels to issues or PRs | 3 | `issues: write` |

### Assignments & Reviews

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `add-reviewer` | Request PR reviews from users | 3 | `pull-requests: write` |
| `assign-to-user` | Assign users to issues | 1 | `issues: write` |
| `assign-to-agent` | Assign Copilot agents to issues | 1 | Custom token |
| `assign-milestone` | Assign issues to milestones | 1 | `issues: write` |

### Projects & Releases

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `create-project` | Create GitHub Projects boards | 1 | PAT with `project` scope |
| `update-project` | Modify project items and fields | 10 | PAT with `project` scope |
| `create-project-status-update` | Post project status updates | Unlimited | PAT with `project` scope |
| `update-release` | Modify release descriptions | 1 | `contents: write` |
| `upload-asset` | Upload files to orphaned branches | 10 | `contents: write` |

### Security & Agent Tasks

| Safe-Output | Description | Default Max | Permission |
|-------------|-------------|-------------|------------|
| `create-code-scanning-alert` | Generate SARIF security reports | Unlimited | `security-events: write` |
| `create-agent-session` | Create Copilot agent sessions | 1 | Custom token |

### System Tools (Always Available)

| Safe-Output | Description | Default Max |
|-------------|-------------|-------------|
| `missing-tool` | Report when AI needs unavailable functionality | Unlimited |
| `missing-data` | Report when AI needs unavailable data | Unlimited |
| `noop` | Log "nothing to do" for transparency | 1 |

### Safe-Output Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `max` | Limit number of operations per run | `max: 5` |
| `title-prefix` | Auto-prefix titles | `title-prefix: "[bot] "` |
| `labels` | Always apply these labels | `labels: [automated, ai]` |
| `allowed-labels` | Restrict what labels AI can add | `allowed-labels: [bug, feature]` |
| `target` | Specify target resource | `target: "triggering"`, `target: "*"`, `target: 123` |
| `target-repo` | Cross-repository operations | `target-repo: "org/other-repo"` |
| `expires` | Auto-close after time period | `expires: "7d"` |
| `staged` | Preview mode (no actual writes) | `staged: true` |
| `close-older-issues` | Close previous issues with same prefix | `close-older-issues: true` |
| `branch-prefix` | PR branch naming convention | `branch-prefix: "ai/"` |
| `allow-empty` | Allow PRs with no code changes | `allow-empty: true` |

### Target Values

| Value | Description |
|-------|-------------|
| `"triggering"` | Operate on the resource that triggered the workflow (default) |
| `"*"` | AI specifies target in its request |
| `123` | Always operate on specific issue/PR/discussion number |

### Cross-Repository Support

| Safe-Output | Cross-Repo Supported |
|-------------|---------------------|
| `create-issue` | ✅ |
| `update-issue` | ✅ |
| `add-comment` | ✅ |
| `add-labels` | ✅ |
| `create-discussion` | ✅ |
| `create-pull-request` | ✅ |
| `push-to-pull-request-branch` | ❌ (same repo only) |
| `upload-asset` | ❌ (same repo only) |
| `create-code-scanning-alert` | ❌ (same repo only) |
| `update-project` | ❌ (same repo only) |

---

## Quick Examples

### Issue Triage Bot
```yaml
on:
  issues:
    types: [opened]
safe-outputs:
  add-labels:
    max: 5
```

### Daily Report
```yaml
on: daily
safe-outputs:
  create-issue:
    title-prefix: "[report] "
    labels: [report]
    close-older-issues: true
```

### PR Review Bot
```yaml
on:
  pull_request:
    types: [opened, synchronize]
safe-outputs:
  add-comment:
    max: 1
  create-pull-request-review-comment:
    max: 10
```

### Slash Command
```yaml
on: /summarize
safe-outputs:
  add-comment:
    target: "triggering"
```

### Cross-Repo Tracker
```yaml
on: daily
safe-outputs:
  create-issue:
    target-repo: "org/central-tracker"
    title-prefix: "[upstream] "
```
