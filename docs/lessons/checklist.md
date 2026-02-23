# Lesson Learn Checklist

## Before writing

- [ ] This issue has reusable value beyond one-time local debugging
- [ ] Existing entries were searched to avoid duplicate lessons
- [ ] Correct template was selected (`quick` or `deep`)

## Before submitting

- [ ] Frontmatter includes all required fields from `schema.md`
- [ ] `id` format is `LL-YYYY-NNN` and is unique
- [ ] `sensitivity` is correctly set (`public`/`internal`/`confidential`)
- [ ] No secrets, tokens, private keys, or credentials are present
- [ ] `symptoms`, `root_cause`, `fix`, and `prevention` are actionable
- [ ] Validation passes: `python3 docs/lessons/scripts/validate_lessons.py`
- [ ] Index rebuilt: `python3 docs/lessons/scripts/build_index.py`

## Reviewer checks

- [ ] Root cause is evidence-based (not only hypothesis)
- [ ] Fix and prevention are testable and ownership is clear
- [ ] Links point to valid artifacts (issue/PR/commit/log/doc)
- [ ] Sensitive content policy is respected

## After merge

- [ ] Status updated to `active`
- [ ] If superseded, old lesson status set to `superseded`
- [ ] Follow-up task for prevention tracking is linked
