# Token & secret rotation — portfolio entry point

## PROFILE_REPO_TOKEN

**Purpose:** GitHub Actions in `mahmood726-cyber/mahmood726-cyber.github.io` uses this PAT to push a regenerated `README.md` into `mahmood726-cyber/mahmood726-cyber` (the profile-readme repo whose contents render at the top of the GitHub profile page).

**Where stored:** Repo-level Actions secret named `PROFILE_REPO_TOKEN` on the `mahmood726-cyber.github.io` repository. Settings → Secrets and variables → Actions → New repository secret.

**Scope:** Fine-grained PAT, *not* classic.

- **Resource owner:** `mahmood726-cyber`
- **Repository access:** Only select `mahmood726-cyber/mahmood726-cyber`
- **Repository permissions:** `Contents` = Read and write. Nothing else.
- **Expiration:** 90 days. Calendar reminder lives in `C:\Users\user\.claude\projects\C--Users-user\memory\` (project memory entry).

**To create:** https://github.com/settings/personal-access-tokens/new

**To rotate:**

1. Create a new fine-grained PAT with the same scope.
2. Update the `PROFILE_REPO_TOKEN` secret value in repo settings, or via:
   ```
   gh secret set PROFILE_REPO_TOKEN --repo mahmood726-cyber/mahmood726-cyber.github.io --body "<new-token>"
   ```
3. Trigger a manual workflow run via Actions → Build site → Run workflow, confirm the profile-README push step succeeded.
4. Delete the old PAT.

## ORCID placeholder

`data/site.yaml::footer.orcid` ships as `0000-0000-0000-0000`. Replace with the real ORCID before first push to master. Can be left as placeholder during local testing.
