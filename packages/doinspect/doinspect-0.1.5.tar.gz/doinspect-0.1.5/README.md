# DoInspect - Docker Container Inspector

`doinspect` is a command-line tool to inspect running Docker containers, including:
- Environment Variables
- Network Usage
- Port Mappings
- Volume Mappings

## Installation
```bash
pip install doinspect
```

## Usage

```
doinspect -c my_container   # Inspect all details
doinspect -c my_container -e  # Show environment variables
doinspect -c my_container -n  # Show network usage
```

## License

MIT License

