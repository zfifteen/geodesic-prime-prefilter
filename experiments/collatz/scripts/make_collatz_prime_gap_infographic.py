"""Generate the Collatz prime-gap divisor-minimum infographic."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "collatz_prime_gap_infographic.png"
FONT = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
WIDTH = 1600
HEIGHT = 2200


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Return the infographic font."""
    return ImageFont.truetype(str(BOLD if bold else FONT), size=size)


def wrap(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, width: int) -> list[str]:
    """Wrap text to a pixel width."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if draw.textbbox((0, 0), candidate, font=font_obj)[2] <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: str,
    width: int,
    line_gap: int = 10,
) -> int:
    """Draw wrapped text and return the next y coordinate."""
    x, y = xy
    for line in wrap(draw, text, font_obj, width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def rounded_box(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    fill: str,
    outline: str,
    width: int = 3,
) -> None:
    """Draw a rounded information box."""
    draw.rounded_rectangle(box, radius=26, fill=fill, outline=outline, width=width)


def metric_card(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    value: str,
    label: str,
    accent: str,
) -> None:
    """Draw one metric card."""
    rounded_box(draw, box, "#ffffff", accent, 4)
    x1, y1, x2, _ = box
    draw.text((x1 + 34, y1 + 28), value, font=font(58, True), fill=accent)
    draw_wrapped(draw, (x1 + 34, y1 + 102), label, font(28), "#2f3640", x2 - x1 - 68, 8)


def main() -> None:
    """Generate the PNG infographic."""
    image = Image.new("RGB", (WIDTH, HEIGHT), "#f7f8fb")
    draw = ImageDraw.Draw(image)

    ink = "#171b1f"
    muted = "#4d5662"
    teal = "#00857a"
    blue = "#255c99"
    red = "#b6403a"
    gold = "#b98218"
    green = "#3f7d3a"

    draw.rectangle((0, 0, WIDTH, 18), fill=teal)
    draw.text(
        (90, 72),
        "A bridge between prime gaps and Collatz descents",
        font=font(62, True),
        fill=ink,
    )
    draw_wrapped(
        draw,
        (92, 158),
        (
            "For each prime gap, choose the first integer inside it with the fewest divisors. "
            "Collatz first-descent blocks hit the neighboring odd cells around that integer "
            "above the same-gap background rate."
        ),
        font(32),
        muted,
        1320,
        10,
    )

    metric_card(draw, (90, 300, 500, 520), "1.76x", "source hit rate versus same-gap background at the 1M odd-seed run", teal)
    metric_card(draw, (595, 300, 1005, 520), "15,558 / 15,558", "terminal adjacent residue checks matched exactly", blue)
    metric_card(draw, (1100, 300, 1510, 520), "3-step", "short first-descent families carry the main median reset signal", gold)

    rounded_box(draw, (90, 610, 1510, 1055), "#ffffff", "#d7dde6", 3)
    draw.text((130, 650), "The construction", font=font(42, True), fill=ink)
    y = draw_wrapped(
        draw,
        (130, 720),
        (
            "Prime-gap side: between consecutive primes, compute the divisor count for each "
            "interior integer. Keep the leftmost interior integer with the smallest divisor count."
        ),
        font(30),
        muted,
        1320,
        10,
    )

    line_y = y + 80
    draw.line((210, line_y, 1390, line_y), fill="#8894a3", width=6)
    for x, label, color in [
        (210, "prime", red),
        (800, "divisor minimum", teal),
        (1390, "next prime", red),
    ]:
        draw.ellipse((x - 20, line_y - 20, x + 20, line_y + 20), fill=color)
        tw = draw.textbbox((0, 0), label, font=font(26, True))[2]
        draw.text((x - tw // 2, line_y + 36), label, font=font(26, True), fill=color)

    draw.text((130, 940), "Collatz side:", font=font(30, True), fill=ink)
    draw_wrapped(
        draw,
        (335, 940),
        "follow odd values until the first odd value below the starting value.",
        font(30),
        muted,
        1020,
        10,
    )

    rounded_box(draw, (90, 1135, 1510, 1535), "#ffffff", "#d7dde6", 3)
    draw.text((130, 1175), "The bridge object", font=font(42, True), fill=ink)
    draw_wrapped(
        draw,
        (130, 1245),
        (
            "When the terminal Collatz source sits one below the prime-gap divisor minimum, "
            "that divisor minimum lands in exactly the power-of-two residue class needed "
            "for the final descent step."
        ),
        font(34),
        ink,
        1320,
        12,
    )
    draw.rounded_rectangle((210, 1402, 1390, 1480), radius=18, fill="#edf8f6", outline=teal, width=3)
    draw.text(
        (250, 1420),
        "prime-gap divisor minimum  +  Collatz terminal power-of-two residue",
        font=font(34, True),
        fill=teal,
    )

    rounded_box(draw, (90, 1615, 1510, 2055), "#ffffff", "#d7dde6", 3)
    draw.text((130, 1655), "Why it matters", font=font(42, True), fill=ink)
    bullets = [
        ("Independent structures meet", "prime-gap divisor minima and Collatz power-of-two descent geometry."),
        ("The effect is directional", "one-below and one-above cases separate cleanly."),
        ("The next target is algebraic", "prove or break a reset inequality for short 3-step residue families."),
    ]
    y = 1720
    for title, body in bullets:
        draw.ellipse((132, y + 8, 152, y + 28), fill=green)
        draw.text((175, y), title, font=font(30, True), fill=ink)
        y = draw_wrapped(draw, (175, y + 42), body, font(27), muted, 1220, 8) + 10

    draw.rectangle((0, 2130, WIDTH, HEIGHT), fill="#171b1f")
    draw.text(
        (90, 2150),
        "Single-script demo: first-descent blocks, prime gaps, divisor counts, same-gap control, terminal residue checks.",
        font=font(27),
        fill="#ffffff",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
