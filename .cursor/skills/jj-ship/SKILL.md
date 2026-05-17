---
name: jj-ship
description: >-
  Ships the current Jujutsu working copy with status review, a clear change
  description, commit, bookmark update, and git push. Use when the user wants
  to commit, push, publish, or ship changes in a jj-managed repo, or mentions
  jj commit, jj git push, or finishing a change.
disable-model-invocation: true
compatibility: Requires the `jj` CLI only (no Jujutsu MCP). Repository should be Jujutsu-backed (typically `.jj/` present). Network needed for `jj git push`.
---

# jj ship (commit + push)

Run this workflow only when the user asked to ship, commit, push, or finish a jj change. Do not use raw `git commit` / `git push` in a jj repo unless the user explicitly requests Git. Use **only** `jj` subcommands in the shell—do not call Jujutsu MCP tools from this workflow.

## Before you start

1. Confirm the workspace root is the intended repository.
2. Run `jj status` and read conflicts / working-copy state from that output.
3. If the status shows conflicts or an unexpected state, stop and report; do not commit.
4. **Data Leak Prevention (Strictly Local):** Verify that no proprietary or sensitive assets—such as raw/processed images, CSV datasets, or trained model checkpoints (`.pt`, `.onnx`, etc.)—are included in the working copy. These files are strictly internal and must **never** leave the local environment or be pushed to a remote repository. Ensure they are explicitly ignored via `.gitignore` or `.jjignore`.

## Describe the change

1. Summarize what will ship in one short title line plus optional body (Conventional Commits if the project already uses them: `feat:`, `fix:`, etc.).
2. If the user gave an exact message, use it verbatim (after trimming).
3. If the working copy is empty, stop and say there is nothing to commit.

## Commit

1. Ensure the change description is set on the revision you are shipping:
   - Prefer: `jj describe -r @ -m "Title line" -m "Optional body paragraph."`
   - Or match whatever one-line style the user already uses in this repo.
2. Create the commit on the current change:
   - `jj commit -m "Same title as describe, or user-provided message"`
   - If `jj commit` fails, print the error and stop.

## Bookmarks (when pushing to a tracked branch)

If this repo uses a bookmark named `main` (or the user names another), update it after a successful commit.

After `jj commit`, the working copy moves to a new empty child revision: the commit you shipped is **`@-`**, not `@`. Point the bookmark at that revision:

```bash
jj bookmark set main -r @-

```

Use the bookmark name the user specifies; default only when they agree `main` is correct.

## Push

1. Run `jj git push` (or the project’s documented variant).
2. If push fails (auth, non-fast-forward, remote rejected), stop with the remote message; do not `--force` unless the user explicitly asks.

### When `jj git push` reports nothing to do

If the output is **“Nothing changed”** while you know local commits are ahead of the remote, or you see a warning like **non-tracking remote bookmark `main@origin**`, the local bookmark is not **tracking** the remote yet. Jujutsu will not move `origin/main` until tracking is set (or you push the bookmark explicitly).

1. Track the remote bookmark (once per clone / until configured):
```bash
jj bookmark track main --remote=origin
```
Use the same bookmark and remote names the repo uses.

2. Push that bookmark and the commits it covers:

```bash
jj git push --bookmark main --remote origin   

```

After that, ordinary `jj git push` (or `--tracked`) usually works for later ships. If the hint names a different remote or bookmark, follow it.

## Aftercare

1. Run `jj status` again and briefly confirm clean or expected state.
2. Tell the user the revision identifier or bookmark you pushed to, if helpful.

## Out of scope unless asked

* Rebases, squashes, abandoning changes, conflict resolution: use the general jujutsu skill or user instructions.
* Signing commits, tags, releases: only if the user requests.
