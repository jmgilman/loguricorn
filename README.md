# loguricorn

<p align="center">
    <a href="https://github.com/jmgilman/loguricorn/actions/workflows/ci.yml">
        <img src="https://github.com/jmgilman/loguricorn/actions/workflows/ci.yml/badge.svg"/>
    </a>
    <a href="https://pypi.org/project/loguricorn">
        <img src="https://img.shields.io/pypi/v/loguricorn"/>
    </a>
</p>

> A small package for rerouting [gunicorn][1] logs to [loguru][2]

This package provides a compatible interface for automatically routing
`gunicorn` logs to the popular `loguru` library.

## Usage

Install the package:

```shell
pip install loguricorn
```

Then pass the custom interface to gunicorn at runtime:

```shell
gunicorn --logger-class loguricorn.Logger tests.app:app
```

All log records will now be routed through the default `loguru.logger`.

## Testing

Testing is done by starting `gunicorn` in a subprocess with the custom logger
enabled and validating that the emitted logs match the expected format.

Install dev dependencies:

```shell
poetry install
```

Run test:

```shell
poetry run tox .
```

## Contributing

Check out the [issues][3] for items needing attention or submit your own and
then:

1. [Fork the repo][4]
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar)
5. Create a new Pull Request

[1]: https://github.com/Delgan/loguru
[2]: https://github.com/benoitc/gunicorn
[3]: https://github.com/jmgilman/loguricorn/issues
[4]: https://github.com/jmgilman/loguricorn/fork
