# 12. Cursor + Figma MCP Prompt Playbook

Replace bracketed placeholders before use.

## Prompt 1: Initial project understanding

```text
Read AGENTS.md and all documents in /docs, beginning with 00_PROJECT_CONTEXT.md.

Do not modify code yet.

Return:
1. the fixed MVP scope,
2. frontend architecture,
3. route list,
4. API dependencies,
5. unresolved TBD values,
6. the first five implementation steps.

Do not infer unresolved project values.
```

## Prompt 2: Create foundations in Figma

```text
Using [FIGMA_FILE_URL], create or update the LocalHub design foundations according to:
- docs/05_DESIGN_SYSTEM.md
- docs/11_FIGMA_FILE_SPEC.md
- tokens/design-tokens.json

Create semantic variables for color, spacing, radius and typography.
Use Auto Layout and semantic layer names.
Do not design application screens yet.
Summarize every variable and component created.
```

## Prompt 3: Create Figma components

```text
Using [FIGMA_FILE_URL], create the LocalHub component set described in docs/06_COMPONENT_SPEC.md and docs/11_FIGMA_FILE_SPEC.md.

Required:
- Button variants and states
- Inputs and textarea states
- Category chips
- Post item/card
- Password and delete modals
- Chat widget states
- Map markers and popup

Reuse the variables already defined in the Figma file.
Use Auto Layout.
Add concise behavior annotations.
```

## Prompt 4: Design a screen in Figma

```text
Using [FIGMA_FILE_URL], design [SCREEN_NAME] for desktop and mobile.

Requirements:
- Follow docs/04_SCREEN_SPEC.md.
- Reuse components from 02_Components.
- Use variables, not raw values.
- Use semantic layers and Auto Layout.
- Include loading, empty and error variants where applicable.
- Add API, interaction and responsive annotations.
```

## Prompt 5: Implement one Figma frame in Vue

```text
Implement the exact Figma node at [FIGMA_NODE_URL] in localhub-frontend.

Required workflow:
1. Read AGENTS.md and relevant /docs files.
2. Fetch design context for the exact node.
3. Fetch its screenshot.
4. Fetch the variables used by the node.
5. Inspect the existing Vue components before writing code.
6. Translate the design to Vue 3 SFC and the existing CSS-token system.
7. Do not use React or Tailwind.
8. Do not add dependencies without explaining why.
9. Add loading, empty and error states from the specification.
10. Compare the result with the Figma screenshot at desktop and mobile sizes.

Before editing, provide a short implementation plan.
After editing, list changed files and validation performed.
```

## Prompt 6: Build frontend skeleton

```text
Create the LocalHub frontend skeleton in localhub-frontend using the structure in docs/08_FRONTEND_ARCHITECTURE.md.

Use:
- Vue 3
- Vite
- JavaScript
- Vue Router
- Axios
- global CSS tokens plus scoped CSS

Create routes and placeholder views only.
Create the shared HTTP client and service module interfaces.
Do not implement final screen styling yet.
Do not modify the backend.
```

## Prompt 7: API integration

```text
Integrate [FEATURE] with the API contract in docs/07_API_CONTRACT.md.

Rules:
- All calls go through src/services.
- Components do not call Axios directly.
- Support loading, success, empty and error states.
- Map FastAPI detail/422 errors to user-facing Korean messages.
- Never log or persist passwords.
- Do not silently change the documented API contract.

Report any backend contract mismatch instead of inventing a workaround.
```

## Prompt 8: Figma fidelity review

```text
Review the implementation for [FIGMA_NODE_URL].

Fetch the current design context and screenshot.
Compare:
- layout
- spacing
- typography
- color tokens
- radius
- responsive behavior
- interactive states

Fix only verified mismatches.
Do not rewrite unrelated code.
Return a concise before/after checklist.
```

## Prompt 9: Scope guard review

```text
Review the current frontend against docs/01_PRODUCT_REQUIREMENTS.md and docs/10_ACCEPTANCE_CRITERIA.md.

Identify:
- missing Must/Should requirements,
- accidental Won't-Have features,
- hardcoded tokens or URLs,
- direct API calls outside services,
- password/security issues,
- missing loading/empty/error states,
- mobile accessibility issues.

Do not modify code until the findings are summarized and prioritized.
```
