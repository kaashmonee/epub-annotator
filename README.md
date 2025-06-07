# EPUB Annotator

A Python project for annotating EPUB files, with a standardized development environment using Docker.

## Project Structure

```
.
├── .devcontainer/          # VS Code devcontainer config (optional)
├── src/                    # Source code
│   ├── __init__.py        # Makes src a Python package
│   └── main.py            # Main application code
├── tests/                  # Test files
│   └── test_main.py       # Tests for main.py
├── scripts/               # Utility scripts
│   └── update-deps.sh     # Script to update dependencies
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── setup-dev-container.sh # Script to set up dev environment
└── README.md             # This file
```

## Development Environment

This project uses Docker for a consistent development environment. You have two options:

### Option 1: Using the Setup Script (Recommended)

1. Make the script executable:
   ```bash
   chmod +x setup-dev-container.sh
   ```

2. Run the script:
   ```bash
   ./setup-dev-container.sh epub-annotator
   ```

This will:
- Create/use the Dockerfile
- Create/use requirements.txt
- Build the Docker image
- Start a development container

### Option 2: Manual Setup

1. Build the Docker image:
   ```bash
   docker build -t epub-annotator .
   ```

2. Run the container:
   ```bash
   docker run -it --rm --name epub-annotator-dev-container -v $(pwd):/app epub-annotator
   ```

## Development Workflow

1. **Start the container** using either option above
2. **Edit code** in your preferred editor
3. **Run tests**:
   ```bash
   pytest tests/
   ```
4. **Run the application**:
   ```bash
   python src/main.py --epub temp/...epub --annotations temp/....html
   ```

## Managing Dependencies

### Adding New Dependencies

1. Install the package in the container:
   ```bash
   pip install new_package
   ```

2. Update requirements.txt:
   ```bash
   ./scripts/update-deps.sh
   ```

### Updating Existing Dependencies

Run the update script:
```bash
./scripts/update-deps.sh
```

## VS Code Integration

If you use VS Code:
1. Install the "Remote - Containers" extension
2. Click the green button in the bottom-left corner
3. Select "Attach to Running Container..."
4. Choose `epub-annotator-dev-container`

## Rebuilding the Container

You only need to rebuild the container if you:
- Change the Dockerfile
- Update requirements.txt
- Change the base Python version

To rebuild:
```bash
docker build -t epub-annotator .
```

## Project Dependencies

- Python 3.11
- pytest for testing
- black for code formatting
- pylint for linting
- python-dotenv for environment variables

## License

uhh idk
