import { i as _e, a as B, r as ge, g as pe, w as O, d as xe, b as T, c as we } from "./Index-gbu2UQQi.js";
const I = window.ms_globals.React, F = window.ms_globals.React.useMemo, re = window.ms_globals.React.useState, oe = window.ms_globals.React.useEffect, me = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, M = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.internalContext.useContextPropsContext, U = window.ms_globals.internalContext.ContextPropsProvider, Ce = window.ms_globals.antd.Dropdown, Ie = window.ms_globals.createItemsContext.createItemsContext;
var ye = /\s/;
function ve(t) {
  for (var e = t.length; e-- && ye.test(t.charAt(e)); )
    ;
  return e;
}
var Ee = /^\s+/;
function Se(t) {
  return t && t.slice(0, ve(t) + 1).replace(Ee, "");
}
var V = NaN, Re = /^[-+]0x[0-9a-f]+$/i, ke = /^0b[01]+$/i, Te = /^0o[0-7]+$/i, Oe = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (_e(t))
    return V;
  if (B(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = B(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Se(t);
  var o = ke.test(t);
  return o || Te.test(t) ? Oe(t.slice(2), o ? 2 : 8) : Re.test(t) ? V : +t;
}
var A = function() {
  return ge.Date.now();
}, Pe = "Expected a function", je = Math.max, Fe = Math.min;
function Le(t, e, o) {
  var s, l, n, r, c, a, x = 0, g = !1, i = !1, _ = !0;
  if (typeof t != "function")
    throw new TypeError(Pe);
  e = q(e) || 0, B(o) && (g = !!o.leading, i = "maxWait" in o, n = i ? je(q(o.maxWait) || 0, e) : n, _ = "trailing" in o ? !!o.trailing : _);
  function d(h) {
    var y = s, k = l;
    return s = l = void 0, x = h, r = t.apply(k, y), r;
  }
  function w(h) {
    return x = h, c = setTimeout(f, e), g ? d(h) : r;
  }
  function b(h) {
    var y = h - a, k = h - x, G = e - y;
    return i ? Fe(G, n - k) : G;
  }
  function u(h) {
    var y = h - a, k = h - x;
    return a === void 0 || y >= e || y < 0 || i && k >= n;
  }
  function f() {
    var h = A();
    if (u(h))
      return C(h);
    c = setTimeout(f, b(h));
  }
  function C(h) {
    return c = void 0, _ && s ? d(h) : (s = l = void 0, r);
  }
  function R() {
    c !== void 0 && clearTimeout(c), x = 0, s = a = l = c = void 0;
  }
  function m() {
    return c === void 0 ? r : C(A());
  }
  function v() {
    var h = A(), y = u(h);
    if (s = arguments, l = this, a = h, y) {
      if (c === void 0)
        return w(a);
      if (i)
        return clearTimeout(c), c = setTimeout(f, e), d(a);
    }
    return c === void 0 && (c = setTimeout(f, e)), r;
  }
  return v.cancel = R, v.flush = m, v;
}
var le = {
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
var Ae = I, Ne = Symbol.for("react.element"), We = Symbol.for("react.fragment"), De = Object.prototype.hasOwnProperty, Me = Ae.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Be = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function se(t, e, o) {
  var s, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) De.call(e, s) && !Be.hasOwnProperty(s) && (l[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) l[s] === void 0 && (l[s] = e[s]);
  return {
    $$typeof: Ne,
    type: t,
    key: n,
    ref: r,
    props: l,
    _owner: Me.current
  };
}
L.Fragment = We;
L.jsx = se;
L.jsxs = se;
le.exports = L;
var p = le.exports;
const {
  SvelteComponent: Ue,
  assign: J,
  binding_callbacks: X,
  check_outros: He,
  children: ce,
  claim_element: ie,
  claim_space: ze,
  component_subscribe: Y,
  compute_slots: Ge,
  create_slot: Ve,
  detach: E,
  element: ae,
  empty: Q,
  exclude_internal_props: Z,
  get_all_dirty_from_scope: qe,
  get_slot_changes: Je,
  group_outros: Xe,
  init: Ye,
  insert_hydration: P,
  safe_not_equal: Qe,
  set_custom_element_data: ue,
  space: Ze,
  transition_in: j,
  transition_out: H,
  update_slot_base: Ke
} = window.__gradio__svelte__internal, {
  beforeUpdate: $e,
  getContext: et,
  onDestroy: tt,
  setContext: nt
} = window.__gradio__svelte__internal;
function K(t) {
  let e, o;
  const s = (
    /*#slots*/
    t[7].default
  ), l = Ve(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = ae("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      e = ie(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ce(e);
      l && l.l(r), r.forEach(E), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, e, r), l && l.m(e, null), t[9](e), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Ke(
        l,
        s,
        n,
        /*$$scope*/
        n[6],
        o ? Je(
          s,
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
      o || (j(l, n), o = !0);
    },
    o(n) {
      H(l, n), o = !1;
    },
    d(n) {
      n && E(e), l && l.d(n), t[9](null);
    }
  };
}
function rt(t) {
  let e, o, s, l, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = ae("react-portal-target"), o = Ze(), n && n.c(), s = Q(), this.h();
    },
    l(r) {
      e = ie(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ce(e).forEach(E), o = ze(r), n && n.l(r), s = Q(), this.h();
    },
    h() {
      ue(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      P(r, e, c), t[8](e), P(r, o, c), n && n.m(r, c), P(r, s, c), l = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && j(n, 1)) : (n = K(r), n.c(), j(n, 1), n.m(s.parentNode, s)) : n && (Xe(), H(n, 1, 1, () => {
        n = null;
      }), He());
    },
    i(r) {
      l || (j(n), l = !0);
    },
    o(r) {
      H(n), l = !1;
    },
    d(r) {
      r && (E(e), E(o), E(s)), t[8](null), n && n.d(r);
    }
  };
}
function $(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function ot(t, e, o) {
  let s, l, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Ge(n);
  let {
    svelteInit: a
  } = e;
  const x = O($(e)), g = O();
  Y(t, g, (m) => o(0, s = m));
  const i = O();
  Y(t, i, (m) => o(1, l = m));
  const _ = [], d = et("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: b,
    subSlotIndex: u
  } = pe() || {}, f = a({
    parent: d,
    props: x,
    target: g,
    slot: i,
    slotKey: w,
    slotIndex: b,
    subSlotIndex: u,
    onDestroy(m) {
      _.push(m);
    }
  });
  nt("$$ms-gr-react-wrapper", f), $e(() => {
    x.set($(e));
  }), tt(() => {
    _.forEach((m) => m());
  });
  function C(m) {
    X[m ? "unshift" : "push"](() => {
      s = m, g.set(s);
    });
  }
  function R(m) {
    X[m ? "unshift" : "push"](() => {
      l = m, i.set(l);
    });
  }
  return t.$$set = (m) => {
    o(17, e = J(J({}, e), Z(m))), "svelteInit" in m && o(5, a = m.svelteInit), "$$scope" in m && o(6, r = m.$$scope);
  }, e = Z(e), [s, l, g, i, c, a, r, n, C, R];
}
class lt extends Ue {
  constructor(e) {
    super(), Ye(this, e, ot, rt, Qe, {
      svelteInit: 5
    });
  }
}
const ee = window.ms_globals.rerender, N = window.ms_globals.tree;
function st(t, e = {}) {
  function o(s) {
    const l = O(), n = new lt({
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
          }, a = r.parent ?? N;
          return a.nodes = [...a.nodes, c], ee({
            createPortal: M,
            node: N
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((x) => x.svelteInstance !== l), ee({
              createPortal: M,
              node: N
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
function ct(t) {
  const [e, o] = re(() => T(t));
  return oe(() => {
    let s = !0;
    return t.subscribe((n) => {
      s && (s = !1, n === e) || o(n);
    });
  }, [t]), e;
}
function it(t) {
  const e = F(() => xe(t, (o) => o), [t]);
  return ct(e);
}
const at = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ut(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const s = t[o];
    return e[o] = dt(o, s), e;
  }, {}) : {};
}
function dt(t, e) {
  return typeof e == "number" && !at.includes(t) ? e + "px" : e;
}
function z(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const l = I.Children.toArray(t._reactElement.props.children).map((n) => {
      if (I.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = z(n.props.el);
        return I.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...I.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(M(I.cloneElement(t._reactElement, {
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
      } = z(n);
      e.push(...c), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function ft(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const S = me(({
  slot: t,
  clone: e,
  className: o,
  style: s,
  observeAttributes: l
}, n) => {
  const r = he(), [c, a] = re([]), {
    forceClone: x
  } = be(), g = x ? !0 : e;
  return oe(() => {
    var b;
    if (!r.current || !t)
      return;
    let i = t;
    function _() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ft(n, u), o && u.classList.add(...o.split(" ")), s) {
        const f = ut(s);
        Object.keys(f).forEach((C) => {
          u.style[C] = f[C];
        });
      }
    }
    let d = null, w = null;
    if (g && window.MutationObserver) {
      let u = function() {
        var m, v, h;
        (m = r.current) != null && m.contains(i) && ((v = r.current) == null || v.removeChild(i));
        const {
          portals: C,
          clonedElement: R
        } = z(t);
        i = R, a(C), i.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          _();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      u();
      const f = Le(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      d = new window.MutationObserver(f), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", _(), (b = r.current) == null || b.appendChild(i);
    return () => {
      var u, f;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((f = r.current) == null || f.removeChild(i)), d == null || d.disconnect();
    };
  }, [t, g, o, s, n, l]), I.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
});
function mt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function ht(t, e = !1) {
  try {
    if (we(t))
      return t;
    if (e && !mt(t))
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
function W(t, e) {
  return F(() => ht(t, e), [t, e]);
}
function te(t, e) {
  const o = F(() => I.Children.toArray(t.originalChildren || t).filter((n) => n.props.node && !n.props.node.ignore && (!e && !n.props.nodeSlotKey || e && e === n.props.nodeSlotKey)).sort((n, r) => {
    if (n.props.node.slotIndex && r.props.node.slotIndex) {
      const c = T(n.props.node.slotIndex) || 0, a = T(r.props.node.slotIndex) || 0;
      return c - a === 0 && n.props.node.subSlotIndex && r.props.node.subSlotIndex ? (T(n.props.node.subSlotIndex) || 0) - (T(r.props.node.subSlotIndex) || 0) : c - a;
    }
    return 0;
  }).map((n) => n.props.node.target), [t, e]);
  return it(o);
}
const _t = ({
  children: t,
  ...e
}) => /* @__PURE__ */ p.jsx(p.Fragment, {
  children: t(e)
});
function de(t) {
  return I.createElement(_t, {
    children: t
  });
}
function fe(t, e, o) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((l, n) => {
      var x;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((x = l.props) == null ? void 0 : x.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(l.slots).forEach((g) => {
        if (!l.slots[g] || !(l.slots[g] instanceof Element) && !l.slots[g].el)
          return;
        const i = g.split(".");
        i.forEach((f, C) => {
          c[f] || (c[f] = {}), C !== i.length - 1 && (c = r[f]);
        });
        const _ = l.slots[g];
        let d, w, b = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        _ instanceof Element ? d = _ : (d = _.el, w = _.callback, b = _.clone ?? b, u = _.forceClone ?? u), u = u ?? !!w, c[i[i.length - 1]] = d ? w ? (...f) => (w(i[i.length - 1], f), /* @__PURE__ */ p.jsx(U, {
          ...l.ctx,
          params: f,
          forceClone: u,
          children: /* @__PURE__ */ p.jsx(S, {
            slot: d,
            clone: b
          })
        })) : de((f) => /* @__PURE__ */ p.jsx(U, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ p.jsx(S, {
            slot: d,
            clone: b,
            ...f
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return l[a] ? r[a] = fe(l[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function ne(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? de((o) => /* @__PURE__ */ p.jsx(U, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ p.jsx(S, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ p.jsx(S, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function D({
  key: t,
  slots: e,
  targets: o
}, s) {
  return e[t] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ p.jsx(I.Fragment, {
    children: ne(n, {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }, r)) : /* @__PURE__ */ p.jsx(p.Fragment, {
    children: ne(e[t], {
      clone: !0,
      params: l,
      forceClone: (s == null ? void 0 : s.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: gt,
  withItemsContextProvider: pt,
  ItemHandler: wt
} = Ie("antd-menu-items"), bt = st(pt(["menu.items"], ({
  getPopupContainer: t,
  slots: e,
  children: o,
  dropdownRender: s,
  buttonsRender: l,
  setSlotParams: n,
  value: r,
  ...c
}) => {
  var w, b, u;
  const a = W(t), x = W(s), g = W(l), i = te(o, "buttonsRender"), _ = te(o), {
    items: {
      "menu.items": d
    }
  } = gt();
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: _.length > 0 ? null : o
    }), /* @__PURE__ */ p.jsx(Ce.Button, {
      ...c,
      buttonsRender: i.length ? D({
        key: "buttonsRender",
        slots: e,
        setSlotParams: n,
        targets: i
      }) : g,
      menu: {
        ...c.menu,
        items: F(() => {
          var f;
          return ((f = c.menu) == null ? void 0 : f.items) || fe(d, {
            clone: !0
          }) || [];
        }, [d, (w = c.menu) == null ? void 0 : w.items]),
        expandIcon: e["menu.expandIcon"] ? D({
          slots: e,
          setSlotParams: n,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : (b = c.menu) == null ? void 0 : b.expandIcon,
        overflowedIndicator: e["menu.overflowedIndicator"] ? /* @__PURE__ */ p.jsx(S, {
          slot: e["menu.overflowedIndicator"]
        }) : (u = c.menu) == null ? void 0 : u.overflowedIndicator
      },
      getPopupContainer: a,
      dropdownRender: e.dropdownRender ? D({
        slots: e,
        setSlotParams: n,
        key: "dropdownRender"
      }) : x,
      icon: e.icon ? /* @__PURE__ */ p.jsx(S, {
        slot: e.icon
      }) : c.icon,
      children: _.length > 0 ? o : r
    })]
  });
}));
export {
  bt as DropdownButton,
  bt as default
};
