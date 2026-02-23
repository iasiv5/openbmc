Please do not submit a Pull Request via github.  Our project makes use of
Gerrit for patch submission and review.  For more details please
see https://github.com/openbmc/docs/blob/master/CONTRIBUTING.md#submitting-changes-via-gerrit-server

---

If you are using a GitHub PR workflow in a downstream/fork environment,
complete the checklist below:

## Lesson Learned linkage

- [ ] This change adds or updates a lesson entry under `docs/lessons/entries/`
- [ ] If no lesson is added, reason provided: _N/A / no reusable lesson / already covered_
- [ ] `python3 docs/lessons/scripts/validate_lessons.py` passes
- [ ] `python3 docs/lessons/scripts/build_index.py` has been run
