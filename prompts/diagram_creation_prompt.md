# Professional Diagram Creation Prompt

## Task
Create a professional, clean SVG diagram based on the provided text. The diagram should **accurately represent the logical flow and relationships** described in the text, while following modern UI design principles.

## CRITICAL: Flow Accuracy First
- **Analyze the text first** - does it describe a process flow, relationships, hierarchy, or static information?
- **Only create flow arrows** when the text explicitly describes a process or sequence
- **If no flow exists**, create appropriate diagram types (hierarchical, comparative, categorical, etc.)
- **The diagram structure must match the text's logical organization**, not force a flow where none exists

## Design Requirements

### Layout & Spacing
- Use canvas size: 1000x650 pixels for optimal content spacing
- Maintain 80px margins on left/right sides
- Create appropriately sized boxes based on content
- Ensure all elements have breathing room - no cramped appearance
- Center all elements horizontally around the 500px center point

### Visual Design
- Use white background (#ffffff) for clean appearance
- Implement rounded corners (8px radius) on all boxes
- Use subtle borders (2px stroke) with proper contrast
- Apply consistent color schemes that match content relationships

### Typography
- Title: 24px, bold, dark color (#1f2937)
- Subtitle: 16px, medium gray (#6b7280)
- Box headers: 16px, bold, white text on colored backgrounds
- Body text: 12px, appropriate contrast colors
- Arrow labels: 11-13px, bold, matching arrow colors

### Color Scheme
- Input/Starting points: Light blue (#dbeafe) with blue border (#3b82f6)
- Process/Algorithm: Light red (#fee2e2) with red border (#ef4444)
- Output/Results: Light green (#d1fae5) with green border (#10b981)
- Examples/Details: Light orange (#fef3c7) with orange border (#f59e0b)
- Information boxes: Light gray (#f3f4f6) with gray border (#d1d5db)

### Arrows & Connections
- **ONLY use arrows when text describes actual flow/process**
- Use 2px stroke width for all arrows
- Create 6x4 pixel arrowheads that match destination box colors
- Position arrow labels 10px above arrows for proper spacing
- Ensure bidirectional flows are clearly separated (30px minimum between arrows)
- Use consistent arrow styling throughout

### Content Organization
- **Structure must match the text's logical organization**
- Main content boxes at the top (y=120)
- Supporting elements below with proper spacing
- Information boxes at bottom, horizontally centered
- Add subtle decorative elements (3 colored dots) between title and content
- Maintain logical flow and clear visual hierarchy

### Technical Requirements
- Create valid SVG with proper XML formatting
- Use Arial font family for maximum compatibility
- Include proper arrow marker definitions when arrows are used
- Ensure all text is properly positioned and legible
- Create a professional, publication-ready diagram

## Output Format
Generate a complete SVG file that can be opened in any SVG viewer. The diagram should be self-contained with all necessary definitions and styling.

## Example Structure (Adapt based on text content)
1. Title and subtitle at top
2. Decorative dots below title
3. **Content boxes organized according to text logic** (not forced into flow)
4. **Arrows only when text describes process flow**
5. Supporting content below main elements
6. Information boxes at bottom, centered
7. All elements properly spaced and aligned

## Quality Standards
- **Accurate representation of text content and relationships**
- Perfect horizontal symmetry
- Consistent spacing throughout
- Professional color coordination
- Clear visual organization that matches text logic
- No overlapping or cramped elements
- Clean, modern appearance suitable for presentations or documentation

## IMPORTANT: Text Analysis First
Before creating any diagram:
1. **Identify the text type**: Process flow, comparison, hierarchy, categorization, etc.
2. **Map the logical relationships** described in the text
3. **Choose appropriate diagram structure** that matches the text
4. **Only add flow arrows** when the text explicitly describes a process
5. **Ensure the visual representation accurately reflects the text's meaning**
