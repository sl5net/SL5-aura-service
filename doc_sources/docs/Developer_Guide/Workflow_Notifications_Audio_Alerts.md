# Workflow Notifications (Audio Alerts)

To improve productivity, you can configure a local Git alias that pushes your code and automatically alerts you (via voice or sound) as soon as the GitHub Actions workflow is finished. This prevents "GitHub-watching fatigue" and lets you focus on other tasks.

### Prerequisites

You need the **GitHub CLI** and a text-to-speech engine or sound player installed on your system.

**For Manjaro / Arch Linux:**
```bash
sudo pacman -S github-cli espeak-ng
gh auth login
```

### Setup

Run the following command in your terminal to create a global Git alias called `pushsound`:

```bash
git config --global alias.pushsound '!git push && sleep 3 && gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "all github workflow has finished"'
```

### Usage

Instead of `git push`, simply run:
```bash
git pushsound
```
Your terminal will wait for the workflow to complete and then announce: *"all github workflow has finished"*.

---

### Customization & Alternatives

Depending on your preference, you might want to use a different alias name or notification method.

#### 1. Recommended Alias Names
If `pushsound` is too long to type, consider these alternatives:
*   `git pw` (Push & Watch) — **Recommended for speed.**
*   `git sync` (Implies pushing and waiting for the "green light")
*   `git palert` (Push Alert)

#### 2. Notification Styles
You can swap the `espeak-ng` part for other types of alerts:

*   **Desktop Notification:**
    `... && notify-send "GitHub Action" "Workflow Finished!"`
*   **System Sound (Bell):**
    `... && paplay /usr/share/sounds/freedesktop/stereo/complete.oga`
*   **Combination (Sound + Voice):**
    `... && paplay /usr/share/sounds/freedesktop/stereo/message.oga && espeak-ng "Done"`

#### 3. Advanced: Team-Safe Version
If multiple developers are pushing to the same repository simultaneously, the default command might track the wrong run. Use this "Branch-Safe" version to only watch your own current branch:

##### checks the first worklow only:

```bash
git config --global alias.pw '!git push && sleep 3 && gh run watch $(gh run list --branch $(git branch --show-current) --limit 1 --json databaseId --jq ".[0].databaseId") && espeak-ng "Workflow finished"'

git config --global alias.pushsound '!git push && sleep 3 && (gh run watch $(gh run list --limit 1 --json databaseId --jq ".[0].databaseId") --exit-status && espeak-ng "workflow successful" || espeak-ng "workflow failed")'

```

##### checks all GitHub registered workflows

git config --global alias.pushsound '!f() { git push && echo "Waiting for GitHub to register workflows..." && sleep 5 && SHA=$(git rev-parse HEAD) && SUCCESS=0 && for id in $(gh run list --commit $SHA --json databaseId -q ".[].databaseId"); do echo "Watching workflow $id..." && gh run watch $id --exit-status || SUCCESS=1; done; [ $SUCCESS -eq 0 ] && espeak-ng "all workflows successful" || espeak-ng "at least one workflow failed"; }; f'


### Troubleshooting
*   **"No runs found":** We include a `sleep 3` because GitHub takes a moment to register the push and start the workflow. If you have a very slow connection, you might need to increase this to `sleep 5`.
*   **Terminal Beeps:** If `espeak-ng` doesn't work, ensure your audio is not muted and the package is correctly installed.
