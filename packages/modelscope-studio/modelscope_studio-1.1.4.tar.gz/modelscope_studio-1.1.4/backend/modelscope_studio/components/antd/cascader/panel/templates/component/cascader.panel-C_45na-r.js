import { i as ae, a as M, r as ue, b as de, g as fe, w as k } from "./Index-CohXxHkw.js";
const y = window.ms_globals.React, ie = window.ms_globals.React.forwardRef, A = window.ms_globals.React.useRef, $ = window.ms_globals.React.useState, F = window.ms_globals.React.useEffect, ce = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, me = window.ms_globals.internalContext.useContextPropsContext, B = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.Cascader, he = window.ms_globals.createItemsContext.createItemsContext;
var pe = /\s/;
function ge(t) {
  for (var e = t.length; e-- && pe.test(t.charAt(e)); )
    ;
  return e;
}
var be = /^\s+/;
function xe(t) {
  return t && t.slice(0, ge(t) + 1).replace(be, "");
}
var H = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, we = /^0b[01]+$/i, Ce = /^0o[0-7]+$/i, ye = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (ae(t))
    return H;
  if (M(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = M(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = xe(t);
  var s = we.test(t);
  return s || Ce.test(t) ? ye(t.slice(2), s ? 2 : 8) : Ee.test(t) ? H : +t;
}
var L = function() {
  return ue.Date.now();
}, Ie = "Expected a function", ve = Math.max, Se = Math.min;
function Re(t, e, s) {
  var l, o, n, r, i, a, h = 0, p = !1, c = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(Ie);
  e = q(e) || 0, M(s) && (p = !!s.leading, c = "maxWait" in s, n = c ? ve(q(s.maxWait) || 0, e) : n, g = "trailing" in s ? !!s.trailing : g);
  function f(_) {
    var C = l, R = o;
    return l = o = void 0, h = _, r = t.apply(R, C), r;
  }
  function b(_) {
    return h = _, i = setTimeout(m, e), p ? f(_) : r;
  }
  function E(_) {
    var C = _ - a, R = _ - h, U = e - C;
    return c ? Se(U, n - R) : U;
  }
  function u(_) {
    var C = _ - a, R = _ - h;
    return a === void 0 || C >= e || C < 0 || c && R >= n;
  }
  function m() {
    var _ = L();
    if (u(_))
      return w(_);
    i = setTimeout(m, E(_));
  }
  function w(_) {
    return i = void 0, g && l ? f(_) : (l = o = void 0, r);
  }
  function S() {
    i !== void 0 && clearTimeout(i), h = 0, l = a = o = i = void 0;
  }
  function d() {
    return i === void 0 ? r : w(L());
  }
  function I() {
    var _ = L(), C = u(_);
    if (l = arguments, o = this, a = _, C) {
      if (i === void 0)
        return b(a);
      if (c)
        return clearTimeout(i), i = setTimeout(m, e), f(a);
    }
    return i === void 0 && (i = setTimeout(m, e)), r;
  }
  return I.cancel = S, I.flush = d, I;
}
function ke(t, e) {
  return de(t, e);
}
var ee = {
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
var Pe = y, Oe = Symbol.for("react.element"), Te = Symbol.for("react.fragment"), je = Object.prototype.hasOwnProperty, Le = Pe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function te(t, e, s) {
  var l, o = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (l in e) je.call(e, l) && !Ne.hasOwnProperty(l) && (o[l] = e[l]);
  if (t && t.defaultProps) for (l in e = t.defaultProps, e) o[l] === void 0 && (o[l] = e[l]);
  return {
    $$typeof: Oe,
    type: t,
    key: n,
    ref: r,
    props: o,
    _owner: Le.current
  };
}
j.Fragment = Te;
j.jsx = te;
j.jsxs = te;
ee.exports = j;
var x = ee.exports;
const {
  SvelteComponent: Ae,
  assign: z,
  binding_callbacks: G,
  check_outros: Fe,
  children: ne,
  claim_element: re,
  claim_space: We,
  component_subscribe: J,
  compute_slots: Me,
  create_slot: De,
  detach: v,
  element: oe,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: Ve,
  get_slot_changes: Ue,
  group_outros: Be,
  init: He,
  insert_hydration: P,
  safe_not_equal: qe,
  set_custom_element_data: se,
  space: ze,
  transition_in: O,
  transition_out: D,
  update_slot_base: Ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: Je,
  getContext: Xe,
  onDestroy: Ye,
  setContext: Ke
} = window.__gradio__svelte__internal;
function K(t) {
  let e, s;
  const l = (
    /*#slots*/
    t[7].default
  ), o = De(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = oe("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = re(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ne(e);
      o && o.l(r), r.forEach(v), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, e, r), o && o.m(e, null), t[9](e), s = !0;
    },
    p(n, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && Ge(
        o,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? Ue(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : Ve(
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
      n && v(e), o && o.d(n), t[9](null);
    }
  };
}
function Qe(t) {
  let e, s, l, o, n = (
    /*$$slots*/
    t[4].default && K(t)
  );
  return {
    c() {
      e = oe("react-portal-target"), s = ze(), n && n.c(), l = X(), this.h();
    },
    l(r) {
      e = re(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ne(e).forEach(v), s = We(r), n && n.l(r), l = X(), this.h();
    },
    h() {
      se(e, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      P(r, e, i), t[8](e), P(r, s, i), n && n.m(r, i), P(r, l, i), o = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && O(n, 1)) : (n = K(r), n.c(), O(n, 1), n.m(l.parentNode, l)) : n && (Be(), D(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(r) {
      o || (O(n), o = !0);
    },
    o(r) {
      D(n), o = !1;
    },
    d(r) {
      r && (v(e), v(s), v(l)), t[8](null), n && n.d(r);
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
function Ze(t, e, s) {
  let l, o, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const i = Me(n);
  let {
    svelteInit: a
  } = e;
  const h = k(Q(e)), p = k();
  J(t, p, (d) => s(0, l = d));
  const c = k();
  J(t, c, (d) => s(1, o = d));
  const g = [], f = Xe("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: E,
    subSlotIndex: u
  } = fe() || {}, m = a({
    parent: f,
    props: h,
    target: p,
    slot: c,
    slotKey: b,
    slotIndex: E,
    subSlotIndex: u,
    onDestroy(d) {
      g.push(d);
    }
  });
  Ke("$$ms-gr-react-wrapper", m), Je(() => {
    h.set(Q(e));
  }), Ye(() => {
    g.forEach((d) => d());
  });
  function w(d) {
    G[d ? "unshift" : "push"](() => {
      l = d, p.set(l);
    });
  }
  function S(d) {
    G[d ? "unshift" : "push"](() => {
      o = d, c.set(o);
    });
  }
  return t.$$set = (d) => {
    s(17, e = z(z({}, e), Y(d))), "svelteInit" in d && s(5, a = d.svelteInit), "$$scope" in d && s(6, r = d.$$scope);
  }, e = Y(e), [l, o, p, c, i, a, r, n, w, S];
}
class $e extends Ae {
  constructor(e) {
    super(), He(this, e, Ze, Qe, qe, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, N = window.ms_globals.tree;
function et(t, e = {}) {
  function s(l) {
    const o = k(), n = new $e({
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
            a.nodes = a.nodes.filter((h) => h.svelteInstance !== o), Z({
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
const tt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function nt(t) {
  return t ? Object.keys(t).reduce((e, s) => {
    const l = t[s];
    return e[s] = rt(s, l), e;
  }, {}) : {};
}
function rt(t, e) {
  return typeof e == "number" && !tt.includes(t) ? e + "px" : e;
}
function V(t) {
  const e = [], s = t.cloneNode(!1);
  if (t._reactElement) {
    const o = y.Children.toArray(t._reactElement.props.children).map((n) => {
      if (y.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = V(n.props.el);
        return y.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...y.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = t._reactElement.props.children, e.push(W(y.cloneElement(t._reactElement, {
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
      } = V(n);
      e.push(...i), s.appendChild(r);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: e
  };
}
function ot(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const T = ie(({
  slot: t,
  clone: e,
  className: s,
  style: l,
  observeAttributes: o
}, n) => {
  const r = A(), [i, a] = $([]), {
    forceClone: h
  } = me(), p = h ? !0 : e;
  return F(() => {
    var E;
    if (!r.current || !t)
      return;
    let c = t;
    function g() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ot(n, u), s && u.classList.add(...s.split(" ")), l) {
        const m = nt(l);
        Object.keys(m).forEach((w) => {
          u.style[w] = m[w];
        });
      }
    }
    let f = null, b = null;
    if (p && window.MutationObserver) {
      let u = function() {
        var d, I, _;
        (d = r.current) != null && d.contains(c) && ((I = r.current) == null || I.removeChild(c));
        const {
          portals: w,
          clonedElement: S
        } = V(t);
        c = S, a(w), c.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          g();
        }, 50), (_ = r.current) == null || _.appendChild(c);
      };
      u();
      const m = Re(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", g(), (E = r.current) == null || E.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = r.current) != null && u.contains(c) && ((m = r.current) == null || m.removeChild(c)), f == null || f.disconnect();
    };
  }, [t, p, s, l, n, o]), y.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
});
function st({
  value: t,
  onValueChange: e
}) {
  const [s, l] = $(t), o = A(e);
  o.current = e;
  const n = A(s);
  return n.current = s, F(() => {
    o.current(s);
  }, [s]), F(() => {
    ke(t, n.current) || l(t);
  }, [t]), [s, l];
}
const lt = ({
  children: t,
  ...e
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: t(e)
});
function it(t) {
  return y.createElement(lt, {
    children: t
  });
}
function le(t, e, s) {
  const l = t.filter(Boolean);
  if (l.length !== 0)
    return l.map((o, n) => {
      var h;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((h = o.props) == null ? void 0 : h.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(o.slots).forEach((p) => {
        if (!o.slots[p] || !(o.slots[p] instanceof Element) && !o.slots[p].el)
          return;
        const c = p.split(".");
        c.forEach((m, w) => {
          i[m] || (i[m] = {}), w !== c.length - 1 && (i = r[m]);
        });
        const g = o.slots[p];
        let f, b, E = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        g instanceof Element ? f = g : (f = g.el, b = g.callback, E = g.clone ?? E, u = g.forceClone ?? u), u = u ?? !!b, i[c[c.length - 1]] = f ? b ? (...m) => (b(c[c.length - 1], m), /* @__PURE__ */ x.jsx(B, {
          ...o.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(T, {
            slot: f,
            clone: E
          })
        })) : it((m) => /* @__PURE__ */ x.jsx(B, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(T, {
            slot: f,
            clone: E,
            ...m
          })
        })) : i[c[c.length - 1]], i = r;
      });
      const a = (e == null ? void 0 : e.children) || "children";
      return o[a] ? r[a] = le(o[a], e, `${n}`) : e != null && e.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
const {
  useItems: ct,
  withItemsContextProvider: at,
  ItemHandler: dt
} = he("antd-cascader-options"), ft = et(at(["default", "options"], ({
  slots: t,
  children: e,
  onValueChange: s,
  onChange: l,
  onLoadData: o,
  options: n,
  ...r
}) => {
  const [i, a] = st({
    onValueChange: s,
    value: r.value
  }), {
    items: h
  } = ct(), p = h.options.length > 0 ? h.options : h.default;
  return /* @__PURE__ */ x.jsxs(x.Fragment, {
    children: [/* @__PURE__ */ x.jsx("div", {
      style: {
        display: "none"
      },
      children: e
    }), /* @__PURE__ */ x.jsx(_e.Panel, {
      ...r,
      value: i,
      options: ce(() => n || le(p, {
        clone: !0
      }), [n, p]),
      loadData: o,
      onChange: (c, ...g) => {
        l == null || l(c, ...g), a(c);
      },
      expandIcon: t.expandIcon ? /* @__PURE__ */ x.jsx(T, {
        slot: t.expandIcon
      }) : r.expandIcon,
      notFoundContent: t.notFoundContent ? /* @__PURE__ */ x.jsx(T, {
        slot: t.notFoundContent
      }) : r.notFoundContent
    })]
  });
}));
export {
  ft as CascaderPanel,
  ft as default
};
