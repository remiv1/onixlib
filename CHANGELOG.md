# Changelog for onixlib

## [0.1.0] - 2026-04-27

### Added

- Initial release of onixlib, a library for parsing and creating ONIX files for the book industry.
- Added support for ONIX 3.0 format.
- Implemented basic parsing functionality to read ONIX files and extract relevant information.
- Added functionality to create ONIX files from Python objects.
- Included comprehensive documentation and examples for using the library.

## [0.1.1] - 2026-05-01

### 2026-05-01 Added

- Add stub files for type checking and improved code quality.

### 2026-05-01 Fixed

- Replace 'ns0:' with empty string in XML parsing to ensure compatibility with different ONIX file formats.

## [0.1.2] - 2026-05-02

### 2026-05-02 Added

- Added `authors` property to `Product` model to retrieve all contributors with role "A01" (written by) and "A02" (co-written by).
- Added `editor` property to `Product` model to retrieve gln and name of the first publisher in supplier detail, if available.
- Added `price` property to `Product` model to retrieve the first price of the product, if available (ttc, ht, currency, vat rate).

## [0.1.3] - 2026-05-02

### 2026-05-02 Fixed

- Refactored `editor` property to use a helper method `_extract_gln` for better readability and maintainability.
- Added type annotations to the `_extract_gln` method for improved code clarity.
- Removed unused imports and cleaned up code for better readability.
- Added `publisher` property to `Product` model to retrieve the publisher information (gln and name) from the first publisher representative in supplier detail, if available.

## [0.1.4] - 2026-05-04

### 2026-05-04 Fixed

- Fix bad handling of supplier gln and name in publisher property by refactoring the code to extract both gln and name together in a helper method `_extract_gln_and_name`.
- Fix dependencies in `pyproject.toml` by adding the xsdata dependency.
