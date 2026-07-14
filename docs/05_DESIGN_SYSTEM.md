# 05. Design System

## Visual direction

Friendly, trustworthy and lightweight local travel service.

- Use generous whitespace.
- Prefer clear cards and restrained shadows.
- Use the primary blue for main actions.
- Use teal for location/map accents.
- Use amber sparingly for highlights.
- Avoid decorative gradients unless approved in Figma.

## Color tokens

| Token | Value | Usage |
|---|---:|---|
| `color.brand.600` | `#2563EB` | Primary buttons and active navigation |
| `color.brand.700` | `#1D4ED8` | Hover/pressed |
| `color.secondary.600` | `#0D9488` | Map and local information accents |
| `color.accent.500` | `#F59E0B` | Limited highlights |
| `color.success.600` | `#16A34A` | Success |
| `color.danger.600` | `#DC2626` | Delete and destructive errors |
| `color.neutral.950` | `#0F172A` | Main text |
| `color.neutral.700` | `#334155` | Secondary text |
| `color.neutral.500` | `#64748B` | Muted text |
| `color.neutral.300` | `#CBD5E1` | Borders |
| `color.neutral.100` | `#F1F5F9` | Subtle surface |
| `color.neutral.50` | `#F8FAFC` | Page background |
| `color.white` | `#FFFFFF` | Card surface |

## Typography

Font stack:

```css
"Pretendard", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

| Token | Size/line-height | Weight |
|---|---|---|
| `display` | 40/52 | 700 |
| `heading-1` | 32/42 | 700 |
| `heading-2` | 24/34 | 700 |
| `heading-3` | 20/30 | 600 |
| `body-lg` | 18/29 | 400 |
| `body` | 16/26 | 400 |
| `body-sm` | 14/22 | 400 |
| `caption` | 12/18 | 500 |

Mobile display and H1 may reduce one step.

## Spacing

Use only this scale unless Figma has an approved exception:

```text
0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80
```

## Radius

| Token | Value |
|---|---:|
| `radius.sm` | 8px |
| `radius.md` | 12px |
| `radius.lg` | 16px |
| `radius.full` | 999px |

## Shadows

- Card: subtle
- Dialog/chat: medium
- Do not stack multiple shadows.

## Breakpoints

| Name | Width |
|---|---:|
| Mobile | 0–767px |
| Tablet | 768–1023px |
| Desktop | 1024px+ |

## Accessibility

- Text contrast should meet WCAG AA.
- Interactive controls have at least 44×44px touch targets when practical.
- Focus states cannot rely on color alone.
- Modals trap focus and close with Escape.
- Form errors are associated with inputs.
