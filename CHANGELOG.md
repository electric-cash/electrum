# Changelog

## [5.0.5](https://github.com/electric-cash/elcash-wallet/compare/v5.0.4...v5.0.5) (2021-11-30)


### Bug Fixes

* Replace non-existant Coinbene exchange with Coingecko ([#75](https://github.com/electric-cash/elcash-wallet/issues/75)) ([f6c1514](https://github.com/electric-cash/elcash-wallet/commit/f6c1514a6de85f9acb3ad196a779a2c64a75ab72))

## [5.0.4](https://github.com/electric-cash/elcash-wallet/compare/v5.0.3...v5.0.4) (2021-09-23)


### Bug Fixes

* remove unused import ([632e6ba](https://github.com/electric-cash/elcash-wallet/commit/632e6bac858574638a95fb125b450f5363c769fd))

## [5.0.3](https://github.com/electric-cash/elcash-wallet/compare/v5.0.2...v5.0.3) (2021-09-14)


### Bug Fixes

* update building scripts and BIP21 scheme ([#57](https://github.com/electric-cash/elcash-wallet/issues/57)) ([0b9b400](https://github.com/electric-cash/elcash-wallet/commit/0b9b400128b7c17937bd7d53b918262b38ac4945)), closes [#56](https://github.com/electric-cash/elcash-wallet/issues/56) [#58](https://github.com/electric-cash/elcash-wallet/issues/58)

## [5.0.2](https://github.com/electric-cash/elcash-wallet/compare/v5.0.1...v5.0.2) (2021-06-21)


### Bug Fixes

* Set up upper limit on mnemonic passphrase ([#52](https://github.com/electric-cash/elcash-wallet/issues/52)) ([b72c74e](https://github.com/electric-cash/elcash-wallet/commit/b72c74ed37ed4e311e882e6c6a12104812401d19)), closes [#50](https://github.com/electric-cash/elcash-wallet/issues/50) [#49](https://github.com/electric-cash/elcash-wallet/issues/49) [#51](https://github.com/electric-cash/elcash-wallet/issues/51)

## [5.0.1](https://github.com/electric-cash/elcash-wallet/compare/v5.0.0...v5.0.1) (2021-06-10)


### Bug Fixes

* Fixed dynamic fee initialization ([#45](https://github.com/electric-cash/elcash-wallet/issues/45)) ([7041129](https://github.com/electric-cash/elcash-wallet/commit/70411293eea91902cec25ccec06813b97224eacf))
* **transaction details:** Align QR code ([#42](https://github.com/electric-cash/elcash-wallet/issues/42)) ([7861fca](https://github.com/electric-cash/elcash-wallet/commit/7861fcaa2552b044892b55a28b3dc83f5a70e024))
* Fixed overlay in amount field ([#26](https://github.com/electric-cash/elcash-wallet/issues/26)) ([3a7bfa8](https://github.com/electric-cash/elcash-wallet/commit/3a7bfa80d31227779f279dbbd9d6892efd6a65a8))
* Updated apt dependencies ([#27](https://github.com/electric-cash/elcash-wallet/issues/27)) ([48c1719](https://github.com/electric-cash/elcash-wallet/commit/48c17199fb6914bc53e389eff56e5bea0fb5dd49))

# [5.0.0](https://github.com/electric-cash/elcash-wallet/compare/v4.0.16...v5.0.0) (2021-02-02)


### Bug Fixes

* **amount field:** Fixed buffer overflow error ([#18](https://github.com/electric-cash/elcash-wallet/issues/18)) ([7a6e29c](https://github.com/electric-cash/elcash-wallet/commit/7a6e29cab15742728aacd7e95184ac6d872a353c))
* **brand:**  Fix fee combobox and added missing brand ([#19](https://github.com/electric-cash/elcash-wallet/issues/19)) ([4706d7d](https://github.com/electric-cash/elcash-wallet/commit/4706d7dc1e1bb142fc55f80594ab390ab80ae5a5))
* **elcash wallet:** Applied QA suggestions ([#12](https://github.com/electric-cash/elcash-wallet/issues/12)) ([aae53a7](https://github.com/electric-cash/elcash-wallet/commit/aae53a7e5d7a45dd02ecd8d10c320697e0be66fe)), closes [#13](https://github.com/electric-cash/elcash-wallet/issues/13)
* **pay to:** Fixed negative amount error in pay to field ([#16](https://github.com/electric-cash/elcash-wallet/issues/16)) ([0ed450c](https://github.com/electric-cash/elcash-wallet/commit/0ed450c373e86345d53848ad3402dfcb426425f8))
* **PoW check:** Removed PoW check on mainnet ([#11](https://github.com/electric-cash/elcash-wallet/issues/11)) ([2cf7fe1](https://github.com/electric-cash/elcash-wallet/commit/2cf7fe19a3a4c23baa9d13314aa24638eedd6bf0))
* **ssl:** Added ssl CA certs connection and shortened sensitive data lifetime ([#4](https://github.com/electric-cash/elcash-wallet/issues/4)) ([9d8bd04](https://github.com/electric-cash/elcash-wallet/commit/9d8bd047533b134546b869a8a115d3bc1b7832fa))


### Features

* **elcash:** Added electric cash coin ([#2](https://github.com/electric-cash/elcash-wallet/issues/2)) ([c96b194](https://github.com/electric-cash/elcash-wallet/commit/c96b1946b6a23f949d20851c486109901e3b67ec))
* **seed method:** Changed into bip39 ([#8](https://github.com/electric-cash/elcash-wallet/issues/8)) ([614abdd](https://github.com/electric-cash/elcash-wallet/commit/614abdd3de9a663dd3e5e854b9e176a4281a1360))

## [4.0.16](https://github.com/electric-cash/elcash-wallet/compare/v4.0.15...v4.0.16) (2021-02-02)


### Bug Fixes

* **builds:** release all binares ([0f4af68](https://github.com/electric-cash/elcash-wallet/commit/0f4af68b5e9105b66cdacc29d5d73a4fdecbbdc2))

## [4.0.15](https://github.com/electric-cash/elcash-wallet/compare/v4.0.14...v4.0.15) (2021-02-02)


### Bug Fixes

* **ci:** restrict release job to master branch ([2235a7e](https://github.com/electric-cash/elcash-wallet/commit/2235a7e9036830f22bd55a24117e29edd3214234))
* **ci:** typo on push branch in release job ([71c8a9a](https://github.com/electric-cash/elcash-wallet/commit/71c8a9a77d2fb9c898c67a089fe2284d1e9150b9))
* **release:** commit bumped up version in release tag/commit ([b60ac52](https://github.com/electric-cash/elcash-wallet/commit/b60ac52d9809ef509de679df56e5468e4d0a0fbb))

## [4.0.14](https://github.com/electric-cash/elcash-wallet/compare/v4.0.13...v4.0.14) (2021-02-02)

## [4.0.13](https://github.com/electric-cash/elcash-wallet/compare/v4.0.12...v4.0.13) (2021-02-02)

## [4.0.12](https://github.com/electric-cash/elcash-wallet/compare/v4.0.11...v4.0.12) (2021-02-02)





## [4.0.12](https://github.com/electric-cash/elcash-wallet/compare/v4.0.11...v4.0.12) (2021-02-02)

## [4.0.11](https://github.com/electric-cash/elcash-wallet/compare/v4.0.10...v4.0.11) (2021-02-02)


### Bug Fixes

* **build:** add package name for release ([72a3bdd](https://github.com/electric-cash/elcash-wallet/commit/72a3bdd7fd8d67972761d7fe1f253ce08873acdc))
* **build:** update automatic release build ([fbad957](https://github.com/electric-cash/elcash-wallet/commit/fbad9576741f6dcc0367cc872b0e5ea966f85f23))
* **release:** fix slack bot dependency ([b0fabf7](https://github.com/electric-cash/elcash-wallet/commit/b0fabf7707b36efa7263e42516cb45fae0dece12))
