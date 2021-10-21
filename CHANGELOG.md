# Changelog

## [0.12.0](https://github.com/sns-sdks/python-facebook/v0.12.0) (2021-10-21)

- Add api for business object.
- Add api for search pages.
- Support new graph version `v12.0`.
- Update for new `from` field for ig business comment.
- Add tests for `Python 3.10`.

## [0.11.2](https://github.com/sns-sdks/python-facebook/v0.11.2) (2021-09-02)

- GraphAPI for post and delete object.
- Add application apis.
- Remove Api version v3.3

## [0.11.1](https://github.com/sns-sdks/python-facebook/v0.11.1) (2021-08-23)

- New structure for Facebook Graph API
- New structure for Instagram Graph API
- New structure for Instagram Basic Display API

## [0.10.0](https://github.com/sns-sdks/python-facebook/v0.10.0) (2021-07-07)

### Features

- New structure for Graph API.

### Broken Change

- Remove python2 support.
- Refactor all methods.


## [0.9.5](https://github.com/sns-sdks/python-facebook/compare/v0.9.3...v0.9.5) (2021-09-02)

### Features

- Add follower field for page
- Remove Api version v3.3


## [0.9.3](https://github.com/sns-sdks/python-facebook/compare/v0.9.1...v0.9.2) (2021-04-28)

### Features

- Update API version to V11.0
- Add parameters `since` and `until` for instaram media api.

### Broken Change

- Replace IgProApi `get_user_medias` method parameter `since_time` and `until_time` With `since` and `until`.


## [0.9.2](https://github.com/sns-sdks/python-facebook/compare/v0.9.1...v0.9.2) (2021-04-28)

### Features

- error update

## [0.9.1](https://github.com/sns-sdks/python-facebook/compare/v0.9.0...v0.9.1) (2021-04-27)

### Features

- Add new fields for IG,FB
- New docs

### Fix

- version bug  #107

## [0.9.0](https://github.com/sns-sdks/python-facebook/compare/v0.8.1...v0.9.0) (2021-03-16)

### Features

- Upgrade api to v10.0
- Instagram business publish content

## [0.8.1](https://github.com/sns-sdks/python-facebook/compare/v0.8.0...v0.8.1) (2021-02-08)

### Features

- Upgrade api to v9.0

### Fix

- Bugs for #91 #93

## [0.8.0](https://github.com/sns-sdks/python-facebook/compare/v0.7.2...v0.8.0) (2021-01-17)

### Features

- Add new api for live videos

### Fix

- Bug for lost children fields for check params. thanks for [@stevenviola](https://github.com/stevenviola)


## [0.7.2](https://github.com/sns-sdks/python-facebook/compare/v0.7.0...v0.7.2) (2020-11-11)

### Features

- Add new api for story, tags for IG.
- Modify Facebook OAuth flow method.
- Add support for Python 3.9.

## [0.7.0](https://github.com/sns-sdks/python-facebook/compare/v0.6.1...v0.7.0) (2020-09-13)

### Features

- Add new api for video,album and photos for facebook.
- Update to support for to Graph API V8.0    

## [0.6.1](https://github.com/sns-sdks/python-facebook/compare/v0.6.0...v0.6.1) (2020-04-02)

### Features

- Introduce simple sleep in requests to avoid reach the limit quickly.

## [0.6.0](https://github.com/sns-sdks/python-facebook/compare/v0.5.5...v0.6.0) (2020-03-12)

### Features

- Introduce new methods for ``Instagram Basic Display Api``.

## [0.5.5](https://github.com/sns-sdks/python-facebook/compare/v0.5.4...v0.5.5) (2020-02-24)

### Features

- Introduce ``instagram`` business account mentions api.
- Add ``facebook`` post subattachments field.

## [0.5.4](https://github.com/sns-sdks/python-facebook/compare/v0.5.3...v0.5.4) (2020-02-14)

### Features

- Introduce ``instagram`` business account insights api.
- Introduce ``instagram`` business account hashtag api.

Simple usage at [GET DATA](https://github.com/sns-sdks/python-facebook/blob/master/README.rst#get-data-1).


## [0.5.3](https://github.com/sns-sdks/python-facebook/compare/v0.5.2...v0.5.3) (2020-01-05)

#### Broken Change

* Now we refactor all api for this library.

You can see the [README](https://github.com/sns-sdks/python-facebook/blob/master/README.rst) to see the changes.


## [0.5.2](https://github.com/sns-sdks/python-facebook/compare/v0.5.1...v0.5.2) (2019-11-13)

#### Features

* **facebook:** :sparkles: add global_brand_page_name fields in page ([34700f2](https://github.com/sns-sdks/python-facebook/commit/34700f2))
* **facebook:** :sparkles: add page default picture return. ([6c8f9ff](https://github.com/sns-sdks/python-facebook/commit/6c8f9ff))

## [0.5.1](https://github.com/sns-sdks/python-facebook/compare/v0.4.3...v0.5.1) (2019-10-23)

#### Features

* **instagram:** :sparkles: instagram owner data api. ([ad9fb89](https://github.com/sns-sdks/python-facebook/commit/ad9fb89))

* Instagram API has refactored. ([26b75ac](https://github.com/sns-sdks/python-facebook/commit/26b75ac))
