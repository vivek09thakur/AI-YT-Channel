from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMP_DIR = ROOT / "temp"
SUBTITLES_DIR = ROOT / "subtitles"
OUTPUT_DIR = ROOT / "output"
ENV_FILE = ROOT / ".env"
CLIENT_SECRET_FILE = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / "token.json"
FONT_CANDIDATES = (
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    Path("C:/Windows/Fonts/arialbd.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/Library/Fonts/Arial Bold.ttf"),
)

HTTP_TIMEOUT = 30
LLM_TIMEOUT = 180
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models"
VERTEX_URL = "https://aiplatform.googleapis.com/v1/publishers/google/models"
VERTEX_KEY_PREFIX = "AQ."
GEMINI_MODEL = "gemini-2.5-flash"

PEXELS_URL = "https://api.pexels.com/videos/search"
STOCK_PER_QUERY = 15
STOCK_MIN_DURATION = 10
STOCK_COUNT = 5
MAX_CLIP_DURATION = 5.0

TTS_ENDPOINTS = (
    "https://tiktok-tts.weilnet.workers.dev/api/generation",
    "https://tiktoktts.com/api/tiktok-tts",
)
TTS_CHUNK = 299
TTS_WORKERS = 4
DEFAULT_VOICE = "en_us_001"
VOICES = {
    "en_us_001": "English (US) · Female 1",
    "en_us_002": "English (US) · Female 2",
    "en_us_006": "English (US) · Male 1",
    "en_us_007": "English (US) · Male 2",
    "en_us_009": "English (US) · Male 3",
    "en_us_010": "English (US) · Male 4",
    "en_uk_001": "English (UK) · Male 1",
    "en_uk_003": "English (UK) · Male 2",
    "en_au_001": "English (AU) · Female",
    "en_au_002": "English (AU) · Male",
    "en_male_narration": "English · Narrator",
    "en_male_funny": "English · Wacky",
    "en_female_emotional": "English · Peaceful",
    "en_us_ghostface": "Character · Ghost Face",
    "en_us_chewbacca": "Character · Chewbacca",
    "en_us_c3po": "Character · C3PO",
    "en_us_stitch": "Character · Stitch",
    "en_us_stormtrooper": "Character · Stormtrooper",
    "en_us_rocket": "Character · Rocket",
    "fr_001": "French · Male 1",
    "fr_002": "French · Male 2",
    "de_001": "German · Female",
    "de_002": "German · Male",
    "es_002": "Spanish · Male",
    "es_mx_002": "Spanish (MX) · Male",
    "br_001": "Portuguese (BR) · Female 1",
    "br_003": "Portuguese (BR) · Female 2",
    "br_004": "Portuguese (BR) · Female 3",
    "br_005": "Portuguese (BR) · Male",
    "id_001": "Indonesian · Female",
    "jp_001": "Japanese · Female 1",
    "jp_003": "Japanese · Female 2",
    "jp_005": "Japanese · Female 3",
    "jp_006": "Japanese · Male",
    "kr_002": "Korean · Male 1",
    "kr_003": "Korean · Female",
    "kr_004": "Korean · Male 2",
}
POSITIONS = {
    "center,bottom": "Bottom",
    "center,center": "Center",
    "center,top": "Top",
}
COLORS = {
    "#FFFF00": "Yellow",
    "#FFFFFF": "White",
    "#F4A261": "Orange",
    "#E63946": "Red",
    "#1D3557": "Blue",
    "#03071E": "Black",
}

WIDTH = 1080
HEIGHT = 1920
ASPECT = WIDTH / HEIGHT
FPS = 30
FRAME_EPSILON = 1 / 120
VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"
PRESET = "medium"
AUDIO_FPS = 44100

FONT_SIZE = 100
STROKE_WIDTH = 5
STROKE_COLOR = "black"
SUBTITLE_MAX_CHARS = 10
TOP_OFFSET = 80
DEFAULT_COLOR = "#FFFF00"
DEFAULT_POSITION = "center,bottom"
ASSEMBLY_LANG = {"br": "pt", "id": "en", "jp": "ja", "kr": "ko"}

YT_SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
YT_CATEGORY = "28"
YT_PRIVACY = "private"
YT_RETRIES = 10
YT_RETRY_CODES = {500, 502, 503, 504}

SCRIPT_PROMPT = """Write a spoken script for a short vertical video.
Subject: {subject}
Paragraphs: {paragraphs}
Language code: {language}
Rules: plain text only, no markdown, no title, no speaker labels, no references to this prompt,
no intro such as "welcome to this video", get straight to the point, exactly {paragraphs} paragraph(s) separated by blank lines."""

TERMS_PROMPT = """Return a JSON object {{"terms": [...]}} with {amount} stock-video search terms (1-3 words each) for a video about: {subject}
Every term must include the main subject. Script for context:
{script}"""

METADATA_PROMPT = """Return a JSON object {{"title": str, "description": str, "keywords": [str]}} for a YouTube Shorts video.
Subject: {subject}
Title: catchy, SEO friendly, under 70 characters. Description: 1-3 engaging sentences. Keywords: 6 short tags.
Script:
{script}"""
