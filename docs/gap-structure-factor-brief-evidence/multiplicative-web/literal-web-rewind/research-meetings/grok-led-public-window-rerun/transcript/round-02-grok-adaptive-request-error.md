# Grok Adaptive V2 Request Error

Command shape:

```text
grok --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure --always-approve --prompt-file /tmp/grok-adaptive-window-brief.md --output-format plain --max-turns 80 --disable-web-search
```

Observed behavior:

```text
no stdout after several minutes; process manually terminated
```

Classification:

```text
operational Grok CLI stall before usable v2 policy output
```

Decision:

```text
retry once with a much smaller prompt; if unavailable, continue under the last valid Grok contract without inventing a hidden-factor path
```
