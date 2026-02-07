#!/usr/bin/env python3
"""
Assemble multi-panel figures for TNBC meta-analysis manuscript.

Creates publication-ready multi-panel figures by combining individual PNG files
with panel labels (A, B, C) at 300 DPI resolution.

Output:
- Figure 1: 3-panel efficacy (pCR, EFS, OS)
- Figure 2: PD-L1 subgroup (single panel, use existing)
- Figure 3: 2-panel safety + publication bias
- Supplementary Figure 1: 2-panel sensitivity (EFS, OS)
- Supplementary Figure 2: 2-panel publication bias (pCR, EFS)
"""

import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import sys


def add_panel_label(img, label, position="top-left", font_size=80, offset=(40, 40)):
    """
    Add panel label (A, B, C) to image.

    Args:
        img: PIL Image object
        label: Label text (e.g., 'A', 'B', 'C')
        position: Label position ('top-left', 'top-right', etc.)
        font_size: Font size in pixels
        offset: (x, y) offset from corner in pixels

    Returns:
        PIL Image with label added
    """
    draw = ImageDraw.Draw(img)

    # Try to use a bold font, fallback to default if not available
    try:
        # macOS system fonts
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            # Linux system fonts
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
            )
        except:
            # Fallback to default
            font = ImageFont.load_default()
            print(f"Warning: Using default font, may not look optimal")

    # Calculate position
    if position == "top-left":
        x, y = offset
    elif position == "top-right":
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        x = img.width - text_width - offset[0]
        y = offset[1]
    else:
        x, y = offset

    # Draw white background box for better visibility
    bbox = draw.textbbox((x, y), label, font=font)
    padding = 10
    draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding],
        fill="white",
        outline="black",
        width=2,
    )

    # Draw text
    draw.text((x, y), label, fill="black", font=font)

    return img


def create_figure_1(input_dir, output_dir):
    """
    Create Figure 1: 3-panel efficacy (pCR, EFS, OS).

    Layout:
    ┌─────────────┐
    │   Panel A   │ pCR forest plot
    ├─────────────┤
    │   Panel B   │ EFS forest plot
    ├─────────────┤
    │   Panel C   │ OS forest plot
    └─────────────┘
    """
    print("Creating Figure 1: Efficacy forest plots...")

    # Load images
    img_pcr = Image.open(input_dir / "forest_plot_pCR.png")
    img_efs = Image.open(input_dir / "forest_plot_EFS.png")
    img_os = Image.open(input_dir / "forest_plot_OS.png")

    # Add panel labels
    img_pcr = add_panel_label(img_pcr, "A")
    img_efs = add_panel_label(img_efs, "B")
    img_os = add_panel_label(img_os, "C")

    # Calculate dimensions for vertical stacking
    widths = [img_pcr.width, img_efs.width, img_os.width]
    heights = [img_pcr.height, img_efs.height, img_os.height]

    max_width = max(widths)
    total_height = sum(heights)

    # Add spacing between panels
    spacing = 40
    total_height += spacing * 2

    # Create combined image
    combined = Image.new("RGB", (max_width, total_height), "white")

    # Paste images
    y_offset = 0
    combined.paste(img_pcr, (0, y_offset))
    y_offset += img_pcr.height + spacing
    combined.paste(img_efs, (0, y_offset))
    y_offset += img_efs.height + spacing
    combined.paste(img_os, (0, y_offset))

    # Save
    output_path = output_dir / "Figure1_Efficacy.png"
    combined.save(output_path, dpi=(300, 300))
    print(f"✅ Saved: {output_path}")
    print(f"   Dimensions: {combined.width}x{combined.height} pixels at 300 DPI")

    return output_path


def create_figure_2(input_dir, output_dir):
    """
    Create Figure 2: PD-L1 subgroup analysis (use existing).

    Just copy the existing file with panel label.
    """
    print("Creating Figure 2: PD-L1 subgroup...")

    # Load image
    img = Image.open(input_dir / "forest_plot_PDL1_subgroups.png")

    # Add panel label (optional, as this is single panel)
    # img = add_panel_label(img, 'A')

    # Save (or just copy)
    output_path = output_dir / "Figure2_PDL1_Subgroup.png"
    img.save(output_path, dpi=(300, 300))
    print(f"✅ Saved: {output_path}")
    print(f"   Dimensions: {img.width}x{img.height} pixels at 300 DPI")

    return output_path


def create_figure_3(input_dir, output_dir):
    """
    Create Figure 3: 2-panel safety + publication bias.

    Layout:
    ┌─────────────┐
    │   Panel A   │ Safety forest plot (SAE)
    ├─────────────┤
    │   Panel B   │ pCR funnel plot
    └─────────────┘
    """
    print("Creating Figure 3: Safety and publication bias...")

    # Load images
    img_safety = Image.open(input_dir / "forest_plot_safety_sae.png")
    img_funnel = Image.open(input_dir / "funnel_plot_pCR.png")

    # Add panel labels
    img_safety = add_panel_label(img_safety, "A")
    img_funnel = add_panel_label(img_funnel, "B")

    # Calculate dimensions
    max_width = max(img_safety.width, img_funnel.width)
    spacing = 40
    total_height = img_safety.height + img_funnel.height + spacing

    # Create combined image
    combined = Image.new("RGB", (max_width, total_height), "white")

    # Paste images
    combined.paste(img_safety, (0, 0))
    combined.paste(img_funnel, (0, img_safety.height + spacing))

    # Save
    output_path = output_dir / "Figure3_Safety_PublicationBias.png"
    combined.save(output_path, dpi=(300, 300))
    print(f"✅ Saved: {output_path}")
    print(f"   Dimensions: {combined.width}x{combined.height} pixels at 300 DPI")

    return output_path


