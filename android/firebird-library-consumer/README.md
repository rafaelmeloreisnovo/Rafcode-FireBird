# Firebird Android library AAR and its independent consumer APK

The GitHub Actions workflow here checks out actual Firebird producer fork rafaelmeloreisnovo/firebird_rafcodephi at immutable commit f19db285f98331192ba3887fa04d2059843623cd, then builds the existing module :embedded to AAR and compiles an original Android :app that depends directly on project(':embedded'). All compilation and APK signature checks happen on GitHub Actions; no locally compiled chat artifact is the authoritative output.

Separate CI artifacts: actual Firebird Android AAR and signed debug Android AAR consumer APK. The app displays ABI and tests whether FirebirdConf from the AAR is present; it also checks whether libfbclient.so is packaged and can load. This tests library integration, NOT Firebird engine operation.

The producer currently contains Kotlin FirebirdConf but no verified native Firebird engine bundle. No server, database, SQL, actual transaction, recovery, or Android physical testing is claimed; ENGINE=BLOCKED_NO_NATIVE_FIREBIRD_ENGINE is an expected typed gap until real native source is built and packaged under the engine producer's IPL/IDPL licenses. No network, secrets, customer database or production writes. Signature uses ephemeral debug CI key, not upgrade-safe. Firebird engine must only be advertised after real native integration and disposable DB E2E.

The CI pins the producer source and does not alter its repo or trigger its large upstream matrix. The UI overlay is original MIT code, distinct from upstream engine and its licenses. rollback: close draft PR or revert additive files; no main or engine source change.
