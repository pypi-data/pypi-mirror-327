import { i as me, a as D, r as he, g as _e, w as P, b as ge } from "./Index-DoJOV_Ca.js";
const E = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, ee = window.ms_globals.React.useMemo, A = window.ms_globals.ReactDOM.createPortal, xe = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, we = window.ms_globals.antd.TreeSelect, pe = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function Ce(e) {
  for (var t = e.length; t-- && be.test(e.charAt(t)); )
    ;
  return t;
}
var ye = /^\s+/;
function Ie(e) {
  return e && e.slice(0, Ce(e) + 1).replace(ye, "");
}
var z = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, ve = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Te = parseInt;
function G(e) {
  if (typeof e == "number")
    return e;
  if (me(e))
    return z;
  if (D(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = D(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ie(e);
  var l = ve.test(e);
  return l || Re.test(e) ? Te(e.slice(2), l ? 2 : 8) : Ee.test(e) ? z : +e;
}
var N = function() {
  return he.Date.now();
}, Se = "Expected a function", ke = Math.max, Oe = Math.min;
function Pe(e, t, l) {
  var c, o, n, r, s, a, p = 0, w = !1, i = !1, _ = !0;
  if (typeof e != "function")
    throw new TypeError(Se);
  t = G(t) || 0, D(l) && (w = !!l.leading, i = "maxWait" in l, n = i ? ke(G(l.maxWait) || 0, t) : n, _ = "trailing" in l ? !!l.trailing : _);
  function f(h) {
    var y = c, T = o;
    return c = o = void 0, p = h, r = e.apply(T, y), r;
  }
  function g(h) {
    return p = h, s = setTimeout(m, t), w ? f(h) : r;
  }
  function b(h) {
    var y = h - a, T = h - p, H = t - y;
    return i ? Oe(H, n - T) : H;
  }
  function u(h) {
    var y = h - a, T = h - p;
    return a === void 0 || y >= t || y < 0 || i && T >= n;
  }
  function m() {
    var h = N();
    if (u(h))
      return C(h);
    s = setTimeout(m, b(h));
  }
  function C(h) {
    return s = void 0, _ && c ? f(h) : (c = o = void 0, r);
  }
  function v() {
    s !== void 0 && clearTimeout(s), p = 0, c = a = o = s = void 0;
  }
  function d() {
    return s === void 0 ? r : C(N());
  }
  function I() {
    var h = N(), y = u(h);
    if (c = arguments, o = this, a = h, y) {
      if (s === void 0)
        return g(a);
      if (i)
        return clearTimeout(s), s = setTimeout(m, t), f(a);
    }
    return s === void 0 && (s = setTimeout(m, t)), r;
  }
  return I.cancel = v, I.flush = d, I;
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
var je = E, Fe = Symbol.for("react.element"), Le = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, We = je.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ne(e, t, l) {
  var c, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (c in t) Ne.call(t, c) && !Ae.hasOwnProperty(c) && (o[c] = t[c]);
  if (e && e.defaultProps) for (c in t = e.defaultProps, t) o[c] === void 0 && (o[c] = t[c]);
  return {
    $$typeof: Fe,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: We.current
  };
}
L.Fragment = Le;
L.jsx = ne;
L.jsxs = ne;
te.exports = L;
var x = te.exports;
const {
  SvelteComponent: De,
  assign: q,
  binding_callbacks: V,
  check_outros: Me,
  children: re,
  claim_element: le,
  claim_space: Ue,
  component_subscribe: J,
  compute_slots: Be,
  create_slot: He,
  detach: S,
  element: oe,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: j,
  safe_not_equal: Je,
  set_custom_element_data: ce,
  space: Xe,
  transition_in: F,
  transition_out: U,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function K(e) {
  let t, l;
  const c = (
    /*#slots*/
    e[7].default
  ), o = He(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = oe("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = re(t);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      j(n, t, r), o && o.m(t, null), e[9](t), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Ye(
        o,
        c,
        n,
        /*$$scope*/
        n[6],
        l ? Ge(
          c,
          /*$$scope*/
          n[6],
          r,
          null
        ) : ze(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (F(o, n), l = !0);
    },
    o(n) {
      U(o, n), l = !1;
    },
    d(n) {
      n && S(t), o && o.d(n), e[9](null);
    }
  };
}
function et(e) {
  let t, l, c, o, n = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      t = oe("react-portal-target"), l = Xe(), n && n.c(), c = X(), this.h();
    },
    l(r) {
      t = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(t).forEach(S), l = Ue(r), n && n.l(r), c = X(), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      j(r, t, s), e[8](t), j(r, l, s), n && n.m(r, s), j(r, c, s), o = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, s), s & /*$$slots*/
      16 && F(n, 1)) : (n = K(r), n.c(), F(n, 1), n.m(c.parentNode, c)) : n && (qe(), U(n, 1, 1, () => {
        n = null;
      }), Me());
    },
    i(r) {
      o || (F(n), o = !0);
    },
    o(r) {
      U(n), o = !1;
    },
    d(r) {
      r && (S(t), S(l), S(c)), e[8](null), n && n.d(r);
    }
  };
}
function Q(e) {
  const {
    svelteInit: t,
    ...l
  } = e;
  return l;
}
function tt(e, t, l) {
  let c, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const s = Be(n);
  let {
    svelteInit: a
  } = t;
  const p = P(Q(t)), w = P();
  J(e, w, (d) => l(0, c = d));
  const i = P();
  J(e, i, (d) => l(1, o = d));
  const _ = [], f = Qe("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: b,
    subSlotIndex: u
  } = _e() || {}, m = a({
    parent: f,
    props: p,
    target: w,
    slot: i,
    slotKey: g,
    slotIndex: b,
    subSlotIndex: u,
    onDestroy(d) {
      _.push(d);
    }
  });
  $e("$$ms-gr-react-wrapper", m), Ke(() => {
    p.set(Q(t));
  }), Ze(() => {
    _.forEach((d) => d());
  });
  function C(d) {
    V[d ? "unshift" : "push"](() => {
      c = d, w.set(c);
    });
  }
  function v(d) {
    V[d ? "unshift" : "push"](() => {
      o = d, i.set(o);
    });
  }
  return e.$$set = (d) => {
    l(17, t = q(q({}, t), Y(d))), "svelteInit" in d && l(5, a = d.svelteInit), "$$scope" in d && l(6, r = d.$$scope);
  }, t = Y(t), [c, o, w, i, s, a, r, n, C, v];
}
class nt extends De {
  constructor(t) {
    super(), Ve(this, t, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, W = window.ms_globals.tree;
function rt(e, t = {}) {
  function l(c) {
    const o = P(), n = new nt({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
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
          }, a = r.parent ?? W;
          return a.nodes = [...a.nodes, s], Z({
            createPortal: A,
            node: W
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((p) => p.svelteInstance !== o), Z({
              createPortal: A,
              node: W
            });
          }), s;
        },
        ...c.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(l);
    });
  });
}
const lt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, l) => {
    const c = e[l];
    return t[l] = ct(l, c), t;
  }, {}) : {};
}
function ct(e, t) {
  return typeof t == "number" && !lt.includes(e) ? t + "px" : t;
}
function B(e) {
  const t = [], l = e.cloneNode(!1);
  if (e._reactElement) {
    const o = E.Children.toArray(e._reactElement.props.children).map((n) => {
      if (E.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = B(n.props.el);
        return E.cloneElement(n, {
          ...n.props,
          el: s,
          children: [...E.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(A(E.cloneElement(e._reactElement, {
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
      type: s,
      useCapture: a
    }) => {
      l.addEventListener(s, r, a);
    });
  });
  const c = Array.from(e.childNodes);
  for (let o = 0; o < c.length; o++) {
    const n = c[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = B(n);
      t.push(...s), l.appendChild(r);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: t
  };
}
function st(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const R = ae(({
  slot: e,
  clone: t,
  className: l,
  style: c,
  observeAttributes: o
}, n) => {
  const r = ue(), [s, a] = de([]), {
    forceClone: p
  } = xe(), w = p ? !0 : t;
  return fe(() => {
    var b;
    if (!r.current || !e)
      return;
    let i = e;
    function _() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), st(n, u), l && u.classList.add(...l.split(" ")), c) {
        const m = ot(c);
        Object.keys(m).forEach((C) => {
          u.style[C] = m[C];
        });
      }
    }
    let f = null, g = null;
    if (w && window.MutationObserver) {
      let u = function() {
        var d, I, h;
        (d = r.current) != null && d.contains(i) && ((I = r.current) == null || I.removeChild(i));
        const {
          portals: C,
          clonedElement: v
        } = B(e);
        i = v, a(C), i.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          _();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      u();
      const m = Pe(() => {
        u(), f == null || f.disconnect(), f == null || f.observe(e, {
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
      i.style.display = "contents", _(), (b = r.current) == null || b.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((m = r.current) == null || m.removeChild(i)), f == null || f.disconnect();
    };
  }, [e, w, l, c, n, o]), E.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function it(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function at(e, t = !1) {
  try {
    if (ge(e))
      return e;
    if (t && !it(e))
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
function k(e, t) {
  return ee(() => at(e, t), [e, t]);
}
function ut(e) {
  return Object.keys(e).reduce((t, l) => (e[l] !== void 0 && (t[l] = e[l]), t), {});
}
const dt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ x.jsx(x.Fragment, {
  children: e(t)
});
function se(e) {
  return E.createElement(dt, {
    children: e
  });
}
function ie(e, t, l) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((o, n) => {
      var p;
      if (typeof o != "object")
        return t != null && t.fallback ? t.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((p = o.props) == null ? void 0 : p.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let s = r;
      Object.keys(o.slots).forEach((w) => {
        if (!o.slots[w] || !(o.slots[w] instanceof Element) && !o.slots[w].el)
          return;
        const i = w.split(".");
        i.forEach((m, C) => {
          s[m] || (s[m] = {}), C !== i.length - 1 && (s = r[m]);
        });
        const _ = o.slots[w];
        let f, g, b = (t == null ? void 0 : t.clone) ?? !1, u = t == null ? void 0 : t.forceClone;
        _ instanceof Element ? f = _ : (f = _.el, g = _.callback, b = _.clone ?? b, u = _.forceClone ?? u), u = u ?? !!g, s[i[i.length - 1]] = f ? g ? (...m) => (g(i[i.length - 1], m), /* @__PURE__ */ x.jsx(M, {
          ...o.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            slot: f,
            clone: b
          })
        })) : se((m) => /* @__PURE__ */ x.jsx(M, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ x.jsx(R, {
            slot: f,
            clone: b,
            ...m
          })
        })) : s[i[i.length - 1]], s = r;
      });
      const a = (t == null ? void 0 : t.children) || "children";
      return o[a] ? r[a] = ie(o[a], t, `${n}`) : t != null && t.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function $(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? se((l) => /* @__PURE__ */ x.jsx(M, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ x.jsx(R, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...l
    })
  })) : /* @__PURE__ */ x.jsx(R, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function O({
  key: e,
  slots: t,
  targets: l
}, c) {
  return t[e] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ x.jsx(E.Fragment, {
    children: $(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ x.jsx(x.Fragment, {
    children: $(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: ft,
  useItems: mt,
  ItemHandler: _t
} = pe("antd-tree-select-tree-nodes"), gt = rt(ft(["default", "treeData"], ({
  slots: e,
  filterTreeNode: t,
  getPopupContainer: l,
  dropdownRender: c,
  tagRender: o,
  treeTitleRender: n,
  treeData: r,
  onValueChange: s,
  onChange: a,
  children: p,
  maxTagPlaceholder: w,
  elRef: i,
  setSlotParams: _,
  onLoadData: f,
  ...g
}) => {
  const b = k(t), u = k(l), m = k(o), C = k(c), v = k(n), {
    items: d
  } = mt(), I = d.treeData.length > 0 ? d.treeData : d.default, h = ee(() => ({
    ...g,
    loadData: f,
    treeData: r || ie(I, {
      clone: !0
    }),
    dropdownRender: e.dropdownRender ? O({
      slots: e,
      setSlotParams: _,
      key: "dropdownRender"
    }) : C,
    allowClear: e["allowClear.clearIcon"] ? {
      clearIcon: /* @__PURE__ */ x.jsx(R, {
        slot: e["allowClear.clearIcon"]
      })
    } : g.allowClear,
    suffixIcon: e.suffixIcon ? /* @__PURE__ */ x.jsx(R, {
      slot: e.suffixIcon
    }) : g.suffixIcon,
    prefix: e.prefix ? /* @__PURE__ */ x.jsx(R, {
      slot: e.prefix
    }) : g.prefix,
    switcherIcon: e.switcherIcon ? O({
      slots: e,
      setSlotParams: _,
      key: "switcherIcon"
    }) : g.switcherIcon,
    getPopupContainer: u,
    tagRender: e.tagRender ? O({
      slots: e,
      setSlotParams: _,
      key: "tagRender"
    }) : m,
    treeTitleRender: e.treeTitleRender ? O({
      slots: e,
      setSlotParams: _,
      key: "treeTitleRender"
    }) : v,
    filterTreeNode: b || t,
    maxTagPlaceholder: e.maxTagPlaceholder ? O({
      slots: e,
      setSlotParams: _,
      key: "maxTagPlaceholder"
    }) : w,
    notFoundContent: e.notFoundContent ? /* @__PURE__ */ x.jsx(R, {
      slot: e.notFoundContent
    }) : g.notFoundContent
  }), [C, t, b, u, w, f, g, _, I, e, m, r, v]);
  return /* @__PURE__ */ x.jsxs(x.Fragment, {
    children: [/* @__PURE__ */ x.jsx("div", {
      style: {
        display: "none"
      },
      children: p
    }), /* @__PURE__ */ x.jsx(we, {
      ...ut(h),
      ref: i,
      onChange: (y, ...T) => {
        a == null || a(y, ...T), s(y);
      }
    })]
  });
}));
export {
  gt as TreeSelect,
  gt as default
};
