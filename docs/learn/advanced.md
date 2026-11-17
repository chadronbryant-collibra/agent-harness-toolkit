# Optional tools for advanced setups

These commands are already included. Run them from the extracted toolkit. Use Python 3.11 or later. Substitute your Python command and workspace location as needed. Quote paths with spaces.

## Copy a starter preset

```text
python3 kit.py list
python3 kit.py --workspace "/path/to/your folder" add write-a-brief
python3 kit.py --workspace "/path/to/your folder" add write-a-brief --apply-plan PLAN_SHA256
```

The first add shows exactly what would be copied. Use its digest to apply the reviewed plan. An edited destination is kept and reported as a conflict. Identical files are skipped. Repeat with `context` or `references` if useful. A copy receipt does not show whether Claude loaded the skill. Reopen the target folder and invoke it.

## Try searchable memory

Pick a local practice folder with appropriate access and backup settings. Add `.harness/` to the workspace's Git ignore rules if applicable. The memory preset adds an enabled configuration without creating a store or saving anything. Apply the preview only after you choose to enable memory in that folder.

```text
python3 kit.py --workspace "/path/to/practice" add memory
python3 kit.py --workspace "/path/to/practice" add memory --apply-plan PLAN_SHA256
```

If you already have a toolkit configuration, keep it. Ask Claude to show the change to the existing `memory.enabled` setting and apply it only when you choose. Then try a fictional preference.

```text
python3 kit.py --workspace "/path/to/practice" memory-status
python3 toolkit.py --workspace "/path/to/practice" memory remember --text "Put blockers first in a brief" --source "user:practice"
python3 toolkit.py --workspace "/path/to/practice" memory search --text "blockers first"
python3 toolkit.py --workspace "/path/to/practice" memory forget --id RETURNED_ID
```

In a new session, give Claude the toolkit and workspace locations and ask it to find the saved preference. For a real decision, save a link or path to its source and reopen it before relying on the decision. The examples pass harmless text on the command line. Keep secrets and sensitive material out of the store and command history. Removing an item from results does not erase every backup.

## Check the selected Apps Script or Google Cloud project

Try these checks from the toolkit with the bundled fictional files.

```text
python3 kit.py check-project clasp --file examples/advanced/clasp-project.json --expected fictional-script-id
python3 kit.py check-project gcloud --file examples/advanced/gcloud-project.ini --expected example-project
```

For Apps Script, point the check at your project's `.clasp.json` inside the selected workspace. For Google Cloud, select the directory containing the configuration you want to inspect as the workspace and pass its relative configuration filename. The check compares the local project with the one you intended and reports whether the CLI is available. It never needs a token or prints the configuration file. Account and resource access need a separate check through the signed-in tool. Use the vendor guides for sign-in and any live operation.

[Apps Script clasp guide](https://developers.google.com/apps-script/guides/clasp) · [Google Cloud named configurations](https://cloud.google.com/sdk/gcloud/reference/config/configurations)

These scripts run locally without Claude calls. When Claude runs them on your behalf, its conversation uses your account's regular billing. A separately installed service may charge for its own work. Check the operation and applicable limit before invoking it. [Spending controls](../models-and-cost.md)
