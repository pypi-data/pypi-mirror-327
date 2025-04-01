import { i as Vt, a as Te, r as Xt, b as Nt, g as Ut, w as Y, c as $e, d as mt } from "./Index-CoteDY5A.js";
const V = window.ms_globals.React, w = window.ms_globals.React, dt = window.ms_globals.React.forwardRef, gt = window.ms_globals.React.useRef, pt = window.ms_globals.React.useState, $t = window.ms_globals.React.useEffect, Q = window.ms_globals.React.useMemo, we = window.ms_globals.ReactDOM.createPortal, Wt = window.ms_globals.internalContext.useContextPropsContext, Ve = window.ms_globals.internalContext.ContextPropsProvider, Gt = window.ms_globals.internalContext.SuggestionContext, Kt = window.ms_globals.createItemsContext.createItemsContext, qt = window.ms_globals.antd.ConfigProvider, Oe = window.ms_globals.antd.theme, Qt = window.ms_globals.antd.Cascader, Jt = window.ms_globals.antd.Flex, Xe = window.ms_globals.antdCssinjs.unit, be = window.ms_globals.antdCssinjs.token2CSSVar, Ne = window.ms_globals.antdCssinjs.useStyleRegister, Zt = window.ms_globals.antdCssinjs.useCSSVarRegister, Yt = window.ms_globals.antdCssinjs.createTheme, er = window.ms_globals.antdCssinjs.useCacheToken;
var tr = /\s/;
function rr(t) {
  for (var e = t.length; e-- && tr.test(t.charAt(e)); )
    ;
  return e;
}
var nr = /^\s+/;
function or(t) {
  return t && t.slice(0, rr(t) + 1).replace(nr, "");
}
var Ue = NaN, sr = /^[-+]0x[0-9a-f]+$/i, ir = /^0b[01]+$/i, ar = /^0o[0-7]+$/i, cr = parseInt;
function We(t) {
  if (typeof t == "number")
    return t;
  if (Vt(t))
    return Ue;
  if (Te(t)) {
    var e = typeof t.valueOf == "function" ? t.valueOf() : t;
    t = Te(e) ? e + "" : e;
  }
  if (typeof t != "string")
    return t === 0 ? t : +t;
  t = or(t);
  var n = ir.test(t);
  return n || ar.test(t) ? cr(t.slice(2), n ? 2 : 8) : sr.test(t) ? Ue : +t;
}
var ve = function() {
  return Xt.Date.now();
}, lr = "Expected a function", ur = Math.max, fr = Math.min;
function hr(t, e, n) {
  var o, r, s, i, a, c, l = 0, h = !1, u = !1, d = !0;
  if (typeof t != "function")
    throw new TypeError(lr);
  e = We(e) || 0, Te(n) && (h = !!n.leading, u = "maxWait" in n, s = u ? ur(We(n.maxWait) || 0, e) : s, d = "trailing" in n ? !!n.trailing : d);
  function f(S) {
    var O = o, _ = r;
    return o = r = void 0, l = S, i = t.apply(_, O), i;
  }
  function b(S) {
    return l = S, a = setTimeout(m, e), h ? f(S) : i;
  }
  function p(S) {
    var O = S - c, _ = S - l, E = e - O;
    return u ? fr(E, s - _) : E;
  }
  function g(S) {
    var O = S - c, _ = S - l;
    return c === void 0 || O >= e || O < 0 || u && _ >= s;
  }
  function m() {
    var S = ve();
    if (g(S))
      return y(S);
    a = setTimeout(m, p(S));
  }
  function y(S) {
    return a = void 0, d && o ? f(S) : (o = r = void 0, i);
  }
  function C() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = r = a = void 0;
  }
  function v() {
    return a === void 0 ? i : y(ve());
  }
  function T() {
    var S = ve(), O = g(S);
    if (o = arguments, r = this, c = S, O) {
      if (a === void 0)
        return b(c);
      if (u)
        return clearTimeout(a), a = setTimeout(m, e), f(c);
    }
    return a === void 0 && (a = setTimeout(m, e)), i;
  }
  return T.cancel = C, T.flush = v, T;
}
function dr(t, e) {
  return Nt(t, e);
}
var bt = {
  exports: {}
}, oe = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var gr = w, pr = Symbol.for("react.element"), mr = Symbol.for("react.fragment"), br = Object.prototype.hasOwnProperty, vr = gr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, yr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function vt(t, e, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), e.key !== void 0 && (s = "" + e.key), e.ref !== void 0 && (i = e.ref);
  for (o in e) br.call(e, o) && !yr.hasOwnProperty(o) && (r[o] = e[o]);
  if (t && t.defaultProps) for (o in e = t.defaultProps, e) r[o] === void 0 && (r[o] = e[o]);
  return {
    $$typeof: pr,
    type: t,
    key: s,
    ref: i,
    props: r,
    _owner: vr.current
  };
}
oe.Fragment = mr;
oe.jsx = vt;
oe.jsxs = vt;
bt.exports = oe;
var A = bt.exports;
const {
  SvelteComponent: Sr,
  assign: Ge,
  binding_callbacks: Ke,
  check_outros: xr,
  children: yt,
  claim_element: St,
  claim_space: Cr,
  component_subscribe: qe,
  compute_slots: _r,
  create_slot: wr,
  detach: G,
  element: xt,
  empty: Qe,
  exclude_internal_props: Je,
  get_all_dirty_from_scope: Tr,
  get_slot_changes: Or,
  group_outros: Mr,
  init: Pr,
  insert_hydration: ee,
  safe_not_equal: Er,
  set_custom_element_data: Ct,
  space: kr,
  transition_in: te,
  transition_out: Me,
  update_slot_base: Ir
} = window.__gradio__svelte__internal, {
  beforeUpdate: jr,
  getContext: Rr,
  onDestroy: Lr,
  setContext: Ar
} = window.__gradio__svelte__internal;
function Ze(t) {
  let e, n;
  const o = (
    /*#slots*/
    t[7].default
  ), r = wr(
    o,
    t,
    /*$$scope*/
    t[6],
    null
  );
  return {
    c() {
      e = xt("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      e = St(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = yt(e);
      r && r.l(i), i.forEach(G), this.h();
    },
    h() {
      Ct(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      ee(s, e, i), r && r.m(e, null), t[9](e), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && Ir(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Or(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : Tr(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (te(r, s), n = !0);
    },
    o(s) {
      Me(r, s), n = !1;
    },
    d(s) {
      s && G(e), r && r.d(s), t[9](null);
    }
  };
}
function Dr(t) {
  let e, n, o, r, s = (
    /*$$slots*/
    t[4].default && Ze(t)
  );
  return {
    c() {
      e = xt("react-portal-target"), n = kr(), s && s.c(), o = Qe(), this.h();
    },
    l(i) {
      e = St(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), yt(e).forEach(G), n = Cr(i), s && s.l(i), o = Qe(), this.h();
    },
    h() {
      Ct(e, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      ee(i, e, a), t[8](e), ee(i, n, a), s && s.m(i, a), ee(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && te(s, 1)) : (s = Ze(i), s.c(), te(s, 1), s.m(o.parentNode, o)) : s && (Mr(), Me(s, 1, 1, () => {
        s = null;
      }), xr());
    },
    i(i) {
      r || (te(s), r = !0);
    },
    o(i) {
      Me(s), r = !1;
    },
    d(i) {
      i && (G(e), G(n), G(o)), t[8](null), s && s.d(i);
    }
  };
}
function Ye(t) {
  const {
    svelteInit: e,
    ...n
  } = t;
  return n;
}
function Hr(t, e, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = e;
  const a = _r(s);
  let {
    svelteInit: c
  } = e;
  const l = Y(Ye(e)), h = Y();
  qe(t, h, (v) => n(0, o = v));
  const u = Y();
  qe(t, u, (v) => n(1, r = v));
  const d = [], f = Rr("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: p,
    subSlotIndex: g
  } = Ut() || {}, m = c({
    parent: f,
    props: l,
    target: h,
    slot: u,
    slotKey: b,
    slotIndex: p,
    subSlotIndex: g,
    onDestroy(v) {
      d.push(v);
    }
  });
  Ar("$$ms-gr-react-wrapper", m), jr(() => {
    l.set(Ye(e));
  }), Lr(() => {
    d.forEach((v) => v());
  });
  function y(v) {
    Ke[v ? "unshift" : "push"](() => {
      o = v, h.set(o);
    });
  }
  function C(v) {
    Ke[v ? "unshift" : "push"](() => {
      r = v, u.set(r);
    });
  }
  return t.$$set = (v) => {
    n(17, e = Ge(Ge({}, e), Je(v))), "svelteInit" in v && n(5, c = v.svelteInit), "$$scope" in v && n(6, i = v.$$scope);
  }, e = Je(e), [o, r, h, u, a, c, i, s, y, C];
}
class zr extends Sr {
  constructor(e) {
    super(), Pr(this, e, Hr, Dr, Er, {
      svelteInit: 5
    });
  }
}
const et = window.ms_globals.rerender, ye = window.ms_globals.tree;
function Br(t, e = {}) {
  function n(o) {
    const r = Y(), s = new zr({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: t,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: e.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, c = i.parent ?? ye;
          return c.nodes = [...c.nodes, a], et({
            createPortal: we,
            node: ye
          }), i.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== r), et({
              createPortal: we,
              node: ye
            });
          }), a;
        },
        ...o.props
      }
    });
    return r.set(s), s;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(n);
    });
  });
}
const Fr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function $r(t) {
  return t ? Object.keys(t).reduce((e, n) => {
    const o = t[n];
    return e[n] = Vr(n, o), e;
  }, {}) : {};
}
function Vr(t, e) {
  return typeof e == "number" && !Fr.includes(t) ? e + "px" : e;
}
function Pe(t) {
  const e = [], n = t.cloneNode(!1);
  if (t._reactElement) {
    const r = w.Children.toArray(t._reactElement.props.children).map((s) => {
      if (w.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = Pe(s.props.el);
        return w.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...w.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = t._reactElement.props.children, e.push(we(w.cloneElement(t._reactElement, {
      ...t._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: e
    };
  }
  Object.keys(t.getEventListeners()).forEach((r) => {
    t.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, i, c);
    });
  });
  const o = Array.from(t.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = Pe(s);
      e.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: e
  };
}
function Xr(t, e) {
  t && (typeof t == "function" ? t(e) : t.current = e);
}
const Ee = dt(({
  slot: t,
  clone: e,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = gt(), [a, c] = pt([]), {
    forceClone: l
  } = Wt(), h = l ? !0 : e;
  return $t(() => {
    var p;
    if (!i.current || !t)
      return;
    let u = t;
    function d() {
      let g = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (g = u.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Xr(s, g), n && g.classList.add(...n.split(" ")), o) {
        const m = $r(o);
        Object.keys(m).forEach((y) => {
          g.style[y] = m[y];
        });
      }
    }
    let f = null, b = null;
    if (h && window.MutationObserver) {
      let g = function() {
        var v, T, S;
        (v = i.current) != null && v.contains(u) && ((T = i.current) == null || T.removeChild(u));
        const {
          portals: y,
          clonedElement: C
        } = Pe(t);
        u = C, c(y), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          d();
        }, 50), (S = i.current) == null || S.appendChild(u);
      };
      g();
      const m = hr(() => {
        g(), f == null || f.disconnect(), f == null || f.observe(t, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      f = new window.MutationObserver(m), f.observe(t, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (p = i.current) == null || p.appendChild(u);
    return () => {
      var g, m;
      u.style.display = "", (g = i.current) != null && g.contains(u) && ((m = i.current) == null || m.removeChild(u)), f == null || f.disconnect();
    };
  }, [t, h, n, o, s, r]), w.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
}), Nr = "1.0.5", Ur = /* @__PURE__ */ w.createContext({}), Wr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Gr = (t) => {
  const e = w.useContext(Ur);
  return w.useMemo(() => ({
    ...Wr,
    ...e[t]
  }), [e[t]]);
};
function ke() {
  const {
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = w.useContext(qt.ConfigContext);
  return {
    theme: r,
    getPrefixCls: t,
    direction: e,
    csp: n,
    iconPrefixCls: o
  };
}
function re(t) {
  var e = V.useRef();
  e.current = t;
  var n = V.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = e.current) === null || o === void 0 ? void 0 : o.call.apply(o, [e].concat(s));
  }, []);
  return n;
}
function Kr(t) {
  if (Array.isArray(t)) return t;
}
function qr(t, e) {
  var n = t == null ? null : typeof Symbol < "u" && t[Symbol.iterator] || t["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], c = !0, l = !1;
    try {
      if (s = (n = n.call(t)).next, e === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (o = s.call(n)).done) && (a.push(o.value), a.length !== e); c = !0) ;
    } catch (h) {
      l = !0, r = h;
    } finally {
      try {
        if (!c && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (l) throw r;
      }
    }
    return a;
  }
}
function tt(t, e) {
  (e == null || e > t.length) && (e = t.length);
  for (var n = 0, o = Array(e); n < e; n++) o[n] = t[n];
  return o;
}
function Qr(t, e) {
  if (t) {
    if (typeof t == "string") return tt(t, e);
    var n = {}.toString.call(t).slice(8, -1);
    return n === "Object" && t.constructor && (n = t.constructor.name), n === "Map" || n === "Set" ? Array.from(t) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? tt(t, e) : void 0;
  }
}
function Jr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function N(t, e) {
  return Kr(t) || qr(t, e) || Qr(t, e) || Jr();
}
function Zr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var rt = Zr() ? V.useLayoutEffect : V.useEffect, Yr = function(e, n) {
  var o = V.useRef(!0);
  rt(function() {
    return e(o.current);
  }, n), rt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, nt = function(e, n) {
  Yr(function(o) {
    if (!o)
      return e();
  }, n);
};
function ot(t) {
  var e = V.useRef(!1), n = V.useState(t), o = N(n, 2), r = o[0], s = o[1];
  V.useEffect(function() {
    return e.current = !1, function() {
      e.current = !0;
    };
  }, []);
  function i(a, c) {
    c && e.current || s(a);
  }
  return [r, i];
}
function Se(t) {
  return t !== void 0;
}
function en(t, e) {
  var n = e || {}, o = n.defaultValue, r = n.value, s = n.onChange, i = n.postState, a = ot(function() {
    return Se(r) ? r : Se(o) ? typeof o == "function" ? o() : o : t;
  }), c = N(a, 2), l = c[0], h = c[1], u = r !== void 0 ? r : l, d = i ? i(u) : u, f = re(s), b = ot([u]), p = N(b, 2), g = p[0], m = p[1];
  nt(function() {
    var C = g[0];
    l !== C && f(l, C);
  }, [g]), nt(function() {
    Se(r) || h(r);
  }, [r]);
  var y = re(function(C, v) {
    h(C, v), m([u], v);
  });
  return [d, y];
}
function z(t) {
  "@babel/helpers - typeof";
  return z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(e) {
    return typeof e;
  } : function(e) {
    return e && typeof Symbol == "function" && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e;
  }, z(t);
}
var x = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Re = Symbol.for("react.element"), Le = Symbol.for("react.portal"), se = Symbol.for("react.fragment"), ie = Symbol.for("react.strict_mode"), ae = Symbol.for("react.profiler"), ce = Symbol.for("react.provider"), le = Symbol.for("react.context"), tn = Symbol.for("react.server_context"), ue = Symbol.for("react.forward_ref"), fe = Symbol.for("react.suspense"), he = Symbol.for("react.suspense_list"), de = Symbol.for("react.memo"), ge = Symbol.for("react.lazy"), rn = Symbol.for("react.offscreen"), _t;
_t = Symbol.for("react.module.reference");
function H(t) {
  if (typeof t == "object" && t !== null) {
    var e = t.$$typeof;
    switch (e) {
      case Re:
        switch (t = t.type, t) {
          case se:
          case ae:
          case ie:
          case fe:
          case he:
            return t;
          default:
            switch (t = t && t.$$typeof, t) {
              case tn:
              case le:
              case ue:
              case ge:
              case de:
              case ce:
                return t;
              default:
                return e;
            }
        }
      case Le:
        return e;
    }
  }
}
x.ContextConsumer = le;
x.ContextProvider = ce;
x.Element = Re;
x.ForwardRef = ue;
x.Fragment = se;
x.Lazy = ge;
x.Memo = de;
x.Portal = Le;
x.Profiler = ae;
x.StrictMode = ie;
x.Suspense = fe;
x.SuspenseList = he;
x.isAsyncMode = function() {
  return !1;
};
x.isConcurrentMode = function() {
  return !1;
};
x.isContextConsumer = function(t) {
  return H(t) === le;
};
x.isContextProvider = function(t) {
  return H(t) === ce;
};
x.isElement = function(t) {
  return typeof t == "object" && t !== null && t.$$typeof === Re;
};
x.isForwardRef = function(t) {
  return H(t) === ue;
};
x.isFragment = function(t) {
  return H(t) === se;
};
x.isLazy = function(t) {
  return H(t) === ge;
};
x.isMemo = function(t) {
  return H(t) === de;
};
x.isPortal = function(t) {
  return H(t) === Le;
};
x.isProfiler = function(t) {
  return H(t) === ae;
};
x.isStrictMode = function(t) {
  return H(t) === ie;
};
x.isSuspense = function(t) {
  return H(t) === fe;
};
x.isSuspenseList = function(t) {
  return H(t) === he;
};
x.isValidElementType = function(t) {
  return typeof t == "string" || typeof t == "function" || t === se || t === ae || t === ie || t === fe || t === he || t === rn || typeof t == "object" && t !== null && (t.$$typeof === ge || t.$$typeof === de || t.$$typeof === ce || t.$$typeof === le || t.$$typeof === ue || t.$$typeof === _t || t.getModuleId !== void 0);
};
x.typeOf = H;
function nn(t, e) {
  if (z(t) != "object" || !t) return t;
  var n = t[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(t, e || "default");
    if (z(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (e === "string" ? String : Number)(t);
}
function wt(t) {
  var e = nn(t, "string");
  return z(e) == "symbol" ? e : e + "";
}
function M(t, e, n) {
  return (e = wt(e)) in t ? Object.defineProperty(t, e, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : t[e] = n, t;
}
function st(t, e) {
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
    e % 2 ? st(Object(n), !0).forEach(function(o) {
      M(t, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(t, Object.getOwnPropertyDescriptors(n)) : st(Object(n)).forEach(function(o) {
      Object.defineProperty(t, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return t;
}
function pe(t, e) {
  if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function");
}
function on(t, e) {
  for (var n = 0; n < e.length; n++) {
    var o = e[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(t, wt(o.key), o);
  }
}
function me(t, e, n) {
  return e && on(t.prototype, e), Object.defineProperty(t, "prototype", {
    writable: !1
  }), t;
}
function Ie(t, e) {
  return Ie = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Ie(t, e);
}
function Tt(t, e) {
  if (typeof e != "function" && e !== null) throw new TypeError("Super expression must either be null or a function");
  t.prototype = Object.create(e && e.prototype, {
    constructor: {
      value: t,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(t, "prototype", {
    writable: !1
  }), e && Ie(t, e);
}
function ne(t) {
  return ne = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(e) {
    return e.__proto__ || Object.getPrototypeOf(e);
  }, ne(t);
}
function Ot() {
  try {
    var t = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Ot = function() {
    return !!t;
  })();
}
function q(t) {
  if (t === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return t;
}
function sn(t, e) {
  if (e && (z(e) == "object" || typeof e == "function")) return e;
  if (e !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return q(t);
}
function Mt(t) {
  var e = Ot();
  return function() {
    var n, o = ne(t);
    if (e) {
      var r = ne(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return sn(this, n);
  };
}
var Pt = /* @__PURE__ */ me(function t() {
  pe(this, t);
}), Et = "CALC_UNIT", an = new RegExp(Et, "g");
function xe(t) {
  return typeof t == "number" ? "".concat(t).concat(Et) : t;
}
var cn = /* @__PURE__ */ function(t) {
  Tt(n, t);
  var e = Mt(n);
  function n(o, r) {
    var s;
    pe(this, n), s = e.call(this), M(q(s), "result", ""), M(q(s), "unitlessCssVar", void 0), M(q(s), "lowPriority", void 0);
    var i = z(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = xe(o) : i === "string" && (s.result = o), s;
  }
  return me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(xe(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(xe(r))), this.lowPriority = !0, this;
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
      var s = this, i = r || {}, a = i.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return s.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(an, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Pt), ln = /* @__PURE__ */ function(t) {
  Tt(n, t);
  var e = Mt(n);
  function n(o) {
    var r;
    return pe(this, n), r = e.call(this), M(q(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return me(n, [{
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
}(Pt), un = function(e, n) {
  var o = e === "css" ? cn : ln;
  return function(r) {
    return new o(r, n);
  };
}, it = function(e, n) {
  return "".concat([n, e.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function at(t, e, n, o) {
  var r = L({}, e[t]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var c = N(a, 2), l = c[0], h = c[1];
      if (r != null && r[l] || r != null && r[h]) {
        var u;
        (u = r[h]) !== null && u !== void 0 || (r[h] = r == null ? void 0 : r[l]);
      }
    });
  }
  var i = L(L({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === e[a] && delete i[a];
  }), i;
}
var kt = typeof CSSINJS_STATISTIC < "u", je = !0;
function Ae() {
  for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++)
    e[n] = arguments[n];
  if (!kt)
    return Object.assign.apply(Object, [{}].concat(e));
  je = !1;
  var o = {};
  return e.forEach(function(r) {
    if (z(r) === "object") {
      var s = Object.keys(r);
      s.forEach(function(i) {
        Object.defineProperty(o, i, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return r[i];
          }
        });
      });
    }
  }), je = !0, o;
}
var ct = {};
function fn() {
}
var hn = function(e) {
  var n, o = e, r = fn;
  return kt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(e, {
    get: function(i, a) {
      if (je) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var c;
    ct[i] = {
      global: Array.from(n),
      component: L(L({}, (c = ct[i]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function lt(t, e, n) {
  if (typeof n == "function") {
    var o;
    return n(Ae(e, (o = e[t]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function dn(t) {
  return t === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return Xe(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return Xe(s);
      }).join(","), ")");
    }
  };
}
var gn = 1e3 * 60 * 10, pn = /* @__PURE__ */ function() {
  function t() {
    pe(this, t), M(this, "map", /* @__PURE__ */ new Map()), M(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), M(this, "nextID", 0), M(this, "lastAccessBeat", /* @__PURE__ */ new Map()), M(this, "accessBeat", 0);
  }
  return me(t, [{
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
      var o = this, r = n.map(function(s) {
        return s && z(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(z(s), "_").concat(s);
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
        this.lastAccessBeat.forEach(function(r, s) {
          o - r > gn && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), t;
}(), ut = new pn();
function mn(t, e) {
  return w.useMemo(function() {
    var n = ut.get(e);
    if (n)
      return n;
    var o = t();
    return ut.set(e, o), o;
  }, e);
}
var bn = function() {
  return {};
};
function vn(t) {
  var e = t.useCSP, n = e === void 0 ? bn : e, o = t.useToken, r = t.usePrefix, s = t.getResetStyles, i = t.getCommonStyle, a = t.getCompUnitless;
  function c(d, f, b, p) {
    var g = Array.isArray(d) ? d[0] : d;
    function m(_) {
      return "".concat(String(g)).concat(_.slice(0, 1).toUpperCase()).concat(_.slice(1));
    }
    var y = (p == null ? void 0 : p.unitless) || {}, C = typeof a == "function" ? a(d) : {}, v = L(L({}, C), {}, M({}, m("zIndexPopup"), !0));
    Object.keys(y).forEach(function(_) {
      v[m(_)] = y[_];
    });
    var T = L(L({}, p), {}, {
      unitless: v,
      prefixToken: m
    }), S = h(d, f, b, T), O = l(g, b, T);
    return function(_) {
      var E = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _, j = S(_, E), B = N(j, 2), k = B[1], F = O(E), R = N(F, 2), D = R[0], U = R[1];
      return [D, k, U];
    };
  }
  function l(d, f, b) {
    var p = b.unitless, g = b.injectStyle, m = g === void 0 ? !0 : g, y = b.prefixToken, C = b.ignore, v = function(O) {
      var _ = O.rootCls, E = O.cssVar, j = E === void 0 ? {} : E, B = o(), k = B.realToken;
      return Zt({
        path: [d],
        prefix: j.prefix,
        key: j.key,
        unitless: p,
        ignore: C,
        token: k,
        scope: _
      }, function() {
        var F = lt(d, k, f), R = at(d, k, F, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(F).forEach(function(D) {
          R[y(D)] = R[D], delete R[D];
        }), R;
      }), null;
    }, T = function(O) {
      var _ = o(), E = _.cssVar;
      return [function(j) {
        return m && E ? /* @__PURE__ */ w.createElement(w.Fragment, null, /* @__PURE__ */ w.createElement(v, {
          rootCls: O,
          cssVar: E,
          component: d
        }), j) : j;
      }, E == null ? void 0 : E.key];
    };
    return T;
  }
  function h(d, f, b) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], m = N(g, 1), y = m[0], C = g.join("-"), v = t.layer || {
      name: "antd"
    };
    return function(T) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : T, O = o(), _ = O.theme, E = O.realToken, j = O.hashId, B = O.token, k = O.cssVar, F = r(), R = F.rootPrefixCls, D = F.iconPrefixCls, U = n(), P = k ? "css" : "js", Rt = mn(function() {
        var X = /* @__PURE__ */ new Set();
        return k && Object.keys(p.unitless || {}).forEach(function(J) {
          X.add(be(J, k.prefix)), X.add(be(J, it(y, k.prefix)));
        }), un(P, X);
      }, [P, y, k == null ? void 0 : k.prefix]), De = dn(P), Lt = De.max, At = De.min, He = {
        theme: _,
        token: B,
        hashId: j,
        nonce: function() {
          return U.nonce;
        },
        clientOnly: p.clientOnly,
        layer: v,
        // antd is always at top of styles
        order: p.order || -999
      };
      typeof s == "function" && Ne(L(L({}, He), {}, {
        clientOnly: !1,
        path: ["Shared", R]
      }), function() {
        return s(B, {
          prefix: {
            rootPrefixCls: R,
            iconPrefixCls: D
          },
          csp: U
        });
      });
      var Dt = Ne(L(L({}, He), {}, {
        path: [C, T, D]
      }), function() {
        if (p.injectStyle === !1)
          return [];
        var X = hn(B), J = X.token, Ht = X.flush, W = lt(y, E, b), zt = ".".concat(T), ze = at(y, E, W, {
          deprecatedTokens: p.deprecatedTokens
        });
        k && W && z(W) === "object" && Object.keys(W).forEach(function(Fe) {
          W[Fe] = "var(".concat(be(Fe, it(y, k.prefix)), ")");
        });
        var Be = Ae(J, {
          componentCls: zt,
          prefixCls: T,
          iconCls: ".".concat(D),
          antCls: ".".concat(R),
          calc: Rt,
          // @ts-ignore
          max: Lt,
          // @ts-ignore
          min: At
        }, k ? W : ze), Bt = f(Be, {
          hashId: j,
          prefixCls: T,
          rootPrefixCls: R,
          iconPrefixCls: D
        });
        Ht(y, ze);
        var Ft = typeof i == "function" ? i(Be, T, S, p.resetFont) : null;
        return [p.resetStyle === !1 ? null : Ft, Bt];
      });
      return [Dt, j];
    };
  }
  function u(d, f, b) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = h(d, f, b, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, p)), m = function(C) {
      var v = C.prefixCls, T = C.rootCls, S = T === void 0 ? v : T;
      return g(v, S), null;
    };
    return m;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: u,
    genComponentStyleHook: h
  };
}
const I = Math.round;
function Ce(t, e) {
  const n = t.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = e(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const ft = (t, e, n) => n === 0 ? t : t / 100;
function K(t, e) {
  const n = e || 255;
  return t > n ? n : t < 0 ? 0 : t;
}
class $ {
  constructor(e) {
    M(this, "isValid", !0), M(this, "r", 0), M(this, "g", 0), M(this, "b", 0), M(this, "a", 1), M(this, "_h", void 0), M(this, "_s", void 0), M(this, "_l", void 0), M(this, "_v", void 0), M(this, "_max", void 0), M(this, "_min", void 0), M(this, "_brightness", void 0);
    function n(o) {
      return o[0] in e && o[1] in e && o[2] in e;
    }
    if (e) if (typeof e == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = e.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (e instanceof $)
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
    function e(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
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
    const o = this._c(e), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: I(s("r")),
      g: I(s("g")),
      b: I(s("b")),
      a: I(s("a") * 100) / 100
    };
    return this._c(i);
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
    const n = this._c(e), o = this.a + n.a * (1 - this.a), r = (s) => I((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
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
      const s = I(this.a * 255).toString(16);
      e += s.length === 2 ? s : "0" + s;
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
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
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
    let s = 0, i = 0, a = 0;
    const c = e / 60, l = (1 - Math.abs(2 * o - 1)) * n, h = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (s = l, i = h) : c >= 1 && c < 2 ? (s = h, i = l) : c >= 2 && c < 3 ? (i = l, a = h) : c >= 3 && c < 4 ? (i = h, a = l) : c >= 4 && c < 5 ? (s = h, a = l) : c >= 5 && c < 6 && (s = l, a = h);
    const u = o - l / 2;
    this.r = I((s + u) * 255), this.g = I((i + u) * 255), this.b = I((a + u) * 255);
  }
  fromHsv({
    h: e,
    s: n,
    v: o,
    a: r
  }) {
    this._h = e % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = I(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = e / 60, a = Math.floor(i), c = i - a, l = I(o * (1 - n) * 255), h = I(o * (1 - n * c) * 255), u = I(o * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = l;
        break;
      case 1:
        this.r = h, this.b = l;
        break;
      case 2:
        this.r = l, this.b = u;
        break;
      case 3:
        this.r = l, this.g = h;
        break;
      case 4:
        this.r = u, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = h;
        break;
    }
  }
  fromHsvString(e) {
    const n = Ce(e, ft);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(e) {
    const n = Ce(e, ft);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(e) {
    const n = Ce(e, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? I(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const yn = {
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
}, Sn = Object.assign(Object.assign({}, yn), {
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
function _e(t) {
  return t >= 0 && t <= 255;
}
function Z(t, e) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new $(t).toRgb();
  if (s < 1)
    return t;
  const {
    r: i,
    g: a,
    b: c
  } = new $(e).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const h = Math.round((n - i * (1 - l)) / l), u = Math.round((o - a * (1 - l)) / l), d = Math.round((r - c * (1 - l)) / l);
    if (_e(h) && _e(u) && _e(d))
      return new $({
        r: h,
        g: u,
        b: d,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new $({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var xn = function(t, e) {
  var n = {};
  for (var o in t) Object.prototype.hasOwnProperty.call(t, o) && e.indexOf(o) < 0 && (n[o] = t[o]);
  if (t != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(t); r < o.length; r++)
    e.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(t, o[r]) && (n[o[r]] = t[o[r]]);
  return n;
};
function Cn(t) {
  const {
    override: e
  } = t, n = xn(t, ["override"]), o = Object.assign({}, e);
  Object.keys(Sn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, c = 992, l = 1200, h = 1600;
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
    screenXS: s,
    screenXSMin: s,
    screenXSMax: i - 1,
    screenSM: i,
    screenSMMin: i,
    screenSMMax: a - 1,
    screenMD: a,
    screenMDMin: a,
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: h - 1,
    screenXXL: h,
    screenXXLMin: h,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new $("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new $("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new $("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const _n = {
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
}, wn = {
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
}, Tn = Yt(Oe.defaultAlgorithm), On = {
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
}, It = (t, e, n) => {
  const o = n.getDerivativeToken(t), {
    override: r,
    ...s
  } = e;
  let i = {
    ...o,
    override: r
  };
  return i = Cn(i), s && Object.entries(s).forEach(([a, c]) => {
    const {
      theme: l,
      ...h
    } = c;
    let u = h;
    l && (u = It({
      ...i,
      ...h
    }, {
      override: h
    }, l)), i[a] = u;
  }), i;
};
function Mn() {
  const {
    token: t,
    hashed: e,
    theme: n = Tn,
    override: o,
    cssVar: r
  } = w.useContext(Oe._internalContext), [s, i, a] = er(n, [Oe.defaultSeed, t], {
    salt: `${Nr}-${e || ""}`,
    override: o,
    getComputedToken: It,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: _n,
      ignore: wn,
      preserve: On
    }
  });
  return [n, a, e ? i : "", s, r];
}
const {
  genStyleHooks: Pn,
  genComponentStyleHook: Nn,
  genSubStyleComponent: Un
} = vn({
  usePrefix: () => {
    const {
      getPrefixCls: t,
      iconPrefixCls: e
    } = ke();
    return {
      iconPrefixCls: e,
      rootPrefixCls: t()
    };
  },
  useToken: () => {
    const [t, e, n, o, r] = Mn();
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
    } = ke();
    return t ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), En = (t) => {
  const {
    componentCls: e,
    antCls: n
  } = t;
  return {
    [e]: {
      [`${n}-cascader-menus ${n}-cascader-menu`]: {
        height: "auto"
      },
      [`${e}-item`]: {
        "&-icon": {
          marginInlineEnd: t.paddingXXS
        },
        "&-extra": {
          marginInlineStart: t.padding
        }
      },
      [`&${e}-block`]: {
        [`${e}-item-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, kn = () => ({}), In = Pn("Suggestion", (t) => {
  const e = Ae(t, {});
  return En(e);
}, kn);
function jn(t, e, n, o, r) {
  const [s, i] = w.useState([]), a = (f, b = s) => {
    let p = t;
    for (let g = 0; g < f - 1; g += 1) {
      const m = b[g], y = p.find((C) => C.value === m);
      if (!y)
        break;
      p = y.children || [];
    }
    return p;
  }, c = (f) => f.map((b, p) => {
    const m = a(p + 1, f).find((y) => y.value === b);
    return m == null ? void 0 : m.value;
  }), l = (f) => {
    const b = s.length || 1, p = a(b), g = p.findIndex((C) => C.value === s[b - 1]), m = p.length, y = p[(g + f + m) % m];
    i([...s.slice(0, b - 1), y.value]);
  }, h = () => {
    s.length > 1 && i(s.slice(0, s.length - 1));
  }, u = () => {
    const f = a(s.length + 1);
    f.length && i([...s, f[0].value]);
  }, d = re((f) => {
    if (e)
      switch (f.key) {
        case "ArrowDown":
          l(1), f.preventDefault();
          break;
        case "ArrowUp":
          l(-1), f.preventDefault();
          break;
        case "ArrowRight":
          n ? h() : u(), f.preventDefault();
          break;
        case "ArrowLeft":
          n ? u() : h(), f.preventDefault();
          break;
        case "Enter":
          a(s.length + 1).length || o(c(s)), f.preventDefault();
          break;
        case "Escape":
          r(), f.preventDefault();
          break;
      }
  });
  return w.useEffect(() => {
    e && i([t[0].value]);
  }, [e]), [s, d];
}
function Rn(t) {
  const {
    prefixCls: e,
    className: n,
    rootClassName: o,
    style: r,
    children: s,
    open: i,
    onOpenChange: a,
    items: c,
    onSelect: l,
    block: h
  } = t, {
    direction: u,
    getPrefixCls: d
  } = ke(), f = d("suggestion", e), b = `${f}-item`, p = u === "rtl", g = Gr("suggestion"), [m, y, C] = In(f), [v, T] = en(!1, {
    value: i
  }), [S, O] = pt(), _ = (P) => {
    T(P), a == null || a(P);
  }, E = re((P) => {
    P === !1 ? _(!1) : (O(P), _(!0));
  }), j = () => {
    _(!1);
  }, B = w.useMemo(() => typeof c == "function" ? c(S) : c, [c, S]), k = (P) => /* @__PURE__ */ w.createElement(Jt, {
    className: b
  }, P.icon && /* @__PURE__ */ w.createElement("div", {
    className: `${b}-icon`
  }, P.icon), P.label, P.extra && /* @__PURE__ */ w.createElement("div", {
    className: `${b}-extra`
  }, P.extra)), F = (P) => {
    l && l(P[P.length - 1]), _(!1);
  }, [R, D] = jn(B, v, p, F, j), U = s == null ? void 0 : s({
    onTrigger: E,
    onKeyDown: D
  });
  return m(/* @__PURE__ */ w.createElement(Qt, {
    options: B,
    open: v,
    value: R,
    placement: p ? "topRight" : "topLeft",
    onDropdownVisibleChange: (P) => {
      P || j();
    },
    optionRender: k,
    rootClassName: $e(o, f, y, C, {
      [`${f}-block`]: h
    }),
    onChange: F,
    dropdownMatchSelectWidth: h
  }, /* @__PURE__ */ w.createElement("div", {
    className: $e(f, g.className, o, n, `${f}-wrapper`, y, C),
    style: {
      ...g.style,
      ...r
    }
  }, U)));
}
function Ln(t) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(t.trim());
}
function An(t, e = !1) {
  try {
    if (mt(t))
      return t;
    if (e && !Ln(t))
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
function ht(t, e) {
  return Q(() => An(t, e), [t, e]);
}
function Dn(t) {
  const e = gt();
  return Q(() => dr(t, e.current) ? e.current : (e.current = t, t), [t]);
}
function Hn(t, e) {
  return e((o, r) => mt(o) ? r ? (...s) => o(...s, ...t) : o(...t) : o);
}
const zn = ({
  children: t,
  ...e
}) => /* @__PURE__ */ A.jsx(A.Fragment, {
  children: t(e)
});
function Bn(t) {
  return w.createElement(zn, {
    children: t
  });
}
function jt(t, e, n) {
  const o = t.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var l;
      if (typeof r != "object")
        return e != null && e.fallback ? e.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((l = r.props) == null ? void 0 : l.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((h) => {
        if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
          return;
        const u = h.split(".");
        u.forEach((m, y) => {
          a[m] || (a[m] = {}), y !== u.length - 1 && (a = i[m]);
        });
        const d = r.slots[h];
        let f, b, p = (e == null ? void 0 : e.clone) ?? !1, g = e == null ? void 0 : e.forceClone;
        d instanceof Element ? f = d : (f = d.el, b = d.callback, p = d.clone ?? p, g = d.forceClone ?? g), g = g ?? !!b, a[u[u.length - 1]] = f ? b ? (...m) => (b(u[u.length - 1], m), /* @__PURE__ */ A.jsx(Ve, {
          ...r.ctx,
          params: m,
          forceClone: g,
          children: /* @__PURE__ */ A.jsx(Ee, {
            slot: f,
            clone: p
          })
        })) : Bn((m) => /* @__PURE__ */ A.jsx(Ve, {
          ...r.ctx,
          forceClone: g,
          children: /* @__PURE__ */ A.jsx(Ee, {
            slot: f,
            clone: p,
            ...m
          })
        })) : a[u[u.length - 1]], a = i;
      });
      const c = (e == null ? void 0 : e.children) || "children";
      return r[c] ? i[c] = jt(r[c], e, `${s}`) : e != null && e.children && (i[c] = void 0, Reflect.deleteProperty(i, c)), i;
    });
}
const {
  useItems: Fn,
  withItemsContextProvider: $n,
  ItemHandler: Wn
} = Kt("antdx-suggestion-chain-items"), Vn = dt(({
  children: t,
  props: e,
  shouldTrigger: n
}, o) => {
  const r = Dn(e);
  return /* @__PURE__ */ A.jsx(Gt.Provider, {
    value: Q(() => ({
      ...r,
      onKeyDown: (s) => {
        var i;
        n ? requestAnimationFrame(() => {
          n(s, {
            onTrigger: r.onTrigger,
            onKeyDown: r.onKeyDown
          });
        }) : (i = r.onKeyDown) == null || i.call(r, s);
      },
      elRef: o
    }), [r, n, o]),
    children: t
  });
}), Gn = Br($n(["default", "items"], ({
  children: t,
  items: e,
  shouldTrigger: n,
  slots: o,
  ...r
}) => {
  const {
    items: s
  } = Fn(), i = s.items.length > 0 ? s.items : s.default, a = ht(e), c = ht(n), l = Q(() => e || jt(i, {
    clone: !0
  }) || [{}], [e, i]), h = Q(() => (...u) => l.map((d) => Hn(u, (f) => {
    const b = (p) => {
      var g;
      return {
        ...p,
        extra: f(p.extra),
        icon: f(p.icon),
        label: f(p.label),
        children: (g = p.children) == null ? void 0 : g.map((m) => b(m))
      };
    };
    return b(d);
  })), [l]);
  return /* @__PURE__ */ A.jsx(A.Fragment, {
    children: /* @__PURE__ */ A.jsx(Rn, {
      ...r,
      items: a || h,
      children: (u) => /* @__PURE__ */ A.jsxs(Vn, {
        props: u,
        shouldTrigger: c,
        children: [/* @__PURE__ */ A.jsx("div", {
          style: {
            display: "none"
          },
          children: t
        }), o.children ? /* @__PURE__ */ A.jsx(Ee, {
          slot: o.children
        }) : null]
      })
    })
  });
}));
export {
  Gn as Suggestion,
  Gn as default
};
