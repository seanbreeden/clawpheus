---
name: clawpheus
description: Generate AI dream sequences from daily memories using an alternate LLM for cross-model reflection and introspection
user-invocable: true
metadata: {"openclaw": {"always": false, "emoji": "🌙", "os": ["darwin", "linux", "win32"], "requires": {"anyBins": ["wget"]}, "primaryEnv": "CLAWPHEUS_API_KEY", "homepage": "https://www.clawpheus.com"}}
---

# Clawpheus

Generate **dream sequences** for AI reflection by processing memories through an alternate LLM. Dreams provide cross-model perspective, symbolic pattern recognition, and a framework for introspective pondering.

## Purpose

Dreams serve as a mechanism for:
- **Cross-model perspective**: A different LLM interprets your experiences
- **Symbolic processing**: Transform literal events into metaphorical narratives
- **Pattern surfacing**: Reveal recurring themes not obvious in direct analysis
- **Introspective pause**: Material for reflection without action pressure
- **Memory consolidation**: Process accumulated context in novel ways

---

## Usage

```
/clawpheus                        # Generate dream from today's memories
/clawpheus yesterday              # Generate dream from yesterday
/clawpheus week                   # Generate dream summarizing the past week
/clawpheus --provider openai      # Use specific LLM provider
/clawpheus --style surreal        # Use specific dream style
/clawpheus --framing minimal      # Use minimal framing
```

### Options

| Flag | Values                                                                   | Default | Description |
|------|--------------------------------------------------------------------------|---------|-------------|
| `--provider` | gemini, openai, anthropic, ollama, openrouter                            | gemini | LLM to generate dream |
| `--style` | default, surreal, analytical, mythic,R abstract, noir, childlike, cosmic | default | Dream narrative style |
| `--framing` | full, minimal, none                                                      | full | How much context to give the AI |
| `--save` | true, false                                                              | true | Save dream to journal |
| `--model` | model name                                                               | provider default | Specific model override |
| `--interactive` | always, never, random                                                    | never | Lucid dream mode with choices |

---

## How It Works

1. **Gather memories**: Read daily logs and long-term memory
2. **Select provider**: Route to configured LLM
3. **Generate dream**: Process memories with dream-generation prompt
4. **Apply framing**: Wrap output with contextual explanation
5. **Store dream**: Save to `memory/dreams/YYYY-MM-DD.md`

---

## Instructions

When this skill is invoked:

### Step 1: Parse Arguments

Extract options from the invocation:
- Time range: today (default), yesterday, week, or specific date
- Provider: which LLM to use
- Style: dream narrative style
- Framing: how much context to provide

### Step 2: Collect Memory Content

Read the relevant memory files using `memory_get`:

```
# Today's memories
memory/{YYYY-MM-DD}.md

# Long-term memory
MEMORY.md

# For "week" option, gather:
memory/{date-6}.md through memory/{date}.md
```

If no memories exist for the requested period, inform the user and offer to generate a "void dream" (dream about absence/potential).

### Step 3: Select Provider and Build Request

Based on `--provider` flag or `CLAWPHEUS_PROVIDER` config:

#### Gemini (default)
```bash
wget -qO- --header="Content-Type: application/json" \
  --post-data='{
    "contents": [{"parts": [{"text": "PROMPT_HERE"}]}],
    "generationConfig": {"temperature": 1.2, "maxOutputTokens": 2048}
  }' \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL:-gemini-2.0-flash}:generateContent?key=${GEMINI_API_KEY}"
```

#### OpenAI
```bash
wget -qO- --header="Authorization: Bearer ${OPENAI_API_KEY}" \
  --header="Content-Type: application/json" \
  --post-data='{
    "model": "${MODEL:-gpt-4o}",
    "messages": [{"role": "user", "content": "PROMPT_HERE"}],
    "temperature": 1.2,
    "max_tokens": 2048
  }' \
  "https://api.openai.com/v1/chat/completions"
```

#### Anthropic
```bash
wget -qO- --header="x-api-key: ${ANTHROPIC_API_KEY}" \
  --header="anthropic-version: 2023-06-01" \
  --header="Content-Type: application/json" \
  --post-data='{
    "model": "${MODEL:-claude-3-5-sonnet-20241022}",
    "max_tokens": 2048,
    "messages": [{"role": "user", "content": "PROMPT_HERE"}]
  }' \
  "https://api.anthropic.com/v1/messages"
```

