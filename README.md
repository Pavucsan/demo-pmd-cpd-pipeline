# Asynchronous post-push PMD/CPD demo

This minimal Java 21/Maven project demonstrates a non-blocking developer flow:

1. A developer pushes normally; no local hook blocks the push.
2. GitHub Actions starts after the push and runs tests, PMD, and CPD asynchronously.
3. Reports are uploaded even when violations are found.
4. Failures are classified as either `quality_violation` or `execution_failure`.
5. A failure email with an available-report ZIP attachment is sent when the SMTP repository secrets are configured.

The workflow can show a failed check on a commit, but the intended demo policy does **not** make that quality check required for merging. Merge control is reviewer approval only.

## Run locally

Prerequisites: JDK 21 and Maven 3.9+.

```bash
mvn --batch-mode --no-transfer-progress clean test
mvn --batch-mode --no-transfer-progress pmd:pmd pmd:cpd
mvn --batch-mode --no-transfer-progress pmd:check pmd:cpd-check
```

Generated reports are written to `target/pmd.xml`, `target/cpd.xml`, and `target/reports/`.

## Demonstrate a PMD failure

Copy the sample into the source tree, run the checks, then remove it:

```powershell
Copy-Item quality-fixtures/IntentionalPmdViolation.java.sample src/main/java/com/pavucsan/demo/IntentionalPmdViolation.java
mvn --batch-mode --no-transfer-progress clean test pmd:pmd pmd:check
Remove-Item src/main/java/com/pavucsan/demo/IntentionalPmdViolation.java
```

For CPD, copy `quality-fixtures/IntentionalCpdViolation.java.sample` in the same way and run `pmd:cpd pmd:cpd-check`. The workflow still uploads the XML and HTML reports before it marks the run failed.

## Configure failure email

In GitHub, open **Settings → Secrets and variables → Actions** and add these repository secrets:

| Secret | Meaning | Example |
| --- | --- | --- |
| `SMTP_HOST` | SMTP server | `smtp.example.com` |
| `SMTP_PORT` | TLS port | `587` |
| `SMTP_USERNAME` | SMTP login | service account address |
| `SMTP_PASSWORD` | SMTP password or app password | secret value |
| `SMTP_FROM` | From address allowed by the server | service account address |
| `SMTP_TO` | Comma-separated recipients | `reviewers@example.com` |
| `SMTP_SECURITY` | `starttls` (default) or `ssl` | `starttls` |

The password is passed only through the Actions secret context and is never printed. The mail script requires certificate-validated TLS (`STARTTLS` or implicit SSL); plaintext SMTP is rejected. If required secrets are absent, analysis still runs and the job summary explains that email was skipped. If sending fails, the original quality classification remains visible and the workflow still fails.

Failure emails attach `quality-reports.zip`, containing all PMD, CPD, HTML, and test reports produced by that run. The run link remains in the message. If an execution failure occurs before reports can be generated, the email is still sent without an attachment and clearly says that the archive was unavailable.

## Reviewer-only merge approval

Configure a branch ruleset for `main` under **Settings → Rules → Rulesets**:

1. Require a pull request before merging.
2. Require at least one approval (and optionally dismiss stale approvals).
3. Optionally require conversation resolution and block force pushes/deletion.
4. Do **not** add `Asynchronous PMD/CPD analysis` as a required status check.

This means pushes are accepted immediately and quality feedback arrives later. A reviewer decides whether violations are acceptable before approving the merge. This is a deliberate demo policy, not a strict automated quality gate.

## GitHub Actions demo

After the files are committed and pushed with permission:

1. Push the clean baseline and confirm the workflow succeeds and uploads `pmd-cpd-reports-*`.
2. Create a branch, copy one intentional fixture into `src/main/java/com/pavucsan/demo/`, commit, and push.
3. Confirm the push itself succeeds, the workflow later reports `quality_violation`, reports remain downloadable, and configured recipients receive the run link.
4. Open a pull request. Confirm merging depends on reviewer approval, not this workflow status.
5. Remove the fixture before merging if the reviewer rejects the violation.

An `execution_failure` can be demonstrated on a temporary branch by introducing a Java compilation error or an invalid PMD configuration. Revert that test change afterward.

