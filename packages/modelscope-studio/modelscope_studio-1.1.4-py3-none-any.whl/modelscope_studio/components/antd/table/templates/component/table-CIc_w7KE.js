import { i as ke, a as X, r as je, g as Ne, w as M, b as Le } from "./Index-DyvOTWQa.js";
const v = window.ms_globals.React, Oe = window.ms_globals.React.forwardRef, Re = window.ms_globals.React.useRef, Te = window.ms_globals.React.useState, Pe = window.ms_globals.React.useEffect, A = window.ms_globals.React.useMemo, Q = window.ms_globals.ReactDOM.createPortal, Fe = window.ms_globals.internalContext.useContextPropsContext, z = window.ms_globals.internalContext.ContextPropsProvider, j = window.ms_globals.antd.Table, D = window.ms_globals.createItemsContext.createItemsContext;
var Ae = /\s/;
function Me(t) {
  for (var e = t.length; e-- && Ae.test(t.charAt(e)); )
    ;
  return e;
}
var Ue = /^\s+/;
function We(t) {
  return t && t.slice(0, Me(t) + 1).replace(Ue, "");
}
var Y = NaN, He = /^[-+]0x[0-9a-f]+$/i, De = /^0b[01]+$/i, Be = /^0o[0-7]+$/i, Ge = parseInt;
function Z(t) {
  if (typeof t == "number")
    return t;
  if (ke(t))
    return Y;
  if (X(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = X(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = We(t);
  var o = De.test(t);
  return o || Be.test(t) ? Ge(t.slice(2), o ? 2 : 8) : He.test(t) ? Y : +t;
}
var G = function() {
  return je.Date.now();
}, Je = "Expected a function", Qe = Math.max, Xe = Math.min;
function ze(t, e, o) {
  var l, i, n, r, s, u, _ = 0, g = !1, c = !1, C = !0;
  if (typeof t != "function")
    throw new TypeError(Je);
  e = Z(e) || 0, X(o) && (g = !!o.leading, c = "maxWait" in o, n = c ? Qe(Z(o.maxWait) || 0, e) : n, C = "trailing" in o ? !!o.trailing : C);
  function d(h) {
    var y = l, T = i;
    return l = i = void 0, _ = h, r = t.apply(T, y), r;
  }
  function w(h) {
    return _ = h, s = setTimeout(m, e), g ? d(h) : r;
  }
  function x(h) {
    var y = h - u, T = h - _, P = e - y;
    return c ? Xe(P, n - T) : P;
  }
  function a(h) {
    var y = h - u, T = h - _;
    return u === void 0 || y >= e || y < 0 || c && T >= n;
  }
  function m() {
    var h = G();
    if (a(h))
      return b(h);
    s = setTimeout(m, x(h));
  }
  function b(h) {
    return s = void 0, C && l ? d(h) : (l = i = void 0, r);
  }
  function S() {
    s !== void 0 && clearTimeout(s), _ = 0, l = u = i = s = void 0;
  }
  function f() {
    return s === void 0 ? r : b(G());
  }
  function O() {
    var h = G(), y = a(h);
    if (l = arguments, i = this, u = h, y) {
      if (s === void 0)
        return w(u);
      if (c)
        return clearTimeout(s), s = setTimeout(m, e), d(u);
    }
    return s === void 0 && (s = setTimeout(m, e)), r;
  }
  return O.cancel = S, O.flush = f, O;
}
var ce = {
  exports: {}
}, B = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var qe = v, Ve = Symbol.for("react.element"), Ke = Symbol.for("react.fragment"), Ye = Object.prototype.hasOwnProperty, Ze = qe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $e = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ae(t, e, o) {
  var l, i = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (r = e.ref);
  for (l in e) Ye.call(e, l) && !$e.hasOwnProperty(l) && (i[l] = e[l]);
  if (t && t.defaultProps) for (l in e = t.defaultProps, e) i[l] === void 0 && (i[l] = e[l]);
  return {
    $$typeof: Ve,
    type: t,
    key: n,
    ref: r,
    props: i,
    _owner: Ze.current
  };
}
B.Fragment = Ke;
B.jsx = ae;
B.jsxs = ae;
ce.exports = B;
var p = ce.exports;
const {
  SvelteComponent: et,
  assign: $,
  binding_callbacks: ee,
  check_outros: tt,
  children: ue,
  claim_element: de,
  claim_space: nt,
  component_subscribe: te,
  compute_slots: rt,
  create_slot: ot,
  detach: k,
  element: fe,
  empty: ne,
  exclude_internal_props: re,
  get_all_dirty_from_scope: it,
  get_slot_changes: lt,
  group_outros: st,
  init: ct,
  insert_hydration: U,
  safe_not_equal: at,
  set_custom_element_data: me,
  space: ut,
  transition_in: W,
  transition_out: q,
  update_slot_base: dt
} = window.__gradio__svelte__internal, {
  beforeUpdate: ft,
  getContext: mt,
  onDestroy: ht,
  setContext: pt
} = window.__gradio__svelte__internal;
function oe(t) {
  let e, o;
  const l = (
    /*#slots*/
    t[7].default
  ), i = ot(
    l,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = fe("svelte-slot"), i && i.c(), this.h();
    },
    l(n) {
      e = de(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = ue(e);
      i && i.l(r), r.forEach(k), this.h();
    },
    h() {
      me(e, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      U(n, e, r), i && i.m(e, null), t[9](e), o = !0;
    },
    p(n, r) {
      i && i.p && (!o || r & /*$$scope*/
      64) && dt(
        i,
        l,
        n,
        /*$$scope*/
        n[6],
        o ? lt(
          l,
          /*$$scope*/
          n[6],
          r,
          null
        ) : it(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      o || (W(i, n), o = !0);
    },
    o(n) {
      q(i, n), o = !1;
    },
    d(n) {
      n && k(e), i && i.d(n), t[9](null);
    }
  };
}
function gt(t) {
  let e, o, l, i, n = (
    /*$$slots*/
    t[4].default && oe(t)
  );
  return {
    c() {
      e = fe("react-portal-target"), o = ut(), n && n.c(), l = ne(), this.h();
    },
    l(r) {
      e = de(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ue(e).forEach(k), o = nt(r), n && n.l(r), l = ne(), this.h();
    },
    h() {
      me(e, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      U(r, e, s), t[8](e), U(r, o, s), n && n.m(r, s), U(r, l, s), i = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, s), s & /*$$slots*/
      16 && W(n, 1)) : (n = oe(r), n.c(), W(n, 1), n.m(l.parentNode, l)) : n && (st(), q(n, 1, 1, () => {
        n = null;
      }), tt());
    },
    i(r) {
      i || (W(n), i = !0);
    },
    o(r) {
      q(n), i = !1;
    },
    d(r) {
      r && (k(e), k(o), k(l)), t[8](null), n && n.d(r);
    }
  };
}
function ie(t) {
  const {
    svelteInit: e,
    ...o
  } = t;
  return o;
}
function _t(t, e, o) {
  let l, i, {
    $$slots: n = {},
    $$scope: r
  } = e;
  const s = rt(n);
  let {
    svelteInit: u
  } = e;
  const _ = M(ie(e)), g = M();
  te(t, g, (f) => o(0, l = f));
  const c = M();
  te(t, c, (f) => o(1, i = f));
  const C = [], d = mt("$$ms-gr-react-wrapper"), {
    slotKey: w,
    slotIndex: x,
    subSlotIndex: a
  } = Ne() || {}, m = u({
    parent: d,
    props: _,
    target: g,
    slot: c,
    slotKey: w,
    slotIndex: x,
    subSlotIndex: a,
    onDestroy(f) {
      C.push(f);
    }
  });
  pt("$$ms-gr-react-wrapper", m), ft(() => {
    _.set(ie(e));
  }), ht(() => {
    C.forEach((f) => f());
  });
  function b(f) {
    ee[f ? "unshift" : "push"](() => {
      l = f, g.set(l);
    });
  }
  function S(f) {
    ee[f ? "unshift" : "push"](() => {
      i = f, c.set(i);
    });
  }
  return t.$$set = (f) => {
    o(17, e = $($({}, e), re(f))), "svelteInit" in f && o(5, u = f.svelteInit), "$$scope" in f && o(6, r = f.$$scope);
  }, e = re(e), [l, i, g, c, s, u, r, n, b, S];
}
class Ct extends et {
  constructor(e) {
    super(), ct(this, e, _t, gt, at, {
      svelteInit: 5
    });
  }
}
const le = window.ms_globals.rerender, J = window.ms_globals.tree;
function wt(t, e = {}) {
  function o(l) {
    const i = M(), n = new Ct({
      ...l,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: t,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: e.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, u = r.parent ?? J;
          return u.nodes = [...u.nodes, s], le({
            createPortal: Q,
            node: J
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((_) => _.svelteInstance !== i), le({
              createPortal: Q,
              node: J
            });
          }), s;
        },
        ...l.props
      }
    });
    return i.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(o);
    });
  });
}
const bt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function xt(t) {
  return t ? Object.keys(t).reduce((e, o) => {
    const l = t[o];
    return e[o] = Et(o, l), e;
  }, {}) : {};
}
function Et(t, e) {
  return typeof e == "number" && !bt.includes(t) ? e + "px" : e;
}
function V(t) {
  const e = [], o = t.cloneNode(!1);
  if (t._reactElement) {
    const i = v.Children.toArray(t._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = V(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: s,
          children: [...v.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return i.originalChildren = t._reactElement.props.children, e.push(Q(v.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: i
    }), o)), {
      clonedElement: o,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((i) => {
    t.getEventListeners(i).forEach(({
      listener: r,
      type: s,
      useCapture: u
    }) => {
      o.addEventListener(s, r, u);
    });
  });
  const l = Array.from(t.childNodes);
  for (let i = 0; i < l.length; i++) {
    const n = l[i];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = V(n);
      e.push(...s), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: e
  };
}
function yt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const R = Oe(({
  slot: t,
  clone: e,
  className: o,
  style: l,
  observeAttributes: i
}, n) => {
  const r = Re(), [s, u] = Te([]), {
    forceClone: _
  } = Fe(), g = _ ? !0 : e;
  return Pe(() => {
    var x;
    if (!r.current || !t)
      return;
    let c = t;
    function C() {
      let a = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (a = c.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), yt(n, a), o && a.classList.add(...o.split(" ")), l) {
        const m = xt(l);
        Object.keys(m).forEach((b) => {
          a.style[b] = m[b];
        });
      }
    }
    let d = null, w = null;
    if (g && window.MutationObserver) {
      let a = function() {
        var f, O, h;
        (f = r.current) != null && f.contains(c) && ((O = r.current) == null || O.removeChild(c));
        const {
          portals: b,
          clonedElement: S
        } = V(t);
        c = S, u(b), c.style.display = "contents", w && clearTimeout(w), w = setTimeout(() => {
          C();
        }, 50), (h = r.current) == null || h.appendChild(c);
      };
      a();
      const m = ze(() => {
        a(), d == null || d.disconnect(), d == null || d.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", C(), (x = r.current) == null || x.appendChild(c);
    return () => {
      var a, m;
      c.style.display = "", (a = r.current) != null && a.contains(c) && ((m = r.current) == null || m.removeChild(c)), d == null || d.disconnect();
    };
  }, [t, g, o, l, n, i]), v.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function It(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function vt(t, e = !1) {
  try {
    if (Le(t))
      return t;
    if (e && !It(t))
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
function I(t, e) {
  return A(() => vt(t, e), [t, e]);
}
function St(t) {
  return Object.keys(t).reduce((e, o) => (t[o] !== void 0 && (e[o] = t[o]), e), {});
}
const Ot = ({
  children: t,
  ...e
}) => /* @__PURE__ */ p.jsx(p.Fragment, {
  children: t(e)
});
function he(t) {
  return v.createElement(Ot, {
    children: t
  });
}
function H(t, e, o) {
  const l = t.filter(Boolean);
  if (l.length !== 0)
    return l.map((i, n) => {
      var _;
      if (typeof i != "object")
        return e != null && e.fallback ? e.fallback(i) : i;
      const r = {
        ...i.props,
        key: ((_ = i.props) == null ? void 0 : _.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let s = r;
      Object.keys(i.slots).forEach((g) => {
        if (!i.slots[g] || !(i.slots[g] instanceof Element) && !i.slots[g].el)
          return;
        const c = g.split(".");
        c.forEach((m, b) => {
          s[m] || (s[m] = {}), b !== c.length - 1 && (s = r[m]);
        });
        const C = i.slots[g];
        let d, w, x = (e == null ? void 0 : e.clone) ?? !1, a = e == null ? void 0 : e.forceClone;
        C instanceof Element ? d = C : (d = C.el, w = C.callback, x = C.clone ?? x, a = C.forceClone ?? a), a = a ?? !!w, s[c[c.length - 1]] = d ? w ? (...m) => (w(c[c.length - 1], m), /* @__PURE__ */ p.jsx(z, {
          ...i.ctx,
          params: m,
          forceClone: a,
          children: /* @__PURE__ */ p.jsx(R, {
            slot: d,
            clone: x
          })
        })) : he((m) => /* @__PURE__ */ p.jsx(z, {
          ...i.ctx,
          forceClone: a,
          children: /* @__PURE__ */ p.jsx(R, {
            slot: d,
            clone: x,
            ...m
          })
        })) : s[c[c.length - 1]], s = r;
      });
      const u = (e == null ? void 0 : e.children) || "children";
      return i[u] ? r[u] = H(i[u], e, `${n}`) : e != null && e.children && (r[u] = void 0, Reflect.deleteProperty(r, u)), r;
    });
}
function se(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? he((o) => /* @__PURE__ */ p.jsx(z, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ p.jsx(R, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...o
    })
  })) : /* @__PURE__ */ p.jsx(R, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function L({
  key: t,
  slots: e,
  targets: o
}, l) {
  return e[t] ? (...i) => o ? o.map((n, r) => /* @__PURE__ */ p.jsx(v.Fragment, {
    children: se(n, {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ p.jsx(p.Fragment, {
    children: se(e[t], {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }) : void 0;
}
const {
  useItems: Rt,
  withItemsContextProvider: Tt,
  ItemHandler: Ft
} = D("antd-table-columns");
D("antd-table-row-selection-selections");
const {
  useItems: Pt,
  withItemsContextProvider: kt,
  ItemHandler: At
} = D("antd-table-row-selection"), {
  useItems: jt,
  withItemsContextProvider: Nt,
  ItemHandler: Mt
} = D("antd-table-expandable");
function F(t) {
  return typeof t == "object" && t !== null ? t : {};
}
const Ut = wt(kt(["rowSelection"], Nt(["expandable"], Tt(["default"], ({
  children: t,
  slots: e,
  columns: o,
  getPopupContainer: l,
  pagination: i,
  loading: n,
  rowKey: r,
  rowClassName: s,
  summary: u,
  rowSelection: _,
  expandable: g,
  sticky: c,
  footer: C,
  showSorterTooltip: d,
  onRow: w,
  onHeaderRow: x,
  setSlotParams: a,
  ...m
}) => {
  const {
    items: {
      default: b
    }
  } = Rt(), {
    items: {
      expandable: S
    }
  } = jt(), {
    items: {
      rowSelection: f
    }
  } = Pt(), O = I(l), h = e["loading.tip"] || e["loading.indicator"], y = F(n), T = e["pagination.showQuickJumper.goButton"] || e["pagination.itemRender"], P = F(i), pe = I(P.showTotal), ge = I(s), _e = I(r, !0), Ce = e["showSorterTooltip.title"] || typeof d == "object", N = F(d), we = I(N.afterOpenChange), be = I(N.getPopupContainer), xe = typeof c == "object", K = F(c), Ee = I(K.getContainer), ye = I(w), Ie = I(x), ve = I(u), Se = I(C);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(j, {
      ...m,
      columns: A(() => (o == null ? void 0 : o.map((E) => E === "EXPAND_COLUMN" ? j.EXPAND_COLUMN : E === "SELECTION_COLUMN" ? j.SELECTION_COLUMN : E)) || H(b, {
        fallback: (E) => E === "EXPAND_COLUMN" ? j.EXPAND_COLUMN : E === "SELECTION_COLUMN" ? j.SELECTION_COLUMN : E
      }), [b, o]),
      onRow: ye,
      onHeaderRow: Ie,
      summary: e.summary ? L({
        slots: e,
        setSlotParams: a,
        key: "summary"
      }) : ve,
      rowSelection: A(() => {
        var E;
        return _ || ((E = H(f)) == null ? void 0 : E[0]);
      }, [_, f]),
      expandable: A(() => {
        var E;
        return g || ((E = H(S)) == null ? void 0 : E[0]);
      }, [g, S]),
      rowClassName: ge,
      rowKey: _e || r,
      sticky: xe ? {
        ...K,
        getContainer: Ee
      } : c,
      showSorterTooltip: Ce ? {
        ...N,
        afterOpenChange: we,
        getPopupContainer: be,
        title: e["showSorterTooltip.title"] ? /* @__PURE__ */ p.jsx(R, {
          slot: e["showSorterTooltip.title"]
        }) : N.title
      } : d,
      pagination: T ? St({
        ...P,
        showTotal: pe,
        showQuickJumper: e["pagination.showQuickJumper.goButton"] ? {
          goButton: /* @__PURE__ */ p.jsx(R, {
            slot: e["pagination.showQuickJumper.goButton"]
          })
        } : P.showQuickJumper,
        itemRender: e["pagination.itemRender"] ? L({
          slots: e,
          setSlotParams: a,
          key: "pagination.itemRender"
        }) : P.itemRender
      }) : i,
      getPopupContainer: O,
      loading: h ? {
        ...y,
        tip: e["loading.tip"] ? /* @__PURE__ */ p.jsx(R, {
          slot: e["loading.tip"]
        }) : y.tip,
        indicator: e["loading.indicator"] ? /* @__PURE__ */ p.jsx(R, {
          slot: e["loading.indicator"]
        }) : y.indicator
      } : n,
      footer: e.footer ? L({
        slots: e,
        setSlotParams: a,
        key: "footer"
      }) : Se,
      title: e.title ? L({
        slots: e,
        setSlotParams: a,
        key: "title"
      }) : m.title
    })]
  });
}))));
export {
  Ut as Table,
  Ut as default
};
