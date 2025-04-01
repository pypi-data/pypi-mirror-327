import { i as ce, a as W, r as ae, g as ue, w as P, b as de } from "./Index-oK1pwag4.js";
const x = window.ms_globals.React, re = window.ms_globals.React.forwardRef, oe = window.ms_globals.React.useRef, le = window.ms_globals.React.useState, se = window.ms_globals.React.useEffect, ie = window.ms_globals.React.useMemo, N = window.ms_globals.ReactDOM.createPortal, fe = window.ms_globals.internalContext.useContextPropsContext, me = window.ms_globals.internalContext.ContextPropsProvider, _e = window.ms_globals.antd.List;
var he = /\s/;
function ge(e) {
  for (var t = e.length; t-- && he.test(e.charAt(t)); )
    ;
  return t;
}
var pe = /^\s+/;
function we(e) {
  return e && e.slice(0, ge(e) + 1).replace(pe, "");
}
var U = NaN, be = /^[-+]0x[0-9a-f]+$/i, xe = /^0b[01]+$/i, ye = /^0o[0-7]+$/i, Ce = parseInt;
function z(e) {
  if (typeof e == "number")
    return e;
  if (ce(e))
    return U;
  if (W(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = W(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = we(e);
  var r = xe.test(e);
  return r || ye.test(e) ? Ce(e.slice(2), r ? 2 : 8) : be.test(e) ? U : +e;
}
var j = function() {
  return ae.Date.now();
}, Ee = "Expected a function", ve = Math.max, Ie = Math.min;
function Se(e, t, r) {
  var l, s, n, o, i, d, h = 0, p = !1, c = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Ee);
  t = z(t) || 0, W(r) && (p = !!r.leading, c = "maxWait" in r, n = c ? ve(z(r.maxWait) || 0, t) : n, w = "trailing" in r ? !!r.trailing : w);
  function m(u) {
    var y = l, R = s;
    return l = s = void 0, h = u, o = e.apply(R, y), o;
  }
  function C(u) {
    return h = u, i = setTimeout(_, t), p ? m(u) : o;
  }
  function E(u) {
    var y = u - d, R = u - h, D = t - y;
    return c ? Ie(D, n - R) : D;
  }
  function f(u) {
    var y = u - d, R = u - h;
    return d === void 0 || y >= t || y < 0 || c && R >= n;
  }
  function _() {
    var u = j();
    if (f(u))
      return b(u);
    i = setTimeout(_, E(u));
  }
  function b(u) {
    return i = void 0, w && l ? m(u) : (l = s = void 0, o);
  }
  function S() {
    i !== void 0 && clearTimeout(i), h = 0, l = d = s = i = void 0;
  }
  function a() {
    return i === void 0 ? o : b(j());
  }
  function v() {
    var u = j(), y = f(u);
    if (l = arguments, s = this, d = u, y) {
      if (i === void 0)
        return C(d);
      if (c)
        return clearTimeout(i), i = setTimeout(_, t), m(d);
    }
    return i === void 0 && (i = setTimeout(_, t)), o;
  }
  return v.cancel = S, v.flush = a, v;
}
var Q = {
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
var Re = x, Te = Symbol.for("react.element"), Pe = Symbol.for("react.fragment"), Oe = Object.prototype.hasOwnProperty, ke = Re.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Le = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Z(e, t, r) {
  var l, s = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) Oe.call(t, l) && !Le.hasOwnProperty(l) && (s[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) s[l] === void 0 && (s[l] = t[l]);
  return {
    $$typeof: Te,
    type: e,
    key: n,
    ref: o,
    props: s,
    _owner: ke.current
  };
}
L.Fragment = Pe;
L.jsx = Z;
L.jsxs = Z;
Q.exports = L;
var g = Q.exports;
const {
  SvelteComponent: je,
  assign: B,
  binding_callbacks: G,
  check_outros: Fe,
  children: $,
  claim_element: ee,
  claim_space: Ne,
  component_subscribe: H,
  compute_slots: We,
  create_slot: Me,
  detach: I,
  element: te,
  empty: K,
  exclude_internal_props: q,
  get_all_dirty_from_scope: Ae,
  get_slot_changes: De,
  group_outros: Ue,
  init: ze,
  insert_hydration: O,
  safe_not_equal: Be,
  set_custom_element_data: ne,
  space: Ge,
  transition_in: k,
  transition_out: M,
  update_slot_base: He
} = window.__gradio__svelte__internal, {
  beforeUpdate: Ke,
  getContext: qe,
  onDestroy: Ve,
  setContext: Je
} = window.__gradio__svelte__internal;
function V(e) {
  let t, r;
  const l = (
    /*#slots*/
    e[7].default
  ), s = Me(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = te("svelte-slot"), s && s.c(), this.h();
    },
    l(n) {
      t = ee(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = $(t);
      s && s.l(o), o.forEach(I), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      O(n, t, o), s && s.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      s && s.p && (!r || o & /*$$scope*/
      64) && He(
        s,
        l,
        n,
        /*$$scope*/
        n[6],
        r ? De(
          l,
          /*$$scope*/
          n[6],
          o,
          null
        ) : Ae(
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
      M(s, n), r = !1;
    },
    d(n) {
      n && I(t), s && s.d(n), e[9](null);
    }
  };
}
function Xe(e) {
  let t, r, l, s, n = (
    /*$$slots*/
    e[4].default && V(e)
  );
  return {
    c() {
      t = te("react-portal-target"), r = Ge(), n && n.c(), l = K(), this.h();
    },
    l(o) {
      t = ee(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), $(t).forEach(I), r = Ne(o), n && n.l(o), l = K(), this.h();
    },
    h() {
      ne(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      O(o, t, i), e[8](t), O(o, r, i), n && n.m(o, i), O(o, l, i), s = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, i), i & /*$$slots*/
      16 && k(n, 1)) : (n = V(o), n.c(), k(n, 1), n.m(l.parentNode, l)) : n && (Ue(), M(n, 1, 1, () => {
        n = null;
      }), Fe());
    },
    i(o) {
      s || (k(n), s = !0);
    },
    o(o) {
      M(n), s = !1;
    },
    d(o) {
      o && (I(t), I(r), I(l)), e[8](null), n && n.d(o);
    }
  };
}
function J(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function Ye(e, t, r) {
  let l, s, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const i = We(n);
  let {
    svelteInit: d
  } = t;
  const h = P(J(t)), p = P();
  H(e, p, (a) => r(0, l = a));
  const c = P();
  H(e, c, (a) => r(1, s = a));
  const w = [], m = qe("$$ms-gr-react-wrapper"), {
    slotKey: C,
    slotIndex: E,
    subSlotIndex: f
  } = ue() || {}, _ = d({
    parent: m,
    props: h,
    target: p,
    slot: c,
    slotKey: C,
    slotIndex: E,
    subSlotIndex: f,
    onDestroy(a) {
      w.push(a);
    }
  });
  Je("$$ms-gr-react-wrapper", _), Ke(() => {
    h.set(J(t));
  }), Ve(() => {
    w.forEach((a) => a());
  });
  function b(a) {
    G[a ? "unshift" : "push"](() => {
      l = a, p.set(l);
    });
  }
  function S(a) {
    G[a ? "unshift" : "push"](() => {
      s = a, c.set(s);
    });
  }
  return e.$$set = (a) => {
    r(17, t = B(B({}, t), q(a))), "svelteInit" in a && r(5, d = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, t = q(t), [l, s, p, c, i, d, o, n, b, S];
}
class Qe extends je {
  constructor(t) {
    super(), ze(this, t, Ye, Xe, Be, {
      svelteInit: 5
    });
  }
}
const X = window.ms_globals.rerender, F = window.ms_globals.tree;
function Ze(e, t = {}) {
  function r(l) {
    const s = P(), n = new Qe({
      ...l,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const i = {
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
          }, d = o.parent ?? F;
          return d.nodes = [...d.nodes, i], X({
            createPortal: N,
            node: F
          }), o.onDestroy(() => {
            d.nodes = d.nodes.filter((h) => h.svelteInstance !== s), X({
              createPortal: N,
              node: F
            });
          }), i;
        },
        ...l.props
      }
    });
    return s.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(r);
    });
  });
}
const $e = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function et(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const l = e[r];
    return t[r] = tt(r, l), t;
  }, {}) : {};
}
function tt(e, t) {
  return typeof t == "number" && !$e.includes(e) ? t + "px" : t;
}
function A(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const s = x.Children.toArray(e._reactElement.props.children).map((n) => {
      if (x.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: i
        } = A(n.props.el);
        return x.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...x.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return s.originalChildren = e._reactElement.props.children, t.push(N(x.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: s
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((s) => {
    e.getEventListeners(s).forEach(({
      listener: o,
      type: i,
      useCapture: d
    }) => {
      r.addEventListener(i, o, d);
    });
  });
  const l = Array.from(e.childNodes);
  for (let s = 0; s < l.length; s++) {
    const n = l[s];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = A(n);
      t.push(...i), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function nt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const T = re(({
  slot: e,
  clone: t,
  className: r,
  style: l,
  observeAttributes: s
}, n) => {
  const o = oe(), [i, d] = le([]), {
    forceClone: h
  } = fe(), p = h ? !0 : t;
  return se(() => {
    var E;
    if (!o.current || !e)
      return;
    let c = e;
    function w() {
      let f = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (f = c.children[0], f.tagName.toLowerCase() === "react-portal-target" && f.children[0] && (f = f.children[0])), nt(n, f), r && f.classList.add(...r.split(" ")), l) {
        const _ = et(l);
        Object.keys(_).forEach((b) => {
          f.style[b] = _[b];
        });
      }
    }
    let m = null, C = null;
    if (p && window.MutationObserver) {
      let f = function() {
        var a, v, u;
        (a = o.current) != null && a.contains(c) && ((v = o.current) == null || v.removeChild(c));
        const {
          portals: b,
          clonedElement: S
        } = A(e);
        c = S, d(b), c.style.display = "contents", C && clearTimeout(C), C = setTimeout(() => {
          w();
        }, 50), (u = o.current) == null || u.appendChild(c);
      };
      f();
      const _ = Se(() => {
        f(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: s
        });
      }, 50);
      m = new window.MutationObserver(_), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", w(), (E = o.current) == null || E.appendChild(c);
    return () => {
      var f, _;
      c.style.display = "", (f = o.current) != null && f.contains(c) && ((_ = o.current) == null || _.removeChild(c)), m == null || m.disconnect();
    };
  }, [e, p, r, l, n, s]), x.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function rt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ot(e, t = !1) {
  try {
    if (de(e))
      return e;
    if (t && !rt(e))
      return;
    if (typeof e == "string") {
      let r = e.trim();
      return r.startsWith(";") && (r = r.slice(1)), r.endsWith(";") && (r = r.slice(0, -1)), new Function(`return (...args) => (${r})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function lt(e, t) {
  return ie(() => ot(e, t), [e, t]);
}
const st = ({
  children: e,
  ...t
}) => /* @__PURE__ */ g.jsx(g.Fragment, {
  children: e(t)
});
function it(e) {
  return x.createElement(st, {
    children: e
  });
}
function Y(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? it((r) => /* @__PURE__ */ g.jsx(me, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ g.jsx(T, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ g.jsx(T, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function ct({
  key: e,
  slots: t,
  targets: r
}, l) {
  return t[e] ? (...s) => r ? r.map((n, o) => /* @__PURE__ */ g.jsx(x.Fragment, {
    children: Y(n, {
      clone: !0,
      params: s,
      forceClone: l == null ? void 0 : l.forceClone
    })
  }, o)) : /* @__PURE__ */ g.jsx(g.Fragment, {
    children: Y(t[e], {
      clone: !0,
      params: s,
      forceClone: l == null ? void 0 : l.forceClone
    })
  }) : void 0;
}
const ut = Ze(({
  slots: e,
  renderItem: t,
  setSlotParams: r,
  ...l
}) => {
  const s = lt(t);
  return /* @__PURE__ */ g.jsx(_e, {
    ...l,
    footer: e.footer ? /* @__PURE__ */ g.jsx(T, {
      slot: e.footer
    }) : l.footer,
    header: e.header ? /* @__PURE__ */ g.jsx(T, {
      slot: e.header
    }) : l.header,
    loadMore: e.loadMore ? /* @__PURE__ */ g.jsx(T, {
      slot: e.loadMore
    }) : l.loadMore,
    renderItem: e.renderItem ? ct({
      slots: e,
      setSlotParams: r,
      key: "renderItem"
    }, {
      forceClone: !0
    }) : s
  });
});
export {
  ut as List,
  ut as default
};
