import { i as ae, a as W, r as ue, g as de, w as P } from "./Index-BZDX3tqk.js";
const C = window.ms_globals.React, se = window.ms_globals.React.forwardRef, le = window.ms_globals.React.useRef, ie = window.ms_globals.React.useState, ce = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, fe = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, k = window.ms_globals.createItemsContext.createItemsContext;
var me = /\s/;
function pe(e) {
  for (var t = e.length; t-- && me.test(e.charAt(t)); )
    ;
  return t;
}
var he = /^\s+/;
function _e(e) {
  return e && e.slice(0, pe(e) + 1).replace(he, "");
}
var U = NaN, ge = /^[-+]0x[0-9a-f]+$/i, be = /^0b[01]+$/i, we = /^0o[0-7]+$/i, xe = parseInt;
function B(e) {
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
  e = _e(e);
  var s = be.test(e);
  return s || we.test(e) ? xe(e.slice(2), s ? 2 : 8) : ge.test(e) ? U : +e;
}
var j = function() {
  return ue.Date.now();
}, Ee = "Expected a function", Ce = Math.max, Ie = Math.min;
function ye(e, t, s) {
  var l, o, n, r, i, u, g = 0, h = !1, c = !1, _ = !0;
  if (typeof e != "function")
    throw new TypeError(Ee);
  t = B(t) || 0, W(s) && (h = !!s.leading, c = "maxWait" in s, n = c ? Ce(B(s.maxWait) || 0, t) : n, _ = "trailing" in s ? !!s.trailing : _);
  function f(p) {
    var E = l, R = o;
    return l = o = void 0, g = p, r = e.apply(R, E), r;
  }
  function b(p) {
    return g = p, i = setTimeout(m, t), h ? f(p) : r;
  }
  function w(p) {
    var E = p - u, R = p - g, F = t - E;
    return c ? Ie(F, n - R) : F;
  }
  function a(p) {
    var E = p - u, R = p - g;
    return u === void 0 || E >= t || E < 0 || c && R >= n;
  }
  function m() {
    var p = j();
    if (a(p))
      return x(p);
    i = setTimeout(m, w(p));
  }
  function x(p) {
    return i = void 0, _ && l ? f(p) : (l = o = void 0, r);
  }
  function S() {
    i !== void 0 && clearTimeout(i), g = 0, l = u = o = i = void 0;
  }
  function d() {
    return i === void 0 ? r : x(j());
  }
  function y() {
    var p = j(), E = a(p);
    if (l = arguments, o = this, u = p, E) {
      if (i === void 0)
        return b(u);
      if (c)
        return clearTimeout(i), i = setTimeout(m, t), f(u);
    }
    return i === void 0 && (i = setTimeout(m, t)), r;
  }
  return y.cancel = S, y.flush = d, y;
}
var Z = {
  exports: {}
}, L = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ve = C, Se = Symbol.for("react.element"), Re = Symbol.for("react.fragment"), Pe = Object.prototype.hasOwnProperty, Te = ve.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(e, t, s) {
  var l, o = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (l in t) Pe.call(t, l) && !Oe.hasOwnProperty(l) && (o[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) o[l] === void 0 && (o[l] = t[l]);
  return {
    $$typeof: Se,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: Te.current
  };
}
L.Fragment = Re;
L.jsx = $;
L.jsxs = $;
Z.exports = L;
var I = Z.exports;
const {
  SvelteComponent: ke,
  assign: z,
  binding_callbacks: G,
  check_outros: Le,
  children: ee,
  claim_element: te,
  claim_space: je,
  component_subscribe: q,
  compute_slots: Ne,
  create_slot: Ae,
  detach: v,
  element: ne,
  empty: V,
  exclude_internal_props: J,
  get_all_dirty_from_scope: We,
  get_slot_changes: He,
  group_outros: De,
  init: Fe,
  insert_hydration: T,
  safe_not_equal: Me,
  set_custom_element_data: re,
  space: Ue,
  transition_in: O,
  transition_out: H,
  update_slot_base: Be
} = window.__gradio__svelte__internal, {
  beforeUpdate: ze,
  getContext: Ge,
  onDestroy: qe,
  setContext: Ve
} = window.__gradio__svelte__internal;
function X(e) {
  let t, s;
  const l = (
    /*#slots*/
    e[7].default
  ), o = Ae(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ne("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = te(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ee(t);
      o && o.l(r), r.forEach(v), this.h();
    },
    h() {
      re(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      T(n, t, r), o && o.m(t, null), e[9](t), s = !0;
    },
    p(n, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && Be(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? He(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : We(
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
      H(o, n), s = !1;
    },
    d(n) {
      n && v(t), o && o.d(n), e[9](null);
    }
  };
}
function Je(e) {
  let t, s, l, o, n = (
    /*$$slots*/
    e[4].default && X(e)
  );
  return {
    c() {
      t = ne("react-portal-target"), s = Ue(), n && n.c(), l = V(), this.h();
    },
    l(r) {
      t = te(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(t).forEach(v), s = je(r), n && n.l(r), l = V(), this.h();
    },
    h() {
      re(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      T(r, t, i), e[8](t), T(r, s, i), n && n.m(r, i), T(r, l, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = X(r), n.c(), O(n, 1), n.m(l.parentNode, l)) : n && (De(), H(n, 1, 1, () => {
        n = null;
      }), Le());
    },
    i(r) {
      o || (O(n), o = !0);
    },
    o(r) {
      H(n), o = !1;
    },
    d(r) {
      r && (v(t), v(s), v(l)), e[8](null), n && n.d(r);
    }
  };
}
function Y(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function Xe(e, t, s) {
  let l, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const i = Ne(n);
  let {
    svelteInit: u
  } = t;
  const g = P(Y(t)), h = P();
  q(e, h, (d) => s(0, l = d));
  const c = P();
  q(e, c, (d) => s(1, o = d));
  const _ = [], f = Ge("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: w,
    subSlotIndex: a
  } = de() || {}, m = u({
    parent: f,
    props: g,
    target: h,
    slot: c,
    slotKey: b,
    slotIndex: w,
    subSlotIndex: a,
    onDestroy(d) {
      _.push(d);
    }
  });
  Ve("$$ms-gr-react-wrapper", m), ze(() => {
    g.set(Y(t));
  }), qe(() => {
    _.forEach((d) => d());
  });
  function x(d) {
    G[d ? "unshift" : "push"](() => {
      l = d, h.set(l);
    });
  }
  function S(d) {
    G[d ? "unshift" : "push"](() => {
      o = d, c.set(o);
    });
  }
  return e.$$set = (d) => {
    s(17, t = z(z({}, t), J(d))), "svelteInit" in d && s(5, u = d.svelteInit), "$$scope" in d && s(6, r = d.$$scope);
  }, t = J(t), [l, o, h, c, i, u, r, n, x, S];
}
class Ye extends ke {
  constructor(t) {
    super(), Fe(this, t, Xe, Je, Me, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, N = window.ms_globals.tree;
function Ke(e, t = {}) {
  function s(l) {
    const o = P(), n = new Ye({
      ...l,
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
          }, u = r.parent ?? N;
          return u.nodes = [...u.nodes, i], K({
            createPortal: A,
            node: N
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((g) => g.svelteInstance !== o), K({
              createPortal: A,
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
const Qe = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Ze(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const l = e[s];
    return t[s] = $e(s, l), t;
  }, {}) : {};
}
function $e(e, t) {
  return typeof t == "number" && !Qe.includes(e) ? t + "px" : t;
}
function D(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement) {
    const o = C.Children.toArray(e._reactElement.props.children).map((n) => {
      if (C.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = D(n.props.el);
        return C.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...C.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(A(C.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), s)), {
      clonedElement: s,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: r,
      type: i,
      useCapture: u
    }) => {
      s.addEventListener(i, r, u);
    });
  });
  const l = Array.from(e.childNodes);
  for (let o = 0; o < l.length; o++) {
    const n = l[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = D(n);
      t.push(...i), s.appendChild(r);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function et(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const Q = se(({
  slot: e,
  clone: t,
  className: s,
  style: l,
  observeAttributes: o
}, n) => {
  const r = le(), [i, u] = ie([]), {
    forceClone: g
  } = fe(), h = g ? !0 : t;
  return ce(() => {
    var w;
    if (!r.current || !e)
      return;
    let c = e;
    function _() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), et(n, a), s && a.classList.add(...s.split(" ")), l) {
        const m = Ze(l);
        Object.keys(m).forEach((x) => {
          a.style[x] = m[x];
        });
      }
    }
    let f = null, b = null;
    if (h && window.MutationObserver) {
      let a = function() {
        var d, y, p;
        (d = r.current) != null && d.contains(c) && ((y = r.current) == null || y.removeChild(c));
        const {
          portals: x,
          clonedElement: S
        } = D(e);
        c = S, u(x), c.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          _();
        }, 50), (p = r.current) == null || p.appendChild(c);
      };
      a();
      const m = ye(() => {
        a(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", _(), (w = r.current) == null || w.appendChild(c);
    return () => {
      var a, m;
      c.style.display = "", (a = r.current) != null && a.contains(c) && ((m = r.current) == null || m.removeChild(c)), f == null || f.disconnect();
    };
  }, [e, h, s, l, n, o]), C.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
}), tt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ I.jsx(I.Fragment, {
  children: e(t)
});
function nt(e) {
  return C.createElement(tt, {
    children: e
  });
}
function oe(e, t, s) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, n) => {
      var g;
      if (typeof o != "object")
        return o;
      const r = {
        ...o.props,
        key: ((g = o.props) == null ? void 0 : g.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(o.slots).forEach((h) => {
        if (!o.slots[h] || !(o.slots[h] instanceof Element) && !o.slots[h].el)
          return;
        const c = h.split(".");
        c.forEach((m, x) => {
          i[m] || (i[m] = {}), x !== c.length - 1 && (i = r[m]);
        });
        const _ = o.slots[h];
        let f, b, w = !1, a = t == null ? void 0 : t.forceClone;
        _ instanceof Element ? f = _ : (f = _.el, b = _.callback, w = _.clone ?? w, a = _.forceClone ?? a), a = a ?? !!b, i[c[c.length - 1]] = f ? b ? (...m) => (b(c[c.length - 1], m), /* @__PURE__ */ I.jsx(M, {
          ...o.ctx,
          params: m,
          forceClone: a,
          children: /* @__PURE__ */ I.jsx(Q, {
            slot: f,
            clone: w
          })
        })) : nt((m) => /* @__PURE__ */ I.jsx(M, {
          ...o.ctx,
          forceClone: a,
          children: /* @__PURE__ */ I.jsx(Q, {
            slot: f,
            clone: w,
            ...m
          })
        })) : i[c[c.length - 1]], i = r;
      });
      const u = "children";
      return o[u] && (r[u] = oe(o[u], t, `${n}`)), r;
    });
}
k("antd-table-columns");
const {
  useItems: rt,
  withItemsContextProvider: ot,
  ItemHandler: it
} = k("antd-table-row-selection-selections"), {
  useItems: ct,
  withItemsContextProvider: at,
  ItemHandler: st
} = k("antd-table-row-selection");
k("antd-table-expandable");
const ut = Ke(ot(["selections"], (e) => {
  const {
    items: {
      selections: t
    }
  } = rt();
  return /* @__PURE__ */ I.jsx(st, {
    ...e,
    itemProps: (s) => ({
      ...s,
      selections: t.length > 0 ? oe(t) : s.selections
    })
  });
}));
export {
  ut as TableRowSelection,
  ut as default
};
