import { i as ae, a as W, r as ue, g as de, w as k, b as fe } from "./Index-gRnxK_JU.js";
const y = window.ms_globals.React, oe = window.ms_globals.React.forwardRef, le = window.ms_globals.React.useRef, ie = window.ms_globals.React.useState, ce = window.ms_globals.React.useEffect, Z = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, me = window.ms_globals.internalContext.useContextPropsContext, _e = window.ms_globals.internalContext.ContextPropsProvider, pe = window.ms_globals.antd.Slider, he = window.ms_globals.createItemsContext.createItemsContext;
var ge = /\s/;
function be(e) {
  for (var t = e.length; t-- && ge.test(e.charAt(t)); )
    ;
  return t;
}
var we = /^\s+/;
function xe(e) {
  return e && e.slice(0, be(e) + 1).replace(we, "");
}
var U = NaN, ye = /^[-+]0x[0-9a-f]+$/i, Ce = /^0b[01]+$/i, Ee = /^0o[0-7]+$/i, Ie = parseInt;
function G(e) {
  if (typeof e == "number")
    return e;
  if (ae(e))
    return U;
  if (W(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = W(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = xe(e);
  var n = Ce.test(e);
  return n || Ee.test(e) ? Ie(e.slice(2), n ? 2 : 8) : ye.test(e) ? U : +e;
}
var F = function() {
  return ue.Date.now();
}, Se = "Expected a function", Pe = Math.max, Re = Math.min;
function ke(e, t, n) {
  var l, o, r, s, i, u, _ = 0, g = !1, c = !1, b = !0;
  if (typeof e != "function")
    throw new TypeError(Se);
  t = G(t) || 0, W(n) && (g = !!n.leading, c = "maxWait" in n, r = c ? Pe(G(n.maxWait) || 0, t) : r, b = "trailing" in n ? !!n.trailing : b);
  function f(d) {
    var C = l, R = o;
    return l = o = void 0, _ = d, s = e.apply(R, C), s;
  }
  function w(d) {
    return _ = d, i = setTimeout(p, t), g ? f(d) : s;
  }
  function E(d) {
    var C = d - u, R = d - _, D = t - C;
    return c ? Re(D, r - R) : D;
  }
  function m(d) {
    var C = d - u, R = d - _;
    return u === void 0 || C >= t || C < 0 || c && R >= r;
  }
  function p() {
    var d = F();
    if (m(d))
      return x(d);
    i = setTimeout(p, E(d));
  }
  function x(d) {
    return i = void 0, b && l ? f(d) : (l = o = void 0, s);
  }
  function P() {
    i !== void 0 && clearTimeout(i), _ = 0, l = u = o = i = void 0;
  }
  function a() {
    return i === void 0 ? s : x(F());
  }
  function I() {
    var d = F(), C = m(d);
    if (l = arguments, o = this, u = d, C) {
      if (i === void 0)
        return w(u);
      if (c)
        return clearTimeout(i), i = setTimeout(p, t), f(u);
    }
    return i === void 0 && (i = setTimeout(p, t)), s;
  }
  return I.cancel = P, I.flush = a, I;
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
var Te = y, Oe = Symbol.for("react.element"), ve = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Fe = Te.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ee(e, t, n) {
  var l, o = {}, r = null, s = null;
  n !== void 0 && (r = "" + n), t.key !== void 0 && (r = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (l in t) je.call(t, l) && !Le.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: Oe,
    type: e,
    key: r,
    ref: s,
    props: o,
    _owner: Fe.current
  };
}
j.Fragment = ve;
j.jsx = ee;
j.jsxs = ee;
$.exports = j;
var h = $.exports;
const {
  SvelteComponent: Ne,
  assign: H,
  binding_callbacks: z,
  check_outros: We,
  children: te,
  claim_element: ne,
  claim_space: Ae,
  component_subscribe: B,
  compute_slots: Me,
  create_slot: De,
  detach: S,
  element: re,
  empty: K,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Ue,
  get_slot_changes: Ge,
  group_outros: He,
  init: ze,
  insert_hydration: T,
  safe_not_equal: Be,
  set_custom_element_data: se,
  space: Ke,
  transition_in: O,
  transition_out: A,
  update_slot_base: qe
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ve,
  getContext: Je,
  onDestroy: Xe,
  setContext: Ye
} = window.__gradio__svelte__internal;
function V(e) {
  let t, n;
  const l = (
    /*#slots*/
    e[7].default
  ), o = De(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = re("svelte-slot"), o && o.c(), this.h();
    },
    l(r) {
      t = ne(r, "SVELTE-SLOT", {
        class: !0
      });
      var s = te(t);
      o && o.l(s), s.forEach(S), this.h();
    },
    h() {
      se(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      T(r, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(r, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && qe(
        o,
        l,
        r,
        /*$$scope*/
        r[6],
        n ? Ge(
          l,
          /*$$scope*/
          r[6],
          s,
          null
        ) : Ue(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      n || (O(o, r), n = !0);
    },
    o(r) {
      A(o, r), n = !1;
    },
    d(r) {
      r && S(t), o && o.d(r), e[9](null);
    }
  };
}
function Qe(e) {
  let t, n, l, o, r = (
    /*$$slots*/
    e[4].default && V(e)
  );
  return {
    c() {
      t = re("react-portal-target"), n = Ke(), r && r.c(), l = K(), this.h();
    },
    l(s) {
      t = ne(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), te(t).forEach(S), n = Ae(s), r && r.l(s), l = K(), this.h();
    },
    h() {
      se(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      T(s, t, i), e[8](t), T(s, n, i), r && r.m(s, i), T(s, l, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? r ? (r.p(s, i), i & /*$$slots*/
      16 && O(r, 1)) : (r = V(s), r.c(), O(r, 1), r.m(l.parentNode, l)) : r && (He(), A(r, 1, 1, () => {
        r = null;
      }), We());
    },
    i(s) {
      o || (O(r), o = !0);
    },
    o(s) {
      A(r), o = !1;
    },
    d(s) {
      s && (S(t), S(n), S(l)), e[8](null), r && r.d(s);
    }
  };
}
function J(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Ze(e, t, n) {
  let l, o, {
    $$slots: r = {},
    $$scope: s
  } = t;
  const i = Me(r);
  let {
    svelteInit: u
  } = t;
  const _ = k(J(t)), g = k();
  B(e, g, (a) => n(0, l = a));
  const c = k();
  B(e, c, (a) => n(1, o = a));
  const b = [], f = Je("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: E,
    subSlotIndex: m
  } = de() || {}, p = u({
    parent: f,
    props: _,
    target: g,
    slot: c,
    slotKey: w,
    slotIndex: E,
    subSlotIndex: m,
    onDestroy(a) {
      b.push(a);
    }
  });
  Ye("$$ms-gr-react-wrapper", p), Ve(() => {
    _.set(J(t));
  }), Xe(() => {
    b.forEach((a) => a());
  });
  function x(a) {
    z[a ? "unshift" : "push"](() => {
      l = a, g.set(l);
    });
  }
  function P(a) {
    z[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  return e.$$set = (a) => {
    n(17, t = H(H({}, t), q(a))), "svelteInit" in a && n(5, u = a.svelteInit), "$$scope" in a && n(6, s = a.$$scope);
  }, t = q(t), [l, o, g, c, i, u, s, r, x, P];
}
class $e extends Ne {
  constructor(t) {
    super(), ze(this, t, Ze, Qe, Be, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, L = window.ms_globals.tree;
function et(e, t = {}) {
  function n(l) {
    const o = k(), r = new $e({
      ...l,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, u = s.parent ?? L;
          return u.nodes = [...u.nodes, i], X({
            createPortal: N,
            node: L
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((_) => _.svelteInstance !== o), X({
              createPortal: N,
              node: L
            });
          }), i;
        },
        ...l.props
      }
    });
    return o.set(r), r;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
const tt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function nt(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const l = e[n];
    return t[n] = rt(n, l), t;
  }, {}) : {};
}
function rt(e, t) {
  return typeof t == "number" && !tt.includes(e) ? t + "px" : t;
}
function M(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = y.Children.toArray(e._reactElement.props.children).map((r) => {
      if (y.isValidElement(r) && r.props.__slot__) {
        const {
          portals: s,
          clonedElement: i
        } = M(r.props.el);
        return y.cloneElement(r, {
          ...r.props,
          el: i,
          children: [...y.Children.toArray(r.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(N(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: i,
      useCapture: u
    }) => {
      n.addEventListener(i, s, u);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const r = l[o];
    if (r.nodeType === 1) {
      const {
        clonedElement: s,
        portals: i
      } = M(r);
      t.push(...i), n.appendChild(s);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function st(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const v = oe(({
  slot: e,
  clone: t,
  className: n,
  style: l,
  observeAttributes: o
}, r) => {
  const s = le(), [i, u] = ie([]), {
    forceClone: _
  } = me(), g = _ ? !0 : t;
  return ce(() => {
    var E;
    if (!s.current || !e)
      return;
    let c = e;
    function b() {
      let m = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (m = c.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), st(r, m), n && m.classList.add(...n.split(" ")), l) {
        const p = nt(l);
        Object.keys(p).forEach((x) => {
          m.style[x] = p[x];
        });
      }
    }
    let f = null, w = null;
    if (g && window.MutationObserver) {
      let m = function() {
        var a, I, d;
        (a = s.current) != null && a.contains(c) && ((I = s.current) == null || I.removeChild(c));
        const {
          portals: x,
          clonedElement: P
        } = M(e);
        c = P, u(x), c.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          b();
        }, 50), (d = s.current) == null || d.appendChild(c);
      };
      m();
      const p = ke(() => {
        m(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(p), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", b(), (E = s.current) == null || E.appendChild(c);
    return () => {
      var m, p;
      c.style.display = "", (m = s.current) != null && m.contains(c) && ((p = s.current) == null || p.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, g, n, l, r, o]), y.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...i);
});
function ot(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function lt(e, t = !1) {
  try {
    if (fe(e))
      return e;
    if (t && !ot(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Y(e, t) {
  return Z(() => lt(e, t), [e, t]);
}
const it = ({
  children: e,
  ...t
}) => /* @__PURE__ */ h.jsx(h.Fragment, {
  children: e(t)
});
function ct(e) {
  return y.createElement(it, {
    children: e
  });
}
function Q(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ct((n) => /* @__PURE__ */ h.jsx(_e, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ h.jsx(v, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ h.jsx(v, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function at({
  key: e,
  slots: t,
  targets: n
}, l) {
  return t[e] ? (...o) => n ? n.map((r, s) => /* @__PURE__ */ h.jsx(y.Fragment, {
    children: Q(r, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ h.jsx(h.Fragment, {
    children: Q(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: ut,
  useItems: dt,
  ItemHandler: _t
} = he("antd-slider-marks"), ft = (e) => e.reduce((t, n) => {
  const l = n == null ? void 0 : n.props.number;
  return l !== void 0 && (t[l] = (n == null ? void 0 : n.slots.label) instanceof Element ? {
    ...n.props,
    label: /* @__PURE__ */ h.jsx(v, {
      slot: n == null ? void 0 : n.slots.label
    })
  } : (n == null ? void 0 : n.slots.children) instanceof Element ? /* @__PURE__ */ h.jsx(v, {
    slot: n == null ? void 0 : n.slots.children
  }) : {
    ...n == null ? void 0 : n.props
  }), t;
}, {}), pt = et(ut(["marks"], ({
  marks: e,
  children: t,
  onValueChange: n,
  onChange: l,
  elRef: o,
  tooltip: r,
  step: s,
  slots: i,
  setSlotParams: u,
  ..._
}) => {
  const g = (w) => {
    l == null || l(w), n(w);
  }, c = Y(r == null ? void 0 : r.getPopupContainer), b = Y(r == null ? void 0 : r.formatter), {
    items: {
      marks: f
    }
  } = dt();
  return /* @__PURE__ */ h.jsxs(h.Fragment, {
    children: [/* @__PURE__ */ h.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ h.jsx(pe, {
      ..._,
      tooltip: {
        ...r,
        getPopupContainer: c,
        formatter: i["tooltip.formatter"] ? at({
          key: "tooltip.formatter",
          setSlotParams: u,
          slots: i
        }) : b
      },
      marks: Z(() => e || ft(f), [f, e]),
      step: s === void 0 ? null : s,
      ref: o,
      onChange: g
    })]
  });
}));
export {
  pt as Slider,
  pt as default
};
