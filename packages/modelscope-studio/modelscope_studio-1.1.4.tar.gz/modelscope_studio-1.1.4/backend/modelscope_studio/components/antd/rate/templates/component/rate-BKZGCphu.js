import { i as ce, a as N, r as ae, g as ue, w as T, b as de } from "./Index-DNksQB3-.js";
const y = window.ms_globals.React, re = window.ms_globals.React.useMemo, se = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, ie = window.ms_globals.React.useState, le = window.ms_globals.React.useEffect, F = window.ms_globals.ReactDOM.createPortal, fe = window.ms_globals.internalContext.useContextPropsContext, me = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.Rate;
var he = /\s/;
function pe(e) {
  for (var t = e.length; t-- && he.test(e.charAt(t)); )
    ;
  return t;
}
var ge = /^\s+/;
function we(e) {
  return e && e.slice(0, pe(e) + 1).replace(ge, "");
}
var D = NaN, be = /^[-+]0x[0-9a-f]+$/i, ye = /^0b[01]+$/i, xe = /^0o[0-7]+$/i, Ee = parseInt;
function U(e) {
  if (typeof e == "number")
    return e;
  if (ce(e))
    return D;
  if (N(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = N(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = we(e);
  var s = ye.test(e);
  return s || xe.test(e) ? Ee(e.slice(2), s ? 2 : 8) : be.test(e) ? D : +e;
}
var L = function() {
  return ae.Date.now();
}, ve = "Expected a function", Ce = Math.max, Se = Math.min;
function Ie(e, t, s) {
  var i, o, n, r, l, u, _ = 0, g = !1, c = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(ve);
  t = U(t) || 0, N(s) && (g = !!s.leading, c = "maxWait" in s, n = c ? Ce(U(s.maxWait) || 0, t) : n, w = "trailing" in s ? !!s.trailing : w);
  function m(d) {
    var x = i, R = o;
    return i = o = void 0, _ = d, r = e.apply(R, x), r;
  }
  function E(d) {
    return _ = d, l = setTimeout(h, t), g ? m(d) : r;
  }
  function v(d) {
    var x = d - u, R = d - _, M = t - x;
    return c ? Se(M, n - R) : M;
  }
  function f(d) {
    var x = d - u, R = d - _;
    return u === void 0 || x >= t || x < 0 || c && R >= n;
  }
  function h() {
    var d = L();
    if (f(d))
      return b(d);
    l = setTimeout(h, v(d));
  }
  function b(d) {
    return l = void 0, w && i ? m(d) : (i = o = void 0, r);
  }
  function I() {
    l !== void 0 && clearTimeout(l), _ = 0, i = u = o = l = void 0;
  }
  function a() {
    return l === void 0 ? r : b(L());
  }
  function C() {
    var d = L(), x = f(d);
    if (i = arguments, o = this, u = d, x) {
      if (l === void 0)
        return E(u);
      if (c)
        return clearTimeout(l), l = setTimeout(h, t), m(u);
    }
    return l === void 0 && (l = setTimeout(h, t)), r;
  }
  return C.cancel = I, C.flush = a, C;
}
var Q = {
  exports: {}
}, k = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Re = y, Te = Symbol.for("react.element"), Pe = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ke = Re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, t, s) {
  var i, o = {}, n = null, r = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (r = t.ref);
  for (i in t) Oe.call(t, i) && !Le.hasOwnProperty(i) && (o[i] = t[i]);
  if (e && e.defaultProps) for (i in t = e.defaultProps, t) o[i] === void 0 && (o[i] = t[i]);
  return {
    $$typeof: Te,
    type: e,
    key: n,
    ref: r,
    props: o,
    _owner: ke.current
  };
}
k.Fragment = Pe;
k.jsx = Z;
k.jsxs = Z;
Q.exports = k;
var p = Q.exports;
const {
  SvelteComponent: je,
  assign: z,
  binding_callbacks: B,
  check_outros: Fe,
  children: $,
  claim_element: ee,
  claim_space: Ne,
  component_subscribe: G,
  compute_slots: We,
  create_slot: Ae,
  detach: S,
  element: te,
  empty: H,
  exclude_internal_props: K,
  get_all_dirty_from_scope: Me,
  get_slot_changes: De,
  group_outros: Ue,
  init: ze,
  insert_hydration: P,
  safe_not_equal: Be,
  set_custom_element_data: ne,
  space: Ge,
  transition_in: O,
  transition_out: W,
  update_slot_base: He
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: qe,
  onDestroy: Ve,
  setContext: Je
} = window.__gradio__svelte__internal;
function q(e) {
  let t, s;
  const i = (
    /*#slots*/
    e[7].default
  ), o = Ae(
    i,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = te("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      t = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var r = $(t);
      o && o.l(r), r.forEach(S), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(n, r) {
      P(n, t, r), o && o.m(t, null), e[9](t), s = !0;
    },
    p(n, r) {
      o && o.p && (!s || r & /*$$scope*/
      64) && He(
        o,
        i,
        n,
        /*$$scope*/
        n[6],
        s ? De(
          i,
          /*$$scope*/
          n[6],
          r,
          null
        ) : Me(
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
      W(o, n), s = !1;
    },
    d(n) {
      n && S(t), o && o.d(n), e[9](null);
    }
  };
}
function Xe(e) {
  let t, s, i, o, n = (
    /*$$slots*/
    e[4].default && q(e)
  );
  return {
    c() {
      t = te("react-portal-target"), s = Ge(), n && n.c(), i = H(), this.h();
    },
    l(r) {
      t = ee(r, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(t).forEach(S), s = Ne(r), n && n.l(r), i = H(), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(r, l) {
      P(r, t, l), e[8](t), P(r, s, l), n && n.m(r, l), P(r, i, l), o = !0;
    },
    p(r, [l]) {
      /*$$slots*/
      r[4].default ? n ? (n.p(r, l), l & /*$$slots*/
      16 && O(n, 1)) : (n = q(r), n.c(), O(n, 1), n.m(i.parentNode, i)) : n && (Ue(), W(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(r) {
      o || (O(n), o = !0);
    },
    o(r) {
      W(n), o = !1;
    },
    d(r) {
      r && (S(t), S(s), S(i)), e[8](null), n && n.d(r);
    }
  };
}
function V(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function Ye(e, t, s) {
  let i, o, {
    $$slots: n = {},
    $$scope: r
  } = t;
  const l = We(n);
  let {
    svelteInit: u
  } = t;
  const _ = T(V(t)), g = T();
  G(e, g, (a) => s(0, i = a));
  const c = T();
  G(e, c, (a) => s(1, o = a));
  const w = [], m = qe("$$ms-gr-react-wrapper"), {
    slotKey: E,
    slotIndex: v,
    subSlotIndex: f
  } = ue() || {}, h = u({
    parent: m,
    props: _,
    target: g,
    slot: c,
    slotKey: E,
    slotIndex: v,
    subSlotIndex: f,
    onDestroy(a) {
      w.push(a);
    }
  });
  Je("$$ms-gr-react-wrapper", h), Ke(() => {
    _.set(V(t));
  }), Ve(() => {
    w.forEach((a) => a());
  });
  function b(a) {
    B[a ? "unshift" : "push"](() => {
      i = a, g.set(i);
    });
  }
  function I(a) {
    B[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  return e.$$set = (a) => {
    s(17, t = z(z({}, t), K(a))), "svelteInit" in a && s(5, u = a.svelteInit), "$$scope" in a && s(6, r = a.$$scope);
  }, t = K(t), [i, o, g, c, l, u, r, n, b, I];
}
class Qe extends je {
  constructor(t) {
    super(), ze(this, t, Ye, Xe, Be, {
      svelteInit: 5
    });
  }
}
const J = window.ms_globals.rerender, j = window.ms_globals.tree;
function Ze(e, t = {}) {
  function s(i) {
    const o = T(), n = new Qe({
      ...i,
      props: {
        svelteInit(r) {
          window.ms_globals.autokey += 1;
          const l = {
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
          }, u = r.parent ?? j;
          return u.nodes = [...u.nodes, l], J({
            createPortal: F,
            node: j
          }), r.onDestroy(() => {
            u.nodes = u.nodes.filter((_) => _.svelteInstance !== o), J({
              createPortal: F,
              node: j
            });
          }), l;
        },
        ...i.props
      }
    });
    return o.set(n), n;
  }
  return new Promise((i) => {
    window.ms_globals.initializePromise.then(() => {
      i(s);
    });
  });
}
function $e(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function et(e, t = !1) {
  try {
    if (de(e))
      return e;
    if (t && !$e(e))
      return;
    if (typeof e == "string") {
      let s = e.trim();
      return s.startsWith(";") && (s = s.slice(1)), s.endsWith(";") && (s = s.slice(0, -1)), new Function(`return (...args) => (${s})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function tt(e, t) {
  return re(() => et(e, t), [e, t]);
}
const nt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rt(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const i = e[s];
    return t[s] = st(s, i), t;
  }, {}) : {};
}
function st(e, t) {
  return typeof t == "number" && !nt.includes(e) ? t + "px" : t;
}
function A(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement) {
    const o = y.Children.toArray(e._reactElement.props.children).map((n) => {
      if (y.isValidElement(n) && n.props.__slot__) {
        const {
          portals: r,
          clonedElement: l
        } = A(n.props.el);
        return y.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...y.Children.toArray(n.props.children), ...r]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(F(y.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), s)), {
      clonedElement: s,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: r,
      type: l,
      useCapture: u
    }) => {
      s.addEventListener(l, r, u);
    });
  });
  const i = Array.from(e.childNodes);
  for (let o = 0; o < i.length; o++) {
    const n = i[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: r,
        portals: l
      } = A(n);
      t.push(...l), s.appendChild(r);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function ot(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const X = se(({
  slot: e,
  clone: t,
  className: s,
  style: i,
  observeAttributes: o
}, n) => {
  const r = oe(), [l, u] = ie([]), {
    forceClone: _
  } = fe(), g = _ ? !0 : t;
  return le(() => {
    var v;
    if (!r.current || !e)
      return;
    let c = e;
    function w() {
      let f = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (f = c.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), ot(n, f), s && f.classList.add(...s.split(" ")), i) {
        const h = rt(i);
        Object.keys(h).forEach((b) => {
          f.style[b] = h[b];
        });
      }
    }
    let m = null, E = null;
    if (g && window.MutationObserver) {
      let f = function() {
        var a, C, d;
        (a = r.current) != null && a.contains(c) && ((C = r.current) == null || C.removeChild(c));
        const {
          portals: b,
          clonedElement: I
        } = A(e);
        c = I, u(b), c.style.display = "contents", E && clearTimeout(E), E = setTimeout(() => {
          w();
        }, 50), (d = r.current) == null || d.appendChild(c);
      };
      f();
      const h = Ie(() => {
        f(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", w(), (v = r.current) == null || v.appendChild(c);
    return () => {
      var f, h;
      c.style.display = "", (f = r.current) != null && f.contains(c) && ((h = r.current) == null || h.removeChild(c)), m == null || m.disconnect();
    };
  }, [e, g, s, i, n, o]), y.createElement("react-child", {
    ref: r,
    style: {
      display: "contents"
    }
  }, ...l);
}), it = ({
  children: e,
  ...t
}) => /* @__PURE__ */ p.jsx(p.Fragment, {
  children: e(t)
});
function lt(e) {
  return y.createElement(it, {
    children: e
  });
}
function Y(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? lt((s) => /* @__PURE__ */ p.jsx(me, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ p.jsx(X, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...s
    })
  })) : /* @__PURE__ */ p.jsx(X, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ct({
  key: e,
  slots: t,
  targets: s
}, i) {
  return t[e] ? (...o) => s ? s.map((n, r) => /* @__PURE__ */ p.jsx(y.Fragment, {
    children: Y(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, r)) : /* @__PURE__ */ p.jsx(p.Fragment, {
    children: Y(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ut = Ze(({
  slots: e,
  children: t,
  onValueChange: s,
  character: i,
  onChange: o,
  setSlotParams: n,
  elRef: r,
  ...l
}) => {
  const u = tt(i, !0);
  return /* @__PURE__ */ p.jsxs(p.Fragment, {
    children: [/* @__PURE__ */ p.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ p.jsx(_e, {
      ...l,
      ref: r,
      onChange: (_) => {
        o == null || o(_), s(_);
      },
      character: e.character ? ct({
        slots: e,
        setSlotParams: n,
        key: "character"
      }) : u || i
    })]
  });
});
export {
  ut as Rate,
  ut as default
};
