import { i as ce, a as N, r as ae, g as ue, w as T, b as de } from "./Index-DKpEyCk4.js";
const b = window.ms_globals.React, re = window.ms_globals.React.useMemo, se = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, ie = window.ms_globals.React.useState, le = window.ms_globals.React.useEffect, F = window.ms_globals.ReactDOM.createPortal, fe = window.ms_globals.internalContext.useContextPropsContext, me = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.QRCode;
var he = /\s/;
function pe(t) {
  for (var e = t.length; e-- && he.test(t.charAt(e)); )
    ;
  return e;
}
var ge = /^\s+/;
function we(t) {
  return t && t.slice(0, pe(t) + 1).replace(ge, "");
}
var D = NaN, be = /^[-+]0x[0-9a-f]+$/i, ye = /^0b[01]+$/i, Ce = /^0o[0-7]+$/i, Ee = parseInt;
function U(t) {
  if (typeof t == "number")
    return t;
  if (ce(t))
    return D;
  if (N(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = N(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = we(t);
  var r = ye.test(t);
  return r || Ce.test(t) ? Ee(t.slice(2), r ? 2 : 8) : be.test(t) ? D : +t;
}
var L = function() {
  return ae.Date.now();
}, xe = "Expected a function", ve = Math.max, Re = Math.min;
function Se(t, e, r) {
  var i, o, n, s, l, d, h = 0, p = !1, c = !1, g = !0;
  if (typeof t != "function")
    throw new TypeError(xe);
  e = U(e) || 0, N(r) && (p = !!r.leading, c = "maxWait" in r, n = c ? ve(U(r.maxWait) || 0, e) : n, g = "trailing" in r ? !!r.trailing : g);
  function m(u) {
    var C = i, I = o;
    return i = o = void 0, h = u, s = t.apply(I, C), s;
  }
  function E(u) {
    return h = u, l = setTimeout(_, e), p ? m(u) : s;
  }
  function x(u) {
    var C = u - d, I = u - h, M = e - C;
    return c ? Re(M, n - I) : M;
  }
  function f(u) {
    var C = u - d, I = u - h;
    return d === void 0 || C >= e || C < 0 || c && I >= n;
  }
  function _() {
    var u = L();
    if (f(u))
      return w(u);
    l = setTimeout(_, x(u));
  }
  function w(u) {
    return l = void 0, g && i ? m(u) : (i = o = void 0, s);
  }
  function S() {
    l !== void 0 && clearTimeout(l), h = 0, i = d = o = l = void 0;
  }
  function a() {
    return l === void 0 ? s : w(L());
  }
  function v() {
    var u = L(), C = f(u);
    if (i = arguments, o = this, d = u, C) {
      if (l === void 0)
        return E(d);
      if (c)
        return clearTimeout(l), l = setTimeout(_, e), m(d);
    }
    return l === void 0 && (l = setTimeout(_, e)), s;
  }
  return v.cancel = S, v.flush = a, v;
}
var Y = {
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
var Ie = b, Te = Symbol.for("react.element"), Pe = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ke = Ie.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(t, e, r) {
  var i, o = {}, n = null, s = null;
  r !== void 0 && (n = "" + r), e.key !== void 0 && (n = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (i in e) Oe.call(e, i) && !Le.hasOwnProperty(i) && (o[i] = e[i]);
  if (t && t.defaultProps) for (i in e = t.defaultProps, e) o[i] === void 0 && (o[i] = e[i]);
  return {
    $$typeof: Te,
    type: t,
    key: n,
    ref: s,
    props: o,
    _owner: ke.current
  };
}
k.Fragment = Pe;
k.jsx = Z;
k.jsxs = Z;
Y.exports = k;
var y = Y.exports;
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
  detach: R,
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
  getContext: Qe,
  onDestroy: qe,
  setContext: Ve
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, r;
  const i = (
    /*#slots*/
    t[7].default
  ), o = Ae(
    i,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = te("svelte-slot"), o && o.c(), this.h();
    },
    l(n) {
      e = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var s = $(e);
      o && o.l(s), s.forEach(R), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(n, s) {
      P(n, e, s), o && o.m(e, null), t[9](e), r = !0;
    },
    p(n, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && He(
        o,
        i,
        n,
        /*$$scope*/
        n[6],
        r ? De(
          i,
          /*$$scope*/
          n[6],
          s,
          null
        ) : Me(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (O(o, n), r = !0);
    },
    o(n) {
      W(o, n), r = !1;
    },
    d(n) {
      n && R(e), o && o.d(n), t[9](null);
    }
  };
}
function Je(t) {
  let e, r, i, o, n = (
    /*$$slots*/
    t[4].default && Q(t)
  );
  return {
    c() {
      e = te("react-portal-target"), r = Ge(), n && n.c(), i = H(), this.h();
    },
    l(s) {
      e = ee(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(e).forEach(R), r = Ne(s), n && n.l(s), i = H(), this.h();
    },
    h() {
      ne(e, "class", "svelte-1rt0kpf");
    },
    m(s, l) {
      P(s, e, l), t[8](e), P(s, r, l), n && n.m(s, l), P(s, i, l), o = !0;
    },
    p(s, [l]) {
      /*$$slots*/
      s[4].default ? n ? (n.p(s, l), l & /*$$slots*/
      16 && O(n, 1)) : (n = Q(s), n.c(), O(n, 1), n.m(i.parentNode, i)) : n && (Ue(), W(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(s) {
      o || (O(n), o = !0);
    },
    o(s) {
      W(n), o = !1;
    },
    d(s) {
      s && (R(e), R(r), R(i)), t[8](null), n && n.d(s);
    }
  };
}
function q(t) {
  const {
    svelteInit: e,
    ...r
  } = t;
  return r;
}
function Xe(t, e, r) {
  let i, o, {
    $$slots: n = {},
    $$scope: s
  } = e;
  const l = We(n);
  let {
    svelteInit: d
  } = e;
  const h = T(q(e)), p = T();
  G(t, p, (a) => r(0, i = a));
  const c = T();
  G(t, c, (a) => r(1, o = a));
  const g = [], m = Qe("$$ms-gr-react-wrapper"), {
    slotKey: E,
    slotIndex: x,
    subSlotIndex: f
  } = ue() || {}, _ = d({
    parent: m,
    props: h,
    target: p,
    slot: c,
    slotKey: E,
    slotIndex: x,
    subSlotIndex: f,
    onDestroy(a) {
      g.push(a);
    }
  });
  Ve("$$ms-gr-react-wrapper", _), Ke(() => {
    h.set(q(e));
  }), qe(() => {
    g.forEach((a) => a());
  });
  function w(a) {
    B[a ? "unshift" : "push"](() => {
      i = a, p.set(i);
    });
  }
  function S(a) {
    B[a ? "unshift" : "push"](() => {
      o = a, c.set(o);
    });
  }
  return t.$$set = (a) => {
    r(17, e = z(z({}, e), K(a))), "svelteInit" in a && r(5, d = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, e = K(e), [i, o, p, c, l, d, s, n, w, S];
}
class Ye extends je {
  constructor(e) {
    super(), ze(this, e, Xe, Je, Be, {
      svelteInit: 5
    });
  }
}
const V = window.ms_globals.rerender, j = window.ms_globals.tree;
function Ze(t, e = {}) {
  function r(i) {
    const o = T(), n = new Ye({
      ...i,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, d = s.parent ?? j;
          return d.nodes = [...d.nodes, l], V({
            createPortal: F,
            node: j
          }), s.onDestroy(() => {
            d.nodes = d.nodes.filter((h) => h.svelteInstance !== o), V({
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
      i(r);
    });
  });
}
function $e(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function et(t, e = !1) {
  try {
    if (de(t))
      return t;
    if (e && !$e(t))
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
function tt(t, e) {
  return re(() => et(t, e), [t, e]);
}
const nt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rt(t) {
  return t ? Object.keys(t).reduce((e, r) => {
    const i = t[r];
    return e[r] = st(r, i), e;
  }, {}) : {};
}
function st(t, e) {
  return typeof e == "number" && !nt.includes(t) ? e + "px" : e;
}
function A(t) {
  const e = [], r = t.cloneNode(!1);
  if (t._reactElement) {
    const o = b.Children.toArray(t._reactElement.props.children).map((n) => {
      if (b.isValidElement(n) && n.props.__slot__) {
        const {
          portals: s,
          clonedElement: l
        } = A(n.props.el);
        return b.cloneElement(n, {
          ...n.props,
          el: l,
          children: [...b.Children.toArray(n.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = t._reactElement.props.children, e.push(F(b.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: o
    }), r)), {
      clonedElement: r,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((o) => {
    t.getEventListeners(o).forEach(({
      listener: s,
      type: l,
      useCapture: d
    }) => {
      r.addEventListener(l, s, d);
    });
  });
  const i = Array.from(t.childNodes);
  for (let o = 0; o < i.length; o++) {
    const n = i[o];
    if (n.nodeType === 1) {
      const {
        clonedElement: s,
        portals: l
      } = A(n);
      e.push(...l), r.appendChild(s);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: e
  };
}
function ot(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const J = se(({
  slot: t,
  clone: e,
  className: r,
  style: i,
  observeAttributes: o
}, n) => {
  const s = oe(), [l, d] = ie([]), {
    forceClone: h
  } = fe(), p = h ? !0 : e;
  return le(() => {
    var x;
    if (!s.current || !t)
      return;
    let c = t;
    function g() {
      let f = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (f = c.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), ot(n, f), r && f.classList.add(...r.split(" ")), i) {
        const _ = rt(i);
        Object.keys(_).forEach((w) => {
          f.style[w] = _[w];
        });
      }
    }
    let m = null, E = null;
    if (p && window.MutationObserver) {
      let f = function() {
        var a, v, u;
        (a = s.current) != null && a.contains(c) && ((v = s.current) == null || v.removeChild(c));
        const {
          portals: w,
          clonedElement: S
        } = A(t);
        c = S, d(w), c.style.display = "contents", E && clearTimeout(E), E = setTimeout(() => {
          g();
        }, 50), (u = s.current) == null || u.appendChild(c);
      };
      f();
      const _ = Se(() => {
        f(), m == null || m.disconnect(), m == null || m.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      m = new window.MutationObserver(_), m.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", g(), (x = s.current) == null || x.appendChild(c);
    return () => {
      var f, _;
      c.style.display = "", (f = s.current) != null && f.contains(c) && ((_ = s.current) == null || _.removeChild(c)), m == null || m.disconnect();
    };
  }, [t, p, r, i, n, o]), b.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...l);
}), it = ({
  children: t,
  ...e
}) => /* @__PURE__ */ y.jsx(y.Fragment, {
  children: t(e)
});
function lt(t) {
  return b.createElement(it, {
    children: t
  });
}
function X(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? lt((r) => /* @__PURE__ */ y.jsx(me, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ y.jsx(J, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...r
    })
  })) : /* @__PURE__ */ y.jsx(J, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function ct({
  key: t,
  slots: e,
  targets: r
}, i) {
  return e[t] ? (...o) => r ? r.map((n, s) => /* @__PURE__ */ y.jsx(b.Fragment, {
    children: X(n, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ y.jsx(y.Fragment, {
    children: X(e[t], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ut = Ze(({
  setSlotParams: t,
  slots: e,
  statusRender: r,
  ...i
}) => {
  const o = tt(r);
  return /* @__PURE__ */ y.jsx(_e, {
    ...i,
    statusRender: e.statusRender ? ct({
      slots: e,
      setSlotParams: t,
      key: "statusRender"
    }) : o
  });
});
export {
  ut as QRCode,
  ut as default
};
