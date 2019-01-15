# Branching and Pull Requests

In order to contribute to conflict-free development of this repository, we suggest implementing localized branches and submitting pull requests.

## A. Forking and cloning from source

First we need to fork the original repository and clone it onto your personal workspace.

1. Fork this repository from GitHub onto your personal account

2. Clone this repository onto your personal workspace

```shell
$ git clone https://github.com/<youraccount>/anlp_ws18
```

3. Add our original repository as an additional remote URL

```shell
$ git remote add upstream https://github.com/glaserL/anlp_ws18
```

4. Before committing any changes, ensure your forked repository is synced with all the updates from the original repository

```shell
$ git fetch upstream

$ git checkout master

$ git merge upstream/master
```

5. Create your own topical branch and begin committing your changes there. It should be named uniquely from other branches, in this case we used `dev_yourname`.

```shell
$ git checkout master

$ git branch dev_yourname

$ git checkout dev_yourname
```

Now, you can start to make changes to your `dev_yourname` branch.

## B. Submitting pull request

Once your changes to the `dev_yourname` branch are complete, please add and commit them with concise commit messages and your callsign.

1. Update your local `master` branch to absorb newly committed changes from the original repository

```shell
$ git fetch upstream

$ git checkout master

$ git merge upstream/master
```

2. If there were new developments to the upstream repository, you can now rebase your `dev_yourname` branch based on these.

```shell
$ git checkout dev_yourname

$ git rebase master
```

3. Push your local commits to your forked repository's `dev_yourname` branch.

```shell
$ git push -u origin dev_yourname
```

4. Go to the forked repository on your GitHub page. Navigate to the `dev_yourname` branch and click the pull request button. Describe the contents/crux of your pull request. Once all is well, submit the pull request.

5. The proposed changes will be reviewed and we will revert regarding the merging process.
