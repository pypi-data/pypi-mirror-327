import { i as de, a as W, r as fe, g as me, w as O } from "./Index-BCAbRmlm.js";
const E = window.ms_globals.React, oe = window.ms_globals.React.forwardRef, ce = window.ms_globals.React.useRef, ae = window.ms_globals.React.useState, ie = window.ms_globals.React.useEffect, ue = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.internalContext.useContextPropsContext, F = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.Breadcrumb, ge = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function pe(t) {
  for (var e = t.length; e-- && be.test(t.charAt(e)); )
    ;
  return e;
}
var xe = /^\s+/;
function Ce(t) {
  return t && t.slice(0, pe(t) + 1).replace(xe, "");
}
var U = NaN, we = /^[-+]0x[0-9a-f]+$/i, Ee = /^0b[01]+$/i, ye = /^0o[0-7]+$/i, ve = parseInt;
function H(t) {
  if (typeof t == "number")
    return t;
  if (de(t))
    return U;
  if (W(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = W(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Ce(t);
  var s = Ee.test(t);
  return s || ye.test(t) ? ve(t.slice(2), s ? 2 : 8) : we.test(t) ? U : +t;
}
var L = function() {
  return fe.Date.now();
}, Ie = "Expected a function", Se = Math.max, Re = Math.min;
function ke(t, e, s) {
  var o, l, r, n, c, i, p = 0, g = !1, a = !1, b = !0;
  if (typeof t != "function")
    throw new TypeError(Ie);
  e = H(e) || 0, W(s) && (g = !!s.leading, a = "maxWait" in s, r = a ? Se(H(s.maxWait) || 0, e) : r, b = "trailing" in s ? !!s.trailing : b);
  function f(h) {
    var y = o, R = l;
    return o = l = void 0, p = h, n = t.apply(R, y), n;
  }
  function x(h) {
    return p = h, c = setTimeout(m, e), g ? f(h) : n;
  }
  function C(h) {
    var y = h - i, R = h - p, D = e - y;
    return a ? Re(D, r - R) : D;
  }
  function u(h) {
    var y = h - i, R = h - p;
    return i === void 0 || y >= e || y < 0 || a && R >= r;
  }
  function m() {
    var h = L();
    if (u(h))
      return w(h);
    c = setTimeout(m, C(h));
  }
  function w(h) {
    return c = void 0, b && o ? f(h) : (o = l = void 0, n);
  }
  function S() {
    c !== void 0 && clearTimeout(c), p = 0, o = i = l = c = void 0;
  }
  function d() {
    return c === void 0 ? n : w(L());
  }
  function v() {
    var h = L(), y = u(h);
    if (o = arguments, l = this, i = h, y) {
      if (c === void 0)
        return x(i);
      if (a)
        return clearTimeout(c), c = setTimeout(m, e), f(i);
    }
    return c === void 0 && (c = setTimeout(m, e)), n;
  }
  return v.cancel = S, v.flush = d, v;
}
var Z = {
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
var Oe = E, Pe = Symbol.for("react.element"), Te = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Le = Oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function $(t, e, s) {
  var o, l = {}, r = null, n = null;
  s !== void 0 && (r = "" + s), e.key !== void 0 && (r = "" + e.key), e.ref !== void 0 && (n = e.ref);
  for (o in e) je.call(e, o) && !Ne.hasOwnProperty(o) && (l[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) l[o] === void 0 && (l[o] = e[o]);
  return {
    $$typeof: Pe,
    type: t,
    key: r,
    ref: n,
    props: l,
    _owner: Le.current
  };
}
j.Fragment = Te;
j.jsx = $;
j.jsxs = $;
Z.exports = j;
var _ = Z.exports;
const {
  SvelteComponent: Ae,
  assign: z,
  binding_callbacks: G,
  check_outros: We,
  children: ee,
  claim_element: te,
  claim_space: Fe,
  component_subscribe: q,
  compute_slots: Me,
  create_slot: Be,
  detach: I,
  element: re,
  empty: V,
  exclude_internal_props: J,
  get_all_dirty_from_scope: De,
  get_slot_changes: Ue,
  group_outros: He,
  init: ze,
  insert_hydration: P,
  safe_not_equal: Ge,
  set_custom_element_data: ne,
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
function X(t) {
  let e, s;
  const o = (
    /*#slots*/
    t[7].default
  ), l = Be(
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
    l(r) {
      e = te(r, "SVELTE-SLOT", {
        class: !0
      });
      var n = ee(e);
      l && l.l(n), n.forEach(I), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(r, n) {
      P(r, e, n), l && l.m(e, null), t[9](e), s = !0;
    },
    p(r, n) {
      l && l.p && (!s || n & /*$$scope*/
      64) && Ve(
        l,
        o,
        r,
        /*$$scope*/
        r[6],
        s ? Ue(
          o,
          /*$$scope*/
          r[6],
          n,
          null
        ) : De(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      s || (T(l, r), s = !0);
    },
    o(r) {
      M(l, r), s = !1;
    },
    d(r) {
      r && I(e), l && l.d(r), t[9](null);
    }
  };
}
function Qe(t) {
  let e, s, o, l, r = (
    /*$$slots*/
    t[4].default && X(t)
  );
  return {
    c() {
      e = re("react-portal-target"), s = qe(), r && r.c(), o = V(), this.h();
    },
    l(n) {
      e = te(n, "REACT-PORTAL-TARGET", {
        class: !0
      }), ee(e).forEach(I), s = Fe(n), r && r.l(n), o = V(), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(n, c) {
      P(n, e, c), t[8](e), P(n, s, c), r && r.m(n, c), P(n, o, c), l = !0;
    },
    p(n, [c]) {
      /*$$slots*/
      n[4].default ? r ? (r.p(n, c), c & /*$$slots*/
      16 && T(r, 1)) : (r = X(n), r.c(), T(r, 1), r.m(o.parentNode, o)) : r && (He(), M(r, 1, 1, () => {
        r = null;
      }), We());
    },
    i(n) {
      l || (T(r), l = !0);
    },
    o(n) {
      M(r), l = !1;
    },
    d(n) {
      n && (I(e), I(s), I(o)), t[8](null), r && r.d(n);
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
function Ze(t, e, s) {
  let o, l, {
    $$slots: r = {},
    $$scope: n
  } = e;
  const c = Me(r);
  let {
    svelteInit: i
  } = e;
  const p = O(Y(e)), g = O();
  q(t, g, (d) => s(0, o = d));
  const a = O();
  q(t, a, (d) => s(1, l = d));
  const b = [], f = Xe("$$ms-gr-react-wrapper"), {
    slotKey: x,
    slotIndex: C,
    subSlotIndex: u
  } = me() || {}, m = i({
    parent: f,
    props: p,
    target: g,
    slot: a,
    slotKey: x,
    slotIndex: C,
    subSlotIndex: u,
    onDestroy(d) {
      b.push(d);
    }
  });
  Ke("$$ms-gr-react-wrapper", m), Je(() => {
    p.set(Y(e));
  }), Ye(() => {
    b.forEach((d) => d());
  });
  function w(d) {
    G[d ? "unshift" : "push"](() => {
      o = d, g.set(o);
    });
  }
  function S(d) {
    G[d ? "unshift" : "push"](() => {
      l = d, a.set(l);
    });
  }
  return t.$$set = (d) => {
    s(17, e = z(z({}, e), J(d))), "svelteInit" in d && s(5, i = d.svelteInit), "$$scope" in d && s(6, n = d.$$scope);
  }, e = J(e), [o, l, g, a, c, i, n, r, w, S];
}
class $e extends Ae {
  constructor(e) {
    super(), ze(this, e, Ze, Qe, Ge, {
      svelteInit: 5
    });
  }
}
const K = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(t, e = {}) {
  function s(o) {
    const l = O(), r = new $e({
      ...o,
      props: {
        svelteInit(n) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: t,
            props: n.props,
            slot: n.slot,
            target: n.target,
            slotIndex: n.slotIndex,
            subSlotIndex: n.subSlotIndex,
            ignore: e.ignore,
            slotKey: n.slotKey,
            nodes: []
          }, i = n.parent ?? N;
          return i.nodes = [...i.nodes, c], K({
            createPortal: A,
            node: N
          }), n.onDestroy(() => {
            i.nodes = i.nodes.filter((p) => p.svelteInstance !== l), K({
              createPortal: A,
              node: N
            });
          }), c;
        },
        ...o.props
      }
    });
    return l.set(r), r;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(s);
    });
  });
}
const tt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rt(t) {
  return t ? Object.keys(t).reduce((e, s) => {
    const o = t[s];
    return e[s] = nt(s, o), e;
  }, {}) : {};
}
function nt(t, e) {
  return typeof e == "number" && !tt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], s = t.cloneNode(!1);
  if (t._reactElement) {
    const l = E.Children.toArray(t._reactElement.props.children).map((r) => {
      if (E.isValidElement(r) && r.props.__slot__) {
        const {
          portals: n,
          clonedElement: c
        } = B(r.props.el);
        return E.cloneElement(r, {
          ...r.props,
          el: c,
          children: [...E.Children.toArray(r.props.children), ...n]
        });
      }
      return null;
    });
    return l.originalChildren = t._reactElement.props.children, e.push(A(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: l
    }), s)), {
      clonedElement: s,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((l) => {
    t.getEventListeners(l).forEach(({
      listener: n,
      type: c,
      useCapture: i
    }) => {
      s.addEventListener(c, n, i);
    });
  });
  const o = Array.from(t.childNodes);
  for (let l = 0; l < o.length; l++) {
    const r = o[l];
    if (r.nodeType === 1) {
      const {
        clonedElement: n,
        portals: c
      } = B(r);
      e.push(...c), s.appendChild(n);
    } else r.nodeType === 3 && s.appendChild(r.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function lt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const k = oe(({
  slot: t,
  clone: e,
  className: s,
  style: o,
  observeAttributes: l
}, r) => {
  const n = ce(), [c, i] = ae([]), {
    forceClone: p
  } = he(), g = p ? !0 : e;
  return ie(() => {
    var C;
    if (!n.current || !t)
      return;
    let a = t;
    function b() {
      let u = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (u = a.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), lt(r, u), s && u.classList.add(...s.split(" ")), o) {
        const m = rt(o);
        Object.keys(m).forEach((w) => {
          u.style[w] = m[w];
        });
      }
    }
    let f = null, x = null;
    if (g && window.MutationObserver) {
      let u = function() {
        var d, v, h;
        (d = n.current) != null && d.contains(a) && ((v = n.current) == null || v.removeChild(a));
        const {
          portals: w,
          clonedElement: S
        } = B(t);
        a = S, i(w), a.style.display = "contents", x && clearTimeout(x), x = setTimeout(() => {
          b();
        }, 50), (h = n.current) == null || h.appendChild(a);
      };
      u();
      const m = ke(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", b(), (C = n.current) == null || C.appendChild(a);
    return () => {
      var u, m;
      a.style.display = "", (u = n.current) != null && u.contains(a) && ((m = n.current) == null || m.removeChild(a)), f == null || f.disconnect();
    };
  }, [t, g, s, o, r, l]), E.createElement("react-child", {
    ref: n,
    style: {
      display: "contents"
    }
  }, ...c);
}), st = ({
  children: t,
  ...e
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: t(e)
});
function le(t) {
  return E.createElement(st, {
    children: t
  });
}
function se(t, e, s) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((l, r) => {
      var p;
      if (typeof l != "object")
        return e != null && e.fallback ? e.fallback(l) : l;
      const n = {
        ...l.props,
        key: ((p = l.props) == null ? void 0 : p.key) ?? (s ? `${s}-${r}` : `${r}`)
      };
      let c = n;
      Object.keys(l.slots).forEach((g) => {
        if (!l.slots[g] || !(l.slots[g] instanceof Element) && !l.slots[g].el)
          return;
        const a = g.split(".");
        a.forEach((m, w) => {
          c[m] || (c[m] = {}), w !== a.length - 1 && (c = n[m]);
        });
        const b = l.slots[g];
        let f, x, C = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        b instanceof Element ? f = b : (f = b.el, x = b.callback, C = b.clone ?? C, u = b.forceClone ?? u), u = u ?? !!x, c[a[a.length - 1]] = f ? x ? (...m) => (x(a[a.length - 1], m), /* @__PURE__ */ _.jsx(F, {
          ...l.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(k, {
            slot: f,
            clone: C
          })
        })) : le((m) => /* @__PURE__ */ _.jsx(F, {
          ...l.ctx,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(k, {
            slot: f,
            clone: C,
            ...m
          })
        })) : c[a[a.length - 1]], c = n;
      });
      const i = (e == null ? void 0 : e.children) || "children";
      return l[i] ? n[i] = se(l[i], e, `${r}`) : e != null && e.children && (n[i] = void 0, Reflect.deleteProperty(n, i)), n;
    });
}
function Q(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? le((s) => /* @__PURE__ */ _.jsx(F, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ _.jsx(k, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...s
    })
  })) : /* @__PURE__ */ _.jsx(k, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ot({
  key: t,
  slots: e,
  targets: s
}, o) {
  return e[t] ? (...l) => s ? s.map((r, n) => /* @__PURE__ */ _.jsx(E.Fragment, {
    children: Q(r, {
      clone: !0,
      params: l,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, n)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: Q(e[t], {
      clone: !0,
      params: l,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: ct,
  withItemsContextProvider: at,
  ItemHandler: ut
} = ge("antd-breadcrumb-items"), dt = et(at(["default", "items"], ({
  slots: t,
  items: e,
  setSlotParams: s,
  children: o,
  ...l
}) => {
  const {
    items: r
  } = ct(), n = r.items.length ? r.items : r.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: o
    }), /* @__PURE__ */ _.jsx(_e, {
      ...l,
      itemRender: t.itemRender ? ot({
        setSlotParams: s,
        slots: t,
        key: "itemRender"
      }, {
        clone: !0
      }) : l.itemRender,
      items: ue(() => e || se(n, {
        // clone: true,
      }), [e, n]),
      separator: t.separator ? /* @__PURE__ */ _.jsx(k, {
        slot: t.separator,
        clone: !0
      }) : l.separator
    })]
  });
}));
export {
  dt as Breadcrumb,
  dt as default
};