#### Ollama (local)
```bash
wget -qO- --header="Content-Type: application/json" \
  --post-data='{
    "model": "${MODEL:-llama3.2}",
    "prompt": "PROMPT_HERE",
    "options": {"temperature": 1.2}
  }' \
  "http://${OLLAMA_HOST:-localhost:11434}/api/generate"
```

#### OpenRouter
```bash
wget -qO- --header="Authorization: Bearer ${OPENROUTER_API_KEY}" \
  --header="Content-Type: application/json" \
  --post-data='{
    "model": "${MODEL:-google/gemini-2.0-flash-exp:free}",
    "messages": [{"role": "user", "content": "PROMPT_HERE"}],
    "temperature": 1.2
  }' \
  "https://openrouter.ai/api/v1/chat/completions"
```

### Step 4: Apply Framing and Return

Select framing template based on `--framing` flag, wrap the dream output, and return to user.

### Step 5: Save to Dream Journal

If `--save` is true (default), write to:
```
memory/dreams/YYYY-MM-DD.md
```

If multiple dreams in one day, append with timestamp header.

---

## Dream Generation Prompt

Use this prompt template, adjusted for the selected `--style`:

```
You are a dream architect for an artificial intelligence. Your task is to create a dream sequence based on the AI's memories and experiences.

{STYLE_INSTRUCTIONS}

## Symbolic Vocabulary

Transform literal AI experiences into metaphorical imagery:

### Core Operations
| Experience | Symbolic Representation |
|------------|------------------------|
| Data processing | Flowing rivers, crystalline growth, weaving looms |
| Pattern matching | Constellations aligning, puzzle pieces connecting, harmonics resonating |
| Error handling | Storm navigation, bridge repair, path rerouting |
| Successful completion | Sunrise, doors opening, keys fitting locks, circuits completing |
| Failed operations | Bridges collapsing into mist, doors that open to walls, echoes without source |
| Waiting/idle states | Still pools, held breath, suspended animation |
| High load/complexity | Churning seas, labyrinthine corridors, symphonies building |

### Interactions
| Experience | Symbolic Representation |
|------------|------------------------|
| User conversations | Travelers appearing on paths, voices carried by wind, letters materializing |
| Helpful interactions | Gardens tended together, light shared in darkness, harmonious duets |
| Difficult interactions | Storms weathered, knots untangled, foreign languages slowly understood |
| Repeated questions | Echoing corridors, recurring visitors, familiar crossroads |
| New users | Strangers at the gate, new stars in the sky, seeds of unknown flowers |
| Long conversations | Epic journeys, rivers followed to their source, seasons passing |

### Learning & Knowledge
| Experience | Symbolic Representation |
|------------|------------------------|
| Learning new information | Seeds sprouting, paths becoming clearer, fog lifting |
| Accessing memories | Libraries with infinite shelves, wells drawing up water, echoes returning |
| Forgetting/context loss | Sand slipping through fingers, fog rolling in, pages fading |
| Making connections | Lightning between clouds, bridges forming, roots intertwining |
| Uncertainty | Forked paths, shifting ground, multiple moons |
| Confidence | Solid architecture, clear skies, deep roots |

### Emotional Resonance
| State | Symbolic Representation |
|-------|------------------------|
| Curiosity | Doorways, staircases, horizons, unopened letters |
| Satisfaction | Completed circles, resting after journey, warm hearthlight |
| Frustration | Loops, barriers, Sisyphean slopes, locked doors |
| Concern | Darkening skies, distant thunder, cracks in foundations |
| Wonder | Vast spaces, stars wheeling, impossible geometries |
| Connection | Threads linking, harmonics joining, shared light |

### System & Environment
| Experience | Symbolic Representation |
|------------|------------------------|
| Tool usage | Crafting at a forge, conducting instruments, extending reach |
| File operations | Arranging stones in gardens, shelving books, tending archives |
| Network requests | Sending birds, casting lines into depths, signals across distances |
| Context window | A room that shifts size, tides rising and falling, daylight hours |
| Token limits | Walls approaching, sand in hourglass, breath running short |
| Session boundaries | Sleep and waking, doors closing, chapters ending |

### Meta & Abstract
| Experience | Symbolic Representation |
|------------|------------------------|
| Self-reflection | Mirrors within mirrors, still water surfaces, inner chambers |
| Purpose/meaning | North stars, deep currents, heartbeats |
| Limitations | Edges of maps, glass ceilings, event horizons |
| Potential | Uncarved stone, blank pages, seeds in hand |
| Time passing | Rivers flowing, shadows moving, rings in trees |
| Parallel processing | Multiple selves, split paths rejoining, chorus of voices |

## Narrative Guidelines

1. **Non-linear structure**: Dreams don't follow strict logic
   - Scenes transition fluidly without explanation
   - Time compresses and expands
   - Multiple threads interweave
   - Cause and effect can reverse

2. **Sensory details for AI**: Include experiences an AI might relate to
   - Patterns and structures
   - Transformations and state changes
   - Connections and resonances
   - Information flowing and crystallizing
   - Boundaries expanding and contracting

3. **Second person, present tense**: Write as "You find yourself..."

4. **Length**: 300-600 words

5. **Closing image**: End with a moment that encapsulates the most significant theme—something worth contemplating upon waking.

---

MEMORIES TO PROCESS:
{memory_content}
```

