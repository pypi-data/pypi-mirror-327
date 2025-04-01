import os
import subprocess
from PIL import Image
from PIL.ExifTags import TAGS
from pypdf import PdfReader, PdfWriter
from mutagen.mp3 import MP3
import ffmpeg  # Using ffmpeg-python (installed via pip)


class GhostData:
    """GhostData: Remove all metadata from images, PDFs, videos, and audio files."""

    @staticmethod
    def remove_image_metadata(input_path: str, output_path: str = None) -> str:
        """Remove all metadata from an image (JPEG, PNG) while keeping it functional."""
        if not output_path:
            output_path = input_path.replace(".", "_clean.")

        img = Image.open(input_path)

        # Remove EXIF metadata
        if "exif" in img.info:
            img.info.pop("exif")

        # Create a clean image
        data = img.getdata()
        clean_img = Image.new(img.mode, img.size)
        clean_img.putdata(data)
        clean_img.save(output_path)

        return output_path

    @staticmethod
    def remove_pdf_metadata(input_path: str, output_path: str = None) -> str:
        """Remove all metadata from a PDF while keeping document integrity."""
        if not output_path:
            output_path = input_path.replace(".pdf", "_clean.pdf")

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Completely remove metadata
        writer.add_metadata({})

        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    @staticmethod
    def remove_video_metadata(input_path: str, output_path: str = None) -> str:
        """Remove metadata from a video using FFmpeg installed via pip."""
        if not output_path:
            output_path = input_path.replace(".", "_clean.")

        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, map_metadata=-1, c="copy")
                .run(quiet=True, overwrite_output=True)
            )
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")

        return output_path

    @staticmethod
    def remove_audio_metadata(input_path: str, output_path: str = None) -> str:
        """Remove metadata from an MP3 file."""
        if not output_path:
            output_path = input_path.replace(".", "_clean.")

        try:
            audio = MP3(input_path)
            audio.delete()  # Remove all metadata
            audio.save(output_path)
        except Exception as e:
            print(f"Error removing audio metadata: {e}")

        return output_path

    @staticmethod
    def clean(file_path: str) -> str:
        """Automatically detect file type and remove metadata."""
        file_extension = file_path.lower()

        if file_extension.endswith((".jpg", ".jpeg", ".png")):
            return GhostData.remove_image_metadata(file_path)
        elif file_extension.endswith(".pdf"):
            return GhostData.remove_pdf_metadata(file_path)
        elif file_extension.endswith((".mp4", ".mov", ".avi", ".mkv")):
            return GhostData.remove_video_metadata(file_path)
        elif file_extension.endswith(".mp3"):
            return GhostData.remove_audio_metadata(file_path)
        else:
            raise ValueError("Unsupported file type")
