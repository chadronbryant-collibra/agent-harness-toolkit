# Check a connection

Use the account and service already available in your client. A successful check means the assistant opened one item you selected on the expected account.

## GitHub

> Check whether you can use GitHub on my intended account. Read the repository details for the repository I name. Show me the account, repository, and default branch.

Use an existing GitHub connector if the client exposes it, or the GitHub CLI if installed. If sign-in is needed, use that client's supported sign-in flow. With the CLI, the person can confirm the active account with `gh api user --jq .login` and the target with `gh repo view OWNER/REPO --json nameWithOwner,visibility,defaultBranchRef`. Read permissions and permission to push are separate.

## Google Workspace

> Check whether this session can open a Google Drive file on my intended account. Use the file link I give you and report whether you could open it.

Use a Google Workspace connector already exposed in the session. If none is available, guide the person to their client's connector settings. An organization may manage which connections can be added. Verify the connected account and read the metadata or content needed for the named file only. Report the result as opened, denied, or unavailable. Request permission changes only if the selected task needs them.

The toolkit's sample files, skills, and setup helper use local files. The connector uses the selected account and its own permissions and usage rules. To disconnect, use the client that granted access.

[GitHub CLI authentication](https://cli.github.com/manual/gh_auth_status) · [Claude integrations](https://code.claude.com/docs/en/mcp)
