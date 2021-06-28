# Contribution guide

**All contributors are to be acknowledged.**

## Workflow

We follow the standard "Fork and pull" model.  Read more about it [here](https://docs.github.com/en/github/collaborating-with-pull-requests/getting-started/about-collaborative-development-models#fork-and-pull-model) and [here](https://gist.github.com/Chaser324/ce0505fbed06b947d962)

## Bugs, tasks, etc

Use this repo's Issues liberally to document bugs, feature requests, tasks (even if it's a cry for community help :), etc

## Dev

It's a simple code base, but setting the environment variable `PYLOGPRIM_DEV` to just exist will output dev logs to the Python logger/stdout.  Also setting the environment variable `LOGDNA_API_KEY` will additionally route dev logs to your LogDNA account.

### Dev Dependencies:
* `logdna` (if environment variables `PYLOGPRIM_DEV` and `LOGDNA_API_KEY` are set)

## Testing

The testing framework is rudimentary at best as of right now. Please ensure to cover contributions through the use of unit tests in [tests/test.py](./tests/test.py)

## [Changelog](./CHANGELOG.md)

Please update the changelog appropriately.

## Code of Conduct

Above all else, show respect to all you encounter.  You do that and we will be fine.
