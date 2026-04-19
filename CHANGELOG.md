# Changelog

All notable changes to this project will be documented in this file.

---

## [1.0.0] - 2026-04-19

### Added

- Initial release of ShieldEye Log Analyzer
- Web platform for current-month log monitoring
- Desktop application for offline and historical log analysis
- Structured logging system for developer-defined event tracking
- MongoDB integration with read-only access (`shieldeye_agent`)
- Event categorization (Authentication, System, Network, Application)
- Log filtering by:
  - event_type
  - level
  - category
  - tags
  - date and keyword search
- SOC-oriented workflow:
  - Detection (web)
  - Investigation (export)
  - Forensic analysis (desktop)

### Desktop

- JSON log import support (MongoDB exports)
- Offline log analysis capability
- Long-term log retention and historical investigation
- Linux `.deb` installation package
- Windows `.exe` installation package

### Security

- No log storage on ShieldEye servers (user-controlled data model)
- Read-only MongoDB access design
- Logging best practices documentation (avoid sensitive data)

### Notes

- Web platform currently limited to current-month log analysis
- Web backend is inactive pending user demand or technical demonstration requests

---

## [Unreleased]

### Planned

- Advanced correlation rules for threat detection
- Timeline-based investigation view
- Export and reporting features
- Improved filtering performance
- Web platform reactivation and scaling
