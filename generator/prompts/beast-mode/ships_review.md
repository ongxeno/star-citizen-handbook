use info from these prompts to create a new ship review page.

first read this prompt for overall structure of the blog: generator\ship-handbook-template.md

use #sc-mcp find-vehicle to get any ship information you need. It could be for the main ship you are reviewing or ships that use for comparison.

use the rest of these prompt to generate each section.
generator\prompts\ships\generate-ship-data.md
generator\prompts\ships\section-1-overview.md
generator\prompts\ships\section-2-exterior.md
generator\prompts\ships\section-3-interior.md
generator\prompts\ships\section-4-flight.md
generator\prompts\ships\section-5-components.md
generator\prompts\ships\section-6-defenses.md
generator\prompts\ships\section-7-comparisons.md
generator\prompts\ships\section-8-tactics.md
generator\prompts\ships\section-9-who-is-this-for.md

combine all section, then polish language following this prompt.
generator\prompts\ships\polish-thai-content.md

put the final markdown article in content\ships.
add link to the new page from content\ships_index.md.