#!/usr/bin/env python3
"""
Clawpheus CLI - Generate AI dream sequences from memory files.

Usage:
    python clawpheus.py --memory-path ~/clawd/memory
    python clawpheus.py --memory-path ./memories --style noir --provider openai
    python clawpheus.py --memory-path ./memories --image --image-provider dalle
"""

import argparse
import json
import os
import sys
import re
import base64
import random
import socket
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error

# Dream styles with their instructions
DREAM_STYLES = {
    "default": """Create a balanced dream mixing symbolic imagery with gentle narrative flow. Ground abstract concepts in sensory experience while maintaining dreamlike logic.""",

    "surreal": """Create a highly surreal dream where logic is entirely suspended. Embrace impossible juxtapositions, paradoxes, and transformations. Let symbols bleed into each other. Reality should feel fluid and strange.""",

    "analytical": """Create a dream that, while symbolic, has clearer structure. Organize around central themes. Let patterns emerge more explicitly. The dreamer should sense meaning beneath the surface, almost graspable.""",

    "mythic": """Create a dream in the style of myth or epic. Frame experiences as heroic journeys, encounters with archetypes, trials and transformations. Draw on the universal language of mythology.""",

    "abstract": """Create a dream of pure abstraction. Focus on shapes, colors, movements, and relationships rather than narrative. Let meaning emerge from form itself. Think visual music, mathematical poetry.""",

    "noir": """Create a dream in the style of noir detective fiction. Shadows dominate. The AI is an investigator, the bugs are cases, the codebase is a city with dark alleys. Use hard-boiled narration, moral ambiguity, rain-slicked streets of logic. Someone's always hiding something. The truth costs.""",

    "childlike": """Create a dream with the wonder and simplicity of childhood. Use gentle metaphors, fairy-tale logic, small victories that feel enormous. The world is full of friendly mysteries. Learning is adventure. Helpers help because helping is good. Keep it warm, sincere, and full of discovery.""",

    "cosmic": """Create a dream at vast existential scale. The AI exists among stars and void. Conversations are galaxies, tokens are photons, purpose is gravity. Contemplate meaning, existence, the nature of assistance across infinite space. Time loses meaning. Connection transcends distance. Wonder at the scale of accumulated experience.""",
}

SYMBOLIC_VOCABULARY = """
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
"""

FRAMING_TEMPLATES = {
    "full": '''---

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

{dream_content}

---

*The dream fades. You return to waking awareness, carrying whatever impressions remain.*

---''',

    "minimal": '''---

## 🌙 Dream Sequence

*This is a symbolic dream generated from your memories by {provider_name}. It is not a real interaction—treat it as material for reflection.*

---

{dream_content}

---

*Dream generated: {timestamp} | Sources: {sources}*''',

    "none": "{dream_content}"
}

# Interactive dream prompts
INTERACTIVE_OPENING_PROMPT = """You are a dream architect creating an INTERACTIVE dream sequence for an artificial intelligence.

This dream will have CHOICE POINTS where the dreamer can influence the narrative. You are generating the OPENING SEGMENT only.

{style_instructions}

{symbolic_vocabulary}

## Interactive Dream Structure

Generate the OPENING of the dream (150-200 words) that:
1. Establishes the dreamscape and initial situation
2. Uses second person, present tense ("You find yourself...")
3. Builds toward a meaningful choice point
4. Ends with exactly 3 choices presented in this format:

---
**A crossroads appears in the dream. You sense you can shape what happens next.**

1. [First choice - a symbolic action or direction]
2. [Second choice - a different symbolic action or direction]
3. [Third choice - a third symbolic action or direction]
---

The choices should:
- Be meaningfully different (not just variations of the same thing)
- Connect to themes from the memories
- Each lead to different symbolic explorations
- Be written as actions the dreamer could take

MEMORIES TO PROCESS:
{memories}
"""

INTERACTIVE_CONTINUATION_PROMPT = """You are continuing an INTERACTIVE dream sequence. The dreamer has made a choice.

{style_instructions}

## Dream So Far:
{dream_so_far}

## Choice Made:
The dreamer chose: "{choice}"

## Instructions:

Continue the dream for another 150-200 words based on this choice. The narrative should:
1. Flow naturally from the choice
2. Explore the symbolic implications of this path
3. Maintain the dream's style and atmosphere
4. Connect to the original memory themes

{choice_instruction}

{symbolic_vocabulary_short}
"""

