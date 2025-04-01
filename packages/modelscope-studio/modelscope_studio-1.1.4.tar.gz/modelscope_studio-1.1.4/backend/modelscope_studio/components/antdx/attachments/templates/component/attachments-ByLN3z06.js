import { i as cr, a as xt, r as ur, g as fr, w as ze, d as dr, b as Te, c as ie, e as pr } from "./Index-CeUPM3o0.js";
const O = window.ms_globals.React, l = window.ms_globals.React, We = window.ms_globals.React.useMemo, Ft = window.ms_globals.React.useState, be = window.ms_globals.React.useEffect, sr = window.ms_globals.React.isValidElement, me = window.ms_globals.React.useRef, ar = window.ms_globals.React.useLayoutEffect, lr = window.ms_globals.React.forwardRef, Nt = window.ms_globals.ReactDOM, Ue = window.ms_globals.ReactDOM.createPortal, mr = window.ms_globals.internalContext.useContextPropsContext, hr = window.ms_globals.internalContext.ContextPropsProvider, gr = window.ms_globals.antd.ConfigProvider, _n = window.ms_globals.antd.Upload, Be = window.ms_globals.antd.theme, vr = window.ms_globals.antd.Progress, ct = window.ms_globals.antd.Button, br = window.ms_globals.antd.Flex, ut = window.ms_globals.antd.Typography, yr = window.ms_globals.antdIcons.FileTextFilled, Sr = window.ms_globals.antdIcons.CloseCircleFilled, xr = window.ms_globals.antdIcons.FileExcelFilled, wr = window.ms_globals.antdIcons.FileImageFilled, Er = window.ms_globals.antdIcons.FileMarkdownFilled, Cr = window.ms_globals.antdIcons.FilePdfFilled, _r = window.ms_globals.antdIcons.FilePptFilled, Lr = window.ms_globals.antdIcons.FileWordFilled, Tr = window.ms_globals.antdIcons.FileZipFilled, Ir = window.ms_globals.antdIcons.PlusOutlined, Rr = window.ms_globals.antdIcons.LeftOutlined, Pr = window.ms_globals.antdIcons.RightOutlined, Ht = window.ms_globals.antdCssinjs.unit, ft = window.ms_globals.antdCssinjs.token2CSSVar, Ut = window.ms_globals.antdCssinjs.useStyleRegister, Mr = window.ms_globals.antdCssinjs.useCSSVarRegister, Or = window.ms_globals.antdCssinjs.createTheme, Fr = window.ms_globals.antdCssinjs.useCacheToken;
var Ar = /\s/;
function $r(e) {
  for (var t = e.length; t-- && Ar.test(e.charAt(t)); )
    ;
  return t;
}
var kr = /^\s+/;
function jr(e) {
  return e && e.slice(0, $r(e) + 1).replace(kr, "");
}
var Bt = NaN, Dr = /^[-+]0x[0-9a-f]+$/i, zr = /^0b[01]+$/i, Nr = /^0o[0-7]+$/i, Hr = parseInt;
function Xt(e) {
  if (typeof e == "number")
    return e;
  if (cr(e))
    return Bt;
  if (xt(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = xt(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = jr(e);
  var n = zr.test(e);
  return n || Nr.test(e) ? Hr(e.slice(2), n ? 2 : 8) : Dr.test(e) ? Bt : +e;
}
function Ur() {
}
var dt = function() {
  return ur.Date.now();
}, Br = "Expected a function", Xr = Math.max, Vr = Math.min;
function Wr(e, t, n) {
  var r, o, i, s, a, c, u = 0, p = !1, f = !1, d = !0;
  if (typeof e != "function")
    throw new TypeError(Br);
  t = Xt(t) || 0, xt(n) && (p = !!n.leading, f = "maxWait" in n, i = f ? Xr(Xt(n.maxWait) || 0, t) : i, d = "trailing" in n ? !!n.trailing : d);
  function h(g) {
    var y = r, E = o;
    return r = o = void 0, u = g, s = e.apply(E, y), s;
  }
  function v(g) {
    return u = g, a = setTimeout(x, t), p ? h(g) : s;
  }
  function b(g) {
    var y = g - c, E = g - u, M = t - y;
    return f ? Vr(M, i - E) : M;
  }
  function m(g) {
    var y = g - c, E = g - u;
    return c === void 0 || y >= t || y < 0 || f && E >= i;
  }
  function x() {
    var g = dt();
    if (m(g))
      return _(g);
    a = setTimeout(x, b(g));
  }
  function _(g) {
    return a = void 0, d && r ? h(g) : (r = o = void 0, s);
  }
  function w() {
    a !== void 0 && clearTimeout(a), u = 0, r = c = o = a = void 0;
  }
  function S() {
    return a === void 0 ? s : _(dt());
  }
  function C() {
    var g = dt(), y = m(g);
    if (r = arguments, o = this, c = g, y) {
      if (a === void 0)
        return v(c);
      if (f)
        return clearTimeout(a), a = setTimeout(x, t), h(c);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return C.cancel = w, C.flush = S, C;
}
var Ln = {
  exports: {}
}, Ge = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Gr = l, Kr = Symbol.for("react.element"), qr = Symbol.for("react.fragment"), Zr = Object.prototype.hasOwnProperty, Qr = Gr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Yr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Tn(e, t, n) {
  var r, o = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (r in t) Zr.call(t, r) && !Yr.hasOwnProperty(r) && (o[r] = t[r]);
  if (e && e.defaultProps) for (r in t = e.defaultProps, t) o[r] === void 0 && (o[r] = t[r]);
  return {
    $$typeof: Kr,
    type: e,
    key: i,
    ref: s,
    props: o,
    _owner: Qr.current
  };
}
Ge.Fragment = qr;
Ge.jsx = Tn;
Ge.jsxs = Tn;
Ln.exports = Ge;
var se = Ln.exports;
const {
  SvelteComponent: Jr,
  assign: Vt,
  binding_callbacks: Wt,
  check_outros: eo,
  children: In,
  claim_element: Rn,
  claim_space: to,
  component_subscribe: Gt,
  compute_slots: no,
  create_slot: ro,
  detach: Se,
  element: Pn,
  empty: Kt,
  exclude_internal_props: qt,
  get_all_dirty_from_scope: oo,
  get_slot_changes: io,
  group_outros: so,
  init: ao,
  insert_hydration: Ne,
  safe_not_equal: lo,
  set_custom_element_data: Mn,
  space: co,
  transition_in: He,
  transition_out: wt,
  update_slot_base: uo
} = window.__gradio__svelte__internal, {
  beforeUpdate: fo,
  getContext: po,
  onDestroy: mo,
  setContext: ho
} = window.__gradio__svelte__internal;
function Zt(e) {
  let t, n;
  const r = (
    /*#slots*/
    e[7].default
  ), o = ro(
    r,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = Pn("svelte-slot"), o && o.c(), this.h();
    },
    l(i) {
      t = Rn(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = In(t);
      o && o.l(s), s.forEach(Se), this.h();
    },
    h() {
      Mn(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      Ne(i, t, s), o && o.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      o && o.p && (!n || s & /*$$scope*/
      64) && uo(
        o,
        r,
        i,
        /*$$scope*/
        i[6],
        n ? io(
          r,
          /*$$scope*/
          i[6],
          s,
          null
        ) : oo(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (He(o, i), n = !0);
    },
    o(i) {
      wt(o, i), n = !1;
    },
    d(i) {
      i && Se(t), o && o.d(i), e[9](null);
    }
  };
}
function go(e) {
  let t, n, r, o, i = (
    /*$$slots*/
    e[4].default && Zt(e)
  );
  return {
    c() {
      t = Pn("react-portal-target"), n = co(), i && i.c(), r = Kt(), this.h();
    },
    l(s) {
      t = Rn(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), In(t).forEach(Se), n = to(s), i && i.l(s), r = Kt(), this.h();
    },
    h() {
      Mn(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      Ne(s, t, a), e[8](t), Ne(s, n, a), i && i.m(s, a), Ne(s, r, a), o = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && He(i, 1)) : (i = Zt(s), i.c(), He(i, 1), i.m(r.parentNode, r)) : i && (so(), wt(i, 1, 1, () => {
        i = null;
      }), eo());
    },
    i(s) {
      o || (He(i), o = !0);
    },
    o(s) {
      wt(i), o = !1;
    },
    d(s) {
      s && (Se(t), Se(n), Se(r)), e[8](null), i && i.d(s);
    }
  };
}
function Qt(e) {
  const {
    svelteInit: t,
    ...n
  } = e;
  return n;
}
function vo(e, t, n) {
  let r, o, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = no(i);
  let {
    svelteInit: c
  } = t;
  const u = ze(Qt(t)), p = ze();
  Gt(e, p, (S) => n(0, r = S));
  const f = ze();
  Gt(e, f, (S) => n(1, o = S));
  const d = [], h = po("$$ms-gr-react-wrapper"), {
    slotKey: v,
    slotIndex: b,
    subSlotIndex: m
  } = fr() || {}, x = c({
    parent: h,
    props: u,
    target: p,
    slot: f,
    slotKey: v,
    slotIndex: b,
    subSlotIndex: m,
    onDestroy(S) {
      d.push(S);
    }
  });
  ho("$$ms-gr-react-wrapper", x), fo(() => {
    u.set(Qt(t));
  }), mo(() => {
    d.forEach((S) => S());
  });
  function _(S) {
    Wt[S ? "unshift" : "push"](() => {
      r = S, p.set(r);
    });
  }
  function w(S) {
    Wt[S ? "unshift" : "push"](() => {
      o = S, f.set(o);
    });
  }
  return e.$$set = (S) => {
    n(17, t = Vt(Vt({}, t), qt(S))), "svelteInit" in S && n(5, c = S.svelteInit), "$$scope" in S && n(6, s = S.$$scope);
  }, t = qt(t), [r, o, p, f, a, c, s, i, _, w];
}
class bo extends Jr {
  constructor(t) {
    super(), ao(this, t, vo, go, lo, {
      svelteInit: 5
    });
  }
}
const Yt = window.ms_globals.rerender, pt = window.ms_globals.tree;
function yo(e, t = {}) {
  function n(r) {
    const o = ze(), i = new bo({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const a = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: e,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? pt;
          return c.nodes = [...c.nodes, a], Yt({
            createPortal: Ue,
            node: pt
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), Yt({
              createPortal: Ue,
              node: pt
            });
          }), a;
        },
        ...r.props
      }
    });
    return o.set(i), i;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
function So(e) {
  const [t, n] = Ft(() => Te(e));
  return be(() => {
    let r = !0;
    return e.subscribe((i) => {
      r && (r = !1, i === t) || n(i);
    });
  }, [e]), t;
}
function xo(e) {
  const t = We(() => dr(e, (n) => n), [e]);
  return So(t);
}
const wo = "1.0.5", Eo = /* @__PURE__ */ l.createContext({}), Co = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, _o = (e) => {
  const t = l.useContext(Eo);
  return l.useMemo(() => ({
    ...Co,
    ...t[e]
  }), [t[e]]);
};
function Ie() {
  return Ie = Object.assign ? Object.assign.bind() : function(e) {
    for (var t = 1; t < arguments.length; t++) {
      var n = arguments[t];
      for (var r in n) ({}).hasOwnProperty.call(n, r) && (e[r] = n[r]);
    }
    return e;
  }, Ie.apply(null, arguments);
}
function Xe() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r,
    theme: o
  } = l.useContext(gr.ConfigContext);
  return {
    theme: o,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: r
  };
}
function Ee(e) {
  var t = O.useRef();
  t.current = e;
  var n = O.useCallback(function() {
    for (var r, o = arguments.length, i = new Array(o), s = 0; s < o; s++)
      i[s] = arguments[s];
    return (r = t.current) === null || r === void 0 ? void 0 : r.call.apply(r, [t].concat(i));
  }, []);
  return n;
}
function Lo(e) {
  if (Array.isArray(e)) return e;
}
function To(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var r, o, i, s, a = [], c = !0, u = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        c = !1;
      } else for (; !(c = (r = i.call(n)).done) && (a.push(r.value), a.length !== t); c = !0) ;
    } catch (p) {
      u = !0, o = p;
    } finally {
      try {
        if (!c && n.return != null && (s = n.return(), Object(s) !== s)) return;
      } finally {
        if (u) throw o;
      }
    }
    return a;
  }
}
function Jt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, r = Array(t); n < t; n++) r[n] = e[n];
  return r;
}
function Io(e, t) {
  if (e) {
    if (typeof e == "string") return Jt(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? Jt(e, t) : void 0;
  }
}
function Ro() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function Z(e, t) {
  return Lo(e) || To(e, t) || Io(e, t) || Ro();
}
function Ke() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var en = Ke() ? O.useLayoutEffect : O.useEffect, Po = function(t, n) {
  var r = O.useRef(!0);
  en(function() {
    return t(r.current);
  }, n), en(function() {
    return r.current = !1, function() {
      r.current = !0;
    };
  }, []);
}, tn = function(t, n) {
  Po(function(r) {
    if (!r)
      return t();
  }, n);
};
function Re(e) {
  var t = O.useRef(!1), n = O.useState(e), r = Z(n, 2), o = r[0], i = r[1];
  O.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, c) {
    c && t.current || i(a);
  }
  return [o, s];
}
function mt(e) {
  return e !== void 0;
}
function Mo(e, t) {
  var n = t || {}, r = n.defaultValue, o = n.value, i = n.onChange, s = n.postState, a = Re(function() {
    return mt(o) ? o : mt(r) ? typeof r == "function" ? r() : r : typeof e == "function" ? e() : e;
  }), c = Z(a, 2), u = c[0], p = c[1], f = o !== void 0 ? o : u, d = s ? s(f) : f, h = Ee(i), v = Re([f]), b = Z(v, 2), m = b[0], x = b[1];
  tn(function() {
    var w = m[0];
    u !== w && h(u, w);
  }, [m]), tn(function() {
    mt(o) || p(o);
  }, [o]);
  var _ = Ee(function(w, S) {
    p(w, S), x([f], S);
  });
  return [d, _];
}
function G(e) {
  "@babel/helpers - typeof";
  return G = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, G(e);
}
var On = {
  exports: {}
}, F = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var At = Symbol.for("react.element"), $t = Symbol.for("react.portal"), qe = Symbol.for("react.fragment"), Ze = Symbol.for("react.strict_mode"), Qe = Symbol.for("react.profiler"), Ye = Symbol.for("react.provider"), Je = Symbol.for("react.context"), Oo = Symbol.for("react.server_context"), et = Symbol.for("react.forward_ref"), tt = Symbol.for("react.suspense"), nt = Symbol.for("react.suspense_list"), rt = Symbol.for("react.memo"), ot = Symbol.for("react.lazy"), Fo = Symbol.for("react.offscreen"), Fn;
Fn = Symbol.for("react.module.reference");
function ae(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case At:
        switch (e = e.type, e) {
          case qe:
          case Qe:
          case Ze:
          case tt:
          case nt:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Oo:
              case Je:
              case et:
              case ot:
              case rt:
              case Ye:
                return e;
              default:
                return t;
            }
        }
      case $t:
        return t;
    }
  }
}
F.ContextConsumer = Je;
F.ContextProvider = Ye;
F.Element = At;
F.ForwardRef = et;
F.Fragment = qe;
F.Lazy = ot;
F.Memo = rt;
F.Portal = $t;
F.Profiler = Qe;
F.StrictMode = Ze;
F.Suspense = tt;
F.SuspenseList = nt;
F.isAsyncMode = function() {
  return !1;
};
F.isConcurrentMode = function() {
  return !1;
};
F.isContextConsumer = function(e) {
  return ae(e) === Je;
};
F.isContextProvider = function(e) {
  return ae(e) === Ye;
};
F.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === At;
};
F.isForwardRef = function(e) {
  return ae(e) === et;
};
F.isFragment = function(e) {
  return ae(e) === qe;
};
F.isLazy = function(e) {
  return ae(e) === ot;
};
F.isMemo = function(e) {
  return ae(e) === rt;
};
F.isPortal = function(e) {
  return ae(e) === $t;
};
F.isProfiler = function(e) {
  return ae(e) === Qe;
};
F.isStrictMode = function(e) {
  return ae(e) === Ze;
};
F.isSuspense = function(e) {
  return ae(e) === tt;
};
F.isSuspenseList = function(e) {
  return ae(e) === nt;
};
F.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === qe || e === Qe || e === Ze || e === tt || e === nt || e === Fo || typeof e == "object" && e !== null && (e.$$typeof === ot || e.$$typeof === rt || e.$$typeof === Ye || e.$$typeof === Je || e.$$typeof === et || e.$$typeof === Fn || e.getModuleId !== void 0);
};
F.typeOf = ae;
On.exports = F;
var ht = On.exports, Ao = Symbol.for("react.element"), $o = Symbol.for("react.transitional.element"), ko = Symbol.for("react.fragment");
function jo(e) {
  return (
    // Base object type
    e && G(e) === "object" && // React Element type
    (e.$$typeof === Ao || e.$$typeof === $o) && // React Fragment type
    e.type === ko
  );
}
var Do = function(t, n) {
  typeof t == "function" ? t(n) : G(t) === "object" && t && "current" in t && (t.current = n);
}, zo = function(t) {
  var n, r;
  if (!t)
    return !1;
  if (An(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var o = ht.isMemo(t) ? t.type.type : t.type;
  return !(typeof o == "function" && !((n = o.prototype) !== null && n !== void 0 && n.render) && o.$$typeof !== ht.ForwardRef || typeof t == "function" && !((r = t.prototype) !== null && r !== void 0 && r.render) && t.$$typeof !== ht.ForwardRef);
};
function An(e) {
  return /* @__PURE__ */ sr(e) && !jo(e);
}
var No = function(t) {
  if (t && An(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function Ho(e, t) {
  if (G(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var r = n.call(e, t || "default");
    if (G(r) != "object") return r;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function $n(e) {
  var t = Ho(e, "string");
  return G(t) == "symbol" ? t : t + "";
}
function T(e, t, n) {
  return (t = $n(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function nn(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var r = Object.getOwnPropertySymbols(e);
    t && (r = r.filter(function(o) {
      return Object.getOwnPropertyDescriptor(e, o).enumerable;
    })), n.push.apply(n, r);
  }
  return n;
}
function L(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? nn(Object(n), !0).forEach(function(r) {
      T(e, r, n[r]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : nn(Object(n)).forEach(function(r) {
      Object.defineProperty(e, r, Object.getOwnPropertyDescriptor(n, r));
    });
  }
  return e;
}
const Pe = /* @__PURE__ */ l.createContext(null);
function rn(e) {
  const {
    getDropContainer: t,
    className: n,
    prefixCls: r,
    children: o
  } = e, {
    disabled: i
  } = l.useContext(Pe), [s, a] = l.useState(), [c, u] = l.useState(null);
  if (l.useEffect(() => {
    const d = t == null ? void 0 : t();
    s !== d && a(d);
  }, [t]), l.useEffect(() => {
    if (s) {
      const d = () => {
        u(!0);
      }, h = (m) => {
        m.preventDefault();
      }, v = (m) => {
        m.relatedTarget || u(!1);
      }, b = (m) => {
        u(!1), m.preventDefault();
      };
      return document.addEventListener("dragenter", d), document.addEventListener("dragover", h), document.addEventListener("dragleave", v), document.addEventListener("drop", b), () => {
        document.removeEventListener("dragenter", d), document.removeEventListener("dragover", h), document.removeEventListener("dragleave", v), document.removeEventListener("drop", b);
      };
    }
  }, [!!s]), !(t && s && !i))
    return null;
  const f = `${r}-drop-area`;
  return /* @__PURE__ */ Ue(/* @__PURE__ */ l.createElement("div", {
    className: ie(f, n, {
      [`${f}-on-body`]: s.tagName === "BODY"
    }),
    style: {
      display: c ? "block" : "none"
    }
  }, o), s);
}
function on(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Uo(e) {
  return e && G(e) === "object" && on(e.nativeElement) ? e.nativeElement : on(e) ? e : null;
}
function Bo(e) {
  var t = Uo(e);
  if (t)
    return t;
  if (e instanceof l.Component) {
    var n;
    return (n = Nt.findDOMNode) === null || n === void 0 ? void 0 : n.call(Nt, e);
  }
  return null;
}
function Xo(e, t) {
  if (e == null) return {};
  var n = {};
  for (var r in e) if ({}.hasOwnProperty.call(e, r)) {
    if (t.includes(r)) continue;
    n[r] = e[r];
  }
  return n;
}
function sn(e, t) {
  if (e == null) return {};
  var n, r, o = Xo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (r = 0; r < i.length; r++) n = i[r], t.includes(n) || {}.propertyIsEnumerable.call(e, n) && (o[n] = e[n]);
  }
  return o;
}
var Vo = /* @__PURE__ */ O.createContext({});
function Ce(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function an(e, t) {
  for (var n = 0; n < t.length; n++) {
    var r = t[n];
    r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(e, $n(r.key), r);
  }
}
function _e(e, t, n) {
  return t && an(e.prototype, t), n && an(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Et(e, t) {
  return Et = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, r) {
    return n.__proto__ = r, n;
  }, Et(e, t);
}
function it(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Et(e, t);
}
function Ve(e) {
  return Ve = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ve(e);
}
function kn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (kn = function() {
    return !!e;
  })();
}
function ye(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function Wo(e, t) {
  if (t && (G(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return ye(e);
}
function st(e) {
  var t = kn();
  return function() {
    var n, r = Ve(e);
    if (t) {
      var o = Ve(this).constructor;
      n = Reflect.construct(r, arguments, o);
    } else n = r.apply(this, arguments);
    return Wo(this, n);
  };
}
var Go = /* @__PURE__ */ function(e) {
  it(n, e);
  var t = st(n);
  function n() {
    return Ce(this, n), t.apply(this, arguments);
  }
  return _e(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(O.Component);
function Ko(e) {
  var t = O.useReducer(function(a) {
    return a + 1;
  }, 0), n = Z(t, 2), r = n[1], o = O.useRef(e), i = Ee(function() {
    return o.current;
  }), s = Ee(function(a) {
    o.current = typeof a == "function" ? a(o.current) : a, r();
  });
  return [i, s];
}
var he = "none", Fe = "appear", Ae = "enter", $e = "leave", ln = "none", le = "prepare", xe = "start", we = "active", kt = "end", jn = "prepared";
function cn(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function qo(e, t) {
  var n = {
    animationend: cn("Animation", "AnimationEnd"),
    transitionend: cn("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var Zo = qo(Ke(), typeof window < "u" ? window : {}), Dn = {};
if (Ke()) {
  var Qo = document.createElement("div");
  Dn = Qo.style;
}
var ke = {};
function zn(e) {
  if (ke[e])
    return ke[e];
  var t = Zo[e];
  if (t)
    for (var n = Object.keys(t), r = n.length, o = 0; o < r; o += 1) {
      var i = n[o];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Dn)
        return ke[e] = t[i], ke[e];
    }
  return "";
}
var Nn = zn("animationend"), Hn = zn("transitionend"), Un = !!(Nn && Hn), un = Nn || "animationend", fn = Hn || "transitionend";
function dn(e, t) {
  if (!e) return null;
  if (G(e) === "object") {
    var n = t.replace(/-\w/g, function(r) {
      return r[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const Yo = function(e) {
  var t = me();
  function n(o) {
    o && (o.removeEventListener(fn, e), o.removeEventListener(un, e));
  }
  function r(o) {
    t.current && t.current !== o && n(t.current), o && o !== t.current && (o.addEventListener(fn, e), o.addEventListener(un, e), t.current = o);
  }
  return O.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [r, n];
};
var Bn = Ke() ? ar : be, Xn = function(t) {
  return +setTimeout(t, 16);
}, Vn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Xn = function(t) {
  return window.requestAnimationFrame(t);
}, Vn = function(t) {
  return window.cancelAnimationFrame(t);
});
var pn = 0, jt = /* @__PURE__ */ new Map();
function Wn(e) {
  jt.delete(e);
}
var Ct = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  pn += 1;
  var r = pn;
  function o(i) {
    if (i === 0)
      Wn(r), t();
    else {
      var s = Xn(function() {
        o(i - 1);
      });
      jt.set(r, s);
    }
  }
  return o(n), r;
};
Ct.cancel = function(e) {
  var t = jt.get(e);
  return Wn(e), Vn(t);
};
const Jo = function() {
  var e = O.useRef(null);
  function t() {
    Ct.cancel(e.current);
  }
  function n(r) {
    var o = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Ct(function() {
      o <= 1 ? r({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(r, o - 1);
    });
    e.current = i;
  }
  return O.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var ei = [le, xe, we, kt], ti = [le, jn], Gn = !1, ni = !0;
function Kn(e) {
  return e === we || e === kt;
}
const ri = function(e, t, n) {
  var r = Re(ln), o = Z(r, 2), i = o[0], s = o[1], a = Jo(), c = Z(a, 2), u = c[0], p = c[1];
  function f() {
    s(le, !0);
  }
  var d = t ? ti : ei;
  return Bn(function() {
    if (i !== ln && i !== kt) {
      var h = d.indexOf(i), v = d[h + 1], b = n(i);
      b === Gn ? s(v, !0) : v && u(function(m) {
        function x() {
          m.isCanceled() || s(v, !0);
        }
        b === !0 ? x() : Promise.resolve(b).then(x);
      });
    }
  }, [e, i]), O.useEffect(function() {
    return function() {
      p();
    };
  }, []), [f, i];
};
function oi(e, t, n, r) {
  var o = r.motionEnter, i = o === void 0 ? !0 : o, s = r.motionAppear, a = s === void 0 ? !0 : s, c = r.motionLeave, u = c === void 0 ? !0 : c, p = r.motionDeadline, f = r.motionLeaveImmediately, d = r.onAppearPrepare, h = r.onEnterPrepare, v = r.onLeavePrepare, b = r.onAppearStart, m = r.onEnterStart, x = r.onLeaveStart, _ = r.onAppearActive, w = r.onEnterActive, S = r.onLeaveActive, C = r.onAppearEnd, g = r.onEnterEnd, y = r.onLeaveEnd, E = r.onVisibleChanged, M = Re(), k = Z(M, 2), j = k[0], I = k[1], P = Ko(he), A = Z(P, 2), R = A[0], D = A[1], ee = Re(null), Q = Z(ee, 2), ce = Q[0], U = Q[1], z = R(), N = me(!1), B = me(null);
  function X() {
    return n();
  }
  var re = me(!1);
  function ge() {
    D(he), U(null, !0);
  }
  var $ = Ee(function(J) {
    var q = R();
    if (q !== he) {
      var ue = X();
      if (!(J && !J.deadline && J.target !== ue)) {
        var Me = re.current, Oe;
        q === Fe && Me ? Oe = C == null ? void 0 : C(ue, J) : q === Ae && Me ? Oe = g == null ? void 0 : g(ue, J) : q === $e && Me && (Oe = y == null ? void 0 : y(ue, J)), Me && Oe !== !1 && ge();
      }
    }
  }), te = Yo($), K = Z(te, 1), H = K[0], oe = function(q) {
    switch (q) {
      case Fe:
        return T(T(T({}, le, d), xe, b), we, _);
      case Ae:
        return T(T(T({}, le, h), xe, m), we, w);
      case $e:
        return T(T(T({}, le, v), xe, x), we, S);
      default:
        return {};
    }
  }, Y = O.useMemo(function() {
    return oe(z);
  }, [z]), W = ri(z, !e, function(J) {
    if (J === le) {
      var q = Y[le];
      return q ? q(X()) : Gn;
    }
    if (ve in Y) {
      var ue;
      U(((ue = Y[ve]) === null || ue === void 0 ? void 0 : ue.call(Y, X(), null)) || null);
    }
    return ve === we && z !== he && (H(X()), p > 0 && (clearTimeout(B.current), B.current = setTimeout(function() {
      $({
        deadline: !0
      });
    }, p))), ve === jn && ge(), ni;
  }), pe = Z(W, 2), or = pe[0], ve = pe[1], ir = Kn(ve);
  re.current = ir;
  var zt = me(null);
  Bn(function() {
    if (!(N.current && zt.current === t)) {
      I(t);
      var J = N.current;
      N.current = !0;
      var q;
      !J && t && a && (q = Fe), J && t && i && (q = Ae), (J && !t && u || !J && f && !t && u) && (q = $e);
      var ue = oe(q);
      q && (e || ue[le]) ? (D(q), or()) : D(he), zt.current = t;
    }
  }, [t]), be(function() {
    // Cancel appear
    (z === Fe && !a || // Cancel enter
    z === Ae && !i || // Cancel leave
    z === $e && !u) && D(he);
  }, [a, i, u]), be(function() {
    return function() {
      N.current = !1, clearTimeout(B.current);
    };
  }, []);
  var at = O.useRef(!1);
  be(function() {
    j && (at.current = !0), j !== void 0 && z === he && ((at.current || j) && (E == null || E(j)), at.current = !0);
  }, [j, z]);
  var lt = ce;
  return Y[le] && ve === xe && (lt = L({
    transition: "none"
  }, lt)), [z, ve, lt, j ?? t];
}
function ii(e) {
  var t = e;
  G(e) === "object" && (t = e.transitionSupport);
  function n(o, i) {
    return !!(o.motionName && t && i !== !1);
  }
  var r = /* @__PURE__ */ O.forwardRef(function(o, i) {
    var s = o.visible, a = s === void 0 ? !0 : s, c = o.removeOnLeave, u = c === void 0 ? !0 : c, p = o.forceRender, f = o.children, d = o.motionName, h = o.leavedClassName, v = o.eventProps, b = O.useContext(Vo), m = b.motion, x = n(o, m), _ = me(), w = me();
    function S() {
      try {
        return _.current instanceof HTMLElement ? _.current : Bo(w.current);
      } catch {
        return null;
      }
    }
    var C = oi(x, a, S, o), g = Z(C, 4), y = g[0], E = g[1], M = g[2], k = g[3], j = O.useRef(k);
    k && (j.current = !0);
    var I = O.useCallback(function(Q) {
      _.current = Q, Do(i, Q);
    }, [i]), P, A = L(L({}, v), {}, {
      visible: a
    });
    if (!f)
      P = null;
    else if (y === he)
      k ? P = f(L({}, A), I) : !u && j.current && h ? P = f(L(L({}, A), {}, {
        className: h
      }), I) : p || !u && !h ? P = f(L(L({}, A), {}, {
        style: {
          display: "none"
        }
      }), I) : P = null;
    else {
      var R;
      E === le ? R = "prepare" : Kn(E) ? R = "active" : E === xe && (R = "start");
      var D = dn(d, "".concat(y, "-").concat(R));
      P = f(L(L({}, A), {}, {
        className: ie(dn(d, y), T(T({}, D, D && R), d, typeof d == "string")),
        style: M
      }), I);
    }
    if (/* @__PURE__ */ O.isValidElement(P) && zo(P)) {
      var ee = No(P);
      ee || (P = /* @__PURE__ */ O.cloneElement(P, {
        ref: I
      }));
    }
    return /* @__PURE__ */ O.createElement(Go, {
      ref: w
    }, P);
  });
  return r.displayName = "CSSMotion", r;
}
const si = ii(Un);
var _t = "add", Lt = "keep", Tt = "remove", gt = "removed";
function ai(e) {
  var t;
  return e && G(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, L(L({}, t), {}, {
    key: String(t.key)
  });
}
function It() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(ai);
}
function li() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], r = 0, o = t.length, i = It(e), s = It(t);
  i.forEach(function(u) {
    for (var p = !1, f = r; f < o; f += 1) {
      var d = s[f];
      if (d.key === u.key) {
        r < f && (n = n.concat(s.slice(r, f).map(function(h) {
          return L(L({}, h), {}, {
            status: _t
          });
        })), r = f), n.push(L(L({}, d), {}, {
          status: Lt
        })), r += 1, p = !0;
        break;
      }
    }
    p || n.push(L(L({}, u), {}, {
      status: Tt
    }));
  }), r < o && (n = n.concat(s.slice(r).map(function(u) {
    return L(L({}, u), {}, {
      status: _t
    });
  })));
  var a = {};
  n.forEach(function(u) {
    var p = u.key;
    a[p] = (a[p] || 0) + 1;
  });
  var c = Object.keys(a).filter(function(u) {
    return a[u] > 1;
  });
  return c.forEach(function(u) {
    n = n.filter(function(p) {
      var f = p.key, d = p.status;
      return f !== u || d !== Tt;
    }), n.forEach(function(p) {
      p.key === u && (p.status = Lt);
    });
  }), n;
}
var ci = ["component", "children", "onVisibleChanged", "onAllRemoved"], ui = ["status"], fi = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function di(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : si, n = /* @__PURE__ */ function(r) {
    it(i, r);
    var o = st(i);
    function i() {
      var s;
      Ce(this, i);
      for (var a = arguments.length, c = new Array(a), u = 0; u < a; u++)
        c[u] = arguments[u];
      return s = o.call.apply(o, [this].concat(c)), T(ye(s), "state", {
        keyEntities: []
      }), T(ye(s), "removeKey", function(p) {
        s.setState(function(f) {
          var d = f.keyEntities.map(function(h) {
            return h.key !== p ? h : L(L({}, h), {}, {
              status: gt
            });
          });
          return {
            keyEntities: d
          };
        }, function() {
          var f = s.state.keyEntities, d = f.filter(function(h) {
            var v = h.status;
            return v !== gt;
          }).length;
          d === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return _e(i, [{
      key: "render",
      value: function() {
        var a = this, c = this.state.keyEntities, u = this.props, p = u.component, f = u.children, d = u.onVisibleChanged;
        u.onAllRemoved;
        var h = sn(u, ci), v = p || O.Fragment, b = {};
        return fi.forEach(function(m) {
          b[m] = h[m], delete h[m];
        }), delete h.keys, /* @__PURE__ */ O.createElement(v, h, c.map(function(m, x) {
          var _ = m.status, w = sn(m, ui), S = _ === _t || _ === Lt;
          return /* @__PURE__ */ O.createElement(t, Ie({}, b, {
            key: w.key,
            visible: S,
            eventProps: w,
            onVisibleChanged: function(g) {
              d == null || d(g, {
                key: w.key
              }), g || a.removeKey(w.key);
            }
          }), function(C, g) {
            return f(L(L({}, C), {}, {
              index: x
            }), g);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, c) {
        var u = a.keys, p = c.keyEntities, f = It(u), d = li(p, f);
        return {
          keyEntities: d.filter(function(h) {
            var v = p.find(function(b) {
              var m = b.key;
              return h.key === m;
            });
            return !(v && v.status === gt && h.status === Tt);
          })
        };
      }
    }]), i;
  }(O.Component);
  return T(n, "defaultProps", {
    component: "div"
  }), n;
}
const pi = di(Un);
function mi(e, t) {
  const {
    children: n,
    upload: r,
    rootClassName: o
  } = e, i = l.useRef(null);
  return l.useImperativeHandle(t, () => i.current), /* @__PURE__ */ l.createElement(_n, Ie({}, r, {
    showUploadList: !1,
    rootClassName: o,
    ref: i
  }), n);
}
const qn = /* @__PURE__ */ l.forwardRef(mi);
var Zn = /* @__PURE__ */ _e(function e() {
  Ce(this, e);
}), Qn = "CALC_UNIT", hi = new RegExp(Qn, "g");
function vt(e) {
  return typeof e == "number" ? "".concat(e).concat(Qn) : e;
}
var gi = /* @__PURE__ */ function(e) {
  it(n, e);
  var t = st(n);
  function n(r, o) {
    var i;
    Ce(this, n), i = t.call(this), T(ye(i), "result", ""), T(ye(i), "unitlessCssVar", void 0), T(ye(i), "lowPriority", void 0);
    var s = G(r);
    return i.unitlessCssVar = o, r instanceof n ? i.result = "(".concat(r.result, ")") : s === "number" ? i.result = vt(r) : s === "string" && (i.result = r), i;
  }
  return _e(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " + ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " + ").concat(vt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result = "".concat(this.result, " - ").concat(o.getResult()) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " - ").concat(vt(o))), this.lowPriority = !0, this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " * ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " * ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "div",
    value: function(o) {
      return this.lowPriority && (this.result = "(".concat(this.result, ")")), o instanceof n ? this.result = "".concat(this.result, " / ").concat(o.getResult(!0)) : (typeof o == "number" || typeof o == "string") && (this.result = "".concat(this.result, " / ").concat(o)), this.lowPriority = !1, this;
    }
  }, {
    key: "getResult",
    value: function(o) {
      return this.lowPriority || o ? "(".concat(this.result, ")") : this.result;
    }
  }, {
    key: "equal",
    value: function(o) {
      var i = this, s = o || {}, a = s.unit, c = !0;
      return typeof a == "boolean" ? c = a : Array.from(this.unitlessCssVar).some(function(u) {
        return i.result.includes(u);
      }) && (c = !1), this.result = this.result.replace(hi, c ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Zn), vi = /* @__PURE__ */ function(e) {
  it(n, e);
  var t = st(n);
  function n(r) {
    var o;
    return Ce(this, n), o = t.call(this), T(ye(o), "result", 0), r instanceof n ? o.result = r.result : typeof r == "number" && (o.result = r), o;
  }
  return _e(n, [{
    key: "add",
    value: function(o) {
      return o instanceof n ? this.result += o.result : typeof o == "number" && (this.result += o), this;
    }
  }, {
    key: "sub",
    value: function(o) {
      return o instanceof n ? this.result -= o.result : typeof o == "number" && (this.result -= o), this;
    }
  }, {
    key: "mul",
    value: function(o) {
      return o instanceof n ? this.result *= o.result : typeof o == "number" && (this.result *= o), this;
    }
  }, {
    key: "div",
    value: function(o) {
      return o instanceof n ? this.result /= o.result : typeof o == "number" && (this.result /= o), this;
    }
  }, {
    key: "equal",
    value: function() {
      return this.result;
    }
  }]), n;
}(Zn), bi = function(t, n) {
  var r = t === "css" ? gi : vi;
  return function(o) {
    return new r(o, n);
  };
}, mn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function hn(e, t, n, r) {
  var o = L({}, t[e]);
  if (r != null && r.deprecatedTokens) {
    var i = r.deprecatedTokens;
    i.forEach(function(a) {
      var c = Z(a, 2), u = c[0], p = c[1];
      if (o != null && o[u] || o != null && o[p]) {
        var f;
        (f = o[p]) !== null && f !== void 0 || (o[p] = o == null ? void 0 : o[u]);
      }
    });
  }
  var s = L(L({}, n), o);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var Yn = typeof CSSINJS_STATISTIC < "u", Rt = !0;
function Dt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!Yn)
    return Object.assign.apply(Object, [{}].concat(t));
  Rt = !1;
  var r = {};
  return t.forEach(function(o) {
    if (G(o) === "object") {
      var i = Object.keys(o);
      i.forEach(function(s) {
        Object.defineProperty(r, s, {
          configurable: !0,
          enumerable: !0,
          get: function() {
            return o[s];
          }
        });
      });
    }
  }), Rt = !0, r;
}
var gn = {};
function yi() {
}
var Si = function(t) {
  var n, r = t, o = yi;
  return Yn && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), r = new Proxy(t, {
    get: function(s, a) {
      if (Rt) {
        var c;
        (c = n) === null || c === void 0 || c.add(a);
      }
      return s[a];
    }
  }), o = function(s, a) {
    var c;
    gn[s] = {
      global: Array.from(n),
      component: L(L({}, (c = gn[s]) === null || c === void 0 ? void 0 : c.component), a)
    };
  }), {
    token: r,
    keys: n,
    flush: o
  };
};
function vn(e, t, n) {
  if (typeof n == "function") {
    var r;
    return n(Dt(t, (r = t[e]) !== null && r !== void 0 ? r : {}));
  }
  return n ?? {};
}
function xi(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "max(".concat(r.map(function(i) {
        return Ht(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, r = new Array(n), o = 0; o < n; o++)
        r[o] = arguments[o];
      return "min(".concat(r.map(function(i) {
        return Ht(i);
      }).join(","), ")");
    }
  };
}
var wi = 1e3 * 60 * 10, Ei = /* @__PURE__ */ function() {
  function e() {
    Ce(this, e), T(this, "map", /* @__PURE__ */ new Map()), T(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), T(this, "nextID", 0), T(this, "lastAccessBeat", /* @__PURE__ */ new Map()), T(this, "accessBeat", 0);
  }
  return _e(e, [{
    key: "set",
    value: function(n, r) {
      this.clear();
      var o = this.getCompositeKey(n);
      this.map.set(o, r), this.lastAccessBeat.set(o, Date.now());
    }
  }, {
    key: "get",
    value: function(n) {
      var r = this.getCompositeKey(n), o = this.map.get(r);
      return this.lastAccessBeat.set(r, Date.now()), this.accessBeat += 1, o;
    }
  }, {
    key: "getCompositeKey",
    value: function(n) {
      var r = this, o = n.map(function(i) {
        return i && G(i) === "object" ? "obj_".concat(r.getObjectID(i)) : "".concat(G(i), "_").concat(i);
      });
      return o.join("|");
    }
  }, {
    key: "getObjectID",
    value: function(n) {
      if (this.objectIDMap.has(n))
        return this.objectIDMap.get(n);
      var r = this.nextID;
      return this.objectIDMap.set(n, r), this.nextID += 1, r;
    }
  }, {
    key: "clear",
    value: function() {
      var n = this;
      if (this.accessBeat > 1e4) {
        var r = Date.now();
        this.lastAccessBeat.forEach(function(o, i) {
          r - o > wi && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), bn = new Ei();
function Ci(e, t) {
  return l.useMemo(function() {
    var n = bn.get(t);
    if (n)
      return n;
    var r = e();
    return bn.set(t, r), r;
  }, t);
}
var _i = function() {
  return {};
};
function Li(e) {
  var t = e.useCSP, n = t === void 0 ? _i : t, r = e.useToken, o = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function c(d, h, v, b) {
    var m = Array.isArray(d) ? d[0] : d;
    function x(E) {
      return "".concat(String(m)).concat(E.slice(0, 1).toUpperCase()).concat(E.slice(1));
    }
    var _ = (b == null ? void 0 : b.unitless) || {}, w = typeof a == "function" ? a(d) : {}, S = L(L({}, w), {}, T({}, x("zIndexPopup"), !0));
    Object.keys(_).forEach(function(E) {
      S[x(E)] = _[E];
    });
    var C = L(L({}, b), {}, {
      unitless: S,
      prefixToken: x
    }), g = p(d, h, v, C), y = u(m, v, C);
    return function(E) {
      var M = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : E, k = g(E, M), j = Z(k, 2), I = j[1], P = y(M), A = Z(P, 2), R = A[0], D = A[1];
      return [R, I, D];
    };
  }
  function u(d, h, v) {
    var b = v.unitless, m = v.injectStyle, x = m === void 0 ? !0 : m, _ = v.prefixToken, w = v.ignore, S = function(y) {
      var E = y.rootCls, M = y.cssVar, k = M === void 0 ? {} : M, j = r(), I = j.realToken;
      return Mr({
        path: [d],
        prefix: k.prefix,
        key: k.key,
        unitless: b,
        ignore: w,
        token: I,
        scope: E
      }, function() {
        var P = vn(d, I, h), A = hn(d, I, P, {
          deprecatedTokens: v == null ? void 0 : v.deprecatedTokens
        });
        return Object.keys(P).forEach(function(R) {
          A[_(R)] = A[R], delete A[R];
        }), A;
      }), null;
    }, C = function(y) {
      var E = r(), M = E.cssVar;
      return [function(k) {
        return x && M ? /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(S, {
          rootCls: y,
          cssVar: M,
          component: d
        }), k) : k;
      }, M == null ? void 0 : M.key];
    };
    return C;
  }
  function p(d, h, v) {
    var b = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(d) ? d : [d, d], x = Z(m, 1), _ = x[0], w = m.join("-"), S = e.layer || {
      name: "antd"
    };
    return function(C) {
      var g = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : C, y = r(), E = y.theme, M = y.realToken, k = y.hashId, j = y.token, I = y.cssVar, P = o(), A = P.rootPrefixCls, R = P.iconPrefixCls, D = n(), ee = I ? "css" : "js", Q = Ci(function() {
        var X = /* @__PURE__ */ new Set();
        return I && Object.keys(b.unitless || {}).forEach(function(re) {
          X.add(ft(re, I.prefix)), X.add(ft(re, mn(_, I.prefix)));
        }), bi(ee, X);
      }, [ee, _, I == null ? void 0 : I.prefix]), ce = xi(ee), U = ce.max, z = ce.min, N = {
        theme: E,
        token: j,
        hashId: k,
        nonce: function() {
          return D.nonce;
        },
        clientOnly: b.clientOnly,
        layer: S,
        // antd is always at top of styles
        order: b.order || -999
      };
      typeof i == "function" && Ut(L(L({}, N), {}, {
        clientOnly: !1,
        path: ["Shared", A]
      }), function() {
        return i(j, {
          prefix: {
            rootPrefixCls: A,
            iconPrefixCls: R
          },
          csp: D
        });
      });
      var B = Ut(L(L({}, N), {}, {
        path: [w, C, R]
      }), function() {
        if (b.injectStyle === !1)
          return [];
        var X = Si(j), re = X.token, ge = X.flush, $ = vn(_, M, v), te = ".".concat(C), K = hn(_, M, $, {
          deprecatedTokens: b.deprecatedTokens
        });
        I && $ && G($) === "object" && Object.keys($).forEach(function(W) {
          $[W] = "var(".concat(ft(W, mn(_, I.prefix)), ")");
        });
        var H = Dt(re, {
          componentCls: te,
          prefixCls: C,
          iconCls: ".".concat(R),
          antCls: ".".concat(A),
          calc: Q,
          // @ts-ignore
          max: U,
          // @ts-ignore
          min: z
        }, I ? $ : K), oe = h(H, {
          hashId: k,
          prefixCls: C,
          rootPrefixCls: A,
          iconPrefixCls: R
        });
        ge(_, K);
        var Y = typeof s == "function" ? s(H, C, g, b.resetFont) : null;
        return [b.resetStyle === !1 ? null : Y, oe];
      });
      return [B, k];
    };
  }
  function f(d, h, v) {
    var b = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = p(d, h, v, L({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, b)), x = function(w) {
      var S = w.prefixCls, C = w.rootCls, g = C === void 0 ? S : C;
      return m(S, g), null;
    };
    return x;
  }
  return {
    genStyleHooks: c,
    genSubStyleComponent: f,
    genComponentStyleHook: p
  };
}
const V = Math.round;
function bt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], r = n.map((o) => parseFloat(o));
  for (let o = 0; o < 3; o += 1)
    r[o] = t(r[o] || 0, n[o] || "", o);
  return n[3] ? r[3] = n[3].includes("%") ? r[3] / 100 : r[3] : r[3] = 1, r;
}
const yn = (e, t, n) => n === 0 ? e : e / 100;
function Le(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class de {
  constructor(t) {
    T(this, "isValid", !0), T(this, "r", 0), T(this, "g", 0), T(this, "b", 0), T(this, "a", 1), T(this, "_h", void 0), T(this, "_s", void 0), T(this, "_l", void 0), T(this, "_v", void 0), T(this, "_max", void 0), T(this, "_min", void 0), T(this, "_brightness", void 0);
    function n(r) {
      return r[0] in t && r[1] in t && r[2] in t;
    }
    if (t) if (typeof t == "string") {
      let o = function(i) {
        return r.startsWith(i);
      };
      const r = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(r) ? this.fromHexString(r) : o("rgb") ? this.fromRgbString(r) : o("hsl") ? this.fromHslString(r) : (o("hsv") || o("hsb")) && this.fromHsvString(r);
    } else if (t instanceof de)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Le(t.r), this.g = Le(t.g), this.b = Le(t.b), this.a = typeof t.a == "number" ? Le(t.a, 1) : 1;
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
    const n = t(this.r), r = t(this.g), o = t(this.b);
    return 0.2126 * n + 0.7152 * r + 0.0722 * o;
  }
  getHue() {
    if (typeof this._h > "u") {
      const t = this.getMax() - this.getMin();
      t === 0 ? this._h = 0 : this._h = V(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() - t / 100;
    return o < 0 && (o = 0), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  lighten(t = 10) {
    const n = this.getHue(), r = this.getSaturation();
    let o = this.getLightness() + t / 100;
    return o > 1 && (o = 1), this._c({
      h: n,
      s: r,
      l: o,
      a: this.a
    });
  }
  /**
   * Mix the current color a given amount with another color, from 0 to 100.
   * 0 means no mixing (return current color).
   */
  mix(t, n = 50) {
    const r = this._c(t), o = n / 100, i = (a) => (r[a] - this[a]) * o + this[a], s = {
      r: V(i("r")),
      g: V(i("g")),
      b: V(i("b")),
      a: V(i("a") * 100) / 100
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
    const n = this._c(t), r = this.a + n.a * (1 - this.a), o = (i) => V((this[i] * this.a + n[i] * n.a * (1 - this.a)) / r);
    return this._c({
      r: o("r"),
      g: o("g"),
      b: o("b"),
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
    const n = (this.r || 0).toString(16);
    t += n.length === 2 ? n : "0" + n;
    const r = (this.g || 0).toString(16);
    t += r.length === 2 ? r : "0" + r;
    const o = (this.b || 0).toString(16);
    if (t += o.length === 2 ? o : "0" + o, typeof this.a == "number" && this.a >= 0 && this.a < 1) {
      const i = V(this.a * 255).toString(16);
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
    const t = this.getHue(), n = V(this.getSaturation() * 100), r = V(this.getLightness() * 100);
    return this.a !== 1 ? `hsla(${t},${n}%,${r}%,${this.a})` : `hsl(${t},${n}%,${r}%)`;
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
  _sc(t, n, r) {
    const o = this.clone();
    return o[t] = Le(n, r), o;
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
    function r(o, i) {
      return parseInt(n[o] + n[i || o], 16);
    }
    n.length < 6 ? (this.r = r(0), this.g = r(1), this.b = r(2), this.a = n[3] ? r(3) / 255 : 1) : (this.r = r(0, 1), this.g = r(2, 3), this.b = r(4, 5), this.a = n[6] ? r(6, 7) / 255 : 1);
  }
  fromHsl({
    h: t,
    s: n,
    l: r,
    a: o
  }) {
    if (this._h = t % 360, this._s = n, this._l = r, this.a = typeof o == "number" ? o : 1, n <= 0) {
      const d = V(r * 255);
      this.r = d, this.g = d, this.b = d;
    }
    let i = 0, s = 0, a = 0;
    const c = t / 60, u = (1 - Math.abs(2 * r - 1)) * n, p = u * (1 - Math.abs(c % 2 - 1));
    c >= 0 && c < 1 ? (i = u, s = p) : c >= 1 && c < 2 ? (i = p, s = u) : c >= 2 && c < 3 ? (s = u, a = p) : c >= 3 && c < 4 ? (s = p, a = u) : c >= 4 && c < 5 ? (i = p, a = u) : c >= 5 && c < 6 && (i = u, a = p);
    const f = r - u / 2;
    this.r = V((i + f) * 255), this.g = V((s + f) * 255), this.b = V((a + f) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: r,
    a: o
  }) {
    this._h = t % 360, this._s = n, this._v = r, this.a = typeof o == "number" ? o : 1;
    const i = V(r * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), c = s - a, u = V(r * (1 - n) * 255), p = V(r * (1 - n * c) * 255), f = V(r * (1 - n * (1 - c)) * 255);
    switch (a) {
      case 0:
        this.g = f, this.b = u;
        break;
      case 1:
        this.r = p, this.b = u;
        break;
      case 2:
        this.r = u, this.b = f;
        break;
      case 3:
        this.r = u, this.g = p;
        break;
      case 4:
        this.r = f, this.g = u;
        break;
      case 5:
      default:
        this.g = u, this.b = p;
        break;
    }
  }
  fromHsvString(t) {
    const n = bt(t, yn);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = bt(t, yn);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = bt(t, (r, o) => (
      // Convert percentage to number. e.g. 50% -> 128
      o.includes("%") ? V(r / 100 * 255) : r
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const Ti = {
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
}, Ii = Object.assign(Object.assign({}, Ti), {
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
function yt(e) {
  return e >= 0 && e <= 255;
}
function je(e, t) {
  const {
    r: n,
    g: r,
    b: o,
    a: i
  } = new de(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: c
  } = new de(t).toRgb();
  for (let u = 0.01; u <= 1; u += 0.01) {
    const p = Math.round((n - s * (1 - u)) / u), f = Math.round((r - a * (1 - u)) / u), d = Math.round((o - c * (1 - u)) / u);
    if (yt(p) && yt(f) && yt(d))
      return new de({
        r: p,
        g: f,
        b: d,
        a: Math.round(u * 100) / 100
      }).toRgbString();
  }
  return new de({
    r: n,
    g: r,
    b: o,
    a: 1
  }).toRgbString();
}
var Ri = function(e, t) {
  var n = {};
  for (var r in e) Object.prototype.hasOwnProperty.call(e, r) && t.indexOf(r) < 0 && (n[r] = e[r]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var o = 0, r = Object.getOwnPropertySymbols(e); o < r.length; o++)
    t.indexOf(r[o]) < 0 && Object.prototype.propertyIsEnumerable.call(e, r[o]) && (n[r[o]] = e[r[o]]);
  return n;
};
function Pi(e) {
  const {
    override: t
  } = e, n = Ri(e, ["override"]), r = Object.assign({}, t);
  Object.keys(Ii).forEach((d) => {
    delete r[d];
  });
  const o = Object.assign(Object.assign({}, n), r), i = 480, s = 576, a = 768, c = 992, u = 1200, p = 1600;
  if (o.motion === !1) {
    const d = "0s";
    o.motionDurationFast = d, o.motionDurationMid = d, o.motionDurationSlow = d;
  }
  return Object.assign(Object.assign(Object.assign({}, o), {
    // ============== Background ============== //
    colorFillContent: o.colorFillSecondary,
    colorFillContentHover: o.colorFill,
    colorFillAlter: o.colorFillQuaternary,
    colorBgContainerDisabled: o.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: o.colorBgContainer,
    colorSplit: je(o.colorBorderSecondary, o.colorBgContainer),
    // ============== Text ============== //
    colorTextPlaceholder: o.colorTextQuaternary,
    colorTextDisabled: o.colorTextQuaternary,
    colorTextHeading: o.colorText,
    colorTextLabel: o.colorTextSecondary,
    colorTextDescription: o.colorTextTertiary,
    colorTextLightSolid: o.colorWhite,
    colorHighlight: o.colorError,
    colorBgTextHover: o.colorFillSecondary,
    colorBgTextActive: o.colorFill,
    colorIcon: o.colorTextTertiary,
    colorIconHover: o.colorText,
    colorErrorOutline: je(o.colorErrorBg, o.colorBgContainer),
    colorWarningOutline: je(o.colorWarningBg, o.colorBgContainer),
    // Font
    fontSizeIcon: o.fontSizeSM,
    // Line
    lineWidthFocus: o.lineWidth * 3,
    // Control
    lineWidth: o.lineWidth,
    controlOutlineWidth: o.lineWidth * 2,
    // Checkbox size and expand icon size
    controlInteractiveSize: o.controlHeight / 2,
    controlItemBgHover: o.colorFillTertiary,
    controlItemBgActive: o.colorPrimaryBg,
    controlItemBgActiveHover: o.colorPrimaryBgHover,
    controlItemBgActiveDisabled: o.colorFill,
    controlTmpOutline: o.colorFillQuaternary,
    controlOutline: je(o.colorPrimaryBg, o.colorBgContainer),
    lineType: o.lineType,
    borderRadius: o.borderRadius,
    borderRadiusXS: o.borderRadiusXS,
    borderRadiusSM: o.borderRadiusSM,
    borderRadiusLG: o.borderRadiusLG,
    fontWeightStrong: 600,
    opacityLoading: 0.65,
    linkDecoration: "none",
    linkHoverDecoration: "none",
    linkFocusDecoration: "none",
    controlPaddingHorizontal: 12,
    controlPaddingHorizontalSM: 8,
    paddingXXS: o.sizeXXS,
    paddingXS: o.sizeXS,
    paddingSM: o.sizeSM,
    padding: o.size,
    paddingMD: o.sizeMD,
    paddingLG: o.sizeLG,
    paddingXL: o.sizeXL,
    paddingContentHorizontalLG: o.sizeLG,
    paddingContentVerticalLG: o.sizeMS,
    paddingContentHorizontal: o.sizeMS,
    paddingContentVertical: o.sizeSM,
    paddingContentHorizontalSM: o.size,
    paddingContentVerticalSM: o.sizeXS,
    marginXXS: o.sizeXXS,
    marginXS: o.sizeXS,
    marginSM: o.sizeSM,
    margin: o.size,
    marginMD: o.sizeMD,
    marginLG: o.sizeLG,
    marginXL: o.sizeXL,
    marginXXL: o.sizeXXL,
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
    screenLGMax: u - 1,
    screenXL: u,
    screenXLMin: u,
    screenXLMax: p - 1,
    screenXXL: p,
    screenXXLMin: p,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new de("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new de("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new de("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const Mi = {
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
}, Oi = {
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
}, Fi = Or(Be.defaultAlgorithm), Ai = {
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
}, Jn = (e, t, n) => {
  const r = n.getDerivativeToken(e), {
    override: o,
    ...i
  } = t;
  let s = {
    ...r,
    override: o
  };
  return s = Pi(s), i && Object.entries(i).forEach(([a, c]) => {
    const {
      theme: u,
      ...p
    } = c;
    let f = p;
    u && (f = Jn({
      ...s,
      ...p
    }, {
      override: p
    }, u)), s[a] = f;
  }), s;
};
function $i() {
  const {
    token: e,
    hashed: t,
    theme: n = Fi,
    override: r,
    cssVar: o
  } = l.useContext(Be._internalContext), [i, s, a] = Fr(n, [Be.defaultSeed, e], {
    salt: `${wo}-${t || ""}`,
    override: r,
    getComputedToken: Jn,
    cssVar: o && {
      prefix: o.prefix,
      key: o.key,
      unitless: Mi,
      ignore: Oi,
      preserve: Ai
    }
  });
  return [n, a, t ? s : "", i, o];
}
const {
  genStyleHooks: ki,
  genComponentStyleHook: us,
  genSubStyleComponent: fs
} = Li({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Xe();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, r, o] = $i();
    return {
      theme: e,
      realToken: t,
      hashId: n,
      token: r,
      cssVar: o
    };
  },
  useCSP: () => {
    const {
      csp: e
    } = Xe();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
}), ji = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list-card`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
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
        padding: n(e.paddingSM).sub(e.lineWidth).equal(),
        paddingInlineStart: n(e.padding).add(e.lineWidth).equal(),
        display: "flex",
        flexWrap: "nowrap",
        gap: e.paddingXS,
        alignItems: "flex-start",
        width: 236,
        // Icon
        [`${r}-icon`]: {
          fontSize: n(e.fontSizeLG).mul(2).equal(),
          lineHeight: 1,
          paddingTop: n(e.paddingXXS).mul(1.5).equal(),
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
        width: o,
        height: o,
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
            borderRadius: n(e.borderRadius).sub(e.lineWidth).equal()
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
          marginInlineEnd: n(e.paddingSM).mul(-1).equal()
        }
      }
    }
  };
}, Pt = {
  "&, *": {
    boxSizing: "border-box"
  }
}, Di = (e) => {
  const {
    componentCls: t,
    calc: n,
    antCls: r
  } = e, o = `${t}-drop-area`, i = `${t}-placeholder`;
  return {
    // ============================== Full Screen ==============================
    [o]: {
      position: "absolute",
      inset: 0,
      zIndex: e.zIndexPopupBase,
      ...Pt,
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
        ...Pt,
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
          gap: n(e.paddingXXS).div(2).equal()
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
}, zi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, r = `${t}-list`, o = n(e.fontSize).mul(e.lineHeight).mul(2).add(e.paddingSM).add(e.paddingSM).equal();
  return {
    [t]: {
      position: "relative",
      width: "100%",
      ...Pt,
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
          maxHeight: n(o).mul(3).equal(),
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
          width: o,
          height: o,
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
}, Ni = (e) => {
  const {
    colorBgContainer: t
  } = e;
  return {
    colorBgPlaceholderHover: new de(t).setA(0.85).toRgbString()
  };
}, er = ki("Attachments", (e) => {
  const t = Dt(e, {});
  return [Di(t), zi(t), ji(t)];
}, Ni), Hi = (e) => e.indexOf("image/") === 0, De = 200;
function Ui(e) {
  return new Promise((t) => {
    if (!e || !e.type || !Hi(e.type)) {
      t("");
      return;
    }
    const n = new Image();
    if (n.onload = () => {
      const {
        width: r,
        height: o
      } = n, i = r / o, s = i > 1 ? De : De * i, a = i > 1 ? De / i : De, c = document.createElement("canvas");
      c.width = s, c.height = a, c.style.cssText = `position: fixed; left: 0; top: 0; width: ${s}px; height: ${a}px; z-index: 9999; display: none;`, document.body.appendChild(c), c.getContext("2d").drawImage(n, 0, 0, s, a);
      const p = c.toDataURL();
      document.body.removeChild(c), window.URL.revokeObjectURL(n.src), t(p);
    }, n.crossOrigin = "anonymous", e.type.startsWith("image/svg+xml")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && typeof r.result == "string" && (n.src = r.result);
      }, r.readAsDataURL(e);
    } else if (e.type.startsWith("image/gif")) {
      const r = new FileReader();
      r.onload = () => {
        r.result && t(r.result);
      }, r.readAsDataURL(e);
    } else
      n.src = window.URL.createObjectURL(e);
  });
}
function Bi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "audio"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M10.7315824,7.11216117 C10.7428131,7.15148751 10.7485063,7.19218979 10.7485063,7.23309113 L10.7485063,8.07742614 C10.7484199,8.27364959 10.6183424,8.44607275 10.4296853,8.50003683 L8.32984514,9.09986306 L8.32984514,11.7071803 C8.32986605,12.5367078 7.67249692,13.217028 6.84345686,13.2454634 L6.79068592,13.2463395 C6.12766108,13.2463395 5.53916361,12.8217001 5.33010655,12.1924966 C5.1210495,11.563293 5.33842118,10.8709227 5.86959669,10.4741173 C6.40077221,10.0773119 7.12636292,10.0652587 7.67042486,10.4442027 L7.67020842,7.74937024 L7.68449368,7.74937024 C7.72405122,7.59919041 7.83988806,7.48101083 7.98924584,7.4384546 L10.1880418,6.81004755 C10.42156,6.74340323 10.6648954,6.87865515 10.7315824,7.11216117 Z M9.60714286,1.31785714 L12.9678571,4.67857143 L9.60714286,4.67857143 L9.60714286,1.31785714 Z",
    fill: "currentColor"
  })));
}
function Xi(e) {
  const {
    percent: t
  } = e, {
    token: n
  } = Be.useToken();
  return /* @__PURE__ */ l.createElement(vr, {
    type: "circle",
    percent: t,
    size: n.fontSizeHeading2 * 2,
    strokeColor: "#FFF",
    trailColor: "rgba(255, 255, 255, 0.3)",
    format: (r) => /* @__PURE__ */ l.createElement("span", {
      style: {
        color: "#FFF"
      }
    }, (r || 0).toFixed(0), "%")
  });
}
function Vi() {
  return /* @__PURE__ */ l.createElement("svg", {
    width: "1em",
    height: "1em",
    viewBox: "0 0 16 16",
    version: "1.1",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink"
  }, /* @__PURE__ */ l.createElement("title", null, "video"), /* @__PURE__ */ l.createElement("g", {
    stroke: "none",
    "stroke-width": "1",
    fill: "none",
    "fill-rule": "evenodd"
  }, /* @__PURE__ */ l.createElement("path", {
    d: "M14.1178571,4.0125 C14.225,4.11964286 14.2857143,4.26428571 14.2857143,4.41607143 L14.2857143,15.4285714 C14.2857143,15.7446429 14.0303571,16 13.7142857,16 L2.28571429,16 C1.96964286,16 1.71428571,15.7446429 1.71428571,15.4285714 L1.71428571,0.571428571 C1.71428571,0.255357143 1.96964286,0 2.28571429,0 L9.86964286,0 C10.0214286,0 10.1678571,0.0607142857 10.275,0.167857143 L14.1178571,4.0125 Z M12.9678571,4.67857143 L9.60714286,1.31785714 L9.60714286,4.67857143 L12.9678571,4.67857143 Z M10.5379461,10.3101106 L6.68957555,13.0059749 C6.59910784,13.0693494 6.47439406,13.0473861 6.41101953,12.9569184 C6.3874624,12.9232903 6.37482581,12.8832269 6.37482581,12.8421686 L6.37482581,7.45043999 C6.37482581,7.33998304 6.46436886,7.25043999 6.57482581,7.25043999 C6.61588409,7.25043999 6.65594753,7.26307658 6.68957555,7.28663371 L10.5379461,9.98249803 C10.6284138,10.0458726 10.6503772,10.1705863 10.5870027,10.2610541 C10.5736331,10.2801392 10.5570312,10.2967411 10.5379461,10.3101106 Z",
    fill: "currentColor"
  })));
}
const St = " ", Mt = "#8c8c8c", tr = ["png", "jpg", "jpeg", "gif", "bmp", "webp", "svg"], Wi = [{
  icon: /* @__PURE__ */ l.createElement(xr, null),
  color: "#22b35e",
  ext: ["xlsx", "xls"]
}, {
  icon: /* @__PURE__ */ l.createElement(wr, null),
  color: Mt,
  ext: tr
}, {
  icon: /* @__PURE__ */ l.createElement(Er, null),
  color: Mt,
  ext: ["md", "mdx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Cr, null),
  color: "#ff4d4f",
  ext: ["pdf"]
}, {
  icon: /* @__PURE__ */ l.createElement(_r, null),
  color: "#ff6e31",
  ext: ["ppt", "pptx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Lr, null),
  color: "#1677ff",
  ext: ["doc", "docx"]
}, {
  icon: /* @__PURE__ */ l.createElement(Tr, null),
  color: "#fab714",
  ext: ["zip", "rar", "7z", "tar", "gz"]
}, {
  icon: /* @__PURE__ */ l.createElement(Vi, null),
  color: "#ff4d4f",
  ext: ["mp4", "avi", "mov", "wmv", "flv", "mkv"]
}, {
  icon: /* @__PURE__ */ l.createElement(Bi, null),
  color: "#8c8c8c",
  ext: ["mp3", "wav", "flac", "ape", "aac", "ogg"]
}];
function Sn(e, t) {
  return t.some((n) => e.toLowerCase() === `.${n}`);
}
function Gi(e) {
  let t = e;
  const n = ["B", "KB", "MB", "GB", "TB", "PB", "EB"];
  let r = 0;
  for (; t >= 1024 && r < n.length - 1; )
    t /= 1024, r++;
  return `${t.toFixed(0)} ${n[r]}`;
}
function Ki(e, t) {
  const {
    prefixCls: n,
    item: r,
    onRemove: o,
    className: i,
    style: s
  } = e, a = l.useContext(Pe), {
    disabled: c
  } = a || {}, {
    name: u,
    size: p,
    percent: f,
    status: d = "done",
    description: h
  } = r, {
    getPrefixCls: v
  } = Xe(), b = v("attachment", n), m = `${b}-list-card`, [x, _, w] = er(b), [S, C] = l.useMemo(() => {
    const R = u || "", D = R.match(/^(.*)\.[^.]+$/);
    return D ? [D[1], R.slice(D[1].length)] : [R, ""];
  }, [u]), g = l.useMemo(() => Sn(C, tr), [C]), y = l.useMemo(() => h || (d === "uploading" ? `${f || 0}%` : d === "error" ? r.response || St : p ? Gi(p) : St), [d, f]), [E, M] = l.useMemo(() => {
    for (const {
      ext: R,
      icon: D,
      color: ee
    } of Wi)
      if (Sn(C, R))
        return [D, ee];
    return [/* @__PURE__ */ l.createElement(yr, {
      key: "defaultIcon"
    }), Mt];
  }, [C]), [k, j] = l.useState();
  l.useEffect(() => {
    if (r.originFileObj) {
      let R = !0;
      return Ui(r.originFileObj).then((D) => {
        R && j(D);
      }), () => {
        R = !1;
      };
    }
    j(void 0);
  }, [r.originFileObj]);
  let I = null;
  const P = r.thumbUrl || r.url || k, A = g && (r.originFileObj || P);
  return A ? I = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("img", {
    alt: "preview",
    src: P
  }), d !== "done" && /* @__PURE__ */ l.createElement("div", {
    className: `${m}-img-mask`
  }, d === "uploading" && f !== void 0 && /* @__PURE__ */ l.createElement(Xi, {
    percent: f,
    prefixCls: m
  }), d === "error" && /* @__PURE__ */ l.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, y)))) : I = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-icon`,
    style: {
      color: M
    }
  }, E), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-content`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-name`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, S ?? St), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-suffix`
  }, C)), /* @__PURE__ */ l.createElement("div", {
    className: `${m}-desc`
  }, /* @__PURE__ */ l.createElement("div", {
    className: `${m}-ellipsis-prefix`
  }, y)))), x(/* @__PURE__ */ l.createElement("div", {
    className: ie(m, {
      [`${m}-status-${d}`]: d,
      [`${m}-type-preview`]: A,
      [`${m}-type-overview`]: !A
    }, i, _, w),
    style: s,
    ref: t
  }, I, !c && o && /* @__PURE__ */ l.createElement("button", {
    type: "button",
    className: `${m}-remove`,
    onClick: () => {
      o(r);
    }
  }, /* @__PURE__ */ l.createElement(Sr, null))));
}
const nr = /* @__PURE__ */ l.forwardRef(Ki), xn = 1;
function qi(e) {
  const {
    prefixCls: t,
    items: n,
    onRemove: r,
    overflow: o,
    upload: i,
    listClassName: s,
    listStyle: a,
    itemClassName: c,
    itemStyle: u
  } = e, p = `${t}-list`, f = l.useRef(null), [d, h] = l.useState(!1), {
    disabled: v
  } = l.useContext(Pe);
  l.useEffect(() => (h(!0), () => {
    h(!1);
  }), []);
  const [b, m] = l.useState(!1), [x, _] = l.useState(!1), w = () => {
    const y = f.current;
    y && (o === "scrollX" ? (m(Math.abs(y.scrollLeft) >= xn), _(y.scrollWidth - y.clientWidth - Math.abs(y.scrollLeft) >= xn)) : o === "scrollY" && (m(y.scrollTop !== 0), _(y.scrollHeight - y.clientHeight !== y.scrollTop)));
  };
  l.useEffect(() => {
    w();
  }, [o]);
  const S = (y) => {
    const E = f.current;
    E && E.scrollTo({
      left: E.scrollLeft + y * E.clientWidth,
      behavior: "smooth"
    });
  }, C = () => {
    S(-1);
  }, g = () => {
    S(1);
  };
  return /* @__PURE__ */ l.createElement("div", {
    className: ie(p, {
      [`${p}-overflow-${e.overflow}`]: o,
      [`${p}-overflow-ping-start`]: b,
      [`${p}-overflow-ping-end`]: x
    }, s),
    ref: f,
    onScroll: w,
    style: a
  }, /* @__PURE__ */ l.createElement(pi, {
    keys: n.map((y) => ({
      key: y.uid,
      item: y
    })),
    motionName: `${p}-card-motion`,
    component: !1,
    motionAppear: d,
    motionLeave: !0,
    motionEnter: !0
  }, ({
    key: y,
    item: E,
    className: M,
    style: k
  }) => /* @__PURE__ */ l.createElement(nr, {
    key: y,
    prefixCls: t,
    item: E,
    onRemove: r,
    className: ie(M, c),
    style: {
      ...k,
      ...u
    }
  })), !v && /* @__PURE__ */ l.createElement(qn, {
    upload: i
  }, /* @__PURE__ */ l.createElement(ct, {
    className: `${p}-upload-btn`,
    type: "dashed"
  }, /* @__PURE__ */ l.createElement(Ir, {
    className: `${p}-upload-btn-icon`
  }))), o === "scrollX" && /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(ct, {
    size: "small",
    shape: "circle",
    className: `${p}-prev-btn`,
    icon: /* @__PURE__ */ l.createElement(Rr, null),
    onClick: C
  }), /* @__PURE__ */ l.createElement(ct, {
    size: "small",
    shape: "circle",
    className: `${p}-next-btn`,
    icon: /* @__PURE__ */ l.createElement(Pr, null),
    onClick: g
  })));
}
function Zi(e, t) {
  const {
    prefixCls: n,
    placeholder: r = {},
    upload: o,
    className: i,
    style: s
  } = e, a = `${n}-placeholder`, c = r || {}, {
    disabled: u
  } = l.useContext(Pe), [p, f] = l.useState(!1), d = () => {
    f(!0);
  }, h = (m) => {
    m.currentTarget.contains(m.relatedTarget) || f(!1);
  }, v = () => {
    f(!1);
  }, b = /* @__PURE__ */ l.isValidElement(r) ? r : /* @__PURE__ */ l.createElement(br, {
    align: "center",
    justify: "center",
    vertical: !0,
    className: `${a}-inner`
  }, /* @__PURE__ */ l.createElement(ut.Text, {
    className: `${a}-icon`
  }, c.icon), /* @__PURE__ */ l.createElement(ut.Title, {
    className: `${a}-title`,
    level: 5
  }, c.title), /* @__PURE__ */ l.createElement(ut.Text, {
    className: `${a}-description`,
    type: "secondary"
  }, c.description));
  return /* @__PURE__ */ l.createElement("div", {
    className: ie(a, {
      [`${a}-drag-in`]: p,
      [`${a}-disabled`]: u
    }, i),
    onDragEnter: d,
    onDragLeave: h,
    onDrop: v,
    "aria-hidden": u,
    style: s
  }, /* @__PURE__ */ l.createElement(_n.Dragger, Ie({
    showUploadList: !1
  }, o, {
    ref: t,
    style: {
      padding: 0,
      border: 0,
      background: "transparent"
    }
  }), b));
}
const Qi = /* @__PURE__ */ l.forwardRef(Zi);
function Yi(e, t) {
  const {
    prefixCls: n,
    rootClassName: r,
    rootStyle: o,
    className: i,
    style: s,
    items: a,
    children: c,
    getDropContainer: u,
    placeholder: p,
    onChange: f,
    overflow: d,
    disabled: h,
    classNames: v = {},
    styles: b = {},
    ...m
  } = e, {
    getPrefixCls: x,
    direction: _
  } = Xe(), w = x("attachment", n), S = _o("attachments"), {
    classNames: C,
    styles: g
  } = S, y = l.useRef(null), E = l.useRef(null);
  l.useImperativeHandle(t, () => ({
    nativeElement: y.current,
    upload: (U) => {
      var N, B;
      const z = (B = (N = E.current) == null ? void 0 : N.nativeElement) == null ? void 0 : B.querySelector('input[type="file"]');
      if (z) {
        const X = new DataTransfer();
        X.items.add(U), z.files = X.files, z.dispatchEvent(new Event("change", {
          bubbles: !0
        }));
      }
    }
  }));
  const [M, k, j] = er(w), I = ie(k, j), [P, A] = Mo([], {
    value: a
  }), R = Ee((U) => {
    A(U.fileList), f == null || f(U);
  }), D = {
    ...m,
    fileList: P,
    onChange: R
  }, ee = (U) => {
    const z = P.filter((N) => N.uid !== U.uid);
    R({
      file: U,
      fileList: z
    });
  };
  let Q;
  const ce = (U, z, N) => {
    const B = typeof p == "function" ? p(U) : p;
    return /* @__PURE__ */ l.createElement(Qi, {
      placeholder: B,
      upload: D,
      prefixCls: w,
      className: ie(C.placeholder, v.placeholder),
      style: {
        ...g.placeholder,
        ...b.placeholder,
        ...z == null ? void 0 : z.style
      },
      ref: N
    });
  };
  if (c)
    Q = /* @__PURE__ */ l.createElement(l.Fragment, null, /* @__PURE__ */ l.createElement(qn, {
      upload: D,
      rootClassName: r,
      ref: E
    }, c), /* @__PURE__ */ l.createElement(rn, {
      getDropContainer: u,
      prefixCls: w,
      className: ie(I, r)
    }, ce("drop")));
  else {
    const U = P.length > 0;
    Q = /* @__PURE__ */ l.createElement("div", {
      className: ie(w, I, {
        [`${w}-rtl`]: _ === "rtl"
      }, i, r),
      style: {
        ...o,
        ...s
      },
      dir: _ || "ltr",
      ref: y
    }, /* @__PURE__ */ l.createElement(qi, {
      prefixCls: w,
      items: P,
      onRemove: ee,
      overflow: d,
      upload: D,
      listClassName: ie(C.list, v.list),
      listStyle: {
        ...g.list,
        ...b.list,
        ...!U && {
          display: "none"
        }
      },
      itemClassName: ie(C.item, v.item),
      itemStyle: {
        ...g.item,
        ...b.item
      }
    }), ce("inline", U ? {
      style: {
        display: "none"
      }
    } : {}, E), /* @__PURE__ */ l.createElement(rn, {
      getDropContainer: u || (() => y.current),
      prefixCls: w,
      className: I
    }, ce("drop")));
  }
  return M(/* @__PURE__ */ l.createElement(Pe.Provider, {
    value: {
      disabled: h
    }
  }, Q));
}
const rr = /* @__PURE__ */ l.forwardRef(Yi);
rr.FileCard = nr;
function Ji(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function es(e, t = !1) {
  try {
    if (pr(e))
      return e;
    if (t && !Ji(e))
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
function ne(e, t) {
  return We(() => es(e, t), [e, t]);
}
function ts(e, t) {
  const n = We(() => l.Children.toArray(e.originalChildren || e).filter((i) => i.props.node && !i.props.node.ignore && (!i.props.nodeSlotKey || t)).sort((i, s) => {
    if (i.props.node.slotIndex && s.props.node.slotIndex) {
      const a = Te(i.props.node.slotIndex) || 0, c = Te(s.props.node.slotIndex) || 0;
      return a - c === 0 && i.props.node.subSlotIndex && s.props.node.subSlotIndex ? (Te(i.props.node.subSlotIndex) || 0) - (Te(s.props.node.subSlotIndex) || 0) : a - c;
    }
    return 0;
  }).map((i) => i.props.node.target), [e, t]);
  return xo(n);
}
const ns = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function rs(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const r = e[n];
    return t[n] = os(n, r), t;
  }, {}) : {};
}
function os(e, t) {
  return typeof t == "number" && !ns.includes(e) ? t + "px" : t;
}
function Ot(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const o = l.Children.toArray(e._reactElement.props.children).map((i) => {
      if (l.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Ot(i.props.el);
        return l.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...l.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return o.originalChildren = e._reactElement.props.children, t.push(Ue(l.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: o
    }), n)), {
      clonedElement: n,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((o) => {
    e.getEventListeners(o).forEach(({
      listener: s,
      type: a,
      useCapture: c
    }) => {
      n.addEventListener(a, s, c);
    });
  });
  const r = Array.from(e.childNodes);
  for (let o = 0; o < r.length; o++) {
    const i = r[o];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Ot(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function is(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const wn = lr(({
  slot: e,
  clone: t,
  className: n,
  style: r,
  observeAttributes: o
}, i) => {
  const s = me(), [a, c] = Ft([]), {
    forceClone: u
  } = mr(), p = u ? !0 : t;
  return be(() => {
    var b;
    if (!s.current || !e)
      return;
    let f = e;
    function d() {
      let m = f;
      if (f.tagName.toLowerCase() === "svelte-slot" && f.children.length === 1 && f.children[0] && (m = f.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), is(i, m), n && m.classList.add(...n.split(" ")), r) {
        const x = rs(r);
        Object.keys(x).forEach((_) => {
          m.style[_] = x[_];
        });
      }
    }
    let h = null, v = null;
    if (p && window.MutationObserver) {
      let m = function() {
        var S, C, g;
        (S = s.current) != null && S.contains(f) && ((C = s.current) == null || C.removeChild(f));
        const {
          portals: _,
          clonedElement: w
        } = Ot(e);
        f = w, c(_), f.style.display = "contents", v && clearTimeout(v), v = setTimeout(() => {
          d();
        }, 50), (g = s.current) == null || g.appendChild(f);
      };
      m();
      const x = Wr(() => {
        m(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: o
        });
      }, 50);
      h = new window.MutationObserver(x), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      f.style.display = "contents", d(), (b = s.current) == null || b.appendChild(f);
    return () => {
      var m, x;
      f.style.display = "", (m = s.current) != null && m.contains(f) && ((x = s.current) == null || x.removeChild(f)), h == null || h.disconnect();
    };
  }, [e, p, n, r, i, o]), l.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), ss = ({
  children: e,
  ...t
}) => /* @__PURE__ */ se.jsx(se.Fragment, {
  children: e(t)
});
function as(e) {
  return l.createElement(ss, {
    children: e
  });
}
function En(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? as((n) => /* @__PURE__ */ se.jsx(hr, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ se.jsx(wn, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ se.jsx(wn, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function fe({
  key: e,
  slots: t,
  targets: n
}, r) {
  return t[e] ? (...o) => n ? n.map((i, s) => /* @__PURE__ */ se.jsx(l.Fragment, {
    children: En(i, {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }, s)) : /* @__PURE__ */ se.jsx(se.Fragment, {
    children: En(t[e], {
      clone: !0,
      params: o,
      forceClone: !0
    })
  }) : void 0;
}
const ls = (e) => !!e.name;
function Cn(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const ds = yo(({
  slots: e,
  upload: t,
  showUploadList: n,
  progress: r,
  beforeUpload: o,
  customRequest: i,
  previewFile: s,
  isImageUrl: a,
  itemRender: c,
  iconRender: u,
  data: p,
  onChange: f,
  onValueChange: d,
  onRemove: h,
  maxCount: v,
  items: b,
  setSlotParams: m,
  placeholder: x,
  getDropContainer: _,
  children: w,
  ...S
}) => {
  const C = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof n == "object", g = Cn(n), y = e["placeholder.title"] || e["placeholder.description"] || e["placeholder.icon"] || typeof x == "object", E = Cn(x), M = ne(g.showPreviewIcon), k = ne(g.showRemoveIcon), j = ne(g.showDownloadIcon), I = ne(o), P = ne(i), A = ne(r == null ? void 0 : r.format), R = ne(s), D = ne(a), ee = ne(c), Q = ne(u), ce = ne(x, !0), U = ne(_), z = ne(p), N = me(!1), [B, X] = Ft(b);
  be(() => {
    X(b);
  }, [b]);
  const re = We(() => (B == null ? void 0 : B.map(($) => ls($) ? $ : {
    ...$,
    name: $.orig_name || $.path,
    uid: $.uid || $.url || $.path,
    status: "done"
  })) || [], [B]), ge = ts(w);
  return /* @__PURE__ */ se.jsxs(se.Fragment, {
    children: [/* @__PURE__ */ se.jsx("div", {
      style: {
        display: "none"
      },
      children: ge.length > 0 ? null : w
    }), /* @__PURE__ */ se.jsx(rr, {
      ...S,
      getDropContainer: U,
      placeholder: e.placeholder ? fe({
        slots: e,
        setSlotParams: m,
        key: "placeholder"
      }) : y ? (...$) => {
        var te, K, H;
        return {
          ...E,
          icon: e["placeholder.icon"] ? (te = fe({
            slots: e,
            setSlotParams: m,
            key: "placeholder.icon"
          })) == null ? void 0 : te(...$) : E.icon,
          title: e["placeholder.title"] ? (K = fe({
            slots: e,
            setSlotParams: m,
            key: "placeholder.title"
          })) == null ? void 0 : K(...$) : E.title,
          description: e["placeholder.description"] ? (H = fe({
            slots: e,
            setSlotParams: m,
            key: "placeholder.description"
          })) == null ? void 0 : H(...$) : E.description
        };
      } : ce || x,
      items: re,
      data: z || p,
      previewFile: R,
      isImageUrl: D,
      maxCount: 1,
      itemRender: e.itemRender ? fe({
        slots: e,
        setSlotParams: m,
        key: "itemRender"
      }) : ee,
      iconRender: e.iconRender ? fe({
        slots: e,
        setSlotParams: m,
        key: "iconRender"
      }) : Q,
      onRemove: ($) => {
        if (N.current)
          return;
        h == null || h($);
        const te = re.findIndex((H) => H.uid === $.uid), K = B.slice();
        K.splice(te, 1), d == null || d(K), f == null || f(K.map((H) => H.path));
      },
      onChange: async ($) => {
        const te = $.file, K = $.fileList;
        if (re.find((H) => H.uid === te.uid)) {
          if (N.current)
            return;
          h == null || h(te);
          const H = re.findIndex((Y) => Y.uid === te.uid), oe = B.slice();
          oe.splice(H, 1), d == null || d(oe), f == null || f(oe.map((Y) => Y.path));
        } else {
          if (I && !await I(te, K) || N.current)
            return !1;
          N.current = !0;
          let H = K;
          if (typeof v == "number") {
            const W = v - B.length;
            H = K.slice(0, W < 0 ? 0 : W);
          } else if (v === 1)
            H = K.slice(0, 1);
          else if (H.length === 0)
            return N.current = !1, !1;
          X((W) => [...v === 1 ? [] : W, ...H.map((pe) => ({
            ...pe,
            size: pe.size,
            uid: pe.uid,
            name: pe.name,
            status: "uploading"
          }))]);
          const oe = (await t(H.map((W) => W.originFileObj))).filter((W) => W), Y = v === 1 ? oe : [...B.filter((W) => !oe.some((pe) => pe.uid === W.uid)), ...oe];
          N.current = !1, d == null || d(Y), f == null || f(Y.map((W) => W.path));
        }
      },
      customRequest: P || Ur,
      progress: r && {
        ...r,
        format: A
      },
      showUploadList: C ? {
        ...g,
        showDownloadIcon: j || g.showDownloadIcon,
        showRemoveIcon: k || g.showRemoveIcon,
        showPreviewIcon: M || g.showPreviewIcon,
        downloadIcon: e["showUploadList.downloadIcon"] ? fe({
          slots: e,
          setSlotParams: m,
          key: "showUploadList.downloadIcon"
        }) : g.downloadIcon,
        removeIcon: e["showUploadList.removeIcon"] ? fe({
          slots: e,
          setSlotParams: m,
          key: "showUploadList.removeIcon"
        }) : g.removeIcon,
        previewIcon: e["showUploadList.previewIcon"] ? fe({
          slots: e,
          setSlotParams: m,
          key: "showUploadList.previewIcon"
        }) : g.previewIcon,
        extra: e["showUploadList.extra"] ? fe({
          slots: e,
          setSlotParams: m,
          key: "showUploadList.extra"
        }) : g.extra
      } : n,
      children: ge.length > 0 ? w : void 0
    })]
  });
});
export {
  ds as Attachments,
  ds as default
};
