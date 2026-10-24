# Git Workflow Guide

Reference for day-to-day development on this project: branches, environments, and the commands used at each step.

---

## Branches and environments

| Branch | Purpose | Deploys to | Commit directly? |
|---|---|---|---|
| `main` | Stable, working version | Production | No, pull requests only |
| `develop` | Integration of finished features | Staging | No, pull requests only |
| `feature/*` | One branch per task | Local only (plus preview deployments) | Yes |
| `hotfix/*` | Urgent fix to production | Local only | Yes |

Code always flows in one direction:

```
feature/*  ──►  develop  ──►  main
 (local)       (staging)   (production)
```

---

## Branch naming

Use lowercase and hyphens, prefixed by type:

- `feature/url-shortener-expansion`
- `feature/whois-domain-age`
- `fix/cors-staging-origin`
- `docs/api-endpoints`
- `hotfix/broken-analyse-endpoint`

---

## Commit messages

Write in the imperative ("Add", not "Added"), keep the first line under ~70 characters.

```
<type>: <short summary>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:

```
feat: add WHOIS domain age check
fix: block private IP ranges in URL fetcher
docs: add environment variable setup to README
test: add unit tests for shortener expansion
```

---

## 1. Starting a new task

```bash
git checkout develop          # switch to develop
git pull                      # get the latest version
git checkout -b feature/task-name   # create and switch to a new branch
```

Check you're on the right branch before writing any code:

```bash
git branch                    # current branch is marked with *
```

---

## 2. While working

```bash
git status                    # see what has changed
git diff                      # see the exact changes (unstaged)
git add <file>                # stage a specific file
git add .                     # stage everything in the current folder
git commit -m "feat: short description"
git push                      # push commits (first push: see below)
```

First push of a new branch:

```bash
git push -u origin feature/task-name
```

Commit little and often. Push at least at the end of each working session so work is backed up.

---

## 3. Finishing a feature (to staging)

1. Make sure everything is committed and pushed:
   ```bash
   git status
   git push
   ```
2. On GitHub, open a **pull request** from `feature/task-name` into `develop`.
3. Write a short description: what changed, why, and which sprint task it relates to.
4. Merge the pull request.
5. Staging deploys automatically. Test the feature on the staging URL.
6. Clean up locally:
   ```bash
   git checkout develop
   git pull
   git branch -d feature/task-name
   ```

---

## 4. Releasing to production (end of sprint)

Only do this when staging is working and tested.

1. On GitHub, open a **pull request** from `develop` into `main`.
2. Title it with the sprint, e.g. `Sprint 3 release`, and list the features included.
3. Merge the pull request.
4. Production deploys automatically. Check the production URL works.

---

## 5. Keeping a feature branch up to date

If `develop` has moved on while you're working on a long-running branch:

```bash
git checkout develop
git pull
git checkout feature/task-name
git merge develop
```

Resolve any conflicts, then commit and push.

---

## 6. Hotfix (production is broken)

```bash
git checkout main
git pull
git checkout -b hotfix/short-description
# fix, commit, push
git push -u origin hotfix/short-description
```

1. Open a pull request from `hotfix/...` into `main` and merge it.
2. Bring the fix back into `develop` so it isn't lost:
   ```bash
   git checkout develop
   git pull
   git merge main
   git push
   ```

---

## 7. Environment variables

- Real secrets live in `.env` files locally and in each hosting platform's settings online.
- `.env` and `.env.local` are in `.gitignore` and must **never** be committed.
- `.env.example` (committed) lists the variable names with no values.
- Staging and production use **separate** API keys.

After adding a new variable:

1. Add it to your local `.env`
2. Add the name to `.env.example` and commit
3. Add it to the staging **and** production settings on the hosting platforms

---

## 8. Useful commands

```bash
git log --oneline --graph     # compact history with branch structure
git log --oneline -10         # last 10 commits
git branch -a                 # list local and remote branches
git fetch --prune             # update remote info, remove deleted branches
git stash                     # temporarily shelve uncommitted changes
git stash pop                 # bring shelved changes back
git push origin --delete feature/task-name   # delete a remote branch
```

---

## 9. Fixing mistakes

**Discard changes to a file (not yet staged):**
```bash
git restore <file>
```

**Unstage a file (keep the changes):**
```bash
git restore --staged <file>
```

**Undo the last commit but keep the changes (not yet pushed):**
```bash
git reset --soft HEAD~1
```

**Fix the last commit message (not yet pushed):**
```bash
git commit --amend -m "new message"
```

**Committed to `develop` by mistake instead of a feature branch (not yet pushed):**
```bash
git branch feature/task-name    # save the commit onto a new branch
git reset --hard HEAD~1         # remove it from develop
git checkout feature/task-name  # carry on working here
```

**Committed a secret (API key, password):**
1. Revoke the key on the provider's site immediately and generate a new one. Deleting the file is not enough; it stays in git history.
2. Remove the file from tracking and make sure it's in `.gitignore`:
   ```bash
   git rm --cached .env
   git commit -m "chore: stop tracking .env"
   ```
3. Update the new key in your local `.env` and on the hosting platforms.

> Avoid `reset --hard`, `push --force`, or rewriting history on `main` or `develop`. If something has already been pushed, fix it with a new commit instead.

---

## Daily checklist

- [ ] `git checkout develop && git pull` before starting anything new
- [ ] Working on a feature branch, not `develop` or `main`
- [ ] Commits are small with clear messages
- [ ] Everything pushed before finishing for the day
- [ ] No `.env` files or secrets in `git status`
- [ ] Features tested on staging before merging into `main`