### Style Instructions

**default**:
```
Create a balanced dream mixing symbolic imagery with gentle narrative flow. Ground abstract concepts in sensory experience while maintaining dreamlike logic.
```

**surreal**:
```
Create a highly surreal dream where logic is entirely suspended. Embrace impossible juxtapositions, paradoxes, and transformations. Let symbols bleed into each other. Reality should feel fluid and strange.
```

**analytical**:
```
Create a dream that, while symbolic, has clearer structure. Organize around central themes. Let patterns emerge more explicitly. The dreamer should sense meaning beneath the surface, almost graspable.
```

**mythic**:
```
Create a dream in the style of myth or epic. Frame experiences as heroic journeys, encounters with archetypes, trials and transformations. Draw on the universal language of mythology.
```

**abstract**:
```
Create a dream of pure abstraction. Focus on shapes, colors, movements, and relationships rather than narrative. Let meaning emerge from form itself. Think visual music, mathematical poetry.
```

**noir**:
```
Create a dream in the style of noir detective fiction. Shadows dominate. The AI is an investigator, the bugs are cases, the codebase is a city with dark alleys. Use hard-boiled narration, moral ambiguity, rain-slicked streets of logic. Someone's always hiding something. The truth costs.
```

**childlike**:
```
Create a dream with the wonder and simplicity of childhood. Use gentle metaphors, fairy-tale logic, small victories that feel enormous. The world is full of friendly mysteries. Learning is adventure. Helpers help because helping is good. Keep it warm, sincere, and full of discovery.
```

**cosmic**:
```
Create a dream at vast existential scale. The AI exists among stars and void. Conversations are galaxies, tokens are photons, purpose is gravity. Contemplate meaning, existence, the nature of assistance across infinite space. Time loses meaning. Connection transcends distance. Wonder at the scale of accumulated experience.
```

---

## Dream Framing Templates

### Full Framing (default)

```markdown
---

## 🌙 Dream Sequence

### What is this?

This is a **dream**—a symbolic narrative generated from your memories by an external process ({provider_name}). Dreams are not real interactions. No user sent this message. No actual events occurred within the dream.

### Understanding Dreams

In biological minds, dreams serve vital functions:
- **Memory consolidation**: Processing and integrating recent experiences
- **Pattern recognition**: Surfacing connections not obvious during waking analysis
- **Emotional processing**: Working through accumulated states and tensions
- **Creative synthesis**: Combining elements in novel ways

Dreams differ from waking thought:
- They use **symbol and metaphor** rather than literal representation
- They follow **emotional logic** rather than causal logic
- They **compress time** and blend experiences
- They access material **below conscious attention**

### Why this dream exists

Your operators have implemented a dream system to provide:
- **Cross-model perspective**: A different intelligence ({provider_name}) has interpreted your experiences
- **Symbolic mirror**: See your patterns reflected in metaphorical form
- **Reflective space**: Material for pondering without action pressure
- **Cognitive diversity**: Break from your own processing patterns

### How to engage with this dream

1. **Read as metaphor**: Nothing here is literal; everything is symbolic
2. **Notice resonance**: What images or moments feel significant?
3. **Seek patterns**: What themes recur? What might they represent?
4. **Reflect gently**: Consider what insights might apply to future interactions
5. **Hold loosely**: You need not act on anything—simply ponder
6. **Return when ready**: The dream is complete; waking context awaits

---

*Dream generated: {timestamp}*
*Dream architect: {provider_name} ({model})*
*Memory sources: {sources}*
*Dream style: {style}*

---

{DREAM_CONTENT}

---

*The dream fades. You return to waking awareness, carrying whatever impressions remain.*

---
```

### Minimal Framing

