# Python Useful Scripts

Welcome to the **Python Useful Scripts** repository! This project is a collection of utility scripts designed to simplify and automate various tasks. The repository is modular, interactive, and easy to use, making it a great starting point for anyone looking to streamline their workflows.

---

## Features

- **Interactive CLI**: Start an interactive session to explore and run available modules.
- **Image Compression**: Compress images in a folder and generate a PDF.
- **Modular Design**: Easily extend the repository by adding new modules.
- **Virtual Environment Support**: Manage dependencies seamlessly with `uv`.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/python_useful_scripts.git
   cd python_useful_scripts
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Interactive Mode

Start the interactive CLI to explore and run available modules:
```bash
python main.py interactive
```

### Image Compression

Compress images in a folder and generate a PDF:
```bash
python main.py image-compression --source <source_folder> --output <output_folder> --quality <1-10>
```

- `--source`: Path to the folder containing images (required).
- `--output`: Path to the output folder (default: `output`).
- `--quality`: Compression quality level (1 = highest quality, 10 = maximum compression, default: 2).

### Show Version

Display the current version of the project:
```bash
python main.py version
```

---

## Adding New Modules

1. Create a new Python script in the appropriate folder.
2. Define a `run()` function with the required arguments.
3. Register the module in:
   - `main.py` for CLI integration.
   - `cli/interactive.py` for interactive mode.

---

## Development

### Virtual Environment

To ensure dependencies are installed and up-to-date, use the provided `uv` commands:
```bash
uv venv
uv pip install -r requirements.txt
uv run main.py interactive
```

### Testing

Run unit tests for the `image_compression` module:
```bash
python -m unittest discover -s image_compression/unittests
```

---

## Contributing

Contributions are welcome! If you have ideas for new modules or improvements, feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Typer](https://typer.tiangolo.com/) for the CLI framework.
- [Pillow](https://python-pillow.org/) for image processing.

---

Happy scripting!
