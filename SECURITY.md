# Security and sensitive submissions

Do not post credentials, personal data, private puzzle answers, or security reports in
public issues, pull requests, forks, or Actions logs. Use the private hiring contact
provided with your invitation. If no private contact/channel has been provided, ask
for one before beginning; this draft does not authorize a timed or paid assignment.

Revoke any exposed credential immediately. Removing it from the latest commit is not
enough: Git history, forks, caches, and logs can preserve it. Let the organizer know
privately so the affected artifacts and release can be investigated.

The local integrity checker is a diagnostic, not a sandbox. The organizer must review
submissions using pristine trusted tools and isolated execution. Candidate images,
verifiers, build scripts, and modified CI must never receive organizer credentials,
production data, privileged self-hosted runners, or a host Docker socket.
