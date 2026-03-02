import argparse
from PIL import Image
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("compress_image.log"),  # Log to a file
        logging.StreamHandler()  # Log to the console
    ]
)

def compress_png(input_path, output_path, compression_level):
    """
    Compress a PNG image file using lossless compression.
    """
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, "PNG", optimize=True, compress_level=compression_level)
    logging.info(f"Compressed PNG: {input_path} -> {output_path}")


def compress_jpg(input_path, output_path, quality):
    """
    Compress a JPEG image file by reducing its quality.
    """
    img = Image.open(input_path)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=quality)
    logging.info(f"Compressed JPEG: {input_path} -> {output_path}")

def compress_images_in_folder(input_folder, output_folder, compression_level):
    """
    Compress all images in the input folder and save them to the output folder.
    Also creates a PDF file from the compressed images.
    """
    os.makedirs(output_folder, exist_ok=True)
    pdf_images = []

    # Map compression level to JPEG quality (1-100) and PNG compress_level (0-9)
    jpeg_quality = max(10, min(100, 100 - (compression_level * 10)))
    png_compress_level = max(0, min(9, compression_level))

    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        if not os.path.isfile(input_path):
            continue

        ext = os.path.splitext(file_name)[1].lower()
        name, _ = os.path.splitext(file_name)
        output_path = os.path.join(output_folder, f"{name}{ext}")

        try:
            if ext in [".png"]:
                compress_png(input_path, output_path, png_compress_level)
            elif ext in [".jpg", ".jpeg"]:
                compress_jpg(input_path, output_path, jpeg_quality)
            else:
                logging.warning(f"Skipping unsupported file: {file_name}")
                continue

            # Add to PDF images list
            img = Image.open(output_path)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            pdf_images.append(img)
        except Exception as e:
            logging.error(f"Error processing {file_name}: {e}")

    # Create a PDF file from the compressed images
    if pdf_images:
        pdf_path = os.path.join(output_folder, "compressed_images.pdf")
        pdf_images[0].save(pdf_path, save_all=True, append_images=pdf_images[1:])
        logging.info(f"PDF created successfully at {pdf_path}")
    else:
        logging.info("No images to include in the PDF.")

def print_usage_info():
    """
    Print usage information about the script and its flags.
    """
    print("""
    Usage: python compress_image.py [OPTIONS]

    Options:
      --source       Path to the source folder containing image files (required).
      --output       Path to the output folder (default: 'output').
      --quality      Compression quality level (1-10). 1 = highest quality, 10 = maximum compression (default: 2).
      --info         Display information about the script and its usage.
    """)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress all images in a folder and create a PDF.")
    parser.add_argument("--source", help="Path to the source folder containing image files")
    parser.add_argument("--output", default="output", help="Path to the output folder (default: 'output')")
    parser.add_argument("--quality", default=2, type=int, choices=range(1, 11), help="Compression quality level (1-10). 1 = highest quality, 10 = maximum compression.")
    parser.add_argument("--info", action="store_true", help="Display information about the script and its usage.")
    args = parser.parse_args()

    if args.info or not args.source:
        print_usage_info()
    else:
        try:
            compress_images_in_folder(args.source, args.output, args.quality)
            logging.info(f"All images compressed successfully and saved to {args.output}")
        except Exception as e:
            logging.error(f"Error: {e}")