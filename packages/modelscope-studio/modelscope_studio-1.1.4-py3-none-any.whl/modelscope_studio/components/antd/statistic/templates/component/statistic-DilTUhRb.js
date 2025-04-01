import { i as ce, a as W, r as ae, g as ue, w as P, b as fe } from "./Index-DxApsgtg.js";
const b = window.ms_globals.React, re = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, se = window.ms_globals.React.useState, ie = window.ms_globals.React.useEffect, le = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, de = window.ms_globals.internalContext.useContextPropsContext, me = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.Statistic;
var he = /\s/;
function pe(t) {
  for (var e = t.length; e-- && he.test(t.charAt(e)); )
    ;
  return e;
}
var ge = /^\s+/;
function xe(t) {
  return t && t.slice(0, pe(t) + 1).replace(ge, "");
}
var U = NaN, we = /^[-+]0x[0-9a-f]+$/i, be = /^0b[01]+$/i, ye = /^0o[0-7]+$/i, Ee = parseInt;
function z(t) {
  if (typeof t == "number")
    return t;
  if (ce(t))
    return U;
  if (W(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = W(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = xe(t);
  var r = be.test(t);
  return r || ye.test(t) ? Ee(t.slice(2), r ? 2 : 8) : we.test(t) ? U : +t;
}
var L = function() {
  return ae.Date.now();
}, ve = "Expected a function", Ce = Math.max, Se = Math.min;
function Ie(t, e, r) {
  var i, s, n, o, l, f, p = 0, g = !1, c = !1, x = !0;
  if (typeof t != "function")
    throw new TypeError(ve);
  e = z(e) || 0, W(r) && (g = !!r.leading, c = "maxWait" in r, n = c ? Ce(z(r.maxWait) || 0, e) : n, x = "trailing" in r ? !!r.trailing : x);
  function m(u) {
    var y = i, R = s;
    return i = s = void 0, p = u, o = t.apply(R, y), o;
  }
  function E(u) {
    return p = u, l = setTimeout(h, e), g ? m(u) : o;
  }
  function v(u) {
    var y = u - f, R = u - p, D = e - y;
    return c ? Se(D, n - R) : D;
  }
  function d(u) {
    var y = u - f, R = u - p;
    return f === void 0 || y >= e || y < 0 || c && R >= n;
  }
  function h() {
    var u = L();
    if (d(u))
      return w(u);
    l = setTimeout(h, v(u));
  }
  function w(u) {
    return l = void 0, x && i ? m(u) : (i = s = void 0, o);
  }
  function I() {
    l !== void 0 && clearTimeout(l), p = 0, i = f = s = l = void 0;
  }
  function a() {
    return l === void 0 ? o : w(L());
  }
  function C() {
    var u = L(), y = d(u);
    if (i = arguments, s = this, f = u, y) {
      if (l === void 0)
        return E(f);
      if (c)
        return clearTimeout(l), l = setTimeout(h, e), m(f);
    }
    return l === void 0 && (l = setTimeout(h, e)), o;
  }
  return C.cancel = I, C.flush = a, C;
}
var Q = {
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
var Re = b, Te = Symbol.for("react.element"), Pe = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ke = Re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, je = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(t, e, r) {
  var i, s = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (i in e) Oe.call(e, i) && !je.hasOwnProperty(i) && (s[i] = e[i]);
  if (t && t.defaultProps) for (i in e = t.defaultProps, e) s[i] === void 0 && (s[i] = e[i]);
  return {
    $$typeof: Te,
    type: t,
    key: n,
    ref: o,
    props: s,
    _owner: ke.current
  };
}
j.Fragment = Pe;
j.jsx = Z;
j.jsxs = Z;
Q.exports = j;
var _ = Q.exports;
const {
  SvelteComponent: Le,
  assign: B,
  binding_callbacks: G,
  check_outros: Fe,
  children: $,
  claim_element: ee,
  claim_space: Ne,
  component_subscribe: H,
  compute_slots: We,
  create_slot: Ae,
  detach: S,
  element: te,
  empty: K,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Me,
  get_slot_changes: De,
  group_outros: Ue,
  init: ze,
  insert_hydration: O,
  safe_not_equal: Be,
  set_custom_element_data: ne,
  space: Ge,
  transition_in: k,
  transition_out: A,
  update_slot_base: He
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: qe,
  onDestroy: Ve,
  setContext: Je
} = window.__gradio__svelte__internal;
function V(t) {
  let e, r;
  const i = (
    /*#slots*/
    t[7].default
  ), s = Ae(
    i,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = te("svelte-slot"), s && s.c(), this.h();
    },
    l(n) {
      e = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = $(e);
      s && s.l(o), o.forEach(S), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      O(n, e, o), s && s.m(e, null), t[9](e), r = !0;
    },
    p(n, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && He(
        s,
        i,
        n,
        /*$$scope*/
        n[6],
        r ? De(
          i,
          /*$$scope*/
          n[6],
          o,
          null
        ) : Me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (k(s, n), r = !0);
    },
    o(n) {
      A(s, n), r = !1;
    },
    d(n) {
      n && S(e), s && s.d(n), t[9](null);
    }
  };
}
function Xe(t) {
  let e, r, i, s, n = (
    /*$$slots*/
    t[4].default && V(t)
  );
  return {
    c() {
      e = te("react-portal-target"), r = Ge(), n && n.c(), i = K(), this.h();
    },
    l(o) {
      e = ee(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(e).forEach(S), r = Ne(o), n && n.l(o), i = K(), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(o, l) {
      O(o, e, l), t[8](e), O(o, r, l), n && n.m(o, l), O(o, i, l), s = !0;
    },
    p(o, [l]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, l), l & /*$$slots*/
      16 && k(n, 1)) : (n = V(o), n.c(), k(n, 1), n.m(i.parentNode, i)) : n && (Ue(), A(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(o) {
      s || (k(n), s = !0);
    },
    o(o) {
      A(n), s = !1;
    },
    d(o) {
      o && (S(e), S(r), S(i)), t[8](null), n && n.d(o);
    }
  };
}
function J(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function Ye(t, e, r) {
  let i, s, {
    $$slots: n = {},
    $$scope: o
  } = e;
  const l = We(n);
  let {
    svelteInit: f
  } = e;
  const p = P(J(e)), g = P();
  H(t, g, (a) => r(0, i = a));
  const c = P();
  H(t, c, (a) => r(1, s = a));
  const x = [], m = qe("$$ms-gr-react-wrapper"), {
    slotKey: E,
    slotIndex: v,
    subSlotIndex: d
  } = ue() || {}, h = f({
    parent: m,
    props: p,
    target: g,
    slot: c,
    slotKey: E,
    slotIndex: v,
    subSlotIndex: d,
    onDestroy(a) {
      x.push(a);
    }
  });
  Je("$$ms-gr-react-wrapper", h), Ke(() => {
    p.set(J(e));
  }), Ve(() => {
    x.forEach((a) => a());
  });
  function w(a) {
    G[a ? "unshift" : "push"](() => {
      i = a, g.set(i);
    });
  }
  function I(a) {
    G[a ? "unshift" : "push"](() => {
      s = a, c.set(s);
    });
  }
  return t.$$set = (a) => {
    r(17, e = B(B({}, e), q(a))), "svelteInit" in a && r(5, f = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, e = q(e), [i, s, g, c, l, f, o, n, w, I];
}
class Qe extends Le {
  constructor(e) {
    super(), ze(this, e, Ye, Xe, Be, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, F = window.ms_globals.tree;
function Ze(t, e = {}) {
  function r(i) {
    const s = P(), n = new Qe({
      ...i,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: s,
            reactComponent: t,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: e.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, f = o.parent ?? F;
          return f.nodes = [...f.nodes, l], X({
            createPortal: N,
            node: F
          }), o.onDestroy(() => {
            f.nodes = f.nodes.filter((p) => p.svelteInstance !== s), X({
              createPortal: N,
              node: F
            });
          }), l;
        },
        ...i.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((i) => {
    window.ms_globals.initializePromise.then(() => {
      i(r);
    });
  });
}
const $e = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function et(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const i = t[r];
    return e[r] = tt(r, i), e;
  }, {}) : {};
}
function tt(t, e) {
  return typeof e == "number" && !$e.includes(t) ? e + "px" : e;
}
function M(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement) {
    const s = b.Children.toArray(t._reactElement.props.children).map((n) => {
      if (b.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: l
        } = M(n.props.el);
        return b.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...b.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = t._reactElement.props.children, e.push(N(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: s
    }), r)), {
      clonedElement: r,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((s) => {
    t.getEventListeners(s).forEach(({
      listener: o,
      type: l,
      useCapture: f
    }) => {
      r.addEventListener(l, o, f);
    });
  });
  const i = Array.from(t.childNodes);
  for (let s = 0; s < i.length; s++) {
    const n = i[s];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: l
      } = M(n);
      e.push(...l), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function nt(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const T = re(({
  slot: t,
  clone: e,
  className: r,
  style: i,
  observeAttributes: s
}, n) => {
  const o = oe(), [l, f] = se([]), {
    forceClone: p
  } = de(), g = p ? !0 : e;
  return ie(() => {
    var v;
    if (!o.current || !t)
      return;
    let c = t;
    function x() {
      let d = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (d = c.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), nt(n, d), r && d.classList.add(...r.split(" ")), i) {
        const h = et(i);
        Object.keys(h).forEach((w) => {
          d.style[w] = h[w];
        });
      }
    }
    let m = null, E = null;
    if (g && window.MutationObserver) {
      let d = function() {
        var a, C, u;
        (a = o.current) != null && a.contains(c) && ((C = o.current) == null || C.removeChild(c));
        const {
          portals: w,
          clonedElement: I
        } = M(t);
        c = I, f(w), c.style.display = "contents", E && clearTimeout(E), E = setTimeout(() => {
          x();
        }, 50), (u = o.current) == null || u.appendChild(c);
      };
      d();
      const h = Ie(() => {
        d(), m == null || m.disconnect(), m == null || m.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: s
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", x(), (v = o.current) == null || v.appendChild(c);
    return () => {
      var d, h;
      c.style.display = "", (d = o.current) != null && d.contains(c) && ((h = o.current) == null || h.removeChild(c)), m == null || m.disconnect();
    };
  }, [t, g, r, i, n, s]), b.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...l);
});
function rt(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function ot(t, e = !1) {
  try {
    if (fe(t))
      return t;
    if (e && !rt(t))
      return;
    if (typeof t == "string") {
      let r = t.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function st(t, e) {
  return le(() => ot(t, e), [t, e]);
}
const it = ({
  children: t,
  ...e
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: t(e)
});
function lt(t) {
  return b.createElement(it, {
    children: t
  });
}
function Y(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? lt((r) => /* @__PURE__ */ _.jsx(me, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ _.jsx(T, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...r
    })
  })) : /* @__PURE__ */ _.jsx(T, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ct({
  key: t,
  slots: e,
  targets: r
}, i) {
  return e[t] ? (...s) => r ? r.map((n, o) => /* @__PURE__ */ _.jsx(b.Fragment, {
    children: Y(n, {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: Y(e[t], {
      clone: !0,
      params: s,
      forceClone: !0
    })
  }) : void 0;
}
const ut = Ze(({
  children: t,
  slots: e,
  setSlotParams: r,
  formatter: i,
  ...s
}) => {
  const n = st(i);
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ _.jsx(_e, {
      ...s,
      formatter: e.formatter ? ct({
        slots: e,
        setSlotParams: r,
        key: "formatter"
      }) : n,
      title: e.title ? /* @__PURE__ */ _.jsx(T, {
        slot: e.title
      }) : s.title,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(T, {
        slot: e.prefix
      }) : s.prefix,
      suffix: e.suffix ? /* @__PURE__ */ _.jsx(T, {
        slot: e.suffix
      }) : s.suffix
    })]
  });
});
export {
  ut as Statistic,
  ut as default
};
