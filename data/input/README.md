# data/input/ - Your Manual Space

This is where you **place the manuals** you want to convert into a Knowledge Graph.

## Accepted Format

### Plain Text (.txt)
```
Chapter 1: Introduction
The CNC 8070 system is a controller...

Chapter 2: Installation
To install the system, first...

Section 2.1: Requirements
The requirements are...
```

### PDF (.pdf)
- Processed automatically
- Requires `pdfplumber` installed: `pip install pdfplumber`

### Markdown (.md)
- Compatible directly
- Headers and structure are preserved

## How to Add a Manual

### Step 1: Prepare the file
```bash
# Option A: Plain text file
cp my_manual.txt data/input/

# Option B: PDF (converted automatically)
cp technical_manual.pdf data/input/
```

### Step 2: Choose a manual ID
Pick a unique `manual-id` (no spaces, no special characters):
```
my_manual          OK
8070_quick_ref     OK
manual_1           OK
my-manual          NOT OK (don't use hyphens)
```

### Step 3: Run the build
```bash
python scripts/build.py \
  --source-chunks data/input/my_manual.txt \
  --manual-id my_manual \
  --mode resume-compatible
```

## Expected Results

After processing, you will see in `data/processed/`:
```
data/processed/
├── my_manual_abox_input.json          # Raw extraction
├── my_manual_abox_generation_manifest.json
├── my_manual_merged.ttl               # Graph without consolidation
├── my_manual_bilingual_eval_report.json
└── [other artifacts...]
```

## Recommendations

### File Size
- **Optimal**: 10,000 - 100,000 words
- **Minimum**: 1,000 words
- **Maximum**: No limit (processed in chunks)

### Text Quality
- **Good**: Structured text with clear paragraphs
- **Better**: Includes chapters, sections, lists
- **Optimal**: Includes diagrams (as descriptive text)

- **Bad**: Poor quality PDF scans (noisy OCR)
- **Worse**: Fragments without context
- **Avoid**: Complex tables without text description

### Language
- **Supported**: Spanish, English, or bilingual
- **Automatic**: Language detection built-in
- **Recommendation**: Keep one language per manual for better performance

## Examples

### Example 1: Simple Manual in English
```bash
# File: data/input/manual_cnc.txt
python scripts/build.py \
  --source-chunks data/input/manual_cnc.txt \
  --manual-id cnc_8070 \
  --mode resume-compatible
```

### Example 2: Multiple Manuals
```bash
# Create batch script
cat > build_all.sh << 'EOF'
python scripts/build.py --source-chunks data/input/manual1.txt --manual-id manual_1
python scripts/build.py --source-chunks data/input/manual2.txt --manual-id manual_2
python scripts/build.py --source-chunks data/input/manual3.txt --manual-id manual_3
EOF

bash build_all.sh
```

### Example 3: With Golden Dataset (Testing)
```bash
# If you have Q&A pairs for evaluation:
# Place in: data/golden_sets/my_qa_test.json

python scripts/build.py \
  --source-chunks data/input/manual.txt \
  --manual-id my_manual \
  --eval-dataset data/golden_sets/my_qa_test.json
```

## Known Limitations

- **PDFs with complex images**: Images are ignored, only text is extracted
- **Large tables**: Better processed if converted to descriptive text
- **Special characters**: UTF-8 handled; verify encoding if issues occur

## Troubleshooting

### "File not found: data/input/..."
Verify that the file exists in `data/input/`

### "Unsupported file format"
Convert to TXT or PDF (these are supported)

### "Build failed: API error"
Verify that your API key is valid in `.env`

---

Ready to add your manual? Run:
```bash
python scripts/build.py --source-chunks data/input/your_file.txt --manual-id your_id
```