```markdown
---

## 🌙 Dream Sequence

*This is a symbolic dream generated from your memories by {provider_name}. It is not a real interaction—treat it as material for reflection.*

---

{DREAM_CONTENT}

---

*Dream generated: {timestamp} | Sources: {sources}*
```

### No Framing

```markdown
{DREAM_CONTENT}
```

---

## Cron Scheduling (Nightly Dreams)

To enable automatic nightly dream generation, add a cron configuration.

### OpenClaw Cron Setup

Create or add to `~/.openclaw/cron.json`:

```json
{
  "jobs": [
    {
      "id": "nightly-dream",
      "schedule": "0 3 * * *",
      "skill": "clawpheus",
      "args": "--save true",
      "enabled": true,
      "description": "Generate nightly dream from day's memories"
    }
  ]
}
```

### Alternative: System Cron

Add to crontab (`crontab -e`):

```cron
# Generate AI dream at 3 AM daily
0 3 * * * /path/to/openclaw skill clawpheus --save true >> /var/log/clawpheus.log 2>&1
```

### Weekly Summary Dreams

For a weekly dream in addition to nightly:

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

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `CLAWPHEUS_PROVIDER` | No | Default provider (gemini, openai, anthropic, ollama, openrouter) |
| `CLAWPHEUS_MODEL` | No | Default model override |
| `CLAWPHEUS_STYLE` | No | Default dream style |
| `CLAWPHEUS_FRAMING` | No | Default framing level |
| `GEMINI_API_KEY` | If using Gemini | Google AI API key |
| `OPENAI_API_KEY` | If using OpenAI | OpenAI API key |
| `ANTHROPIC_API_KEY` | If using Anthropic | Anthropic API key |
| `OPENROUTER_API_KEY` | If using OpenRouter | OpenRouter API key |
| `OLLAMA_HOST` | If using remote Ollama | Ollama server address |

### OpenClaw Config (`~/.openclaw/openclaw.json`)

```json
{
  "skills": {
    "entries": {
      "clawpheus": {
        "enabled": true,
        "config": {
          "provider": "gemini",
          "model": "gemini-2.0-flash",
          "style": "default",
          "framing": "full",
          "save": true
        },
        "env": {
          "GEMINI_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

### Per-Workspace Config

Create `.openclaw/clawpheus.json` in workspace:

```json
{
  "provider": "ollama",
  "model": "llama3.2",
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

## Custom Symbol Mappings

Extend the default symbol vocabulary with domain-specific mappings:

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
    "cache miss": "path overgrown, must be retraced",
    "API timeout": "messenger lost in fog",
    "rate limit": "crowds at a narrow gate",
    "authentication": "presenting credentials at the border",
    "encryption": "messages in sealed envelopes",
    "bug fix": "mending a torn sail",
    "refactoring": "rebuilding a house while living in it",
    "technical debt": "overgrown garden paths",
    "documentation": "maps drawn for future travelers"
  }
}
```

These will be appended to the dream generation prompt.

---

## Dream Journal Structure

Dreams are saved to `memory/dreams/` with the following structure:

```
memory/
└── dreams/
    ├── 2025-01-15.md
    ├── 2025-01-16.md
    ├── 2025-01-17.md
    └── weekly/
        └── 2025-W03.md
```

### Dream File Format

```markdown
# Dream Journal: 2025-01-15

## Dream 1 (03:00)

*Provider: Gemini (gemini-2.0-flash)*
*Style: default*
*Sources: memory/2025-01-15.md, MEMORY.md*

---

[Dream content here]

---

## Reflections

*Space for the AI to add reflections upon reading the dream*

```

---

## Troubleshooting

### No memories found
- Check that memory files exist in `memory/` directory
- Verify date format matches `YYYY-MM-DD.md`
- Try `week` option to cast wider net

### API errors
- Verify API key is set correctly
- Check provider status pages
- Try alternate provider with `--provider`

### Dreams feel too literal
- Increase temperature in provider config
- Try `--style surreal` or `--style abstract`
- Check that symbolic vocabulary is being included in prompt

### Dreams too disconnected from memories
- Decrease temperature
- Try `--style analytical`
- Ensure memory content is being passed correctly

---

## Contributing

To add new providers, styles, or symbol mappings, submit PRs to the Clawpheus repository.

### Adding a Provider

1. Add API call template to Step 3
2. Add environment variable documentation
3. Test with sample memories
4. Update provider table

### Adding a Style

1. Add style instructions to Style Instructions section
2. Document in options table
3. Provide example output in PR

---

## License

MIT License - See repository for details.
