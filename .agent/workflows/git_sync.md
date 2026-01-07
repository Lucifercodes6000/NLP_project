---
description: "Sync local changes to the remote git repository."
---

1. Check the current status of the repository.
   ```bash
   git status
   ```

// turbo
2. Add all changes to the staging area.
   ```bash
   git add .
   ```

3. Commit the changes. Replace "work in progress" with a specific message if needed.
   ```bash
   git commit -m "update: periodic sync of local work"
   ```

4. Push the changes to the remote repository.
   ```bash
   git push
   ```
