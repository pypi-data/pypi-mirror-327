import { i as me, a as D, r as he, g as _e, w as O, b as ge } from "./Index-CZPL2g4i.js";
const v = window.ms_globals.React, ae = window.ms_globals.React.forwardRef, ue = window.ms_globals.React.useRef, de = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, ee = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, pe = window.ms_globals.internalContext.useContextPropsContext, U = window.ms_globals.internalContext.ContextPropsProvider, xe = window.ms_globals.antd.Select, we = window.ms_globals.createItemsContext.createItemsContext;
var be = /\s/;
function Ie(e) {
  for (var t = e.length; t-- && be.test(e.charAt(t)); )
    ;
  return t;
}
var Ce = /^\s+/;
function ye(e) {
  return e && e.slice(0, Ie(e) + 1).replace(Ce, "");
}
var z = NaN, ve = /^[-+]0x[0-9a-f]+$/i, Ee = /^0b[01]+$/i, Re = /^0o[0-7]+$/i, Se = parseInt;
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
  e = ye(e);
  var o = Ee.test(e);
  return o || Re.test(e) ? Se(e.slice(2), o ? 2 : 8) : ve.test(e) ? z : +e;
}
var W = function() {
  return he.Date.now();
}, ke = "Expected a function", Te = Math.max, Pe = Math.min;
function je(e, t, o) {
  var c, l, n, r, i, u, w = 0, p = !1, s = !1, x = !0;
  if (typeof e != "function")
    throw new TypeError(ke);
  t = G(t) || 0, D(o) && (p = !!o.leading, s = "maxWait" in o, n = s ? Te(G(o.maxWait) || 0, t) : n, x = "trailing" in o ? !!o.trailing : x);
  function a(m) {
    var C = c, R = l;
    return c = l = void 0, w = m, r = e.apply(R, C), r;
  }
  function g(m) {
    return w = m, i = setTimeout(h, t), p ? a(m) : r;
  }
  function b(m) {
    var C = m - u, R = m - w, j = t - C;
    return s ? Pe(j, n - R) : j;
  }
  function d(m) {
    var C = m - u, R = m - w;
    return u === void 0 || C >= t || C < 0 || s && R >= n;
  }
  function h() {
    var m = W();
    if (d(m))
      return I(m);
    i = setTimeout(h, b(m));
  }
  function I(m) {
    return i = void 0, x && c ? a(m) : (c = l = void 0, r);
  }
  function S() {
    i !== void 0 && clearTimeout(i), w = 0, c = u = l = i = void 0;
  }
  function f() {
    return i === void 0 ? r : I(W());
  }
  function E() {
    var m = W(), C = d(m);
    if (c = arguments, l = this, u = m, C) {
      if (i === void 0)
        return g(u);
      if (s)
        return clearTimeout(i), i = setTimeout(h, t), a(u);
    }
    return i === void 0 && (i = setTimeout(h, t)), r;
  }
  return E.cancel = S, E.flush = f, E;
}
var te = {
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
var Oe = v, Fe = Symbol.for("react.element"), Le = Symbol.for("react.fragment"), Ne = Object.prototype.hasOwnProperty, We = Oe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ae = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ne(e, t, o) {
  var c, l = {}, n = null, r = null;
  o !== void 0 && (n = "" + o), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (c in t) Ne.call(t, c) && !Ae.hasOwnProperty(c) && (l[c] = t[c]);
  if (e && e.defaultProps) for (c in t = e.defaultProps, t) l[c] === void 0 && (l[c] = t[c]);
  return {
    $$typeof: Fe,
    type: e,
    key: n,
    ref: r,
    props: l,
    _owner: We.current
  };
}
N.Fragment = Le;
N.jsx = ne;
N.jsxs = ne;
te.exports = N;
var _ = te.exports;
const {
  SvelteComponent: Me,
  assign: q,
  binding_callbacks: V,
  check_outros: De,
  children: re,
  claim_element: le,
  claim_space: Ue,
  component_subscribe: J,
  compute_slots: Be,
  create_slot: He,
  detach: T,
  element: oe,
  empty: X,
  exclude_internal_props: Y,
  get_all_dirty_from_scope: ze,
  get_slot_changes: Ge,
  group_outros: qe,
  init: Ve,
  insert_hydration: F,
  safe_not_equal: Je,
  set_custom_element_data: ce,
  space: Xe,
  transition_in: L,
  transition_out: B,
  update_slot_base: Ye
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: Qe,
  onDestroy: Ze,
  setContext: $e
} = window.__gradio__svelte__internal;
function K(e) {
  let t, o;
  const c = (
    /*#slots*/
    e[7].default
  ), l = He(
    c,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = oe("svelte-slot"), l && l.c(), this.h();
    },
    l(n) {
      t = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = re(t);
      l && l.l(r), r.forEach(T), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      F(n, t, r), l && l.m(t, null), e[9](t), o = !0;
    },
    p(n, r) {
      l && l.p && (!o || r & /*$$scope*/
      64) && Ye(
        l,
        c,
        n,
        /*$$scope*/
        n[6],
        o ? Ge(
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
      o || (L(l, n), o = !0);
    },
    o(n) {
      B(l, n), o = !1;
    },
    d(n) {
      n && T(t), l && l.d(n), e[9](null);
    }
  };
}
function et(e) {
  let t, o, c, l, n = (
    /*$$slots*/
    e[4].default && K(e)
  );
  return {
    c() {
      t = oe("react-portal-target"), o = Xe(), n && n.c(), c = X(), this.h();
    },
    l(r) {
      t = le(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), re(t).forEach(T), o = Ue(r), n && n.l(r), c = X(), this.h();
    },
    h() {
      ce(t, "class", "svelte-1rt0kpf");
    },
    m(r, i) {
      F(r, t, i), e[8](t), F(r, o, i), n && n.m(r, i), F(r, c, i), l = !0;
    },
    p(r, [i]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, i), i & /*$$slots*/
      16 && L(n, 1)) : (n = K(r), n.c(), L(n, 1), n.m(c.parentNode, c)) : n && (qe(), B(n, 1, 1, () => {
        n = null;
      }), De());
    },
    i(r) {
      l || (L(n), l = !0);
    },
    o(r) {
      B(n), l = !1;
    },
    d(r) {
      r && (T(t), T(o), T(c)), e[8](null), n && n.d(r);
    }
  };
}
function Q(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function tt(e, t, o) {
  let c, l, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const i = Be(n);
  let {
    svelteInit: u
  } = t;
  const w = O(Q(t)), p = O();
  J(e, p, (f) => o(0, c = f));
  const s = O();
  J(e, s, (f) => o(1, l = f));
  const x = [], a = Qe("$$ms-gr-react-wrapper"), {
    slotKey: g,
    slotIndex: b,
    subSlotIndex: d
  } = _e() || {}, h = u({
    parent: a,
    props: w,
    target: p,
    slot: s,
    slotKey: g,
    slotIndex: b,
    subSlotIndex: d,
    onDestroy(f) {
      x.push(f);
    }
  });
  $e("$$ms-gr-react-wrapper", h), Ke(() => {
    w.set(Q(t));
  }), Ze(() => {
    x.forEach((f) => f());
  });
  function I(f) {
    V[f ? "unshift" : "push"](() => {
      c = f, p.set(c);
    });
  }
  function S(f) {
    V[f ? "unshift" : "push"](() => {
      l = f, s.set(l);
    });
  }
  return e.$$set = (f) => {
    o(17, t = q(q({}, t), Y(f))), "svelteInit" in f && o(5, u = f.svelteInit), "$$scope" in f && o(6, r = f.$$scope);
  }, t = Y(t), [c, l, p, s, i, u, r, n, I, S];
}
class nt extends Me {
  constructor(t) {
    super(), Ve(this, t, tt, et, Je, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, A = window.ms_globals.tree;
function rt(e, t = {}) {
  function o(c) {
    const l = O(), n = new nt({
      ...c,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: e,
            props: r.props,
            slot: r.slot,
            target: r.target,
            slotIndex: r.slotIndex,
            subSlotIndex: r.subSlotIndex,
            ignore: t.ignore,
            slotKey: r.slotKey,
            nodes: []
          }, u = r.parent ?? A;
          return u.nodes = [...u.nodes, i], Z({
            createPortal: M,
            node: A
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((w) => w.svelteInstance !== l), Z({
              createPortal: M,
              node: A
            });
          }), i;
        },
        ...c.props
      }
    });
    return l.set(n), n;
  }
  return new Promise((c) => {
    window.ms_globals.initializePromise.then(() => {
      c(o);
    });
  });
}
const lt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, o) => {
    const c = e[o];
    return t[o] = ct(o, c), t;
  }, {}) : {};
}
function ct(e, t) {
  return typeof t == "number" && !lt.includes(e) ? t + "px" : t;
}
function H(e) {
  const t = [], o = e.cloneNode(!1);
  if (e._reactElement) {
    const l = v.Children.toArray(e._reactElement.props.children).map((n) => {
      if (v.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: i
        } = H(n.props.el);
        return v.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...v.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return l.originalChildren = e._reactElement.props.children, t.push(M(v.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: l
    }), o)), {
      clonedElement: o,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((l) => {
    e.getEventListeners(l).forEach(({
      listener: r,
      type: i,
      useCapture: u
    }) => {
      o.addEventListener(i, r, u);
    });
  });
  const c = Array.from(e.childNodes);
  for (let l = 0; l < c.length; l++) {
    const n = c[l];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: i
      } = H(n);
      t.push(...i), o.appendChild(r);
    } else n.nodeType === 3 && o.appendChild(n.cloneNode());
  }
  return {
    clonedElement: o,
    portals: t
  };
}
function it(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const y = ae(({
  slot: e,
  clone: t,
  className: o,
  style: c,
  observeAttributes: l
}, n) => {
  const r = ue(), [i, u] = de([]), {
    forceClone: w
  } = pe(), p = w ? !0 : t;
  return fe(() => {
    var b;
    if (!r.current || !e)
      return;
    let s = e;
    function x() {
      let d = s;
      if (s.tagName.toLowerCase() === "svelte-slot" && s.children.length === 1 && s.children[0] && (d = s.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), it(n, d), o && d.classList.add(...o.split(" ")), c) {
        const h = ot(c);
        Object.keys(h).forEach((I) => {
          d.style[I] = h[I];
        });
      }
    }
    let a = null, g = null;
    if (p && window.MutationObserver) {
      let d = function() {
        var f, E, m;
        (f = r.current) != null && f.contains(s) && ((E = r.current) == null || E.removeChild(s));
        const {
          portals: I,
          clonedElement: S
        } = H(e);
        s = S, u(I), s.style.display = "contents", g && clearTimeout(g), g = setTimeout(() => {
          x();
        }, 50), (m = r.current) == null || m.appendChild(s);
      };
      d();
      const h = je(() => {
        d(), a == null || a.disconnect(), a == null || a.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: l
        });
      }, 50);
      a = new window.MutationObserver(h), a.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      s.style.display = "contents", x(), (b = r.current) == null || b.appendChild(s);
    return () => {
      var d, h;
      s.style.display = "", (d = r.current) != null && d.contains(s) && ((h = r.current) == null || h.removeChild(s)), a == null || a.disconnect();
    };
  }, [e, p, o, c, n, l]), v.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...i);
});
function st(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function at(e, t = !1) {
  try {
    if (ge(e))
      return e;
    if (t && !st(e))
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
function k(e, t) {
  return ee(() => at(e, t), [e, t]);
}
const ut = ({
  children: e,
  ...t
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: e(t)
});
function ie(e) {
  return v.createElement(ut, {
    children: e
  });
}
function se(e, t, o) {
  const c = e.filter(Boolean);
  if (c.length !== 0)
    return c.map((l, n) => {
      var w;
      if (typeof l != "object")
        return t != null && t.fallback ? t.fallback(l) : l;
      const r = {
        ...l.props,
        key: ((w = l.props) == null ? void 0 : w.key) ?? (o ? `${o}-${n}` : `${n}`)
      };
      let i = r;
      Object.keys(l.slots).forEach((p) => {
        if (!l.slots[p] || !(l.slots[p] instanceof Element) && !l.slots[p].el)
          return;
        const s = p.split(".");
        s.forEach((h, I) => {
          i[h] || (i[h] = {}), I !== s.length - 1 && (i = r[h]);
        });
        const x = l.slots[p];
        let a, g, b = (t == null ? void 0 : t.clone) ?? !1, d = t == null ? void 0 : t.forceClone;
        x instanceof Element ? a = x : (a = x.el, g = x.callback, b = x.clone ?? b, d = x.forceClone ?? d), d = d ?? !!g, i[s[s.length - 1]] = a ? g ? (...h) => (g(s[s.length - 1], h), /* @__PURE__ */ _.jsx(U, {
          ...l.ctx,
          params: h,
          forceClone: d,
          children: /* @__PURE__ */ _.jsx(y, {
            slot: a,
            clone: b
          })
        })) : ie((h) => /* @__PURE__ */ _.jsx(U, {
          ...l.ctx,
          forceClone: d,
          children: /* @__PURE__ */ _.jsx(y, {
            slot: a,
            clone: b,
            ...h
          })
        })) : i[s[s.length - 1]], i = r;
      });
      const u = (t == null ? void 0 : t.children) || "children";
      return l[u] ? r[u] = se(l[u], t, `${n}`) : t != null && t.children && (r[u] = void 0, Reflect.deleteProperty(r, u)), r;
    });
}
function $(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ie((o) => /* @__PURE__ */ _.jsx(U, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ _.jsx(y, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...o
    })
  })) : /* @__PURE__ */ _.jsx(y, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function P({
  key: e,
  slots: t,
  targets: o
}, c) {
  return t[e] ? (...l) => o ? o.map((n, r) => /* @__PURE__ */ _.jsx(v.Fragment, {
    children: $(n, {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: $(t[e], {
      clone: !0,
      params: l,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: dt,
  useItems: ft,
  ItemHandler: ht
} = we("antd-select-options"), _t = rt(dt(["options", "default"], ({
  slots: e,
  children: t,
  onValueChange: o,
  filterOption: c,
  onChange: l,
  options: n,
  getPopupContainer: r,
  dropdownRender: i,
  optionRender: u,
  tagRender: w,
  labelRender: p,
  filterSort: s,
  elRef: x,
  setSlotParams: a,
  ...g
}) => {
  const b = k(r), d = k(c), h = k(i), I = k(s), S = k(u), f = k(w), E = k(p), {
    items: m
  } = ft(), C = m.options.length > 0 ? m.options : m.default;
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ _.jsx(xe, {
      ...g,
      ref: x,
      options: ee(() => n || se(C, {
        children: "options",
        clone: !0
      }), [C, n]),
      onChange: (R, ...j) => {
        l == null || l(R, ...j), o(R);
      },
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(y, {
          slot: e["allowClear.clearIcon"]
        })
      } : g.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(y, {
        slot: e.prefix
      }) : g.prefix,
      removeIcon: e.removeIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.removeIcon
      }) : g.removeIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.suffixIcon
      }) : g.suffixIcon,
      notFoundContent: e.notFoundContent ? /* @__PURE__ */ _.jsx(y, {
        slot: e.notFoundContent
      }) : g.notFoundContent,
      menuItemSelectedIcon: e.menuItemSelectedIcon ? /* @__PURE__ */ _.jsx(y, {
        slot: e.menuItemSelectedIcon
      }) : g.menuItemSelectedIcon,
      filterOption: d || c,
      maxTagPlaceholder: e.maxTagPlaceholder ? P({
        slots: e,
        setSlotParams: a,
        key: "maxTagPlaceholder"
      }) : g.maxTagPlaceholder,
      getPopupContainer: b,
      dropdownRender: e.dropdownRender ? P({
        slots: e,
        setSlotParams: a,
        key: "dropdownRender"
      }) : h,
      optionRender: e.optionRender ? P({
        slots: e,
        setSlotParams: a,
        key: "optionRender"
      }) : S,
      tagRender: e.tagRender ? P({
        slots: e,
        setSlotParams: a,
        key: "tagRender"
      }) : f,
      labelRender: e.labelRender ? P({
        slots: e,
        setSlotParams: a,
        key: "labelRender"
      }) : E,
      filterSort: I
    })]
  });
}));
export {
  _t as Select,
  _t as default
};
