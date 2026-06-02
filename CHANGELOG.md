# Changelog

All notable changes to this project will be documented in this file.

---

## [1.1.0] - 2026-05-02

### Added

* Application identity configuration for consistent data storage paths across deployments
* Improved database path diagnostics and validation

### Changed

* Event logs are now displayed in descending timestamp order (newest first)
* Improved database storage consistency between source execution and packaged releases
* Updated SQLite version verification workflow
* Improved JSON import processing workflow

### Fixed

* Fixed JSON import failures caused by concatenated MongoDB export files
* Fixed event log ordering that displayed oldest records first
* Fixed database initialization issues caused by incorrect class method usage
* Fixed application data path inconsistencies between:

  * Source execution (`python3 main.py`)
  * Binary releases (`.bin`)
  * Package installations (`.deb`)
* Fixed alert scanning callback scope issues
* Fixed database path creation issues during development mode
* Fixed multiple database file creation caused by inconsistent application identity configuration

### Security

* Improved database engine version validation
* Improved SQLCipher integration checks
* Improved database initialization and key verification handling

### Notes

* Existing users may have historical database files stored in legacy application data directories created by previous releases.
* Version 1.1.0 standardizes application data storage for future releases.

## [1.0.0] - 2026-04-19

### Added

* Initial release of ShieldEye Log Analyzer
* Web platform for current-month log monitoring
* Desktop application for offline and historical log analysis
* Structured logging system for developer-defined event tracking
* MongoDB integration with read-only access (`shieldeye_agent`)
* Event categorization (Authentication, System, Network, Application)
* Log filtering by:
  * event_type
  * level
  * category
  * tags
  * date and keyword search
* SOC-oriented workflow:
  * Detection (web)
  * Investigation (export)
  * Forensic analysis (desktop)

### Desktop

* JSON log import support (MongoDB exports)
* Offline log analysis capability
* Long-term log retention and historical investigation
* Linux `.deb` installation package
* Windows `.exe` installation package

### Security

* No log storage on ShieldEye servers (user-controlled data model)
* Read-only MongoDB access design
* Logging best practices documentation (avoid sensitive data)

### Notes

* Web platform currently limited to current-month log analysis
* Web backend is inactive pending user demand or technical demonstration requests

---
