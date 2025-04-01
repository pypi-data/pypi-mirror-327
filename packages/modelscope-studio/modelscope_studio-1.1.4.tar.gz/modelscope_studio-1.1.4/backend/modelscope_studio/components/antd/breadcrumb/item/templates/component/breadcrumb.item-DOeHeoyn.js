import { i as fe, a as B, r as me, g as he, w as P, b as _e } from "./Index-B_EXJTyL.js";
const I = window.ms_globals.React, ie = window.ms_globals.React.forwardRef, ae = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, ue = window.ms_globals.React.useEffect, A = window.ms_globals.ReactDOM.createPortal, pe = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, ee = window.ms_globals.createItemsContext.createItemsContext;
var ge = /\s/;
function we(t) {
  for (var e = t.length; e-- && ge.test(t.charAt(e)); )
    ;
  return e;
}
var xe = /^\s+/;
function be(t) {
  return t && t.slice(0, we(t) + 1).replace(xe, "");
}
var G = NaN, ve = /^[-+]0x[0-9a-f]+$/i, Ie = /^0b[01]+$/i, Ce = /^0o[0-7]+$/i, ye = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (fe(t))
    return G;
  if (B(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = B(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = be(t);
  var o = Ie.test(t);
  return o || Ce.test(t) ? ye(t.slice(2), o ? 2 : 8) : ve.test(t) ? G : +t;
}
var N = function() {
  return me.Date.now();
}, Ee = "Expected a function", Re = Math.max, Se = Math.min;
function Pe(t, e, o) {
  var s, l, n, r, c, a, g = 0, _ = !1, i = !1, p = !0;
  if (typeof t != "function")
    throw new TypeError(Ee);
  e = q(e) || 0, B(o) && (_ = !!o.leading, i = "maxWait" in o, n = i ? Re(q(o.maxWait) || 0, e) : n, p = "trailing" in o ? !!o.trailing : p);
  function u(h) {
    var y = s, S = l;
    return s = l = void 0, g = h, r = t.apply(S, y), r;
  }
  function w(h) {
    return g = h, c = setTimeout(f, e), _ ? u(h) : r;
  }
  function x(h) {
    var y = h - a, S = h - g, z = e - y;
    return i ? Se(z, n - S) : z;
  }
  function d(h) {
    var y = h - a, S = h - g;
    return a === void 0 || y >= e || y < 0 || i && S >= n;
  }
  function f() {
    var h = N();
    if (d(h))
      return b(h);
    c = setTimeout(f, x(h));
  }
  function b(h) {
    return c = void 0, p && s ? u(h) : (s = l = void 0, r);
  }
  function C() {
    c !== void 0 && clearTimeout(c), g = 0, s = a = l = c = void 0;
  }
  function m() {
    return c === void 0 ? r : b(N());
  }
  function E() {
    var h = N(), y = d(h);
    if (s = arguments, l = this, a = h, y) {
      if (c === void 0)
        return w(a);
      if (i)
        return clearTimeout(c), c = setTimeout(f, e), u(a);
    }
    return c === void 0 && (c = setTimeout(f, e)), r;
  }
  return E.cancel = C, E.flush = m, E;
}
var te = {
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
var ke = I, Oe = Symbol.for("react.element"), Te = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Le = ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ne(t, e, o) {
  var s, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) je.call(e, s) && !Ne.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: Oe,
    type: t,
    key: n,
    ref: r,
    props: l,
    _owner: Le.current
  };
}
L.Fragment = Te;
L.jsx = ne;
L.jsxs = ne;
te.exports = L;
var v = te.exports;
const {
  SvelteComponent: We,
  assign: V,
  binding_callbacks: J,
  check_outros: Fe,
  children: re,
  claim_element: le,
  claim_space: Ae,
  component_subscribe: X,
  compute_slots: Be,
  create_slot: Me,
  detach: R,
  element: oe,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: De,
  get_slot_changes: He,
  group_outros: Ue,
  init: ze,
  insert_hydration: k,
  safe_not_equal: Ge,
  set_custom_element_data: se,
  space: qe,
  transition_in: O,
  transition_out: D,
  update_slot_base: Ve
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), l = Me(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = oe("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = re(e);
      l && l.l(r), r.forEach(R), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      k(n, e, r), l && l.m(e, null), t[9](e), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Ve(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? He(
          s,
          /*$$scope*/
          n[6],
          r,
          null
        ) : De(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (O(l, n), o = !0);
    },
    o(n) {
      D(l, n), o = !1;
    },
    d(n) {
      n && R(e), l && l.d(n), t[9](null);
    }
  };
}
function Qe(t) {
  let e, o, s, l, n = (
    /*$$slots*/
    t[4].default && Q(t)
  );
  return {
    c() {
      e = oe("react-portal-target"), o = qe(), n && n.c(), s = Y(), this.h();
    },
    l(r) {
      e = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(e).forEach(R), o = Ae(r), n && n.l(r), s = Y(), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      k(r, e, c), t[8](e), k(r, o, c), n && n.m(r, c), k(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && O(n, 1)) : (n = Q(r), n.c(), O(n, 1), n.m(s.parentNode, s)) : n && (Ue(), D(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(r) {
      l || (O(n), l = !0);
    },
    o(r) {
      D(n), l = !1;
    },
    d(r) {
      r && (R(e), R(o), R(s)), t[8](null), n && n.d(r);
    }
  };
}
function Z(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function Ze(t, e, o) {
  let s, l, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Be(n);
  let {
    svelteInit: a
  } = e;
  const g = P(Z(e)), _ = P();
  X(t, _, (m) => o(0, s = m));
  const i = P();
  X(t, i, (m) => o(1, l = m));
  const p = [], u = Xe("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: x,
    subSlotIndex: d
  } = he() || {}, f = a({
    parent: u,
    props: g,
    target: _,
    slot: i,
    slotKey: w,
    slotIndex: x,
    subSlotIndex: d,
    onDestroy(m) {
      p.push(m);
    }
  });
  Ke("$$ms-gr-react-wrapper", f), Je(() => {
    g.set(Z(e));
  }), Ye(() => {
    p.forEach((m) => m());
  });
  function b(m) {
    J[m ? "unshift" : "push"](() => {
      s = m, _.set(s);
    });
  }
  function C(m) {
    J[m ? "unshift" : "push"](() => {
      l = m, i.set(l);
    });
  }
  return t.$$set = (m) => {
    o(17, e = V(V({}, e), K(m))), "svelteInit" in m && o(5, a = m.svelteInit), "$$scope" in m && o(6, r = m.$$scope);
  }, e = K(e), [s, l, _, i, c, a, r, n, b, C];
}
class $e extends We {
  constructor(e) {
    super(), ze(this, e, Ze, Qe, Ge, {
      svelteInit: 5
    });
  }
}
const $ = window.ms_globals.rerender, W = window.ms_globals.tree;
function et(t, e = {}) {
  function o(s) {
    const l = P(), n = new $e({
      ...s,
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
          }, a = r.parent ?? W;
          return a.nodes = [...a.nodes, c], $({
            createPortal: A,
            node: W
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((g) => g.svelteInstance !== l), $({
              createPortal: A,
              node: W
            });
          }), c;
        },
        ...s.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(o);
    });
  });
}
function tt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function nt(t, e = !1) {
  try {
    if (_e(t))
      return t;
    if (e && !tt(t))
      return;
    if (typeof t == "string") {
      let o = t.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
const rt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function lt(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = ot(o, s), e;
  }, {}) : {};
}
function ot(t, e) {
  return typeof e == "number" && !rt.includes(t) ? e + "px" : e;
}
function H(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const l = I.Children.toArray(t._reactElement.props.children).map((n) => {
      if (I.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = H(n.props.el);
        return I.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...I.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(A(I.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: r,
      type: c,
      useCapture: a
    }) => {
      o.addEventListener(c, r, a);
    });
  });
  const s = Array.from(t.childNodes);
  for (let l = 0; l < s.length; l++) {
    const n = s[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = H(n);
      e.push(...c), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function st(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const T = ie(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: l
}, n) => {
  const r = ae(), [c, a] = de([]), {
    forceClone: g
  } = pe(), _ = g ? !0 : e;
  return ue(() => {
    var x;
    if (!r.current || !t)
      return;
    let i = t;
    function p() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), st(n, d), o && d.classList.add(...o.split(" ")), s) {
        const f = lt(s);
        Object.keys(f).forEach((b) => {
          d.style[b] = f[b];
        });
      }
    }
    let u = null, w = null;
    if (_ && window.MutationObserver) {
      let d = function() {
        var m, E, h;
        (m = r.current) != null && m.contains(i) && ((E = r.current) == null || E.removeChild(i));
        const {
          portals: b,
          clonedElement: C
        } = H(t);
        i = C, a(b), i.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          p();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      d();
      const f = Pe(() => {
        d(), u == null || u.disconnect(), u == null || u.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      u = new window.MutationObserver(f), u.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (x = r.current) == null || x.appendChild(i);
    return () => {
      var d, f;
      i.style.display = "", (d = r.current) != null && d.contains(i) && ((f = r.current) == null || f.removeChild(i)), u == null || u.disconnect();
    };
  }, [t, _, o, s, n, l]), I.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
}), ct = ({
  children: t,
  ...e
}) => /* @__PURE__ */ v.jsx(v.Fragment, {
  children: t(e)
});
function ce(t) {
  return I.createElement(ct, {
    children: t
  });
}
function U(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, n) => {
      var g;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((g = l.props) == null ? void 0 : g.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(l.slots).forEach((_) => {
        if (!l.slots[_] || !(l.slots[_] instanceof Element) && !l.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((f, b) => {
          c[f] || (c[f] = {}), b !== i.length - 1 && (c = r[f]);
        });
        const p = l.slots[_];
        let u, w, x = (e == null ? void 0 : e.clone) ?? !1, d = e == null ? void 0 : e.forceClone;
        p instanceof Element ? u = p : (u = p.el, w = p.callback, x = p.clone ?? x, d = p.forceClone ?? d), d = d ?? !!w, c[i[i.length - 1]] = u ? w ? (...f) => (w(i[i.length - 1], f), /* @__PURE__ */ v.jsx(M, {
          ...l.ctx,
          params: f,
          forceClone: d,
          children: /* @__PURE__ */ v.jsx(T, {
            slot: u,
            clone: x
          })
        })) : ce((f) => /* @__PURE__ */ v.jsx(M, {
          ...l.ctx,
          forceClone: d,
          children: /* @__PURE__ */ v.jsx(T, {
            slot: u,
            clone: x,
            ...f
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return l[a] ? r[a] = U(l[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function j(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ce((o) => /* @__PURE__ */ v.jsx(M, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ v.jsx(T, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ v.jsx(T, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function F({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ v.jsx(I.Fragment, {
    children: j(n, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, r)) : /* @__PURE__ */ v.jsx(v.Fragment, {
    children: j(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: it,
  withItemsContextProvider: at,
  ItemHandler: ft
} = ee("antd-menu-items"), {
  useItems: mt,
  withItemsContextProvider: ht,
  ItemHandler: dt
} = ee("antd-breadcrumb-items"), _t = et(at(["menu.items", "dropdownProps.menu.items"], ({
  setSlotParams: t,
  itemSlots: e,
  ...o
}) => {
  const {
    items: {
      "menu.items": s,
      "dropdownProps.menu.items": l
    }
  } = it();
  return /* @__PURE__ */ v.jsx(dt, {
    ...o,
    itemProps: (n) => {
      var g, _, i, p, u, w, x, d, f, b, C;
      const r = {
        ...n.menu || {},
        items: (g = n.menu) != null && g.items || s.length > 0 ? U(s, {
          clone: !0
        }) : void 0,
        expandIcon: F({
          setSlotParams: t,
          slots: e,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) || ((_ = n.menu) == null ? void 0 : _.expandIcon),
        overflowedIndicator: j(e["menu.overflowedIndicator"]) || ((i = n.menu) == null ? void 0 : i.overflowedIndicator)
      }, c = {
        ...((p = n.dropdownProps) == null ? void 0 : p.menu) || {},
        items: (w = (u = n.dropdownProps) == null ? void 0 : u.menu) != null && w.items || l.length > 0 ? U(l, {
          clone: !0
        }) : void 0,
        expandIcon: F({
          setSlotParams: t,
          slots: e,
          key: "dropdownProps.menu.expandIcon"
        }, {
          clone: !0
        }) || ((d = (x = n.dropdownProps) == null ? void 0 : x.menu) == null ? void 0 : d.expandIcon),
        overflowedIndicator: j(e["dropdownProps.menu.overflowedIndicator"]) || ((b = (f = n.dropdownProps) == null ? void 0 : f.menu) == null ? void 0 : b.overflowedIndicator)
      }, a = {
        ...n.dropdownProps || {},
        dropdownRender: e["dropdownProps.dropdownRender"] ? F({
          setSlotParams: t,
          slots: e,
          key: "dropdownProps.dropdownRender"
        }, {
          clone: !0
        }) : nt((C = n.dropdownProps) == null ? void 0 : C.dropdownRender),
        menu: Object.values(c).filter(Boolean).length > 0 ? c : void 0
      };
      return {
        ...n,
        menu: Object.values(r).filter(Boolean).length > 0 ? r : void 0,
        dropdownProps: Object.values(a).filter(Boolean).length > 0 ? a : void 0
      };
    }
  });
}));
export {
  _t as BreadcrumbItem,
  _t as default
};
