# Contributing

Thanks for contributing to `data-reliability-mesh-rl`.

## Expectations

- Keep changes production-minded and testable.
- Prefer small pull requests with clear scope.
- Update documentation when public behavior changes.
- Add or extend tests for core engine and API behavior.

## Local verification

```bash
python -m pytest tests -q
python -m compileall services src tests
npm --prefix apps/dashboard run build
```

