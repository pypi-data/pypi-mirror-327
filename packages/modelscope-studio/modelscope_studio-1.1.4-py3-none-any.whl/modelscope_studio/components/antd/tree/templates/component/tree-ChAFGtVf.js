import { i as he, a as A, r as _e, g as ge, w as k, b as we } from "./Index-BEjbu_C7.js";
const E = window.ms_globals.React, ue = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, fe = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, te = window.ms_globals.React.useMemo, W = window.ms_globals.ReactDOM.createPortal, be = window.ms_globals.internalContext.useContextPropsContext, M = window.ms_globals.internalContext.ContextPropsProvider, z = window.ms_globals.antd.Tree, pe = window.ms_globals.createItemsContext.createItemsContext;
var xe = /\s/;
function ye(t) {
  for (var e = t.length; e-- && xe.test(t.charAt(e)); )
    ;
  return e;
}
var ve = /^\s+/;
function Ie(t) {
  return t && t.slice(0, ye(t) + 1).replace(ve, "");
}
var G = NaN, Ce = /^[-+]0x[0-9a-f]+$/i, Ee = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Te = parseInt;
function q(t) {
  if (typeof t == "number")
    return t;
  if (he(t))
    return G;
  if (A(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = A(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = Ie(t);
  var l = Ee.test(t);
  return l || Re.test(t) ? Te(t.slice(2), l ? 2 : 8) : Ce.test(t) ? G : +t;
}
var N = function() {
  return _e.Date.now();
}, Oe = "Expected a function", Se = Math.max, je = Math.min;
function ke(t, e, l) {
  var s, o, n, r, c, d, b = 0, _ = !1, i = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(Oe);
  e = q(e) || 0, A(l) && (_ = !!l.leading, i = "maxWait" in l, n = i ? Se(q(l.maxWait) || 0, e) : n, g = "trailing" in l ? !!l.trailing : g);
  function a(h) {
    var y = s, I = o;
    return s = o = void 0, b = h, r = t.apply(I, y), r;
  }
  function p(h) {
    return b = h, c = setTimeout(m, e), _ ? a(h) : r;
  }
  function x(h) {
    var y = h - d, I = h - b, H = e - y;
    return i ? je(H, n - I) : H;
  }
  function u(h) {
    var y = h - d, I = h - b;
    return d === void 0 || y >= e || y < 0 || i && I >= n;
  }
  function m() {
    var h = N();
    if (u(h))
      return v(h);
    c = setTimeout(m, x(h));
  }
  function v(h) {
    return c = void 0, g && s ? a(h) : (s = o = void 0, r);
  }
  function R() {
    c !== void 0 && clearTimeout(c), b = 0, s = d = o = c = void 0;
  }
  function f() {
    return c === void 0 ? r : v(N());
  }
  function C() {
    var h = N(), y = u(h);
    if (s = arguments, o = this, d = h, y) {
      if (c === void 0)
        return p(d);
      if (i)
        return clearTimeout(c), c = setTimeout(m, e), a(d);
    }
    return c === void 0 && (c = setTimeout(m, e)), r;
  }
  return C.cancel = R, C.flush = f, C;
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
var Le = E, Pe = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, De = Le.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, We = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function re(t, e, l) {
  var s, o = {}, n = null, r = null;
  l !== void 0 && (n = "" + l), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (s in e) Ne.call(e, s) && !We.hasOwnProperty(s) && (o[s] = e[s]);
  if (t && t.defaultProps) for (s in e = t.defaultProps, e) o[s] === void 0 && (o[s] = e[s]);
  return {
    $$typeof: Pe,
    type: t,
    key: n,
    ref: r,
    props: o,
    _owner: De.current
  };
}
F.Fragment = Fe;
F.jsx = re;
F.jsxs = re;
ne.exports = F;
var w = ne.exports;
const {
  SvelteComponent: Ae,
  assign: V,
  binding_callbacks: J,
  check_outros: Me,
  children: le,
  claim_element: oe,
  claim_space: Ue,
  component_subscribe: X,
  compute_slots: Be,
  create_slot: He,
  detach: T,
  element: se,
  empty: Y,
  exclude_internal_props: K,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: L,
  safe_not_equal: Je,
  set_custom_element_data: ce,
  space: Xe,
  transition_in: P,
  transition_out: U,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, l;
  const s = (
    /*#slots*/
    t[7].default
  ), o = He(
    s,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = se("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = oe(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = le(e);
      o && o.l(r), r.forEach(T), this.h();
    },
    h() {
      ce(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      L(n, e, r), o && o.m(e, null), t[9](e), l = !0;
    },
    p(n, r) {
      o && o.p && (!l || r & /*$$scope*/
      64) && Ye(
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
        ) : ze(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      l || (P(o, n), l = !0);
    },
    o(n) {
      U(o, n), l = !1;
    },
    d(n) {
      n && T(e), o && o.d(n), t[9](null);
    }
  };
}
function et(t) {
  let e, l, s, o, n = (
    /*$$slots*/
    t[4].default && Q(t)
  );
  return {
    c() {
      e = se("react-portal-target"), l = Xe(), n && n.c(), s = Y(), this.h();
    },
    l(r) {
      e = oe(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), le(e).forEach(T), l = Ue(r), n && n.l(r), s = Y(), this.h();
    },
    h() {
      ce(e, "class", "svelte-1rt0kpf");
    },
    m(r, c) {
      L(r, e, c), t[8](e), L(r, l, c), n && n.m(r, c), L(r, s, c), o = !0;
    },
    p(r, [c]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, c), c & /*$$slots*/
      16 && P(n, 1)) : (n = Q(r), n.c(), P(n, 1), n.m(s.parentNode, s)) : n && (qe(), U(n, 1, 1, () => {
        n = null;
      }), Me());
    },
    i(r) {
      o || (P(n), o = !0);
    },
    o(r) {
      U(n), o = !1;
    },
    d(r) {
      r && (T(e), T(l), T(s)), t[8](null), n && n.d(r);
    }
  };
}
function Z(t) {
  const {
    svelteInit: e,
    ...l
  } = t;
  return l;
}
function tt(t, e, l) {
  let s, o, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const c = Be(n);
  let {
    svelteInit: d
  } = e;
  const b = k(Z(e)), _ = k();
  X(t, _, (f) => l(0, s = f));
  const i = k();
  X(t, i, (f) => l(1, o = f));
  const g = [], a = Qe("$$ms-gr-react-wrapper"), {
    slotKey: p,
    slotIndex: x,
    subSlotIndex: u
  } = ge() || {}, m = d({
    parent: a,
    props: b,
    target: _,
    slot: i,
    slotKey: p,
    slotIndex: x,
    subSlotIndex: u,
    onDestroy(f) {
      g.push(f);
    }
  });
  $e("$$ms-gr-react-wrapper", m), Ke(() => {
    b.set(Z(e));
  }), Ze(() => {
    g.forEach((f) => f());
  });
  function v(f) {
    J[f ? "unshift" : "push"](() => {
      s = f, _.set(s);
    });
  }
  function R(f) {
    J[f ? "unshift" : "push"](() => {
      o = f, i.set(o);
    });
  }
  return t.$$set = (f) => {
    l(17, e = V(V({}, e), K(f))), "svelteInit" in f && l(5, d = f.svelteInit), "$$scope" in f && l(6, r = f.$$scope);
  }, e = K(e), [s, o, _, i, c, d, r, n, v, R];
}
class nt extends Ae {
  constructor(e) {
    super(), Ve(this, e, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const $ = window.ms_globals.rerender, D = window.ms_globals.tree;
function rt(t, e = {}) {
  function l(s) {
    const o = k(), n = new nt({
      ...s,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const c = {
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
          }, d = r.parent ?? D;
          return d.nodes = [...d.nodes, c], $({
            createPortal: W,
            node: D
          }), r.onDestroy(() => {
            d.nodes = d.nodes.filter((b) => b.svelteInstance !== o), $({
              createPortal: W,
              node: D
            });
          }), c;
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
const lt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(t) {
  return t ? Object.keys(t).reduce((e, l) => {
    const s = t[l];
    return e[l] = st(l, s), e;
  }, {}) : {};
}
function st(t, e) {
  return typeof e == "number" && !lt.includes(t) ? e + "px" : e;
}
function B(t) {
  const e = [], l = t.cloneNode(!1);
  if (t._reactElement) {
    const o = E.Children.toArray(t._reactElement.props.children).map((n) => {
      if (E.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: c
        } = B(n.props.el);
        return E.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...E.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = t._reactElement.props.children, e.push(W(E.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: o
    }), l)), {
      clonedElement: l,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: r,
      type: c,
      useCapture: d
    }) => {
      l.addEventListener(c, r, d);
    });
  });
  const s = Array.from(t.childNodes);
  for (let o = 0; o < s.length; o++) {
    const n = s[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: c
      } = B(n);
      e.push(...c), l.appendChild(r);
    } else n.nodeType === 3 && l.appendChild(n.cloneNode());
  }
  return {
    clonedElement: l,
    portals: e
  };
}
function ct(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const O = ue(({
  slot: t,
  clone: e,
  className: l,
  style: s,
  observeAttributes: o
}, n) => {
  const r = de(), [c, d] = fe([]), {
    forceClone: b
  } = be(), _ = b ? !0 : e;
  return me(() => {
    var x;
    if (!r.current || !t)
      return;
    let i = t;
    function g() {
      let u = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (u = i.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), ct(n, u), l && u.classList.add(...l.split(" ")), s) {
        const m = ot(s);
        Object.keys(m).forEach((v) => {
          u.style[v] = m[v];
        });
      }
    }
    let a = null, p = null;
    if (_ && window.MutationObserver) {
      let u = function() {
        var f, C, h;
        (f = r.current) != null && f.contains(i) && ((C = r.current) == null || C.removeChild(i));
        const {
          portals: v,
          clonedElement: R
        } = B(t);
        i = R, d(v), i.style.display = "contents", p && clearTimeout(p), p = setTimeout(() => {
          g();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      u();
      const m = ke(() => {
        u(), a == null || a.disconnect(), a == null || a.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      a = new window.MutationObserver(m), a.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", g(), (x = r.current) == null || x.appendChild(i);
    return () => {
      var u, m;
      i.style.display = "", (u = r.current) != null && u.contains(i) && ((m = r.current) == null || m.removeChild(i)), a == null || a.disconnect();
    };
  }, [t, _, l, s, n, o]), E.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...c);
});
function it(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function at(t, e = !1) {
  try {
    if (we(t))
      return t;
    if (e && !it(t))
      return;
    if (typeof t == "string") {
      let l = t.trim();
      return l.startsWith(";") && (l = l.slice(1)), l.endsWith(";") && (l = l.slice(0, -1)), new Function(`return (...args) => (${l})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function S(t, e) {
  return te(() => at(t, e), [t, e]);
}
function ut(t) {
  return Object.keys(t).reduce((e, l) => (t[l] !== void 0 && (e[l] = t[l]), e), {});
}
const dt = ({
  children: t,
  ...e
}) => /* @__PURE__ */ w.jsx(w.Fragment, {
  children: t(e)
});
function ie(t) {
  return E.createElement(dt, {
    children: t
  });
}
function ae(t, e, l) {
  const s = t.filter(Boolean);
  if (s.length !== 0)
    return s.map((o, n) => {
      var b;
      if (typeof o != "object")
        return e != null && e.fallback ? e.fallback(o) : o;
      const r = {
        ...o.props,
        key: ((b = o.props) == null ? void 0 : b.key) ?? (l ? `${l}-${n}` : `${n}`)
      };
      let c = r;
      Object.keys(o.slots).forEach((_) => {
        if (!o.slots[_] || !(o.slots[_] instanceof Element) && !o.slots[_].el)
          return;
        const i = _.split(".");
        i.forEach((m, v) => {
          c[m] || (c[m] = {}), v !== i.length - 1 && (c = r[m]);
        });
        const g = o.slots[_];
        let a, p, x = (e == null ? void 0 : e.clone) ?? !1, u = e == null ? void 0 : e.forceClone;
        g instanceof Element ? a = g : (a = g.el, p = g.callback, x = g.clone ?? x, u = g.forceClone ?? u), u = u ?? !!p, c[i[i.length - 1]] = a ? p ? (...m) => (p(i[i.length - 1], m), /* @__PURE__ */ w.jsx(M, {
          ...o.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ w.jsx(O, {
            slot: a,
            clone: x
          })
        })) : ie((m) => /* @__PURE__ */ w.jsx(M, {
          ...o.ctx,
          forceClone: u,
          children: /* @__PURE__ */ w.jsx(O, {
            slot: a,
            clone: x,
            ...m
          })
        })) : c[i[i.length - 1]], c = r;
      });
      const d = (e == null ? void 0 : e.children) || "children";
      return o[d] ? r[d] = ae(o[d], e, `${n}`) : e != null && e.children && (r[d] = void 0, Reflect.deleteProperty(r, d)), r;
    });
}
function ee(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? ie((l) => /* @__PURE__ */ w.jsx(M, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ w.jsx(O, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...l
    })
  })) : /* @__PURE__ */ w.jsx(O, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function j({
  key: t,
  slots: e,
  targets: l
}, s) {
  return e[t] ? (...o) => l ? l.map((n, r) => /* @__PURE__ */ w.jsx(E.Fragment, {
    children: ee(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ w.jsx(w.Fragment, {
    children: ee(e[t], {
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
} = pe("antd-tree-tree-nodes"), gt = rt(ft(["default", "treeData"], ({
  slots: t,
  filterTreeNode: e,
  treeData: l,
  draggable: s,
  allowDrop: o,
  onCheck: n,
  onSelect: r,
  onExpand: c,
  children: d,
  directory: b,
  setSlotParams: _,
  onLoadData: i,
  titleRender: g,
  ...a
}) => {
  const p = S(e), x = S(s), u = S(g), m = S(typeof s == "object" ? s.nodeDraggable : void 0), v = S(o), R = b ? z.DirectoryTree : z, {
    items: f
  } = mt(), C = f.treeData.length > 0 ? f.treeData : f.default, h = te(() => ({
    ...a,
    treeData: l || ae(C, {
      clone: !0
    }),
    showLine: t["showLine.showLeafIcon"] ? {
      showLeafIcon: j({
        slots: t,
        setSlotParams: _,
        key: "showLine.showLeafIcon"
      })
    } : a.showLine,
    icon: t.icon ? j({
      slots: t,
      setSlotParams: _,
      key: "icon"
    }) : a.icon,
    switcherLoadingIcon: t.switcherLoadingIcon ? /* @__PURE__ */ w.jsx(O, {
      slot: t.switcherLoadingIcon
    }) : a.switcherLoadingIcon,
    switcherIcon: t.switcherIcon ? j({
      slots: t,
      setSlotParams: _,
      key: "switcherIcon"
    }) : a.switcherIcon,
    titleRender: t.titleRender ? j({
      slots: t,
      setSlotParams: _,
      key: "titleRender"
    }) : u,
    draggable: t["draggable.icon"] || m ? {
      icon: t["draggable.icon"] ? /* @__PURE__ */ w.jsx(O, {
        slot: t["draggable.icon"]
      }) : typeof s == "object" ? s.icon : void 0,
      nodeDraggable: m
    } : x || s,
    loadData: i
  }), [a, l, C, t, _, m, s, u, x, i]);
  return /* @__PURE__ */ w.jsxs(w.Fragment, {
    children: [/* @__PURE__ */ w.jsx("div", {
      style: {
        display: "none"
      },
      children: d
    }), /* @__PURE__ */ w.jsx(R, {
      ...ut(h),
      filterTreeNode: p,
      allowDrop: v,
      onSelect: (y, ...I) => {
        r == null || r(y, ...I);
      },
      onExpand: (y, ...I) => {
        c == null || c(y, ...I);
      },
      onCheck: (y, ...I) => {
        n == null || n(y, ...I);
      }
    })]
  });
}));
export {
  gt as Tree,
  gt as default
};
