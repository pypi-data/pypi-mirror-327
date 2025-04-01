import { i as ue, a as B, r as de, b as fe, g as me, w as O, c as _e } from "./Index-B2IEVs8w.js";
const b = window.ms_globals.React, ce = window.ms_globals.React.forwardRef, N = window.ms_globals.React.useRef, te = window.ms_globals.React.useState, W = window.ms_globals.React.useEffect, ne = window.ms_globals.React.useMemo, M = window.ms_globals.ReactDOM.createPortal, he = window.ms_globals.internalContext.useContextPropsContext, pe = window.ms_globals.internalContext.ContextPropsProvider, ge = window.ms_globals.antd.Input;
var we = /\s/;
function xe(e) {
  for (var t = e.length; t-- && we.test(e.charAt(t)); )
    ;
  return t;
}
var ye = /^\s+/;
function be(e) {
  return e && e.slice(0, xe(e) + 1).replace(ye, "");
}
var q = NaN, Ee = /^[-+]0x[0-9a-f]+$/i, ve = /^0b[01]+$/i, Ce = /^0o[0-7]+$/i, Ie = parseInt;
function z(e) {
  if (typeof e == "number")
    return e;
  if (ue(e))
    return q;
  if (B(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = B(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = be(e);
  var n = ve.test(e);
  return n || Ce.test(e) ? Ie(e.slice(2), n ? 2 : 8) : Ee.test(e) ? q : +e;
}
var L = function() {
  return de.Date.now();
}, Re = "Expected a function", Se = Math.max, Pe = Math.min;
function Te(e, t, n) {
  var i, s, r, o, l, u, m = 0, g = !1, a = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Re);
  t = z(t) || 0, B(n) && (g = !!n.leading, a = "maxWait" in n, r = a ? Se(z(n.maxWait) || 0, t) : r, w = "trailing" in n ? !!n.trailing : w);
  function _(d) {
    var v = i, P = s;
    return i = s = void 0, m = d, o = e.apply(P, v), o;
  }
  function x(d) {
    return m = d, l = setTimeout(h, t), g ? _(d) : o;
  }
  function E(d) {
    var v = d - u, P = d - m, V = t - v;
    return a ? Pe(V, r - P) : V;
  }
  function f(d) {
    var v = d - u, P = d - m;
    return u === void 0 || v >= t || v < 0 || a && P >= r;
  }
  function h() {
    var d = L();
    if (f(d))
      return y(d);
    l = setTimeout(h, E(d));
  }
  function y(d) {
    return l = void 0, w && i ? _(d) : (i = s = void 0, o);
  }
  function S() {
    l !== void 0 && clearTimeout(l), m = 0, i = u = s = l = void 0;
  }
  function c() {
    return l === void 0 ? o : y(L());
  }
  function I() {
    var d = L(), v = f(d);
    if (i = arguments, s = this, u = d, v) {
      if (l === void 0)
        return x(u);
      if (a)
        return clearTimeout(l), l = setTimeout(h, t), _(u);
    }
    return l === void 0 && (l = setTimeout(h, t)), o;
  }
  return I.cancel = S, I.flush = c, I;
}
function Oe(e, t) {
  return fe(e, t);
}
var re = {
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
var je = b, ke = Symbol.for("react.element"), Fe = Symbol.for("react.fragment"), Le = Object.prototype.hasOwnProperty, Ae = je.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ne = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function oe(e, t, n) {
  var i, s = {}, r = null, o = null;
  n !== void 0 && (r = "" + n), t.key !== void 0 && (r = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (i in t) Le.call(t, i) && !Ne.hasOwnProperty(i) && (s[i] = t[i]);
  if (e && e.defaultProps) for (i in t = e.defaultProps, t) s[i] === void 0 && (s[i] = t[i]);
  return {
    $$typeof: ke,
    type: e,
    key: r,
    ref: o,
    props: s,
    _owner: Ae.current
  };
}
F.Fragment = Fe;
F.jsx = oe;
F.jsxs = oe;
re.exports = F;
var p = re.exports;
const {
  SvelteComponent: We,
  assign: G,
  binding_callbacks: H,
  check_outros: Me,
  children: se,
  claim_element: ie,
  claim_space: Be,
  component_subscribe: K,
  compute_slots: De,
  create_slot: Ue,
  detach: R,
  element: le,
  empty: J,
  exclude_internal_props: X,
  get_all_dirty_from_scope: Ve,
  get_slot_changes: qe,
  group_outros: ze,
  init: Ge,
  insert_hydration: j,
  safe_not_equal: He,
  set_custom_element_data: ae,
  space: Ke,
  transition_in: k,
  transition_out: D,
  update_slot_base: Je
} = window.__gradio__svelte__internal, {
  beforeUpdate: Xe,
  getContext: Ye,
  onDestroy: Qe,
  setContext: Ze
} = window.__gradio__svelte__internal;
function Y(e) {
  let t, n;
  const i = (
    /*#slots*/
    e[7].default
  ), s = Ue(
    i,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = le("svelte-slot"), s && s.c(), this.h();
    },
    l(r) {
      t = ie(r, "SVELTE-SLOT", {
        class: !0
      });
      var o = se(t);
      s && s.l(o), o.forEach(R), this.h();
    },
    h() {
      ae(t, "class", "svelte-1rt0kpf");
    },
    m(r, o) {
      j(r, t, o), s && s.m(t, null), e[9](t), n = !0;
    },
    p(r, o) {
      s && s.p && (!n || o & /*$$scope*/
      64) && Je(
        s,
        i,
        r,
        /*$$scope*/
        r[6],
        n ? qe(
          i,
          /*$$scope*/
          r[6],
          o,
          null
        ) : Ve(
          /*$$scope*/
          r[6]
        ),
        null
      );
    },
    i(r) {
      n || (k(s, r), n = !0);
    },
    o(r) {
      D(s, r), n = !1;
    },
    d(r) {
      r && R(t), s && s.d(r), e[9](null);
    }
  };
}
function $e(e) {
  let t, n, i, s, r = (
    /*$$slots*/
    e[4].default && Y(e)
  );
  return {
    c() {
      t = le("react-portal-target"), n = Ke(), r && r.c(), i = J(), this.h();
    },
    l(o) {
      t = ie(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), se(t).forEach(R), n = Be(o), r && r.l(o), i = J(), this.h();
    },
    h() {
      ae(t, "class", "svelte-1rt0kpf");
    },
    m(o, l) {
      j(o, t, l), e[8](t), j(o, n, l), r && r.m(o, l), j(o, i, l), s = !0;
    },
    p(o, [l]) {
      /*$$slots*/
      o[4].default ? r ? (r.p(o, l), l & /*$$slots*/
      16 && k(r, 1)) : (r = Y(o), r.c(), k(r, 1), r.m(i.parentNode, i)) : r && (ze(), D(r, 1, 1, () => {
        r = null;
      }), Me());
    },
    i(o) {
      s || (k(r), s = !0);
    },
    o(o) {
      D(r), s = !1;
    },
    d(o) {
      o && (R(t), R(n), R(i)), e[8](null), r && r.d(o);
    }
  };
}
function Q(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function et(e, t, n) {
  let i, s, {
    $$slots: r = {},
    $$scope: o
  } = t;
  const l = De(r);
  let {
    svelteInit: u
  } = t;
  const m = O(Q(t)), g = O();
  K(e, g, (c) => n(0, i = c));
  const a = O();
  K(e, a, (c) => n(1, s = c));
  const w = [], _ = Ye("$$ms-gr-react-wrapper"), {
    slotKey: x,
    slotIndex: E,
    subSlotIndex: f
  } = me() || {}, h = u({
    parent: _,
    props: m,
    target: g,
    slot: a,
    slotKey: x,
    slotIndex: E,
    subSlotIndex: f,
    onDestroy(c) {
      w.push(c);
    }
  });
  Ze("$$ms-gr-react-wrapper", h), Xe(() => {
    m.set(Q(t));
  }), Qe(() => {
    w.forEach((c) => c());
  });
  function y(c) {
    H[c ? "unshift" : "push"](() => {
      i = c, g.set(i);
    });
  }
  function S(c) {
    H[c ? "unshift" : "push"](() => {
      s = c, a.set(s);
    });
  }
  return e.$$set = (c) => {
    n(17, t = G(G({}, t), X(c))), "svelteInit" in c && n(5, u = c.svelteInit), "$$scope" in c && n(6, o = c.$$scope);
  }, t = X(t), [i, s, g, a, l, u, o, r, y, S];
}
class tt extends We {
  constructor(t) {
    super(), Ge(this, t, et, $e, He, {
      svelteInit: 5
    });
  }
}
const Z = window.ms_globals.rerender, A = window.ms_globals.tree;
function nt(e, t = {}) {
  function n(i) {
    const s = O(), r = new tt({
      ...i,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, u = o.parent ?? A;
          return u.nodes = [...u.nodes, l], Z({
            createPortal: M,
            node: A
          }), o.onDestroy(() => {
            u.nodes = u.nodes.filter((m) => m.svelteInstance !== s), Z({
              createPortal: M,
              node: A
            });
          }), l;
        },
        ...i.props
      }
    });
    return s.set(r), r;
  }
  return new Promise((i) => {
    window.ms_globals.initializePromise.then(() => {
      i(n);
    });
  });
}
const rt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function ot(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const i = e[n];
    return t[n] = st(n, i), t;
  }, {}) : {};
}
function st(e, t) {
  return typeof t == "number" && !rt.includes(e) ? t + "px" : t;
}
function U(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const s = b.Children.toArray(e._reactElement.props.children).map((r) => {
      if (b.isValidElement(r) && r.props.__slot__) {
        const {
          portals: o,
          clonedElement: l
        } = U(r.props.el);
        return b.cloneElement(r, {
          ...r.props,
          el: l,
          children: [...b.Children.toArray(r.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = e._reactElement.props.children, t.push(M(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: s
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: o,
      type: l,
      useCapture: u
    }) => {
      n.addEventListener(l, o, u);
    });
  });
  const i = Array.from(e.childNodes);
  for (let s = 0; s < i.length; s++) {
    const r = i[s];
    if (r.nodeType === 1) {
      const {
        clonedElement: o,
        portals: l
      } = U(r);
      t.push(...l), n.appendChild(o);
    } else r.nodeType === 3 && n.appendChild(r.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function it(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const C = ce(({
  slot: e,
  clone: t,
  className: n,
  style: i,
  observeAttributes: s
}, r) => {
  const o = N(), [l, u] = te([]), {
    forceClone: m
  } = he(), g = m ? !0 : t;
  return W(() => {
    var E;
    if (!o.current || !e)
      return;
    let a = e;
    function w() {
      let f = a;
      if (a.tagName.toLowerCase() === "svelte-slot" && a.children.length === 1 && a.children[0] && (f = a.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), it(r, f), n && f.classList.add(...n.split(" ")), i) {
        const h = ot(i);
        Object.keys(h).forEach((y) => {
          f.style[y] = h[y];
        });
      }
    }
    let _ = null, x = null;
    if (g && window.MutationObserver) {
      let f = function() {
        var c, I, d;
        (c = o.current) != null && c.contains(a) && ((I = o.current) == null || I.removeChild(a));
        const {
          portals: y,
          clonedElement: S
        } = U(e);
        a = S, u(y), a.style.display = "contents", x && clearTimeout(x), x = setTimeout(() => {
          w();
        }, 50), (d = o.current) == null || d.appendChild(a);
      };
      f();
      const h = Te(() => {
        f(), _ == null || _.disconnect(), _ == null || _.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: s
        });
      }, 50);
      _ = new window.MutationObserver(h), _.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      a.style.display = "contents", w(), (E = o.current) == null || E.appendChild(a);
    return () => {
      var f, h;
      a.style.display = "", (f = o.current) != null && f.contains(a) && ((h = o.current) == null || h.removeChild(a)), _ == null || _.disconnect();
    };
  }, [e, g, n, i, r, s]), b.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...l);
});
function lt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function at(e, t = !1) {
  try {
    if (_e(e))
      return e;
    if (t && !lt(e))
      return;
    if (typeof e == "string") {
      let n = e.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function T(e, t) {
  return ne(() => at(e, t), [e, t]);
}
function ct({
  value: e,
  onValueChange: t
}) {
  const [n, i] = te(e), s = N(t);
  s.current = t;
  const r = N(n);
  return r.current = n, W(() => {
    s.current(n);
  }, [n]), W(() => {
    Oe(e, r.current) || i(e);
  }, [e]), [n, i];
}
function ut(e) {
  return Object.keys(e).reduce((t, n) => (e[n] !== void 0 && (t[n] = e[n]), t), {});
}
const dt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ p.jsx(p.Fragment, {
  children: e(t)
});
function ft(e) {
  return b.createElement(dt, {
    children: e
  });
}
function $(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ft((n) => /* @__PURE__ */ p.jsx(pe, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ p.jsx(C, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ p.jsx(C, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ee({
  key: e,
  slots: t,
  targets: n
}, i) {
  return t[e] ? (...s) => n ? n.map((r, o) => /* @__PURE__ */ p.jsx(b.Fragment, {
    children: $(r, {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ p.jsx(p.Fragment, {
    children: $(t[e], {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }) : void 0;
}
const _t = nt(({
  slots: e,
  children: t,
  count: n,
  showCount: i,
  onValueChange: s,
  onChange: r,
  iconRender: o,
  elRef: l,
  setSlotParams: u,
  ...m
}) => {
  const g = T(n == null ? void 0 : n.strategy), a = T(n == null ? void 0 : n.exceedFormatter), w = T(n == null ? void 0 : n.show), _ = T(typeof i == "object" ? i.formatter : void 0), x = T(o), [E, f] = ct({
    onValueChange: s,
    value: m.value
  });
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(ge.Password, {
      ...m,
      value: E,
      ref: l,
      onChange: (h) => {
        r == null || r(h), f(h.target.value);
      },
      iconRender: e.iconRender ? ee({
        slots: e,
        setSlotParams: u,
        key: "iconRender"
      }) : x,
      showCount: e["showCount.formatter"] ? {
        formatter: ee({
          slots: e,
          setSlotParams: u,
          key: "showCount.formatter"
        })
      } : typeof i == "object" && _ ? {
        ...i,
        formatter: _
      } : i,
      count: ne(() => ut({
        ...n,
        exceedFormatter: a,
        strategy: g,
        show: w || (n == null ? void 0 : n.show)
      }), [n, a, g, w]),
      addonAfter: e.addonAfter ? /* @__PURE__ */ p.jsx(C, {
        slot: e.addonAfter
      }) : m.addonAfter,
      addonBefore: e.addonBefore ? /* @__PURE__ */ p.jsx(C, {
        slot: e.addonBefore
      }) : m.addonBefore,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ p.jsx(C, {
          slot: e["allowClear.clearIcon"]
        })
      } : m.allowClear,
      prefix: e.prefix ? /* @__PURE__ */ p.jsx(C, {
        slot: e.prefix
      }) : m.prefix,
      suffix: e.suffix ? /* @__PURE__ */ p.jsx(C, {
        slot: e.suffix
      }) : m.suffix
    })]
  });
});
export {
  _t as InputPassword,
  _t as default
};
