# Total Replace Instructions

1. Keep a backup of the current documentation folder.
2. Extract this ZIP outside the repository and inspect `MANIFEST.txt`.
3. Replace the documentation root with the contents of this package, not the enclosing ZIP directory if your repository already has its own root.
4. Keep source Markdown and `assets/diagrams`; do not keep only Word/PDF exports.
5. Review `git diff --stat` and `git diff --check`.
6. Search for secrets before commit.
7. Commit on a documentation branch using explicit paths.

Suggested commit message:

```text
docs(gaia): reconstruct reference and sprint documentation
```
