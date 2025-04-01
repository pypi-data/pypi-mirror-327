import { i as fe, a as M, r as me, g as _e, w as k, b as pe } from "./Index-CXgFE9ED.js";
const x = window.ms_globals.React, T = window.ms_globals.React.useMemo, ce = window.ms_globals.React.forwardRef, ae = window.ms_globals.React.useRef, ue = window.ms_globals.React.useState, de = window.ms_globals.React.useEffect, D = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.internalContext.useContextPropsContext, ge = window.ms_globals.internalContext.ContextPropsProvider, ye = window.ms_globals.antd.Calendar, G = window.ms_globals.dayjs;
var we = /\s/;
function be(e) {
  for (var t = e.length; t-- && we.test(e.charAt(t)); )
    ;
  return t;
}
var ve = /^\s+/;
function xe(e) {
  return e && e.slice(0, be(e) + 1).replace(ve, "");
}
var H = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, Ce = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Ie = parseInt;
function V(e) {
  if (typeof e == "number")
    return e;
  if (fe(e))
    return H;
  if (M(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = M(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = xe(e);
  var l = Ce.test(e);
  return l || Re.test(e) ? Ie(e.slice(2), l ? 2 : 8) : Ee.test(e) ? H : +e;
}
var L = function() {
  return me.Date.now();
}, Se = "Expected a function", Oe = Math.max, Te = Math.min;
function ke(e, t, l) {
  var s, o, n, r, i, d, p = 0, g = !1, a = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Se);
  t = V(t) || 0, M(l) && (g = !!l.leading, a = "maxWait" in l, n = a ? Oe(V(l.maxWait) || 0, t) : n, w = "trailing" in l ? !!l.trailing : w);
  function f(c) {
    var h = s, S = o;
    return s = o = void 0, p = c, r = e.apply(S, h), r;
  }
  function v(c) {
    return p = c, i = setTimeout(_, t), g ? f(c) : r;
  }
  function E(c) {
    var h = c - d, S = c - p, B = t - h;
    return a ? Te(B, n - S) : B;
  }
  function m(c) {
    var h = c - d, S = c - p;
    return d === void 0 || h >= t || h < 0 || a && S >= n;
  }
  function _() {
    var c = L();
    if (m(c))
      return b(c);
    i = setTimeout(_, E(c));
  }
  function b(c) {
    return i = void 0, w && s ? f(c) : (s = o = void 0, r);
  }
  function R() {
    i !== void 0 && clearTimeout(i), p = 0, s = d = o = i = void 0;
  }
  function u() {
    return i === void 0 ? r : b(L());
  }
  function C() {
    var c = L(), h = m(c);
    if (s = arguments, o = this, d = c, h) {
      if (i === void 0)
        return v(d);
      if (a)
        return clearTimeout(i), i = setTimeout(_, t), f(d);
    }
    return i === void 0 && (i = setTimeout(_, t)), r;
  }
  return C.cancel = R, C.flush = u, C;
}
var ne = {
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
var Pe = x, je = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Le = Object.prototype.hasOwnProperty, Ae = Pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(e, t, l) {
  var s, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (s in t) Le.call(t, s) && !Ne.hasOwnProperty(s) && (o[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) o[s] === void 0 && (o[s] = t[s]);
  return {
    $$typeof: je,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: Ae.current
  };
}
F.Fragment = Fe;
F.jsx = re;
F.jsxs = re;
ne.exports = F;
var y = ne.exports;
const {
  SvelteComponent: We,
  assign: K,
  binding_callbacks: q,
  check_outros: De,
  children: le,
  claim_element: oe,
  claim_space: Me,
  component_subscribe: J,
  compute_slots: Ue,
  create_slot: ze,
  detach: I,
  element: se,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: Be,
  get_slot_changes: Ge,
  group_outros: He,
  init: Ve,
  insert_hydration: P,
  safe_not_equal: Ke,
  set_custom_element_data: ie,
  space: qe,
  transition_in: j,
  transition_out: U,
  update_slot_base: Je
} = window.__gradio__svelte__internal, {
  beforeUpdate: Xe,
  getContext: Ye,
  onDestroy: Qe,
  setContext: Ze
} = window.__gradio__svelte__internal;
function Q(e) {
  let t, l;
  const s = (
    /*#slots*/
    e[7].default
  ), o = ze(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = se("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = oe(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = le(t);
      o && o.l(r), r.forEach(I), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, t, r), o && o.m(t, null), e[9](t), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Je(
        o,
        s,
        n,
        /*$$scope*/
        n[6],
        l ? Ge(
          s,
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
      l || (j(o, n), l = !0);
    },
    o(n) {
      U(o, n), l = !1;
    },
    d(n) {
      n && I(t), o && o.d(n), e[9](null);
    }
  };
}
function $e(e) {
  let t, l, s, o, n = (
    /*$$slots*/
    e[4].default && Q(e)
  );
  return {
    c() {
      t = se("react-portal-target"), l = qe(), n && n.c(), s = X(), this.h();
    },
    l(r) {
      t = oe(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), le(t).forEach(I), l = Me(r), n && n.l(r), s = X(), this.h();
    },
    h() {
      ie(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      P(r, t, i), e[8](t), P(r, l, i), n && n.m(r, i), P(r, s, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && j(n, 1)) : (n = Q(r), n.c(), j(n, 1), n.m(s.parentNode, s)) : n && (He(), U(n, 1, 1, () => {
        n = null;
      }), De());
    },
    i(r) {
      o || (j(n), o = !0);
    },
    o(r) {
      U(n), o = !1;
    },
    d(r) {
      r && (I(t), I(l), I(s)), e[8](null), n && n.d(r);
    }
  };
}
function Z(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function et(e, t, l) {
  let s, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const i = Ue(n);
  let {
    svelteInit: d
  } = t;
  const p = k(Z(t)), g = k();
  J(e, g, (u) => l(0, s = u));
  const a = k();
  J(e, a, (u) => l(1, o = u));
  const w = [], f = Ye("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: E,
    subSlotIndex: m
  } = _e() || {}, _ = d({
    parent: f,
    props: p,
    target: g,
    slot: a,
    slotKey: v,
    slotIndex: E,
    subSlotIndex: m,
    onDestroy(u) {
      w.push(u);
    }
  });
  Ze("$$ms-gr-react-wrapper", _), Xe(() => {
    p.set(Z(t));
  }), Qe(() => {
    w.forEach((u) => u());
  });
  function b(u) {
    q[u ? "unshift" : "push"](() => {
      s = u, g.set(s);
    });
  }
  function R(u) {
    q[u ? "unshift" : "push"](() => {
      o = u, a.set(o);
    });
  }
  return e.$$set = (u) => {
    l(17, t = K(K({}, t), Y(u))), "svelteInit" in u && l(5, d = u.svelteInit), "$$scope" in u && l(6, r = u.$$scope);
  }, t = Y(t), [s, o, g, a, i, d, r, n, b, R];
}
class tt extends We {
  constructor(t) {
    super(), Ve(this, t, et, $e, Ke, {
      svelteInit: 5
    });
  }
}
const $ = window.ms_globals.rerender, A = window.ms_globals.tree;
function nt(e, t = {}) {
  function l(s) {
    const o = k(), n = new tt({
      ...s,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: t.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, d = r.parent ?? A;
          return d.nodes = [...d.nodes, i], $({
            createPortal: D,
            node: A
          }), r.onDestroy(() => {
            d.nodes = d.nodes.filter((p) => p.svelteInstance !== o), $({
              createPortal: D,
              node: A
            });
          }), i;
        },
        ...s.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(l);
    });
  });
}
function rt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function lt(e, t = !1) {
  try {
    if (pe(e))
      return e;
    if (t && !rt(e))
      return;
    if (typeof e == "string") {
      let l = e.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function O(e, t) {
  return T(() => lt(e, t), [e, t]);
}
const ot = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function st(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const s = e[l];
    return t[l] = it(l, s), t;
  }, {}) : {};
}
function it(e, t) {
  return typeof t == "number" && !ot.includes(e) ? t + "px" : t;
}
function z(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement) {
    const o = x.Children.toArray(e._reactElement.props.children).map((n) => {
      if (x.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = z(n.props.el);
        return x.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...x.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(D(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), l)), {
      clonedElement: l,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: r,
      type: i,
      useCapture: d
    }) => {
      l.addEventListener(i, r, d);
    });
  });
  const s = Array.from(e.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = z(n);
      t.push(...i), l.appendChild(r);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function ct(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const ee = ce(({
  slot: e,
  clone: t,
  className: l,
  style: s,
  observeAttributes: o
}, n) => {
  const r = ae(), [i, d] = ue([]), {
    forceClone: p
  } = he(), g = p ? !0 : t;
  return de(() => {
    var E;
    if (!r.current || !e)
      return;
    let a = e;
    function w() {
      let m = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (m = a.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), ct(n, m), l && m.classList.add(...l.split(" ")), s) {
        const _ = st(s);
        Object.keys(_).forEach((b) => {
          m.style[b] = _[b];
        });
      }
    }
    let f = null, v = null;
    if (g && window.MutationObserver) {
      let m = function() {
        var u, C, c;
        (u = r.current) != null && u.contains(a) && ((C = r.current) == null || C.removeChild(a));
        const {
          portals: b,
          clonedElement: R
        } = z(e);
        a = R, d(b), a.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          w();
        }, 50), (c = r.current) == null || c.appendChild(a);
      };
      m();
      const _ = ke(() => {
        m(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(_), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", w(), (E = r.current) == null || E.appendChild(a);
    return () => {
      var m, _;
      a.style.display = "", (m = r.current) != null && m.contains(a) && ((_ = r.current) == null || _.removeChild(a)), f == null || f.disconnect();
    };
  }, [e, g, l, s, n, o]), x.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
}), at = ({
  children: e,
  ...t
}) => /* @__PURE__ */ y.jsx(y.Fragment, {
  children: e(t)
});
function ut(e) {
  return x.createElement(at, {
    children: e
  });
}
function te(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ut((l) => /* @__PURE__ */ y.jsx(ge, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ y.jsx(ee, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...l
    })
  })) : /* @__PURE__ */ y.jsx(ee, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function N({
  key: e,
  slots: t,
  targets: l
}, s) {
  return t[e] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ y.jsx(x.Fragment, {
    children: te(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ y.jsx(y.Fragment, {
    children: te(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
function W(e) {
  return G(typeof e == "number" ? e * 1e3 : e);
}
const ft = nt(({
  disabledDate: e,
  value: t,
  defaultValue: l,
  validRange: s,
  onChange: o,
  onPanelChange: n,
  onSelect: r,
  onValueChange: i,
  setSlotParams: d,
  cellRender: p,
  fullCellRender: g,
  headerRender: a,
  children: w,
  slots: f,
  ...v
}) => {
  const E = O(e), m = O(p), _ = O(g), b = O(a), R = T(() => t ? W(t) : void 0, [t]), u = T(() => l ? W(l) : void 0, [l]), C = T(() => Array.isArray(s) ? s.map((c) => W(c)) : void 0, [s]);
  return /* @__PURE__ */ y.jsxs(y.Fragment, {
    children: [/* @__PURE__ */ y.jsx("div", {
      style: {
        display: "none"
      },
      children: w
    }), /* @__PURE__ */ y.jsx(ye, {
      ...v,
      value: R,
      defaultValue: u,
      validRange: C,
      disabledDate: E,
      cellRender: f.cellRender ? N({
        slots: f,
        setSlotParams: d,
        key: "cellRender"
      }) : m,
      fullCellRender: f.fullCellRender ? N({
        slots: f,
        setSlotParams: d,
        key: "fullCellRender"
      }) : _,
      headerRender: f.headerRender ? N({
        slots: f,
        setSlotParams: d,
        key: "headerRender"
      }) : b,
      onChange: (c, ...h) => {
        i(c.valueOf() / 1e3), o == null || o(c.valueOf() / 1e3, ...h);
      },
      onPanelChange: (c, ...h) => {
        n == null || n(c.valueOf() / 1e3, ...h);
      },
      onSelect: (c, ...h) => {
        r == null || r(c.valueOf() / 1e3, ...h);
      }
    })]
  });
});
export {
  ft as Calendar,
  ft as default
};
