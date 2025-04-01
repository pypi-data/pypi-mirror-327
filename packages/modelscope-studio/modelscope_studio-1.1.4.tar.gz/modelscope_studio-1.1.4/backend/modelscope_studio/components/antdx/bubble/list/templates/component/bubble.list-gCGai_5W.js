import { i as Ut, a as ne, r as Gt, g as Kt, w as ce, c as Y, b as Fe } from "./Index-CW2TbCyQ.js";
const I = window.ms_globals.React, h = window.ms_globals.React, le = window.ms_globals.React.useMemo, Xt = window.ms_globals.React.forwardRef, Nt = window.ms_globals.React.useRef, Vt = window.ms_globals.React.useState, Wt = window.ms_globals.React.useEffect, Le = window.ms_globals.ReactDOM.createPortal, qt = window.ms_globals.internalContext.useContextPropsContext, qe = window.ms_globals.internalContext.ContextPropsProvider, yt = window.ms_globals.createItemsContext.createItemsContext, Yt = window.ms_globals.antd.ConfigProvider, $e = window.ms_globals.antd.theme, Qt = window.ms_globals.antd.Avatar, oe = window.ms_globals.antdCssinjs.unit, Oe = window.ms_globals.antdCssinjs.token2CSSVar, Ye = window.ms_globals.antdCssinjs.useStyleRegister, Jt = window.ms_globals.antdCssinjs.useCSSVarRegister, Zt = window.ms_globals.antdCssinjs.createTheme, er = window.ms_globals.antdCssinjs.useCacheToken, vt = window.ms_globals.antdCssinjs.Keyframes;
var tr = /\s/;
function rr(e) {
  for (var t = e.length; t-- && tr.test(e.charAt(t)); )
    ;
  return t;
}
var nr = /^\s+/;
function or(e) {
  return e && e.slice(0, rr(e) + 1).replace(nr, "");
}
var Qe = NaN, sr = /^[-+]0x[0-9a-f]+$/i, ir = /^0b[01]+$/i, ar = /^0o[0-7]+$/i, lr = parseInt;
function Je(e) {
  if (typeof e == "number")
    return e;
  if (Ut(e))
    return Qe;
  if (ne(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = ne(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = or(e);
  var n = ir.test(e);
  return n || ar.test(e) ? lr(e.slice(2), n ? 2 : 8) : sr.test(e) ? Qe : +e;
}
var Pe = function() {
  return Gt.Date.now();
}, cr = "Expected a function", ur = Math.max, fr = Math.min;
function dr(e, t, n) {
  var o, r, s, i, a, l, f = 0, c = !1, u = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(cr);
  t = Je(t) || 0, ne(n) && (c = !!n.leading, u = "maxWait" in n, s = u ? ur(Je(n.maxWait) || 0, t) : s, d = "trailing" in n ? !!n.trailing : d);
  function b(y) {
    var M = o, O = r;
    return o = r = void 0, f = y, i = e.apply(O, M), i;
  }
  function v(y) {
    return f = y, a = setTimeout(m, t), c ? b(y) : i;
  }
  function x(y) {
    var M = y - l, O = y - f, S = t - M;
    return u ? fr(S, s - O) : S;
  }
  function g(y) {
    var M = y - l, O = y - f;
    return l === void 0 || M >= t || M < 0 || u && O >= s;
  }
  function m() {
    var y = Pe();
    if (g(y))
      return _(y);
    a = setTimeout(m, x(y));
  }
  function _(y) {
    return a = void 0, d && o ? b(y) : (o = r = void 0, i);
  }
  function k() {
    a !== void 0 && clearTimeout(a), f = 0, o = l = r = a = void 0;
  }
  function p() {
    return a === void 0 ? i : _(Pe());
  }
  function C() {
    var y = Pe(), M = g(y);
    if (o = arguments, r = this, l = y, M) {
      if (a === void 0)
        return v(l);
      if (u)
        return clearTimeout(a), a = setTimeout(m, t), b(l);
    }
    return a === void 0 && (a = setTimeout(m, t)), i;
  }
  return C.cancel = k, C.flush = p, C;
}
var St = {
  exports: {}
}, me = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var hr = h, gr = Symbol.for("react.element"), mr = Symbol.for("react.fragment"), pr = Object.prototype.hasOwnProperty, br = hr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, yr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function xt(e, t, n) {
  var o, r = {}, s = null, i = null;
  n !== void 0 && (s = "" + n), t.key !== void 0 && (s = "" + t.key), t.ref !== void 0 && (i = t.ref);
  for (o in t) pr.call(t, o) && !yr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: gr,
    type: e,
    key: s,
    ref: i,
    props: r,
    _owner: br.current
  };
}
me.Fragment = mr;
me.jsx = xt;
me.jsxs = xt;
St.exports = me;
var B = St.exports;
const {
  SvelteComponent: vr,
  assign: Ze,
  binding_callbacks: et,
  check_outros: Sr,
  children: Ct,
  claim_element: wt,
  claim_space: xr,
  component_subscribe: tt,
  compute_slots: Cr,
  create_slot: wr,
  detach: Q,
  element: _t,
  empty: rt,
  exclude_internal_props: nt,
  get_all_dirty_from_scope: _r,
  get_slot_changes: Tr,
  group_outros: Er,
  init: Mr,
  insert_hydration: ue,
  safe_not_equal: Or,
  set_custom_element_data: Tt,
  space: Pr,
  transition_in: fe,
  transition_out: De,
  update_slot_base: Ir
} = window.__gradio__svelte__internal, {
  beforeUpdate: Rr,
  getContext: kr,
  onDestroy: jr,
  setContext: Lr
} = window.__gradio__svelte__internal;
function ot(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = wr(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = _t("svelte-slot"), r && r.c(), this.h();
    },
    l(s) {
      t = wt(s, "SVELTE-SLOT", {
        class: !0
      });
      var i = Ct(t);
      r && r.l(i), i.forEach(Q), this.h();
    },
    h() {
      Tt(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      ue(s, t, i), r && r.m(t, null), e[9](t), n = !0;
    },
    p(s, i) {
      r && r.p && (!n || i & /*$$scope*/
      64) && Ir(
        r,
        o,
        s,
        /*$$scope*/
        s[6],
        n ? Tr(
          o,
          /*$$scope*/
          s[6],
          i,
          null
        ) : _r(
          /*$$scope*/
          s[6]
        ),
        null
      );
    },
    i(s) {
      n || (fe(r, s), n = !0);
    },
    o(s) {
      De(r, s), n = !1;
    },
    d(s) {
      s && Q(t), r && r.d(s), e[9](null);
    }
  };
}
function $r(e) {
  let t, n, o, r, s = (
    /*$$slots*/
    e[4].default && ot(e)
  );
  return {
    c() {
      t = _t("react-portal-target"), n = Pr(), s && s.c(), o = rt(), this.h();
    },
    l(i) {
      t = wt(i, "REACT-PORTAL-TARGET", {
        class: !0
      }), Ct(t).forEach(Q), n = xr(i), s && s.l(i), o = rt(), this.h();
    },
    h() {
      Tt(t, "class", "svelte-1rt0kpf");
    },
    m(i, a) {
      ue(i, t, a), e[8](t), ue(i, n, a), s && s.m(i, a), ue(i, o, a), r = !0;
    },
    p(i, [a]) {
      /*$$slots*/
      i[4].default ? s ? (s.p(i, a), a & /*$$slots*/
      16 && fe(s, 1)) : (s = ot(i), s.c(), fe(s, 1), s.m(o.parentNode, o)) : s && (Er(), De(s, 1, 1, () => {
        s = null;
      }), Sr());
    },
    i(i) {
      r || (fe(s), r = !0);
    },
    o(i) {
      De(s), r = !1;
    },
    d(i) {
      i && (Q(t), Q(n), Q(o)), e[8](null), s && s.d(i);
    }
  };
}
function st(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function Dr(e, t, n) {
  let o, r, {
    $$slots: s = {},
    $$scope: i
  } = t;
  const a = Cr(s);
  let {
    svelteInit: l
  } = t;
  const f = ce(st(t)), c = ce();
  tt(e, c, (p) => n(0, o = p));
  const u = ce();
  tt(e, u, (p) => n(1, r = p));
  const d = [], b = kr("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: x,
    subSlotIndex: g
  } = Kt() || {}, m = l({
    parent: b,
    props: f,
    target: c,
    slot: u,
    slotKey: v,
    slotIndex: x,
    subSlotIndex: g,
    onDestroy(p) {
      d.push(p);
    }
  });
  Lr("$$ms-gr-react-wrapper", m), Rr(() => {
    f.set(st(t));
  }), jr(() => {
    d.forEach((p) => p());
  });
  function _(p) {
    et[p ? "unshift" : "push"](() => {
      o = p, c.set(o);
    });
  }
  function k(p) {
    et[p ? "unshift" : "push"](() => {
      r = p, u.set(r);
    });
  }
  return e.$$set = (p) => {
    n(17, t = Ze(Ze({}, t), nt(p))), "svelteInit" in p && n(5, l = p.svelteInit), "$$scope" in p && n(6, i = p.$$scope);
  }, t = nt(t), [o, r, c, u, a, l, i, s, _, k];
}
class Br extends vr {
  constructor(t) {
    super(), Mr(this, t, Dr, $r, Or, {
      svelteInit: 5
    });
  }
}
const it = window.ms_globals.rerender, Ie = window.ms_globals.tree;
function Hr(e, t = {}) {
  function n(o) {
    const r = ce(), s = new Br({
      ...o,
      props: {
        svelteInit(i) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: i.props,
            slot: i.slot,
            target: i.target,
            slotIndex: i.slotIndex,
            subSlotIndex: i.subSlotIndex,
            ignore: t.ignore,
            slotKey: i.slotKey,
            nodes: []
          }, l = i.parent ?? Ie;
          return l.nodes = [...l.nodes, a], it({
            createPortal: Le,
            node: Ie
          }), i.onDestroy(() => {
            l.nodes = l.nodes.filter((f) => f.svelteInstance !== r), it({
              createPortal: Le,
              node: Ie
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
const zr = "1.0.5", Ar = /* @__PURE__ */ h.createContext({}), Fr = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Xr = (e) => {
  const t = h.useContext(Ar);
  return h.useMemo(() => ({
    ...Fr,
    ...t[e]
  }), [t[e]]);
};
function se() {
  return se = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var o in n) ({}).hasOwnProperty.call(n, o) && (e[o] = n[o]);
    }
    return e;
  }, se.apply(null, arguments);
}
function he() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = h.useContext(Yt.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function Et(e) {
  var t = I.useRef();
  t.current = e;
  var n = I.useCallback(function() {
    for (var o, r = arguments.length, s = new Array(r), i = 0; i < r; i++)
      s[i] = arguments[i];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(s));
  }, []);
  return n;
}
function Nr(e) {
  if (Array.isArray(e)) return e;
}
function Vr(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, s, i, a = [], l = !0, f = !1;
    try {
      if (s = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = s.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (c) {
      f = !0, r = c;
    } finally {
      try {
        if (!l && n.return != null && (i = n.return(), Object(i) !== i)) return;
      } finally {
        if (f) throw r;
      }
    }
    return a;
  }
}
function at(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function Wr(e, t) {
  if (e) {
    if (typeof e == "string") return at(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? at(e, t) : void 0;
  }
}
function Ur() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function de(e, t) {
  return Nr(e) || Vr(e, t) || Wr(e, t) || Ur();
}
function Gr() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var lt = Gr() ? I.useLayoutEffect : I.useEffect, Kr = function(t, n) {
  var o = I.useRef(!0);
  lt(function() {
    return t(o.current);
  }, n), lt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
};
function N(e) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, N(e);
}
var E = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Xe = Symbol.for("react.element"), Ne = Symbol.for("react.portal"), pe = Symbol.for("react.fragment"), be = Symbol.for("react.strict_mode"), ye = Symbol.for("react.profiler"), ve = Symbol.for("react.provider"), Se = Symbol.for("react.context"), qr = Symbol.for("react.server_context"), xe = Symbol.for("react.forward_ref"), Ce = Symbol.for("react.suspense"), we = Symbol.for("react.suspense_list"), _e = Symbol.for("react.memo"), Te = Symbol.for("react.lazy"), Yr = Symbol.for("react.offscreen"), Mt;
Mt = Symbol.for("react.module.reference");
function H(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Xe:
        switch (e = e.type, e) {
          case pe:
          case ye:
          case be:
          case Ce:
          case we:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case qr:
              case Se:
              case xe:
              case Te:
              case _e:
              case ve:
                return e;
              default:
                return t;
            }
        }
      case Ne:
        return t;
    }
  }
}
E.ContextConsumer = Se;
E.ContextProvider = ve;
E.Element = Xe;
E.ForwardRef = xe;
E.Fragment = pe;
E.Lazy = Te;
E.Memo = _e;
E.Portal = Ne;
E.Profiler = ye;
E.StrictMode = be;
E.Suspense = Ce;
E.SuspenseList = we;
E.isAsyncMode = function() {
  return !1;
};
E.isConcurrentMode = function() {
  return !1;
};
E.isContextConsumer = function(e) {
  return H(e) === Se;
};
E.isContextProvider = function(e) {
  return H(e) === ve;
};
E.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Xe;
};
E.isForwardRef = function(e) {
  return H(e) === xe;
};
E.isFragment = function(e) {
  return H(e) === pe;
};
E.isLazy = function(e) {
  return H(e) === Te;
};
E.isMemo = function(e) {
  return H(e) === _e;
};
E.isPortal = function(e) {
  return H(e) === Ne;
};
E.isProfiler = function(e) {
  return H(e) === ye;
};
E.isStrictMode = function(e) {
  return H(e) === be;
};
E.isSuspense = function(e) {
  return H(e) === Ce;
};
E.isSuspenseList = function(e) {
  return H(e) === we;
};
E.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === pe || e === ye || e === be || e === Ce || e === we || e === Yr || typeof e == "object" && e !== null && (e.$$typeof === Te || e.$$typeof === _e || e.$$typeof === ve || e.$$typeof === Se || e.$$typeof === xe || e.$$typeof === Mt || e.getModuleId !== void 0);
};
E.typeOf = H;
function Qr(e, t) {
  if (N(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t || "default");
    if (N(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Ot(e) {
  var t = Qr(e, "string");
  return N(t) == "symbol" ? t : t + "";
}
function R(e, t, n) {
  return (t = Ot(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function ct(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function D(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? ct(Object(n), !0).forEach(function(o) {
      R(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : ct(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function Ee(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function Jr(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Ot(o.key), o);
  }
}
function Me(e, t, n) {
  return t && Jr(e.prototype, t), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Be(e, t) {
  return Be = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Be(e, t);
}
function Pt(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Be(e, t);
}
function ge(e) {
  return ge = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, ge(e);
}
function It() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (It = function() {
    return !!e;
  })();
}
function re(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Zr(e, t) {
  if (t && (N(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return re(e);
}
function Rt(e) {
  var t = It();
  return function() {
    var n, o = ge(e);
    if (t) {
      var r = ge(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return Zr(this, n);
  };
}
var kt = /* @__PURE__ */ Me(function e() {
  Ee(this, e);
}), jt = "CALC_UNIT", en = new RegExp(jt, "g");
function Re(e) {
  return typeof e == "number" ? "".concat(e).concat(jt) : e;
}
var tn = /* @__PURE__ */ function(e) {
  Pt(n, e);
  var t = Rt(n);
  function n(o, r) {
    var s;
    Ee(this, n), s = t.call(this), R(re(s), "result", ""), R(re(s), "unitlessCssVar", void 0), R(re(s), "lowPriority", void 0);
    var i = N(o);
    return s.unitlessCssVar = r, o instanceof n ? s.result = "(".concat(o.result, ")") : i === "number" ? s.result = Re(o) : i === "string" && (s.result = o), s;
  }
  return Me(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(Re(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(Re(r))), this.lowPriority = !0, this;
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
      var s = this, i = r || {}, a = i.unit, l = !0;
      return typeof a == "boolean" ? l = a : Array.from(this.unitlessCssVar).some(function(f) {
        return s.result.includes(f);
      }) && (l = !1), this.result = this.result.replace(en, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(kt), rn = /* @__PURE__ */ function(e) {
  Pt(n, e);
  var t = Rt(n);
  function n(o) {
    var r;
    return Ee(this, n), r = t.call(this), R(re(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Me(n, [{
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
}(kt), nn = function(t, n) {
  var o = t === "css" ? tn : rn;
  return function(r) {
    return new o(r, n);
  };
}, ut = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function ft(e, t, n, o) {
  var r = D({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var s = o.deprecatedTokens;
    s.forEach(function(a) {
      var l = de(a, 2), f = l[0], c = l[1];
      if (r != null && r[f] || r != null && r[c]) {
        var u;
        (u = r[c]) !== null && u !== void 0 || (r[c] = r == null ? void 0 : r[f]);
      }
    });
  }
  var i = D(D({}, n), r);
  return Object.keys(i).forEach(function(a) {
    i[a] === t[a] && delete i[a];
  }), i;
}
var Lt = typeof CSSINJS_STATISTIC < "u", He = !0;
function Ve() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!Lt)
    return Object.assign.apply(Object, [{}].concat(t));
  He = !1;
  var o = {};
  return t.forEach(function(r) {
    if (N(r) === "object") {
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
  }), He = !0, o;
}
var dt = {};
function on() {
}
var sn = function(t) {
  var n, o = t, r = on;
  return Lt && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(i, a) {
      if (He) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return i[a];
    }
  }), r = function(i, a) {
    var l;
    dt[i] = {
      global: Array.from(n),
      component: D(D({}, (l = dt[i]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function ht(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Ve(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function an(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(s) {
        return oe(s);
      }).join(","), ")");
    }
  };
}
var ln = 1e3 * 60 * 10, cn = /* @__PURE__ */ function() {
  function e() {
    Ee(this, e), R(this, "map", /* @__PURE__ */ new Map()), R(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), R(this, "nextID", 0), R(this, "lastAccessBeat", /* @__PURE__ */ new Map()), R(this, "accessBeat", 0);
  }
  return Me(e, [{
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
        return s && N(s) === "object" ? "obj_".concat(o.getObjectID(s)) : "".concat(N(s), "_").concat(s);
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
          o - r > ln && (n.map.delete(s), n.lastAccessBeat.delete(s));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), gt = new cn();
function un(e, t) {
  return h.useMemo(function() {
    var n = gt.get(t);
    if (n)
      return n;
    var o = e();
    return gt.set(t, o), o;
  }, t);
}
var fn = function() {
  return {};
};
function dn(e) {
  var t = e.useCSP, n = t === void 0 ? fn : t, o = e.useToken, r = e.usePrefix, s = e.getResetStyles, i = e.getCommonStyle, a = e.getCompUnitless;
  function l(d, b, v, x) {
    var g = Array.isArray(d) ? d[0] : d;
    function m(O) {
      return "".concat(String(g)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var _ = (x == null ? void 0 : x.unitless) || {}, k = typeof a == "function" ? a(d) : {}, p = D(D({}, k), {}, R({}, m("zIndexPopup"), !0));
    Object.keys(_).forEach(function(O) {
      p[m(O)] = _[O];
    });
    var C = D(D({}, x), {}, {
      unitless: p,
      prefixToken: m
    }), y = c(d, b, v, C), M = f(g, v, C);
    return function(O) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, P = y(O, S), z = de(P, 2), L = z[1], A = M(S), w = de(A, 2), T = w[0], j = w[1];
      return [T, L, j];
    };
  }
  function f(d, b, v) {
    var x = v.unitless, g = v.injectStyle, m = g === void 0 ? !0 : g, _ = v.prefixToken, k = v.ignore, p = function(M) {
      var O = M.rootCls, S = M.cssVar, P = S === void 0 ? {} : S, z = o(), L = z.realToken;
      return Jt({
        path: [d],
        prefix: P.prefix,
        key: P.key,
        unitless: x,
        ignore: k,
        token: L,
        scope: O
      }, function() {
        var A = ht(d, L, b), w = ft(d, L, A, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(A).forEach(function(T) {
          w[_(T)] = w[T], delete w[T];
        }), w;
      }), null;
    }, C = function(M) {
      var O = o(), S = O.cssVar;
      return [function(P) {
        return m && S ? /* @__PURE__ */ h.createElement(h.Fragment, null, /* @__PURE__ */ h.createElement(p, {
          rootCls: M,
          cssVar: S,
          component: d
        }), P) : P;
      }, S == null ? void 0 : S.key];
    };
    return C;
  }
  function c(d, b, v) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], m = de(g, 1), _ = m[0], k = g.join("-"), p = e.layer || {
      name: "antd"
    };
    return function(C) {
      var y = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, M = o(), O = M.theme, S = M.realToken, P = M.hashId, z = M.token, L = M.cssVar, A = r(), w = A.rootPrefixCls, T = A.iconPrefixCls, j = n(), F = L ? "css" : "js", W = un(function() {
        var X = /* @__PURE__ */ new Set();
        return L && Object.keys(x.unitless || {}).forEach(function(G) {
          X.add(Oe(G, L.prefix)), X.add(Oe(G, ut(_, L.prefix)));
        }), nn(F, X);
      }, [F, _, L == null ? void 0 : L.prefix]), U = an(F), K = U.max, J = U.min, Z = {
        theme: O,
        token: z,
        hashId: P,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: x.clientOnly,
        layer: p,
        // antd is always at top of styles
        order: x.order || -999
      };
      typeof s == "function" && Ye(D(D({}, Z), {}, {
        clientOnly: !1,
        path: ["Shared", w]
      }), function() {
        return s(z, {
          prefix: {
            rootPrefixCls: w,
            iconPrefixCls: T
          },
          csp: j
        });
      });
      var ee = Ye(D(D({}, Z), {}, {
        path: [k, C, T]
      }), function() {
        if (x.injectStyle === !1)
          return [];
        var X = sn(z), G = X.token, Ht = X.flush, q = ht(_, S, v), zt = ".".concat(C), Ue = ft(_, S, q, {
          deprecatedTokens: x.deprecatedTokens
        });
        L && q && N(q) === "object" && Object.keys(q).forEach(function(Ke) {
          q[Ke] = "var(".concat(Oe(Ke, ut(_, L.prefix)), ")");
        });
        var Ge = Ve(G, {
          componentCls: zt,
          prefixCls: C,
          iconCls: ".".concat(T),
          antCls: ".".concat(w),
          calc: W,
          // @ts-ignore
          max: K,
          // @ts-ignore
          min: J
        }, L ? q : Ue), At = b(Ge, {
          hashId: P,
          prefixCls: C,
          rootPrefixCls: w,
          iconPrefixCls: T
        });
        Ht(_, Ue);
        var Ft = typeof i == "function" ? i(Ge, C, y, x.resetFont) : null;
        return [x.resetStyle === !1 ? null : Ft, At];
      });
      return [ee, P];
    };
  }
  function u(d, b, v) {
    var x = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = c(d, b, v, D({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, x)), m = function(k) {
      var p = k.prefixCls, C = k.rootCls, y = C === void 0 ? p : C;
      return g(p, y), null;
    };
    return m;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: c
  };
}
const $ = Math.round;
function ke(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const mt = (e, t, n) => n === 0 ? e : e / 100;
function te(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class V {
  constructor(t) {
    R(this, "isValid", !0), R(this, "r", 0), R(this, "g", 0), R(this, "b", 0), R(this, "a", 1), R(this, "_h", void 0), R(this, "_s", void 0), R(this, "_l", void 0), R(this, "_v", void 0), R(this, "_max", void 0), R(this, "_min", void 0), R(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(s) {
        return o.startsWith(s);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof V)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = te(t.r), this.g = te(t.g), this.b = te(t.b), this.a = typeof t.a == "number" ? te(t.a, 1) : 1;
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
    function t(s) {
      const i = s / 255;
      return i <= 0.03928 ? i / 12.92 : Math.pow((i + 0.055) / 1.055, 2.4);
    }
    const n = t(this.r), o = t(this.g), r = t(this.b);
    return 0.2126 * n + 0.7152 * o + 0.0722 * r;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = $(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const o = this._c(t), r = n / 100, s = (a) => (o[a] - this[a]) * r + this[a], i = {
      r: $(s("r")),
      g: $(s("g")),
      b: $(s("b")),
      a: $(s("a") * 100) / 100
    };
    return this._c(i);
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
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (s) => $((this[s] * this.a + n[s] * n.a * (1 - this.a)) / o);
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
      const s = $(this.a * 255).toString(16);
      t += s.length === 2 ? s : "0" + s;
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
    const t = this.getHue(), n = $(this.getSaturation() * 100), o = $(this.getLightness() * 100);
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
    return r[t] = te(n, o), r;
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
    function o(r, s) {
      return parseInt(n[r] + n[s || r], 16);
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
      const d = $(o * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let s = 0, i = 0, a = 0;
    const l = t / 60, f = (1 - Math.abs(2 * o - 1)) * n, c = f * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (s = f, i = c) : l >= 1 && l < 2 ? (s = c, i = f) : l >= 2 && l < 3 ? (i = f, a = c) : l >= 3 && l < 4 ? (i = c, a = f) : l >= 4 && l < 5 ? (s = c, a = f) : l >= 5 && l < 6 && (s = f, a = c);
    const u = o - f / 2;
    this.r = $((s + u) * 255), this.g = $((i + u) * 255), this.b = $((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const s = $(o * 255);
    if (this.r = s, this.g = s, this.b = s, n <= 0)
      return;
    const i = t / 60, a = Math.floor(i), l = i - a, f = $(o * (1 - n) * 255), c = $(o * (1 - n * l) * 255), u = $(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = f;
        break;
      case 1:
        this.r = c, this.b = f;
        break;
      case 2:
        this.r = f, this.b = u;
        break;
      case 3:
        this.r = f, this.g = c;
        break;
      case 4:
        this.r = u, this.g = f;
        break;
      case 5:
      default:
        this.g = f, this.b = c;
        break;
    }
  }
  fromHsvString(t) {
    const n = ke(t, mt);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = ke(t, mt);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = ke(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? $(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const hn = {
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
}, gn = Object.assign(Object.assign({}, hn), {
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
function je(e) {
  return e >= 0 && e <= 255;
}
function ie(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: s
  } = new V(e).toRgb();
  if (s < 1)
    return e;
  const {
    r: i,
    g: a,
    b: l
  } = new V(t).toRgb();
  for (let f = 0.01; f <= 1; f += 0.01) {
    const c = Math.round((n - i * (1 - f)) / f), u = Math.round((o - a * (1 - f)) / f), d = Math.round((r - l * (1 - f)) / f);
    if (je(c) && je(u) && je(d))
      return new V({
        r: c,
        g: u,
        b: d,
        a: Math.round(f * 100) / 100
      }).toRgbString();
  }
  return new V({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var mn = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function pn(e) {
  const {
    override: t
  } = e, n = mn(e, ["override"]), o = Object.assign({}, t);
  Object.keys(gn).forEach((d) => {
    delete o[d];
  });
  const r = Object.assign(Object.assign({}, n), o), s = 480, i = 576, a = 768, l = 992, f = 1200, c = 1600;
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
    colorSplit: ie(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: ie(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: ie(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: ie(r.colorPrimaryBg, r.colorBgContainer),
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
    screenMDMax: l - 1,
    screenLG: l,
    screenLGMin: l,
    screenLGMax: f - 1,
    screenXL: f,
    screenXLMin: f,
    screenXLMax: c - 1,
    screenXXL: c,
    screenXXLMin: c,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new V("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new V("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new V("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const bn = {
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
}, yn = {
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
}, vn = Zt($e.defaultAlgorithm), Sn = {
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
}, $t = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...s
  } = t;
  let i = {
    ...o,
    override: r
  };
  return i = pn(i), s && Object.entries(s).forEach(([a, l]) => {
    const {
      theme: f,
      ...c
    } = l;
    let u = c;
    f && (u = $t({
      ...i,
      ...c
    }, {
      override: c
    }, f)), i[a] = u;
  }), i;
};
function xn() {
  const {
    token: e,
    hashed: t,
    theme: n = vn,
    override: o,
    cssVar: r
  } = h.useContext($e._internalContext), [s, i, a] = er(n, [$e.defaultSeed, e], {
    salt: `${zr}-${t || ""}`,
    override: o,
    getComputedToken: $t,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: bn,
      ignore: yn,
      preserve: Sn
    }
  });
  return [n, a, t ? i : "", s, r];
}
const {
  genStyleHooks: Cn,
  genComponentStyleHook: ao,
  genSubStyleComponent: lo
} = dn({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = he();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = xn();
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
    } = he();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var wn = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, _n = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Tn = "".concat(wn, " ").concat(_n).split(/[\s\n]+/), En = "aria-", Mn = "data-";
function pt(e, t) {
  return e.indexOf(t) === 0;
}
function On(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = D({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || pt(r, En)) || // Data
    n.data && pt(r, Mn) || // Attr
    n.attr && Tn.includes(r)) && (o[r] = e[r]);
  }), o;
}
function ae(e) {
  return typeof e == "string";
}
const Pn = (e, t, n, o) => {
  const [r, s] = I.useState(""), [i, a] = I.useState(1), l = t && ae(e);
  return Kr(() => {
    s(e), !l && ae(e) ? a(e.length) : ae(e) && ae(r) && e.indexOf(r) !== 0 && a(1);
  }, [e]), I.useEffect(() => {
    if (l && i < e.length) {
      const c = setTimeout(() => {
        a((u) => u + n);
      }, o);
      return () => {
        clearTimeout(c);
      };
    }
  }, [i, t, e]), [l ? e.slice(0, i) : e, l && i < e.length];
};
function In(e) {
  return I.useMemo(() => {
    if (!e)
      return [!1, 0, 0, null];
    let t = {
      step: 1,
      interval: 50,
      // set default suffix is empty
      suffix: null
    };
    return typeof e == "object" && (t = {
      ...t,
      ...e
    }), [!0, t.step, t.interval, t.suffix];
  }, [e]);
}
const Rn = ({
  prefixCls: e
}) => /* @__PURE__ */ h.createElement("span", {
  className: `${e}-dot`
}, /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-1"
}), /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-2"
}), /* @__PURE__ */ h.createElement("i", {
  className: `${e}-dot-item`,
  key: "item-3"
})), kn = (e) => {
  const {
    componentCls: t,
    paddingSM: n,
    padding: o
  } = e;
  return {
    [t]: {
      [`${t}-content`]: {
        // Shared: filled, outlined, shadow
        "&-filled,&-outlined,&-shadow": {
          padding: `${oe(n)} ${oe(o)}`,
          borderRadius: e.borderRadiusLG
        },
        // Filled:
        "&-filled": {
          backgroundColor: e.colorFillContent
        },
        // Outlined:
        "&-outlined": {
          border: `1px solid ${e.colorBorderSecondary}`
        },
        // Shadow:
        "&-shadow": {
          boxShadow: e.boxShadowTertiary
        }
      }
    }
  };
}, jn = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    padding: s,
    calc: i
  } = e, a = i(n).mul(o).div(2).add(r).equal(), l = `${t}-content`;
  return {
    [t]: {
      [l]: {
        // round:
        "&-round": {
          borderRadius: {
            _skip_check_: !0,
            value: a
          },
          paddingInline: i(s).mul(1.25).equal()
        }
      },
      // corner:
      [`&-start ${l}-corner`]: {
        borderStartStartRadius: e.borderRadiusXS
      },
      [`&-end ${l}-corner`]: {
        borderStartEndRadius: e.borderRadiusXS
      }
    }
  };
}, Ln = (e) => {
  const {
    componentCls: t,
    padding: n
  } = e;
  return {
    [`${t}-list`]: {
      display: "flex",
      flexDirection: "column",
      gap: n,
      overflowY: "auto"
    }
  };
}, $n = new vt("loadingMove", {
  "0%": {
    transform: "translateY(0)"
  },
  "10%": {
    transform: "translateY(4px)"
  },
  "20%": {
    transform: "translateY(0)"
  },
  "30%": {
    transform: "translateY(-4px)"
  },
  "40%": {
    transform: "translateY(0)"
  }
}), Dn = new vt("cursorBlink", {
  "0%": {
    opacity: 1
  },
  "50%": {
    opacity: 0
  },
  "100%": {
    opacity: 1
  }
}), Bn = (e) => {
  const {
    componentCls: t,
    fontSize: n,
    lineHeight: o,
    paddingSM: r,
    colorText: s,
    calc: i
  } = e;
  return {
    [t]: {
      display: "flex",
      columnGap: r,
      [`&${t}-end`]: {
        justifyContent: "end",
        flexDirection: "row-reverse",
        [`& ${t}-content-wrapper`]: {
          alignItems: "flex-end"
        }
      },
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      [`&${t}-typing ${t}-content:last-child::after`]: {
        content: '"|"',
        fontWeight: 900,
        userSelect: "none",
        opacity: 1,
        marginInlineStart: "0.1em",
        animationName: Dn,
        animationDuration: "0.8s",
        animationIterationCount: "infinite",
        animationTimingFunction: "linear"
      },
      // ============================ Avatar =============================
      [`& ${t}-avatar`]: {
        display: "inline-flex",
        justifyContent: "center",
        alignSelf: "flex-start"
      },
      // ======================== Header & Footer ========================
      [`& ${t}-header, & ${t}-footer`]: {
        fontSize: n,
        lineHeight: o,
        color: e.colorText
      },
      [`& ${t}-header`]: {
        marginBottom: e.paddingXXS
      },
      [`& ${t}-footer`]: {
        marginTop: r
      },
      // =========================== Content =============================
      [`& ${t}-content-wrapper`]: {
        flex: "auto",
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-start",
        minWidth: 0,
        maxWidth: "100%"
      },
      [`& ${t}-content`]: {
        position: "relative",
        boxSizing: "border-box",
        minWidth: 0,
        maxWidth: "100%",
        color: s,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        minHeight: i(r).mul(2).add(i(o).mul(n)).equal(),
        wordBreak: "break-word",
        [`& ${t}-dot`]: {
          position: "relative",
          height: "100%",
          display: "flex",
          alignItems: "center",
          columnGap: e.marginXS,
          padding: `0 ${oe(e.paddingXXS)}`,
          "&-item": {
            backgroundColor: e.colorPrimary,
            borderRadius: "100%",
            width: 4,
            height: 4,
            animationName: $n,
            animationDuration: "2s",
            animationIterationCount: "infinite",
            animationTimingFunction: "linear",
            "&:nth-child(1)": {
              animationDelay: "0s"
            },
            "&:nth-child(2)": {
              animationDelay: "0.2s"
            },
            "&:nth-child(3)": {
              animationDelay: "0.4s"
            }
          }
        }
      }
    }
  };
}, Hn = () => ({}), Dt = Cn("Bubble", (e) => {
  const t = Ve(e, {});
  return [Bn(t), Ln(t), kn(t), jn(t)];
}, Hn), Bt = /* @__PURE__ */ h.createContext({}), zn = (e, t) => {
  const {
    prefixCls: n,
    className: o,
    rootClassName: r,
    style: s,
    classNames: i = {},
    styles: a = {},
    avatar: l,
    placement: f = "start",
    loading: c = !1,
    loadingRender: u,
    typing: d,
    content: b = "",
    messageRender: v,
    variant: x = "filled",
    shape: g,
    onTypingComplete: m,
    header: _,
    footer: k,
    ...p
  } = e, {
    onUpdate: C
  } = h.useContext(Bt), y = h.useRef(null);
  h.useImperativeHandle(t, () => ({
    nativeElement: y.current
  }));
  const {
    direction: M,
    getPrefixCls: O
  } = he(), S = O("bubble", n), P = Xr("bubble"), [z, L, A, w] = In(d), [T, j] = Pn(b, z, L, A);
  h.useEffect(() => {
    C == null || C();
  }, [T]);
  const F = h.useRef(!1);
  h.useEffect(() => {
    !j && !c ? F.current || (F.current = !0, m == null || m()) : F.current = !1;
  }, [j, c]);
  const [W, U, K] = Dt(S), J = Y(S, r, P.className, o, U, K, `${S}-${f}`, {
    [`${S}-rtl`]: M === "rtl",
    [`${S}-typing`]: j && !c && !v && !w
  }), Z = /* @__PURE__ */ h.isValidElement(l) ? l : /* @__PURE__ */ h.createElement(Qt, l), ee = v ? v(T) : T;
  let X;
  c ? X = u ? u() : /* @__PURE__ */ h.createElement(Rn, {
    prefixCls: S
  }) : X = /* @__PURE__ */ h.createElement(h.Fragment, null, ee, j && w);
  let G = /* @__PURE__ */ h.createElement("div", {
    style: {
      ...P.styles.content,
      ...a.content
    },
    className: Y(`${S}-content`, `${S}-content-${x}`, g && `${S}-content-${g}`, P.classNames.content, i.content)
  }, X);
  return (_ || k) && (G = /* @__PURE__ */ h.createElement("div", {
    className: `${S}-content-wrapper`
  }, _ && /* @__PURE__ */ h.createElement("div", {
    className: Y(`${S}-header`, P.classNames.header, i.header),
    style: {
      ...P.styles.header,
      ...a.header
    }
  }, _), G, k && /* @__PURE__ */ h.createElement("div", {
    className: Y(`${S}-footer`, P.classNames.footer, i.footer),
    style: {
      ...P.styles.footer,
      ...a.footer
    }
  }, k))), W(/* @__PURE__ */ h.createElement("div", se({
    style: {
      ...P.style,
      ...s
    },
    className: J
  }, p, {
    ref: y
  }), l && /* @__PURE__ */ h.createElement("div", {
    style: {
      ...P.styles.avatar,
      ...a.avatar
    },
    className: Y(`${S}-avatar`, P.classNames.avatar, i.avatar)
  }, Z), G));
}, We = /* @__PURE__ */ h.forwardRef(zn);
function An(e) {
  const [t, n] = h.useState(e.length), o = h.useMemo(() => e.slice(0, t), [e, t]), r = h.useMemo(() => {
    const i = o[o.length - 1];
    return i ? i.key : null;
  }, [o]);
  h.useEffect(() => {
    var i;
    if (!(o.length && o.every((a, l) => {
      var f;
      return a.key === ((f = e[l]) == null ? void 0 : f.key);
    }))) {
      if (o.length === 0)
        n(1);
      else
        for (let a = 0; a < o.length; a += 1)
          if (o[a].key !== ((i = e[a]) == null ? void 0 : i.key)) {
            n(a);
            break;
          }
    }
  }, [e]);
  const s = Et((i) => {
    i === r && n(t + 1);
  });
  return [o, s];
}
function Fn(e, t) {
  const n = I.useCallback((o) => typeof t == "function" ? t(o) : t ? t[o.role] || {} : {}, [t]);
  return I.useMemo(() => (e || []).map((o, r) => {
    const s = o.key ?? `preset_${r}`;
    return {
      ...n(o),
      ...o,
      key: s
    };
  }), [e, n]);
}
const Xn = 1, Nn = (e, t) => {
  const {
    prefixCls: n,
    rootClassName: o,
    className: r,
    items: s,
    autoScroll: i = !0,
    roles: a,
    ...l
  } = e, f = On(l, {
    attr: !0,
    aria: !0
  }), c = I.useRef(null), u = I.useRef({}), {
    getPrefixCls: d
  } = he(), b = d("bubble", n), v = `${b}-list`, [x, g, m] = Dt(b), [_, k] = I.useState(!1);
  I.useEffect(() => (k(!0), () => {
    k(!1);
  }), []);
  const p = Fn(s, a), [C, y] = An(p), [M, O] = I.useState(!0), [S, P] = I.useState(0), z = (w) => {
    const T = w.target;
    O(T.scrollHeight - Math.abs(T.scrollTop) - T.clientHeight <= Xn);
  };
  I.useEffect(() => {
    i && c.current && M && c.current.scrollTo({
      top: c.current.scrollHeight
    });
  }, [S]), I.useEffect(() => {
    var w;
    if (i) {
      const T = (w = C[C.length - 2]) == null ? void 0 : w.key, j = u.current[T];
      if (j) {
        const {
          nativeElement: F
        } = j, {
          top: W,
          bottom: U
        } = F.getBoundingClientRect(), {
          top: K,
          bottom: J
        } = c.current.getBoundingClientRect();
        W < J && U > K && (P((ee) => ee + 1), O(!0));
      }
    }
  }, [C.length]), I.useImperativeHandle(t, () => ({
    nativeElement: c.current,
    scrollTo: ({
      key: w,
      offset: T,
      behavior: j = "smooth",
      block: F
    }) => {
      if (typeof T == "number")
        c.current.scrollTo({
          top: T,
          behavior: j
        });
      else if (w !== void 0) {
        const W = u.current[w];
        if (W) {
          const U = C.findIndex((K) => K.key === w);
          O(U === C.length - 1), W.nativeElement.scrollIntoView({
            behavior: j,
            block: F
          });
        }
      }
    }
  }));
  const L = Et(() => {
    i && P((w) => w + 1);
  }), A = I.useMemo(() => ({
    onUpdate: L
  }), []);
  return x(/* @__PURE__ */ I.createElement(Bt.Provider, {
    value: A
  }, /* @__PURE__ */ I.createElement("div", se({}, f, {
    className: Y(v, o, r, g, m, {
      [`${v}-reach-end`]: M
    }),
    ref: c,
    onScroll: z
  }), C.map(({
    key: w,
    ...T
  }) => /* @__PURE__ */ I.createElement(We, se({}, T, {
    key: w,
    ref: (j) => {
      j ? u.current[w] = j : delete u.current[w];
    },
    typing: _ ? T.typing : !1,
    onTypingComplete: () => {
      var j;
      (j = T.onTypingComplete) == null || j.call(T), y(w);
    }
  }))))));
}, Vn = /* @__PURE__ */ I.forwardRef(Nn);
We.List = Vn;
function Wn(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function Un(e, t = !1) {
  try {
    if (Fe(e))
      return e;
    if (t && !Wn(e))
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
function Gn(e, t) {
  return le(() => Un(e, t), [e, t]);
}
function Kn(e, t) {
  return t((o, r) => Fe(o) ? r ? (...s) => o(...s, ...e) : o(...e) : o);
}
const qn = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function Yn(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = Qn(n, o), t;
  }, {}) : {};
}
function Qn(e, t) {
  return typeof t == "number" && !qn.includes(e) ? t + "px" : t;
}
function ze(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = h.Children.toArray(e._reactElement.props.children).map((s) => {
      if (h.isValidElement(s) && s.props.__slot__) {
        const {
          portals: i,
          clonedElement: a
        } = ze(s.props.el);
        return h.cloneElement(s, {
          ...s.props,
          el: a,
          children: [...h.Children.toArray(s.props.children), ...i]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(Le(h.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: i,
      type: a,
      useCapture: l
    }) => {
      n.addEventListener(a, i, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const s = o[r];
    if (s.nodeType === 1) {
      const {
        clonedElement: i,
        portals: a
      } = ze(s);
      t.push(...a), n.appendChild(i);
    } else s.nodeType === 3 && n.appendChild(s.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function Jn(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const bt = Xt(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, s) => {
  const i = Nt(), [a, l] = Vt([]), {
    forceClone: f
  } = qt(), c = f ? !0 : t;
  return Wt(() => {
    var x;
    if (!i.current || !e)
      return;
    let u = e;
    function d() {
      let g = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (g = u.children[0], g.tagName.toLowerCase() === "react-portal-target" && g.children[0] && (g = g.children[0])), Jn(s, g), n && g.classList.add(...n.split(" ")), o) {
        const m = Yn(o);
        Object.keys(m).forEach((_) => {
          g.style[_] = m[_];
        });
      }
    }
    let b = null, v = null;
    if (c && window.MutationObserver) {
      let g = function() {
        var p, C, y;
        (p = i.current) != null && p.contains(u) && ((C = i.current) == null || C.removeChild(u));
        const {
          portals: _,
          clonedElement: k
        } = ze(e);
        u = k, l(_), u.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (y = i.current) == null || y.appendChild(u);
      };
      g();
      const m = dr(() => {
        g(), b == null || b.disconnect(), b == null || b.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      b = new window.MutationObserver(m), b.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", d(), (x = i.current) == null || x.appendChild(u);
    return () => {
      var g, m;
      u.style.display = "", (g = i.current) != null && g.contains(u) && ((m = i.current) == null || m.removeChild(u)), b == null || b.disconnect();
    };
  }, [e, c, n, o, s, r]), h.createElement("react-child", {
    ref: i,
    style: {
      display: "contents"
    }
  }, ...a);
}), Zn = ({
  children: e,
  ...t
}) => /* @__PURE__ */ B.jsx(B.Fragment, {
  children: e(t)
});
function eo(e) {
  return h.createElement(Zn, {
    children: e
  });
}
function Ae(e, t, n) {
  const o = e.filter(Boolean);
  if (o.length !== 0)
    return o.map((r, s) => {
      var f;
      if (typeof r != "object")
        return t != null && t.fallback ? t.fallback(r) : r;
      const i = {
        ...r.props,
        key: ((f = r.props) == null ? void 0 : f.key) ?? (n ? `${n}-${s}` : `${s}`)
      };
      let a = i;
      Object.keys(r.slots).forEach((c) => {
        if (!r.slots[c] || !(r.slots[c] instanceof Element) && !r.slots[c].el)
          return;
        const u = c.split(".");
        u.forEach((m, _) => {
          a[m] || (a[m] = {}), _ !== u.length - 1 && (a = i[m]);
        });
        const d = r.slots[c];
        let b, v, x = (t == null ? void 0 : t.clone) ?? !1, g = t == null ? void 0 : t.forceClone;
        d instanceof Element ? b = d : (b = d.el, v = d.callback, x = d.clone ?? x, g = d.forceClone ?? g), g = g ?? !!v, a[u[u.length - 1]] = b ? v ? (...m) => (v(u[u.length - 1], m), /* @__PURE__ */ B.jsx(qe, {
          ...r.ctx,
          params: m,
          forceClone: g,
          children: /* @__PURE__ */ B.jsx(bt, {
            slot: b,
            clone: x
          })
        })) : eo((m) => /* @__PURE__ */ B.jsx(qe, {
          ...r.ctx,
          forceClone: g,
          children: /* @__PURE__ */ B.jsx(bt, {
            slot: b,
            clone: x,
            ...m
          })
        })) : a[u[u.length - 1]], a = i;
      });
      const l = (t == null ? void 0 : t.children) || "children";
      return r[l] ? i[l] = Ae(r[l], t, `${s}`) : t != null && t.children && (i[l] = void 0, Reflect.deleteProperty(i, l)), i;
    });
}
const {
  useItems: to,
  withItemsContextProvider: ro,
  ItemHandler: co
} = yt("antdx-bubble.list-items"), {
  useItems: no,
  withItemsContextProvider: oo,
  ItemHandler: uo
} = yt("antdx-bubble.list-roles");
function so(e, t) {
  return Kn(t, (n) => {
    var o, r;
    return {
      ...e,
      avatar: Fe(e.avatar) ? n(e.avatar) : ne(e.avatar) ? {
        ...e.avatar,
        icon: n((o = e.avatar) == null ? void 0 : o.icon),
        src: n((r = e.avatar) == null ? void 0 : r.src)
      } : e.avatar,
      footer: n(e.footer),
      header: n(e.header),
      loadingRender: n(e.loadingRender, !0),
      messageRender: n(e.messageRender, !0)
    };
  });
}
const fo = Hr(oo(["roles"], ro(["items", "default"], ({
  items: e,
  roles: t,
  children: n,
  ...o
}) => {
  const r = Gn(t), {
    items: {
      roles: s
    }
  } = no(), {
    items: i
  } = to(), a = le(() => {
    var c;
    return t || ((c = Ae(s, {
      clone: !0,
      forceClone: !0
    })) == null ? void 0 : c.reduce((u, d) => (d.role !== void 0 && (u[d.role] = d), u), {}));
  }, [s, t]), l = i.items.length > 0 ? i.items : i.default, f = le(() => (c, u) => c.role && (a || {})[c.role] ? so((a || {})[c.role], [c, u]) : {
    messageRender(d) {
      return /* @__PURE__ */ B.jsx(B.Fragment, {
        children: ne(d) ? JSON.stringify(d) : d
      });
    }
  }, [a]);
  return /* @__PURE__ */ B.jsxs(B.Fragment, {
    children: [/* @__PURE__ */ B.jsx("div", {
      style: {
        display: "none"
      },
      children: n
    }), /* @__PURE__ */ B.jsx(We.List, {
      ...o,
      items: le(() => e || Ae(l), [e, l]),
      roles: r || f
    })]
  });
})));
export {
  fo as BubbleList,
  fo as default
};
