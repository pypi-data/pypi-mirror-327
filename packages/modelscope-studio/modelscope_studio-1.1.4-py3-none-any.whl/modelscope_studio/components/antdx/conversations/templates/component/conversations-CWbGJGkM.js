import { i as Yt, a as Pe, r as er, g as tr, w as Y, c as re, b as xt } from "./Index-BdBG00C6.js";
const F = window.ms_globals.React, y = window.ms_globals.React, qt = window.ms_globals.React.forwardRef, Qt = window.ms_globals.React.useRef, Jt = window.ms_globals.React.useState, Zt = window.ms_globals.React.useEffect, Me = window.ms_globals.React.useMemo, Ee = window.ms_globals.ReactDOM.createPortal, rr = window.ms_globals.internalContext.useContextPropsContext, Ie = window.ms_globals.internalContext.ContextPropsProvider, St = window.ms_globals.createItemsContext.createItemsContext, nr = window.ms_globals.antd.ConfigProvider, je = window.ms_globals.antd.theme, Ct = window.ms_globals.antd.Typography, or = window.ms_globals.antd.Tooltip, ir = window.ms_globals.antd.Dropdown, sr = window.ms_globals.antdIcons.EllipsisOutlined, ne = window.ms_globals.antdCssinjs.unit, ve = window.ms_globals.antdCssinjs.token2CSSVar, Ue = window.ms_globals.antdCssinjs.useStyleRegister, ar = window.ms_globals.antdCssinjs.useCSSVarRegister, lr = window.ms_globals.antdCssinjs.createTheme, cr = window.ms_globals.antdCssinjs.useCacheToken;
var ur = /\s/;
function fr(t) {
  for (var e = t.length; e-- && ur.test(t.charAt(e)); )
    ;
  return e;
}
var dr = /^\s+/;
function hr(t) {
  return t && t.slice(0, fr(t) + 1).replace(dr, "");
}
var We = NaN, gr = /^[-+]0x[0-9a-f]+$/i, mr = /^0b[01]+$/i, pr = /^0o[0-7]+$/i, br = parseInt;
function Ke(t) {
  if (typeof t == "number")
    return t;
  if (Yt(t))
    return We;
  if (Pe(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = Pe(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = hr(t);
  var n = mr.test(t);
  return n || pr.test(t) ? br(t.slice(2), n ? 2 : 8) : gr.test(t) ? We : +t;
}
var xe = function() {
  return er.Date.now();
}, yr = "Expected a function", vr = Math.max, xr = Math.min;
function Sr(t, e, n) {
  var o, r, i, s, a, l, c = 0, f = !1, u = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(yr);
  e = Ke(e) || 0, Pe(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? vr(Ke(n.maxWait) || 0, e) : i, d = "trailing" in n ? !!n.trailing : d);
  function g(x) {
    var T = o, M = r;
    return o = r = void 0, c = x, s = t.apply(M, T), s;
  }
  function m(x) {
    return c = x, a = setTimeout(b, e), f ? g(x) : s;
  }
  function v(x) {
    var T = x - l, M = x - c, P = e - T;
    return u ? xr(P, i - M) : P;
  }
  function h(x) {
    var T = x - l, M = x - c;
    return l === void 0 || T >= e || T < 0 || u && M >= i;
  }
  function b() {
    var x = xe();
    if (h(x))
      return S(x);
    a = setTimeout(b, v(x));
  }
  function S(x) {
    return a = void 0, d && o ? g(x) : (o = r = void 0, s);
  }
  function E() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function p() {
    return a === void 0 ? s : S(xe());
  }
  function C() {
    var x = xe(), T = h(x);
    if (o = arguments, r = this, l = x, T) {
      if (a === void 0)
        return m(l);
      if (u)
        return clearTimeout(a), a = setTimeout(b, e), g(l);
    }
    return a === void 0 && (a = setTimeout(b, e)), s;
  }
  return C.cancel = E, C.flush = p, C;
}
var _t = {
  exports: {}
}, se = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Cr = y, _r = Symbol.for("react.element"), wr = Symbol.for("react.fragment"), Tr = Object.prototype.hasOwnProperty, Or = Cr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Mr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function wt(t, e, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), e.key !== void 0 && (i = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) Tr.call(e, o) && !Mr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: _r,
    type: t,
    key: i,
    ref: s,
    props: r,
    _owner: Or.current
  };
}
se.Fragment = wr;
se.jsx = wt;
se.jsxs = wt;
_t.exports = se;
var j = _t.exports;
const {
  SvelteComponent: Er,
  assign: qe,
  binding_callbacks: Qe,
  check_outros: Pr,
  children: Tt,
  claim_element: Ot,
  claim_space: Ir,
  component_subscribe: Je,
  compute_slots: jr,
  create_slot: kr,
  detach: U,
  element: Mt,
  empty: Ze,
  exclude_internal_props: Ye,
  get_all_dirty_from_scope: Lr,
  get_slot_changes: Rr,
  group_outros: Dr,
  init: Hr,
  insert_hydration: ee,
  safe_not_equal: Ar,
  set_custom_element_data: Et,
  space: $r,
  transition_in: te,
  transition_out: ke,
  update_slot_base: zr
} = window.__gradio__svelte__internal, {
  beforeUpdate: Br,
  getContext: Xr,
  onDestroy: Fr,
  setContext: Vr
} = window.__gradio__svelte__internal;
function et(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = kr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = Mt("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      e = Ot(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = Tt(e);
      r && r.l(s), s.forEach(U), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      ee(i, e, s), r && r.m(e, null), t[9](e), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && zr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? Rr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Lr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (te(r, i), n = !0);
    },
    o(i) {
      ke(r, i), n = !1;
    },
    d(i) {
      i && U(e), r && r.d(i), t[9](null);
    }
  };
}
function Nr(t) {
  let e, n, o, r, i = (
    /*$$slots*/
    t[4].default && et(t)
  );
  return {
    c() {
      e = Mt("react-portal-target"), n = $r(), i && i.c(), o = Ze(), this.h();
    },
    l(s) {
      e = Ot(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), Tt(e).forEach(U), n = Ir(s), i && i.l(s), o = Ze(), this.h();
    },
    h() {
      Et(e, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ee(s, e, a), t[8](e), ee(s, n, a), i && i.m(s, a), ee(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && te(i, 1)) : (i = et(s), i.c(), te(i, 1), i.m(o.parentNode, o)) : i && (Dr(), ke(i, 1, 1, () => {
        i = null;
      }), Pr());
    },
    i(s) {
      r || (te(i), r = !0);
    },
    o(s) {
      ke(i), r = !1;
    },
    d(s) {
      s && (U(e), U(n), U(o)), t[8](null), i && i.d(s);
    }
  };
}
function tt(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Gr(t, e, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const a = jr(i);
  let {
    svelteInit: l
  } = e;
  const c = Y(tt(e)), f = Y();
  Je(t, f, (p) => n(0, o = p));
  const u = Y();
  Je(t, u, (p) => n(1, r = p));
  const d = [], g = Xr("$$ms-gr-react-wrapper"), {
    slotKey: m,
    slotIndex: v,
    subSlotIndex: h
  } = tr() || {}, b = l({
    parent: g,
    props: c,
    target: f,
    slot: u,
    slotKey: m,
    slotIndex: v,
    subSlotIndex: h,
    onDestroy(p) {
      d.push(p);
    }
  });
  Vr("$$ms-gr-react-wrapper", b), Br(() => {
    c.set(tt(e));
  }), Fr(() => {
    d.forEach((p) => p());
  });
  function S(p) {
    Qe[p ? "unshift" : "push"](() => {
      o = p, f.set(o);
    });
  }
  function E(p) {
    Qe[p ? "unshift" : "push"](() => {
      r = p, u.set(r);
    });
  }
  return t.$$set = (p) => {
    n(17, e = qe(qe({}, e), Ye(p))), "svelteInit" in p && n(5, l = p.svelteInit), "$$scope" in p && n(6, s = p.$$scope);
  }, e = Ye(e), [o, r, f, u, a, l, s, i, S, E];
}
class Ur extends Er {
  constructor(e) {
    super(), Hr(this, e, Gr, Nr, Ar, {
      svelteInit: 5
    });
  }
}
const rt = window.ms_globals.rerender, Se = window.ms_globals.tree;
function Wr(t, e = {}) {
  function n(o) {
    const r = Y(), i = new Ur({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, l = s.parent ?? Se;
          return l.nodes = [...l.nodes, a], rt({
            createPortal: Ee,
            node: Se
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), rt({
              createPortal: Ee,
              node: Se
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(i), i;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Kr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function qr(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = Qr(n, o), e;
  }, {}) : {};
}
function Qr(t, e) {
  return typeof e == "number" && !Kr.includes(t) ? e + "px" : e;
}
function Le(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = y.Children.toArray(t._reactElement.props.children).map((i) => {
      if (y.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Le(i.props.el);
        return y.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...y.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(Ee(y.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Le(i);
      e.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Jr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Q = qt(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = Qt(), [a, l] = Jt([]), {
    forceClone: c
  } = rr(), f = c ? !0 : e;
  return Zt(() => {
    var v;
    if (!s.current || !t)
      return;
    let u = t;
    function d() {
      let h = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (h = u.children[0], h.tagName.toLowerCase() === "react-portal-target" && h.children[0] && (h = h.children[0])), Jr(i, h), n && h.classList.add(...n.split(" ")), o) {
        const b = qr(o);
        Object.keys(b).forEach((S) => {
          h.style[S] = b[S];
        });
      }
    }
    let g = null, m = null;
    if (f && window.MutationObserver) {
      let h = function() {
        var p, C, x;
        (p = s.current) != null && p.contains(u) && ((C = s.current) == null || C.removeChild(u));
        const {
          portals: S,
          clonedElement: E
        } = Le(t);
        u = E, l(S), u.style.display = "contents", m && clearTimeout(m), m = setTimeout(() => {
          d();
        }, 50), (x = s.current) == null || x.appendChild(u);
      };
      h();
      const b = Sr(() => {
        h(), g == null || g.disconnect(), g == null || g.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      g = new window.MutationObserver(b), g.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (v = s.current) == null || v.appendChild(u);
    return () => {
      var h, b;
      u.style.display = "", (h = s.current) != null && h.contains(u) && ((b = s.current) == null || b.removeChild(u)), g == null || g.disconnect();
    };
  }, [t, f, n, o, i, r]), y.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Zr = "1.0.5", Yr = /* @__PURE__ */ y.createContext({}), en = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, tn = (t) => {
  const e = y.useContext(Yr);
  return y.useMemo(() => ({
    ...en,
    ...e[t]
  }), [e[t]]);
};
function oe() {
  return oe = Object.assign ? Object.assign.bind() : function(t) {
    for (var e = 1; e < arguments.length; e++) {
      var n = arguments[e];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (t[o] = n[o]);
    }
    return t;
  }, oe.apply(null, arguments);
}
function Re() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = y.useContext(nr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function nt(t) {
  var e = F.useRef();
  e.current = t;
  var n = F.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(i));
  }, []);
  return n;
}
function rn(t) {
  if (Array.isArray(t)) return t;
}
function nn(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== e); l = !0) ;
    } catch (f) {
      c = !0, r = f;
    } finally {
      try {
        if (!l && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw r;
      }
    }
    return a;
  }
}
function ot(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function on(t, e) {
  if (t) {
    if (typeof t == "string") return ot(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? ot(t, e) : void 0;
  }
}
function sn() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function N(t, e) {
  return rn(t) || nn(t, e) || on(t, e) || sn();
}
function an() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var it = an() ? F.useLayoutEffect : F.useEffect, ln = function(e, n) {
  var o = F.useRef(!0);
  it(function() {
    return e(o.current);
  }, n), it(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, st = function(e, n) {
  ln(function(o) {
    if (!o)
      return e();
  }, n);
};
function at(t) {
  var e = F.useRef(!1), n = F.useState(t), o = N(n, 2), r = o[0], i = o[1];
  F.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function s(a, l) {
    l && e.current || i(a);
  }
  return [r, s];
}
function Ce(t) {
  return t !== void 0;
}
function cn(t, e) {
  var n = e || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = at(function() {
    return Ce(r) ? r : Ce(o) ? typeof o == "function" ? o() : o : typeof t == "function" ? t() : t;
  }), l = N(a, 2), c = l[0], f = l[1], u = r !== void 0 ? r : c, d = s ? s(u) : u, g = nt(i), m = at([u]), v = N(m, 2), h = v[0], b = v[1];
  st(function() {
    var E = h[0];
    c !== E && g(c, E);
  }, [h]), st(function() {
    Ce(r) || f(r);
  }, [r]);
  var S = nt(function(E, p) {
    f(E, p), b([u], p);
  });
  return [d, S];
}
function A(t) {
  "@babel/helpers - typeof";
  return A = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, A(t);
}
var w = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var $e = Symbol.for("react.element"), ze = Symbol.for("react.portal"), ae = Symbol.for("react.fragment"), le = Symbol.for("react.strict_mode"), ce = Symbol.for("react.profiler"), ue = Symbol.for("react.provider"), fe = Symbol.for("react.context"), un = Symbol.for("react.server_context"), de = Symbol.for("react.forward_ref"), he = Symbol.for("react.suspense"), ge = Symbol.for("react.suspense_list"), me = Symbol.for("react.memo"), pe = Symbol.for("react.lazy"), fn = Symbol.for("react.offscreen"), Pt;
Pt = Symbol.for("react.module.reference");
function H(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case $e:
        switch (t = t.type, t) {
          case ae:
          case ce:
          case le:
          case he:
          case ge:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case un:
              case fe:
              case de:
              case pe:
              case me:
              case ue:
                return t;
              default:
                return e;
            }
        }
      case ze:
        return e;
    }
  }
}
w.ContextConsumer = fe;
w.ContextProvider = ue;
w.Element = $e;
w.ForwardRef = de;
w.Fragment = ae;
w.Lazy = pe;
w.Memo = me;
w.Portal = ze;
w.Profiler = ce;
w.StrictMode = le;
w.Suspense = he;
w.SuspenseList = ge;
w.isAsyncMode = function() {
  return !1;
};
w.isConcurrentMode = function() {
  return !1;
};
w.isContextConsumer = function(t) {
  return H(t) === fe;
};
w.isContextProvider = function(t) {
  return H(t) === ue;
};
w.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === $e;
};
w.isForwardRef = function(t) {
  return H(t) === de;
};
w.isFragment = function(t) {
  return H(t) === ae;
};
w.isLazy = function(t) {
  return H(t) === pe;
};
w.isMemo = function(t) {
  return H(t) === me;
};
w.isPortal = function(t) {
  return H(t) === ze;
};
w.isProfiler = function(t) {
  return H(t) === ce;
};
w.isStrictMode = function(t) {
  return H(t) === le;
};
w.isSuspense = function(t) {
  return H(t) === he;
};
w.isSuspenseList = function(t) {
  return H(t) === ge;
};
w.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === ae || t === ce || t === le || t === he || t === ge || t === fn || typeof t == "object" && t !== null && (t.$$typeof === pe || t.$$typeof === me || t.$$typeof === ue || t.$$typeof === fe || t.$$typeof === de || t.$$typeof === Pt || t.getModuleId !== void 0);
};
w.typeOf = H;
function dn(t, e) {
  if (A(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e || "default");
    if (A(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function It(t) {
  var e = dn(t, "string");
  return A(e) == "symbol" ? e : e + "";
}
function O(t, e, n) {
  return (e = It(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function lt(t, e) {
  var n = Object.keys(t);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(t);
    e && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(t, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function L(t) {
  for (var e = 1; e < arguments.length; e++) {
    var n = arguments[e] != null ? arguments[e] : {};
    e % 2 ? lt(Object(n), !0).forEach(function(o) {
      O(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : lt(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function be(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function hn(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, It(o.key), o);
  }
}
function ye(t, e, n) {
  return e && hn(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function De(t, e) {
  return De = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, De(t, e);
}
function jt(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && De(t, e);
}
function ie(t) {
  return ie = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ie(t);
}
function kt() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (kt = function() {
    return !!t;
  })();
}
function q(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function gn(t, e) {
  if (e && (A(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return q(t);
}
function Lt(t) {
  var e = kt();
  return function() {
    var n, o = ie(t);
    if (e) {
      var r = ie(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return gn(this, n);
  };
}
var Rt = /* @__PURE__ */ ye(function t() {
  be(this, t);
}), Dt = "CALC_UNIT", mn = new RegExp(Dt, "g");
function _e(t) {
  return typeof t == "number" ? "".concat(t).concat(Dt) : t;
}
var pn = /* @__PURE__ */ function(t) {
  jt(n, t);
  var e = Lt(n);
  function n(o, r) {
    var i;
    be(this, n), i = e.call(this), O(q(i), "result", ""), O(q(i), "unitlessCssVar", void 0), O(q(i), "lowPriority", void 0);
    var s = A(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = _e(o) : s === "string" && (i.result = o), i;
  }
  return ye(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(_e(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(_e(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " * ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " * ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(r) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), r instanceof n ? this.result = "".concat(this.result, " / ").concat(r.getResult(!0)) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " / ").concat(r)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(r) {
      return this.lowPriority || r ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(r) {
      var i = this, s = r || {}, a = s.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (l = !1), this.result = this.result.replace(mn, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Rt), bn = /* @__PURE__ */ function(t) {
  jt(n, t);
  var e = Lt(n);
  function n(o) {
    var r;
    return be(this, n), r = e.call(this), O(q(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ye(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result += r.result : typeof r == "number" && (this.result += r), this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result -= r.result : typeof r == "number" && (this.result -= r), this;
    }
  }, {
    key: "mul",
    value: function(r) {
      return r instanceof n ? this.result *= r.result : typeof r == "number" && (this.result *= r), this;
    }
  }, {
    key: "div",
    value: function(r) {
      return r instanceof n ? this.result /= r.result : typeof r == "number" && (this.result /= r), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Rt), yn = function(e, n) {
  var o = e === "css" ? pn : bn;
  return function(r) {
    return new o(r, n);
  };
}, ct = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ut(t, e, n, o) {
  var r = L({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = N(a, 2), c = l[0], f = l[1];
      if (r != null && r[c] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = L(L({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === e[a] && delete s[a];
  }), s;
}
var Ht = typeof CSSINJS_STATISTIC < "u", He = !0;
function Be() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!Ht)
    return Object.assign.apply(Object, [{}].concat(e));
  He = !1;
  var o = {};
  return e.forEach(function(r) {
    if (A(r) === "object") {
      var i = Object.keys(r);
      i.forEach(function(s) {
        Object.defineProperty(o, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[s];
          }
        });
      });
    }
  }), He = !0, o;
}
var ft = {};
function vn() {
}
var xn = function(e) {
  var n, o = e, r = vn;
  return Ht && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(s, a) {
      if (He) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    ft[s] = {
      global: Array.from(n),
      component: L(L({}, (l = ft[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function dt(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Be(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function Sn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return ne(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return ne(i);
      }).join(","), ")");
    }
  };
}
var Cn = 1e3 * 60 * 10, _n = /* @__PURE__ */ function() {
  function t() {
    be(this, t), O(this, "map", /* @__PURE__ */ new Map()), O(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), O(this, "nextID", 0), O(this, "lastAccessBeat", /* @__PURE__ */ new Map()), O(this, "accessBeat", 0);
  }
  return ye(t, [{
    key: "set",
    value: function(n, o) {
      this.clear();
      var r = this.getCompositeKey(n);
      this.map.set(r, o), this.lastAccessBeat.set(r, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var o = this.getCompositeKey(n), r = this.map.get(o);
      return this.lastAccessBeat.set(o, Date.now()), this.accessBeat += 1, r;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var o = this, r = n.map(function(i) {
        return i && A(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(A(i), "_").concat(i);
      });
      return r.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var o = this.nextID;
      return this.objectIDMap.set(n, o), this.nextID += 1, o;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var o = Date.now();
        this.lastAccessBeat.forEach(function(r, i) {
          o - r > Cn && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), ht = new _n();
function wn(t, e) {
  return y.useMemo(function() {
    var n = ht.get(e);
    if (n)
      return n;
    var o = t();
    return ht.set(e, o), o;
  }, e);
}
var Tn = function() {
  return {};
};
function On(t) {
  var e = t.useCSP, n = e === void 0 ? Tn : e, o = t.useToken, r = t.usePrefix, i = t.getResetStyles, s = t.getCommonStyle, a = t.getCompUnitless;
  function l(d, g, m, v) {
    var h = Array.isArray(d) ? d[0] : d;
    function b(M) {
      return "".concat(String(h)).concat(M.slice(0, 1).toUpperCase()).concat(M.slice(1));
    }
    var S = (v == null ? void 0 : v.unitless) || {}, E = typeof a == "function" ? a(d) : {}, p = L(L({}, E), {}, O({}, b("zIndexPopup"), !0));
    Object.keys(S).forEach(function(M) {
      p[b(M)] = S[M];
    });
    var C = L(L({}, v), {}, {
      unitless: p,
      prefixToken: b
    }), x = f(d, g, m, C), T = c(h, m, C);
    return function(M) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : M, R = x(M, P), $ = N(R, 2), _ = $[1], z = T(P), k = N(z, 2), D = k[0], B = k[1];
      return [D, _, B];
    };
  }
  function c(d, g, m) {
    var v = m.unitless, h = m.injectStyle, b = h === void 0 ? !0 : h, S = m.prefixToken, E = m.ignore, p = function(T) {
      var M = T.rootCls, P = T.cssVar, R = P === void 0 ? {} : P, $ = o(), _ = $.realToken;
      return ar({
        path: [d],
        prefix: R.prefix,
        key: R.key,
        unitless: v,
        ignore: E,
        token: _,
        scope: M
      }, function() {
        var z = dt(d, _, g), k = ut(d, _, z, {
          deprecatedTokens: m == null ? void 0 : m.deprecatedTokens
        });
        return Object.keys(z).forEach(function(D) {
          k[S(D)] = k[D], delete k[D];
        }), k;
      }), null;
    }, C = function(T) {
      var M = o(), P = M.cssVar;
      return [function(R) {
        return b && P ? /* @__PURE__ */ y.createElement(y.Fragment, null, /* @__PURE__ */ y.createElement(p, {
          rootCls: T,
          cssVar: P,
          component: d
        }), R) : R;
      }, P == null ? void 0 : P.key];
    };
    return C;
  }
  function f(d, g, m) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = Array.isArray(d) ? d : [d, d], b = N(h, 1), S = b[0], E = h.join("-"), p = t.layer || {
      name: "antd"
    };
    return function(C) {
      var x = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, T = o(), M = T.theme, P = T.realToken, R = T.hashId, $ = T.token, _ = T.cssVar, z = r(), k = z.rootPrefixCls, D = z.iconPrefixCls, B = n(), W = _ ? "css" : "js", Xt = wn(function() {
        var V = /* @__PURE__ */ new Set();
        return _ && Object.keys(v.unitless || {}).forEach(function(J) {
          V.add(ve(J, _.prefix)), V.add(ve(J, ct(S, _.prefix)));
        }), yn(W, V);
      }, [W, S, _ == null ? void 0 : _.prefix]), Xe = Sn(W), Ft = Xe.max, Vt = Xe.min, Fe = {
        theme: M,
        token: $,
        hashId: R,
        nonce: function() {
          return B.nonce;
        },
        clientOnly: v.clientOnly,
        layer: p,
        // antd is always at top of styles
        order: v.order || -999
      };
      typeof i == "function" && Ue(L(L({}, Fe), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return i($, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: D
          },
          csp: B
        });
      });
      var Nt = Ue(L(L({}, Fe), {}, {
        path: [E, C, D]
      }), function() {
        if (v.injectStyle === !1)
          return [];
        var V = xn($), J = V.token, Gt = V.flush, G = dt(S, P, m), Ut = ".".concat(C), Ve = ut(S, P, G, {
          deprecatedTokens: v.deprecatedTokens
        });
        _ && G && A(G) === "object" && Object.keys(G).forEach(function(Ge) {
          G[Ge] = "var(".concat(ve(Ge, ct(S, _.prefix)), ")");
        });
        var Ne = Be(J, {
          componentCls: Ut,
          prefixCls: C,
          iconCls: ".".concat(D),
          antCls: ".".concat(k),
          calc: Xt,
          // @ts-ignore
          max: Ft,
          // @ts-ignore
          min: Vt
        }, _ ? G : Ve), Wt = g(Ne, {
          hashId: R,
          prefixCls: C,
          rootPrefixCls: k,
          iconPrefixCls: D
        });
        Gt(S, Ve);
        var Kt = typeof s == "function" ? s(Ne, C, x, v.resetFont) : null;
        return [v.resetStyle === !1 ? null : Kt, Wt];
      });
      return [Nt, R];
    };
  }
  function u(d, g, m) {
    var v = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, h = f(d, g, m, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, v)), b = function(E) {
      var p = E.prefixCls, C = E.rootCls, x = C === void 0 ? p : C;
      return h(p, x), null;
    };
    return b;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const I = Math.round;
function we(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const gt = (t, e, n) => n === 0 ? t : t / 100;
function K(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class X {
  constructor(e) {
    O(this, "isValid", !0), O(this, "r", 0), O(this, "g", 0), O(this, "b", 0), O(this, "a", 1), O(this, "_h", void 0), O(this, "_s", void 0), O(this, "_l", void 0), O(this, "_v", void 0), O(this, "_max", void 0), O(this, "_min", void 0), O(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof X)
      this.r = e.r, this.g = e.g, this.b = e.b, this.a = e.a, this._h = e._h, this._s = e._s, this._l = e._l, this._v = e._v;
    else if (n("rgb"))
      this.r = K(e.r), this.g = K(e.g), this.b = K(e.b), this.a = typeof e.a == "number" ? K(e.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(e);
    else if (n("hsv"))
      this.fromHsv(e);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(e));
  }
  // ======================= Setter =======================
  setR(e) {
    return this._sc("r", e);
  }
  setG(e) {
    return this._sc("g", e);
  }
  setB(e) {
    return this._sc("b", e);
  }
  setA(e) {
    return this._sc("a", e, 1);
  }
  setHue(e) {
    const n = this.toHsv();
    return n.h = e, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function e(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = e(this.r), o = e(this.g), r = e(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._h = 0 : this._h = I(60 * (this.r === this.getMax() ? (this.g - this.b) / e + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / e + 2 : (this.r - this.g) / e + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const e = this.getMax() - this.getMin();
      e === 0 ? this._s = 0 : this._s = e / this.getMax();
    }
    return this._s;
  }
  getLightness() {
    return typeof this._l > "u" && (this._l = (this.getMax() + this.getMin()) / 510), this._l;
  }
  getValue() {
    return typeof this._v > "u" && (this._v = this.getMax() / 255), this._v;
  }
  /**
   * Returns the perceived brightness of the color, from 0-255.
   * Note: this is not the b of HSB
   * @see http://www.w3.org/TR/AERT#color-contrast
   */
  getBrightness() {
    return typeof this._brightness > "u" && (this._brightness = (this.r * 299 + this.g * 587 + this.b * 114) / 1e3), this._brightness;
  }
  // ======================== Func ========================
  darken(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - e / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(e = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + e / 100;
    return r > 1 && (r = 1), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(e, n = 50) {
    const o = this._c(e), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: I(i("r")),
      g: I(i("g")),
      b: I(i("b")),
      a: I(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(e = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, e);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(e = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, e);
  }
  onBackground(e) {
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (i) => I((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
    return this._c({
      r: r("r"),
      g: r("g"),
      b: r("b"),
      a: o
    });
  }
  // ======================= Status =======================
  isDark() {
    return this.getBrightness() < 128;
  }
  isLight() {
    return this.getBrightness() >= 128;
  }
  // ======================== MISC ========================
  equals(e) {
    return this.r === e.r && this.g === e.g && this.b === e.b && this.a === e.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let e = "#";
    const n = (this.r || 0).toString(16);
    e += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    e += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (e += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = I(this.a * 255).toString(16);
      e += i.length === 2 ? i : "0" + i;
    }
    return e;
  }
  /** CSS support color pattern */
  toHsl() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      l: this.getLightness(),
      a: this.a
    };
  }
  /** CSS support color pattern */
  toHslString() {
    const e = this.getHue(), n = I(this.getSaturation() * 100), o = I(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${e},${n}%,${o}%,${this.a})` : `hsl(${e},${n}%,${o}%)`;
  }
  /** Same as toHsb */
  toHsv() {
    return {
      h: this.getHue(),
      s: this.getSaturation(),
      v: this.getValue(),
      a: this.a
    };
  }
  toRgb() {
    return {
      r: this.r,
      g: this.g,
      b: this.b,
      a: this.a
    };
  }
  toRgbString() {
    return this.a !== 1 ? `rgba(${this.r},${this.g},${this.b},${this.a})` : `rgb(${this.r},${this.g},${this.b})`;
  }
  toString() {
    return this.toRgbString();
  }
  // ====================== Privates ======================
  /** Return a new FastColor object with one channel changed */
  _sc(e, n, o) {
    const r = this.clone();
    return r[e] = K(n, o), r;
  }
  _c(e) {
    return new this.constructor(e);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(e) {
    const n = e.replace("#", "");
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: e,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = e % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const d = I(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const l = e / 60, c = (1 - Math.abs(2 * o - 1)) * n, f = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = f) : l >= 1 && l < 2 ? (i = f, s = c) : l >= 2 && l < 3 ? (s = c, a = f) : l >= 3 && l < 4 ? (s = f, a = c) : l >= 4 && l < 5 ? (i = f, a = c) : l >= 5 && l < 6 && (i = c, a = f);
    const u = o - c / 2;
    this.r = I((i + u) * 255), this.g = I((s + u) * 255), this.b = I((a + u) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = I(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = e / 60, a = Math.floor(s), l = s - a, c = I(o * (1 - n) * 255), f = I(o * (1 - n * l) * 255), u = I(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = u;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = u, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
        break;
    }
  }
  fromHsvString(e) {
    const n = we(e, gt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(e) {
    const n = we(e, gt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(e) {
    const n = we(e, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? I(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Mn = {
  blue: "#1677FF",
  purple: "#722ED1",
  cyan: "#13C2C2",
  green: "#52C41A",
  magenta: "#EB2F96",
  /**
   * @deprecated Use magenta instead
   */
  pink: "#EB2F96",
  red: "#F5222D",
  orange: "#FA8C16",
  yellow: "#FADB14",
  volcano: "#FA541C",
  geekblue: "#2F54EB",
  gold: "#FAAD14",
  lime: "#A0D911"
}, En = Object.assign(Object.assign({}, Mn), {
  // Color
  colorPrimary: "#1677ff",
  colorSuccess: "#52c41a",
  colorWarning: "#faad14",
  colorError: "#ff4d4f",
  colorInfo: "#1677ff",
  colorLink: "",
  colorTextBase: "",
  colorBgBase: "",
  // Font
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
'Noto Color Emoji'`,
  fontFamilyCode: "'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace",
  fontSize: 14,
  // Line
  lineWidth: 1,
  lineType: "solid",
  // Motion
  motionUnit: 0.1,
  motionBase: 0,
  motionEaseOutCirc: "cubic-bezier(0.08, 0.82, 0.17, 1)",
  motionEaseInOutCirc: "cubic-bezier(0.78, 0.14, 0.15, 0.86)",
  motionEaseOut: "cubic-bezier(0.215, 0.61, 0.355, 1)",
  motionEaseInOut: "cubic-bezier(0.645, 0.045, 0.355, 1)",
  motionEaseOutBack: "cubic-bezier(0.12, 0.4, 0.29, 1.46)",
  motionEaseInBack: "cubic-bezier(0.71, -0.46, 0.88, 0.6)",
  motionEaseInQuint: "cubic-bezier(0.755, 0.05, 0.855, 0.06)",
  motionEaseOutQuint: "cubic-bezier(0.23, 1, 0.32, 1)",
  // Radius
  borderRadius: 6,
  // Size
  sizeUnit: 4,
  sizeStep: 4,
  sizePopupArrow: 16,
  // Control Base
  controlHeight: 32,
  // zIndex
  zIndexBase: 0,
  zIndexPopupBase: 1e3,
  // Image
  opacityImage: 1,
  // Wireframe
  wireframe: !1,
  // Motion
  motion: !0
});
function Te(t) {
  return t >= 0 && t <= 255;
}
function Z(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new X(t).toRgb();
  if (i < 1)
    return t;
  const {
    r: s,
    g: a,
    b: l
  } = new X(e).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((n - s * (1 - c)) / c), u = Math.round((o - a * (1 - c)) / c), d = Math.round((r - l * (1 - c)) / c);
    if (Te(f) && Te(u) && Te(d))
      return new X({
        r: f,
        g: u,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new X({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Pn = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function In(t) {
  const {
    override: e
  } = t, n = Pn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(En).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, f = 1600;
  if (r.motion === !1) {
    const d = "0s";
    r.motionDurationFast = d, r.motionDurationMid = d, r.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: Z(r.colorBorderSecondary, r.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: r.colorTextQuaternary,
    colorTextDisabled: r.colorTextQuaternary,
    colorTextHeading: r.colorText,
    colorTextLabel: r.colorTextSecondary,
    colorTextDescription: r.colorTextTertiary,
    colorTextLightSolid: r.colorWhite,
    colorHighlight: r.colorError,
    colorBgTextHover: r.colorFillSecondary,
    colorBgTextActive: r.colorFill,
    colorIcon: r.colorTextTertiary,
    colorIconHover: r.colorText,
    colorErrorOutline: Z(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Z(r.colorWarningBg, r.colorBgContainer),
    // Font
    fontSizeIcon: r.fontSizeSM,
    // Line
    lineWidthFocus: r.lineWidth * 3,
    // Control
    lineWidth: r.lineWidth,
    controlOutlineWidth: r.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: r.controlHeight / 2,
    controlItemBgHover: r.colorFillTertiary,
    controlItemBgActive: r.colorPrimaryBg,
    controlItemBgActiveHover: r.colorPrimaryBgHover,
    controlItemBgActiveDisabled: r.colorFill,
    controlTmpOutline: r.colorFillQuaternary,
    controlOutline: Z(r.colorPrimaryBg, r.colorBgContainer),
    lineType: r.lineType,
    borderRadius: r.borderRadius,
    borderRadiusXS: r.borderRadiusXS,
    borderRadiusSM: r.borderRadiusSM,
    borderRadiusLG: r.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: r.sizeXXS,
    paddingXS: r.sizeXS,
    paddingSM: r.sizeSM,
    padding: r.size,
    paddingMD: r.sizeMD,
    paddingLG: r.sizeLG,
    paddingXL: r.sizeXL,
    paddingContentHorizontalLG: r.sizeLG,
    paddingContentVerticalLG: r.sizeMS,
    paddingContentHorizontal: r.sizeMS,
    paddingContentVertical: r.sizeSM,
    paddingContentHorizontalSM: r.size,
    paddingContentVerticalSM: r.sizeXS,
    marginXXS: r.sizeXXS,
    marginXS: r.sizeXS,
    marginSM: r.sizeSM,
    margin: r.size,
    marginMD: r.sizeMD,
    marginLG: r.sizeLG,
    marginXL: r.sizeXL,
    marginXXL: r.sizeXXL,
    boxShadow: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowSecondary: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTertiary: `
      0 1px 2px 0 rgba(0, 0, 0, 0.03),
      0 1px 6px -1px rgba(0, 0, 0, 0.02),
      0 2px 4px 0 rgba(0, 0, 0, 0.02)
    `,
    screenXS: i,
    screenXSMin: i,
    screenXSMax: s - 1,
    screenSM: s,
    screenSMMin: s,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new X("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new X("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new X("rgba(0, 0, 0, 0.09)").toRgbString()}
    `,
    boxShadowDrawerRight: `
      -6px 0 16px 0 rgba(0, 0, 0, 0.08),
      -3px 0 6px -4px rgba(0, 0, 0, 0.12),
      -9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerLeft: `
      6px 0 16px 0 rgba(0, 0, 0, 0.08),
      3px 0 6px -4px rgba(0, 0, 0, 0.12),
      9px 0 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerUp: `
      0 6px 16px 0 rgba(0, 0, 0, 0.08),
      0 3px 6px -4px rgba(0, 0, 0, 0.12),
      0 9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowDrawerDown: `
      0 -6px 16px 0 rgba(0, 0, 0, 0.08),
      0 -3px 6px -4px rgba(0, 0, 0, 0.12),
      0 -9px 28px 8px rgba(0, 0, 0, 0.05)
    `,
    boxShadowTabsOverflowLeft: "inset 10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowRight: "inset -10px 0 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowTop: "inset 0 10px 8px -8px rgba(0, 0, 0, 0.08)",
    boxShadowTabsOverflowBottom: "inset 0 -10px 8px -8px rgba(0, 0, 0, 0.08)"
  }), o);
}
const jn = {
  lineHeight: !0,
  lineHeightSM: !0,
  lineHeightLG: !0,
  lineHeightHeading1: !0,
  lineHeightHeading2: !0,
  lineHeightHeading3: !0,
  lineHeightHeading4: !0,
  lineHeightHeading5: !0,
  opacityLoading: !0,
  fontWeightStrong: !0,
  zIndexPopupBase: !0,
  zIndexBase: !0,
  opacityImage: !0
}, kn = {
  size: !0,
  sizeSM: !0,
  sizeLG: !0,
  sizeMD: !0,
  sizeXS: !0,
  sizeXXS: !0,
  sizeMS: !0,
  sizeXL: !0,
  sizeXXL: !0,
  sizeUnit: !0,
  sizeStep: !0,
  motionBase: !0,
  motionUnit: !0
}, Ln = lr(je.defaultAlgorithm), Rn = {
  screenXS: !0,
  screenXSMin: !0,
  screenXSMax: !0,
  screenSM: !0,
  screenSMMin: !0,
  screenSMMax: !0,
  screenMD: !0,
  screenMDMin: !0,
  screenMDMax: !0,
  screenLG: !0,
  screenLGMin: !0,
  screenLGMax: !0,
  screenXL: !0,
  screenXLMin: !0,
  screenXLMax: !0,
  screenXXL: !0,
  screenXXLMin: !0
}, At = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...i
  } = e;
  let s = {
    ...o,
    override: r
  };
  return s = In(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...f
    } = l;
    let u = f;
    c && (u = At({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[a] = u;
  }), s;
};
function Dn() {
  const {
    token: t,
    hashed: e,
    theme: n = Ln,
    override: o,
    cssVar: r
  } = y.useContext(je._internalContext), [i, s, a] = cr(n, [je.defaultSeed, t], {
    salt: `${Zr}-${e || ""}`,
    override: o,
    getComputedToken: At,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: jn,
      ignore: kn,
      preserve: Rn
    }
  });
  return [n, a, e ? s : "", i, r];
}
const {
  genStyleHooks: Hn,
  genComponentStyleHook: io,
  genSubStyleComponent: so
} = On({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = Re();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = Dn();
    return {
      theme: t,
      realToken: e,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: t
    } = Re();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var An = `accept acceptCharset accessKey action allowFullScreen allowTransparency
    alt async autoComplete autoFocus autoPlay capture cellPadding cellSpacing challenge
    charSet checked classID className colSpan cols content contentEditable contextMenu
    controls coords crossOrigin data dateTime default defer dir disabled download draggable
    encType form formAction formEncType formMethod formNoValidate formTarget frameBorder
    headers height hidden high href hrefLang htmlFor httpEquiv icon id inputMode integrity
    is keyParams keyType kind label lang list loop low manifest marginHeight marginWidth max maxLength media
    mediaGroup method min minLength multiple muted name noValidate nonce open
    optimum pattern placeholder poster preload radioGroup readOnly rel required
    reversed role rowSpan rows sandbox scope scoped scrolling seamless selected
    shape size sizes span spellCheck src srcDoc srcLang srcSet start step style
    summary tabIndex target title type useMap value width wmode wrap`, $n = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, zn = "".concat(An, " ").concat($n).split(/[\s\n]+/), Bn = "aria-", Xn = "data-";
function mt(t, e) {
  return t.indexOf(e) === 0;
}
function $t(t) {
  var e = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  e === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : e === !0 ? n = {
    aria: !0
  } : n = L({}, e);
  var o = {};
  return Object.keys(t).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || mt(r, Bn)) || // Data
    n.data && mt(r, Xn) || // Attr
    n.attr && zn.includes(r)) && (o[r] = t[r]);
  }), o;
}
const zt = /* @__PURE__ */ y.createContext(null), pt = ({
  children: t
}) => {
  const {
    prefixCls: e
  } = y.useContext(zt);
  return /* @__PURE__ */ y.createElement("div", {
    className: re(`${e}-group-title`)
  }, t && /* @__PURE__ */ y.createElement(Ct.Text, null, t));
}, Fn = (t) => {
  t.stopPropagation();
}, Vn = (t) => {
  const {
    prefixCls: e,
    info: n,
    className: o,
    direction: r,
    onClick: i,
    active: s,
    menu: a,
    ...l
  } = t, c = $t(l, {
    aria: !0,
    data: !0,
    attr: !0
  }), {
    disabled: f
  } = n, [u, d] = y.useState(!1), [g, m] = y.useState(!1), v = re(o, `${e}-item`, {
    [`${e}-item-active`]: s && !f
  }, {
    [`${e}-item-disabled`]: f
  }), h = () => {
    !f && i && i(n);
  }, b = (S) => {
    S && m(!S);
  };
  return /* @__PURE__ */ y.createElement(or, {
    title: n.label,
    open: u && g,
    onOpenChange: m,
    placement: r === "rtl" ? "left" : "right"
  }, /* @__PURE__ */ y.createElement("li", oe({}, c, {
    className: v,
    onClick: h
  }), n.icon && /* @__PURE__ */ y.createElement("div", {
    className: `${e}-icon`
  }, n.icon), /* @__PURE__ */ y.createElement(Ct.Text, {
    className: `${e}-label`,
    ellipsis: {
      onEllipsis: d
    }
  }, n.label), a && !f && /* @__PURE__ */ y.createElement(ir, {
    menu: a,
    placement: r === "rtl" ? "bottomLeft" : "bottomRight",
    trigger: ["click"],
    disabled: f,
    onOpenChange: b
  }, /* @__PURE__ */ y.createElement(sr, {
    onClick: Fn,
    disabled: f,
    className: `${e}-menu-icon`
  }))));
}, Oe = "__ungrouped", Nn = (t, e = []) => {
  const [n, o, r] = y.useMemo(() => {
    if (!t)
      return [!1, void 0, void 0];
    let i = {
      sort: void 0,
      title: void 0
    };
    return typeof t == "object" && (i = {
      ...i,
      ...t
    }), [!0, i.sort, i.title];
  }, [t]);
  return y.useMemo(() => {
    if (!n)
      return [[{
        name: Oe,
        data: e,
        title: void 0
      }], n];
    const i = e.reduce((l, c) => {
      const f = c.group || Oe;
      return l[f] || (l[f] = []), l[f].push(c), l;
    }, {});
    return [(o ? Object.keys(i).sort(o) : Object.keys(i)).map((l) => ({
      name: l === Oe ? void 0 : l,
      title: r,
      data: i[l]
    })), n];
  }, [e, t]);
}, Gn = (t) => {
  const {
    componentCls: e
  } = t;
  return {
    [e]: {
      display: "flex",
      flexDirection: "column",
      gap: t.paddingXXS,
      overflowY: "auto",
      padding: t.paddingSM,
      [`&${e}-rtl`]: {
        direction: "rtl"
      },
      // 会话列表
      [`& ${e}-list`]: {
        display: "flex",
        gap: t.paddingXXS,
        flexDirection: "column",
        [`& ${e}-item`]: {
          paddingInlineStart: t.paddingXL
        },
        [`& ${e}-label`]: {
          color: t.colorTextDescription
        }
      },
      // 会话列表项
      [`& ${e}-item`]: {
        display: "flex",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        gap: t.paddingXS,
        padding: `0 ${ne(t.paddingXS)}`,
        alignItems: "center",
        borderRadius: t.borderRadiusLG,
        cursor: "pointer",
        transition: `all ${t.motionDurationMid} ${t.motionEaseInOut}`,
        // 悬浮样式
        "&:hover": {
          backgroundColor: t.colorBgTextHover
        },
        // 选中样式
        "&-active": {
          backgroundColor: t.colorBgTextHover,
          [`& ${e}-label, ${e}-menu-icon`]: {
            color: t.colorText
          }
        },
        // 禁用样式
        "&-disabled": {
          cursor: "not-allowed",
          [`& ${e}-label`]: {
            color: t.colorTextDisabled
          }
        },
        // 悬浮、选中时激活操作菜单
        "&:hover, &-active": {
          [`& ${e}-menu-icon`]: {
            opacity: 1
          }
        }
      },
      // 会话名
      [`& ${e}-label`]: {
        flex: 1,
        color: t.colorText
      },
      // 会话操作菜单
      [`& ${e}-menu-icon`]: {
        opacity: 0,
        fontSize: t.fontSizeXL
      },
      // 会话图标
      [`& ${e}-group-title`]: {
        display: "flex",
        alignItems: "center",
        height: t.controlHeightLG,
        minHeight: t.controlHeightLG,
        padding: `0 ${ne(t.paddingXS)}`
      }
    }
  };
}, Un = () => ({}), Wn = Hn("Conversations", (t) => {
  const e = Be(t, {});
  return Gn(e);
}, Un), Kn = (t) => {
  const {
    prefixCls: e,
    rootClassName: n,
    items: o,
    activeKey: r,
    defaultActiveKey: i,
    onActiveChange: s,
    menu: a,
    styles: l = {},
    classNames: c = {},
    groupable: f,
    className: u,
    style: d,
    ...g
  } = t, m = $t(g, {
    attr: !0,
    aria: !0,
    data: !0
  }), [v, h] = cn(i, {
    value: r
  }), [b, S] = Nn(f, o), {
    getPrefixCls: E,
    direction: p
  } = Re(), C = E("conversations", e), x = tn("conversations"), [T, M, P] = Wn(C), R = re(C, x.className, u, n, M, P, {
    [`${C}-rtl`]: p === "rtl"
  }), $ = (_) => {
    h(_.key), s && s(_.key);
  };
  return T(/* @__PURE__ */ y.createElement("ul", oe({}, m, {
    style: {
      ...x.style,
      ...d
    },
    className: R
  }), b.map((_, z) => {
    var D;
    const k = _.data.map((B, W) => /* @__PURE__ */ y.createElement(Vn, {
      key: B.key || `key-${W}`,
      info: B,
      prefixCls: C,
      direction: p,
      className: re(c.item, x.classNames.item),
      style: {
        ...x.styles.item,
        ...l.item
      },
      menu: typeof a == "function" ? a(B) : a,
      active: v === B.key,
      onClick: $
    }));
    return S ? /* @__PURE__ */ y.createElement("li", {
      key: _.name || `key-${z}`
    }, /* @__PURE__ */ y.createElement(zt.Provider, {
      value: {
        prefixCls: C
      }
    }, ((D = _.title) == null ? void 0 : D.call(_, _.name, {
      components: {
        GroupTitle: pt
      }
    })) || /* @__PURE__ */ y.createElement(pt, {
      key: _.name
    }, _.name)), /* @__PURE__ */ y.createElement("ul", {
      className: `${C}-list`
    }, k)) : k;
  })));
};
function qn(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function Qn(t, e = !1) {
  try {
    if (xt(t))
      return t;
    if (e && !qn(t))
      return;
    if (typeof t == "string") {
      let n = t.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function bt(t, e) {
  return Me(() => Qn(t, e), [t, e]);
}
const Jn = ({
  children: t,
  ...e
}) => /* @__PURE__ */ j.jsx(j.Fragment, {
  children: t(e)
});
function Bt(t) {
  return y.createElement(Jn, {
    children: t
  });
}
function Ae(t, e, n) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, i) => {
      var c;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const s = {
        ...r.props,
        key: ((c = r.props) == null ? void 0 : c.key) ?? (n ? `${n}-${i}` : `${i}`)
      };
      let a = s;
      Object.keys(r.slots).forEach((f) => {
        if (!r.slots[f] || !(r.slots[f] instanceof Element) && !r.slots[f].el)
          return;
        const u = f.split(".");
        u.forEach((b, S) => {
          a[b] || (a[b] = {}), S !== u.length - 1 && (a = s[b]);
        });
        const d = r.slots[f];
        let g, m, v = (e == null ? void 0 : e.clone) ?? !1, h = e == null ? void 0 : e.forceClone;
        d instanceof Element ? g = d : (g = d.el, m = d.callback, v = d.clone ?? v, h = d.forceClone ?? h), h = h ?? !!m, a[u[u.length - 1]] = g ? m ? (...b) => (m(u[u.length - 1], b), /* @__PURE__ */ j.jsx(Ie, {
          ...r.ctx,
          params: b,
          forceClone: h,
          children: /* @__PURE__ */ j.jsx(Q, {
            slot: g,
            clone: v
          })
        })) : Bt((b) => /* @__PURE__ */ j.jsx(Ie, {
          ...r.ctx,
          forceClone: h,
          children: /* @__PURE__ */ j.jsx(Q, {
            slot: g,
            clone: v,
            ...b
          })
        })) : a[u[u.length - 1]], a = s;
      });
      const l = (e == null ? void 0 : e.children) || "children";
      return r[l] ? s[l] = Ae(r[l], e, `${i}`) : e != null && e.children && (s[l] = void 0, Reflect.deleteProperty(s, l)), s;
    });
}
function yt(t, e) {
  return t ? e != null && e.forceClone || e != null && e.params ? Bt((n) => /* @__PURE__ */ j.jsx(Ie, {
    forceClone: e == null ? void 0 : e.forceClone,
    params: e == null ? void 0 : e.params,
    children: /* @__PURE__ */ j.jsx(Q, {
      slot: t,
      clone: e == null ? void 0 : e.clone,
      ...n
    })
  })) : /* @__PURE__ */ j.jsx(Q, {
    slot: t,
    clone: e == null ? void 0 : e.clone
  }) : null;
}
function vt({
  key: t,
  slots: e,
  targets: n
}, o) {
  return e[t] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ j.jsx(y.Fragment, {
    children: yt(i, {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ j.jsx(j.Fragment, {
    children: yt(e[t], {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const {
  useItems: Zn,
  withItemsContextProvider: Yn,
  ItemHandler: ao
} = St("antd-menu-items"), {
  useItems: eo,
  withItemsContextProvider: to,
  ItemHandler: lo
} = St("antdx-conversations-items");
function ro(t) {
  return typeof t == "object" && t !== null ? t : {};
}
function no(t, e) {
  return Object.keys(t).reduce((n, o) => {
    if (o.startsWith("on") && xt(t[o])) {
      const r = t[o];
      n[o] = (...i) => {
        r == null || r(e, ...i);
      };
    } else
      n[o] = t[o];
    return n;
  }, {});
}
const co = Wr(Yn(["menu.items"], to(["default", "items"], ({
  slots: t,
  setSlotParams: e,
  children: n,
  items: o,
  ...r
}) => {
  const {
    items: {
      "menu.items": i
    }
  } = Zn(), s = bt(r.menu), a = typeof r.groupable == "object" || t["groupable.title"], l = ro(r.groupable), c = bt(r.groupable), f = Me(() => {
    var g;
    if (typeof r.menu == "string")
      return s;
    {
      const m = r.menu || {};
      return ((g = m.items) == null ? void 0 : g.length) || i.length > 0 ? (h) => ({
        ...no(m, h),
        items: m.items || Ae(i, {
          clone: !0
        }) || [],
        expandIcon: t["menu.expandIcon"] ? vt({
          slots: t,
          setSlotParams: e,
          key: "menu.expandIcon"
        }, {
          clone: !0
        }) : m.expandIcon,
        overflowedIndicator: t["menu.overflowedIndicator"] ? /* @__PURE__ */ j.jsx(Q, {
          slot: t["menu.overflowedIndicator"]
        }) : m.overflowedIndicator
      }) : void 0;
    }
  }, [s, i, r.menu, e, t]), {
    items: u
  } = eo(), d = u.items.length > 0 ? u.items : u.default;
  return /* @__PURE__ */ j.jsxs(j.Fragment, {
    children: [/* @__PURE__ */ j.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ j.jsx(Kn, {
      ...r,
      menu: f,
      items: Me(() => o || Ae(d, {
        clone: !0
      }), [o, d]),
      groupable: a ? {
        ...l,
        title: t["groupable.title"] ? vt({
          slots: t,
          setSlotParams: e,
          key: "groupable.title"
        }) : l.title,
        sort: c || l.sort
      } : r.groupable
    })]
  });
})));
export {
  co as Conversations,
  co as default
};
