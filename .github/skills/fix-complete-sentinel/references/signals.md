# Fix Completion Signals

Use this reference to decide when to ask archival question.

## Strong signals (high confidence)

- Same workflow shows failure first, then success on rerun
- Build/test/task summary reports all succeeded after prior error
- User explicitly confirms verification:
  - fixed
  - verified
  - resolved
  - passed

## Medium signals

- Command exit code is 0 for previously failing target
- Error keywords disappear and success keywords appear in latest output

## Weak signals (do not trigger alone)

- Code changed without rerun
- User says "try" or "maybe fixed" without verification

## Trigger policy

- Trigger prompt only when at least one strong signal is present
- If only medium signals exist, require `--had-failure` context
- Never prompt repeatedly in the same fix cycle

## Prompt text

Use exact question:

`要不要归档这次经验？`
