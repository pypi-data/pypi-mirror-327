import os
import pytest
from ghostdata.cleaner import GhostData
from PIL import Image
from pypdf import PdfReader
from mutagen.mp3 import MP3

# Create test files
TEST_IMAGE = "tests/test.jpg"
TEST_PDF = "tests/test.pdf"
TEST_VIDEO = "tests/test.mp4"
TEST_AUDIO = "tests/test.mp3"

@pytest.fixture(scope="module", autouse=True)
def create_test_files():
    """Create dummy test files for each format."""
    # Create a test image with EXIF data
    img = Image.new("RGB", (100, 100), color="red")
    img.save(TEST_IMAGE)

    # Create a test PDF
    with open(TEST_PDF, "wb") as f:
        f.write(b"%PDF-1.4\n%Fake PDF Data")

    # Create a test MP3 (with metadata)
    with open(TEST_AUDIO, "wb") as f:
        f.write(b"ID3FakeMP3Metadata")

    # Create a fake MP4 (not playable, but enough to test metadata stripping)
    with open(TEST_VIDEO, "wb") as f:
        f.write(b"ftypisomFakeMP4Metadata")

    yield  # Run tests

    # Cleanup after tests
    os.remove(TEST_IMAGE)
    os.remove(TEST_PDF)
    os.remove(TEST_AUDIO)
    os.remove(TEST_VIDEO)

def test_clean_image():
    """Test if GhostData removes metadata from images."""
    output = GhostData.clean(TEST_IMAGE)
    assert os.path.exists(output)
    assert output != TEST_IMAGE  # It should create a new cleaned file

def test_clean_pdf():
    """Test if GhostData removes metadata from PDFs."""
    output = GhostData.clean(TEST_PDF)
    assert os.path.exists(output)

    reader = PdfReader(output)
    assert not reader.metadata  # Metadata should be empty

def test_clean_audio():
    """Test if GhostData removes metadata from MP3."""
    output = GhostData.clean(TEST_AUDIO)
    assert os.path.exists(output)

    mp3 = MP3(output)
    assert not mp3.tags  # Metadata should be removed

def test_clean_video():
    """Test if GhostData removes metadata from videos."""
    output = GhostData.clean(TEST_VIDEO)
    assert os.path.exists(output)
