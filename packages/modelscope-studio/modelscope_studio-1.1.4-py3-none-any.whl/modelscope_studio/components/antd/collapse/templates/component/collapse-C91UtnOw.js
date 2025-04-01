import { i as fe, a as W, r as de, g as me, w as k, b as he } from "./Index-BFVXhvX8.js";
const C = window.ms_globals.React, Z = window.ms_globals.React.useMemo, ce = window.ms_globals.React.forwardRef, ie = window.ms_globals.React.useRef, ae = window.ms_globals.React.useState, ue = window.ms_globals.React.useEffect, N = window.ms_globals.ReactDOM.createPortal, _e = window.ms_globals.internalContext.useContextPropsContext, A = window.ms_globals.internalContext.ContextPropsProvider, ge = window.ms_globals.antd.Collapse, pe = window.ms_globals.createItemsContext.createItemsContext;
var xe = /\s/;
function be(t) {
  for (var e = t.length; e-- && xe.test(t.charAt(e)); )
    ;
  return e;
}
var we = /^\s+/;
function ye(t) {
  return t && t.slice(0, be(t) + 1).replace(we, "");
}
var B = NaN, Ce = /^[-+]0x[0-9a-f]+$/i, Ee = /^0b[01]+$/i, ve = /^0o[0-7]+$/i, Ie = parseInt;
function H(t) {
  if (typeof t == "number")
    return t;
  if (fe(t))
    return B;
  if (W(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = W(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = ye(t);
  var s = Ee.test(t);
  return s || ve.test(t) ? Ie(t.slice(2), s ? 2 : 8) : Ce.test(t) ? B : +t;
}
var L = function() {
  return de.Date.now();
}, Se = "Expected a function", Re = Math.max, ke = Math.min;
function Oe(t, e, s) {
  var o, l, n, r, c, a, g = 0, _ = !1, i = !1, p = !0;
  if (typeof t != "function")
    throw new TypeError(Se);
  e = H(e) || 0, W(s) && (_ = !!s.leading, i = "maxWait" in s, n = i ? Re(H(s.maxWait) || 0, e) : n, p = "trailing" in s ? !!s.trailing : p);
  function d(h) {
    var E = o, R = l;
    return o = l = void 0, g = h, r = t.apply(R, E), r;
  }
  function b(h) {
    return g = h, c = setTimeout(m, e), _ ? d(h) : r;
  }
  function w(h) {
    var E = h - a, R = h - g, U = e - E;
    return i ? ke(U, n - R) : U;
  }
  function u(h) {
    var E = h - a, R = h - g;
    return a === void 0 || E >= e || E < 0 || i && R >= n;
  }
  function m() {
    var h = L();
    if (u(h))
      return y(h);
    c = setTimeout(m, w(h));
  }
  function y(h) {
    return c = void 0, p && o ? d(h) : (o = l = void 0, r);
  }
  function S() {
    c !== void 0 && clearTimeout(c), g = 0, o = a = l = c = void 0;
  }
  function f() {
    return c === void 0 ? r : y(L());
  }
  function v() {
    var h = L(), E = u(h);
    if (o = arguments, l = this, a = h, E) {
      if (c === void 0)
        return b(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), d(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), r;
  }
  return v.cancel = S, v.flush = f, v;
}
var $ = {
  exports: {}
}, j = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Pe = C, Te = Symbol.for("react.element"), je = Symbol.for("react.fragment"), Le = Object.prototype.hasOwnProperty, Fe = Pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ee(t, e, s) {
  var o, l = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (o in e) Le.call(e, o) && !Ne.hasOwnProperty(o) && (l[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: Te,
    type: t,
    key: n,
    ref: r,
    props: l,
    _owner: Fe.current
  };
}
j.Fragment = je;
j.jsx = ee;
j.jsxs = ee;
$.exports = j;
var x = $.exports;
const {
  SvelteComponent: We,
  assign: z,
  binding_callbacks: G,
  check_outros: Ae,
  children: te,
  claim_element: ne,
  claim_space: Me,
  component_subscribe: q,
  compute_slots: De,
  create_slot: Ue,
  detach: I,
  element: re,
  empty: V,
  exclude_internal_props: J,
  get_all_dirty_from_scope: Be,
  get_slot_changes: He,
  group_outros: ze,
  init: Ge,
  insert_hydration: O,
  safe_not_equal: qe,
  set_custom_element_data: le,
  space: Ve,
  transition_in: P,
  transition_out: M,
  update_slot_base: Je
} = window.__gradio__svelte__internal, {
  beforeUpdate: Xe,
  getContext: Ye,
  onDestroy: Ke,
  setContext: Qe
} = window.__gradio__svelte__internal;
function X(t) {
  let e, s;
  const o = (
    /*#slots*/
    t[7].default
  ), l = Ue(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = re("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = ne(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = te(e);
      l && l.l(r), r.forEach(I), this.h();
    },
    h() {
      le(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      O(n, e, r), l && l.m(e, null), t[9](e), s = !0;
    },
    p(n, r) {
      l && l.p && (!s || r & /*$$scope*/
      64) && Je(
        l,
        o,
        n,
        /*$$scope*/
        n[6],
        s ? He(
          o,
          /*$$scope*/
          n[6],
          r,
          null
        ) : Be(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (P(l, n), s = !0);
    },
    o(n) {
      M(l, n), s = !1;
    },
    d(n) {
      n && I(e), l && l.d(n), t[9](null);
    }
  };
}
function Ze(t) {
  let e, s, o, l, n = (
    /*$$slots*/
    t[4].default && X(t)
  );
  return {
    c() {
      e = re("react-portal-target"), s = Ve(), n && n.c(), o = V(), this.h();
    },
    l(r) {
      e = ne(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), te(e).forEach(I), s = Me(r), n && n.l(r), o = V(), this.h();
    },
    h() {
      le(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      O(r, e, c), t[8](e), O(r, s, c), n && n.m(r, c), O(r, o, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && P(n, 1)) : (n = X(r), n.c(), P(n, 1), n.m(o.parentNode, o)) : n && (ze(), M(n, 1, 1, () => {
        n = null;
      }), Ae());
    },
    i(r) {
      l || (P(n), l = !0);
    },
    o(r) {
      M(n), l = !1;
    },
    d(r) {
      r && (I(e), I(s), I(o)), t[8](null), n && n.d(r);
    }
  };
}
function Y(t) {
  const {
    svelteInit: e,
    ...s
  } = t;
  return s;
}
function $e(t, e, s) {
  let o, l, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = De(n);
  let {
    svelteInit: a
  } = e;
  const g = k(Y(e)), _ = k();
  q(t, _, (f) => s(0, o = f));
  const i = k();
  q(t, i, (f) => s(1, l = f));
  const p = [], d = Ye("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: w,
    subSlotIndex: u
  } = me() || {}, m = a({
    parent: d,
    props: g,
    target: _,
    slot: i,
    slotKey: b,
    slotIndex: w,
    subSlotIndex: u,
    onDestroy(f) {
      p.push(f);
    }
  });
  Qe("$$ms-gr-react-wrapper", m), Xe(() => {
    g.set(Y(e));
  }), Ke(() => {
    p.forEach((f) => f());
  });
  function y(f) {
    G[f ? "unshift" : "push"](() => {
      o = f, _.set(o);
    });
  }
  function S(f) {
    G[f ? "unshift" : "push"](() => {
      l = f, i.set(l);
    });
  }
  return t.$$set = (f) => {
    s(17, e = z(z({}, e), J(f))), "svelteInit" in f && s(5, a = f.svelteInit), "$$scope" in f && s(6, r = f.$$scope);
  }, e = J(e), [o, l, _, i, c, a, r, n, y, S];
}
class et extends We {
  constructor(e) {
    super(), Ge(this, e, $e, Ze, qe, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, F = window.ms_globals.tree;
function tt(t, e = {}) {
  function s(o) {
    const l = k(), n = new et({
      ...o,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: e.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? F;
          return a.nodes = [...a.nodes, c], K({
            createPortal: N,
            node: F
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((g) => g.svelteInstance !== l), K({
              createPortal: N,
              node: F
            });
          }), c;
        },
        ...o.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(s);
    });
  });
}
function nt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function rt(t, e = !1) {
  try {
    if (he(t))
      return t;
    if (e && !nt(t))
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
function lt(t, e) {
  return Z(() => rt(t, e), [t, e]);
}
const st = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(t) {
  return t ? Object.keys(t).reduce((e, s) => {
    const o = t[s];
    return e[s] = ct(s, o), e;
  }, {}) : {};
}
function ct(t, e) {
  return typeof e == "number" && !st.includes(t) ? e + "px" : e;
}
function D(t) {
  const e = [], s = t.cloneNode(!1);
  if (t._reactElement) {
    const l = C.Children.toArray(t._reactElement.props.children).map((n) => {
      if (C.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = D(n.props.el);
        return C.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...C.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(N(C.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), s)), {
      clonedElement: s,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: r,
      type: c,
      useCapture: a
    }) => {
      s.addEventListener(c, r, a);
    });
  });
  const o = Array.from(t.childNodes);
  for (let l = 0; l < o.length; l++) {
    const n = o[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = D(n);
      e.push(...c), s.appendChild(r);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function it(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const T = ce(({
  slot: t,
  clone: e,
  className: s,
  style: o,
  observeAttributes: l
}, n) => {
  const r = ie(), [c, a] = ae([]), {
    forceClone: g
  } = _e(), _ = g ? !0 : e;
  return ue(() => {
    var w;
    if (!r.current || !t)
      return;
    let i = t;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), it(n, u), s && u.classList.add(...s.split(" ")), o) {
        const m = ot(o);
        Object.keys(m).forEach((y) => {
          u.style[y] = m[y];
        });
      }
    }
    let d = null, b = null;
    if (_ && window.MutationObserver) {
      let u = function() {
        var f, v, h;
        (f = r.current) != null && f.contains(i) && ((v = r.current) == null || v.removeChild(i));
        const {
          portals: y,
          clonedElement: S
        } = D(t);
        i = S, a(y), i.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          p();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      u();
      const m = Oe(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (w = r.current) == null || w.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((m = r.current) == null || m.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, _, s, o, n, l]), C.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
}), at = ({
  children: t,
  ...e
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: t(e)
});
function se(t) {
  return C.createElement(at, {
    children: t
  });
}
function oe(t, e, s) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((l, n) => {
      var g;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(l.slots).forEach((_) => {
        if (!l.slots[_] || !(l.slots[_] instanceof Element) && !l.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((m, y) => {
          c[m] || (c[m] = {}), y !== i.length - 1 && (c = r[m]);
        });
        const p = l.slots[_];
        let d, b, w = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        p instanceof Element ? d = p : (d = p.el, b = p.callback, w = p.clone ?? w, u = p.forceClone ?? u), u = u ?? !!b, c[i[i.length - 1]] = d ? b ? (...m) => (b(i[i.length - 1], m), /* @__PURE__ */ x.jsx(A, {
          ...l.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(T, {
            slot: d,
            clone: w
          })
        })) : se((m) => /* @__PURE__ */ x.jsx(A, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(T, {
            slot: d,
            clone: w,
            ...m
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return l[a] ? r[a] = oe(l[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function Q(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? se((s) => /* @__PURE__ */ x.jsx(A, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ x.jsx(T, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...s
    })
  })) : /* @__PURE__ */ x.jsx(T, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ut({
  key: t,
  slots: e,
  targets: s
}, o) {
  return e[t] ? (...l) => s ? s.map((n, r) => /* @__PURE__ */ x.jsx(C.Fragment, {
    children: Q(n, {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ x.jsx(x.Fragment, {
    children: Q(e[t], {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: ft,
  useItems: dt,
  ItemHandler: ht
} = pe("antd-collapse-items"), _t = tt(ft(["default", "items"], ({
  slots: t,
  items: e,
  children: s,
  onChange: o,
  setSlotParams: l,
  expandIcon: n,
  ...r
}) => {
  const {
    items: c
  } = dt(), a = c.items.length > 0 ? c.items : c.default, g = lt(n);
  return /* @__PURE__ */ x.jsxs(x.Fragment, {
    children: [/* @__PURE__ */ x.jsx("div", {
      style: {
        display: "none"
      },
      children: s
    }), /* @__PURE__ */ x.jsx(ge, {
      ...r,
      onChange: (_) => {
        o == null || o(_);
      },
      expandIcon: t.expandIcon ? ut({
        slots: t,
        setSlotParams: l,
        key: "expandIcon"
      }) : g,
      items: Z(() => e || oe(a, {
        // for the children slot
        // clone: true,
      }), [e, a])
    })]
  });
}));
export {
  _t as Collapse,
  _t as default
};
