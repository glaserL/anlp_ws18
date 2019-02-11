# Guidelines for Pull Requests

In order to contribute to conflict-free development of this repository, we suggest implementing localized branches and submitting pull requests. The suggested process of doing so will be described here in parts A and B.

## A. Local branching

First we need to clone this repository onto your personal workspace and implement a local/remote branch.

1. Create a branch on GitHub by using the web-based UI. Click on the branch option and type a unique name for a branch. In our case, we assume this to be `dev`.

2. Clone this repository onto your personal workspace.

```shell
$ git clone https://github.com/glaserL/anlp_ws18
```

3. Ensure your cloned repository is synced with all the updates from the upstream repository.

```shell
$ git fetch origin

$ git checkout master

$ git merge origin/master
```

4. Create your own topical branch and begin committing your changes there. Since it is a branch local to your workspace, its name would not matter to the upstream repository. However, for simplicity we will also name this as `dev`.

```shell
$ git checkout master

$ git branch dev

$ git checkout dev
```

Now, you can start to make changes changes to your `dev` branch.

## B. Submitting pull request

Once your changes to the `dev` branch are complete, please add and commit them with concise commit messages and your callsign.

1. Update your local `master` branch to absorb newly committed changes from the upstream repository.

```shell
$ git fetch origin

$ git checkout master

$ git merge origin/master
```

2. If there were new developments to the upstream repository, you can now rebase your `dev` branch based on these.

```shell
$ git checkout dev

$ git rebase master
```

3. Push your local commits to your repository's remote `dev` branch.

```shell
$ git push origin dev
```

4. Go to the repository's page on your GitHub page. Navigate to the `dev` branch and click the pull request button. Describe the contents/crux of your pull request. Once all is well, submit the pull request.

5. The proposed changes will be reviewed and then merged with the master branch.