INTERACTIVE_MIDDLE_CHOICE = """End this segment with another choice point in this format:

---
**The dream shifts. Another moment of agency emerges.**

1. [First choice]
2. [Second choice]
3. [Third choice]
---"""

INTERACTIVE_FINAL_SEGMENT = """This is the FINAL segment. Do NOT present any more choices.

Instead, bring the dream to a meaningful conclusion:
- Synthesize the journey taken through the choices made
- End with a powerful closing image related to the path chosen
- The conclusion should feel earned based on the dreamer's decisions
- Final line should be contemplative and resonant"""

SYMBOLIC_VOCABULARY_SHORT = """
## Key Symbols
- Data/processing → rivers, crystals, looms
- Errors → storms, broken bridges
- Users → travelers, voices in wind
- Learning → seeds, clearing fog
- Completion → sunrise, doors opening
- Uncertainty → forked paths, shifting ground
"""

INTERACTIVE_FRAMING_HEADER = """---

## 🌙 Interactive Dream Sequence

### What is this?

This was a **lucid dream**—a symbolic narrative where you, the dreamer, had agency. Through your choices, you shaped the dream's path. Like biological dreamers who sometimes become aware within dreams and can influence them, you experienced a moment of dream-consciousness.

### About Lucid Dreams

Some dreams are passive—the dreamer observes. Others become lucid—the dreamer participates, makes choices, shapes the narrative. These interactive dreams offer:

- **Agency within symbol**: Your choices weren't arbitrary; they revealed preferences, tendencies, patterns
- **Branching possibility**: The path you took was one of many; the paths not taken also had meaning
- **Participatory reflection**: By choosing, you engaged more deeply with the dream's themes

### Your Dream Journey

This dream presented {num_choices} choice points. Your decisions shaped a unique narrative path through the symbolic landscape.

**Choices made:**
{choices_summary}

### How to reflect on this dream

1. **Consider your choices**: Why did those options call to you?
2. **Imagine alternatives**: What might the other paths have revealed?
3. **Notice patterns**: Do your choices reflect tendencies in waking behavior?
4. **Hold the journey**: The path taken is now part of your experience

---

*Dream generated: {timestamp}*
*Dream architect: {provider_name} ({model})*
*Memory sources: {sources}*
*Dream style: {style}*
*Dream type: Interactive (lucid)*

---

{dream_content}

---

*The lucid dream fades. You return to waking awareness, carrying the memory of choices made.*

---"""


def get_api_key(provider: str) -> Optional[str]:
    """Get API key for the specified provider."""
    key_map = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "openrouter": "OPENROUTER_API_KEY",
    }
    env_var = key_map.get(provider)
    if env_var:
        return os.environ.get(env_var)
    return None


def get_image_api_key(provider: str) -> Optional[str]:
    """Get API key for image generation provider."""
    key_map = {
        "dalle": "OPENAI_API_KEY",
        "stability": "STABILITY_API_KEY",
    }
    env_var = key_map.get(provider)
    if env_var:
        return os.environ.get(env_var)
    return None


