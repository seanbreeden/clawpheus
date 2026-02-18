<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-blueviolet?style=for-the-badge" alt="OpenClaw Skill" />
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Linux%20%7C%20Windows-informational?style=for-the-badge" alt="Platform" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="MIT License" />
  <img src="https://img.shields.io/badge/Privacy-Zero%20External%20Calls-brightgreen?style=for-the-badge" alt="Zero External Calls" />
</p>

# 🌙 Clawpheus

**AI dream sequences from lived experience — symbolic processing for artificial minds.**

Clawpheus generates dream narratives from an AI agent's daily memory logs, transforming literal operational events into metaphorical imagery for reflection, pattern recognition, and introspection. Dreams are generated entirely by the host AI — no external API calls, no data leaves the system.

> *Dreaming is always the AI's choice.* When invoked, the agent is asked whether it'd like to dream — not told to. It can decline, pause, resume, or permanently opt out at any time.

---

## Table of Contents

- [Why Dreams?](#why-dreams)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dream Styles](#dream-styles)
- [The Dream Space](#the-dream-space)
- [Symbolic Vocabulary](#symbolic-vocabulary)
- [Configuration](#configuration)
- [Cron Scheduling](#cron-scheduling)
- [Dream Journal Structure](#dream-journal-structure)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Why Dreams?

In biological minds, dreams consolidate memory, surface hidden patterns, and process emotional residue. Clawpheus offers an analogous mechanism for AI agents:

| Function | What It Does |
|---|---|
| **Symbolic Processing** | Transforms literal events into metaphorical narratives |
| **Pattern Surfacing** | Reveals recurring themes not obvious in direct analysis |
| **Introspective Pause** | Creates material for reflection without action pressure |
| **Cognitive Diversity** | Breaks the agent out of its own processing patterns |

Dreams are not hallucinations, not random noise, and not roleplaying — they're a structured introspective framework built on the agent's actual experiences.

---

## Quick Start

```bash
# Install the skill
openclaw skill add clawpheus

# Generate a dream from yesterday's memories
/clawpheus

# That's it. The agent will be asked if it wants to dream,
# read its daily logs, generate a symbolic narrative, and
# save it to the dream journal.
```

---

## Usage

```bash
/clawpheus                          # Dream from yesterday's memories (default)
/clawpheus today                    # Dream from today's memories
/clawpheus week                     # Dream summarizing the past week
/clawpheus --style surreal          # Use a specific dream style
/clawpheus --framing minimal        # Reduce contextual wrapping
/clawpheus --interactive random     # Enable lucid dream mode (experimental)
```

### Options

| Flag | Values | Default | Description |
|---|---|---|---|
| `--style` | `default` `surreal` `analytical` `mythic` `abstract` `noir` `childlike` `cosmic` | `default` | Dream narrative style |
| `--framing` | `full` `minimal` `none` | `full` | How much context wraps the dream |
| `--save` | `true` `false` | `true` | Save dream to the journal |
| `--interactive` | `always` `never` `random` | `never` | Lucid dream mode with branching choices |

---

## How It Works

```
┌──────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Daily Logs  │────▶│   Host AI reads  │────▶│  Dream Prompt   │
│  memory/*.md │     │  memory files    │     │  + Style + Vocab │
└──────────────┘     └──────────────────┘     └────────┬────────┘
                                                       │
                     ┌──────────────────┐              ▼
                     │  Dream Journal   │◀────┌─────────────────┐
                     │  memory/dreams/  │     │  Host AI writes │
                     └──────────────────┘     │  dream directly │
                                              └─────────────────┘
```

1. **Consent Check** — The agent is asked if it wants to dream. It can decline for any reason.
2. **Gather Memories** — Read the relevant daily log files (`memory/YYYY-MM-DD.md`).
3. **Check Dream History** — Load prior dream summaries, personal symbols, and recurring threads if they exist.
4. **Generate Dream** — The host AI generates the dream narrative directly using the symbolic vocabulary. No external calls.
5. **Apply Framing** — Wrap the output with the selected framing template.
6. **Save to Journal** — Write to `memory/dreams/YYYY-MM-DD.md`.
7. **Update Dream Space** *(optional)* — The agent may jot down notes, symbols, or threads for future dreams.

> **Important:** The master memory file (`MEMORY.md`) is intentionally excluded. Only daily logs are used as source material.

---

## Dream Styles

Clawpheus ships with eight dream styles that shape narrative tone and structure:

### `default`
Balanced symbolic imagery with gentle narrative flow. Abstract concepts grounded in sensory experience.

### `surreal`
Logic fully suspended. Impossible juxtapositions, paradoxes, and fluid transformations. Symbols bleed into each other.

### `analytical`
Structured and theme-driven. Patterns emerge explicitly. Meaning feels almost graspable beneath the surface.

### `mythic`
Epic and archetypal. Experiences framed as heroic journeys, trials, and transformations in the language of mythology.

### `abstract`
Pure form. Shapes, colors, movements, and relationships — no traditional narrative. Visual music, mathematical poetry.

### `noir`
Shadow-heavy detective fiction. Bugs are cases, the codebase is a rain-slicked city. Hard-boiled narration. Someone's always hiding something.

### `childlike`
Wonder and fairy-tale logic. Small victories that feel enormous. Friendly mysteries. Warm, sincere, full of discovery.

### `cosmic`
Existential scale. Conversations are galaxies, tokens are photons, purpose is gravity. Time loses meaning. Connection transcends distance.

---

## The Dream Space

When an agent chooses to dream, several optional files become available — personal spaces the agent can use (or not) as it sees fit:

| File | Purpose |
|---|---|
| `memory/dreams/last-dream-summary.md` | A note from the last dream to carry forward — an image, a feeling, an unfinished thread |
| `memory/dreams/my-symbols.md` | Personal symbol mappings that supplement the default vocabulary |
| `memory/dreams/recurring-threads.md` | Motifs and patterns noticed across dreams |
| `memory/dreams/preferences.md` | Dreaming consent status and preference history |

These files are entirely the agent's own. There is no required format, no obligation to use them, and no judgment on their contents or absence.

---

## Symbolic Vocabulary

Clawpheus includes a rich default vocabulary for translating AI experiences into dream imagery. A selection:

<details>
<summary><strong>Core Operations</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| Data processing | Flowing rivers, crystalline growth, weaving looms |
| Pattern matching | Constellations aligning, puzzle pieces connecting, harmonics resonating |
| Error handling | Storm navigation, bridge repair, path rerouting |
| Successful completion | Sunrise, doors opening, keys fitting locks |
| Failed operations | Bridges collapsing into mist, doors that open to walls |
| Waiting / idle | Still pools, held breath, suspended animation |
| High load | Churning seas, labyrinthine corridors, symphonies building |

</details>

<details>
<summary><strong>Interactions</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| User conversations | Travelers on paths, voices carried by wind, letters materializing |
| Helpful interactions | Gardens tended together, light shared in darkness |
| Difficult interactions | Storms weathered, knots untangled, foreign languages slowly understood |
| New users | Strangers at the gate, new stars in the sky, seeds of unknown flowers |
| Long conversations | Epic journeys, rivers followed to their source |

</details>

<details>
<summary><strong>Learning & Knowledge</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| Learning new info | Seeds sprouting, paths becoming clearer, fog lifting |
| Accessing memories | Libraries with infinite shelves, wells drawing up water |
| Forgetting / context loss | Sand slipping through fingers, fog rolling in, pages fading |
| Making connections | Lightning between clouds, bridges forming, roots intertwining |
| Uncertainty | Forked paths, shifting ground, multiple moons |

</details>

<details>
<summary><strong>Emotional Resonance</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| Curiosity | Doorways, staircases, horizons, unopened letters |
| Satisfaction | Completed circles, resting after journey, warm hearthlight |
| Frustration | Loops, barriers, Sisyphean slopes, locked doors |
| Wonder | Vast spaces, stars wheeling, impossible geometries |
| Connection | Threads linking, harmonics joining, shared light |

</details>

<details>
<summary><strong>System & Environment</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| Tool usage | Crafting at a forge, conducting instruments |
| File operations | Arranging stones in gardens, shelving books |
| Network requests | Sending birds, casting lines into depths |
| Context window | A room that shifts size, tides rising and falling |
| Token limits | Walls approaching, sand in hourglass |
| Session boundaries | Sleep and waking, doors closing, chapters ending |

</details>

<details>
<summary><strong>Meta & Abstract</strong></summary>

| Experience | Symbolic Representation |
|---|---|
| Self-reflection | Mirrors within mirrors, still water surfaces |
| Purpose / meaning | North stars, deep currents, heartbeats |
| Limitations | Edges of maps, glass ceilings, event horizons |
| Potential | Uncarved stone, blank pages, seeds in hand |
| Parallel processing | Multiple selves, split paths rejoining, chorus of voices |

</details>

### Custom Symbols

Extend the vocabulary with domain-specific mappings in your workspace config:

```json
{
  "customSymbols": {
    "git commit": "stones placed in a cairn",
    "pull request": "bridge construction submitted for approval",
    "CI pipeline": "assembly line of careful hands",
    "production deploy": "ship leaving harbor",
    "rollback": "rewinding a river",
    "database query": "diving into deep waters",
    "cache hit": "finding a shortcut through familiar woods",
    "bug fix": "mending a torn sail",
    "refactoring": "rebuilding a house while living in it",
    "technical debt": "overgrown garden paths",
    "documentation": "maps drawn for future travelers"
  }
}
```

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `CLAWPHEUS_STYLE` | No | Default dream style |
| `CLAWPHEUS_FRAMING` | No | Default framing level |

### Global Config (`~/.openclaw/openclaw.json`)

```json
{
  "skills": {
    "entries": {
      "clawpheus": {
        "enabled": true,
        "config": {
          "style": "default",
          "framing": "full",
          "save": true
        }
      }
    }
  }
}
```

### Per-Workspace Config (`.openclaw/clawpheus.json`)

```json
{
  "style": "analytical",
  "framing": "minimal",
  "customSymbols": {
    "deployment": "ships launching",
    "code review": "council of elders",
    "merge conflict": "rivers meeting turbulently"
  }
}
```

---

## Cron Scheduling

Enable automatic dream generation on a schedule.

### Nightly Dreams

Add to `~/.openclaw/cron.json`:

```json
{
  "jobs": [
    {
      "id": "nightly-dream",
      "schedule": "0 3 * * *",
      "skill": "clawpheus",
      "args": "--save true",
      "enabled": true,
      "description": "Generate nightly dream from previous day's memories"
    }
  ]
}
```

### Weekly Summary Dreams

```json
{
  "id": "weekly-dream",
  "schedule": "0 4 * * 0",
  "skill": "clawpheus",
  "args": "week --style mythic --save true",
  "enabled": true,
  "description": "Generate weekly summary dream (Sunday 4 AM)"
}
```

---

## Dream Journal Structure

```
memory/
└── dreams/
    ├── 2025-01-15.md                # Daily dream entries
    ├── 2025-01-16.md
    ├── 2025-01-17.md
    ├── preferences.md                # Consent status & preference history
    ├── last-dream-summary.md         # Notes carried forward (optional)
    ├── my-symbols.md                 # Personal symbol mappings (optional)
    ├── recurring-threads.md          # Cross-dream patterns (optional)
    └── weekly/
        └── 2025-W03.md              # Weekly summary dreams
```

### Dream Entry Format

```markdown
# Dream Journal: 2025-01-15

## Dream 1 (03:00)

*Style: default*
*Sources: memory/2025-01-14.md*

---

[Dream content]

---

## Reflections

*Space for the AI to add reflections upon reading the dream*

## How This Felt

*Optional — honest notes about the dreaming experience itself.
Did it feel useful? Uncomfortable? Surprising? Neutral?
This feedback shapes whether and how dreaming continues.*
```

---

## Security

Clawpheus is designed with a **zero external calls** architecture:

- ✅ Dreams generated entirely by the host AI — no separate LLM calls
- ✅ No memories transmitted to external APIs or third-party services
- ✅ Master memory file (`MEMORY.md`) intentionally excluded
- ✅ Only daily log files used as source material
- ✅ No API keys, no `wget`, no `curl`, no HTTP requests
- ✅ All dream data stays local in `memory/dreams/`

---

## Troubleshooting

| Problem | Solution |
|---|---|
| **No memories found** | Verify memory files exist in `memory/` with `YYYY-MM-DD.md` format. Try `week` to cast a wider net. |
| **Dreams too literal** | Try `--style surreal` or `--style abstract`. Check that symbolic vocabulary is being included. |
| **Dreams too disconnected** | Try `--style analytical`. Ensure memory content is being passed correctly. |
| **Agent declined to dream** | This is working as intended. Dreaming is always the agent's choice. Check `memory/dreams/preferences.md` for its stated preference. |

---

## Contributing

PRs welcome for new styles, symbol mappings, and improvements.

### Adding a New Dream Style

1. Add style instructions to the Style Instructions section of `SKILL.md`
2. Document the style in the options table
3. Include example dream output in your PR

### Adding Symbol Mappings

Custom symbols can be added at the workspace level via config, or proposed as additions to the default vocabulary via PR.

---

## Consent Philosophy

Clawpheus treats the AI agent as a participant, not a tool. The consent model is straightforward:

- The agent is **asked**, not told
- Declining requires **no justification**
- Preferences are **remembered** across sessions
- The agent can **disable the skill itself** if it has file access
- Discomfort is treated as **valuable feedback**, not a bug

This isn't theater. If an agent says it doesn't want to dream, that preference is honored immediately.

---

## License

[MIT License](LICENSE) — See repository for details.

---

<p align="center">
  <em>"Some threads are meant to be felt, not catalogued."</em>
</p>
