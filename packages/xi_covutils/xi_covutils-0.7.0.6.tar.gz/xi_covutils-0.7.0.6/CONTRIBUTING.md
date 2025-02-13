# Contribution guidelines

## For a new feature / bug fix

- Report an issue.
- Create a new i/issue_number branch.
- After resolve issue, check this before pushing a new branch.
  - Add type annotations for new functions.
  - Run tests / pylint.
  - Update documentation.
  - Update README.md
  - Update requeriments.txt file.
  - Update setup.py requirements.
  - Update development_requirements.txt.
  - Update MANIFEST.in.
  - Update version with bump_version.py script.
  - Modify Changelog.
- Create a merge request from the issue branch to master.
- Merge the branch or wait to other to merge it.
- Add a new TAG if consider that enough changes have accumulated
  from last tagged version.
- Push commit and tag to remote repository.