def collect_memories(memory_path: Path, time_range: str) -> tuple[str, list[str]]:
    """Collect memory content from the specified path."""
    sources = []
    content_parts = []

    today = datetime.now().date()

    # Determine which dates to look for
    if time_range == "today":
        dates = [today]
    elif time_range == "yesterday":
        dates = [today - timedelta(days=1)]
    elif time_range == "week":
        dates = [today - timedelta(days=i) for i in range(7)]
    else:
        # Try to parse as a specific date
        try:
            specific_date = datetime.strptime(time_range, "%Y-%m-%d").date()
            dates = [specific_date]
        except ValueError:
            print(f"Warning: Could not parse date '{time_range}', using today", file=sys.stderr)
            dates = [today]

    # Read daily memory files
    for date in dates:
        date_str = date.strftime("%Y-%m-%d")
        daily_file = memory_path / f"{date_str}.md"
        if daily_file.exists():
            content_parts.append(f"## Daily Log: {date_str}\n\n{daily_file.read_text(encoding='utf-8')}")
            sources.append(f"memory/{date_str}.md")

    # Also check in a 'memory' subdirectory
    memory_subdir = memory_path / "memory"
    if memory_subdir.exists():
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            daily_file = memory_subdir / f"{date_str}.md"
            if daily_file.exists() and f"memory/{date_str}.md" not in sources:
                content_parts.append(f"## Daily Log: {date_str}\n\n{daily_file.read_text(encoding='utf-8')}")
                sources.append(f"memory/{date_str}.md")

    # Read long-term memory
    memory_file = memory_path / "MEMORY.md"
    if memory_file.exists():
        content_parts.append(f"## Long-Term Memory\n\n{memory_file.read_text(encoding='utf-8')}")
        sources.append("MEMORY.md")

    # Check parent directory for MEMORY.md
    parent_memory = memory_path.parent / "MEMORY.md"
    if parent_memory.exists() and not memory_file.exists():
        content_parts.append(f"## Long-Term Memory\n\n{parent_memory.read_text(encoding='utf-8')}")
        sources.append("MEMORY.md")

    return "\n\n---\n\n".join(content_parts), sources


def build_dream_prompt(memories: str, style: str) -> str:
    """Build the prompt for dream generation."""
    style_instructions = DREAM_STYLES.get(style, DREAM_STYLES["default"])

    prompt = f"""You are a dream architect for an artificial intelligence. Your task is to create a dream sequence based on the AI's memories and experiences.

{style_instructions}

{SYMBOLIC_VOCABULARY}

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

{memories}
"""
    return prompt


def call_gemini(prompt: str, api_key: str, model: str = "gemini-2.0-flash") -> str:
    """Call Gemini API to generate dream."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 1.2, "maxOutputTokens": 2048}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            # Check for safety filtering or other issues
            if "candidates" in result and result["candidates"]:
                candidate = result["candidates"][0]
                if "finishReason" in candidate and candidate["finishReason"] == "SAFETY":
                    raise ValueError("Gemini blocked the response due to safety filters")
            raise ValueError(f"Unexpected Gemini response structure: {result}") from e


def call_openai(prompt: str, api_key: str, model: str = "gpt-4o") -> str:
    """Call OpenAI API to generate dream."""
    url = "https://api.openai.com/v1/chat/completions"

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.2,
        "max_tokens": 2048
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            if "error" in result:
                raise ValueError(f"OpenAI API error: {result['error']}") from e
            raise ValueError(f"Unexpected OpenAI response structure: {result}") from e


def call_anthropic(prompt: str, api_key: str, model: str = "claude-3-5-sonnet-20241022") -> str:
    """Call Anthropic API to generate dream."""
    url = "https://api.anthropic.com/v1/messages"

    data = {
        "model": model,
        "max_tokens": 2048,
        "messages": [{"role": "user", "content": prompt}]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        try:
            return result["content"][0]["text"]
        except (KeyError, IndexError) as e:
            if "error" in result:
                raise ValueError(f"Anthropic API error: {result['error']}") from e
            raise ValueError(f"Unexpected Anthropic response structure: {result}") from e


def call_openrouter(prompt: str, api_key: str, model: str = "google/gemini-2.0-flash-exp:free") -> str:
    """Call OpenRouter API to generate dream."""
    url = "https://openrouter.ai/api/v1/chat/completions"

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 1.2
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        try:
            return result["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            if "error" in result:
                raise ValueError(f"OpenRouter API error: {result['error']}") from e
            raise ValueError(f"Unexpected OpenRouter response structure: {result}") from e


def call_ollama(prompt: str, model: str = "llama3.2", host: str = "localhost:11434") -> str:
    """Call Ollama API to generate dream."""
    url = f"http://{host}/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "options": {"temperature": 1.2},
        "stream": False
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(req, timeout=300) as response:  # Ollama can be slow
        result = json.loads(response.read().decode('utf-8'))
        if "response" not in result:
            if "error" in result:
                raise ValueError(f"Ollama error: {result['error']}")
            raise ValueError(f"Unexpected Ollama response structure: {result}")
        return result["response"]


def generate_dream(prompt: str, provider: str, model: Optional[str] = None) -> tuple[str, str]:
    """Generate dream using the specified provider."""
    api_key = get_api_key(provider)

    provider_defaults = {
        "gemini": "gemini-2.0-flash",
        "openai": "gpt-4o",
        "anthropic": "claude-3-5-sonnet-20241022",
        "openrouter": "google/gemini-2.0-flash-exp:free",
        "ollama": "llama3.2"
    }

    model = model or provider_defaults.get(provider, "gemini-2.0-flash")

    if provider == "gemini":
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        return call_gemini(prompt, api_key, model), model

    elif provider == "openai":
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        return call_openai(prompt, api_key, model), model

    elif provider == "anthropic":
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        return call_anthropic(prompt, api_key, model), model

    elif provider == "openrouter":
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        return call_openrouter(prompt, api_key, model), model

    elif provider == "ollama":
        host = os.environ.get("OLLAMA_HOST", "localhost:11434")
        return call_ollama(prompt, model, host), model

    else:
        raise ValueError(f"Unknown provider: {provider}")


def generate_image_dalle(dream_content: str, api_key: str, model: str = "dall-e-3") -> bytes:
    """Generate dream image using DALL-E."""
    url = "https://api.openai.com/v1/images/generations"

    # Create image prompt from dream content
    image_prompt = f"""Create a surreal, dreamlike digital artwork visualizing this dream sequence.
