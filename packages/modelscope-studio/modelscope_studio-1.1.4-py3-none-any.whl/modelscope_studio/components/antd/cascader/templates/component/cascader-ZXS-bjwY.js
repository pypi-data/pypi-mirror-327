import { i as Ce, a as B, r as be, b as ye, g as Ie, w as F, c as Ee } from "./Index-Cw6xVYJK.js";
const v = window.ms_globals.React, we = window.ms_globals.React.forwardRef, D = window.ms_globals.React.useRef, le = window.ms_globals.React.useState, V = window.ms_globals.React.useEffect, ce = window.ms_globals.React.useMemo, U = window.ms_globals.ReactDOM.createPortal, ve = window.ms_globals.internalContext.useContextPropsContext, H = window.ms_globals.internalContext.ContextPropsProvider, Re = window.ms_globals.antd.Cascader, Se = window.ms_globals.createItemsContext.createItemsContext;
var ke = /\s/;
function je(e) {
  for (var n = e.length; n-- && ke.test(e.charAt(n)); )
    ;
  return n;
}
var Te = /^\s+/;
function Pe(e) {
  return e && e.slice(0, je(e) + 1).replace(Te, "");
}
var X = NaN, Fe = /^[-+]0x[0-9a-f]+$/i, Oe = /^0b[01]+$/i, Le = /^0o[0-7]+$/i, Ne = parseInt;
function Y(e) {
  if (typeof e == "number")
    return e;
  if (Ce(e))
    return X;
  if (B(e)) {
    var n = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = B(n) ? n + "" : n;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Pe(e);
  var o = Oe.test(e);
  return o || Le.test(e) ? Ne(e.slice(2), o ? 2 : 8) : Fe.test(e) ? X : +e;
}
var A = function() {
  return be.Date.now();
}, We = "Expected a function", Ae = Math.max, Me = Math.min;
function De(e, n, o) {
  var c, l, t, r, s, a, w = 0, x = !1, i = !1, p = !0;
  if (typeof e != "function")
    throw new TypeError(We);
  n = Y(n) || 0, B(o) && (x = !!o.leading, i = "maxWait" in o, t = i ? Ae(Y(o.maxWait) || 0, n) : t, p = "trailing" in o ? !!o.trailing : p);
  function u(h) {
    var C = c, k = l;
    return c = l = void 0, w = h, r = e.apply(k, C), r;
  }
  function b(h) {
    return w = h, s = setTimeout(m, n), x ? u(h) : r;
  }
  function g(h) {
    var C = h - a, k = h - w, P = n - C;
    return i ? Me(P, t - k) : P;
  }
  function d(h) {
    var C = h - a, k = h - w;
    return a === void 0 || C >= n || C < 0 || i && k >= t;
  }
  function m() {
    var h = A();
    if (d(h))
      return y(h);
    s = setTimeout(m, g(h));
  }
  function y(h) {
    return s = void 0, p && c ? u(h) : (c = l = void 0, r);
  }
  function S() {
    s !== void 0 && clearTimeout(s), w = 0, c = a = l = s = void 0;
  }
  function f() {
    return s === void 0 ? r : y(A());
  }
  function R() {
    var h = A(), C = d(h);
    if (c = arguments, l = this, a = h, C) {
      if (s === void 0)
        return b(a);
      if (i)
        return clearTimeout(s), s = setTimeout(m, n), u(a);
    }
    return s === void 0 && (s = setTimeout(m, n)), r;
  }
  return R.cancel = S, R.flush = f, R;
}
function Ve(e, n) {
  return ye(e, n);
}
var se = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ue = v, Be = Symbol.for("react.element"), He = Symbol.for("react.fragment"), qe = Object.prototype.hasOwnProperty, ze = Ue.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ge = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ie(e, n, o) {
  var c, l = {}, t = null, r = null;
  o !== void 0 && (t = "" + o), n.key !== void 0 && (t = "" + n.key), n.ref !== void 0 && (r = n.ref);
  for (c in n) qe.call(n, c) && !Ge.hasOwnProperty(c) && (l[c] = n[c]);
  if (e && e.defaultProps) for (c in n = e.defaultProps, n) l[c] === void 0 && (l[c] = n[c]);
  return {
    $$typeof: Be,
    type: e,
    key: t,
    ref: r,
    props: l,
    _owner: ze.current
  };
}
N.Fragment = He;
N.jsx = ie;
N.jsxs = ie;
se.exports = N;
var _ = se.exports;
const {
  SvelteComponent: Je,
  assign: K,
  binding_callbacks: Q,
  check_outros: Xe,
  children: ae,
  claim_element: ue,
  claim_space: Ye,
  component_subscribe: Z,
  compute_slots: Ke,
  create_slot: Qe,
  detach: j,
  element: de,
  empty: $,
  exclude_internal_props: ee,
  get_all_dirty_from_scope: Ze,
  get_slot_changes: $e,
  group_outros: en,
  init: nn,
  insert_hydration: O,
  safe_not_equal: tn,
  set_custom_element_data: fe,
  space: rn,
  transition_in: L,
  transition_out: q,
  update_slot_base: on
} = window.__gradio__svelte__internal, {
  beforeUpdate: ln,
  getContext: cn,
  onDestroy: sn,
  setContext: an
} = window.__gradio__svelte__internal;
function ne(e) {
  let n, o;
  const c = (
    /*#slots*/
    e[7].default
  ), l = Qe(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      n = de("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      n = ue(t, "SVELTE-SLOT", {
        class: !0
      });
      var r = ae(n);
      l && l.l(r), r.forEach(j), this.h();
    },
    h() {
      fe(n, "class", "svelte-1rt0kpf");
    },
    m(t, r) {
      O(t, n, r), l && l.m(n, null), e[9](n), o = !0;
    },
    p(t, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && on(
        l,
        c,
        t,
        /*$$scope*/
        t[6],
        o ? $e(
          c,
          /*$$scope*/
          t[6],
          r,
          null
        ) : Ze(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (L(l, t), o = !0);
    },
    o(t) {
      q(l, t), o = !1;
    },
    d(t) {
      t && j(n), l && l.d(t), e[9](null);
    }
  };
}
function un(e) {
  let n, o, c, l, t = (
    /*$$slots*/
    e[4].default && ne(e)
  );
  return {
    c() {
      n = de("react-portal-target"), o = rn(), t && t.c(), c = $(), this.h();
    },
    l(r) {
      n = ue(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), ae(n).forEach(j), o = Ye(r), t && t.l(r), c = $(), this.h();
    },
    h() {
      fe(n, "class", "svelte-1rt0kpf");
    },
    m(r, s) {
      O(r, n, s), e[8](n), O(r, o, s), t && t.m(r, s), O(r, c, s), l = !0;
    },
    p(r, [s]) {
      /*$$slots*/
      r[4].default ? t ? (t.p(r, s), s & /*$$slots*/
      16 && L(t, 1)) : (t = ne(r), t.c(), L(t, 1), t.m(c.parentNode, c)) : t && (en(), q(t, 1, 1, () => {
        t = null;
      }), Xe());
    },
    i(r) {
      l || (L(t), l = !0);
    },
    o(r) {
      q(t), l = !1;
    },
    d(r) {
      r && (j(n), j(o), j(c)), e[8](null), t && t.d(r);
    }
  };
}
function te(e) {
  const {
    svelteInit: n,
    ...o
  } = e;
  return o;
}
function dn(e, n, o) {
  let c, l, {
    $$slots: t = {},
    $$scope: r
  } = n;
  const s = Ke(t);
  let {
    svelteInit: a
  } = n;
  const w = F(te(n)), x = F();
  Z(e, x, (f) => o(0, c = f));
  const i = F();
  Z(e, i, (f) => o(1, l = f));
  const p = [], u = cn("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: g,
    subSlotIndex: d
  } = Ie() || {}, m = a({
    parent: u,
    props: w,
    target: x,
    slot: i,
    slotKey: b,
    slotIndex: g,
    subSlotIndex: d,
    onDestroy(f) {
      p.push(f);
    }
  });
  an("$$ms-gr-react-wrapper", m), ln(() => {
    w.set(te(n));
  }), sn(() => {
    p.forEach((f) => f());
  });
  function y(f) {
    Q[f ? "unshift" : "push"](() => {
      c = f, x.set(c);
    });
  }
  function S(f) {
    Q[f ? "unshift" : "push"](() => {
      l = f, i.set(l);
    });
  }
  return e.$$set = (f) => {
    o(17, n = K(K({}, n), ee(f))), "svelteInit" in f && o(5, a = f.svelteInit), "$$scope" in f && o(6, r = f.$$scope);
  }, n = ee(n), [c, l, x, i, s, a, r, t, y, S];
}
class fn extends Je {
  constructor(n) {
    super(), nn(this, n, dn, un, tn, {
      svelteInit: 5
    });
  }
}
const re = window.ms_globals.rerender, M = window.ms_globals.tree;
function mn(e, n = {}) {
  function o(c) {
    const l = F(), t = new fn({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const s = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: n.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, a = r.parent ?? M;
          return a.nodes = [...a.nodes, s], re({
            createPortal: U,
            node: M
          }), r.onDestroy(() => {
            a.nodes = a.nodes.filter((w) => w.svelteInstance !== l), re({
              createPortal: U,
              node: M
            });
          }), s;
        },
        ...c.props
      }
    });
    return l.set(t), t;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(o);
    });
  });
}
const hn = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function _n(e) {
  return e ? Object.keys(e).reduce((n, o) => {
    const c = e[o];
    return n[o] = gn(o, c), n;
  }, {}) : {};
}
function gn(e, n) {
  return typeof n == "number" && !hn.includes(e) ? n + "px" : n;
}
function z(e) {
  const n = [], o = e.cloneNode(!1);
  if (e._reactElement) {
    const l = v.Children.toArray(e._reactElement.props.children).map((t) => {
      if (v.isValidElement(t) && t.props.__slot__) {
        const {
          portals: r,
          clonedElement: s
        } = z(t.props.el);
        return v.cloneElement(t, {
          ...t.props,
          el: s,
          children: [...v.Children.toArray(t.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = e._reactElement.props.children, n.push(U(v.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: n
    };
  }
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: r,
      type: s,
      useCapture: a
    }) => {
      o.addEventListener(s, r, a);
    });
  });
  const c = Array.from(e.childNodes);
  for (let l = 0; l < c.length; l++) {
    const t = c[l];
    if (t.nodeType === 1) {
      const {
        clonedElement: r,
        portals: s
      } = z(t);
      n.push(...s), o.appendChild(r);
    } else t.nodeType === 3 && o.appendChild(t.cloneNode());
  }
  return {
    clonedElement: o,
    portals: n
  };
}
function pn(e, n) {
  e && (typeof e == "function" ? e(n) : e.current = n);
}
const I = we(({
  slot: e,
  clone: n,
  className: o,
  style: c,
  observeAttributes: l
}, t) => {
  const r = D(), [s, a] = le([]), {
    forceClone: w
  } = ve(), x = w ? !0 : n;
  return V(() => {
    var g;
    if (!r.current || !e)
      return;
    let i = e;
    function p() {
      let d = i;
      if (i.tagName.toLowerCase() === "svelte-slot" && i.children.length === 1 && i.children[0] && (d = i.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), pn(t, d), o && d.classList.add(...o.split(" ")), c) {
        const m = _n(c);
        Object.keys(m).forEach((y) => {
          d.style[y] = m[y];
        });
      }
    }
    let u = null, b = null;
    if (x && window.MutationObserver) {
      let d = function() {
        var f, R, h;
        (f = r.current) != null && f.contains(i) && ((R = r.current) == null || R.removeChild(i));
        const {
          portals: y,
          clonedElement: S
        } = z(e);
        i = S, a(y), i.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          p();
        }, 50), (h = r.current) == null || h.appendChild(i);
      };
      d();
      const m = De(() => {
        d(), u == null || u.disconnect(), u == null || u.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      u = new window.MutationObserver(m), u.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      i.style.display = "contents", p(), (g = r.current) == null || g.appendChild(i);
    return () => {
      var d, m;
      i.style.display = "", (d = r.current) != null && d.contains(i) && ((m = r.current) == null || m.removeChild(i)), u == null || u.disconnect();
    };
  }, [e, x, o, c, t, l]), v.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...s);
});
function xn(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function wn(e, n = !1) {
  try {
    if (Ee(e))
      return e;
    if (n && !xn(e))
      return;
    if (typeof e == "string") {
      let o = e.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function E(e, n) {
  return ce(() => wn(e, n), [e, n]);
}
function Cn({
  value: e,
  onValueChange: n
}) {
  const [o, c] = le(e), l = D(n);
  l.current = n;
  const t = D(o);
  return t.current = o, V(() => {
    l.current(o);
  }, [o]), V(() => {
    Ve(e, t.current) || c(e);
  }, [e]), [o, c];
}
const bn = ({
  children: e,
  ...n
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: e(n)
});
function me(e) {
  return v.createElement(bn, {
    children: e
  });
}
function he(e, n, o) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((l, t) => {
      var w;
      if (typeof l != "object")
        return n != null && n.fallback ? n.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((w = l.props) == null ? void 0 : w.key) ?? (o ? `${o}-${t}` : `${t}`)
      };
      let s = r;
      Object.keys(l.slots).forEach((x) => {
        if (!l.slots[x] || !(l.slots[x] instanceof Element) && !l.slots[x].el)
          return;
        const i = x.split(".");
        i.forEach((m, y) => {
          s[m] || (s[m] = {}), y !== i.length - 1 && (s = r[m]);
        });
        const p = l.slots[x];
        let u, b, g = (n == null ? void 0 : n.clone) ?? !1, d = n == null ? void 0 : n.forceClone;
        p instanceof Element ? u = p : (u = p.el, b = p.callback, g = p.clone ?? g, d = p.forceClone ?? d), d = d ?? !!b, s[i[i.length - 1]] = u ? b ? (...m) => (b(i[i.length - 1], m), /* @__PURE__ */ _.jsx(H, {
          ...l.ctx,
          params: m,
          forceClone: d,
          children: /* @__PURE__ */ _.jsx(I, {
            slot: u,
            clone: g
          })
        })) : me((m) => /* @__PURE__ */ _.jsx(H, {
          ...l.ctx,
          forceClone: d,
          children: /* @__PURE__ */ _.jsx(I, {
            slot: u,
            clone: g,
            ...m
          })
        })) : s[i[i.length - 1]], s = r;
      });
      const a = (n == null ? void 0 : n.children) || "children";
      return l[a] ? r[a] = he(l[a], n, `${t}`) : n != null && n.children && (r[a] = void 0, Reflect.deleteProperty(r, a)), r;
    });
}
function oe(e, n) {
  return e ? n != null && n.forceClone || n != null && n.params ? me((o) => /* @__PURE__ */ _.jsx(H, {
    forceClone: n == null ? void 0 : n.forceClone,
    params: n == null ? void 0 : n.params,
    children: /* @__PURE__ */ _.jsx(I, {
      slot: e,
      clone: n == null ? void 0 : n.clone,
      ...o
    })
  })) : /* @__PURE__ */ _.jsx(I, {
    slot: e,
    clone: n == null ? void 0 : n.clone
  }) : null;
}
function T({
  key: e,
  slots: n,
  targets: o
}, c) {
  return n[e] ? (...l) => o ? o.map((t, r) => /* @__PURE__ */ _.jsx(v.Fragment, {
    children: oe(t, {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: oe(n[e], {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }) : void 0;
}
const {
  useItems: yn,
  withItemsContextProvider: In,
  ItemHandler: Rn
} = Se("antd-cascader-options");
function En(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Sn = mn(In(["default", "options"], ({
  slots: e,
  children: n,
  onValueChange: o,
  onChange: c,
  displayRender: l,
  elRef: t,
  getPopupContainer: r,
  tagRender: s,
  maxTagPlaceholder: a,
  dropdownRender: w,
  optionRender: x,
  showSearch: i,
  options: p,
  setSlotParams: u,
  onLoadData: b,
  ...g
}) => {
  const d = E(r), m = E(l), y = E(s), S = E(x), f = E(w), R = E(a), h = typeof i == "object" || e["showSearch.render"], C = En(i), k = E(C.filter), P = E(C.render), _e = E(C.sort), [ge, pe] = Cn({
    onValueChange: o,
    value: g.value
  }), {
    items: W
  } = yn(), G = W.options.length > 0 ? W.options : W.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ _.jsx(Re, {
      ...g,
      ref: t,
      value: ge,
      options: ce(() => p || he(G, {
        clone: !0
      }), [p, G]),
      showSearch: h ? {
        ...C,
        filter: k || C.filter,
        render: e["showSearch.render"] ? T({
          slots: e,
          setSlotParams: u,
          key: "showSearch.render"
        }) : P || C.render,
        sort: _e || C.sort
      } : i,
      loadData: b,
      optionRender: S,
      getPopupContainer: d,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(I, {
        slot: e.prefix
      }) : g.prefix,
      dropdownRender: e.dropdownRender ? T({
        slots: e,
        setSlotParams: u,
        key: "dropdownRender"
      }) : f,
      displayRender: e.displayRender ? T({
        slots: e,
        setSlotParams: u,
        key: "displayRender"
      }) : m,
      tagRender: e.tagRender ? T({
        slots: e,
        setSlotParams: u,
        key: "tagRender"
      }) : y,
      onChange: (J, ...xe) => {
        c == null || c(J, ...xe), pe(J);
      },
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(I, {
        slot: e.suffixIcon
      }) : g.suffixIcon,
      expandIcon: e.expandIcon ? /* @__PURE__ */ _.jsx(I, {
        slot: e.expandIcon
      }) : g.expandIcon,
      removeIcon: e.removeIcon ? /* @__PURE__ */ _.jsx(I, {
        slot: e.removeIcon
      }) : g.removeIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ _.jsx(I, {
        slot: e.notFoundContent
      }) : g.notFoundContent,
      maxTagPlaceholder: e.maxTagPlaceholder ? T({
        slots: e,
        setSlotParams: u,
        key: "maxTagPlaceholder"
      }) : R || a,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(I, {
          slot: e["allowClear.clearIcon"]
        })
      } : g.allowClear
    })]
  });
}));
export {
  Sn as Cascader,
  Sn as default
};
