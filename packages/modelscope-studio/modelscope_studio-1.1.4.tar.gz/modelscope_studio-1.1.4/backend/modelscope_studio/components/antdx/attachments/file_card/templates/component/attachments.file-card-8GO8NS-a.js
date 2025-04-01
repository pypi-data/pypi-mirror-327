import { g as Gr, w as Ae, c as K } from "./Index-BRZjO3Ri.js";
const P = window.ms_globals.React, a = window.ms_globals.React, Ur = window.ms_globals.React.isValidElement, ae = window.ms_globals.React.useRef, Wr = window.ms_globals.React.useLayoutEffect, Ie = window.ms_globals.React.useEffect, Ot = window.ms_globals.ReactDOM, pt = window.ms_globals.ReactDOM.createPortal, Kr = window.ms_globals.antd.ConfigProvider, ur = window.ms_globals.antd.Upload, ke = window.ms_globals.antd.theme, qr = window.ms_globals.antd.Progress, rt = window.ms_globals.antd.Button, Zr = window.ms_globals.antd.Flex, nt = window.ms_globals.antd.Typography, Qr = window.ms_globals.antdIcons.FileTextFilled, Yr = window.ms_globals.antdIcons.CloseCircleFilled, Jr = window.ms_globals.antdIcons.FileExcelFilled, en = window.ms_globals.antdIcons.FileImageFilled, tn = window.ms_globals.antdIcons.FileMarkdownFilled, rn = window.ms_globals.antdIcons.FilePdfFilled, nn = window.ms_globals.antdIcons.FilePptFilled, on = window.ms_globals.antdIcons.FileWordFilled, sn = window.ms_globals.antdIcons.FileZipFilled, an = window.ms_globals.antdIcons.PlusOutlined, ln = window.ms_globals.antdIcons.LeftOutlined, cn = window.ms_globals.antdIcons.RightOutlined, It = window.ms_globals.antdCssinjs.unit, ot = window.ms_globals.antdCssinjs.token2CSSVar, At = window.ms_globals.antdCssinjs.useStyleRegister, un = window.ms_globals.antdCssinjs.useCSSVarRegister, fn = window.ms_globals.antdCssinjs.createTheme, dn = window.ms_globals.antdCssinjs.useCacheToken;
var fr = {
  exports: {}
}, ze = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var pn = a, gn = Symbol.for("react.element"), mn = Symbol.for("react.fragment"), hn = Object.prototype.hasOwnProperty, vn = pn.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, bn = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function dr(e, t, o) {
  var r, n = {}, i = null, s = null;
  o !== void 0 && (i = "" + o), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) hn.call(t, r) && !bn.hasOwnProperty(r) && (n[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) n[r] === void 0 && (n[r] = t[r]);
  return {
    $$typeof: gn,
    type: e,
    key: i,
    ref: s,
    props: n,
    _owner: vn.current
  };
}
ze.Fragment = mn;
ze.jsx = dr;
ze.jsxs = dr;
fr.exports = ze;
var yn = fr.exports;
const {
  SvelteComponent: Sn,
  assign: $t,
  binding_callbacks: Ft,
  check_outros: xn,
  children: pr,
  claim_element: gr,
  claim_space: wn,
  component_subscribe: kt,
  compute_slots: En,
  create_slot: Cn,
  detach: ce,
  element: mr,
  empty: jt,
  exclude_internal_props: Dt,
  get_all_dirty_from_scope: _n,
  get_slot_changes: Ln,
  group_outros: Tn,
  init: Rn,
  insert_hydration: $e,
  safe_not_equal: Mn,
  set_custom_element_data: hr,
  space: Pn,
  transition_in: Fe,
  transition_out: gt,
  update_slot_base: On
} = window.__gradio__svelte__internal, {
  beforeUpdate: In,
  getContext: An,
  onDestroy: $n,
  setContext: Fn
} = window.__gradio__svelte__internal;
function zt(e) {
  let t, o;
  const r = (
    /*#slots*/
    e[7].default
  ), n = Cn(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = mr("svelte-slot"), n && n.c(), this.h();
    },
    l(i) {
      t = gr(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = pr(t);
      n && n.l(s), s.forEach(ce), this.h();
    },
    h() {
      hr(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      $e(i, t, s), n && n.m(t, null), e[9](t), o = !0;
    },
    p(i, s) {
      n && n.p && (!o || s & /*$$scope*/
      64) && On(
        n,
        r,
        i,
        /*$$scope*/
        i[6],
        o ? Ln(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : _n(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      o || (Fe(n, i), o = !0);
    },
    o(i) {
      gt(n, i), o = !1;
    },
    d(i) {
      i && ce(t), n && n.d(i), e[9](null);
    }
  };
}
function kn(e) {
  let t, o, r, n, i = (
    /*$$slots*/
    e[4].default && zt(e)
  );
  return {
    c() {
      t = mr("react-portal-target"), o = Pn(), i && i.c(), r = jt(), this.h();
    },
    l(s) {
      t = gr(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), pr(t).forEach(ce), o = wn(s), i && i.l(s), r = jt(), this.h();
    },
    h() {
      hr(t, "class", "svelte-1rt0kpf");
    },
    m(s, l) {
      $e(s, t, l), e[8](t), $e(s, o, l), i && i.m(s, l), $e(s, r, l), n = !0;
    },
    p(s, [l]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, l), l & /*$$slots*/
      16 && Fe(i, 1)) : (i = zt(s), i.c(), Fe(i, 1), i.m(r.parentNode, r)) : i && (Tn(), gt(i, 1, 1, () => {
        i = null;
      }), xn());
    },
    i(s) {
      n || (Fe(i), n = !0);
    },
    o(s) {
      gt(i), n = !1;
    },
    d(s) {
      s && (ce(t), ce(o), ce(r)), e[8](null), i && i.d(s);
    }
  };
}
function Ht(e) {
  const {
    svelteInit: t,
    ...o
  } = e;
  return o;
}
function jn(e, t, o) {
  let r, n, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const l = En(i);
  let {
    svelteInit: u
  } = t;
  const c = Ae(Ht(t)), f = Ae();
  kt(e, f, (b) => o(0, r = b));
  const p = Ae();
  kt(e, p, (b) => o(1, n = b));
  const d = [], m = An("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: h,
    subSlotIndex: g
  } = Gr() || {}, I = u({
    parent: m,
    props: c,
    target: f,
    slot: p,
    slotKey: v,
    slotIndex: h,
    subSlotIndex: g,
    onDestroy(b) {
      d.push(b);
    }
  });
  Fn("$$ms-gr-react-wrapper", I), In(() => {
    c.set(Ht(t));
  }), $n(() => {
    d.forEach((b) => b());
  });
  function _(b) {
    Ft[b ? "unshift" : "push"](() => {
      r = b, f.set(r);
    });
  }
  function S(b) {
    Ft[b ? "unshift" : "push"](() => {
      n = b, p.set(n);
    });
  }
  return e.$$set = (b) => {
    o(17, t = $t($t({}, t), Dt(b))), "svelteInit" in b && o(5, u = b.svelteInit), "$$scope" in b && o(6, s = b.$$scope);
  }, t = Dt(t), [r, n, f, p, l, u, s, i, _, S];
}
class Dn extends Sn {
  constructor(t) {
    super(), Rn(this, t, jn, kn, Mn, {
      svelteInit: 5
    });
  }
}
const Nt = window.ms_globals.rerender, it = window.ms_globals.tree;
function zn(e, t = {}) {
  function o(r) {
    const n = Ae(), i = new Dn({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const l = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, u = s.parent ?? it;
          return u.nodes = [...u.nodes, l], Nt({
            createPortal: pt,
            node: it
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((c) => c.svelteInstance !== n), Nt({
              createPortal: pt,
              node: it
            });
          }), l;
        },
        ...r.props
      }
    });
    return n.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(o);
    });
  });
}
const Hn = "1.0.5", Nn = /* @__PURE__ */ a.createContext({}), Bn = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Vn = (e) => {
  const t = a.useContext(Nn);
  return a.useMemo(() => ({
    ...Bn,
    ...t[e]
  }), [t[e]]);
};
function he() {
  return he = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var o = arguments[t];
      for (var r in o) ({}).hasOwnProperty.call(o, r) && (e[r] = o[r]);
    }
    return e;
  }, he.apply(null, arguments);
}
function je() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: o,
    iconPrefixCls: r,
    theme: n
  } = a.useContext(Kr.ConfigContext);
  return {
    theme: n,
    getPrefixCls: e,
    direction: t,
    csp: o,
    iconPrefixCls: r
  };
}
function de(e) {
  var t = P.useRef();
  t.current = e;
  var o = P.useCallback(function() {
    for (var r, n = arguments.length, i = new Array(n), s = 0; s < n; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return o;
}
function Xn(e) {
  if (Array.isArray(e)) return e;
}
function Un(e, t) {
  var o = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (o != null) {
    var r, n, i, s, l = [], u = !0, c = !1;
    try {
      if (i = (o = o.call(e)).next, t === 0) {
        if (Object(o) !== o) return;
        u = !1;
      } else for (; !(u = (r = i.call(o)).done) && (l.push(r.value), l.length !== t); u = !0) ;
    } catch (f) {
      c = !0, n = f;
    } finally {
      try {
        if (!u && o.return != null && (s = o.return(), Object(s) !== s)) return;
      } finally {
        if (c) throw n;
      }
    }
    return l;
  }
}
function Bt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var o = 0, r = Array(t); o < t; o++) r[o] = e[o];
  return r;
}
function Wn(e, t) {
  if (e) {
    if (typeof e == "string") return Bt(e, t);
    var o = {}.toString.call(e).slice(8, -1);
    return o === "Object" && e.constructor && (o = e.constructor.name), o === "Map" || o === "Set" ? Array.from(e) : o === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(o) ? Bt(e, t) : void 0;
  }
}
function Gn() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function V(e, t) {
  return Xn(e) || Un(e, t) || Wn(e, t) || Gn();
}
function He() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Vt = He() ? P.useLayoutEffect : P.useEffect, Kn = function(t, o) {
  var r = P.useRef(!0);
  Vt(function() {
    return t(r.current);
  }, o), Vt(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, Xt = function(t, o) {
  Kn(function(r) {
    if (!r)
      return t();
  }, o);
};
function ve(e) {
  var t = P.useRef(!1), o = P.useState(e), r = V(o, 2), n = r[0], i = r[1];
  P.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(l, u) {
    u && t.current || i(l);
  }
  return [n, s];
}
function st(e) {
  return e !== void 0;
}
function qn(e, t) {
  var o = t || {}, r = o.defaultValue, n = o.value, i = o.onChange, s = o.postState, l = ve(function() {
    return st(n) ? n : st(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), u = V(l, 2), c = u[0], f = u[1], p = n !== void 0 ? n : c, d = s ? s(p) : p, m = de(i), v = ve([p]), h = V(v, 2), g = h[0], I = h[1];
  Xt(function() {
    var S = g[0];
    c !== S && m(c, S);
  }, [g]), Xt(function() {
    st(n) || f(n);
  }, [n]);
  var _ = de(function(S, b) {
    f(S, b), I([p], b);
  });
  return [d, _];
}
function N(e) {
  "@babel/helpers - typeof";
  return N = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, N(e);
}
var vr = {
  exports: {}
}, O = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ct = Symbol.for("react.element"), _t = Symbol.for("react.portal"), Ne = Symbol.for("react.fragment"), Be = Symbol.for("react.strict_mode"), Ve = Symbol.for("react.profiler"), Xe = Symbol.for("react.provider"), Ue = Symbol.for("react.context"), Zn = Symbol.for("react.server_context"), We = Symbol.for("react.forward_ref"), Ge = Symbol.for("react.suspense"), Ke = Symbol.for("react.suspense_list"), qe = Symbol.for("react.memo"), Ze = Symbol.for("react.lazy"), Qn = Symbol.for("react.offscreen"), br;
br = Symbol.for("react.module.reference");
function q(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case Ct:
        switch (e = e.type, e) {
          case Ne:
          case Ve:
          case Be:
          case Ge:
          case Ke:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Zn:
              case Ue:
              case We:
              case Ze:
              case qe:
              case Xe:
                return e;
              default:
                return t;
            }
        }
      case _t:
        return t;
    }
  }
}
O.ContextConsumer = Ue;
O.ContextProvider = Xe;
O.Element = Ct;
O.ForwardRef = We;
O.Fragment = Ne;
O.Lazy = Ze;
O.Memo = qe;
O.Portal = _t;
O.Profiler = Ve;
O.StrictMode = Be;
O.Suspense = Ge;
O.SuspenseList = Ke;
O.isAsyncMode = function() {
  return !1;
};
O.isConcurrentMode = function() {
  return !1;
};
O.isContextConsumer = function(e) {
  return q(e) === Ue;
};
O.isContextProvider = function(e) {
  return q(e) === Xe;
};
O.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === Ct;
};
O.isForwardRef = function(e) {
  return q(e) === We;
};
O.isFragment = function(e) {
  return q(e) === Ne;
};
O.isLazy = function(e) {
  return q(e) === Ze;
};
O.isMemo = function(e) {
  return q(e) === qe;
};
O.isPortal = function(e) {
  return q(e) === _t;
};
O.isProfiler = function(e) {
  return q(e) === Ve;
};
O.isStrictMode = function(e) {
  return q(e) === Be;
};
O.isSuspense = function(e) {
  return q(e) === Ge;
};
O.isSuspenseList = function(e) {
  return q(e) === Ke;
};
O.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Ne || e === Ve || e === Be || e === Ge || e === Ke || e === Qn || typeof e == "object" && e !== null && (e.$$typeof === Ze || e.$$typeof === qe || e.$$typeof === Xe || e.$$typeof === Ue || e.$$typeof === We || e.$$typeof === br || e.getModuleId !== void 0);
};
O.typeOf = q;
vr.exports = O;
var at = vr.exports, Yn = Symbol.for("react.element"), Jn = Symbol.for("react.transitional.element"), eo = Symbol.for("react.fragment");
function to(e) {
  return (
    // Base object type
    e && N(e) === "object" && // React Element type
    (e.$$typeof === Yn || e.$$typeof === Jn) && // React Fragment type
    e.type === eo
  );
}
var ro = function(t, o) {
  typeof t == "function" ? t(o) : N(t) === "object" && t && "current" in t && (t.current = o);
}, no = function(t) {
  var o, r;
  if (!t)
    return !1;
  if (yr(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var n = at.isMemo(t) ? t.type.type : t.type;
  return !(typeof n == "function" && !((o = n.prototype) !== null && o !== void 0 && o.render) && n.$$typeof !== at.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== at.ForwardRef);
};
function yr(e) {
  return /* @__PURE__ */ Ur(e) && !to(e);
}
var oo = function(t) {
  if (t && yr(t)) {
    var o = t;
    return o.props.propertyIsEnumerable("ref") ? o.props.ref : o.ref;
  }
  return null;
};
function io(e, t) {
  if (N(e) != "object" || !e) return e;
  var o = e[Symbol.toPrimitive];
  if (o !== void 0) {
    var r = o.call(e, t || "default");
    if (N(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Sr(e) {
  var t = io(e, "string");
  return N(t) == "symbol" ? t : t + "";
}
function w(e, t, o) {
  return (t = Sr(t)) in e ? Object.defineProperty(e, t, {
    value: o,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = o, e;
}
function Ut(e, t) {
  var o = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(n) {
      return Object.getOwnPropertyDescriptor(e, n).enumerable;
    })), o.push.apply(o, r);
  }
  return o;
}
function x(e) {
  for (var t = 1; t < arguments.length; t++) {
    var o = arguments[t] != null ? arguments[t] : {};
    t % 2 ? Ut(Object(o), !0).forEach(function(r) {
      w(e, r, o[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(o)) : Ut(Object(o)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(o, r));
    });
  }
  return e;
}
const be = /* @__PURE__ */ a.createContext(null);
function Wt(e) {
  const {
    getDropContainer: t,
    className: o,
    prefixCls: r,
    children: n
  } = e, {
    disabled: i
  } = a.useContext(be), [s, l] = a.useState(), [u, c] = a.useState(null);
  if (a.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && l(d);
  }, [t]), a.useEffect(() => {
    if (s) {
      const d = () => {
        c(!0);
      }, m = (g) => {
        g.preventDefault();
      }, v = (g) => {
        g.relatedTarget || c(!1);
      }, h = (g) => {
        c(!1), g.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", m), document.addEventListener("dragleave", v), document.addEventListener("drop", h), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", m), document.removeEventListener("dragleave", v), document.removeEventListener("drop", h);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const p = `${r}-drop-area`;
  return /* @__PURE__ */ pt(/* @__PURE__ */ a.createElement("div", {
    className: K(p, o, {
      [`${p}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: u ? "block" : "none"
    }
  }, n), s);
}
function Gt(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function so(e) {
  return e && N(e) === "object" && Gt(e.nativeElement) ? e.nativeElement : Gt(e) ? e : null;
}
function ao(e) {
  var t = so(e);
  if (t)
    return t;
  if (e instanceof a.Component) {
    var o;
    return (o = Ot.findDOMNode) === null || o === void 0 ? void 0 : o.call(Ot, e);
  }
  return null;
}
function lo(e, t) {
  if (e == null) return {};
  var o = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.includes(r)) continue;
    o[r] = e[r];
  }
  return o;
}
function Kt(e, t) {
  if (e == null) return {};
  var o, r, n = lo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) o = i[r], t.includes(o) || {}.propertyIsEnumerable.call(e, o) && (n[o] = e[o]);
  }
  return n;
}
var co = /* @__PURE__ */ P.createContext({});
function pe(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function qt(e, t) {
  for (var o = 0; o < t.length; o++) {
    var r = t[o];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, Sr(r.key), r);
  }
}
function ge(e, t, o) {
  return t && qt(e.prototype, t), o && qt(e, o), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function mt(e, t) {
  return mt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(o, r) {
    return o.__proto__ = r, o;
  }, mt(e, t);
}
function Qe(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && mt(e, t);
}
function De(e) {
  return De = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, De(e);
}
function xr() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (xr = function() {
    return !!e;
  })();
}
function le(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function uo(e, t) {
  if (t && (N(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return le(e);
}
function Ye(e) {
  var t = xr();
  return function() {
    var o, r = De(e);
    if (t) {
      var n = De(this).constructor;
      o = Reflect.construct(r, arguments, n);
    } else o = r.apply(this, arguments);
    return uo(this, o);
  };
}
var fo = /* @__PURE__ */ function(e) {
  Qe(o, e);
  var t = Ye(o);
  function o() {
    return pe(this, o), t.apply(this, arguments);
  }
  return ge(o, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), o;
}(P.Component);
function po(e) {
  var t = P.useReducer(function(l) {
    return l + 1;
  }, 0), o = V(t, 2), r = o[1], n = P.useRef(e), i = de(function() {
    return n.current;
  }), s = de(function(l) {
    n.current = typeof l == "function" ? l(n.current) : l, r();
  });
  return [i, s];
}
var ne = "none", Le = "appear", Te = "enter", Re = "leave", Zt = "none", Q = "prepare", ue = "start", fe = "active", Lt = "end", wr = "prepared";
function Qt(e, t) {
  var o = {};
  return o[e.toLowerCase()] = t.toLowerCase(), o["Webkit".concat(e)] = "webkit".concat(t), o["Moz".concat(e)] = "moz".concat(t), o["ms".concat(e)] = "MS".concat(t), o["O".concat(e)] = "o".concat(t.toLowerCase()), o;
}
function go(e, t) {
  var o = {
    animationend: Qt("Animation", "AnimationEnd"),
    transitionend: Qt("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete o.animationend.animation, "TransitionEvent" in t || delete o.transitionend.transition), o;
}
var mo = go(He(), typeof window < "u" ? window : {}), Er = {};
if (He()) {
  var ho = document.createElement("div");
  Er = ho.style;
}
var Me = {};
function Cr(e) {
  if (Me[e])
    return Me[e];
  var t = mo[e];
  if (t)
    for (var o = Object.keys(t), r = o.length, n = 0; n < r; n += 1) {
      var i = o[n];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Er)
        return Me[e] = t[i], Me[e];
    }
  return "";
}
var _r = Cr("animationend"), Lr = Cr("transitionend"), Tr = !!(_r && Lr), Yt = _r || "animationend", Jt = Lr || "transitionend";
function er(e, t) {
  if (!e) return null;
  if (N(e) === "object") {
    var o = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[o];
  }
  return "".concat(e, "-").concat(t);
}
const vo = function(e) {
  var t = ae();
  function o(n) {
    n && (n.removeEventListener(Jt, e), n.removeEventListener(Yt, e));
  }
  function r(n) {
    t.current && t.current !== n && o(t.current), n && n !== t.current && (n.addEventListener(Jt, e), n.addEventListener(Yt, e), t.current = n);
  }
  return P.useEffect(function() {
    return function() {
      o(t.current);
    };
  }, []), [r, o];
};
var Rr = He() ? Wr : Ie, Mr = function(t) {
  return +setTimeout(t, 16);
}, Pr = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Mr = function(t) {
  return window.requestAnimationFrame(t);
}, Pr = function(t) {
  return window.cancelAnimationFrame(t);
});
var tr = 0, Tt = /* @__PURE__ */ new Map();
function Or(e) {
  Tt.delete(e);
}
var ht = function(t) {
  var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  tr += 1;
  var r = tr;
  function n(i) {
    if (i === 0)
      Or(r), t();
    else {
      var s = Mr(function() {
        n(i - 1);
      });
      Tt.set(r, s);
    }
  }
  return n(o), r;
};
ht.cancel = function(e) {
  var t = Tt.get(e);
  return Or(e), Pr(t);
};
const bo = function() {
  var e = P.useRef(null);
  function t() {
    ht.cancel(e.current);
  }
  function o(r) {
    var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = ht(function() {
      n <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : o(r, n - 1);
    });
    e.current = i;
  }
  return P.useEffect(function() {
    return function() {
      t();
    };
  }, []), [o, t];
};
var yo = [Q, ue, fe, Lt], So = [Q, wr], Ir = !1, xo = !0;
function Ar(e) {
  return e === fe || e === Lt;
}
const wo = function(e, t, o) {
  var r = ve(Zt), n = V(r, 2), i = n[0], s = n[1], l = bo(), u = V(l, 2), c = u[0], f = u[1];
  function p() {
    s(Q, !0);
  }
  var d = t ? So : yo;
  return Rr(function() {
    if (i !== Zt && i !== Lt) {
      var m = d.indexOf(i), v = d[m + 1], h = o(i);
      h === Ir ? s(v, !0) : v && c(function(g) {
        function I() {
          g.isCanceled() || s(v, !0);
        }
        h === !0 ? I() : Promise.resolve(h).then(I);
      });
    }
  }, [e, i]), P.useEffect(function() {
    return function() {
      f();
    };
  }, []), [p, i];
};
function Eo(e, t, o, r) {
  var n = r.motionEnter, i = n === void 0 ? !0 : n, s = r.motionAppear, l = s === void 0 ? !0 : s, u = r.motionLeave, c = u === void 0 ? !0 : u, f = r.motionDeadline, p = r.motionLeaveImmediately, d = r.onAppearPrepare, m = r.onEnterPrepare, v = r.onLeavePrepare, h = r.onAppearStart, g = r.onEnterStart, I = r.onLeaveStart, _ = r.onAppearActive, S = r.onEnterActive, b = r.onLeaveActive, E = r.onAppearEnd, M = r.onEnterEnd, y = r.onLeaveEnd, C = r.onVisibleChanged, $ = ve(), F = V($, 2), k = F[0], L = F[1], R = po(ne), A = V(R, 2), T = A[0], j = A[1], Z = ve(null), G = V(Z, 2), re = G[0], H = G[1], D = T(), U = ae(!1), Y = ae(null);
  function X() {
    return o();
  }
  var oe = ae(!1);
  function ye() {
    j(ne), H(null, !0);
  }
  var te = de(function(W) {
    var B = T();
    if (B !== ne) {
      var J = X();
      if (!(W && !W.deadline && W.target !== J)) {
        var Ce = oe.current, _e;
        B === Le && Ce ? _e = E == null ? void 0 : E(J, W) : B === Te && Ce ? _e = M == null ? void 0 : M(J, W) : B === Re && Ce && (_e = y == null ? void 0 : y(J, W)), Ce && _e !== !1 && ye();
      }
    }
  }), Je = vo(te), Se = V(Je, 1), xe = Se[0], we = function(B) {
    switch (B) {
      case Le:
        return w(w(w({}, Q, d), ue, h), fe, _);
      case Te:
        return w(w(w({}, Q, m), ue, g), fe, S);
      case Re:
        return w(w(w({}, Q, v), ue, I), fe, b);
      default:
        return {};
    }
  }, ie = P.useMemo(function() {
    return we(D);
  }, [D]), Ee = wo(D, !e, function(W) {
    if (W === Q) {
      var B = ie[Q];
      return B ? B(X()) : Ir;
    }
    if (se in ie) {
      var J;
      H(((J = ie[se]) === null || J === void 0 ? void 0 : J.call(ie, X(), null)) || null);
    }
    return se === fe && D !== ne && (xe(X()), f > 0 && (clearTimeout(Y.current), Y.current = setTimeout(function() {
      te({
        deadline: !0
      });
    }, f))), se === wr && ye(), xo;
  }), Mt = V(Ee, 2), Vr = Mt[0], se = Mt[1], Xr = Ar(se);
  oe.current = Xr;
  var Pt = ae(null);
  Rr(function() {
    if (!(U.current && Pt.current === t)) {
      L(t);
      var W = U.current;
      U.current = !0;
      var B;
      !W && t && l && (B = Le), W && t && i && (B = Te), (W && !t && c || !W && p && !t && c) && (B = Re);
      var J = we(B);
      B && (e || J[Q]) ? (j(B), Vr()) : j(ne), Pt.current = t;
    }
  }, [t]), Ie(function() {
    // Cancel appear
    (D === Le && !l || // Cancel enter
    D === Te && !i || // Cancel leave
    D === Re && !c) && j(ne);
  }, [l, i, c]), Ie(function() {
    return function() {
      U.current = !1, clearTimeout(Y.current);
    };
  }, []);
  var et = P.useRef(!1);
  Ie(function() {
    k && (et.current = !0), k !== void 0 && D === ne && ((et.current || k) && (C == null || C(k)), et.current = !0);
  }, [k, D]);
  var tt = re;
  return ie[Q] && se === ue && (tt = x({
    transition: "none"
  }, tt)), [D, se, tt, k ?? t];
}
function Co(e) {
  var t = e;
  N(e) === "object" && (t = e.transitionSupport);
  function o(n, i) {
    return !!(n.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ P.forwardRef(function(n, i) {
    var s = n.visible, l = s === void 0 ? !0 : s, u = n.removeOnLeave, c = u === void 0 ? !0 : u, f = n.forceRender, p = n.children, d = n.motionName, m = n.leavedClassName, v = n.eventProps, h = P.useContext(co), g = h.motion, I = o(n, g), _ = ae(), S = ae();
    function b() {
      try {
        return _.current instanceof HTMLElement ? _.current : ao(S.current);
      } catch {
        return null;
      }
    }
    var E = Eo(I, l, b, n), M = V(E, 4), y = M[0], C = M[1], $ = M[2], F = M[3], k = P.useRef(F);
    F && (k.current = !0);
    var L = P.useCallback(function(G) {
      _.current = G, ro(i, G);
    }, [i]), R, A = x(x({}, v), {}, {
      visible: l
    });
    if (!p)
      R = null;
    else if (y === ne)
      F ? R = p(x({}, A), L) : !c && k.current && m ? R = p(x(x({}, A), {}, {
        className: m
      }), L) : f || !c && !m ? R = p(x(x({}, A), {}, {
        style: {
          display: "none"
        }
      }), L) : R = null;
    else {
      var T;
      C === Q ? T = "prepare" : Ar(C) ? T = "active" : C === ue && (T = "start");
      var j = er(d, "".concat(y, "-").concat(T));
      R = p(x(x({}, A), {}, {
        className: K(er(d, y), w(w({}, j, j && T), d, typeof d == "string")),
        style: $
      }), L);
    }
    if (/* @__PURE__ */ P.isValidElement(R) && no(R)) {
      var Z = oo(R);
      Z || (R = /* @__PURE__ */ P.cloneElement(R, {
        ref: L
      }));
    }
    return /* @__PURE__ */ P.createElement(fo, {
      ref: S
    }, R);
  });
  return r.displayName = "CSSMotion", r;
}
const _o = Co(Tr);
var vt = "add", bt = "keep", yt = "remove", lt = "removed";
function Lo(e) {
  var t;
  return e && N(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, x(x({}, t), {}, {
    key: String(t.key)
  });
}
function St() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(Lo);
}
function To() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], o = [], r = 0, n = t.length, i = St(e), s = St(t);
  i.forEach(function(c) {
    for (var f = !1, p = r; p < n; p += 1) {
      var d = s[p];
      if (d.key === c.key) {
        r < p && (o = o.concat(s.slice(r, p).map(function(m) {
          return x(x({}, m), {}, {
            status: vt
          });
        })), r = p), o.push(x(x({}, d), {}, {
          status: bt
        })), r += 1, f = !0;
        break;
      }
    }
    f || o.push(x(x({}, c), {}, {
      status: yt
    }));
  }), r < n && (o = o.concat(s.slice(r).map(function(c) {
    return x(x({}, c), {}, {
      status: vt
    });
  })));
  var l = {};
  o.forEach(function(c) {
    var f = c.key;
    l[f] = (l[f] || 0) + 1;
  });
  var u = Object.keys(l).filter(function(c) {
    return l[c] > 1;
  });
  return u.forEach(function(c) {
    o = o.filter(function(f) {
      var p = f.key, d = f.status;
      return p !== c || d !== yt;
    }), o.forEach(function(f) {
      f.key === c && (f.status = bt);
    });
  }), o;
}
var Ro = ["component", "children", "onVisibleChanged", "onAllRemoved"], Mo = ["status"], Po = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function Oo(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : _o, o = /* @__PURE__ */ function(r) {
    Qe(i, r);
    var n = Ye(i);
    function i() {
      var s;
      pe(this, i);
      for (var l = arguments.length, u = new Array(l), c = 0; c < l; c++)
        u[c] = arguments[c];
      return s = n.call.apply(n, [this].concat(u)), w(le(s), "state", {
        keyEntities: []
      }), w(le(s), "removeKey", function(f) {
        s.setState(function(p) {
          var d = p.keyEntities.map(function(m) {
            return m.key !== f ? m : x(x({}, m), {}, {
              status: lt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var p = s.state.keyEntities, d = p.filter(function(m) {
            var v = m.status;
            return v !== lt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return ge(i, [{
      key: "render",
      value: function() {
        var l = this, u = this.state.keyEntities, c = this.props, f = c.component, p = c.children, d = c.onVisibleChanged;
        c.onAllRemoved;
        var m = Kt(c, Ro), v = f || P.Fragment, h = {};
        return Po.forEach(function(g) {
          h[g] = m[g], delete m[g];
        }), delete m.keys, /* @__PURE__ */ P.createElement(v, m, u.map(function(g, I) {
          var _ = g.status, S = Kt(g, Mo), b = _ === vt || _ === bt;
          return /* @__PURE__ */ P.createElement(t, he({}, h, {
            key: S.key,
            visible: b,
            eventProps: S,
            onVisibleChanged: function(M) {
              d == null || d(M, {
                key: S.key
              }), M || l.removeKey(S.key);
            }
          }), function(E, M) {
            return p(x(x({}, E), {}, {
              index: I
            }), M);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(l, u) {
        var c = l.keys, f = u.keyEntities, p = St(c), d = To(f, p);
        return {
          keyEntities: d.filter(function(m) {
            var v = f.find(function(h) {
              var g = h.key;
              return m.key === g;
            });
            return !(v && v.status === lt && m.status === yt);
          })
        };
      }
    }]), i;
  }(P.Component);
  return w(o, "defaultProps", {
    component: "div"
  }), o;
}
const Io = Oo(Tr);
function Ao(e, t) {
  const {
    children: o,
    upload: r,
    rootClassName: n
  } = e, i = a.useRef(null);
  return a.useImperativeHandle(t, () => i.current), /* @__PURE__ */ a.createElement(ur, he({}, r, {
    showUploadList: !1,
    rootClassName: n,
    ref: i
  }), o);
}
const $r = /* @__PURE__ */ a.forwardRef(Ao);
var Fr = /* @__PURE__ */ ge(function e() {
  pe(this, e);
}), kr = "CALC_UNIT", $o = new RegExp(kr, "g");
function ct(e) {
  return typeof e == "number" ? "".concat(e).concat(kr) : e;
}
var Fo = /* @__PURE__ */ function(e) {
  Qe(o, e);
  var t = Ye(o);
  function o(r, n) {
    var i;
    pe(this, o), i = t.call(this), w(le(i), "result", ""), w(le(i), "unitlessCssVar", void 0), w(le(i), "lowPriority", void 0);
    var s = N(r);
    return i.unitlessCssVar = n, r instanceof o ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = ct(r) : s === "string" && (i.result = r), i;
  }
  return ge(o, [{
    key: "add",
    value: function(n) {
      return n instanceof o ? this.result = "".concat(this.result, " + ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " + ").concat(ct(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof o ? this.result = "".concat(this.result, " - ").concat(n.getResult()) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " - ").concat(ct(n))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof o ? this.result = "".concat(this.result, " * ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " * ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(n) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), n instanceof o ? this.result = "".concat(this.result, " / ").concat(n.getResult(!0)) : (typeof n == "number" || typeof n == "string") && (this.result = "".concat(this.result, " / ").concat(n)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(n) {
      return this.lowPriority || n ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(n) {
      var i = this, s = n || {}, l = s.unit, u = !0;
      return typeof l == "boolean" ? u = l : Array.from(this.unitlessCssVar).some(function(c) {
        return i.result.includes(c);
      }) && (u = !1), this.result = this.result.replace($o, u ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), o;
}(Fr), ko = /* @__PURE__ */ function(e) {
  Qe(o, e);
  var t = Ye(o);
  function o(r) {
    var n;
    return pe(this, o), n = t.call(this), w(le(n), "result", 0), r instanceof o ? n.result = r.result : typeof r == "number" && (n.result = r), n;
  }
  return ge(o, [{
    key: "add",
    value: function(n) {
      return n instanceof o ? this.result += n.result : typeof n == "number" && (this.result += n), this;
    }
  }, {
    key: "sub",
    value: function(n) {
      return n instanceof o ? this.result -= n.result : typeof n == "number" && (this.result -= n), this;
    }
  }, {
    key: "mul",
    value: function(n) {
      return n instanceof o ? this.result *= n.result : typeof n == "number" && (this.result *= n), this;
    }
  }, {
    key: "div",
    value: function(n) {
      return n instanceof o ? this.result /= n.result : typeof n == "number" && (this.result /= n), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), o;
}(Fr), jo = function(t, o) {
  var r = t === "css" ? Fo : ko;
  return function(n) {
    return new r(n, o);
  };
}, rr = function(t, o) {
  return "".concat([o, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function nr(e, t, o, r) {
  var n = x({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(l) {
      var u = V(l, 2), c = u[0], f = u[1];
      if (n != null && n[c] || n != null && n[f]) {
        var p;
        (p = n[f]) !== null && p !== void 0 || (n[f] = n == null ? void 0 : n[c]);
      }
    });
  }
  var s = x(x({}, o), n);
  return Object.keys(s).forEach(function(l) {
    s[l] === t[l] && delete s[l];
  }), s;
}
var jr = typeof CSSINJS_STATISTIC < "u", xt = !0;
function Rt() {
  for (var e = arguments.length, t = new Array(e), o = 0; o < e; o++)
    t[o] = arguments[o];
  if (!jr)
    return Object.assign.apply(Object, [{}].concat(t));
  xt = !1;
  var r = {};
  return t.forEach(function(n) {
    if (N(n) === "object") {
      var i = Object.keys(n);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return n[s];
          }
        });
      });
    }
  }), xt = !0, r;
}
var or = {};
function Do() {
}
var zo = function(t) {
  var o, r = t, n = Do;
  return jr && typeof Proxy < "u" && (o = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, l) {
      if (xt) {
        var u;
        (u = o) === null || u === void 0 || u.add(l);
      }
      return s[l];
    }
  }), n = function(s, l) {
    var u;
    or[s] = {
      global: Array.from(o),
      component: x(x({}, (u = or[s]) === null || u === void 0 ? void 0 : u.component), l)
    };
  }), {
    token: r,
    keys: o,
    flush: n
  };
};
function ir(e, t, o) {
  if (typeof o == "function") {
    var r;
    return o(Rt(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return o ?? {};
}
function Ho(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var o = arguments.length, r = new Array(o), n = 0; n < o; n++)
        r[n] = arguments[n];
      return "max(".concat(r.map(function(i) {
        return It(i);
      }).join(","), ")");
    },
    min: function() {
      for (var o = arguments.length, r = new Array(o), n = 0; n < o; n++)
        r[n] = arguments[n];
      return "min(".concat(r.map(function(i) {
        return It(i);
      }).join(","), ")");
    }
  };
}
var No = 1e3 * 60 * 10, Bo = /* @__PURE__ */ function() {
  function e() {
    pe(this, e), w(this, "map", /* @__PURE__ */ new Map()), w(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), w(this, "nextID", 0), w(this, "lastAccessBeat", /* @__PURE__ */ new Map()), w(this, "accessBeat", 0);
  }
  return ge(e, [{
    key: "set",
    value: function(o, r) {
      this.clear();
      var n = this.getCompositeKey(o);
      this.map.set(n, r), this.lastAccessBeat.set(n, Date.now());
    }
  }, {
    key: "get",
    value: function(o) {
      var r = this.getCompositeKey(o), n = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, n;
    }
  }, {
    key: "getCompositeKey",
    value: function(o) {
      var r = this, n = o.map(function(i) {
        return i && N(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(N(i), "_").concat(i);
      });
      return n.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(o) {
      if (this.objectIDMap.has(o))
        return this.objectIDMap.get(o);
      var r = this.nextID;
      return this.objectIDMap.set(o, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var o = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(n, i) {
          r - n > No && (o.map.delete(i), o.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), sr = new Bo();
function Vo(e, t) {
  return a.useMemo(function() {
    var o = sr.get(t);
    if (o)
      return o;
    var r = e();
    return sr.set(t, r), r;
  }, t);
}
var Xo = function() {
  return {};
};
function Uo(e) {
  var t = e.useCSP, o = t === void 0 ? Xo : t, r = e.useToken, n = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, l = e.getCompUnitless;
  function u(d, m, v, h) {
    var g = Array.isArray(d) ? d[0] : d;
    function I(C) {
      return "".concat(String(g)).concat(C.slice(0, 1).toUpperCase()).concat(C.slice(1));
    }
    var _ = (h == null ? void 0 : h.unitless) || {}, S = typeof l == "function" ? l(d) : {}, b = x(x({}, S), {}, w({}, I("zIndexPopup"), !0));
    Object.keys(_).forEach(function(C) {
      b[I(C)] = _[C];
    });
    var E = x(x({}, h), {}, {
      unitless: b,
      prefixToken: I
    }), M = f(d, m, v, E), y = c(g, v, E);
    return function(C) {
      var $ = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, F = M(C, $), k = V(F, 2), L = k[1], R = y($), A = V(R, 2), T = A[0], j = A[1];
      return [T, L, j];
    };
  }
  function c(d, m, v) {
    var h = v.unitless, g = v.injectStyle, I = g === void 0 ? !0 : g, _ = v.prefixToken, S = v.ignore, b = function(y) {
      var C = y.rootCls, $ = y.cssVar, F = $ === void 0 ? {} : $, k = r(), L = k.realToken;
      return un({
        path: [d],
        prefix: F.prefix,
        key: F.key,
        unitless: h,
        ignore: S,
        token: L,
        scope: C
      }, function() {
        var R = ir(d, L, m), A = nr(d, L, R, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(R).forEach(function(T) {
          A[_(T)] = A[T], delete A[T];
        }), A;
      }), null;
    }, E = function(y) {
      var C = r(), $ = C.cssVar;
      return [function(F) {
        return I && $ ? /* @__PURE__ */ a.createElement(a.Fragment, null, /* @__PURE__ */ a.createElement(b, {
          rootCls: y,
          cssVar: $,
          component: d
        }), F) : F;
      }, $ == null ? void 0 : $.key];
    };
    return E;
  }
  function f(d, m, v) {
    var h = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = Array.isArray(d) ? d : [d, d], I = V(g, 1), _ = I[0], S = g.join("-"), b = e.layer || {
      name: "antd"
    };
    return function(E) {
      var M = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, y = r(), C = y.theme, $ = y.realToken, F = y.hashId, k = y.token, L = y.cssVar, R = n(), A = R.rootPrefixCls, T = R.iconPrefixCls, j = o(), Z = L ? "css" : "js", G = Vo(function() {
        var X = /* @__PURE__ */ new Set();
        return L && Object.keys(h.unitless || {}).forEach(function(oe) {
          X.add(ot(oe, L.prefix)), X.add(ot(oe, rr(_, L.prefix)));
        }), jo(Z, X);
      }, [Z, _, L == null ? void 0 : L.prefix]), re = Ho(Z), H = re.max, D = re.min, U = {
        theme: C,
        token: k,
        hashId: F,
        nonce: function() {
          return j.nonce;
        },
        clientOnly: h.clientOnly,
        layer: b,
        // antd is always at top of styles
        order: h.order || -999
      };
      typeof i == "function" && At(x(x({}, U), {}, {
        clientOnly: !1,
        path: ["Shared", A]
      }), function() {
        return i(k, {
          prefix: {
            rootPrefixCls: A,
            iconPrefixCls: T
          },
          csp: j
        });
      });
      var Y = At(x(x({}, U), {}, {
        path: [S, E, T]
      }), function() {
        if (h.injectStyle === !1)
          return [];
        var X = zo(k), oe = X.token, ye = X.flush, te = ir(_, $, v), Je = ".".concat(E), Se = nr(_, $, te, {
          deprecatedTokens: h.deprecatedTokens
        });
        L && te && N(te) === "object" && Object.keys(te).forEach(function(Ee) {
          te[Ee] = "var(".concat(ot(Ee, rr(_, L.prefix)), ")");
        });
        var xe = Rt(oe, {
          componentCls: Je,
          prefixCls: E,
          iconCls: ".".concat(T),
          antCls: ".".concat(A),
          calc: G,
          // @ts-ignore
          max: H,
          // @ts-ignore
          min: D
        }, L ? te : Se), we = m(xe, {
          hashId: F,
          prefixCls: E,
          rootPrefixCls: A,
          iconPrefixCls: T
        });
        ye(_, Se);
        var ie = typeof s == "function" ? s(xe, E, M, h.resetFont) : null;
        return [h.resetStyle === !1 ? null : ie, we];
      });
      return [Y, F];
    };
  }
  function p(d, m, v) {
    var h = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, g = f(d, m, v, x({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, h)), I = function(S) {
      var b = S.prefixCls, E = S.rootCls, M = E === void 0 ? b : E;
      return g(b, M), null;
    };
    return I;
  }
  return {
    genStyleHooks: u,
    genSubStyleComponent: p,
    genComponentStyleHook: f
  };
}
const z = Math.round;
function ut(e, t) {
  const o = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = o.map((n) => parseFloat(n));
  for (let n = 0; n < 3; n += 1)
    r[n] = t(r[n] || 0, o[n] || "", n);
  return o[3] ? r[3] = o[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const ar = (e, t, o) => o === 0 ? e : e / 100;
function me(e, t) {
  const o = t || 255;
  return e > o ? o : e < 0 ? 0 : e;
}
class ee {
  constructor(t) {
    w(this, "isValid", !0), w(this, "r", 0), w(this, "g", 0), w(this, "b", 0), w(this, "a", 1), w(this, "_h", void 0), w(this, "_s", void 0), w(this, "_l", void 0), w(this, "_v", void 0), w(this, "_max", void 0), w(this, "_min", void 0), w(this, "_brightness", void 0);
    function o(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let n = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : n("rgb") ? this.fromRgbString(r) : n("hsl") ? this.fromHslString(r) : (n("hsv") || n("hsb")) && this.fromHsvString(r);
    } else if (t instanceof ee)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (o("rgb"))
      this.r = me(t.r), this.g = me(t.g), this.b = me(t.b), this.a = typeof t.a == "number" ? me(t.a, 1) : 1;
    else if (o("hsl"))
      this.fromHsl(t);
    else if (o("hsv"))
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
    const o = this.toHsv();
    return o.h = t, this._c(o);
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
    const o = t(this.r), r = t(this.g), n = t(this.b);
    return 0.2126 * o + 0.7152 * r + 0.0722 * n;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = z(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const o = this.getHue(), r = this.getSaturation();
    let n = this.getLightness() - t / 100;
    return n < 0 && (n = 0), this._c({
      h: o,
      s: r,
      l: n,
      a: this.a
    });
  }
  lighten(t = 10) {
    const o = this.getHue(), r = this.getSaturation();
    let n = this.getLightness() + t / 100;
    return n > 1 && (n = 1), this._c({
      h: o,
      s: r,
      l: n,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, o = 50) {
    const r = this._c(t), n = o / 100, i = (l) => (r[l] - this[l]) * n + this[l], s = {
      r: z(i("r")),
      g: z(i("g")),
      b: z(i("b")),
      a: z(i("a") * 100) / 100
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
    const o = this._c(t), r = this.a + o.a * (1 - this.a), n = (i) => z((this[i] * this.a + o[i] * o.a * (1 - this.a)) / r);
    return this._c({
      r: n("r"),
      g: n("g"),
      b: n("b"),
      a: r
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
    const o = (this.r || 0).toString(16);
    t += o.length === 2 ? o : "0" + o;
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const n = (this.b || 0).toString(16);
    if (t += n.length === 2 ? n : "0" + n, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = z(this.a * 255).toString(16);
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
    const t = this.getHue(), o = z(this.getSaturation() * 100), r = z(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${o}%,${r}%,${this.a})` : `hsl(${t},${o}%,${r}%)`;
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
  _sc(t, o, r) {
    const n = this.clone();
    return n[t] = me(o, r), n;
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
    const o = t.replace("#", "");
    function r(n, i) {
      return parseInt(o[n] + o[i || n], 16);
    }
    o.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = o[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = o[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: o,
    l: r,
    a: n
  }) {
    if (this._h = t % 360, this._s = o, this._l = r, this.a = typeof n == "number" ? n : 1, o <= 0) {
      const d = z(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, l = 0;
    const u = t / 60, c = (1 - Math.abs(2 * r - 1)) * o, f = c * (1 - Math.abs(u % 2 - 1));
    u >= 0 && u < 1 ? (i = c, s = f) : u >= 1 && u < 2 ? (i = f, s = c) : u >= 2 && u < 3 ? (s = c, l = f) : u >= 3 && u < 4 ? (s = f, l = c) : u >= 4 && u < 5 ? (i = f, l = c) : u >= 5 && u < 6 && (i = c, l = f);
    const p = r - c / 2;
    this.r = z((i + p) * 255), this.g = z((s + p) * 255), this.b = z((l + p) * 255);
  }
  fromHsv({
    h: t,
    s: o,
    v: r,
    a: n
  }) {
    this._h = t % 360, this._s = o, this._v = r, this.a = typeof n == "number" ? n : 1;
    const i = z(r * 255);
    if (this.r = i, this.g = i, this.b = i, o <= 0)
      return;
    const s = t / 60, l = Math.floor(s), u = s - l, c = z(r * (1 - o) * 255), f = z(r * (1 - o * u) * 255), p = z(r * (1 - o * (1 - u)) * 255);
    switch (l) {
      case 0:
        this.g = p, this.b = c;
        break;
      case 1:
        this.r = f, this.b = c;
        break;
      case 2:
        this.r = c, this.b = p;
        break;
      case 3:
        this.r = c, this.g = f;
        break;
      case 4:
        this.r = p, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = f;
        break;
    }
  }
  fromHsvString(t) {
    const o = ut(t, ar);
    this.fromHsv({
      h: o[0],
      s: o[1],
      v: o[2],
      a: o[3]
    });
  }
  fromHslString(t) {
    const o = ut(t, ar);
    this.fromHsl({
      h: o[0],
      s: o[1],
      l: o[2],
      a: o[3]
    });
  }
  fromRgbString(t) {
    const o = ut(t, (r, n) => (
      // Convert percentage to number. e.g. 50% -> 128
      n.includes("%") ? z(r / 100 * 255) : r
    ));
    this.r = o[0], this.g = o[1], this.b = o[2], this.a = o[3];
  }
}
const Wo = {
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
}, Go = Object.assign(Object.assign({}, Wo), {
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
function ft(e) {
  return e >= 0 && e <= 255;
}
function Pe(e, t) {
  const {
    r: o,
    g: r,
    b: n,
    a: i
  } = new ee(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: l,
    b: u
  } = new ee(t).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const f = Math.round((o - s * (1 - c)) / c), p = Math.round((r - l * (1 - c)) / c), d = Math.round((n - u * (1 - c)) / c);
    if (ft(f) && ft(p) && ft(d))
      return new ee({
        r: f,
        g: p,
        b: d,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new ee({
    r: o,
    g: r,
    b: n,
    a: 1
  }).toRgbString();
}
var Ko = function(e, t) {
  var o = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (o[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var n = 0, r = Object.getOwnPropertySymbols(e); n < r.length; n++)
    t.indexOf(r[n]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[n]) && (o[r[n]] = e[r[n]]);
  return o;
};
function qo(e) {
  const {
    override: t
  } = e, o = Ko(e, ["override"]), r = Object.assign({}, t);
  Object.keys(Go).forEach((d) => {
    delete r[d];
  });
  const n = Object.assign(Object.assign({}, o), r), i = 480, s = 576, l = 768, u = 992, c = 1200, f = 1600;
  if (n.motion === !1) {
    const d = "0s";
    n.motionDurationFast = d, n.motionDurationMid = d, n.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, n), {
    // ============== Background ============== //
    colorFillContent: n.colorFillSecondary,
    colorFillContentHover: n.colorFill,
    colorFillAlter: n.colorFillQuaternary,
    colorBgContainerDisabled: n.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: n.colorBgContainer,
    colorSplit: Pe(n.colorBorderSecondary, n.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: n.colorTextQuaternary,
    colorTextDisabled: n.colorTextQuaternary,
    colorTextHeading: n.colorText,
    colorTextLabel: n.colorTextSecondary,
    colorTextDescription: n.colorTextTertiary,
    colorTextLightSolid: n.colorWhite,
    colorHighlight: n.colorError,
    colorBgTextHover: n.colorFillSecondary,
    colorBgTextActive: n.colorFill,
    colorIcon: n.colorTextTertiary,
    colorIconHover: n.colorText,
    colorErrorOutline: Pe(n.colorErrorBg, n.colorBgContainer),
    colorWarningOutline: Pe(n.colorWarningBg, n.colorBgContainer),
    // Font
    fontSizeIcon: n.fontSizeSM,
    // Line
    lineWidthFocus: n.lineWidth * 3,
    // Control
    lineWidth: n.lineWidth,
    controlOutlineWidth: n.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: n.controlHeight / 2,
    controlItemBgHover: n.colorFillTertiary,
    controlItemBgActive: n.colorPrimaryBg,
    controlItemBgActiveHover: n.colorPrimaryBgHover,
    controlItemBgActiveDisabled: n.colorFill,
    controlTmpOutline: n.colorFillQuaternary,
    controlOutline: Pe(n.colorPrimaryBg, n.colorBgContainer),
    lineType: n.lineType,
    borderRadius: n.borderRadius,
    borderRadiusXS: n.borderRadiusXS,
    borderRadiusSM: n.borderRadiusSM,
    borderRadiusLG: n.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: n.sizeXXS,
    paddingXS: n.sizeXS,
    paddingSM: n.sizeSM,
    padding: n.size,
    paddingMD: n.sizeMD,
    paddingLG: n.sizeLG,
    paddingXL: n.sizeXL,
    paddingContentHorizontalLG: n.sizeLG,
    paddingContentVerticalLG: n.sizeMS,
    paddingContentHorizontal: n.sizeMS,
    paddingContentVertical: n.sizeSM,
    paddingContentHorizontalSM: n.size,
    paddingContentVerticalSM: n.sizeXS,
    marginXXS: n.sizeXXS,
    marginXS: n.sizeXS,
    marginSM: n.sizeSM,
    margin: n.size,
    marginMD: n.sizeMD,
    marginLG: n.sizeLG,
    marginXL: n.sizeXL,
    marginXXL: n.sizeXXL,
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
    screenSMMax: l - 1,
    screenMD: l,
    screenMDMin: l,
    screenMDMax: u - 1,
    screenLG: u,
    screenLGMin: u,
    screenLGMax: c - 1,
    screenXL: c,
    screenXLMin: c,
    screenXLMax: f - 1,
    screenXXL: f,
    screenXXLMin: f,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ee("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ee("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ee("rgba(0, 0, 0, 0.09)").toRgbString()}
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
  }), r);
}
const Zo = {
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
}, Qo = {
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
}, Yo = fn(ke.defaultAlgorithm), Jo = {
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
}, Dr = (e, t, o) => {
  const r = o.getDerivativeToken(e), {
    override: n,
    ...i
  } = t;
  let s = {
    ...r,
    override: n
  };
  return s = qo(s), i && Object.entries(i).forEach(([l, u]) => {
    const {
      theme: c,
      ...f
    } = u;
    let p = f;
    c && (p = Dr({
      ...s,
      ...f
    }, {
      override: f
    }, c)), s[l] = p;
  }), s;
};
function ei() {
  const {
    token: e,
    hashed: t,
    theme: o = Yo,
    override: r,
    cssVar: n
  } = a.useContext(ke._internalContext), [i, s, l] = dn(o, [ke.defaultSeed, e], {
    salt: `${Hn}-${t || ""}`,
    override: r,
    getComputedToken: Dr,
    cssVar: n && {
      prefix: n.prefix,
      key: n.key,
      unitless: Zo,
      ignore: Qo,
      preserve: Jo
    }
  });
  return [o, l, t ? s : "", i, n];
}
const {
  genStyleHooks: ti,
  genComponentStyleHook: yi,
  genSubStyleComponent: Si
} = Uo({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = je();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, o, r, n] = ei();
    return {
      theme: e,
      realToken: t,
      hashId: o,
      token: r,
      cssVar: n
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = je();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), ri = (e) => {
  const {
    componentCls: t,
    calc: o
  } = e, r = `${t}-list-card`, n = o(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [r]: {
      borderRadius: e.borderRadius,
      position: "relative",
      background: e.colorFillContent,
      borderWidth: e.lineWidth,
      borderStyle: "solid",
      borderColor: "transparent",
      flex: "none",
      // =============================== Desc ================================
      [`${r}-name,${r}-desc`]: {
        display: "flex",
        flexWrap: "nowrap",
        maxWidth: "100%"
      },
      [`${r}-ellipsis-prefix`]: {
        flex: "0 1 auto",
        minWidth: 0,
        overflow: "hidden",
        textOverflow: "ellipsis",
        whiteSpace: "nowrap"
      },
      [`${r}-ellipsis-suffix`]: {
        flex: "none"
      },
      // ============================= Overview ==============================
      "&-type-overview": {
        padding: o(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: o(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: o(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: o(e.paddingXXS).mul(1.5).equal(),
          flex: "none"
        },
        // Content
        [`${r}-content`]: {
          flex: "auto",
          minWidth: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "stretch"
        },
        [`${r}-desc`]: {
          color: e.colorTextTertiary
        }
      },
      // ============================== Preview ==============================
      "&-type-preview": {
        width: n,
        height: n,
        lineHeight: 1,
        [`&:not(${r}-status-error)`]: {
          border: 0
        },
        // Img
        img: {
          width: "100%",
          height: "100%",
          verticalAlign: "top",
          objectFit: "cover",
          borderRadius: "inherit"
        },
        // Mask
        [`${r}-img-mask`]: {
          position: "absolute",
          inset: 0,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: `rgba(0, 0, 0, ${e.opacityLoading})`,
          borderRadius: "inherit"
        },
        // Error
        [`&${r}-status-error`]: {
          [`img, ${r}-img-mask`]: {
            borderRadius: o(e.borderRadius).sub(e.lineWidth).equal()
          },
          [`${r}-desc`]: {
            paddingInline: e.paddingXXS
          }
        },
        // Progress
        [`${r}-progress`]: {}
      },
      // ============================ Remove Icon ============================
      [`${r}-remove`]: {
        position: "absolute",
        top: 0,
        insetInlineEnd: 0,
        border: 0,
        padding: e.paddingXXS,
        background: "transparent",
        lineHeight: 1,
        transform: "translate(50%, -50%)",
        fontSize: e.fontSize,
        cursor: "pointer",
        opacity: e.opacityLoading,
        display: "none",
        "&:dir(rtl)": {
          transform: "translate(-50%, -50%)"
        },
        "&:hover": {
          opacity: 1
        },
        "&:active": {
          opacity: e.opacityLoading
        }
      },
      [`&:hover ${r}-remove`]: {
        display: "block"
      },
      // ============================== Status ===============================
      "&-status-error": {
        borderColor: e.colorError,
        [`${r}-desc`]: {
          color: e.colorError
        }
      },
      // ============================== Motion ===============================
      "&-motion": {
        transition: ["opacity", "width", "margin", "padding"].map((i) => `${i} ${e.motionDurationSlow}`).join(","),
        "&-appear-start": {
          width: 0,
          transition: "none"
        },
        "&-leave-active": {
          opacity: 0,
          width: 0,
          paddingInline: 0,
          borderInlineWidth: 0,
          marginInlineEnd: o(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, wt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, ni = (e) => {
  const {
    componentCls: t,
    calc: o,
    antCls: r
  } = e, n = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [n]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...wt,
      "&-on-body": {
        position: "fixed",
        inset: 0
      },
      "&-hide-placement": {
        [`${i}-inner`]: {
          display: "none"
        }
      },
      [i]: {
        padding: 0
      }
    },
    "&": {
      // ============================= Placeholder =============================
      [i]: {
        height: "100%",
        borderRadius: e.borderRadius,
        borderWidth: e.lineWidthBold,
        borderStyle: "dashed",
        borderColor: "transparent",
        padding: e.padding,
        position: "relative",
        backdropFilter: "blur(10px)",
        background: e.colorBgPlaceholderHover,
        ...wt,
        [`${r}-upload-wrapper ${r}-upload${r}-upload-btn`]: {
          padding: 0
        },
        [`&${i}-drag-in`]: {
          borderColor: e.colorPrimaryHover
        },
        [`&${i}-disabled`]: {
          opacity: 0.25,
          pointerEvents: "none"
        },
        [`${i}-inner`]: {
          gap: o(e.paddingXXS).div(2).equal()
        },
        [`${i}-icon`]: {
          fontSize: e.fontSizeHeading2,
          lineHeight: 1
        },
        [`${i}-title${i}-title`]: {
          margin: 0,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight
        },
        [`${i}-description`]: {}
      }
    }
  };
}, oi = (e) => {
  const {
    componentCls: t,
    calc: o
  } = e, r = `${t}-list`, n = o(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...wt,
      // =============================== File List ===============================
      [r]: {
        display: "flex",
        flexWrap: "wrap",
        gap: e.paddingSM,
        fontSize: e.fontSize,
        lineHeight: e.lineHeight,
        color: e.colorText,
        paddingBlock: e.paddingSM,
        paddingInline: e.padding,
        width: "100%",
        background: e.colorBgContainer,
        // Hide scrollbar
        scrollbarWidth: "none",
        "-ms-overflow-style": "none",
        "&::-webkit-scrollbar": {
          display: "none"
        },
        // Scroll
        "&-overflow-scrollX, &-overflow-scrollY": {
          "&:before, &:after": {
            content: '""',
            position: "absolute",
            opacity: 0,
            transition: `opacity ${e.motionDurationSlow}`,
            zIndex: 1
          }
        },
        "&-overflow-ping-start:before": {
          opacity: 1
        },
        "&-overflow-ping-end:after": {
          opacity: 1
        },
        "&-overflow-scrollX": {
          overflowX: "auto",
          overflowY: "hidden",
          flexWrap: "nowrap",
          "&:before, &:after": {
            insetBlock: 0,
            width: 8
          },
          "&:before": {
            insetInlineStart: 0,
            background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetInlineEnd: 0,
            background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:dir(rtl)": {
            "&:before": {
              background: "linear-gradient(to left, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            },
            "&:after": {
              background: "linear-gradient(to right, rgba(0,0,0,0.06), rgba(0,0,0,0));"
            }
          }
        },
        "&-overflow-scrollY": {
          overflowX: "hidden",
          overflowY: "auto",
          maxHeight: o(n).mul(3).equal(),
          "&:before, &:after": {
            insetInline: 0,
            height: 8
          },
          "&:before": {
            insetBlockStart: 0,
            background: "linear-gradient(to bottom, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          },
          "&:after": {
            insetBlockEnd: 0,
            background: "linear-gradient(to top, rgba(0,0,0,0.06), rgba(0,0,0,0));"
          }
        },
        // ======================================================================
        // ==                              Upload                              ==
        // ======================================================================
        "&-upload-btn": {
          width: n,
          height: n,
          fontSize: e.fontSizeHeading2,
          color: "#999"
        },
        // ======================================================================
        // ==                             PrevNext                             ==
        // ======================================================================
        "&-prev-btn, &-next-btn": {
          position: "absolute",
          top: "50%",
          transform: "translateY(-50%)",
          boxShadow: e.boxShadowTertiary,
          opacity: 0,
          pointerEvents: "none"
        },
        "&-prev-btn": {
          left: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&-next-btn": {
          right: {
            _skip_check_: !0,
            value: e.padding
          }
        },
        "&:dir(ltr)": {
          [`&${r}-overflow-ping-start ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-end ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        },
        "&:dir(rtl)": {
          [`&${r}-overflow-ping-end ${r}-prev-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          },
          [`&${r}-overflow-ping-start ${r}-next-btn`]: {
            opacity: 1,
            pointerEvents: "auto"
          }
        }
      }
    }
  };
}, ii = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new ee(t).setA(0.85).toRgbString()
  };
}, zr = ti("Attachments", (e) => {
  const t = Rt(e, {});
  return [ni(t), oi(t), ri(t)];
}, ii), si = (e) => e.indexOf("image/") === 0, Oe = 200;
function ai(e) {
  return new Promise((t) => {
    if (!e || !e.type || !si(e.type)) {
      t("");
      return;
    }
    const o = new Image();
    if (o.onload = () => {
      const {
        width: r,
        height: n
      } = o, i = r / n, s = i > 1 ? Oe : Oe * i, l = i > 1 ? Oe / i : Oe, u = document.createElement("canvas");
      u.width = s, u.height = l, u.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${l}px; z-index: 9999; display: none;`, document.body.appendChild(u), u.getContext("2d").drawImage(o, 0, 0, s, l);
      const f = u.toDataURL();
      document.body.removeChild(u), window.URL.revokeObjectURL(o.src), t(f);
    }, o.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (o.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      o.src = window.URL.createObjectURL(e);
  });
}
function li() {
  return /* @__PURE__ */ a.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ a.createElement("title", null, "audio"), /* @__PURE__ */ a.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ a.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function ci(e) {
  const {
    percent: t
  } = e, {
    token: o
  } = ke.useToken();
  return /* @__PURE__ */ a.createElement(qr, {
    type: "circle",
    percent: t,
    size: o.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ a.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function ui() {
  return /* @__PURE__ */ a.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ a.createElement("title", null, "video"), /* @__PURE__ */ a.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ a.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const dt = " ", Et = "#8c8c8c", Hr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], fi = [{
  icon: /* @__PURE__ */ a.createElement(Jr, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ a.createElement(en, null),
  color: Et,
  ext: Hr
}, {
  icon: /* @__PURE__ */ a.createElement(tn, null),
  color: Et,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ a.createElement(rn, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ a.createElement(nn, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ a.createElement(on, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ a.createElement(sn, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ a.createElement(ui, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ a.createElement(li, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function lr(e, t) {
  return t.some((o) => e.toLowerCase() === `.${o}`);
}
function di(e) {
  let t = e;
  const o = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < o.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${o[r]}`;
}
function pi(e, t) {
  const {
    prefixCls: o,
    item: r,
    onRemove: n,
    className: i,
    style: s
  } = e, l = a.useContext(be), {
    disabled: u
  } = l || {}, {
    name: c,
    size: f,
    percent: p,
    status: d = "done",
    description: m
  } = r, {
    getPrefixCls: v
  } = je(), h = v("attachment", o), g = `${h}-list-card`, [I, _, S] = zr(h), [b, E] = a.useMemo(() => {
    const T = c || "", j = T.match(/^(.*)\.[^.]+$/);
    return j ? [j[1], T.slice(j[1].length)] : [T, ""];
  }, [c]), M = a.useMemo(() => lr(E, Hr), [E]), y = a.useMemo(() => m || (d === "uploading" ? `${p || 0}%` : d === "error" ? r.response || dt : f ? di(f) : dt), [d, p]), [C, $] = a.useMemo(() => {
    for (const {
      ext: T,
      icon: j,
      color: Z
    } of fi)
      if (lr(E, T))
        return [j, Z];
    return [/* @__PURE__ */ a.createElement(Qr, {
      key: "defaultIcon"
    }), Et];
  }, [E]), [F, k] = a.useState();
  a.useEffect(() => {
    if (r.originFileObj) {
      let T = !0;
      return ai(r.originFileObj).then((j) => {
        T && k(j);
      }), () => {
        T = !1;
      };
    }
    k(void 0);
  }, [r.originFileObj]);
  let L = null;
  const R = r.thumbUrl || r.url || F, A = M && (r.originFileObj || R);
  return A ? L = /* @__PURE__ */ a.createElement(a.Fragment, null, /* @__PURE__ */ a.createElement("img", {
    alt: "preview",
    src: R
  }), d !== "done" && /* @__PURE__ */ a.createElement("div", {
    className: `${g}-img-mask`
  }, d === "uploading" && p !== void 0 && /* @__PURE__ */ a.createElement(ci, {
    percent: p,
    prefixCls: g
  }), d === "error" && /* @__PURE__ */ a.createElement("div", {
    className: `${g}-desc`
  }, /* @__PURE__ */ a.createElement("div", {
    className: `${g}-ellipsis-prefix`
  }, y)))) : L = /* @__PURE__ */ a.createElement(a.Fragment, null, /* @__PURE__ */ a.createElement("div", {
    className: `${g}-icon`,
    style: {
      color: $
    }
  }, C), /* @__PURE__ */ a.createElement("div", {
    className: `${g}-content`
  }, /* @__PURE__ */ a.createElement("div", {
    className: `${g}-name`
  }, /* @__PURE__ */ a.createElement("div", {
    className: `${g}-ellipsis-prefix`
  }, b ?? dt), /* @__PURE__ */ a.createElement("div", {
    className: `${g}-ellipsis-suffix`
  }, E)), /* @__PURE__ */ a.createElement("div", {
    className: `${g}-desc`
  }, /* @__PURE__ */ a.createElement("div", {
    className: `${g}-ellipsis-prefix`
  }, y)))), I(/* @__PURE__ */ a.createElement("div", {
    className: K(g, {
      [`${g}-status-${d}`]: d,
      [`${g}-type-preview`]: A,
      [`${g}-type-overview`]: !A
    }, i, _, S),
    style: s,
    ref: t
  }, L, !u && n && /* @__PURE__ */ a.createElement("button", {
    type: "button",
    className: `${g}-remove`,
    onClick: () => {
      n(r);
    }
  }, /* @__PURE__ */ a.createElement(Yr, null))));
}
const Nr = /* @__PURE__ */ a.forwardRef(pi), cr = 1;
function gi(e) {
  const {
    prefixCls: t,
    items: o,
    onRemove: r,
    overflow: n,
    upload: i,
    listClassName: s,
    listStyle: l,
    itemClassName: u,
    itemStyle: c
  } = e, f = `${t}-list`, p = a.useRef(null), [d, m] = a.useState(!1), {
    disabled: v
  } = a.useContext(be);
  a.useEffect(() => (m(!0), () => {
    m(!1);
  }), []);
  const [h, g] = a.useState(!1), [I, _] = a.useState(!1), S = () => {
    const y = p.current;
    y && (n === "scrollX" ? (g(Math.abs(y.scrollLeft) >= cr), _(y.scrollWidth - y.clientWidth - Math.abs(y.scrollLeft) >= cr)) : n === "scrollY" && (g(y.scrollTop !== 0), _(y.scrollHeight - y.clientHeight !== y.scrollTop)));
  };
  a.useEffect(() => {
    S();
  }, [n]);
  const b = (y) => {
    const C = p.current;
    C && C.scrollTo({
      left: C.scrollLeft + y * C.clientWidth,
      behavior: "smooth"
    });
  }, E = () => {
    b(-1);
  }, M = () => {
    b(1);
  };
  return /* @__PURE__ */ a.createElement("div", {
    className: K(f, {
      [`${f}-overflow-${e.overflow}`]: n,
      [`${f}-overflow-ping-start`]: h,
      [`${f}-overflow-ping-end`]: I
    }, s),
    ref: p,
    onScroll: S,
    style: l
  }, /* @__PURE__ */ a.createElement(Io, {
    keys: o.map((y) => ({
      key: y.uid,
      item: y
    })),
    motionName: `${f}-card-motion`,
    component: !1,
    motionAppear: d,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: y,
    item: C,
    className: $,
    style: F
  }) => /* @__PURE__ */ a.createElement(Nr, {
    key: y,
    prefixCls: t,
    item: C,
    onRemove: r,
    className: K($, u),
    style: {
      ...F,
      ...c
    }
  })), !v && /* @__PURE__ */ a.createElement($r, {
    upload: i
  }, /* @__PURE__ */ a.createElement(rt, {
    className: `${f}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ a.createElement(an, {
    className: `${f}-upload-btn-icon`
  }))), n === "scrollX" && /* @__PURE__ */ a.createElement(a.Fragment, null, /* @__PURE__ */ a.createElement(rt, {
    size: "small",
    shape: "circle",
    className: `${f}-prev-btn`,
    icon: /* @__PURE__ */ a.createElement(ln, null),
    onClick: E
  }), /* @__PURE__ */ a.createElement(rt, {
    size: "small",
    shape: "circle",
    className: `${f}-next-btn`,
    icon: /* @__PURE__ */ a.createElement(cn, null),
    onClick: M
  })));
}
function mi(e, t) {
  const {
    prefixCls: o,
    placeholder: r = {},
    upload: n,
    className: i,
    style: s
  } = e, l = `${o}-placeholder`, u = r || {}, {
    disabled: c
  } = a.useContext(be), [f, p] = a.useState(!1), d = () => {
    p(!0);
  }, m = (g) => {
    g.currentTarget.contains(g.relatedTarget) || p(!1);
  }, v = () => {
    p(!1);
  }, h = /* @__PURE__ */ a.isValidElement(r) ? r : /* @__PURE__ */ a.createElement(Zr, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${l}-inner`
  }, /* @__PURE__ */ a.createElement(nt.Text, {
    className: `${l}-icon`
  }, u.icon), /* @__PURE__ */ a.createElement(nt.Title, {
    className: `${l}-title`,
    level: 5
  }, u.title), /* @__PURE__ */ a.createElement(nt.Text, {
    className: `${l}-description`,
    type: "secondary"
  }, u.description));
  return /* @__PURE__ */ a.createElement("div", {
    className: K(l, {
      [`${l}-drag-in`]: f,
      [`${l}-disabled`]: c
    }, i),
    onDragEnter: d,
    onDragLeave: m,
    onDrop: v,
    "aria-hidden": c,
    style: s
  }, /* @__PURE__ */ a.createElement(ur.Dragger, he({
    showUploadList: !1
  }, n, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), h));
}
const hi = /* @__PURE__ */ a.forwardRef(mi);
function vi(e, t) {
  const {
    prefixCls: o,
    rootClassName: r,
    rootStyle: n,
    className: i,
    style: s,
    items: l,
    children: u,
    getDropContainer: c,
    placeholder: f,
    onChange: p,
    overflow: d,
    disabled: m,
    classNames: v = {},
    styles: h = {},
    ...g
  } = e, {
    getPrefixCls: I,
    direction: _
  } = je(), S = I("attachment", o), b = Vn("attachments"), {
    classNames: E,
    styles: M
  } = b, y = a.useRef(null), C = a.useRef(null);
  a.useImperativeHandle(t, () => ({
    nativeElement: y.current,
    upload: (H) => {
      var U, Y;
      const D = (Y = (U = C.current) == null ? void 0 : U.nativeElement) == null ? void 0 : Y.querySelector('input[type="file"]');
      if (D) {
        const X = new DataTransfer();
        X.items.add(H), D.files = X.files, D.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [$, F, k] = zr(S), L = K(F, k), [R, A] = qn([], {
    value: l
  }), T = de((H) => {
    A(H.fileList), p == null || p(H);
  }), j = {
    ...g,
    fileList: R,
    onChange: T
  }, Z = (H) => {
    const D = R.filter((U) => U.uid !== H.uid);
    T({
      file: H,
      fileList: D
    });
  };
  let G;
  const re = (H, D, U) => {
    const Y = typeof f == "function" ? f(H) : f;
    return /* @__PURE__ */ a.createElement(hi, {
      placeholder: Y,
      upload: j,
      prefixCls: S,
      className: K(E.placeholder, v.placeholder),
      style: {
        ...M.placeholder,
        ...h.placeholder,
        ...D == null ? void 0 : D.style
      },
      ref: U
    });
  };
  if (u)
    G = /* @__PURE__ */ a.createElement(a.Fragment, null, /* @__PURE__ */ a.createElement($r, {
      upload: j,
      rootClassName: r,
      ref: C
    }, u), /* @__PURE__ */ a.createElement(Wt, {
      getDropContainer: c,
      prefixCls: S,
      className: K(L, r)
    }, re("drop")));
  else {
    const H = R.length > 0;
    G = /* @__PURE__ */ a.createElement("div", {
      className: K(S, L, {
        [`${S}-rtl`]: _ === "rtl"
      }, i, r),
      style: {
        ...n,
        ...s
      },
      dir: _ || "ltr",
      ref: y
    }, /* @__PURE__ */ a.createElement(gi, {
      prefixCls: S,
      items: R,
      onRemove: Z,
      overflow: d,
      upload: j,
      listClassName: K(E.list, v.list),
      listStyle: {
        ...M.list,
        ...h.list,
        ...!H && {
          display: "none"
        }
      },
      itemClassName: K(E.item, v.item),
      itemStyle: {
        ...M.item,
        ...h.item
      }
    }), re("inline", H ? {
      style: {
        display: "none"
      }
    } : {}, C), /* @__PURE__ */ a.createElement(Wt, {
      getDropContainer: c || (() => y.current),
      prefixCls: S,
      className: L
    }, re("drop")));
  }
  return $(/* @__PURE__ */ a.createElement(be.Provider, {
    value: {
      disabled: m
    }
  }, G));
}
const Br = /* @__PURE__ */ a.forwardRef(vi);
Br.FileCard = Nr;
const xi = zn((e) => /* @__PURE__ */ yn.jsx(Br.FileCard, {
  ...e,
  item: e.item || {}
}));
export {
  xi as AttachmentsFileCard,
  xi as default
};
