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
