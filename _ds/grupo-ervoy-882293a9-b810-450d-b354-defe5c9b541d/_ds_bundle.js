/* @ds-bundle: {"namespace":"Ervoy","components":[{"name":"AccentRule","sourcePath":"components/identity/AccentRule/AccentRule.jsx"},{"name":"Button","sourcePath":"components/actions/Button/Button.jsx"},{"name":"ContactBlock","sourcePath":"components/page/ContactBlock/ContactBlock.jsx"},{"name":"Endorsement","sourcePath":"components/identity/Endorsement/Endorsement.jsx"},{"name":"Footer","sourcePath":"components/navigation/Footer/Footer.jsx"},{"name":"Hero","sourcePath":"components/page/Hero/Hero.jsx"},{"name":"KeyFigure","sourcePath":"components/page/KeyFigure/KeyFigure.jsx"},{"name":"Logo","sourcePath":"components/identity/Logo/Logo.jsx"},{"name":"SectionLabel","sourcePath":"components/identity/SectionLabel/SectionLabel.jsx"},{"name":"SiteHeader","sourcePath":"components/navigation/SiteHeader/SiteHeader.jsx"}],"sourceHashes":{"components/identity/AccentRule/AccentRule.jsx":"3fddfef53866","components/identity/AccentRule/AccentRule.d.ts":"fff7dca4d180","components/identity/AccentRule/AccentRule.prompt.md":"161cfd5005d3","components/actions/Button/Button.jsx":"9f55e5fe6bad","components/actions/Button/Button.d.ts":"eea469abd1e1","components/actions/Button/Button.prompt.md":"c343c6069173","components/page/ContactBlock/ContactBlock.jsx":"12117fc5a9f2","components/page/ContactBlock/ContactBlock.d.ts":"056fd653cc6e","components/page/ContactBlock/ContactBlock.prompt.md":"3fb18082a74d","components/identity/Endorsement/Endorsement.jsx":"57ce07217d1c","components/identity/Endorsement/Endorsement.d.ts":"98019a67b6da","components/identity/Endorsement/Endorsement.prompt.md":"e07dc09bb347","components/navigation/Footer/Footer.jsx":"c1877faefa09","components/navigation/Footer/Footer.d.ts":"5c35f10b5716","components/navigation/Footer/Footer.prompt.md":"3a5e061d44c5","components/page/Hero/Hero.jsx":"1a0e7812cf67","components/page/Hero/Hero.d.ts":"92091ea76869","components/page/Hero/Hero.prompt.md":"991d7fe6e4f7","components/page/KeyFigure/KeyFigure.jsx":"6f06de1d0b55","components/page/KeyFigure/KeyFigure.d.ts":"5ab54202fa9b","components/page/KeyFigure/KeyFigure.prompt.md":"e4fead71d500","components/identity/Logo/Logo.jsx":"8f490d9a979c","components/identity/Logo/Logo.d.ts":"dd07eae8c0c5","components/identity/Logo/Logo.prompt.md":"5a57df260e01","components/identity/SectionLabel/SectionLabel.jsx":"a7582430bf6e","components/identity/SectionLabel/SectionLabel.d.ts":"ab17dff0fff9","components/identity/SectionLabel/SectionLabel.prompt.md":"432ba9c755d3","components/navigation/SiteHeader/SiteHeader.jsx":"7e4ba37d33d6","components/navigation/SiteHeader/SiteHeader.d.ts":"745a2ec8131d","components/navigation/SiteHeader/SiteHeader.prompt.md":"438cb30309f8"},"inlinedExternals":[],"builtBy":"cc-design-sync"} */
"use strict";
var Ervoy = (() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __esm = (fn, res, err) => function __init() {
    if (err) throw err[0];
    try {
      return fn && (res = (0, fn[__getOwnPropNames(fn)[0]])(fn = 0)), res;
    } catch (e) {
      throw err = [e], e;
    }
  };
  var __commonJS = (cb, mod) => function __require() {
    try {
      return mod || (0, cb[__getOwnPropNames(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
    } catch (e) {
      throw mod = 0, e;
    }
  };
  var __export = (target, all) => {
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __copyProps = (to, from, except, desc) => {
    if (from && typeof from === "object" || typeof from === "function") {
      for (let key of __getOwnPropNames(from))
        if (!__hasOwnProp.call(to, key) && key !== except)
          __defProp(to, key, { get: () => from[key], enumerable: !(desc = __getOwnPropDesc(from, key)) || desc.enumerable });
    }
    return to;
  };
  var __toESM = (mod, isNodeMode, target) => (target = mod != null ? __create(__getProtoOf(mod)) : {}, __copyProps(
    // If the importer is in node compatibility mode or this is not an ESM
    // file that has been converted to a CommonJS file using a Babel-
    // compatible transform (i.e. "__esModule" has not been set), then set
    // "default" to the CommonJS "module.exports" for node compatibility.
    isNodeMode || !mod || !mod.__esModule ? __defProp(target, "default", { value: mod, enumerable: true }) : target,
    mod
  ));
  var __toCommonJS = (mod) => __copyProps(__defProp({}, "__esModule", { value: true }), mod);

  // <define:import.meta.env>
  var init_define_import_meta_env = __esm({
    "<define:import.meta.env>"() {
    }
  });

  // shim:react-shim
  var require_react_shim = __commonJS({
    "shim:react-shim"(exports, module) {
      init_define_import_meta_env();
      var R = window.React;
      function np(p, k) {
        var o = {};
        for (var x in p) if (x !== "children") o[x] = p[x];
        if (k !== void 0) o.key = k;
        return o;
      }
      function jsx12(t, p, k) {
        var c = p && p.children;
        return c === void 0 ? R.createElement(t, np(p, k)) : R.createElement(t, np(p, k), c);
      }
      function jsxs9(t, p, k) {
        return R.createElement.apply(R, [t, np(p, k)].concat(p.children));
      }
      module.exports = R;
      module.exports.jsx = jsx12;
      module.exports.jsxs = jsxs9;
      module.exports.jsxDEV = function(t, p, k, s) {
        return (s ? jsxs9 : jsx12)(t, p, k);
      };
      module.exports.Fragment = R.Fragment;
    }
  });

  // dist/index.js
  var index_exports = {};
  __export(index_exports, {
    AccentRule: () => AccentRule,
    Button: () => Button,
    ContactBlock: () => ContactBlock,
    Endorsement: () => Endorsement,
    Footer: () => Footer,
    Hero: () => Hero,
    KeyFigure: () => KeyFigure,
    Logo: () => Logo,
    SectionLabel: () => SectionLabel,
    SiteHeader: () => SiteHeader
  });
  init_define_import_meta_env();
  var import_jsx_runtime = __toESM(require_react_shim(), 1);
  var import_jsx_runtime2 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime3 = __toESM(require_react_shim(), 1);
  var import_react = __toESM(require_react_shim(), 1);
  var import_jsx_runtime4 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime5 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime6 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime7 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime8 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime9 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime10 = __toESM(require_react_shim(), 1);
  var import_jsx_runtime11 = __toESM(require_react_shim(), 1);
  function AccentRule({ width = "72px", align = "left", className }) {
    return /* @__PURE__ */ (0, import_jsx_runtime.jsx)(
      "div",
      {
        role: "presentation",
        className: ["ervoy-accent-rule", className].filter(Boolean).join(" "),
        style: { width: align === "full" ? "100%" : width }
      }
    );
  }
  function Button({
    children,
    href,
    variant = "primary",
    onDark,
    type = "button",
    onClick,
    className
  }) {
    const cls = [
      "ervoy-btn",
      `ervoy-btn--${variant}`,
      onDark ? "ervoy-btn--on-dark" : null,
      className
    ].filter(Boolean).join(" ");
    if (href) {
      return /* @__PURE__ */ (0, import_jsx_runtime2.jsx)("a", { className: cls, href, onClick, children });
    }
    return /* @__PURE__ */ (0, import_jsx_runtime2.jsx)("button", { className: cls, type, onClick, children });
  }
  function ContactBlock({
    name,
    title,
    phones,
    email,
    website,
    address,
    onDark,
    className
  }) {
    const lines = [
      ...(phones ?? []).map((p) => ({ key: p, href: `tel:${p.replace(/[^+0-9]/g, "")}`, text: p })),
      ...email ? [{ key: email, href: `mailto:${email}`, text: email }] : [],
      ...website ? [{ key: website, href: `https://${website.replace(/^https?:\/\//, "")}`, text: website }] : []
    ];
    return /* @__PURE__ */ (0, import_jsx_runtime3.jsxs)(
      "div",
      {
        className: ["ervoy-contact", onDark ? "ervoy-contact--on-dark" : null, className].filter(Boolean).join(" "),
        children: [
          name && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("p", { className: "ervoy-contact__name", children: name }),
          title && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("p", { className: "ervoy-contact__title", children: title }),
          lines.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("div", { className: "ervoy-contact__lines", children: lines.map((l) => /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("a", { className: "ervoy-contact__line", href: l.href, children: l.text }, l.key)) }),
          address && /* @__PURE__ */ (0, import_jsx_runtime3.jsx)("p", { className: "ervoy-contact__address", children: address })
        ]
      }
    );
  }
  var NAVY = "#0A263C";
  var wordmarkViewBox = "-40 -40 3505.53 1080";
  var wordmarkRatio = 1080 / 3505.53;
  var wordmarkX = 201 / 3505.53;
  var iconViewBox = "-40 -40 1080 1080";
  var iconRatio = 1;
  var iconX = 200 / 1080;
  function wordmarkArt(ink, id) {
    const e = `wgE-${id}`;
    const v = `wgV-${id}`;
    return /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)(import_jsx_runtime4.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("defs", { children: [
        /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("linearGradient", { id: e, gradientUnits: "userSpaceOnUse", x1: "0", y1: "0", x2: "526.96", y2: "0", children: [
          /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "0", stopColor: "#651728" }),
          /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "1", stopColor: "#9F384B" })
        ] }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("linearGradient", { id: v, gradientUnits: "userSpaceOnUse", x1: "0", y1: "363.99", x2: "0", y2: "973.89", children: [
          /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "0", stopColor: "#9F384B" }),
          /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "1", stopColor: "#651728" })
        ] })
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("g", { children: [
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("rect", { fill: `url(#${e})`, x: "0", y: "363.99", width: "526.96", height: "129.2" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("rect", { fill: ink, x: "0", y: "607.16", width: "454.74", height: "125.25" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("rect", { fill: ink, x: "0", y: "846.38", width: "512.85", height: "127.51" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            d: "M619.93,363.99 H968.82 A207.32,207.32 0 0 1 1042.64,765.03 L1224.38,973.89 L1062.97,973.89 L885.22,778.62 H735.74 V973.89 H619.93 V660.94 H964.41 A89.94,89.94 0 0 0 964.41,481.05 H619.93 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "polygon",
          {
            fill: `url(#${v})`,
            points: "1223.42,366.42 1572.58,973.89 1630.94,972.42 1995.38,365.37 1817.79,364.43 1603.43,727.26 1395.35,363.99"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            fillRule: "evenodd",
            d: "M2022.05,674.12 A338.23,325.88 0 1 0 2698.5,674.12 A338.23,325.88 0 1 0 2022.05,674.12 Z M2144.99,674.12 A215.29,205.46 0 1 0 2575.56,674.12 A215.29,205.46 0 1 0 2144.99,674.12 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "polygon",
          {
            fill: ink,
            points: "2700.38,364.18 2993.5,763.13 2993.5,972.98 3116.44,973.89 3117.01,762.96 3425.53,364.54 3270.18,363.99 3055.95,633.92 2852.94,364.18"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            d: "M856.88,95.2 A100.4,100.51 0 1 1 838.59,42.47 L820.91,54.97 A78.75,78.86 0 1 0 833.95,115.4 H756.77 V95.2 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            fillRule: "evenodd",
            d: "M1120.45,3.37 H1216.93 A55.81,55.81 0 0 1 1223.7,114.58 L1279.33,196.24 L1252.94,196.24 L1196.55,114.99 H1140.93 V196.24 H1120.45 Z M1140.93,24 H1215.69 A35.81,35.81 0 0 1 1215.69,95.61 H1140.93 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            d: "M1545.84,3.01 H1566.79 V120.52 A59.42,59.42 0 0 0 1685.63,120.52 V3.01 H1706.59 V120.52 A80.38,80.38 0 0 1 1545.84,120.52 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            fillRule: "evenodd",
            d: "M1970.95,3.48 H2064.31 A55.78,55.78 0 0 1 2064.31,115.04 H1991.53 V197.02 H1970.95 Z M1991.53,23.94 H2063.14 A35.63,35.63 0 0 1 2063.14,95.21 H1991.53 Z"
          }
        ),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "path",
          {
            fill: ink,
            fillRule: "evenodd",
            d: "M2369.15,100.21 A101.58,99.61 0 1 0 2572.31,100.21 A101.58,99.61 0 1 0 2369.15,100.21 Z M2390.01,100.21 A80.72,78.74 0 1 0 2551.45,100.21 A80.72,78.74 0 1 0 2390.01,100.21 Z"
          }
        )
      ] })
    ] });
  }
  function iconArt(ink, id) {
    const b = `igB-${id}`;
    return /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)(import_jsx_runtime4.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("defs", { children: /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("linearGradient", { id: b, gradientUnits: "userSpaceOnUse", x1: "35", y1: "0", x2: "525.45", y2: "0", children: [
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "0", stopColor: "#651728" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("stop", { offset: "1", stopColor: "#9F384B" })
      ] }) }),
      /* @__PURE__ */ (0, import_jsx_runtime4.jsxs)("g", { children: [
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("rect", { fill: ink, x: "0", y: "0", width: "1000", height: "1000", rx: "162.81", ry: "162.81" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("polygon", { fill: `url(#${b})`, points: "308.6,336.94 249.15,213.84 35.12,214.19 35.1,336.42" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("polygon", { fill: `url(#${b})`, points: "35.35,435.78 35,556.58 410.98,557.22 351.09,435.09" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("polygon", { fill: `url(#${b})`, points: "525.45,776.66 465.19,654.59 35.27,654.65 35.08,776.01" }),
        /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
          "polygon",
          {
            fill: "#FFFFFF",
            points: "965,214.61 811.09,214.61 638.4,525.41 492.53,214.61 342.55,214.62 630.37,786.16"
          }
        )
      ] })
    ] });
  }
  function iconWhiteArt() {
    return /* @__PURE__ */ (0, import_jsx_runtime4.jsx)("g", { children: /* @__PURE__ */ (0, import_jsx_runtime4.jsx)(
      "path",
      {
        fill: "#FFFFFF",
        fillRule: "evenodd",
        d: "M162.81,0 H837.19 A162.81,162.81 0 0 1 1000,162.81 V837.19 A162.81,162.81 0 0 1 837.19,1000 H162.81 A162.81,162.81 0 0 1 0,837.19 V162.81 A162.81,162.81 0 0 1 162.81,0 Z M308.6,336.94 L249.15,213.84 L35.12,214.19 L35.1,336.42 Z M35.35,435.78 L35,556.58 L410.98,557.22 L351.09,435.09 Z M525.45,776.66 L465.19,654.59 L35.27,654.65 L35.08,776.01 Z M965,214.61 L811.09,214.61 L638.4,525.41 L492.53,214.61 L342.55,214.62 L630.37,786.16 Z"
      }
    ) });
  }
  function Logo({
    variant = "wordmark",
    tone = "auto",
    width,
    clearSpace,
    className
  }) {
    const id = (0, import_react.useId)().replace(/[^a-zA-Z0-9]/g, "");
    const isIcon = variant === "icon";
    const min = isIcon ? 24 : 160;
    let w = width ?? (isIcon ? 48 : 180);
    if (w < min) {
      if (typeof console !== "undefined") {
        console.warn(
          `[Ervoy.Logo] ${variant} below its minimum reproduction size (${min}px). Clamped. Use the icon instead of a small wordmark.`
        );
      }
      w = min;
    }
    const viewBox = isIcon ? iconViewBox : wordmarkViewBox;
    const ratio = isIcon ? iconRatio : wordmarkRatio;
    const unit = isIcon ? iconX : wordmarkX;
    const svgProps = {
      viewBox,
      width: w,
      height: Math.round(w * ratio),
      role: "img",
      "aria-label": "GRUPO ERVOY",
      focusable: "false",
      xmlns: "http://www.w3.org/2000/svg"
    };
    const pad = clearSpace ? Math.round(w * unit) * (clearSpace === 2 ? 2 : 1) : void 0;
    const body = isIcon ? tone === "auto" ? /* @__PURE__ */ (0, import_jsx_runtime5.jsxs)(import_jsx_runtime5.Fragment, { children: [
      /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("svg", { ...svgProps, className: "ervoy-logo__on-light", children: iconArt(NAVY, id) }),
      /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("svg", { ...svgProps, className: "ervoy-logo__on-dark", children: iconWhiteArt() })
    ] }) : tone === "white" ? /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("svg", { ...svgProps, children: iconWhiteArt() }) : /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("svg", { ...svgProps, children: iconArt(tone === "primary" ? NAVY : "#FFFFFF", id) }) : /* @__PURE__ */ (0, import_jsx_runtime5.jsx)("svg", { ...svgProps, children: wordmarkArt(
      tone === "auto" ? `var(--ervoy-logo-ink, ${NAVY})` : tone === "primary" ? NAVY : "#FFFFFF",
      id
    ) });
    return /* @__PURE__ */ (0, import_jsx_runtime5.jsx)(
      "span",
      {
        className: ["ervoy-logo", className].filter(Boolean).join(" "),
        "data-variant": variant,
        "data-tone": tone,
        "data-clear-space": clearSpace ? clearSpace === 2 ? "2X" : "1X" : void 0,
        style: pad ? { padding: pad } : void 0,
        children: body
      }
    );
  }
  function Endorsement({
    wording = "A GRUPO ERVOY company",
    tone = "auto",
    width = 160,
    onDark
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime6.jsxs)(
      "div",
      {
        className: ["ervoy-endorsement", onDark ? "ervoy-endorsement--on-dark" : null].filter(Boolean).join(" "),
        children: [
          /* @__PURE__ */ (0, import_jsx_runtime6.jsx)("p", { className: "ervoy-endorsement__wording", children: wording }),
          /* @__PURE__ */ (0, import_jsx_runtime6.jsx)(Logo, { tone, width })
        ]
      }
    );
  }
  function Footer({
    legal = "GRUPO ERVOY, S.A. de C.V. \xB7 Monterrey, Nuevo Le\xF3n, M\xE9xico",
    columns,
    onDark
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime7.jsxs)("footer", { className: ["ervoy-footer", onDark ? "ervoy-footer--on-dark" : null].filter(Boolean).join(" "), children: [
      /* @__PURE__ */ (0, import_jsx_runtime7.jsxs)("div", { className: "ervoy-footer__top", children: [
        /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("div", { className: "ervoy-footer__brand", children: /* @__PURE__ */ (0, import_jsx_runtime7.jsx)(Logo, { width: 160 }) }),
        (columns ?? []).map((col, i) => /* @__PURE__ */ (0, import_jsx_runtime7.jsxs)("div", { className: "ervoy-footer__col", children: [
          col.heading && /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("p", { className: "ervoy-footer__heading", children: col.heading }),
          (col.items ?? []).map(
            (item) => item.href ? /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("a", { className: "ervoy-footer__link", href: item.href, children: item.label }, item.label) : /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("p", { className: "ervoy-footer__text", children: item.label }, item.label)
          )
        ] }, col.heading ?? i))
      ] }),
      /* @__PURE__ */ (0, import_jsx_runtime7.jsx)("p", { className: "ervoy-footer__legal", children: legal })
    ] });
  }
  function SectionLabel({ children, accent, className }) {
    return /* @__PURE__ */ (0, import_jsx_runtime8.jsx)(
      "p",
      {
        className: ["ervoy-section-label", accent ? "is-accent" : null, className].filter(Boolean).join(" "),
        children
      }
    );
  }
  function Hero({
    label,
    headline,
    subheadline,
    action,
    secondaryAction,
    onDark,
    accentRule = true
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("section", { className: ["ervoy-hero", onDark ? "ervoy-hero--on-dark" : null].filter(Boolean).join(" "), children: /* @__PURE__ */ (0, import_jsx_runtime9.jsxs)("div", { className: "ervoy-hero__inner", children: [
      label && /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(SectionLabel, { children: label }),
      accentRule && /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(AccentRule, {}),
      /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("h1", { className: "ervoy-hero__headline", children: headline }),
      subheadline && /* @__PURE__ */ (0, import_jsx_runtime9.jsx)("p", { className: "ervoy-hero__sub", children: subheadline }),
      (action || secondaryAction) && /* @__PURE__ */ (0, import_jsx_runtime9.jsxs)("div", { className: "ervoy-hero__actions", children: [
        action && /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(Button, { href: action.href, onDark, children: action.label }),
        secondaryAction && /* @__PURE__ */ (0, import_jsx_runtime9.jsx)(Button, { href: secondaryAction.href, variant: "secondary", onDark, children: secondaryAction.label })
      ] })
    ] }) });
  }
  function KeyFigure({ figure, caption, accent, className }) {
    return /* @__PURE__ */ (0, import_jsx_runtime10.jsxs)("div", { className: ["ervoy-figure", accent ? "is-accent" : null, className].filter(Boolean).join(" "), children: [
      /* @__PURE__ */ (0, import_jsx_runtime10.jsx)("p", { className: "ervoy-figure__value", children: figure }),
      caption && /* @__PURE__ */ (0, import_jsx_runtime10.jsx)("p", { className: "ervoy-figure__caption", children: caption })
    ] });
  }
  function SiteHeader({
    items,
    languages,
    activeLanguage,
    action,
    onDark,
    compact,
    homeHref = "/",
    logoWidth = 180
  }) {
    return /* @__PURE__ */ (0, import_jsx_runtime11.jsxs)("header", { className: ["ervoy-header", onDark ? "ervoy-header--on-dark" : null].filter(Boolean).join(" "), children: [
      /* @__PURE__ */ (0, import_jsx_runtime11.jsx)("a", { className: "ervoy-header__home", href: homeHref, "aria-label": "GRUPO ERVOY - home", children: compact ? /* @__PURE__ */ (0, import_jsx_runtime11.jsx)(Logo, { variant: "icon", width: 36 }) : /* @__PURE__ */ (0, import_jsx_runtime11.jsx)(Logo, { width: logoWidth }) }),
      /* @__PURE__ */ (0, import_jsx_runtime11.jsxs)("div", { className: "ervoy-header__right", children: [
        items && items.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime11.jsx)("nav", { className: "ervoy-header__nav", "aria-label": "Main", children: items.map((item) => /* @__PURE__ */ (0, import_jsx_runtime11.jsx)(
          "a",
          {
            className: "ervoy-header__link",
            href: item.href ?? "#",
            "aria-current": item.current ? "page" : void 0,
            children: item.label
          },
          item.label
        )) }),
        languages && languages.length > 0 && /* @__PURE__ */ (0, import_jsx_runtime11.jsx)("div", { className: "ervoy-header__langs", "aria-label": "Language", children: languages.map((code, i) => /* @__PURE__ */ (0, import_jsx_runtime11.jsxs)("span", { style: { display: "contents" }, children: [
          i > 0 && /* @__PURE__ */ (0, import_jsx_runtime11.jsx)("span", { className: "ervoy-header__sep", children: "/" }),
          /* @__PURE__ */ (0, import_jsx_runtime11.jsx)(
            "a",
            {
              className: ["ervoy-header__lang", code === activeLanguage ? "is-active" : null].filter(Boolean).join(" "),
              href: `#${code.toLowerCase()}`,
              "aria-current": code === activeLanguage ? "true" : void 0,
              children: code
            }
          )
        ] }, code)) }),
        action && /* @__PURE__ */ (0, import_jsx_runtime11.jsx)(Button, { href: action.href, onDark, children: action.label })
      ] })
    ] });
  }
  return __toCommonJS(index_exports);
})();
window.Ervoy=Ervoy.__dsMainNs?Object.assign({},Ervoy,Ervoy.__dsMainNs,{__dsMainNs:undefined}):Ervoy;
