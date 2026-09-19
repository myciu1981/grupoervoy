## Building with GRUPO ERVOY

There is no provider and no wrapper. Components read CSS custom properties, so the only setup is the stylesheet and a theme attribute.

### Setup

Import `styles.css` once at the root. Its `@import` closure carries the tokens, the component styles and the Red Hat Display / Red Hat Text webfonts, so nothing else needs wiring.

Set the theme on `<html>`: `data-theme="light"` is the white ground and the default; `data-theme="dark"` is the Ervoy Navy ground. A page is one or the other, never both at equal weight. Inside a light page, a single navy band is done with a component's own `onDark` prop (`SiteHeader`, `Hero`, `Footer`, `ContactBlock`, `Endorsement`), not by switching the theme.

### The styling idiom: tokens, not utility classes

This system has no utility-class vocabulary. Components style themselves; style your own layout glue with the custom properties below. Never invent class names.

Colour, semantic (these flip with the theme, so prefer them): `--surface`, `--surface-sunken`, `--surface-inverse`, `--heading`, `--ink`, `--ink-secondary`, `--ink-meta`, `--ink-inverse`, `--rule`, `--rule-strong`, `--action`, `--action-ink`, `--focus-ring`.

Colour, brand literals (fixed in both themes): `--navy`, `--navy-deep`, `--crimson-deep`, `--crimson-light`, `--crimson-flat`, `--slate`, `--graphite`, `--grey-60`, `--grey-30`, `--mist`, `--white`.

Type: families `--font-display` and `--font-text`; ready-made classes `.h1`, `.h2`, `.h3`, `.subheadline`, `.section-label`, `.figure`, `.body`, `.body-lg`, `.body-emphasis`, `.small`, `.caption`.

Spacing: `--space-1`, `-2`, `-3`, `-4`, `-5`, `-6`, `-8`, `-10`, `-12`, `-16`, `-20`, `-24` (a 4px base). Radius: `--radius-none` is the default because the identity is square; `--radius-sm` and `--radius-md` exist for controls and cards. Borders: `--border-hairline`, `--border-signature`, `--border-accent`. Gradient: `--gradient-crimson`.

### Rules that are not stylistic preferences

- Crimson is one element per page, roughly 2% of it. `AccentRule` spends it, and so does `SectionLabel accent` or `KeyFigure accent`. Never two on one page.
- Never set text in `--crimson-light` or `--crimson-deep`, and never crimson text on navy (2.7:1). `--crimson-flat` is the only crimson that reads as text, and only on a light ground.
- Never `--grey-60` as text on navy (3.3:1). `--ink-meta` already resolves to `--grey-30` there.
- Headlines are sentence case, left-aligned. Capitals appear only in `SectionLabel`.
- Never a font weight above 600. Medium and Semibold carry every emphasis this system needs.
- Never recolour, stretch, rotate or add effects to `Logo`, and never render it under 160px (24px for `variant="icon"`). Leave its clear space empty.
- No shadows anywhere. Separate surfaces with `--rule`, `--rule-strong` or `--surface-sunken`.
- Budget a page at roughly 70% white, 20% navy, 8% neutrals, 2% crimson.

### Where the truth lives

Read `styles.css` and the files it imports before styling anything - they are the real values, not a summary. Per-component usage, including what each prop expects and the do-not list, is in `guidelines/` and in each component's `.prompt.md`.

### An idiomatic build

```jsx
const { SiteHeader, Hero, KeyFigure, Footer } = window.Ervoy;

<>
  <SiteHeader
    items={[{ label: "Services", href: "#services" }, { label: "Contact", href: "#contact", current: true }]}
    languages={["ES", "EN", "PL"]}
    activeLanguage="EN"
    action={{ label: "Talk to us", href: "#contact" }}
  />

  <Hero
    label="Market entry - Mexico"
    headline="Your partner for entering the Mexican market."
    subheadline="International trade, commercial representation, import/export and brand development."
    action={{ label: "Talk to us", href: "#contact" }}
  />

  {/* Layout glue is yours; every value is a token. The Hero above already spent
      the page's crimson, so none of these figures takes accent. */}
  <section style={{ background: "var(--surface-sunken)", padding: "var(--space-24) var(--space-6)" }}>
    <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: "var(--space-16)" }}>
      <KeyFigure figure="2 h" caption="Road access to the US border" />
      <KeyFigure figure="#1" caption="Industrial GDP among Mexican states" />
      <KeyFigure figure="40+" caption="European manufacturers already in the metro area" />
    </div>
  </section>

  <Footer onDark columns={[{ heading: "Contact", items: [{ label: "info@grupoervoy.com", href: "mailto:info@grupoervoy.com" }] }]} />
</>
```

# Ervoy (@ervoy/ui@1.0.0)

This design system is the published @ervoy/ui React library, bundled as a single
browser global. All 10 components are the real upstream code.

## Where things are

- `_ds_bundle.js` — the whole-DS bundle at the project root; loads every component to `window.Ervoy`. First line is a `/* @ds-bundle: … */` metadata header.
- `styles.css` — the single stylesheet entry: it `@import`s the tokens, fonts, and component styles (`_ds_bundle.css`). Link this one file.
- `components/<group>/<Name>/<Name>.prompt.md` (example JSX + variants), `<Name>.d.ts` (types), `<Name>.html` (variant grid).
- `tokens/*.css` — CSS custom properties, names verbatim from upstream.
- `fonts/` — `@font-face` files + `fonts.css` (when the package ships fonts).
- `guidelines/` — the design system's own usage guidance (10 doc(s), see `guidelines/index.md`). Read these before composing larger layouts.

For a specific component, `read_file("components/<group>/<Name>/<Name>.prompt.md")`.

## Loading

Add these two lines to your page once (React must be on the page first):

```html
<link rel="stylesheet" href="styles.css">
<script src="_ds_bundle.js"></script>
```

Components are then available at `window.Ervoy.*`. Mount into a dedicated child node (e.g. `<div id="ds-root">`), not the host page's own React root, so the two trees don't collide:

```jsx
const { AccentRule } = window.Ervoy;
ReactDOM.createRoot(document.getElementById('ds-root')).render(<AccentRule />);
```

## Tokens

48 CSS custom properties from @ervoy/ui. Names are
preserved verbatim from upstream. They are declared inside `_ds_bundle.css` (this DS ships one compiled stylesheet rather than separate token files).

- **color** (6): `--surface`, `--surface-sunken`, `--surface-inverse`, …
- **spacing** (12): `--space-1`, `--space-2`, `--space-3`, …
- **typography** (2): `--font-display`, `--font-text`
- **radius** (4): `--radius-none`, `--radius-sm`, `--radius-md`, …
- **other** (24): `--navy`, `--navy-deep`, `--crimson-deep`, …

## Components

### identity
- `AccentRule` — The crimson gradient rule. It is the page's single accent, and there is only
- `Endorsement` — The parent mark a portfolio brand carries. On a brand-owned piece the brand
- `Logo` — The GRUPO ERVOY wordmark or icon, at a size the brand book allows, optionally
- `SectionLabel` — A small caps label above a heading. The only element in the system set in

### actions
- `Button` — A text action. Primary is a navy fill, secondary a hairline outline with no

### page
- `ContactBlock` — Contact details for a person or the company, carrying the e-mail signature's
- `Hero` — The top block of a page: the one h1, its subheadline, and at most two
- `KeyFigure` — A number and the line that explains it. Three across a row is the shape the

### navigation
- `Footer` — The end of a page: the wordmark, up to three short columns, and the legal
- `SiteHeader` — The site header: wordmark left, navigation, language switcher and at most one
