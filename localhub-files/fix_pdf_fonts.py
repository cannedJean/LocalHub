"""
Rebuild missing ToUnicode CMaps for a PDF whose embedded fonts have no
Unicode mapping (common with Korean PDFs exported from HWP/Word "print to
PDF" using Identity-H encoding). Visual rendering is fine, but text
extraction / copy-paste / search produces garbled (mojibake) text.

For CIDFontType2 fonts with Identity-H encoding, CID == GID, so we can
recover glyph -> Unicode by reading the embedded TrueType font's own
'cmap' table and inverting it. For simple TrueType fonts we do the same
using the font's cmap plus the /Differences encoding when present.
"""
import sys
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, DictionaryObject
from fontTools.ttLib import TTFont


def build_gid_to_unicode(font_bytes: bytes) -> dict[int, int]:
    tt = TTFont(BytesIO(font_bytes), lazy=True)
    gid_to_unicode: dict[int, int] = {}
    cmap = tt.getBestCmap() if tt.get("cmap") else None
    glyph_order = tt.getGlyphOrder()
    name_to_gid = {name: i for i, name in enumerate(glyph_order)}
    if cmap:
        for codepoint, glyph_name in cmap.items():
            gid = name_to_gid.get(glyph_name)
            if gid is not None and gid not in gid_to_unicode:
                gid_to_unicode[gid] = codepoint
    return gid_to_unicode


def make_tounicode_stream(gid_to_unicode: dict[int, int]) -> bytes:
    items = sorted(gid_to_unicode.items())
    lines = []
    lines.append("/CIDInit /ProcSet findresource begin")
    lines.append("12 dict begin")
    lines.append("begincmap")
    lines.append("/CIDSystemInfo <<")
    lines.append("  /Registry (Adobe)")
    lines.append("  /Ordering (UCS)")
    lines.append("  /Supplement 0")
    lines.append(">> def")
    lines.append("/CMapName /Adobe-Identity-UCS def")
    lines.append("/CMapType 2 def")
    lines.append("1 begincodespacerange")
    lines.append("<0000> <FFFF>")
    lines.append("endcodespacerange")

    CHUNK = 100
    for start in range(0, len(items), CHUNK):
        chunk = items[start:start + CHUNK]
        lines.append(f"{len(chunk)} beginbfchar")
        for gid, uni in chunk:
            lines.append(f"<{gid:04X}> <{uni:04X}>")
        lines.append("endbfchar")

    lines.append("endcmap")
    lines.append("CMapName currentdict /CMap defineresource pop")
    lines.append("end")
    lines.append("end")
    return ("\n".join(lines) + "\n").encode("latin-1")


def get_embedded_font_bytes(font_descriptor) -> bytes | None:
    for key in ("/FontFile2", "/FontFile", "/FontFile3"):
        if key in font_descriptor:
            return font_descriptor[key].get_object().get_data()
    return None


def process(input_path: str, output_path: str) -> None:
    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.append(reader)

    fixed = 0
    skipped = 0

    seen_font_ids = set()
    for page in writer.pages:
        resources = page.get("/Resources")
        if not resources or "/Font" not in resources:
            continue
        font_dict = resources["/Font"]
        for font_key in list(font_dict.keys()):
            font_ref = font_dict.raw_get(font_key)
            font_obj = font_ref.get_object()
            font_id = id(font_obj)
            if font_id in seen_font_ids:
                continue
            seen_font_ids.add(font_id)

            if "/ToUnicode" in font_obj:
                continue

            subtype = font_obj.get("/Subtype")
            descriptor = None
            if subtype == "/Type0":
                descendants = font_obj.get("/DescendantFonts")
                if not descendants:
                    skipped += 1
                    continue
                desc_font = descendants[0].get_object()
                descriptor = desc_font.get("/FontDescriptor")
            else:
                descriptor = font_obj.get("/FontDescriptor")

            if descriptor is None:
                skipped += 1
                continue
            descriptor = descriptor.get_object()

            font_bytes = get_embedded_font_bytes(descriptor)
            if font_bytes is None:
                skipped += 1
                continue

            try:
                gid_to_unicode = build_gid_to_unicode(font_bytes)
            except Exception as exc:
                print(f"  ! failed to parse embedded font for {font_key}: {exc}")
                skipped += 1
                continue

            if not gid_to_unicode:
                skipped += 1
                continue

            cmap_bytes = make_tounicode_stream(gid_to_unicode)
            stream_obj = DecodedStreamObject()
            stream_obj.set_data(cmap_bytes)
            ref = writer._add_object(stream_obj)
            font_obj[NameObject("/ToUnicode")] = ref
            fixed += 1
            print(f"  fixed {font_key} ({font_obj.get('/BaseFont')}) - {len(gid_to_unicode)} glyph mappings")

    print(f"\nFonts fixed: {fixed}, skipped: {skipped}")

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    src = sys.argv[1]
    dst = sys.argv[2]
    process(src, dst)
