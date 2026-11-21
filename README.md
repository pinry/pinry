# ![Pinry](docs/src/imgs/logo-dark.png)

![NodeJS Build](https://github.com/octanewt/pinry/actions/workflows/node.js.yml/badge.svg)
![Python Build](https://github.com/octanewt/pinry/actions/workflows/pythonpackage.yml/badge.svg)
![Docker Build](https://github.com/octanewt/pinry/actions/workflows/docker.yml/badge.svg)

The open-source core of Pinry, a tiling image board system for people
who want to save, tag, and share images, videos and webpages in an easy
to skim through format.

This is a fork of [pinry/pinry](https://github.com/pinry/pinry). Version 3.0 rebuilds it on Django 5.2 LTS, Python 3.12+, Vue 3 and Vite; see [Pinry 3.0](docs/src/upgrade-guide.md) for what changed. There is no upgrade path from 2.x.


## Features
- Image fetch and online preview
- Tagging system for Pins
- Browser Extensions
- Multi-user support
- Works well with docker
- Both public and private boards (add @2020.02.11)
- Search by tags / Search boards with name (add @2020.02.14)
- Full API support via DRF (add @2022.02.19)
- CLI support (Add image or url to Pinry via [command-line tool](https://github.com/pinry/pinry-cli-py)) (add @2022.02.20)
- i18n support (if you want to help to translate, please contact us in issues) (add @2020.04.23)
  - [x] English
  - [x] 简体中文
  - [x] French Support by [Lilian](https://github.com/LilianBoulard)
  
## Preview
![image](https://user-images.githubusercontent.com/4109722/166976413-38b575f2-a246-4852-ba05-11bca5f9b052.png)


## Install with Docker
Build the image from this repository and run it with Docker Compose, on
**amd64** or **arm64**:

    cp .env.example .env    # set SECRET_KEY and ALLOWED_HOSTS
    cp docker-compose.example.yml docker-compose.yml
    docker compose up -d --build

See [Install with Docker](docs/src/install-with-docker.md) for HTTPS,
PostgreSQL and every setting.

## Development

Pinry needs Python 3.12+ with [uv](https://docs.astral.sh/uv/) and Node 26
with pnpm. See [Developing Pinry](docs/src/development.md), and
[API support](docs/src/api.md) for the REST API.

## Contributors

The core contributors for Pinry have been/currently are:

* Isaac Bythewood <http://isaacbythewood.com/>
* Krzysztof Klimonda <https://github.com/kklimonda>
* Lapo Luchini <https://github.com/lapo-luchini>
* Ji Qu <https://winkidney.com/>

For a full list of contributors check out the [GitHub Contributors Graph](https://github.com/pinry/pinry/graphs/contributors)