def create_supp_figure_1(input_dir, output_dir):
    """
    Create Supplementary Figure 1: 2-panel sensitivity analyses.

    Layout:
    ┌─────────────┐
    │   Panel A   │ EFS leave-one-out
    ├─────────────┤
    │   Panel B   │ OS leave-one-out
    └─────────────┘
    """
    print("Creating Supplementary Figure 1: Sensitivity analyses...")

    # Load images
    img_efs = Image.open(input_dir / "efs_leave_one_out.png")
    img_os = Image.open(input_dir / "os_leave_one_out.png")

    # Add panel labels
    img_efs = add_panel_label(img_efs, "A")
    img_os = add_panel_label(img_os, "B")

    # Calculate dimensions
    max_width = max(img_efs.width, img_os.width)
    spacing = 40
    total_height = img_efs.height + img_os.height + spacing

    # Create combined image
    combined = Image.new("RGB", (max_width, total_height), "white")

    # Paste images
    combined.paste(img_efs, (0, 0))
    combined.paste(img_os, (0, img_efs.height + spacing))

    # Save
    output_path = output_dir / "SupplementaryFigure1_Sensitivity.png"
    combined.save(output_path, dpi=(300, 300))
    print(f"✅ Saved: {output_path}")
    print(f"   Dimensions: {combined.width}x{combined.height} pixels at 300 DPI")

    return output_path


def create_supp_figure_2(input_dir, output_dir):
    """
    Create Supplementary Figure 2: 2-panel publication bias.

    Layout:
    ┌─────────────┐
    │   Panel A   │ pCR funnel plot
    ├─────────────┤
    │   Panel B   │ EFS funnel plot
    └─────────────┘
    """
    print("Creating Supplementary Figure 2: Publication bias...")

    # Load images
    img_pcr = Image.open(input_dir / "funnel_plot_pCR.png")
    img_efs = Image.open(input_dir / "funnel_plot_EFS.png")

    # Add panel labels
    img_pcr = add_panel_label(img_pcr, "A")
    img_efs = add_panel_label(img_efs, "B")

    # Calculate dimensions
    max_width = max(img_pcr.width, img_efs.width)
    spacing = 40
    total_height = img_pcr.height + img_efs.height + spacing

    # Create combined image
    combined = Image.new("RGB", (max_width, total_height), "white")

    # Paste images
    combined.paste(img_pcr, (0, 0))
    combined.paste(img_efs, (0, img_pcr.height + spacing))

    # Save
    output_path = output_dir / "SupplementaryFigure2_PublicationBias.png"
    combined.save(output_path, dpi=(300, 300))
    print(f"✅ Saved: {output_path}")
    print(f"   Dimensions: {combined.width}x{combined.height} pixels at 300 DPI")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Assemble multi-panel figures for TNBC meta-analysis manuscript"
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("/Users/htlin/meta-pipe/06_analysis/figures"),
        help="Input directory with individual PNG files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("/Users/htlin/meta-pipe/07_manuscript/figures"),
        help="Output directory for assembled figures",
    )
    parser.add_argument(
        "--figures",
        nargs="+",
        choices=["1", "2", "3", "S1", "S2", "all"],
        default=["all"],
        help="Which figures to create (default: all)",
    )

    args = parser.parse_args()

    # Create output directory
    args.output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📊 Assembling Figures")
    print(f"Input:  {args.input_dir}")
    print(f"Output: {args.output_dir}\n")

    # Verify input files exist
    required_files = [
        "forest_plot_pCR.png",
        "forest_plot_EFS.png",
        "forest_plot_OS.png",
        "forest_plot_PDL1_subgroups.png",
        "forest_plot_safety_sae.png",
        "funnel_plot_pCR.png",
        "funnel_plot_EFS.png",
        "efs_leave_one_out.png",
        "os_leave_one_out.png",
    ]

    missing = []
    for filename in required_files:
        if not (args.input_dir / filename).exists():
            missing.append(filename)

    if missing:
        print(f"❌ Error: Missing input files:")
        for f in missing:
            print(f"   - {f}")
        sys.exit(1)

    # Create figures
    created_figures = []

    if "all" in args.figures or "1" in args.figures:
        created_figures.append(create_figure_1(args.input_dir, args.output_dir))

    if "all" in args.figures or "2" in args.figures:
        created_figures.append(create_figure_2(args.input_dir, args.output_dir))

    if "all" in args.figures or "3" in args.figures:
        created_figures.append(create_figure_3(args.input_dir, args.output_dir))

    if "all" in args.figures or "S1" in args.figures:
        created_figures.append(create_supp_figure_1(args.input_dir, args.output_dir))

    if "all" in args.figures or "S2" in args.figures:
        created_figures.append(create_supp_figure_2(args.input_dir, args.output_dir))

    print(f"\n✅ Successfully created {len(created_figures)} figures:")
    for path in created_figures:
        print(f"   - {path.name}")

    print(f"\n📁 Output directory: {args.output_dir}")
    print(f"\n🎯 Next steps:")
    print(f"   1. Review assembled figures for quality")
    print(f"   2. Insert figures into manuscript")
    print(f"   3. Add figure legends")
    print(f"   4. Verify panel labels are visible")


if __name__ == "__main__":
    main()
