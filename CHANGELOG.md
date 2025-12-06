# Changelog

## [0.3.0] - Unreleased
### Added
- **Plugin System Enhancements**:
  - Added support for plugin configuration via `fyodor plugin settings`.
  - Added persistent configuration storage in `~/.fyodor/plugins/config.json`.
- **New Plugins**:
  - `github`: Integration with GitHub for listing repos, creating issues, and viewing PRs.
  - `slack_notifier`: Send notifications to Slack webhooks.
  - `usage_dashboard`: Background system usage monitoring with TUI (`fyodor dashboard`).
  - `team_collaboration`: Role-Based Access Control (RBAC) extending the user management system.
- **User Management**:
  - Added role support to users (admin/user).
  - Added permission checking hooks.

### Changed
- `UserManager` now stores roles and passwords in a dictionary structure instead of just password hashes.
- CLI updated to include `dashboard` command.
