import { i as fe, a as W, r as me, g as he, w as k, c as _e } from "./Index-CRn989FQ.js";
const v = window.ms_globals.React, ie = window.ms_globals.React.forwardRef, ae = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, ue = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, pe = window.ms_globals.internalContext.useContextPropsContext, F = window.ms_globals.internalContext.ContextPropsProvider, R = window.ms_globals.createItemsContext.createItemsContext;
var ge = /\s/;
function we(t) {
  for (var e = t.length; e-- && ge.test(t.charAt(e)); )
    ;
  return e;
}
var be = /^\s+/;
function xe(t) {
  return t && t.slice(0, we(t) + 1).replace(be, "");
}
var z = NaN, Ce = /^[-+]0x[0-9a-f]+$/i, ve = /^0b[01]+$/i, Ie = /^0o[0-7]+$/i, Ee = parseInt;
function G(t) {
  if (typeof t == "number")
    return t;
  if (fe(t))
    return z;
  if (W(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = W(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = xe(t);
  var o = ve.test(t);
  return o || Ie.test(t) ? Ee(t.slice(2), o ? 2 : 8) : Ce.test(t) ? z : +t;
}
var L = function() {
  return me.Date.now();
}, ye = "Expected a function", Pe = Math.max, Se = Math.min;
function Re(t, e, o) {
  var s, r, n, l, c, a, g = 0, _ = !1, i = !1, p = !0;
  if (typeof t != "function")
    throw new TypeError(ye);
  e = G(e) || 0, W(o) && (_ = !!o.leading, i = "maxWait" in o, n = i ? Pe(G(o.maxWait) || 0, e) : n, p = "trailing" in o ? !!o.trailing : p);
  function d(h) {
    var I = s, S = r;
    return s = r = void 0, g = h, l = t.apply(S, I), l;
  }
  function w(h) {
    return g = h, c = setTimeout(m, e), _ ? d(h) : l;
  }
  function x(h) {
    var I = h - a, S = h - g, U = e - I;
    return i ? Se(U, n - S) : U;
  }
  function u(h) {
    var I = h - a, S = h - g;
    return a === void 0 || I >= e || I < 0 || i && S >= n;
  }
  function m() {
    var h = L();
    if (u(h))
      return C(h);
    c = setTimeout(m, x(h));
  }
  function C(h) {
    return c = void 0, p && s ? d(h) : (s = r = void 0, l);
  }
  function P() {
    c !== void 0 && clearTimeout(c), g = 0, s = a = r = c = void 0;
  }
  function f() {
    return c === void 0 ? l : C(L());
  }
  function E() {
    var h = L(), I = u(h);
    if (s = arguments, r = this, a = h, I) {
      if (c === void 0)
        return w(a);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), d(a);
    }
    return c === void 0 && (c = setTimeout(m, e)), l;
  }
  return E.cancel = P, E.flush = f, E;
}
var ee = {
  exports: {}
}, D = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var ke = v, Oe = Symbol.for("react.element"), Te = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, De = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function te(t, e, o) {
  var s, r = {}, n = null, l = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (l = e.ref);
  for (s in e) je.call(e, s) && !Le.hasOwnProperty(s) && (r[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) r[s] === void 0 && (r[s] = e[s]);
  return {
    $$typeof: Oe,
    type: t,
    key: n,
    ref: l,
    props: r,
    _owner: De.current
  };
}
D.Fragment = Te;
D.jsx = te;
D.jsxs = te;
ee.exports = D;
var b = ee.exports;
const {
  SvelteComponent: Ne,
  assign: q,
  binding_callbacks: V,
  check_outros: Ae,
  children: re,
  claim_element: ne,
  claim_space: We,
  component_subscribe: J,
  compute_slots: Fe,
  create_slot: Me,
  detach: y,
  element: le,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: Be,
  get_slot_changes: He,
  group_outros: Ue,
  init: ze,
  insert_hydration: O,
  safe_not_equal: Ge,
  set_custom_element_data: oe,
  space: qe,
  transition_in: T,
  transition_out: M,
  update_slot_base: Ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function K(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), r = Me(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = le("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      e = ne(n, "SVELTE-SLOT", {
        class: !0
      });
      var l = re(e);
      r && r.l(l), l.forEach(y), this.h();
    },
    h() {
      oe(e, "class", "svelte-1rt0kpf");
    },
    m(n, l) {
      O(n, e, l), r && r.m(e, null), t[9](e), o = !0;
    },
    p(n, l) {
      r && r.p && (!o || l & /*$$scope*/
      64) && Ve(
        r,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? He(
          s,
          /*$$scope*/
          n[6],
          l,
          null
        ) : Be(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (T(r, n), o = !0);
    },
    o(n) {
      M(r, n), o = !1;
    },
    d(n) {
      n && y(e), r && r.d(n), t[9](null);
    }
  };
}
function Qe(t) {
  let e, o, s, r, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = le("react-portal-target"), o = qe(), n && n.c(), s = X(), this.h();
    },
    l(l) {
      e = ne(l, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(e).forEach(y), o = We(l), n && n.l(l), s = X(), this.h();
    },
    h() {
      oe(e, "class", "svelte-1rt0kpf");
    },
    m(l, c) {
      O(l, e, c), t[8](e), O(l, o, c), n && n.m(l, c), O(l, s, c), r = !0;
    },
    p(l, [c]) {
      /*$$slots*/
      l[4].default ? n ? (n.p(l, c), c & /*$$slots*/
      16 && T(n, 1)) : (n = K(l), n.c(), T(n, 1), n.m(s.parentNode, s)) : n && (Ue(), M(n, 1, 1, () => {
        n = null;
      }), Ae());
    },
    i(l) {
      r || (T(n), r = !0);
    },
    o(l) {
      M(n), r = !1;
    },
    d(l) {
      l && (y(e), y(o), y(s)), t[8](null), n && n.d(l);
    }
  };
}
function Q(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function Ze(t, e, o) {
  let s, r, {
    $$slots: n = {},
    $$scope: l
  } = e;
  const c = Fe(n);
  let {
    svelteInit: a
  } = e;
  const g = k(Q(e)), _ = k();
  J(t, _, (f) => o(0, s = f));
  const i = k();
  J(t, i, (f) => o(1, r = f));
  const p = [], d = Xe("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: x,
    subSlotIndex: u
  } = he() || {}, m = a({
    parent: d,
    props: g,
    target: _,
    slot: i,
    slotKey: w,
    slotIndex: x,
    subSlotIndex: u,
    onDestroy(f) {
      p.push(f);
    }
  });
  Ke("$$ms-gr-react-wrapper", m), Je(() => {
    g.set(Q(e));
  }), Ye(() => {
    p.forEach((f) => f());
  });
  function C(f) {
    V[f ? "unshift" : "push"](() => {
      s = f, _.set(s);
    });
  }
  function P(f) {
    V[f ? "unshift" : "push"](() => {
      r = f, i.set(r);
    });
  }
  return t.$$set = (f) => {
    o(17, e = q(q({}, e), Y(f))), "svelteInit" in f && o(5, a = f.svelteInit), "$$scope" in f && o(6, l = f.$$scope);
  }, e = Y(e), [s, r, _, i, c, a, l, n, C, P];
}
class $e extends Ne {
  constructor(e) {
    super(), ze(this, e, Ze, Qe, Ge, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(t, e = {}) {
  function o(s) {
    const r = k(), n = new $e({
      ...s,
      props: {
        svelteInit(l) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: l.props,
            slot: l.slot,
            target: l.target,
            slotIndex: l.slotIndex,
            subSlotIndex: l.subSlotIndex,
            ignore: e.ignore,
            slotKey: l.slotKey,
            nodes: []
          }, a = l.parent ?? N;
          return a.nodes = [...a.nodes, c], Z({
            createPortal: A,
            node: N
          }), l.onDestroy(() => {
            a.nodes = a.nodes.filter((g) => g.svelteInstance !== r), Z({
              createPortal: A,
              node: N
            });
          }), c;
        },
        ...s.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(o);
    });
  });
}
const tt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rt(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = nt(o, s), e;
  }, {}) : {};
}
function nt(t, e) {
  return typeof e == "number" && !tt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const r = v.Children.toArray(t._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: l,
          clonedElement: c
        } = B(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...v.Children.toArray(n.props.children), ...l]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(A(v.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: l,
      type: c,
      useCapture: a
    }) => {
      o.addEventListener(c, l, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let r = 0; r < s.length; r++) {
    const n = s[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: l,
        portals: c
      } = B(n);
      e.push(...c), o.appendChild(l);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function lt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const j = ie(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: r
}, n) => {
  const l = ae(), [c, a] = de([]), {
    forceClone: g
  } = pe(), _ = g ? !0 : e;
  return ue(() => {
    var x;
    if (!l.current || !t)
      return;
    let i = t;
    function p() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), lt(n, u), o && u.classList.add(...o.split(" ")), s) {
        const m = rt(s);
        Object.keys(m).forEach((C) => {
          u.style[C] = m[C];
        });
      }
    }
    let d = null, w = null;
    if (_ && window.MutationObserver) {
      let u = function() {
        var f, E, h;
        (f = l.current) != null && f.contains(i) && ((E = l.current) == null || E.removeChild(i));
        const {
          portals: C,
          clonedElement: P
        } = B(t);
        i = P, a(C), i.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          p();
        }, 50), (h = l.current) == null || h.appendChild(i);
      };
      u();
      const m = Re(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (x = l.current) == null || x.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = l.current) != null && u.contains(i) && ((m = l.current) == null || m.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, _, o, s, n, r]), v.createElement("react-child", {
    ref: l,
    style: {
      display: "contents"
    }
  }, ...c);
}), ot = ({
  children: t,
  ...e
}) => /* @__PURE__ */ b.jsx(b.Fragment, {
  children: t(e)
});
function se(t) {
  return v.createElement(ot, {
    children: t
  });
}
function ce(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((r, n) => {
      var g;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const l = {
        ...r.props,
        key: ((g = r.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = l;
      Object.keys(r.slots).forEach((_) => {
        if (!r.slots[_] || !(r.slots[_] instanceof Element) && !r.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((m, C) => {
          c[m] || (c[m] = {}), C !== i.length - 1 && (c = l[m]);
        });
        const p = r.slots[_];
        let d, w, x = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        p instanceof Element ? d = p : (d = p.el, w = p.callback, x = p.clone ?? x, u = p.forceClone ?? u), u = u ?? !!w, c[i[i.length - 1]] = d ? w ? (...m) => (w(i[i.length - 1], m), /* @__PURE__ */ b.jsx(F, {
          ...r.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(j, {
            slot: d,
            clone: x
          })
        })) : se((m) => /* @__PURE__ */ b.jsx(F, {
          ...r.ctx,
          forceClone: u,
          children: /* @__PURE__ */ b.jsx(j, {
            slot: d,
            clone: x,
            ...m
          })
        })) : c[i[i.length - 1]], c = l;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return r[a] ? l[a] = ce(r[a], e, `${n}`) : e != null && e.children && (l[a] = void 0, Reflect.deleteProperty(l, a)), l;
    });
}
function H(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? se((o) => /* @__PURE__ */ b.jsx(F, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ b.jsx(j, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ b.jsx(j, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function $({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...r) => o ? o.map((n, l) => /* @__PURE__ */ b.jsx(v.Fragment, {
    children: H(n, {
      clone: !0,
      params: r,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, l)) : /* @__PURE__ */ b.jsx(b.Fragment, {
    children: H(e[t], {
      clone: !0,
      params: r,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: st,
  withItemsContextProvider: ct,
  ItemHandler: dt
} = R("antd-menu-items"), {
  useItems: ut,
  withItemsContextProvider: ft,
  ItemHandler: it
} = R("antd-table-columns");
R("antd-table-row-selection-selections");
R("antd-table-row-selection");
R("antd-table-expandable");
const mt = et(ct(["filterDropdownProps.menu.items"], ({
  setSlotParams: t,
  itemSlots: e,
  ...o
}) => {
  const {
    items: {
      "filterDropdownProps.menu.items": s
    }
  } = st();
  return /* @__PURE__ */ b.jsx(it, {
    ...o,
    itemProps: (r) => {
      var c, a, g, _, i, p, d, w;
      const n = {
        ...((c = r.filterDropdownProps) == null ? void 0 : c.menu) || {},
        items: (g = (a = r.filterDropdownProps) == null ? void 0 : a.menu) != null && g.items || s.length > 0 ? ce(s, {
          clone: !0
        }) : void 0,
        expandIcon: $({
          setSlotParams: t,
          slots: e,
          key: "filterDropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((i = (_ = r.filterDropdownProps) == null ? void 0 : _.menu) == null ? void 0 : i.expandIcon),
        overflowedIndicator: H(e["filterDropdownProps.menu.overflowedIndicator"]) || ((d = (p = r.filterDropdownProps) == null ? void 0 : p.menu) == null ? void 0 : d.overflowedIndicator)
      }, l = {
        ...r.filterDropdownProps || {},
        dropdownRender: e["filterDropdownProps.dropdownRender"] ? $({
          setSlotParams: t,
          slots: e,
          key: "filterDropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : _e((w = r.filterDropdownProps) == null ? void 0 : w.dropdownRender),
        menu: Object.values(n).filter(Boolean).length > 0 ? n : void 0
      };
      return {
        ...r,
        filterDropdownProps: Object.values(l).filter(Boolean).length > 0 ? l : void 0
      };
    }
  });
}));
export {
  mt as TableColumn,
  mt as default
};
