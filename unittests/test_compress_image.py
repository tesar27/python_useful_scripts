import unittest
import os
from PIL import Image
from compress_image import compress_png, compress_jpg, compress_images_in_folder

class TestImageCompression(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test directories and files in the project directory
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this script
        cls.test_input_folder = os.path.join(base_dir, "test_input")
        cls.test_output_folder = os.path.join(base_dir, "test_output")
        os.makedirs(cls.test_input_folder, exist_ok=True)
        os.makedirs(cls.test_output_folder, exist_ok=True)

        # Create a sample PNG and JPEG file
        cls.png_file = os.path.join(cls.test_input_folder, "test_image.png")
        cls.jpg_file = os.path.join(cls.test_input_folder, "test_image.jpg")

        img = Image.new("RGB", (100, 100), color="red")
        img.save(cls.png_file, "PNG")
        img.save(cls.jpg_file, "JPEG")

    @classmethod
    def tearDownClass(cls):
        # Clean up test directories and files
        for folder in [cls.test_input_folder, cls.test_output_folder]:
            for file in os.listdir(folder):
                os.remove(os.path.join(folder, file))
            os.rmdir(folder)

    def test_compress_png(self):
        output_file = os.path.join(self.test_output_folder, "compressed_test_image.png")
        compress_png(self.png_file, output_file, compression_level=5)
        self.assertTrue(os.path.exists(output_file))

    def test_compress_jpg(self):
        output_file = os.path.join(self.test_output_folder, "compressed_test_image.jpg")
        compress_jpg(self.jpg_file, output_file, quality=75)
        self.assertTrue(os.path.exists(output_file))

    def test_compress_images_in_folder(self):
        compress_images_in_folder(self.test_input_folder, self.test_output_folder, compression_level=5)
        compressed_files = os.listdir(self.test_output_folder)
        self.assertIn("test_image.png", compressed_files)
        self.assertIn("test_image.jpg", compressed_files)
        self.assertIn("compressed_images.pdf", compressed_files)

if __name__ == "__main__":
    unittest.main()