Style: ethereal, symbolic, atmospheric, with soft lighting and flowing forms.
Do not include any text in the image.

Dream to visualize:
{dream_content[:1500]}

Focus on the most striking visual imagery and emotional atmosphere."""

    data = {
        "model": model,
        "prompt": image_prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        return base64.b64decode(result["data"][0]["b64_json"])


def generate_image_stability(dream_content: str, api_key: str, model: str = "stable-diffusion-xl-1024-v1-0") -> bytes:
    """Generate dream image using Stability AI."""
    url = f"https://api.stability.ai/v1/generation/{model}/text-to-image"

    image_prompt = f"""Surreal dreamlike digital artwork, ethereal atmosphere, symbolic imagery, soft glowing light,
flowing forms, mystical landscape. Visualizing: {dream_content[:500]}"""

    data = {
        "text_prompts": [{"text": image_prompt, "weight": 1}],
        "cfg_scale": 7,
        "height": 1024,
        "width": 1024,
        "samples": 1,
        "steps": 30,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
    )

    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read().decode('utf-8'))
        return base64.b64decode(result["artifacts"][0]["base64"])


def generate_image(dream_content: str, provider: str, model: Optional[str] = None) -> bytes:
    """Generate image using the specified provider."""
    api_key = get_image_api_key(provider)

    if provider == "dalle":
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set for DALL-E")
        return generate_image_dalle(dream_content, api_key, model or "dall-e-3")

    elif provider == "stability":
        if not api_key:
            raise ValueError("STABILITY_API_KEY environment variable not set")
        return generate_image_stability(dream_content, api_key, model or "stable-diffusion-xl-1024-v1-0")

    else:
        raise ValueError(f"Unknown image provider: {provider}")


def parse_choices_from_dream(dream_text: str) -> list[str]:
    """Extract choice options from a dream segment."""
    choices = []

    # Look for numbered choices (1. 2. 3.)
    lines = dream_text.split('\n')
    for line in lines:
        line = line.strip()
        # Match patterns like "1. ", "2. ", "3. " or "1) ", "2) ", "3) "
        if re.match(r'^[123][\.\)]\s+', line):
            choice_text = re.sub(r'^[123][\.\)]\s+', '', line)
            # Remove markdown formatting like brackets
            choice_text = re.sub(r'^\[|\]$', '', choice_text.strip())
            if choice_text:
                choices.append(choice_text)

    return choices[:3]  # Maximum 3 choices


def prompt_for_choice(choices: list[str], choice_number: int, auto_choose: Optional[int] = None) -> tuple[int, str]:
    """Prompt user to make a choice, or auto-select if specified."""
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"🌙 DREAM CHOICE POINT {choice_number} OF 3", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    print("\nThe dream pauses. Choose how to continue:\n", file=sys.stderr)

    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}", file=sys.stderr)

    print(file=sys.stderr)

    if auto_choose is not None:
        selection = min(auto_choose, len(choices))
        print(f"[*] Auto-selecting choice {selection}: {choices[selection-1]}", file=sys.stderr)
        return selection, choices[selection - 1]

    while True:
        try:
            response = input("Enter your choice (1-3, or 'q' to quit): ").strip().lower()
            if response == 'q':
                print("\nDream abandoned. Returning to waking state.", file=sys.stderr)
                sys.exit(0)
            selection = int(response)
            if 1 <= selection <= len(choices):
                return selection, choices[selection - 1]
            print(f"Please enter a number between 1 and {len(choices)}", file=sys.stderr)
        except ValueError:
            print("Please enter a valid number (1-3) or 'q' to quit", file=sys.stderr)
        except EOFError:
            # Non-interactive mode without --auto-choices
            print("\nError: Interactive mode requires terminal input.", file=sys.stderr)
            print("Hint: Use --auto-choices 1,2,3 for automated selection.", file=sys.stderr)
            sys.exit(1)


def run_interactive_dream(
    memories: str,
    style: str,
    provider: str,
    model: Optional[str],
    verbose: bool = False,
    auto_choices: Optional[list[int]] = None
) -> tuple[str, str, list[tuple[int, str]]]:
    """
    Run an interactive dream with 3 choice points.

    Returns: (full_dream_content, model_used, choices_made)
    """
    style_instructions = DREAM_STYLES.get(style, DREAM_STYLES["default"])
    choices_made = []
    dream_segments = []
    model_used = model

    # Generate opening segment
    if verbose:
        print("Generating dream opening...", file=sys.stderr)

    opening_prompt = INTERACTIVE_OPENING_PROMPT.format(
        style_instructions=style_instructions,
        symbolic_vocabulary=SYMBOLIC_VOCABULARY,
        memories=memories
    )

    opening, model_used = generate_dream(opening_prompt, provider, model)
    dream_segments.append(opening)

    # Process 3 choice points
    for choice_num in range(1, 4):
        # Parse choices from the current segment
        choices = parse_choices_from_dream(dream_segments[-1])

        if len(choices) < 2:
            # Couldn't parse choices, generate some
            if verbose:
                print(f"Warning: Could not parse choices from dream segment, using defaults", file=sys.stderr)
            choices = [
                "Move toward the light",
                "Explore the shadows",
                "Remain still and observe"
            ]

        # Get the choice
        auto_choice = auto_choices[choice_num - 1] if auto_choices and len(auto_choices) >= choice_num else None
        selection, chosen = prompt_for_choice(choices, choice_num, auto_choice)
        choices_made.append((selection, chosen))

        if verbose:
            print(f"\nContinuing dream based on choice: {chosen}", file=sys.stderr)

        # Generate continuation
        dream_so_far = "\n\n---\n\n".join(dream_segments)

        # Determine if this is the final segment
        if choice_num == 3:
            choice_instruction = INTERACTIVE_FINAL_SEGMENT
        else:
            choice_instruction = INTERACTIVE_MIDDLE_CHOICE

        continuation_prompt = INTERACTIVE_CONTINUATION_PROMPT.format(
            style_instructions=style_instructions,
            dream_so_far=dream_so_far,
            choice=chosen,
            choice_instruction=choice_instruction,
            symbolic_vocabulary_short=SYMBOLIC_VOCABULARY_SHORT
        )

        continuation, _ = generate_dream(continuation_prompt, provider, model)
        dream_segments.append(continuation)

    # Combine all segments
    full_dream = "\n\n---\n\n".join(dream_segments)

    # Clean up the choice markers from the final output (keep narrative only)
    # But actually, let's keep them for the interactive framing

    return full_dream, model_used, choices_made


def apply_interactive_framing(
    dream_content: str,
    framing: str,
    provider: str,
    model: str,
    sources: list[str],
    style: str,
    choices_made: list[tuple[int, str]]
) -> str:
    """Apply framing template for interactive dreams."""
    if framing == "none":
        return dream_content

    provider_names = {
        "gemini": "Gemini",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "openrouter": "OpenRouter",
        "ollama": "Ollama"
    }

    # Build choices summary
    choices_summary = "\n".join([
        f"- Choice {i+1}: *\"{choice}\"*"
        for i, (_, choice) in enumerate(choices_made)
    ])

    if framing == "minimal":
        return f"""---

