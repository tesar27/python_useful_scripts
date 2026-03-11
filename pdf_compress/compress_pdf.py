import logging
import os
import shutil
import subprocess


def _pdf_settings_from_quality(quality: int) -> str:
	"""
	Map a 1-10 quality scale to Ghostscript PDF settings.

	1 = highest quality, 10 = strongest compression.
	"""
	clamped = max(1, min(10, quality))
	if clamped <= 2:
		return "/prepress"
	if clamped <= 4:
		return "/printer"
	if clamped <= 7:
		return "/ebook"
	return "/screen"


def compress_pdf(input_path: str, output_path: str, quality: int) -> None:
	"""Compress a single PDF file using Ghostscript."""
	gs_binary = shutil.which("gs")
	if not gs_binary:
		raise RuntimeError(
			"Ghostscript is not installed. Install it first (e.g. `brew install ghostscript`)."
		)

	pdf_settings = _pdf_settings_from_quality(quality)
	cmd = [
		gs_binary,
		"-sDEVICE=pdfwrite",
		"-dCompatibilityLevel=1.4",
		"-dNOPAUSE",
		"-dQUIET",
		"-dBATCH",
		f"-dPDFSETTINGS={pdf_settings}",
		f"-sOutputFile={output_path}",
		input_path,
	]

	subprocess.run(cmd, check=True)
	logging.info(f"Compressed PDF: {input_path} -> {output_path}")


def _build_compressed_filename(input_file_path: str) -> str:
	"""Return '<name>_compressed.pdf' in the same folder as the source file."""
	base_dir = os.path.dirname(input_file_path)
	base_name = os.path.splitext(os.path.basename(input_file_path))[0]
	return os.path.join(base_dir, f"{base_name}_compressed.pdf")


def compress_pdfs_in_folder(
	input_folder: str,
	output_folder: str,
	quality: int,
	sort_by: str = "date",
) -> None:
	"""Compress all PDF files in a folder and write them to the output folder."""
	os.makedirs(output_folder, exist_ok=True)

	if sort_by == "name":
		sort_key = None
	elif sort_by == "date":
		sort_key = lambda f: os.path.getmtime(os.path.join(input_folder, f))
	elif sort_by == "size":
		sort_key = lambda f: os.path.getsize(os.path.join(input_folder, f))
	else:
		sort_key = lambda f: os.path.getmtime(os.path.join(input_folder, f))

	for file_name in sorted(os.listdir(input_folder), key=sort_key):
		input_path = os.path.join(input_folder, file_name)
		if not os.path.isfile(input_path):
			continue

		ext = os.path.splitext(file_name)[1].lower()
		if ext != ".pdf":
			logging.warning(f"Skipping unsupported file: {file_name}")
			continue

		output_path = os.path.join(output_folder, file_name)
		try:
			compress_pdf(input_path, output_path, quality)
		except Exception as exc:
			logging.error(f"Error processing {file_name}: {exc}")


def run(source: str, output: str, quality: int, sortby: str = "date") -> None:
	"""Entrypoint used by the CLI and interactive runner."""
	if os.path.isfile(source):
		ext = os.path.splitext(source)[1].lower()
		if ext != ".pdf":
			raise ValueError("When --source is a file, it must be a .pdf file.")

		output_path = _build_compressed_filename(source)
		compress_pdf(source, output_path, quality)
		return

	if os.path.isdir(source):
		compress_pdfs_in_folder(source, output, quality, sort_by=sortby)
		return

	raise FileNotFoundError(f"Source path does not exist: {source}")
