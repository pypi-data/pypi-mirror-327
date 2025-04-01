import { i as pe, a as H, r as _e, g as he, w as T, d as ge, b as k, c as xe } from "./Index-BT7ebki3.js";
const C = window.ms_globals.React, L = window.ms_globals.React.useMemo, ne = window.ms_globals.React.useState, re = window.ms_globals.React.useEffect, fe = window.ms_globals.React.forwardRef, me = window.ms_globals.React.useRef, W = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.antd.ColorPicker, ye = window.ms_globals.createItemsContext.createItemsContext;
var Ee = /\s/;
function Ce(t) {
  for (var e = t.length; e-- && Ee.test(t.charAt(e)); )
    ;
  return e;
}
var Ie = /^\s+/;
function ve(t) {
  return t && t.slice(0, Ce(t) + 1).replace(Ie, "");
}
var G = NaN, Se = /^[-+]0x[0-9a-f]+$/i, Re = /^0b[01]+$/i, ke = /^0o[0-7]+$/i, Te = parseInt;
function z(t) {
  if (typeof t == "number")
    return t;
  if (pe(t))
    return G;
  if (H(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = H(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = ve(t);
  var s = Re.test(t);
  return s || ke.test(t) ? Te(t.slice(2), s ? 2 : 8) : Se.test(t) ? G : +t;
}
var A = function() {
  return _e.Date.now();
}, Pe = "Expected a function", Oe = Math.max, je = Math.min;
function Le(t, e, s) {
  var l, o, n, r, i, a, _ = 0, h = !1, c = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(Pe);
  e = z(e) || 0, H(s) && (h = !!s.leading, c = "maxWait" in s, n = c ? Oe(z(s.maxWait) || 0, e) : n, g = "trailing" in s ? !!s.trailing : g);
  function d(p) {
    var I = l, R = o;
    return l = o = void 0, _ = p, r = t.apply(R, I), r;
  }
  function w(p) {
    return _ = p, i = setTimeout(f, e), h ? d(p) : r;
  }
  function x(p) {
    var I = p - a, R = p - _, U = e - I;
    return c ? je(U, n - R) : U;
  }
  function u(p) {
    var I = p - a, R = p - _;
    return a === void 0 || I >= e || I < 0 || c && R >= n;
  }
  function f() {
    var p = A();
    if (u(p))
      return y(p);
    i = setTimeout(f, x(p));
  }
  function y(p) {
    return i = void 0, g && l ? d(p) : (l = o = void 0, r);
  }
  function E() {
    i !== void 0 && clearTimeout(i), _ = 0, l = a = o = i = void 0;
  }
  function m() {
    return i === void 0 ? r : y(A());
  }
  function v() {
    var p = A(), I = u(p);
    if (l = arguments, o = this, a = p, I) {
      if (i === void 0)
        return w(a);
      if (c)
        return clearTimeout(i), i = setTimeout(f, e), d(a);
    }
    return i === void 0 && (i = setTimeout(f, e)), r;
  }
  return v.cancel = E, v.flush = m, v;
}
var se = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Fe = C, Ae = Symbol.for("react.element"), Ne = Symbol.for("react.fragment"), We = Object.prototype.hasOwnProperty, He = Fe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Me = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function oe(t, e, s) {
  var l, o = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (l in e) We.call(e, l) && !Me.hasOwnProperty(l) && (o[l] = e[l]);
  if (t && t.defaultProps) for (l in e = t.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: Ae,
    type: t,
    key: n,
    ref: r,
    props: o,
    _owner: He.current
  };
}
F.Fragment = Ne;
F.jsx = oe;
F.jsxs = oe;
se.exports = F;
var b = se.exports;
const {
  SvelteComponent: De,
  assign: q,
  binding_callbacks: V,
  check_outros: Be,
  children: le,
  claim_element: ie,
  claim_space: Ue,
  component_subscribe: J,
  compute_slots: Ge,
  create_slot: ze,
  detach: S,
  element: ce,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: qe,
  get_slot_changes: Ve,
  group_outros: Je,
  init: Xe,
  insert_hydration: P,
  safe_not_equal: Ye,
  set_custom_element_data: ae,
  space: Ke,
  transition_in: O,
  transition_out: D,
  update_slot_base: Qe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ze,
  getContext: $e,
  onDestroy: et,
  setContext: tt
} = window.__gradio__svelte__internal;
function K(t) {
  let e, s;
  const l = (
    /*#slots*/
    t[7].default
  ), o = ze(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = ce("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = ie(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = le(e);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ae(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, e, r), o && o.m(e, null), t[9](e), s = !0;
    },
    p(n, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && Qe(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? Ve(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : qe(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (O(o, n), s = !0);
    },
    o(n) {
      D(o, n), s = !1;
    },
    d(n) {
      n && S(e), o && o.d(n), t[9](null);
    }
  };
}
function nt(t) {
  let e, s, l, o, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = ce("react-portal-target"), s = Ke(), n && n.c(), l = X(), this.h();
    },
    l(r) {
      e = ie(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), le(e).forEach(S), s = Ue(r), n && n.l(r), l = X(), this.h();
    },
    h() {
      ae(e, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      P(r, e, i), t[8](e), P(r, s, i), n && n.m(r, i), P(r, l, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = K(r), n.c(), O(n, 1), n.m(l.parentNode, l)) : n && (Je(), D(n, 1, 1, () => {
        n = null;
      }), Be());
    },
    i(r) {
      o || (O(n), o = !0);
    },
    o(r) {
      D(n), o = !1;
    },
    d(r) {
      r && (S(e), S(s), S(l)), t[8](null), n && n.d(r);
    }
  };
}
function Q(t) {
  const {
    svelteInit: e,
    ...s
  } = t;
  return s;
}
function rt(t, e, s) {
  let l, o, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const i = Ge(n);
  let {
    svelteInit: a
  } = e;
  const _ = T(Q(e)), h = T();
  J(t, h, (m) => s(0, l = m));
  const c = T();
  J(t, c, (m) => s(1, o = m));
  const g = [], d = $e("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: x,
    subSlotIndex: u
  } = he() || {}, f = a({
    parent: d,
    props: _,
    target: h,
    slot: c,
    slotKey: w,
    slotIndex: x,
    subSlotIndex: u,
    onDestroy(m) {
      g.push(m);
    }
  });
  tt("$$ms-gr-react-wrapper", f), Ze(() => {
    _.set(Q(e));
  }), et(() => {
    g.forEach((m) => m());
  });
  function y(m) {
    V[m ? "unshift" : "push"](() => {
      l = m, h.set(l);
    });
  }
  function E(m) {
    V[m ? "unshift" : "push"](() => {
      o = m, c.set(o);
    });
  }
  return t.$$set = (m) => {
    s(17, e = q(q({}, e), Y(m))), "svelteInit" in m && s(5, a = m.svelteInit), "$$scope" in m && s(6, r = m.$$scope);
  }, e = Y(e), [l, o, h, c, i, a, r, n, y, E];
}
class st extends De {
  constructor(e) {
    super(), Xe(this, e, rt, nt, Ye, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, N = window.ms_globals.tree;
function ot(t, e = {}) {
  function s(l) {
    const o = T(), n = new st({
      ...l,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: e.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? N;
          return a.nodes = [...a.nodes, i], Z({
            createPortal: W,
            node: N
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((_) => _.svelteInstance !== o), Z({
              createPortal: W,
              node: N
            });
          }), i;
        },
        ...l.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(s);
    });
  });
}
function lt(t) {
  const [e, s] = ne(() => k(t));
  return re(() => {
    let l = !0;
    return t.subscribe((n) => {
      l && (l = !1, n === e) || s(n);
    });
  }, [t]), e;
}
function it(t) {
  const e = L(() => ge(t, (s) => s), [t]);
  return lt(e);
}
function ct(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function at(t, e = !1) {
  try {
    if (xe(t))
      return t;
    if (e && !ct(t))
      return;
    if (typeof t == "string") {
      let s = t.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function $(t, e) {
  return L(() => at(t, e), [t, e]);
}
function ut(t, e) {
  const s = L(() => C.Children.toArray(t.originalChildren || t).filter((n) => n.props.node && !n.props.node.ignore && (!n.props.nodeSlotKey || e)).sort((n, r) => {
    if (n.props.node.slotIndex && r.props.node.slotIndex) {
      const i = k(n.props.node.slotIndex) || 0, a = k(r.props.node.slotIndex) || 0;
      return i - a === 0 && n.props.node.subSlotIndex && r.props.node.subSlotIndex ? (k(n.props.node.subSlotIndex) || 0) - (k(r.props.node.subSlotIndex) || 0) : i - a;
    }
    return 0;
  }).map((n) => n.props.node.target), [t, e]);
  return it(s);
}
const dt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ft(t) {
  return t ? Object.keys(t).reduce((e, s) => {
    const l = t[s];
    return e[s] = mt(s, l), e;
  }, {}) : {};
}
function mt(t, e) {
  return typeof e == "number" && !dt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], s = t.cloneNode(!1);
  if (t._reactElement) {
    const o = C.Children.toArray(t._reactElement.props.children).map((n) => {
      if (C.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = B(n.props.el);
        return C.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...C.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = t._reactElement.props.children, e.push(W(C.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: o
    }), s)), {
      clonedElement: s,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: r,
      type: i,
      useCapture: a
    }) => {
      s.addEventListener(i, r, a);
    });
  });
  const l = Array.from(t.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = B(n);
      e.push(...i), s.appendChild(r);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function pt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const j = fe(({
  slot: t,
  clone: e,
  className: s,
  style: l,
  observeAttributes: o
}, n) => {
  const r = me(), [i, a] = ne([]), {
    forceClone: _
  } = be(), h = _ ? !0 : e;
  return re(() => {
    var x;
    if (!r.current || !t)
      return;
    let c = t;
    function g() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), pt(n, u), s && u.classList.add(...s.split(" ")), l) {
        const f = ft(l);
        Object.keys(f).forEach((y) => {
          u.style[y] = f[y];
        });
      }
    }
    let d = null, w = null;
    if (h && window.MutationObserver) {
      let u = function() {
        var m, v, p;
        (m = r.current) != null && m.contains(c) && ((v = r.current) == null || v.removeChild(c));
        const {
          portals: y,
          clonedElement: E
        } = B(t);
        c = E, a(y), c.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          g();
        }, 50), (p = r.current) == null || p.appendChild(c);
      };
      u();
      const f = Le(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      d = new window.MutationObserver(f), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", g(), (x = r.current) == null || x.appendChild(c);
    return () => {
      var u, f;
      c.style.display = "", (u = r.current) != null && u.contains(c) && ((f = r.current) == null || f.removeChild(c)), d == null || d.disconnect();
    };
  }, [t, h, s, l, n, o]), C.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
}), _t = ({
  children: t,
  ...e
}) => /* @__PURE__ */ b.jsx(b.Fragment, {
  children: t(e)
});
function ue(t) {
  return C.createElement(_t, {
    children: t
  });
}
function de(t, e, s) {
  const l = t.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, n) => {
      var _;
      if (typeof o != "object")
        return o;
      const r = {
        ...o.props,
        key: ((_ = o.props) == null ? void 0 : _.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(o.slots).forEach((h) => {
        if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
          return;
        const c = h.split(".");
        c.forEach((f, y) => {
          i[f] || (i[f] = {}), y !== c.length - 1 && (i = r[f]);
        });
        const g = o.slots[h];
        let d, w, x = !1, u = e == null ? void 0 : e.forceClone;
        g instanceof Element ? d = g : (d = g.el, w = g.callback, x = g.clone ?? x, u = g.forceClone ?? u), u = u ?? !!w, i[c[c.length - 1]] = d ? w ? (...f) => (w(c[c.length - 1], f), /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          params: f,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(j, {
            slot: d,
            clone: x
          })
        })) : ue((f) => /* @__PURE__ */ b.jsx(M, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(j, {
            slot: d,
            clone: x,
            ...f
          })
        })) : i[c[c.length - 1]], i = r;
      });
      const a = "children";
      return o[a] && (r[a] = de(o[a], e, `${n}`)), r;
    });
}
function ee(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ue((s) => /* @__PURE__ */ b.jsx(M, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ b.jsx(j, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...s
    })
  })) : /* @__PURE__ */ b.jsx(j, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function te({
  key: t,
  slots: e,
  targets: s
}, l) {
  return e[t] ? (...o) => s ? s.map((n, r) => /* @__PURE__ */ b.jsx(C.Fragment, {
    children: ee(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ b.jsx(b.Fragment, {
    children: ee(e[t], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: ht,
  useItems: gt,
  ItemHandler: bt
} = ye("antd-color-picker-presets"), wt = ot(ht(["presets"], ({
  onValueChange: t,
  onChange: e,
  panelRender: s,
  showText: l,
  value: o,
  presets: n,
  children: r,
  value_format: i,
  setSlotParams: a,
  slots: _,
  ...h
}) => {
  const c = $(s), g = $(l), d = ut(r), {
    items: {
      presets: w
    }
  } = gt();
  return /* @__PURE__ */ b.jsxs(b.Fragment, {
    children: [d.length === 0 && /* @__PURE__ */ b.jsx("div", {
      style: {
        display: "none"
      },
      children: r
    }), /* @__PURE__ */ b.jsx(we, {
      ...h,
      value: o,
      presets: L(() => n || de(w), [n, w]),
      showText: _.showText ? te({
        slots: _,
        setSlotParams: a,
        key: "showText"
      }) : g || l,
      panelRender: _.panelRender ? te({
        slots: _,
        setSlotParams: a,
        key: "panelRender"
      }) : c,
      onChange: (x, ...u) => {
        if (x.isGradient()) {
          const y = x.getColors().map((E) => {
            const m = {
              rgb: E.color.toRgbString(),
              hex: E.color.toHexString(),
              hsb: E.color.toHsbString()
            };
            return {
              ...E,
              color: m[i]
            };
          });
          e == null || e(y, ...u), t(y);
          return;
        }
        const f = {
          rgb: x.toRgbString(),
          hex: x.toHexString(),
          hsb: x.toHsbString()
        };
        e == null || e(f[i], ...u), t(f[i]);
      },
      children: d.length === 0 ? null : r
    })]
  });
}));
export {
  wt as ColorPicker,
  wt as default
};