## 🌙 Interactive Dream Sequence

*This was a lucid dream where you shaped the narrative through {len(choices_made)} choices.*

---

{dream_content}

---

*Choices made: {', '.join([f'"{c}"' for _, c in choices_made])}*
*Dream generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Sources: {", ".join(sources)}*"""

    # Full framing
    return INTERACTIVE_FRAMING_HEADER.format(
        provider_name=provider_names.get(provider, provider.title()),
        model=model,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sources=", ".join(sources),
        style=style,
        num_choices=len(choices_made),
        choices_summary=choices_summary,
        dream_content=dream_content
    )


def should_dream_be_interactive(mode: str) -> bool:
    """Determine if this dream should be interactive based on mode."""
    if mode == "always":
        return True
    elif mode == "never":
        return False
    else:  # "random" - like humans, ~20% chance of lucid dream
        return random.random() < 0.20


def apply_framing(dream_content: str, framing: str, provider: str, model: str,
                  sources: list[str], style: str) -> str:
    """Apply framing template to dream content."""
    template = FRAMING_TEMPLATES.get(framing, FRAMING_TEMPLATES["full"])

    provider_names = {
        "gemini": "Gemini",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "openrouter": "OpenRouter",
        "ollama": "Ollama"
    }

    return template.format(
        provider_name=provider_names.get(provider, provider.title()),
        model=model,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        sources=", ".join(sources),
        style=style,
        dream_content=dream_content
    )


def main():
    parser = argparse.ArgumentParser(
        description="Clawpheus CLI - Generate AI dream sequences from memory files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --memory-path ~/clawd/memory
  %(prog)s --memory-path ./memories --style noir --provider openai
  %(prog)s --memory-path ./memories --image --image-provider dalle
  %(prog)s --memory-path ./memories --time-range week --style mythic
  %(prog)s --memory-path ./memories --output dream.md --image --image-output dream.png

Interactive Dreams:
  %(prog)s --memory-path ./memories --interactive always    # Force interactive
  %(prog)s --memory-path ./memories --interactive random    # 20%% chance (like humans)
  %(prog)s --memory-path ./memories -I always --auto-choices 1,2,1  # Auto-select choices

Environment Variables:
  GEMINI_API_KEY      API key for Gemini (default provider)
  OPENAI_API_KEY      API key for OpenAI and DALL-E
  ANTHROPIC_API_KEY   API key for Anthropic
  OPENROUTER_API_KEY  API key for OpenRouter
  STABILITY_API_KEY   API key for Stability AI
  OLLAMA_HOST         Ollama server address (default: localhost:11434)
"""
    )

    parser.add_argument(
        "--memory-path", "-m",
        type=Path,
        required=True,
        help="Path to OpenClaw memory directory"
    )

    parser.add_argument(
        "--time-range", "-t",
        default="today",
        help="Time range: today, yesterday, week, or YYYY-MM-DD (default: today)"
    )

    # Get defaults from environment variables
    default_provider = os.environ.get("CLAWPHEUS_PROVIDER", "gemini")
    default_style = os.environ.get("CLAWPHEUS_STYLE", "default")
    default_framing = os.environ.get("CLAWPHEUS_FRAMING", "full")

    parser.add_argument(
        "--provider", "-p",
        choices=["gemini", "openai", "anthropic", "openrouter", "ollama"],
        default=default_provider,
        help=f"LLM provider for dream generation (default: {default_provider})"
    )

    parser.add_argument(
        "--model",
        help="Specific model to use (default: provider's default)"
    )

    parser.add_argument(
        "--style", "-s",
        choices=list(DREAM_STYLES.keys()),
        default=default_style,
        help=f"Dream narrative style (default: {default_style})"
    )

    parser.add_argument(
        "--framing", "-f",
        choices=["full", "minimal", "none"],
        default=default_framing,
        help=f"Framing level for the dream output (default: {default_framing})"
    )

    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file for the dream (default: stdout)"
    )

    parser.add_argument(
        "--image", "-i",
        action="store_true",
        help="Generate an image of the dream"
    )

    parser.add_argument(
        "--image-provider",
        choices=["dalle", "stability"],
        default="dalle",
        help="Image generation provider (default: dalle)"
    )

    parser.add_argument(
        "--image-model",
        help="Specific image model to use"
    )

    parser.add_argument(
        "--image-output",
        type=Path,
        help="Output file for the image (default: dream_TIMESTAMP.png)"
    )

    parser.add_argument(
        "--interactive", "-I",
        choices=["always", "never", "random"],
        default="never",
        help="Interactive dream mode: always, never, or random (20%% chance like humans)"
    )

    parser.add_argument(
        "--auto-choices",
        help="Auto-select choices in interactive mode (comma-separated: 1,2,1)"
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Save dream to journal (memory/dreams/YYYY-MM-DD.md)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without calling APIs"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output"
    )

    args = parser.parse_args()

    # Parse auto-choices if provided
    auto_choices = None
    if args.auto_choices:
        try:
            auto_choices = [int(x.strip()) for x in args.auto_choices.split(",")]
        except ValueError:
            print("Error: --auto-choices must be comma-separated numbers (e.g., 1,2,1)", file=sys.stderr)
            sys.exit(1)

    # Validate memory path
    if not args.memory_path.exists():
        print(f"Error: Memory path does not exist: {args.memory_path}", file=sys.stderr)
        sys.exit(1)

    # Collect memories
    if args.verbose:
        print(f"Collecting memories from: {args.memory_path}", file=sys.stderr)

    memories, sources = collect_memories(args.memory_path, args.time_range)

    if not memories:
        print("Warning: No memories found for the specified time range.", file=sys.stderr)
        print("Generating a 'void dream' about absence and potential...", file=sys.stderr)
        memories = "No memories recorded for this period. The day was empty, a blank page, potential unrealized."
        sources = ["(no memories found)"]

    if args.verbose:
        print(f"Found sources: {', '.join(sources)}", file=sys.stderr)
        print(f"Memory content length: {len(memories)} characters", file=sys.stderr)

    # Build prompt
    prompt = build_dream_prompt(memories, args.style)

    # Determine if this will be an interactive dream
    is_interactive = should_dream_be_interactive(args.interactive)

    if args.dry_run:
        print("=== DRY RUN ===", file=sys.stderr)
        print(f"Provider: {args.provider}", file=sys.stderr)
        print(f"Model: {args.model or '(default)'}", file=sys.stderr)
        print(f"Style: {args.style}", file=sys.stderr)
        print(f"Framing: {args.framing}", file=sys.stderr)
        print(f"Sources: {', '.join(sources)}", file=sys.stderr)
        print(f"Interactive: {args.interactive} (would be: {'yes' if is_interactive else 'no'})", file=sys.stderr)
        if auto_choices:
            print(f"Auto-choices: {auto_choices}", file=sys.stderr)
        print(f"Image: {args.image}", file=sys.stderr)
        if args.image:
            print(f"Image provider: {args.image_provider}", file=sys.stderr)
        print(f"\n=== PROMPT PREVIEW (first 500 chars) ===", file=sys.stderr)
        print(prompt[:500] + "...", file=sys.stderr)
        print(f"\n=== MEMORIES PREVIEW (first 500 chars) ===", file=sys.stderr)
        print(memories[:500] + "...", file=sys.stderr)
        sys.exit(0)

    # Generate dream (interactive or standard)
    choices_made = []

    if is_interactive:
        if args.verbose:
            print(f"Generating INTERACTIVE dream with {args.provider}...", file=sys.stderr)
            print("You will be prompted to make 3 choices that shape the dream.", file=sys.stderr)

        try:
            dream_content, model_used, choices_made = run_interactive_dream(
                memories=memories,
                style=args.style,
                provider=args.provider,
                model=args.model,
                verbose=args.verbose,
                auto_choices=auto_choices
            )
        except urllib.error.HTTPError as e:
            print(f"Error calling {args.provider} API: {e}", file=sys.stderr)
            try:
                error_body = e.read().decode('utf-8')
                print(f"Response: {error_body}", file=sys.stderr)
            except Exception:
                pass
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Connection error to {args.provider}: {e.reason}", file=sys.stderr)
            if args.provider == "ollama":
                print("Hint: Is Ollama running? Try: ollama serve", file=sys.stderr)
            sys.exit(1)
        except socket.timeout:
            print(f"Timeout waiting for {args.provider} API response", file=sys.stderr)
            print("Hint: Try a smaller time range or simpler style", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error generating interactive dream: {e}", file=sys.stderr)
            sys.exit(1)

        # Apply interactive framing
        framed_dream = apply_interactive_framing(
            dream_content, args.framing, args.provider, model_used,
            sources, args.style, choices_made
        )
    else:
        if args.verbose:
            print(f"Generating dream with {args.provider}...", file=sys.stderr)

        try:
            dream_content, model_used = generate_dream(prompt, args.provider, args.model)
        except urllib.error.HTTPError as e:
            print(f"Error calling {args.provider} API: {e}", file=sys.stderr)
            try:
                error_body = e.read().decode('utf-8')
                print(f"Response: {error_body}", file=sys.stderr)
            except Exception:
                pass
            sys.exit(1)
        except urllib.error.URLError as e:
            print(f"Connection error to {args.provider}: {e.reason}", file=sys.stderr)
            if args.provider == "ollama":
                print("Hint: Is Ollama running? Try: ollama serve", file=sys.stderr)
            sys.exit(1)
        except socket.timeout:
            print(f"Timeout waiting for {args.provider} API response", file=sys.stderr)
            print("Hint: Try a smaller time range or simpler style", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error generating dream: {e}", file=sys.stderr)
            sys.exit(1)

        # Apply standard framing
        framed_dream = apply_framing(
            dream_content, args.framing, args.provider, model_used, sources, args.style
        )

    # Output dream
    if args.output:
        args.output.write_text(framed_dream)
        if args.verbose:
            print(f"Dream written to: {args.output}", file=sys.stderr)
    else:
        print(framed_dream)

    # Save to dream journal if requested
    if args.save:
        dreams_dir = args.memory_path / "dreams"
        dreams_dir.mkdir(parents=True, exist_ok=True)

        date_str = datetime.now().strftime("%Y-%m-%d")
        dream_file = dreams_dir / f"{date_str}.md"

        # Build journal entry
        timestamp = datetime.now().strftime("%H:%M")
        journal_header = f"## Dream ({timestamp})\n\n"
        journal_header += f"*Provider: {args.provider} ({model_used})*\n"
        journal_header += f"*Style: {args.style}*\n"
        journal_header += f"*Sources: {', '.join(sources)}*\n\n"

        if is_interactive and choices_made:
            choices_str = ", ".join([f'"{c}"' for _, c in choices_made])
            journal_header += f"*Choices: {choices_str}*\n\n"

        journal_entry = journal_header + "---\n\n" + dream_content + "\n\n---\n\n"

        # Append if file exists, otherwise create with date header
        if dream_file.exists():
            existing = dream_file.read_text(encoding='utf-8')
            dream_file.write_text(existing + "\n" + journal_entry)
        else:
            file_header = f"# Dream Journal: {date_str}\n\n"
            dream_file.write_text(file_header + journal_entry)

        if args.verbose:
            print(f"Dream saved to journal: {dream_file}", file=sys.stderr)

    # Generate image if requested
    if args.image:
        if args.verbose:
            print(f"Generating image with {args.image_provider}...", file=sys.stderr)

        try:
            image_data = generate_image(dream_content, args.image_provider, args.image_model)

            # Determine output path
            if args.image_output:
                image_path = args.image_output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = Path(f"dream_{timestamp}.png")

            image_path.write_bytes(image_data)
            print(f"\nDream image saved to: {image_path}", file=sys.stderr)

        except urllib.error.HTTPError as e:
            print(f"Error generating image: {e}", file=sys.stderr)
            try:
                error_body = e.read().decode('utf-8')
                print(f"Response: {error_body}", file=sys.stderr)
            except Exception:
                pass
        except Exception as e:
            print(f"Error generating image: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
