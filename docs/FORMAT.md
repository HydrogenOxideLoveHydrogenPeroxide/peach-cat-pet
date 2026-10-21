# Sprite formats

Both images are transparent RGBA PNGs. Each cell is 192 × 208 pixels; there are 8 columns. Used frames start at the left of each row; unused cells are fully transparent.

| Zero-based row | State | Frames | Meaning |
| --- | --- | --- | --- |
| 0 | idle | 6 | Breathing and blinking at rest |
| 1 | running-right | 8 | Move right, no laptop |
| 2 | running-left | 8 | Move left, no laptop |
| 3 | waving | 4 | Greeting |
| 4 | jumping | 5 | Jump and land |
| 5 | failed | 8 | Failure reaction |
| 6 | waiting | 6 | Ask for input / approval |
| 7 | running | 6 | Active work: typing on the laptop |
| 8 | review | 6 | Inspect completed work |

**`running` means processing a task. Directional locomotion uses `running-left` / `running-right`.**

The local package contains exactly these 9 rows (1536 × 1872), with 57 used frames. Its `pet.json` uses `id`, `displayName`, `description`, and `spritesheetPath`; these are local package metadata, not an account-scoped pet ID.

The complete v2 image adds two rows (1536 × 2288, 73 used frames):

| Row | Clockwise gaze directions in degrees |
| --- | --- |
| 9 | 0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5 |
| 10 | 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5 |

Screen coordinates: 0 = up, 90 = right, 180 = down, 270 = left. Neutral gaze uses idle. `assets/atlas.json` describes the full sheet and frame durations for integrations; it is not itself a Codex local `pet.json` manifest.

## Verified format references

Local installation layout and manifest:

- [OpenAI skills: Codex pet contract](https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/hatch-pet/references/codex-pet-contract.md)
- [OpenAI Codex: pet manifest loader and default animation mapping](https://github.com/openai/codex/blob/c419fd01a70dd1d05356da443ac44328bda2e6f4/codex-rs/tui/src/pets/model.rs)

Package validation checks image size, transparency, all used and unused cells, and preservation of the working animation. The complete v2 artwork also passed the Pets preflight before being exported to this repository. The installer is tested against temporary Codex homes; client UI selection is performed by the person installing it.
