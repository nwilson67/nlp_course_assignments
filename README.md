# Course Assignments for Intro to NLP
Assignments associated with DSAI 5810/6810 Fall 2025 Intro to NLP.

## Setup Instructions

1. First fork this repo ("Create New Fork"). 

<img src="images/Screenshot%202025-08-22%20at%208.40.27%E2%80%AFPM.png" alt="drawing" width="200"/>

2. Make repo private.

3. Add me (Matt) as a contributor.

4. To get updates from the original repo run the following:

Add upstream original repo. Only need to do this once. URL should be the HTTPS URL of the original repo.
```commandline
git remote add upstream [URL_of_original_repo]
```

Fetch latest updates
```commandline
git fetch upstream
```

Finally, make sure to switch to your main branch (git checkout) and merge in the latest from the original repo.
```commandline
git checkout main
git merge upstream/main
```

## Submitting an Assignment
When submitting an assignment, make a PR and add me as a reviewer.

To do this for each assignment:
- Create a new branch. Do your assignment on this branch.
- While on the new branch, once you add or edit a file and you feel good about the changes, run `git add [file_name]`
- Then run `git commit -m "write a commit message here"`
- Then run `git push` to push your local changes to the remote repo (Github)

Then when you've submitted all of your changes, go to the branch on Github and create a Pull Request and add me as a reviewer.
I'll review your PR and then you can merge your PR into main.

Some other helpful git commands:
- `git status`: see the current status from gits perspective
- `git diff [file_name]`: see what changes you will be adding and committing.