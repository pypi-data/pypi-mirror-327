import { i as Rt, a as we, r as Lt, g as Ht, w as J, c as V } from "./Index-BQAPkVdd.js";
const b = window.ms_globals.React, Et = window.ms_globals.React.forwardRef, jt = window.ms_globals.React.useRef, It = window.ms_globals.React.useState, kt = window.ms_globals.React.useEffect, Ce = window.ms_globals.ReactDOM.createPortal, zt = window.ms_globals.internalContext.useContextPropsContext, At = window.ms_globals.antd.ConfigProvider, Te = window.ms_globals.antd.theme, De = window.ms_globals.antd.Typography, me = window.ms_globals.antd.Flex, Xe = window.ms_globals.antdCssinjs.unit, be = window.ms_globals.antdCssinjs.token2CSSVar, $e = window.ms_globals.antdCssinjs.useStyleRegister, Bt = window.ms_globals.antdCssinjs.useCSSVarRegister, Dt = window.ms_globals.antdCssinjs.createTheme, Xt = window.ms_globals.antdCssinjs.useCacheToken;
var $t = /\s/;
function Ft(e) {
  for (var t = e.length; t-- && $t.test(e.charAt(t)); )
    ;
  return t;
}
var Nt = /^\s+/;
function Vt(e) {
  return e && e.slice(0, Ft(e) + 1).replace(Nt, "");
}
var Fe = NaN, Wt = /^[-+]0x[0-9a-f]+$/i, Ut = /^0b[01]+$/i, Gt = /^0o[0-7]+$/i, qt = parseInt;
function Ne(e) {
  if (typeof e == "number")
    return e;
  if (Rt(e))
    return Fe;
  if (we(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = we(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Vt(e);
  var n = Ut.test(e);
  return n || Gt.test(e) ? qt(e.slice(2), n ? 2 : 8) : Wt.test(e) ? Fe : +e;
}
var ye = function() {
  return Lt.Date.now();
}, Kt = "Expected a function", Qt = Math.max, Jt = Math.min;
function Zt(e, t, n) {
  var o, r, i, s, a, c, l = 0, f = !1, u = !1, h = !0;
  if (typeof e != "function")
    throw new TypeError(Kt);
  t = Ne(t) || 0, we(n) && (f = !!n.leading, u = "maxWait" in n, i = u ? Qt(Ne(n.maxWait) || 0, t) : i, h = "trailing" in n ? !!n.trailing : h);
  function v(m) {
    var w = o, O = r;
    return o = r = void 0, l = m, s = e.apply(O, w), s;
  }
  function S(m) {
    return l = m, a = setTimeout(x, t), f ? v(m) : s;
  }
  function p(m) {
    var w = m - c, O = m - l, P = t - w;
    return u ? Jt(P, i - O) : P;
  }
  function d(m) {
    var w = m - c, O = m - l;
    return c === void 0 || w >= t || w < 0 || u && O >= i;
  }
  function x() {
    var m = ye();
    if (d(m))
      return _(m);
    a = setTimeout(x, p(m));
  }
  function _(m) {
    return a = void 0, h && o ? v(m) : (o = r = void 0, s);
  }
  function E() {
    a !== void 0 && clearTimeout(a), l = 0, o = c = r = a = void 0;
  }
  function g() {
    return a === void 0 ? s : _(ye());
  }
  function C() {
    var m = ye(), w = d(m);
    if (o = arguments, r = this, c = m, w) {
      if (a === void 0)
        return S(c);
      if (u)
        return clearTimeout(a), a = setTimeout(x, t), v(c);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return C.cancel = E, C.flush = g, C;
}
var st = {
  exports: {}
}, re = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Yt = b, er = Symbol.for("react.element"), tr = Symbol.for("react.fragment"), rr = Object.prototype.hasOwnProperty, nr = Yt.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, or = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function at(e, t, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) rr.call(t, o) && !or.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: er,
    type: e,
    key: i,
    ref: s,
    props: r,
    _owner: nr.current
  };
}
re.Fragment = tr;
re.jsx = at;
re.jsxs = at;
st.exports = re;
var B = st.exports;
const {
  SvelteComponent: ir,
  assign: Ve,
  binding_callbacks: We,
  check_outros: sr,
  children: ct,
  claim_element: lt,
  claim_space: ar,
  component_subscribe: Ue,
  compute_slots: cr,
  create_slot: lr,
  detach: N,
  element: ut,
  empty: Ge,
  exclude_internal_props: qe,
  get_all_dirty_from_scope: ur,
  get_slot_changes: fr,
  group_outros: hr,
  init: dr,
  insert_hydration: Z,
  safe_not_equal: gr,
  set_custom_element_data: ft,
  space: pr,
  transition_in: Y,
  transition_out: Oe,
  update_slot_base: mr
} = window.__gradio__svelte__internal, {
  beforeUpdate: br,
  getContext: yr,
  onDestroy: vr,
  setContext: xr
} = window.__gradio__svelte__internal;
function Ke(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = lr(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ut("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      t = lt(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = ct(t);
      r && r.l(s), s.forEach(N), this.h();
    },
    h() {
      ft(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Z(i, t, s), r && r.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && mr(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? fr(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : ur(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Y(r, i), n = !0);
    },
    o(i) {
      Oe(r, i), n = !1;
    },
    d(i) {
      i && N(t), r && r.d(i), e[9](null);
    }
  };
}
function Sr(e) {
  let t, n, o, r, i = (
    /*$$slots*/
    e[4].default && Ke(e)
  );
  return {
    c() {
      t = ut("react-portal-target"), n = pr(), i && i.c(), o = Ge(), this.h();
    },
    l(s) {
      t = lt(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), ct(t).forEach(N), n = ar(s), i && i.l(s), o = Ge(), this.h();
    },
    h() {
      ft(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Z(s, t, a), e[8](t), Z(s, n, a), i && i.m(s, a), Z(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Y(i, 1)) : (i = Ke(s), i.c(), Y(i, 1), i.m(o.parentNode, o)) : i && (hr(), Oe(i, 1, 1, () => {
        i = null;
      }), sr());
    },
    i(s) {
      r || (Y(i), r = !0);
    },
    o(s) {
      Oe(i), r = !1;
    },
    d(s) {
      s && (N(t), N(n), N(o)), e[8](null), i && i.d(s);
    }
  };
}
function Qe(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function _r(e, t, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = cr(i);
  let {
    svelteInit: c
  } = t;
  const l = J(Qe(t)), f = J();
  Ue(e, f, (g) => n(0, o = g));
  const u = J();
  Ue(e, u, (g) => n(1, r = g));
  const h = [], v = yr("$$ms-gr-react-wrapper"), {
    slotKey: S,
    slotIndex: p,
    subSlotIndex: d
  } = Ht() || {}, x = c({
    parent: v,
    props: l,
    target: f,
    slot: u,
    slotKey: S,
    slotIndex: p,
    subSlotIndex: d,
    onDestroy(g) {
      h.push(g);
    }
  });
  xr("$$ms-gr-react-wrapper", x), br(() => {
    l.set(Qe(t));
  }), vr(() => {
    h.forEach((g) => g());
  });
  function _(g) {
    We[g ? "unshift" : "push"](() => {
      o = g, f.set(o);
    });
  }
  function E(g) {
    We[g ? "unshift" : "push"](() => {
      r = g, u.set(r);
    });
  }
  return e.$$set = (g) => {
    n(17, t = Ve(Ve({}, t), qe(g))), "svelteInit" in g && n(5, c = g.svelteInit), "$$scope" in g && n(6, s = g.$$scope);
  }, t = qe(t), [o, r, f, u, a, c, s, i, _, E];
}
class Cr extends ir {
  constructor(t) {
    super(), dr(this, t, _r, Sr, gr, {
      svelteInit: 5
    });
  }
}
const Je = window.ms_globals.rerender, ve = window.ms_globals.tree;
function wr(e, t = {}) {
  function n(o) {
    const r = J(), i = new Cr({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? ve;
          return c.nodes = [...c.nodes, a], Je({
            createPortal: Ce,
            node: ve
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((l) => l.svelteInstance !== r), Je({
              createPortal: Ce,
              node: ve
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
const Tr = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Or(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = Mr(n, o), t;
  }, {}) : {};
}
function Mr(e, t) {
  return typeof t == "number" && !Tr.includes(e) ? t + "px" : t;
}
function Me(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = b.Children.toArray(e._reactElement.props.children).map((i) => {
      if (b.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Me(i.props.el);
        return b.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...b.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Ce(b.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, s, c);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Me(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Pr(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const K = Et(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = jt(), [a, c] = It([]), {
    forceClone: l
  } = zt(), f = l ? !0 : t;
  return kt(() => {
    var p;
    if (!s.current || !e)
      return;
    let u = e;
    function h() {
      let d = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (d = u.children[0], d.tagName.toLowerCase() === "react-portal-target" && d.children[0] && (d = d.children[0])), Pr(i, d), n && d.classList.add(...n.split(" ")), o) {
        const x = Or(o);
        Object.keys(x).forEach((_) => {
          d.style[_] = x[_];
        });
      }
    }
    let v = null, S = null;
    if (f && window.MutationObserver) {
      let d = function() {
        var g, C, m;
        (g = s.current) != null && g.contains(u) && ((C = s.current) == null || C.removeChild(u));
        const {
          portals: _,
          clonedElement: E
        } = Me(e);
        u = E, c(_), u.style.display = "contents", S && clearTimeout(S), S = setTimeout(() => {
          h();
        }, 50), (m = s.current) == null || m.appendChild(u);
      };
      d();
      const x = Zt(() => {
        d(), v == null || v.disconnect(), v == null || v.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      v = new window.MutationObserver(x), v.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", h(), (p = s.current) == null || p.appendChild(u);
    return () => {
      var d, x;
      u.style.display = "", (d = s.current) != null && d.contains(u) && ((x = s.current) == null || x.removeChild(u)), v == null || v.disconnect();
    };
  }, [e, f, n, o, i, r]), b.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), Er = "1.0.5", jr = /* @__PURE__ */ b.createContext({}), Ir = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, kr = (e) => {
  const t = b.useContext(jr);
  return b.useMemo(() => ({
    ...Ir,
    ...t[e]
  }), [t[e]]);
};
function Pe() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = b.useContext(At.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Rr(e) {
  if (Array.isArray(e)) return e;
}
function Lr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], c = !0, l = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); c = !0) ;
    } catch (f) {
      l = !0, r = f;
    } finally {
      try {
        if (!c && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (l) throw r;
      }
    }
    return a;
  }
}
function Ze(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function Hr(e, t) {
  if (e) {
    if (typeof e == "string") return Ze(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? Ze(e, t) : void 0;
  }
}
function zr() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function ee(e, t) {
  return Rr(e) || Lr(e, t) || Hr(e, t) || zr();
}
function H(e) {
  "@babel/helpers - typeof";
  return H = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, H(e);
}
var y = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ie = Symbol.for("react.element"), ke = Symbol.for("react.portal"), ne = Symbol.for("react.fragment"), oe = Symbol.for("react.strict_mode"), ie = Symbol.for("react.profiler"), se = Symbol.for("react.provider"), ae = Symbol.for("react.context"), Ar = Symbol.for("react.server_context"), ce = Symbol.for("react.forward_ref"), le = Symbol.for("react.suspense"), ue = Symbol.for("react.suspense_list"), fe = Symbol.for("react.memo"), he = Symbol.for("react.lazy"), Br = Symbol.for("react.offscreen"), ht;
ht = Symbol.for("react.module.reference");
function R(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ie:
        switch (e = e.type, e) {
          case ne:
          case ie:
          case oe:
          case le:
          case ue:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Ar:
              case ae:
              case ce:
              case he:
              case fe:
              case se:
                return e;
              default:
                return t;
            }
        }
      case ke:
        return t;
    }
  }
}
y.ContextConsumer = ae;
y.ContextProvider = se;
y.Element = Ie;
y.ForwardRef = ce;
y.Fragment = ne;
y.Lazy = he;
y.Memo = fe;
y.Portal = ke;
y.Profiler = ie;
y.StrictMode = oe;
y.Suspense = le;
y.SuspenseList = ue;
y.isAsyncMode = function() {
  return !1;
};
y.isConcurrentMode = function() {
  return !1;
};
y.isContextConsumer = function(e) {
  return R(e) === ae;
};
y.isContextProvider = function(e) {
  return R(e) === se;
};
y.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ie;
};
y.isForwardRef = function(e) {
  return R(e) === ce;
};
y.isFragment = function(e) {
  return R(e) === ne;
};
y.isLazy = function(e) {
  return R(e) === he;
};
y.isMemo = function(e) {
  return R(e) === fe;
};
y.isPortal = function(e) {
  return R(e) === ke;
};
y.isProfiler = function(e) {
  return R(e) === ie;
};
y.isStrictMode = function(e) {
  return R(e) === oe;
};
y.isSuspense = function(e) {
  return R(e) === le;
};
y.isSuspenseList = function(e) {
  return R(e) === ue;
};
y.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === ne || e === ie || e === oe || e === le || e === ue || e === Br || typeof e == "object" && e !== null && (e.$$typeof === he || e.$$typeof === fe || e.$$typeof === se || e.$$typeof === ae || e.$$typeof === ce || e.$$typeof === ht || e.getModuleId !== void 0);
};
y.typeOf = R;
function Dr(e, t) {
  if (H(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t || "default");
    if (H(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function dt(e) {
  var t = Dr(e, "string");
  return H(t) == "symbol" ? t : t + "";
}
function T(e, t, n) {
  return (t = dt(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function Ye(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function I(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Ye(Object(n), !0).forEach(function(o) {
      T(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : Ye(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function de(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function Xr(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, dt(o.key), o);
  }
}
function ge(e, t, n) {
  return t && Xr(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Ee(e, t) {
  return Ee = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Ee(e, t);
}
function gt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Ee(e, t);
}
function te(e) {
  return te = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, te(e);
}
function pt() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (pt = function() {
    return !!e;
  })();
}
function U(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function $r(e, t) {
  if (t && (H(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return U(e);
}
function mt(e) {
  var t = pt();
  return function() {
    var n, o = te(e);
    if (t) {
      var r = te(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return $r(this, n);
  };
}
var bt = /* @__PURE__ */ ge(function e() {
  de(this, e);
}), yt = "CALC_UNIT", Fr = new RegExp(yt, "g");
function xe(e) {
  return typeof e == "number" ? "".concat(e).concat(yt) : e;
}
var Nr = /* @__PURE__ */ function(e) {
  gt(n, e);
  var t = mt(n);
  function n(o, r) {
    var i;
    de(this, n), i = t.call(this), T(U(i), "result", ""), T(U(i), "unitlessCssVar", void 0), T(U(i), "lowPriority", void 0);
    var s = H(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = xe(o) : s === "string" && (i.result = o), i;
  }
  return ge(n, [{
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
      var i = this, s = r || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(l) {
        return i.result.includes(l);
      }) && (c = !1), this.result = this.result.replace(Fr, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(bt), Vr = /* @__PURE__ */ function(e) {
  gt(n, e);
  var t = mt(n);
  function n(o) {
    var r;
    return de(this, n), r = t.call(this), T(U(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return ge(n, [{
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
}(bt), Wr = function(t, n) {
  var o = t === "css" ? Nr : Vr;
  return function(r) {
    return new o(r, n);
  };
}, et = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function tt(e, t, n, o) {
  var r = I({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var c = ee(a, 2), l = c[0], f = c[1];
      if (r != null && r[l] || r != null && r[f]) {
        var u;
        (u = r[f]) !== null && u !== void 0 || (r[f] = r == null ? void 0 : r[l]);
      }
    });
  }
  var s = I(I({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var vt = typeof CSSINJS_STATISTIC < "u", je = !0;
function Re() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!vt)
    return Object.assign.apply(Object, [{}].concat(t));
  je = !1;
  var o = {};
  return t.forEach(function(r) {
    if (H(r) === "object") {
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
  }), je = !0, o;
}
var rt = {};
function Ur() {
}
var Gr = function(t) {
  var n, o = t, r = Ur;
  return vt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (je) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var c;
    rt[s] = {
      global: Array.from(n),
      component: I(I({}, (c = rt[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function nt(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Re(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function qr(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return Xe(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return Xe(i);
      }).join(","), ")");
    }
  };
}
var Kr = 1e3 * 60 * 10, Qr = /* @__PURE__ */ function() {
  function e() {
    de(this, e), T(this, "map", /* @__PURE__ */ new Map()), T(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), T(this, "nextID", 0), T(this, "lastAccessBeat", /* @__PURE__ */ new Map()), T(this, "accessBeat", 0);
  }
  return ge(e, [{
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
        return i && H(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(H(i), "_").concat(i);
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
          o - r > Kr && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), ot = new Qr();
function Jr(e, t) {
  return b.useMemo(function() {
    var n = ot.get(t);
    if (n)
      return n;
    var o = e();
    return ot.set(t, o), o;
  }, t);
}
var Zr = function() {
  return {};
};
function Yr(e) {
  var t = e.useCSP, n = t === void 0 ? Zr : t, o = e.useToken, r = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(h, v, S, p) {
    var d = Array.isArray(h) ? h[0] : h;
    function x(O) {
      return "".concat(String(d)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var _ = (p == null ? void 0 : p.unitless) || {}, E = typeof a == "function" ? a(h) : {}, g = I(I({}, E), {}, T({}, x("zIndexPopup"), !0));
    Object.keys(_).forEach(function(O) {
      g[x(O)] = _[O];
    });
    var C = I(I({}, p), {}, {
      unitless: g,
      prefixToken: x
    }), m = f(h, v, S, C), w = l(d, S, C);
    return function(O) {
      var P = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, L = m(O, P), D = ee(L, 2), j = D[1], X = w(P), k = ee(X, 2), z = k[0], G = k[1];
      return [z, j, G];
    };
  }
  function l(h, v, S) {
    var p = S.unitless, d = S.injectStyle, x = d === void 0 ? !0 : d, _ = S.prefixToken, E = S.ignore, g = function(w) {
      var O = w.rootCls, P = w.cssVar, L = P === void 0 ? {} : P, D = o(), j = D.realToken;
      return Bt({
        path: [h],
        prefix: L.prefix,
        key: L.key,
        unitless: p,
        ignore: E,
        token: j,
        scope: O
      }, function() {
        var X = nt(h, j, v), k = tt(h, j, X, {
          deprecatedTokens: S == null ? void 0 : S.deprecatedTokens
        });
        return Object.keys(X).forEach(function(z) {
          k[_(z)] = k[z], delete k[z];
        }), k;
      }), null;
    }, C = function(w) {
      var O = o(), P = O.cssVar;
      return [function(L) {
        return x && P ? /* @__PURE__ */ b.createElement(b.Fragment, null, /* @__PURE__ */ b.createElement(g, {
          rootCls: w,
          cssVar: P,
          component: h
        }), L) : L;
      }, P == null ? void 0 : P.key];
    };
    return C;
  }
  function f(h, v, S) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, d = Array.isArray(h) ? h : [h, h], x = ee(d, 1), _ = x[0], E = d.join("-"), g = e.layer || {
      name: "antd"
    };
    return function(C) {
      var m = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, w = o(), O = w.theme, P = w.realToken, L = w.hashId, D = w.token, j = w.cssVar, X = r(), k = X.rootPrefixCls, z = X.iconPrefixCls, G = n(), pe = j ? "css" : "js", St = Jr(function() {
        var $ = /* @__PURE__ */ new Set();
        return j && Object.keys(p.unitless || {}).forEach(function(q) {
          $.add(be(q, j.prefix)), $.add(be(q, et(_, j.prefix)));
        }), Wr(pe, $);
      }, [pe, _, j == null ? void 0 : j.prefix]), Le = qr(pe), _t = Le.max, Ct = Le.min, He = {
        theme: O,
        token: D,
        hashId: L,
        nonce: function() {
          return G.nonce;
        },
        clientOnly: p.clientOnly,
        layer: g,
        // antd is always at top of styles
        order: p.order || -999
      };
      typeof i == "function" && $e(I(I({}, He), {}, {
        clientOnly: !1,
        path: ["Shared", k]
      }), function() {
        return i(D, {
          prefix: {
            rootPrefixCls: k,
            iconPrefixCls: z
          },
          csp: G
        });
      });
      var wt = $e(I(I({}, He), {}, {
        path: [E, C, z]
      }), function() {
        if (p.injectStyle === !1)
          return [];
        var $ = Gr(D), q = $.token, Tt = $.flush, F = nt(_, P, S), Ot = ".".concat(C), ze = tt(_, P, F, {
          deprecatedTokens: p.deprecatedTokens
        });
        j && F && H(F) === "object" && Object.keys(F).forEach(function(Be) {
          F[Be] = "var(".concat(be(Be, et(_, j.prefix)), ")");
        });
        var Ae = Re(q, {
          componentCls: Ot,
          prefixCls: C,
          iconCls: ".".concat(z),
          antCls: ".".concat(k),
          calc: St,
          // @ts-ignore
          max: _t,
          // @ts-ignore
          min: Ct
        }, j ? F : ze), Mt = v(Ae, {
          hashId: L,
          prefixCls: C,
          rootPrefixCls: k,
          iconPrefixCls: z
        });
        Tt(_, ze);
        var Pt = typeof s == "function" ? s(Ae, C, m, p.resetFont) : null;
        return [p.resetStyle === !1 ? null : Pt, Mt];
      });
      return [wt, L];
    };
  }
  function u(h, v, S) {
    var p = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, d = f(h, v, S, I({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, p)), x = function(E) {
      var g = E.prefixCls, C = E.rootCls, m = C === void 0 ? g : C;
      return d(g, m), null;
    };
    return x;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: u,
    genComponentStyleHook: f
  };
}
const M = Math.round;
function Se(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const it = (e, t, n) => n === 0 ? e : e / 100;
function W(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class A {
  constructor(t) {
    T(this, "isValid", !0), T(this, "r", 0), T(this, "g", 0), T(this, "b", 0), T(this, "a", 1), T(this, "_h", void 0), T(this, "_s", void 0), T(this, "_l", void 0), T(this, "_v", void 0), T(this, "_max", void 0), T(this, "_min", void 0), T(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof A)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = W(t.r), this.g = W(t.g), this.b = W(t.b), this.a = typeof t.a == "number" ? W(t.a, 1) : 1;
    else if (n("hsl"))
      this.fromHsl(t);
    else if (n("hsv"))
      this.fromHsv(t);
    else
      throw new Error("@ant-design/fast-color: unsupported input " + JSON.stringify(t));
  }
  // ======================= Setter =======================
  setR(t) {
    return this._sc("r", t);
  }
  setG(t) {
    return this._sc("g", t);
  }
  setB(t) {
    return this._sc("b", t);
  }
  setA(t) {
    return this._sc("a", t, 1);
  }
  setHue(t) {
    const n = this.toHsv();
    return n.h = t, this._c(n);
  }
  // ======================= Getter =======================
  /**
   * Returns the perceived luminance of a color, from 0-1.
   * @see http://www.w3.org/TR/2008/REC-WCAG20-20081211/#relativeluminancedef
   */
  getLuminance() {
    function t(i) {
      const s = i / 255;
      return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = M(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
    }
    return this._h;
  }
  getSaturation() {
    if (typeof this._s > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._s = 0 : this._s = t / this.getMax();
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
  darken(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() - t / 100;
    return r < 0 && (r = 0), this._c({
      h: n,
      s: o,
      l: r,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), o = this.getSaturation();
    let r = this.getLightness() + t / 100;
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
  mix(t, n = 50) {
    const o = this._c(t), r = n / 100, i = (a) => (o[a] - this[a]) * r + this[a], s = {
      r: M(i("r")),
      g: M(i("g")),
      b: M(i("b")),
      a: M(i("a") * 100) / 100
    };
    return this._c(s);
  }
  /**
   * Mix the color with pure white, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return white.
   */
  tint(t = 10) {
    return this.mix({
      r: 255,
      g: 255,
      b: 255,
      a: 1
    }, t);
  }
  /**
   * Mix the color with pure black, from 0 to 100.
   * Providing 0 will do nothing, providing 100 will always return black.
   */
  shade(t = 10) {
    return this.mix({
      r: 0,
      g: 0,
      b: 0,
      a: 1
    }, t);
  }
  onBackground(t) {
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (i) => M((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
  equals(t) {
    return this.r === t.r && this.g === t.g && this.b === t.b && this.a === t.a;
  }
  clone() {
    return this._c(this);
  }
  // ======================= Format =======================
  toHexString() {
    let t = "#";
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const o = (this.g || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.b || 0).toString(16);
    if (t += r.length === 2 ? r : "0" + r, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = M(this.a * 255).toString(16);
      t += i.length === 2 ? i : "0" + i;
    }
    return t;
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
    const t = this.getHue(), n = M(this.getSaturation() * 100), o = M(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${o}%,${this.a})` : `hsl(${t},${n}%,${o}%)`;
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
  _sc(t, n, o) {
    const r = this.clone();
    return r[t] = W(n, o), r;
  }
  _c(t) {
    return new this.constructor(t);
  }
  getMax() {
    return typeof this._max > "u" && (this._max = Math.max(this.r, this.g, this.b)), this._max;
  }
  getMin() {
    return typeof this._min > "u" && (this._min = Math.min(this.r, this.g, this.b)), this._min;
  }
  fromHexString(t) {
    const n = t.replace("#", "");
    function o(r, i) {
      return parseInt(n[r] + n[i || r], 16);
    }
    n.length < 6 ? (this.r = o(0), this.g = o(1), this.b = o(2), this.a = n[3] ? o(3) / 255 : 1) : (this.r = o(0, 1), this.g = o(2, 3), this.b = o(4, 5), this.a = n[6] ? o(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: o,
    a: r
  }) {
    if (this._h = t % 360, this._s = n, this._l = o, this.a = typeof r == "number" ? r : 1, n <= 0) {
      const h = M(o * 255);
      this.r = h, this.g = h, this.b = h;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, l = (1 - Math.abs(2 * o - 1)) * n, f = l * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = l, s = f) : c >= 1 && c < 2 ? (i = f, s = l) : c >= 2 && c < 3 ? (s = l, a = f) : c >= 3 && c < 4 ? (s = f, a = l) : c >= 4 && c < 5 ? (i = f, a = l) : c >= 5 && c < 6 && (i = l, a = f);
    const u = o - l / 2;
    this.r = M((i + u) * 255), this.g = M((s + u) * 255), this.b = M((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = M(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, l = M(o * (1 - n) * 255), f = M(o * (1 - n * c) * 255), u = M(o * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = l;
        break;
      case 1:
        this.r = f, this.b = l;
        break;
      case 2:
        this.r = l, this.b = u;
        break;
      case 3:
        this.r = l, this.g = f;
        break;
      case 4:
        this.r = u, this.g = l;
        break;
      case 5:
      default:
        this.g = l, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const n = Se(t, it);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = Se(t, it);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = Se(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? M(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const en = {
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
}, tn = Object.assign(Object.assign({}, en), {
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
function _e(e) {
  return e >= 0 && e <= 255;
}
function Q(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new A(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new A(t).toRgb();
  for (let l = 0.01; l <= 1; l += 0.01) {
    const f = Math.round((n - s * (1 - l)) / l), u = Math.round((o - a * (1 - l)) / l), h = Math.round((r - c * (1 - l)) / l);
    if (_e(f) && _e(u) && _e(h))
      return new A({
        r: f,
        g: u,
        b: h,
        a: Math.round(l * 100) / 100
      }).toRgbString();
  }
  return new A({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var rn = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function nn(e) {
  const {
    override: t
  } = e, n = rn(e, ["override"]), o = Object.assign({}, t);
  Object.keys(tn).forEach((h) => {
    delete o[h];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, c = 992, l = 1200, f = 1600;
  if (r.motion === !1) {
    const h = "0s";
    r.motionDurationFast = h, r.motionDurationMid = h, r.motionDurationSlow = h;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: Q(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: Q(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Q(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: Q(r.colorPrimaryBg, r.colorBgContainer),
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
    screenMDMax: c - 1,
    screenLG: c,
    screenLGMin: c,
    screenLGMax: l - 1,
    screenXL: l,
    screenXLMin: l,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new A("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new A("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new A("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const on = {
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
}, sn = {
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
}, an = Dt(Te.defaultAlgorithm), cn = {
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
}, xt = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...i
  } = t;
  let s = {
    ...o,
    override: r
  };
  return s = nn(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: l,
      ...f
    } = c;
    let u = f;
    l && (u = xt({
      ...s,
      ...f
    }, {
      override: f
    }, l)), s[a] = u;
  }), s;
};
function ln() {
  const {
    token: e,
    hashed: t,
    theme: n = an,
    override: o,
    cssVar: r
  } = b.useContext(Te._internalContext), [i, s, a] = Xt(n, [Te.defaultSeed, e], {
    salt: `${Er}-${t || ""}`,
    override: o,
    getComputedToken: xt,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: on,
      ignore: sn,
      preserve: cn
    }
  });
  return [n, a, t ? s : "", i, r];
}
const {
  genStyleHooks: un,
  genComponentStyleHook: yn,
  genSubStyleComponent: vn
} = Yr({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Pe();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = ln();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: o,
      cssVar: r
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Pe();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), fn = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, o = n(e.fontSizeHeading3).mul(e.lineHeightHeading3).equal(), r = n(e.fontSize).mul(e.lineHeight).equal();
  return {
    [t]: {
      gap: e.padding,
      // ======================== Icon ========================
      [`${t}-icon`]: {
        height: n(o).add(r).add(e.paddingXXS).equal(),
        display: "flex",
        img: {
          height: "100%"
        }
      },
      // ==================== Content Wrap ====================
      [`${t}-content-wrapper`]: {
        gap: e.paddingXS,
        flex: "auto",
        minWidth: 0,
        [`${t}-title-wrapper`]: {
          gap: e.paddingXS
        },
        [`${t}-title`]: {
          margin: 0
        },
        [`${t}-extra`]: {
          marginInlineStart: "auto"
        }
      }
    }
  };
}, hn = (e) => {
  const {
    componentCls: t
  } = e;
  return {
    [t]: {
      // ======================== Filled ========================
      "&-filled": {
        paddingInline: e.padding,
        paddingBlock: e.paddingSM,
        background: e.colorFillContent,
        borderRadius: e.borderRadiusLG
      },
      // ====================== Borderless ======================
      "&-borderless": {
        [`${t}-title`]: {
          fontSize: e.fontSizeHeading3,
          lineHeight: e.lineHeightHeading3
        }
      }
    }
  };
}, dn = () => ({}), gn = un("Welcome", (e) => {
  const t = Re(e, {});
  return [fn(t), hn(t)];
}, dn);
function pn(e, t) {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    style: i,
    variant: s = "filled",
    // Semantic
    classNames: a = {},
    styles: c = {},
    // Layout
    icon: l,
    title: f,
    description: u,
    extra: h
  } = e, {
    direction: v,
    getPrefixCls: S
  } = Pe(), p = S("welcome", n), d = kr("welcome"), [x, _, E] = gn(p), g = b.useMemo(() => {
    if (!l)
      return null;
    let w = l;
    return typeof l == "string" && l.startsWith("http") && (w = /* @__PURE__ */ b.createElement("img", {
      src: l,
      alt: "icon"
    })), /* @__PURE__ */ b.createElement("div", {
      className: V(`${p}-icon`, d.classNames.icon, a.icon),
      style: c.icon
    }, w);
  }, [l]), C = b.useMemo(() => f ? /* @__PURE__ */ b.createElement(De.Title, {
    level: 4,
    className: V(`${p}-title`, d.classNames.title, a.title),
    style: c.title
  }, f) : null, [f]), m = b.useMemo(() => h ? /* @__PURE__ */ b.createElement("div", {
    className: V(`${p}-extra`, d.classNames.extra, a.extra),
    style: c.extra
  }, h) : null, [h]);
  return x(/* @__PURE__ */ b.createElement(me, {
    ref: t,
    className: V(p, d.className, r, o, _, E, `${p}-${s}`, {
      [`${p}-rtl`]: v === "rtl"
    }),
    style: i
  }, g, /* @__PURE__ */ b.createElement(me, {
    vertical: !0,
    className: `${p}-content-wrapper`
  }, h ? /* @__PURE__ */ b.createElement(me, {
    align: "flex-start",
    className: `${p}-title-wrapper`
  }, C, m) : C, u && /* @__PURE__ */ b.createElement(De.Text, {
    className: V(`${p}-description`, d.classNames.description, a.description),
    style: c.description
  }, u))));
}
const mn = /* @__PURE__ */ b.forwardRef(pn), xn = wr(({
  slots: e,
  children: t,
  ...n
}) => /* @__PURE__ */ B.jsxs(B.Fragment, {
  children: [/* @__PURE__ */ B.jsx("div", {
    style: {
      display: "none"
    },
    children: t
  }), /* @__PURE__ */ B.jsx(mn, {
    ...n,
    extra: e.extra ? /* @__PURE__ */ B.jsx(K, {
      slot: e.extra
    }) : n.extra,
    icon: e.icon ? /* @__PURE__ */ B.jsx(K, {
      slot: e.icon
    }) : n.icon,
    title: e.title ? /* @__PURE__ */ B.jsx(K, {
      slot: e.title
    }) : n.title,
    description: e.description ? /* @__PURE__ */ B.jsx(K, {
      slot: e.description
    }) : n.description
  })]
}));
export {
  xn as Welcome,
  xn as default
};
