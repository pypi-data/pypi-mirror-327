import { i as fr, a as Ct, r as dr, b as hr, g as pr, w as Fe, c as ee, d as mr } from "./Index-BDg3GgNK.js";
const p = window.ms_globals.React, v = window.ms_globals.React, ir = window.ms_globals.React.forwardRef, J = window.ms_globals.React.useRef, Tn = window.ms_globals.React.useState, fe = window.ms_globals.React.useEffect, sr = window.ms_globals.React.isValidElement, ar = window.ms_globals.React.useLayoutEffect, cr = window.ms_globals.React.useImperativeHandle, lr = window.ms_globals.React.memo, ur = window.ms_globals.React.useMemo, Ht = window.ms_globals.ReactDOM, xt = window.ms_globals.ReactDOM.createPortal, gr = window.ms_globals.internalContext.useContextPropsContext, vr = window.ms_globals.internalContext.ContextPropsProvider, yr = window.ms_globals.antd.ConfigProvider, Et = window.ms_globals.antd.theme, Rn = window.ms_globals.antd.Button, br = window.ms_globals.antd.Input, Sr = window.ms_globals.antd.Flex, xr = window.ms_globals.antdIcons.CloseOutlined, Cr = window.ms_globals.antdIcons.ClearOutlined, Er = window.ms_globals.antdIcons.ArrowUpOutlined, wr = window.ms_globals.antdIcons.AudioMutedOutlined, _r = window.ms_globals.antdIcons.AudioOutlined, wt = window.ms_globals.antdCssinjs.unit, dt = window.ms_globals.antdCssinjs.token2CSSVar, Vt = window.ms_globals.antdCssinjs.useStyleRegister, Tr = window.ms_globals.antdCssinjs.useCSSVarRegister, Rr = window.ms_globals.antdCssinjs.createTheme, Pr = window.ms_globals.antdCssinjs.useCacheToken;
var Mr = /\s/;
function Or(e) {
  for (var t = e.length; t-- && Mr.test(e.charAt(t)); )
    ;
  return t;
}
var Ar = /^\s+/;
function kr(e) {
  return e && e.slice(0, Or(e) + 1).replace(Ar, "");
}
var Ft = NaN, Lr = /^[-+]0x[0-9a-f]+$/i, Ir = /^0b[01]+$/i, jr = /^0o[0-7]+$/i, Dr = parseInt;
function zt(e) {
  if (typeof e == "number")
    return e;
  if (fr(e))
    return Ft;
  if (Ct(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = Ct(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = kr(e);
  var n = Ir.test(e);
  return n || jr.test(e) ? Dr(e.slice(2), n ? 2 : 8) : Lr.test(e) ? Ft : +e;
}
var ht = function() {
  return dr.Date.now();
}, $r = "Expected a function", Nr = Math.max, Br = Math.min;
function Hr(e, t, n) {
  var o, r, i, s, a, l, c = 0, d = !1, u = !1, f = !0;
  if (typeof e != "function")
    throw new TypeError($r);
  t = zt(t) || 0, Ct(n) && (d = !!n.leading, u = "maxWait" in n, i = u ? Nr(zt(n.maxWait) || 0, t) : i, f = "trailing" in n ? !!n.trailing : f);
  function h(S) {
    var M = o, O = r;
    return o = r = void 0, c = S, s = e.apply(O, M), s;
  }
  function b(S) {
    return c = S, a = setTimeout(x, t), d ? h(S) : s;
  }
  function g(S) {
    var M = S - l, O = S - c, L = t - M;
    return u ? Br(L, i - O) : L;
  }
  function m(S) {
    var M = S - l, O = S - c;
    return l === void 0 || M >= t || M < 0 || u && O >= i;
  }
  function x() {
    var S = ht();
    if (m(S))
      return E(S);
    a = setTimeout(x, g(S));
  }
  function E(S) {
    return a = void 0, f && o ? h(S) : (o = r = void 0, s);
  }
  function T() {
    a !== void 0 && clearTimeout(a), c = 0, o = l = r = a = void 0;
  }
  function y() {
    return a === void 0 ? s : E(ht());
  }
  function R() {
    var S = ht(), M = m(S);
    if (o = arguments, r = this, l = S, M) {
      if (a === void 0)
        return b(l);
      if (u)
        return clearTimeout(a), a = setTimeout(x, t), h(l);
    }
    return a === void 0 && (a = setTimeout(x, t)), s;
  }
  return R.cancel = T, R.flush = y, R;
}
function Vr(e, t) {
  return hr(e, t);
}
var Pn = {
  exports: {}
}, qe = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Fr = v, zr = Symbol.for("react.element"), Xr = Symbol.for("react.fragment"), Ur = Object.prototype.hasOwnProperty, Wr = Fr.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Kr = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function Mn(e, t, n) {
  var o, r = {}, i = null, s = null;
  n !== void 0 && (i = "" + n), t.key !== void 0 && (i = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) Ur.call(t, o) && !Kr.hasOwnProperty(o) && (r[o] = t[o]);
  if (e && e.defaultProps) for (o in t = e.defaultProps, t) r[o] === void 0 && (r[o] = t[o]);
  return {
    $$typeof: zr,
    type: e,
    key: i,
    ref: s,
    props: r,
    _owner: Wr.current
  };
}
qe.Fragment = Xr;
qe.jsx = Mn;
qe.jsxs = Mn;
Pn.exports = qe;
var W = Pn.exports;
const {
  SvelteComponent: Gr,
  assign: Xt,
  binding_callbacks: Ut,
  check_outros: qr,
  children: On,
  claim_element: An,
  claim_space: Qr,
  component_subscribe: Wt,
  compute_slots: Yr,
  create_slot: Zr,
  detach: be,
  element: kn,
  empty: Kt,
  exclude_internal_props: Gt,
  get_all_dirty_from_scope: Jr,
  get_slot_changes: eo,
  group_outros: to,
  init: no,
  insert_hydration: ze,
  safe_not_equal: ro,
  set_custom_element_data: Ln,
  space: oo,
  transition_in: Xe,
  transition_out: _t,
  update_slot_base: io
} = window.__gradio__svelte__internal, {
  beforeUpdate: so,
  getContext: ao,
  onDestroy: co,
  setContext: lo
} = window.__gradio__svelte__internal;
function qt(e) {
  let t, n;
  const o = (
    /*#slots*/
    e[7].default
  ), r = Zr(
    o,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = kn("svelte-slot"), r && r.c(), this.h();
    },
    l(i) {
      t = An(i, "SVELTE-SLOT", {
        class: !0
      });
      var s = On(t);
      r && r.l(s), s.forEach(be), this.h();
    },
    h() {
      Ln(t, "class", "svelte-1rt0kpf");
    },
    m(i, s) {
      ze(i, t, s), r && r.m(t, null), e[9](t), n = !0;
    },
    p(i, s) {
      r && r.p && (!n || s & /*$$scope*/
      64) && io(
        r,
        o,
        i,
        /*$$scope*/
        i[6],
        n ? eo(
          o,
          /*$$scope*/
          i[6],
          s,
          null
        ) : Jr(
          /*$$scope*/
          i[6]
        ),
        null
      );
    },
    i(i) {
      n || (Xe(r, i), n = !0);
    },
    o(i) {
      _t(r, i), n = !1;
    },
    d(i) {
      i && be(t), r && r.d(i), e[9](null);
    }
  };
}
function uo(e) {
  let t, n, o, r, i = (
    /*$$slots*/
    e[4].default && qt(e)
  );
  return {
    c() {
      t = kn("react-portal-target"), n = oo(), i && i.c(), o = Kt(), this.h();
    },
    l(s) {
      t = An(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), On(t).forEach(be), n = Qr(s), i && i.l(s), o = Kt(), this.h();
    },
    h() {
      Ln(t, "class", "svelte-1rt0kpf");
    },
    m(s, a) {
      ze(s, t, a), e[8](t), ze(s, n, a), i && i.m(s, a), ze(s, o, a), r = !0;
    },
    p(s, [a]) {
      /*$$slots*/
      s[4].default ? i ? (i.p(s, a), a & /*$$slots*/
      16 && Xe(i, 1)) : (i = qt(s), i.c(), Xe(i, 1), i.m(o.parentNode, o)) : i && (to(), _t(i, 1, 1, () => {
        i = null;
      }), qr());
    },
    i(s) {
      r || (Xe(i), r = !0);
    },
    o(s) {
      _t(i), r = !1;
    },
    d(s) {
      s && (be(t), be(n), be(o)), e[8](null), i && i.d(s);
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
function fo(e, t, n) {
  let o, r, {
    $$slots: i = {},
    $$scope: s
  } = t;
  const a = Yr(i);
  let {
    svelteInit: l
  } = t;
  const c = Fe(Qt(t)), d = Fe();
  Wt(e, d, (y) => n(0, o = y));
  const u = Fe();
  Wt(e, u, (y) => n(1, r = y));
  const f = [], h = ao("$$ms-gr-react-wrapper"), {
    slotKey: b,
    slotIndex: g,
    subSlotIndex: m
  } = pr() || {}, x = l({
    parent: h,
    props: c,
    target: d,
    slot: u,
    slotKey: b,
    slotIndex: g,
    subSlotIndex: m,
    onDestroy(y) {
      f.push(y);
    }
  });
  lo("$$ms-gr-react-wrapper", x), so(() => {
    c.set(Qt(t));
  }), co(() => {
    f.forEach((y) => y());
  });
  function E(y) {
    Ut[y ? "unshift" : "push"](() => {
      o = y, d.set(o);
    });
  }
  function T(y) {
    Ut[y ? "unshift" : "push"](() => {
      r = y, u.set(r);
    });
  }
  return e.$$set = (y) => {
    n(17, t = Xt(Xt({}, t), Gt(y))), "svelteInit" in y && n(5, l = y.svelteInit), "$$scope" in y && n(6, s = y.$$scope);
  }, t = Gt(t), [o, r, d, u, a, l, s, i, E, T];
}
class ho extends Gr {
  constructor(t) {
    super(), no(this, t, fo, uo, ro, {
      svelteInit: 5
    });
  }
}
const Yt = window.ms_globals.rerender, pt = window.ms_globals.tree;
function po(e, t = {}) {
  function n(o) {
    const r = Fe(), i = new ho({
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
          }, l = s.parent ?? pt;
          return l.nodes = [...l.nodes, a], Yt({
            createPortal: xt,
            node: pt
          }), s.onDestroy(() => {
            l.nodes = l.nodes.filter((c) => c.svelteInstance !== r), Yt({
              createPortal: xt,
              node: pt
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
const mo = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function go(e) {
  return e ? Object.keys(e).reduce((t, n) => {
    const o = e[n];
    return t[n] = vo(n, o), t;
  }, {}) : {};
}
function vo(e, t) {
  return typeof t == "number" && !mo.includes(e) ? t + "px" : t;
}
function Tt(e) {
  const t = [], n = e.cloneNode(!1);
  if (e._reactElement) {
    const r = v.Children.toArray(e._reactElement.props.children).map((i) => {
      if (v.isValidElement(i) && i.props.__slot__) {
        const {
          portals: s,
          clonedElement: a
        } = Tt(i.props.el);
        return v.cloneElement(i, {
          ...i.props,
          el: a,
          children: [...v.Children.toArray(i.props.children), ...s]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(xt(v.cloneElement(e._reactElement, {
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
      useCapture: l
    }) => {
      n.addEventListener(a, s, l);
    });
  });
  const o = Array.from(e.childNodes);
  for (let r = 0; r < o.length; r++) {
    const i = o[r];
    if (i.nodeType === 1) {
      const {
        clonedElement: s,
        portals: a
      } = Tt(i);
      t.push(...a), n.appendChild(s);
    } else i.nodeType === 3 && n.appendChild(i.cloneNode());
  }
  return {
    clonedElement: n,
    portals: t
  };
}
function yo(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const We = ir(({
  slot: e,
  clone: t,
  className: n,
  style: o,
  observeAttributes: r
}, i) => {
  const s = J(), [a, l] = Tn([]), {
    forceClone: c
  } = gr(), d = c ? !0 : t;
  return fe(() => {
    var g;
    if (!s.current || !e)
      return;
    let u = e;
    function f() {
      let m = u;
      if (u.tagName.toLowerCase() === "svelte-slot" && u.children.length === 1 && u.children[0] && (m = u.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), yo(i, m), n && m.classList.add(...n.split(" ")), o) {
        const x = go(o);
        Object.keys(x).forEach((E) => {
          m.style[E] = x[E];
        });
      }
    }
    let h = null, b = null;
    if (d && window.MutationObserver) {
      let m = function() {
        var y, R, S;
        (y = s.current) != null && y.contains(u) && ((R = s.current) == null || R.removeChild(u));
        const {
          portals: E,
          clonedElement: T
        } = Tt(e);
        u = T, l(E), u.style.display = "contents", b && clearTimeout(b), b = setTimeout(() => {
          f();
        }, 50), (S = s.current) == null || S.appendChild(u);
      };
      m();
      const x = Hr(() => {
        m(), h == null || h.disconnect(), h == null || h.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      h = new window.MutationObserver(x), h.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      u.style.display = "contents", f(), (g = s.current) == null || g.appendChild(u);
    return () => {
      var m, x;
      u.style.display = "", (m = s.current) != null && m.contains(u) && ((x = s.current) == null || x.removeChild(u)), h == null || h.disconnect();
    };
  }, [e, d, n, o, i, r]), v.createElement("react-child", {
    ref: s,
    style: {
      display: "contents"
    }
  }, ...a);
}), bo = "1.0.5", So = /* @__PURE__ */ v.createContext({}), xo = {
  classNames: {},
  styles: {},
  className: "",
  style: {}
}, Co = (e) => {
  const t = v.useContext(So);
  return v.useMemo(() => ({
    ...xo,
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
function Rt() {
  const {
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o,
    theme: r
  } = v.useContext(yr.ConfigContext);
  return {
    theme: r,
    getPrefixCls: e,
    direction: t,
    csp: n,
    iconPrefixCls: o
  };
}
function he(e) {
  var t = p.useRef();
  t.current = e;
  var n = p.useCallback(function() {
    for (var o, r = arguments.length, i = new Array(r), s = 0; s < r; s++)
      i[s] = arguments[s];
    return (o = t.current) === null || o === void 0 ? void 0 : o.call.apply(o, [t].concat(i));
  }, []);
  return n;
}
function Eo(e) {
  if (Array.isArray(e)) return e;
}
function wo(e, t) {
  var n = e == null ? null : typeof Symbol < "u" && e[Symbol.iterator] || e["@@iterator"];
  if (n != null) {
    var o, r, i, s, a = [], l = !0, c = !1;
    try {
      if (i = (n = n.call(e)).next, t === 0) {
        if (Object(n) !== n) return;
        l = !1;
      } else for (; !(l = (o = i.call(n)).done) && (a.push(o.value), a.length !== t); l = !0) ;
    } catch (d) {
      c = !0, r = d;
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
function Zt(e, t) {
  (t == null || t > e.length) && (t = e.length);
  for (var n = 0, o = Array(t); n < t; n++) o[n] = e[n];
  return o;
}
function _o(e, t) {
  if (e) {
    if (typeof e == "string") return Zt(e, t);
    var n = {}.toString.call(e).slice(8, -1);
    return n === "Object" && e.constructor && (n = e.constructor.name), n === "Map" || n === "Set" ? Array.from(e) : n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? Zt(e, t) : void 0;
  }
}
function To() {
  throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`);
}
function X(e, t) {
  return Eo(e) || wo(e, t) || _o(e, t) || To();
}
function Qe() {
  return !!(typeof window < "u" && window.document && window.document.createElement);
}
var Jt = Qe() ? p.useLayoutEffect : p.useEffect, Ro = function(t, n) {
  var o = p.useRef(!0);
  Jt(function() {
    return t(o.current);
  }, n), Jt(function() {
    return o.current = !1, function() {
      o.current = !0;
    };
  }, []);
}, en = function(t, n) {
  Ro(function(o) {
    if (!o)
      return t();
  }, n);
};
function Ae(e) {
  var t = p.useRef(!1), n = p.useState(e), o = X(n, 2), r = o[0], i = o[1];
  p.useEffect(function() {
    return t.current = !1, function() {
      t.current = !0;
    };
  }, []);
  function s(a, l) {
    l && t.current || i(a);
  }
  return [r, s];
}
function mt(e) {
  return e !== void 0;
}
function In(e, t) {
  var n = t || {}, o = n.defaultValue, r = n.value, i = n.onChange, s = n.postState, a = Ae(function() {
    return mt(r) ? r : mt(o) ? typeof o == "function" ? o() : o : typeof e == "function" ? e() : e;
  }), l = X(a, 2), c = l[0], d = l[1], u = r !== void 0 ? r : c, f = s ? s(u) : u, h = he(i), b = Ae([u]), g = X(b, 2), m = g[0], x = g[1];
  en(function() {
    var T = m[0];
    c !== T && h(c, T);
  }, [m]), en(function() {
    mt(r) || d(r);
  }, [r]);
  var E = he(function(T, y) {
    d(T, y), x([u], y);
  });
  return [f, E];
}
function z(e) {
  "@babel/helpers - typeof";
  return z = typeof Symbol == "function" && typeof Symbol.iterator == "symbol" ? function(t) {
    return typeof t;
  } : function(t) {
    return t && typeof Symbol == "function" && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t;
  }, z(e);
}
var jn = {
  exports: {}
}, A = {};
/**
 * @license React
 * react-is.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var jt = Symbol.for("react.element"), Dt = Symbol.for("react.portal"), Ye = Symbol.for("react.fragment"), Ze = Symbol.for("react.strict_mode"), Je = Symbol.for("react.profiler"), et = Symbol.for("react.provider"), tt = Symbol.for("react.context"), Po = Symbol.for("react.server_context"), nt = Symbol.for("react.forward_ref"), rt = Symbol.for("react.suspense"), ot = Symbol.for("react.suspense_list"), it = Symbol.for("react.memo"), st = Symbol.for("react.lazy"), Mo = Symbol.for("react.offscreen"), Dn;
Dn = Symbol.for("react.module.reference");
function K(e) {
  if (typeof e == "object" && e !== null) {
    var t = e.$$typeof;
    switch (t) {
      case jt:
        switch (e = e.type, e) {
          case Ye:
          case Je:
          case Ze:
          case rt:
          case ot:
            return e;
          default:
            switch (e = e && e.$$typeof, e) {
              case Po:
              case tt:
              case nt:
              case st:
              case it:
              case et:
                return e;
              default:
                return t;
            }
        }
      case Dt:
        return t;
    }
  }
}
A.ContextConsumer = tt;
A.ContextProvider = et;
A.Element = jt;
A.ForwardRef = nt;
A.Fragment = Ye;
A.Lazy = st;
A.Memo = it;
A.Portal = Dt;
A.Profiler = Je;
A.StrictMode = Ze;
A.Suspense = rt;
A.SuspenseList = ot;
A.isAsyncMode = function() {
  return !1;
};
A.isConcurrentMode = function() {
  return !1;
};
A.isContextConsumer = function(e) {
  return K(e) === tt;
};
A.isContextProvider = function(e) {
  return K(e) === et;
};
A.isElement = function(e) {
  return typeof e == "object" && e !== null && e.$$typeof === jt;
};
A.isForwardRef = function(e) {
  return K(e) === nt;
};
A.isFragment = function(e) {
  return K(e) === Ye;
};
A.isLazy = function(e) {
  return K(e) === st;
};
A.isMemo = function(e) {
  return K(e) === it;
};
A.isPortal = function(e) {
  return K(e) === Dt;
};
A.isProfiler = function(e) {
  return K(e) === Je;
};
A.isStrictMode = function(e) {
  return K(e) === Ze;
};
A.isSuspense = function(e) {
  return K(e) === rt;
};
A.isSuspenseList = function(e) {
  return K(e) === ot;
};
A.isValidElementType = function(e) {
  return typeof e == "string" || typeof e == "function" || e === Ye || e === Je || e === Ze || e === rt || e === ot || e === Mo || typeof e == "object" && e !== null && (e.$$typeof === st || e.$$typeof === it || e.$$typeof === et || e.$$typeof === tt || e.$$typeof === nt || e.$$typeof === Dn || e.getModuleId !== void 0);
};
A.typeOf = K;
jn.exports = A;
var gt = jn.exports, Oo = Symbol.for("react.element"), Ao = Symbol.for("react.transitional.element"), ko = Symbol.for("react.fragment");
function Lo(e) {
  return (
    // Base object type
    e && z(e) === "object" && // React Element type
    (e.$$typeof === Oo || e.$$typeof === Ao) && // React Fragment type
    e.type === ko
  );
}
var Io = function(t, n) {
  typeof t == "function" ? t(n) : z(t) === "object" && t && "current" in t && (t.current = n);
}, jo = function(t) {
  var n, o;
  if (!t)
    return !1;
  if ($n(t) && t.props.propertyIsEnumerable("ref"))
    return !0;
  var r = gt.isMemo(t) ? t.type.type : t.type;
  return !(typeof r == "function" && !((n = r.prototype) !== null && n !== void 0 && n.render) && r.$$typeof !== gt.ForwardRef || typeof t == "function" && !((o = t.prototype) !== null && o !== void 0 && o.render) && t.$$typeof !== gt.ForwardRef);
};
function $n(e) {
  return /* @__PURE__ */ sr(e) && !Lo(e);
}
var Do = function(t) {
  if (t && $n(t)) {
    var n = t;
    return n.props.propertyIsEnumerable("ref") ? n.props.ref : n.ref;
  }
  return null;
};
function $o(e, t) {
  for (var n = e, o = 0; o < t.length; o += 1) {
    if (n == null)
      return;
    n = n[t[o]];
  }
  return n;
}
function No(e, t) {
  if (z(e) != "object" || !e) return e;
  var n = e[Symbol.toPrimitive];
  if (n !== void 0) {
    var o = n.call(e, t || "default");
    if (z(o) != "object") return o;
    throw new TypeError("@@toPrimitive must return a primitive value.");
  }
  return (t === "string" ? String : Number)(e);
}
function Nn(e) {
  var t = No(e, "string");
  return z(t) == "symbol" ? t : t + "";
}
function _(e, t, n) {
  return (t = Nn(t)) in e ? Object.defineProperty(e, t, {
    value: n,
    enumerable: !0,
    configurable: !0,
    writable: !0
  }) : e[t] = n, e;
}
function tn(e, t) {
  var n = Object.keys(e);
  if (Object.getOwnPropertySymbols) {
    var o = Object.getOwnPropertySymbols(e);
    t && (o = o.filter(function(r) {
      return Object.getOwnPropertyDescriptor(e, r).enumerable;
    })), n.push.apply(n, o);
  }
  return n;
}
function w(e) {
  for (var t = 1; t < arguments.length; t++) {
    var n = arguments[t] != null ? arguments[t] : {};
    t % 2 ? tn(Object(n), !0).forEach(function(o) {
      _(e, o, n[o]);
    }) : Object.getOwnPropertyDescriptors ? Object.defineProperties(e, Object.getOwnPropertyDescriptors(n)) : tn(Object(n)).forEach(function(o) {
      Object.defineProperty(e, o, Object.getOwnPropertyDescriptor(n, o));
    });
  }
  return e;
}
function nn(e) {
  return e instanceof HTMLElement || e instanceof SVGElement;
}
function Bo(e) {
  return e && z(e) === "object" && nn(e.nativeElement) ? e.nativeElement : nn(e) ? e : null;
}
function Ho(e) {
  var t = Bo(e);
  if (t)
    return t;
  if (e instanceof v.Component) {
    var n;
    return (n = Ht.findDOMNode) === null || n === void 0 ? void 0 : n.call(Ht, e);
  }
  return null;
}
function Vo(e, t) {
  if (e == null) return {};
  var n = {};
  for (var o in e) if ({}.hasOwnProperty.call(e, o)) {
    if (t.includes(o)) continue;
    n[o] = e[o];
  }
  return n;
}
function rn(e, t) {
  if (e == null) return {};
  var n, o, r = Vo(e, t);
  if (Object.getOwnPropertySymbols) {
    var i = Object.getOwnPropertySymbols(e);
    for (o = 0; o < i.length; o++) n = i[o], t.includes(n) || {}.propertyIsEnumerable.call(e, n) && (r[n] = e[n]);
  }
  return r;
}
var Fo = /* @__PURE__ */ p.createContext({});
function Ce(e, t) {
  if (!(e instanceof t)) throw new TypeError("Cannot call a class as a function");
}
function on(e, t) {
  for (var n = 0; n < t.length; n++) {
    var o = t[n];
    o.enumerable = o.enumerable || !1, o.configurable = !0, "value" in o && (o.writable = !0), Object.defineProperty(e, Nn(o.key), o);
  }
}
function Ee(e, t, n) {
  return t && on(e.prototype, t), n && on(e, n), Object.defineProperty(e, "prototype", {
    writable: !1
  }), e;
}
function Pt(e, t) {
  return Pt = Object.setPrototypeOf ? Object.setPrototypeOf.bind() : function(n, o) {
    return n.__proto__ = o, n;
  }, Pt(e, t);
}
function at(e, t) {
  if (typeof t != "function" && t !== null) throw new TypeError("Super expression must either be null or a function");
  e.prototype = Object.create(t && t.prototype, {
    constructor: {
      value: e,
      writable: !0,
      configurable: !0
    }
  }), Object.defineProperty(e, "prototype", {
    writable: !1
  }), t && Pt(e, t);
}
function Ke(e) {
  return Ke = Object.setPrototypeOf ? Object.getPrototypeOf.bind() : function(t) {
    return t.__proto__ || Object.getPrototypeOf(t);
  }, Ke(e);
}
function Bn() {
  try {
    var e = !Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], function() {
    }));
  } catch {
  }
  return (Bn = function() {
    return !!e;
  })();
}
function de(e) {
  if (e === void 0) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
  return e;
}
function zo(e, t) {
  if (t && (z(t) == "object" || typeof t == "function")) return t;
  if (t !== void 0) throw new TypeError("Derived constructors may only return object or undefined");
  return de(e);
}
function ct(e) {
  var t = Bn();
  return function() {
    var n, o = Ke(e);
    if (t) {
      var r = Ke(this).constructor;
      n = Reflect.construct(o, arguments, r);
    } else n = o.apply(this, arguments);
    return zo(this, n);
  };
}
var Xo = /* @__PURE__ */ function(e) {
  at(n, e);
  var t = ct(n);
  function n() {
    return Ce(this, n), t.apply(this, arguments);
  }
  return Ee(n, [{
    key: "render",
    value: function() {
      return this.props.children;
    }
  }]), n;
}(p.Component);
function Uo(e) {
  var t = p.useReducer(function(a) {
    return a + 1;
  }, 0), n = X(t, 2), o = n[1], r = p.useRef(e), i = he(function() {
    return r.current;
  }), s = he(function(a) {
    r.current = typeof a == "function" ? a(r.current) : a, o();
  });
  return [i, s];
}
var ue = "none", je = "appear", De = "enter", $e = "leave", sn = "none", q = "prepare", Se = "start", xe = "active", $t = "end", Hn = "prepared";
function an(e, t) {
  var n = {};
  return n[e.toLowerCase()] = t.toLowerCase(), n["Webkit".concat(e)] = "webkit".concat(t), n["Moz".concat(e)] = "moz".concat(t), n["ms".concat(e)] = "MS".concat(t), n["O".concat(e)] = "o".concat(t.toLowerCase()), n;
}
function Wo(e, t) {
  var n = {
    animationend: an("Animation", "AnimationEnd"),
    transitionend: an("Transition", "TransitionEnd")
  };
  return e && ("AnimationEvent" in t || delete n.animationend.animation, "TransitionEvent" in t || delete n.transitionend.transition), n;
}
var Ko = Wo(Qe(), typeof window < "u" ? window : {}), Vn = {};
if (Qe()) {
  var Go = document.createElement("div");
  Vn = Go.style;
}
var Ne = {};
function Fn(e) {
  if (Ne[e])
    return Ne[e];
  var t = Ko[e];
  if (t)
    for (var n = Object.keys(t), o = n.length, r = 0; r < o; r += 1) {
      var i = n[r];
      if (Object.prototype.hasOwnProperty.call(t, i) && i in Vn)
        return Ne[e] = t[i], Ne[e];
    }
  return "";
}
var zn = Fn("animationend"), Xn = Fn("transitionend"), Un = !!(zn && Xn), cn = zn || "animationend", ln = Xn || "transitionend";
function un(e, t) {
  if (!e) return null;
  if (z(e) === "object") {
    var n = t.replace(/-\w/g, function(o) {
      return o[1].toUpperCase();
    });
    return e[n];
  }
  return "".concat(e, "-").concat(t);
}
const qo = function(e) {
  var t = J();
  function n(r) {
    r && (r.removeEventListener(ln, e), r.removeEventListener(cn, e));
  }
  function o(r) {
    t.current && t.current !== r && n(t.current), r && r !== t.current && (r.addEventListener(ln, e), r.addEventListener(cn, e), t.current = r);
  }
  return p.useEffect(function() {
    return function() {
      n(t.current);
    };
  }, []), [o, n];
};
var Wn = Qe() ? ar : fe, Kn = function(t) {
  return +setTimeout(t, 16);
}, Gn = function(t) {
  return clearTimeout(t);
};
typeof window < "u" && "requestAnimationFrame" in window && (Kn = function(t) {
  return window.requestAnimationFrame(t);
}, Gn = function(t) {
  return window.cancelAnimationFrame(t);
});
var fn = 0, Nt = /* @__PURE__ */ new Map();
function qn(e) {
  Nt.delete(e);
}
var Mt = function(t) {
  var n = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 1;
  fn += 1;
  var o = fn;
  function r(i) {
    if (i === 0)
      qn(o), t();
    else {
      var s = Kn(function() {
        r(i - 1);
      });
      Nt.set(o, s);
    }
  }
  return r(n), o;
};
Mt.cancel = function(e) {
  var t = Nt.get(e);
  return qn(e), Gn(t);
};
const Qo = function() {
  var e = p.useRef(null);
  function t() {
    Mt.cancel(e.current);
  }
  function n(o) {
    var r = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 2;
    t();
    var i = Mt(function() {
      r <= 1 ? o({
        isCanceled: function() {
          return i !== e.current;
        }
      }) : n(o, r - 1);
    });
    e.current = i;
  }
  return p.useEffect(function() {
    return function() {
      t();
    };
  }, []), [n, t];
};
var Yo = [q, Se, xe, $t], Zo = [q, Hn], Qn = !1, Jo = !0;
function Yn(e) {
  return e === xe || e === $t;
}
const ei = function(e, t, n) {
  var o = Ae(sn), r = X(o, 2), i = r[0], s = r[1], a = Qo(), l = X(a, 2), c = l[0], d = l[1];
  function u() {
    s(q, !0);
  }
  var f = t ? Zo : Yo;
  return Wn(function() {
    if (i !== sn && i !== $t) {
      var h = f.indexOf(i), b = f[h + 1], g = n(i);
      g === Qn ? s(b, !0) : b && c(function(m) {
        function x() {
          m.isCanceled() || s(b, !0);
        }
        g === !0 ? x() : Promise.resolve(g).then(x);
      });
    }
  }, [e, i]), p.useEffect(function() {
    return function() {
      d();
    };
  }, []), [u, i];
};
function ti(e, t, n, o) {
  var r = o.motionEnter, i = r === void 0 ? !0 : r, s = o.motionAppear, a = s === void 0 ? !0 : s, l = o.motionLeave, c = l === void 0 ? !0 : l, d = o.motionDeadline, u = o.motionLeaveImmediately, f = o.onAppearPrepare, h = o.onEnterPrepare, b = o.onLeavePrepare, g = o.onAppearStart, m = o.onEnterStart, x = o.onLeaveStart, E = o.onAppearActive, T = o.onEnterActive, y = o.onLeaveActive, R = o.onAppearEnd, S = o.onEnterEnd, M = o.onLeaveEnd, O = o.onVisibleChanged, L = Ae(), B = X(L, 2), $ = B[0], k = B[1], P = Uo(ue), I = X(P, 2), j = I[0], N = I[1], Q = Ae(null), Y = X(Q, 2), pe = Y[0], me = Y[1], U = j(), te = J(!1), ae = J(null);
  function H() {
    return n();
  }
  var ne = J(!1);
  function ce() {
    N(ue), me(null, !0);
  }
  var G = he(function(V) {
    var C = j();
    if (C !== ue) {
      var D = H();
      if (!(V && !V.deadline && V.target !== D)) {
        var Z = ne.current, Ie;
        C === je && Z ? Ie = R == null ? void 0 : R(D, V) : C === De && Z ? Ie = S == null ? void 0 : S(D, V) : C === $e && Z && (Ie = M == null ? void 0 : M(D, V)), Z && Ie !== !1 && ce();
      }
    }
  }), ge = qo(G), ve = X(ge, 1), ye = ve[0], we = function(C) {
    switch (C) {
      case je:
        return _(_(_({}, q, f), Se, g), xe, E);
      case De:
        return _(_(_({}, q, h), Se, m), xe, T);
      case $e:
        return _(_(_({}, q, b), Se, x), xe, y);
      default:
        return {};
    }
  }, re = p.useMemo(function() {
    return we(U);
  }, [U]), le = ei(U, !e, function(V) {
    if (V === q) {
      var C = re[q];
      return C ? C(H()) : Qn;
    }
    if (oe in re) {
      var D;
      me(((D = re[oe]) === null || D === void 0 ? void 0 : D.call(re, H(), null)) || null);
    }
    return oe === xe && U !== ue && (ye(H()), d > 0 && (clearTimeout(ae.current), ae.current = setTimeout(function() {
      G({
        deadline: !0
      });
    }, d))), oe === Hn && ce(), Jo;
  }), ke = X(le, 2), _e = ke[0], oe = ke[1], ft = Yn(oe);
  ne.current = ft;
  var Le = J(null);
  Wn(function() {
    if (!(te.current && Le.current === t)) {
      k(t);
      var V = te.current;
      te.current = !0;
      var C;
      !V && t && a && (C = je), V && t && i && (C = De), (V && !t && c || !V && u && !t && c) && (C = $e);
      var D = we(C);
      C && (e || D[q]) ? (N(C), _e()) : N(ue), Le.current = t;
    }
  }, [t]), fe(function() {
    // Cancel appear
    (U === je && !a || // Cancel enter
    U === De && !i || // Cancel leave
    U === $e && !c) && N(ue);
  }, [a, i, c]), fe(function() {
    return function() {
      te.current = !1, clearTimeout(ae.current);
    };
  }, []);
  var Te = p.useRef(!1);
  fe(function() {
    $ && (Te.current = !0), $ !== void 0 && U === ue && ((Te.current || $) && (O == null || O($)), Te.current = !0);
  }, [$, U]);
  var Re = pe;
  return re[q] && oe === Se && (Re = w({
    transition: "none"
  }, Re)), [U, oe, Re, $ ?? t];
}
function ni(e) {
  var t = e;
  z(e) === "object" && (t = e.transitionSupport);
  function n(r, i) {
    return !!(r.motionName && t && i !== !1);
  }
  var o = /* @__PURE__ */ p.forwardRef(function(r, i) {
    var s = r.visible, a = s === void 0 ? !0 : s, l = r.removeOnLeave, c = l === void 0 ? !0 : l, d = r.forceRender, u = r.children, f = r.motionName, h = r.leavedClassName, b = r.eventProps, g = p.useContext(Fo), m = g.motion, x = n(r, m), E = J(), T = J();
    function y() {
      try {
        return E.current instanceof HTMLElement ? E.current : Ho(T.current);
      } catch {
        return null;
      }
    }
    var R = ti(x, a, y, r), S = X(R, 4), M = S[0], O = S[1], L = S[2], B = S[3], $ = p.useRef(B);
    B && ($.current = !0);
    var k = p.useCallback(function(Y) {
      E.current = Y, Io(i, Y);
    }, [i]), P, I = w(w({}, b), {}, {
      visible: a
    });
    if (!u)
      P = null;
    else if (M === ue)
      B ? P = u(w({}, I), k) : !c && $.current && h ? P = u(w(w({}, I), {}, {
        className: h
      }), k) : d || !c && !h ? P = u(w(w({}, I), {}, {
        style: {
          display: "none"
        }
      }), k) : P = null;
    else {
      var j;
      O === q ? j = "prepare" : Yn(O) ? j = "active" : O === Se && (j = "start");
      var N = un(f, "".concat(M, "-").concat(j));
      P = u(w(w({}, I), {}, {
        className: ee(un(f, M), _(_({}, N, N && j), f, typeof f == "string")),
        style: L
      }), k);
    }
    if (/* @__PURE__ */ p.isValidElement(P) && jo(P)) {
      var Q = Do(P);
      Q || (P = /* @__PURE__ */ p.cloneElement(P, {
        ref: k
      }));
    }
    return /* @__PURE__ */ p.createElement(Xo, {
      ref: T
    }, P);
  });
  return o.displayName = "CSSMotion", o;
}
const Zn = ni(Un);
var Ot = "add", At = "keep", kt = "remove", vt = "removed";
function ri(e) {
  var t;
  return e && z(e) === "object" && "key" in e ? t = e : t = {
    key: e
  }, w(w({}, t), {}, {
    key: String(t.key)
  });
}
function Lt() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [];
  return e.map(ri);
}
function oi() {
  var e = arguments.length > 0 && arguments[0] !== void 0 ? arguments[0] : [], t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : [], n = [], o = 0, r = t.length, i = Lt(e), s = Lt(t);
  i.forEach(function(c) {
    for (var d = !1, u = o; u < r; u += 1) {
      var f = s[u];
      if (f.key === c.key) {
        o < u && (n = n.concat(s.slice(o, u).map(function(h) {
          return w(w({}, h), {}, {
            status: Ot
          });
        })), o = u), n.push(w(w({}, f), {}, {
          status: At
        })), o += 1, d = !0;
        break;
      }
    }
    d || n.push(w(w({}, c), {}, {
      status: kt
    }));
  }), o < r && (n = n.concat(s.slice(o).map(function(c) {
    return w(w({}, c), {}, {
      status: Ot
    });
  })));
  var a = {};
  n.forEach(function(c) {
    var d = c.key;
    a[d] = (a[d] || 0) + 1;
  });
  var l = Object.keys(a).filter(function(c) {
    return a[c] > 1;
  });
  return l.forEach(function(c) {
    n = n.filter(function(d) {
      var u = d.key, f = d.status;
      return u !== c || f !== kt;
    }), n.forEach(function(d) {
      d.key === c && (d.status = At);
    });
  }), n;
}
var ii = ["component", "children", "onVisibleChanged", "onAllRemoved"], si = ["status"], ai = ["eventProps", "visible", "children", "motionName", "motionAppear", "motionEnter", "motionLeave", "motionLeaveImmediately", "motionDeadline", "removeOnLeave", "leavedClassName", "onAppearPrepare", "onAppearStart", "onAppearActive", "onAppearEnd", "onEnterStart", "onEnterActive", "onEnterEnd", "onLeaveStart", "onLeaveActive", "onLeaveEnd"];
function ci(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : Zn, n = /* @__PURE__ */ function(o) {
    at(i, o);
    var r = ct(i);
    function i() {
      var s;
      Ce(this, i);
      for (var a = arguments.length, l = new Array(a), c = 0; c < a; c++)
        l[c] = arguments[c];
      return s = r.call.apply(r, [this].concat(l)), _(de(s), "state", {
        keyEntities: []
      }), _(de(s), "removeKey", function(d) {
        s.setState(function(u) {
          var f = u.keyEntities.map(function(h) {
            return h.key !== d ? h : w(w({}, h), {}, {
              status: vt
            });
          });
          return {
            keyEntities: f
          };
        }, function() {
          var u = s.state.keyEntities, f = u.filter(function(h) {
            var b = h.status;
            return b !== vt;
          }).length;
          f === 0 && s.props.onAllRemoved && s.props.onAllRemoved();
        });
      }), s;
    }
    return Ee(i, [{
      key: "render",
      value: function() {
        var a = this, l = this.state.keyEntities, c = this.props, d = c.component, u = c.children, f = c.onVisibleChanged;
        c.onAllRemoved;
        var h = rn(c, ii), b = d || p.Fragment, g = {};
        return ai.forEach(function(m) {
          g[m] = h[m], delete h[m];
        }), delete h.keys, /* @__PURE__ */ p.createElement(b, h, l.map(function(m, x) {
          var E = m.status, T = rn(m, si), y = E === Ot || E === At;
          return /* @__PURE__ */ p.createElement(t, se({}, g, {
            key: T.key,
            visible: y,
            eventProps: T,
            onVisibleChanged: function(S) {
              f == null || f(S, {
                key: T.key
              }), S || a.removeKey(T.key);
            }
          }), function(R, S) {
            return u(w(w({}, R), {}, {
              index: x
            }), S);
          });
        }));
      }
    }], [{
      key: "getDerivedStateFromProps",
      value: function(a, l) {
        var c = a.keys, d = l.keyEntities, u = Lt(c), f = oi(d, u);
        return {
          keyEntities: f.filter(function(h) {
            var b = d.find(function(g) {
              var m = g.key;
              return h.key === m;
            });
            return !(b && b.status === vt && h.status === kt);
          })
        };
      }
    }]), i;
  }(p.Component);
  return _(n, "defaultProps", {
    component: "div"
  }), n;
}
ci(Un);
var Jn = /* @__PURE__ */ Ee(function e() {
  Ce(this, e);
}), er = "CALC_UNIT", li = new RegExp(er, "g");
function yt(e) {
  return typeof e == "number" ? "".concat(e).concat(er) : e;
}
var ui = /* @__PURE__ */ function(e) {
  at(n, e);
  var t = ct(n);
  function n(o, r) {
    var i;
    Ce(this, n), i = t.call(this), _(de(i), "result", ""), _(de(i), "unitlessCssVar", void 0), _(de(i), "lowPriority", void 0);
    var s = z(o);
    return i.unitlessCssVar = r, o instanceof n ? i.result = "(".concat(o.result, ")") : s === "number" ? i.result = yt(o) : s === "string" && (i.result = o), i;
  }
  return Ee(n, [{
    key: "add",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " + ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " + ").concat(yt(r))), this.lowPriority = !0, this;
    }
  }, {
    key: "sub",
    value: function(r) {
      return r instanceof n ? this.result = "".concat(this.result, " - ").concat(r.getResult()) : (typeof r == "number" || typeof r == "string") && (this.result = "".concat(this.result, " - ").concat(yt(r))), this.lowPriority = !0, this;
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
      }) && (l = !1), this.result = this.result.replace(li, l ? "px" : ""), typeof this.lowPriority < "u" ? "calc(".concat(this.result, ")") : this.result;
    }
  }]), n;
}(Jn), fi = /* @__PURE__ */ function(e) {
  at(n, e);
  var t = ct(n);
  function n(o) {
    var r;
    return Ce(this, n), r = t.call(this), _(de(r), "result", 0), o instanceof n ? r.result = o.result : typeof o == "number" && (r.result = o), r;
  }
  return Ee(n, [{
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
}(Jn), di = function(t, n) {
  var o = t === "css" ? ui : fi;
  return function(r) {
    return new o(r, n);
  };
}, dn = function(t, n) {
  return "".concat([n, t.replace(/([A-Z]+)([A-Z][a-z]+)/g, "$1-$2").replace(/([a-z])([A-Z])/g, "$1-$2")].filter(Boolean).join("-"));
};
function hn(e, t, n, o) {
  var r = w({}, t[e]);
  if (o != null && o.deprecatedTokens) {
    var i = o.deprecatedTokens;
    i.forEach(function(a) {
      var l = X(a, 2), c = l[0], d = l[1];
      if (r != null && r[c] || r != null && r[d]) {
        var u;
        (u = r[d]) !== null && u !== void 0 || (r[d] = r == null ? void 0 : r[c]);
      }
    });
  }
  var s = w(w({}, n), r);
  return Object.keys(s).forEach(function(a) {
    s[a] === t[a] && delete s[a];
  }), s;
}
var tr = typeof CSSINJS_STATISTIC < "u", It = !0;
function Bt() {
  for (var e = arguments.length, t = new Array(e), n = 0; n < e; n++)
    t[n] = arguments[n];
  if (!tr)
    return Object.assign.apply(Object, [{}].concat(t));
  It = !1;
  var o = {};
  return t.forEach(function(r) {
    if (z(r) === "object") {
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
  }), It = !0, o;
}
var pn = {};
function hi() {
}
var pi = function(t) {
  var n, o = t, r = hi;
  return tr && typeof Proxy < "u" && (n = /* @__PURE__ */ new Set(), o = new Proxy(t, {
    get: function(s, a) {
      if (It) {
        var l;
        (l = n) === null || l === void 0 || l.add(a);
      }
      return s[a];
    }
  }), r = function(s, a) {
    var l;
    pn[s] = {
      global: Array.from(n),
      component: w(w({}, (l = pn[s]) === null || l === void 0 ? void 0 : l.component), a)
    };
  }), {
    token: o,
    keys: n,
    flush: r
  };
};
function mn(e, t, n) {
  if (typeof n == "function") {
    var o;
    return n(Bt(t, (o = t[e]) !== null && o !== void 0 ? o : {}));
  }
  return n ?? {};
}
function mi(e) {
  return e === "js" ? {
    max: Math.max,
    min: Math.min
  } : {
    max: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "max(".concat(o.map(function(i) {
        return wt(i);
      }).join(","), ")");
    },
    min: function() {
      for (var n = arguments.length, o = new Array(n), r = 0; r < n; r++)
        o[r] = arguments[r];
      return "min(".concat(o.map(function(i) {
        return wt(i);
      }).join(","), ")");
    }
  };
}
var gi = 1e3 * 60 * 10, vi = /* @__PURE__ */ function() {
  function e() {
    Ce(this, e), _(this, "map", /* @__PURE__ */ new Map()), _(this, "objectIDMap", /* @__PURE__ */ new WeakMap()), _(this, "nextID", 0), _(this, "lastAccessBeat", /* @__PURE__ */ new Map()), _(this, "accessBeat", 0);
  }
  return Ee(e, [{
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
        return i && z(i) === "object" ? "obj_".concat(o.getObjectID(i)) : "".concat(z(i), "_").concat(i);
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
          o - r > gi && (n.map.delete(i), n.lastAccessBeat.delete(i));
        }), this.accessBeat = 0;
      }
    }
  }]), e;
}(), gn = new vi();
function yi(e, t) {
  return v.useMemo(function() {
    var n = gn.get(t);
    if (n)
      return n;
    var o = e();
    return gn.set(t, o), o;
  }, t);
}
var bi = function() {
  return {};
};
function Si(e) {
  var t = e.useCSP, n = t === void 0 ? bi : t, o = e.useToken, r = e.usePrefix, i = e.getResetStyles, s = e.getCommonStyle, a = e.getCompUnitless;
  function l(f, h, b, g) {
    var m = Array.isArray(f) ? f[0] : f;
    function x(O) {
      return "".concat(String(m)).concat(O.slice(0, 1).toUpperCase()).concat(O.slice(1));
    }
    var E = (g == null ? void 0 : g.unitless) || {}, T = typeof a == "function" ? a(f) : {}, y = w(w({}, T), {}, _({}, x("zIndexPopup"), !0));
    Object.keys(E).forEach(function(O) {
      y[x(O)] = E[O];
    });
    var R = w(w({}, g), {}, {
      unitless: y,
      prefixToken: x
    }), S = d(f, h, b, R), M = c(m, b, R);
    return function(O) {
      var L = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : O, B = S(O, L), $ = X(B, 2), k = $[1], P = M(L), I = X(P, 2), j = I[0], N = I[1];
      return [j, k, N];
    };
  }
  function c(f, h, b) {
    var g = b.unitless, m = b.injectStyle, x = m === void 0 ? !0 : m, E = b.prefixToken, T = b.ignore, y = function(M) {
      var O = M.rootCls, L = M.cssVar, B = L === void 0 ? {} : L, $ = o(), k = $.realToken;
      return Tr({
        path: [f],
        prefix: B.prefix,
        key: B.key,
        unitless: g,
        ignore: T,
        token: k,
        scope: O
      }, function() {
        var P = mn(f, k, h), I = hn(f, k, P, {
          deprecatedTokens: b == null ? void 0 : b.deprecatedTokens
        });
        return Object.keys(P).forEach(function(j) {
          I[E(j)] = I[j], delete I[j];
        }), I;
      }), null;
    }, R = function(M) {
      var O = o(), L = O.cssVar;
      return [function(B) {
        return x && L ? /* @__PURE__ */ v.createElement(v.Fragment, null, /* @__PURE__ */ v.createElement(y, {
          rootCls: M,
          cssVar: L,
          component: f
        }), B) : B;
      }, L == null ? void 0 : L.key];
    };
    return R;
  }
  function d(f, h, b) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = Array.isArray(f) ? f : [f, f], x = X(m, 1), E = x[0], T = m.join("-"), y = e.layer || {
      name: "antd"
    };
    return function(R) {
      var S = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : R, M = o(), O = M.theme, L = M.realToken, B = M.hashId, $ = M.token, k = M.cssVar, P = r(), I = P.rootPrefixCls, j = P.iconPrefixCls, N = n(), Q = k ? "css" : "js", Y = yi(function() {
        var H = /* @__PURE__ */ new Set();
        return k && Object.keys(g.unitless || {}).forEach(function(ne) {
          H.add(dt(ne, k.prefix)), H.add(dt(ne, dn(E, k.prefix)));
        }), di(Q, H);
      }, [Q, E, k == null ? void 0 : k.prefix]), pe = mi(Q), me = pe.max, U = pe.min, te = {
        theme: O,
        token: $,
        hashId: B,
        nonce: function() {
          return N.nonce;
        },
        clientOnly: g.clientOnly,
        layer: y,
        // antd is always at top of styles
        order: g.order || -999
      };
      typeof i == "function" && Vt(w(w({}, te), {}, {
        clientOnly: !1,
        path: ["Shared", I]
      }), function() {
        return i($, {
          prefix: {
            rootPrefixCls: I,
            iconPrefixCls: j
          },
          csp: N
        });
      });
      var ae = Vt(w(w({}, te), {}, {
        path: [T, R, j]
      }), function() {
        if (g.injectStyle === !1)
          return [];
        var H = pi($), ne = H.token, ce = H.flush, G = mn(E, L, b), ge = ".".concat(R), ve = hn(E, L, G, {
          deprecatedTokens: g.deprecatedTokens
        });
        k && G && z(G) === "object" && Object.keys(G).forEach(function(le) {
          G[le] = "var(".concat(dt(le, dn(E, k.prefix)), ")");
        });
        var ye = Bt(ne, {
          componentCls: ge,
          prefixCls: R,
          iconCls: ".".concat(j),
          antCls: ".".concat(I),
          calc: Y,
          // @ts-ignore
          max: me,
          // @ts-ignore
          min: U
        }, k ? G : ve), we = h(ye, {
          hashId: B,
          prefixCls: R,
          rootPrefixCls: I,
          iconPrefixCls: j
        });
        ce(E, ve);
        var re = typeof s == "function" ? s(ye, R, S, g.resetFont) : null;
        return [g.resetStyle === !1 ? null : re, we];
      });
      return [ae, B];
    };
  }
  function u(f, h, b) {
    var g = arguments.length > 3 && arguments[3] !== void 0 ? arguments[3] : {}, m = d(f, h, b, w({
      resetStyle: !1,
      // Sub Style should default after root one
      order: -998
    }, g)), x = function(T) {
      var y = T.prefixCls, R = T.rootCls, S = R === void 0 ? y : R;
      return m(y, S), null;
    };
    return x;
  }
  return {
    genStyleHooks: l,
    genSubStyleComponent: u,
    genComponentStyleHook: d
  };
}
const F = Math.round;
function bt(e, t) {
  const n = e.replace(/^[^(]*\((.*)/, "$1").replace(/\).*/, "").match(/\d*\.?\d+%?/g) || [], o = n.map((r) => parseFloat(r));
  for (let r = 0; r < 3; r += 1)
    o[r] = t(o[r] || 0, n[r] || "", r);
  return n[3] ? o[3] = n[3].includes("%") ? o[3] / 100 : o[3] : o[3] = 1, o;
}
const vn = (e, t, n) => n === 0 ? e : e / 100;
function Pe(e, t) {
  const n = t || 255;
  return e > n ? n : e < 0 ? 0 : e;
}
class ie {
  constructor(t) {
    _(this, "isValid", !0), _(this, "r", 0), _(this, "g", 0), _(this, "b", 0), _(this, "a", 1), _(this, "_h", void 0), _(this, "_s", void 0), _(this, "_l", void 0), _(this, "_v", void 0), _(this, "_max", void 0), _(this, "_min", void 0), _(this, "_brightness", void 0);
    function n(o) {
      return o[0] in t && o[1] in t && o[2] in t;
    }
    if (t) if (typeof t == "string") {
      let r = function(i) {
        return o.startsWith(i);
      };
      const o = t.trim();
      /^#?[A-F\d]{3,8}$/i.test(o) ? this.fromHexString(o) : r("rgb") ? this.fromRgbString(o) : r("hsl") ? this.fromHslString(o) : (r("hsv") || r("hsb")) && this.fromHsvString(o);
    } else if (t instanceof ie)
      this.r = t.r, this.g = t.g, this.b = t.b, this.a = t.a, this._h = t._h, this._s = t._s, this._l = t._l, this._v = t._v;
    else if (n("rgb"))
      this.r = Pe(t.r), this.g = Pe(t.g), this.b = Pe(t.b), this.a = typeof t.a == "number" ? Pe(t.a, 1) : 1;
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
      t === 0 ? this._h = 0 : this._h = F(60 * (this.r === this.getMax() ? (this.g - this.b) / t + (this.g < this.b ? 6 : 0) : this.g === this.getMax() ? (this.b - this.r) / t + 2 : (this.r - this.g) / t + 4));
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
      r: F(i("r")),
      g: F(i("g")),
      b: F(i("b")),
      a: F(i("a") * 100) / 100
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
    const n = this._c(t), o = this.a + n.a * (1 - this.a), r = (i) => F((this[i] * this.a + n[i] * n.a * (1 - this.a)) / o);
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
      const i = F(this.a * 255).toString(16);
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
    const t = this.getHue(), n = F(this.getSaturation() * 100), o = F(this.getLightness() * 100);
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
    return r[t] = Pe(n, o), r;
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
      const f = F(o * 255);
      this.r = f, this.g = f, this.b = f;
    }
    let i = 0, s = 0, a = 0;
    const l = t / 60, c = (1 - Math.abs(2 * o - 1)) * n, d = c * (1 - Math.abs(l % 2 - 1));
    l >= 0 && l < 1 ? (i = c, s = d) : l >= 1 && l < 2 ? (i = d, s = c) : l >= 2 && l < 3 ? (s = c, a = d) : l >= 3 && l < 4 ? (s = d, a = c) : l >= 4 && l < 5 ? (i = d, a = c) : l >= 5 && l < 6 && (i = c, a = d);
    const u = o - c / 2;
    this.r = F((i + u) * 255), this.g = F((s + u) * 255), this.b = F((a + u) * 255);
  }
  fromHsv({
    h: t,
    s: n,
    v: o,
    a: r
  }) {
    this._h = t % 360, this._s = n, this._v = o, this.a = typeof r == "number" ? r : 1;
    const i = F(o * 255);
    if (this.r = i, this.g = i, this.b = i, n <= 0)
      return;
    const s = t / 60, a = Math.floor(s), l = s - a, c = F(o * (1 - n) * 255), d = F(o * (1 - n * l) * 255), u = F(o * (1 - n * (1 - l)) * 255);
    switch (a) {
      case 0:
        this.g = u, this.b = c;
        break;
      case 1:
        this.r = d, this.b = c;
        break;
      case 2:
        this.r = c, this.b = u;
        break;
      case 3:
        this.r = c, this.g = d;
        break;
      case 4:
        this.r = u, this.g = c;
        break;
      case 5:
      default:
        this.g = c, this.b = d;
        break;
    }
  }
  fromHsvString(t) {
    const n = bt(t, vn);
    this.fromHsv({
      h: n[0],
      s: n[1],
      v: n[2],
      a: n[3]
    });
  }
  fromHslString(t) {
    const n = bt(t, vn);
    this.fromHsl({
      h: n[0],
      s: n[1],
      l: n[2],
      a: n[3]
    });
  }
  fromRgbString(t) {
    const n = bt(t, (o, r) => (
      // Convert percentage to number. e.g. 50% -> 128
      r.includes("%") ? F(o / 100 * 255) : o
    ));
    this.r = n[0], this.g = n[1], this.b = n[2], this.a = n[3];
  }
}
const xi = {
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
}, Ci = Object.assign(Object.assign({}, xi), {
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
function St(e) {
  return e >= 0 && e <= 255;
}
function Be(e, t) {
  const {
    r: n,
    g: o,
    b: r,
    a: i
  } = new ie(e).toRgb();
  if (i < 1)
    return e;
  const {
    r: s,
    g: a,
    b: l
  } = new ie(t).toRgb();
  for (let c = 0.01; c <= 1; c += 0.01) {
    const d = Math.round((n - s * (1 - c)) / c), u = Math.round((o - a * (1 - c)) / c), f = Math.round((r - l * (1 - c)) / c);
    if (St(d) && St(u) && St(f))
      return new ie({
        r: d,
        g: u,
        b: f,
        a: Math.round(c * 100) / 100
      }).toRgbString();
  }
  return new ie({
    r: n,
    g: o,
    b: r,
    a: 1
  }).toRgbString();
}
var Ei = function(e, t) {
  var n = {};
  for (var o in e) Object.prototype.hasOwnProperty.call(e, o) && t.indexOf(o) < 0 && (n[o] = e[o]);
  if (e != null && typeof Object.getOwnPropertySymbols == "function") for (var r = 0, o = Object.getOwnPropertySymbols(e); r < o.length; r++)
    t.indexOf(o[r]) < 0 && Object.prototype.propertyIsEnumerable.call(e, o[r]) && (n[o[r]] = e[o[r]]);
  return n;
};
function wi(e) {
  const {
    override: t
  } = e, n = Ei(e, ["override"]), o = Object.assign({}, t);
  Object.keys(Ci).forEach((f) => {
    delete o[f];
  });
  const r = Object.assign(Object.assign({}, n), o), i = 480, s = 576, a = 768, l = 992, c = 1200, d = 1600;
  if (r.motion === !1) {
    const f = "0s";
    r.motionDurationFast = f, r.motionDurationMid = f, r.motionDurationSlow = f;
  }
  return Object.assign(Object.assign(Object.assign({}, r), {
    // ============== Background ============== //
    colorFillContent: r.colorFillSecondary,
    colorFillContentHover: r.colorFill,
    colorFillAlter: r.colorFillQuaternary,
    colorBgContainerDisabled: r.colorFillTertiary,
    // ============== Split ============== //
    colorBorderBg: r.colorBgContainer,
    colorSplit: Be(r.colorBorderSecondary, r.colorBgContainer),
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
    colorErrorOutline: Be(r.colorErrorBg, r.colorBgContainer),
    colorWarningOutline: Be(r.colorWarningBg, r.colorBgContainer),
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
    controlOutline: Be(r.colorPrimaryBg, r.colorBgContainer),
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
    screenXLMax: d - 1,
    screenXXL: d,
    screenXXLMin: d,
    boxShadowPopoverArrow: "2px 2px 5px rgba(0, 0, 0, 0.05)",
    boxShadowCard: `
      0 1px 2px -2px ${new ie("rgba(0, 0, 0, 0.16)").toRgbString()},
      0 3px 6px 0 ${new ie("rgba(0, 0, 0, 0.12)").toRgbString()},
      0 5px 12px 4px ${new ie("rgba(0, 0, 0, 0.09)").toRgbString()}
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
const _i = {
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
}, Ti = {
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
}, Ri = Rr(Et.defaultAlgorithm), Pi = {
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
}, nr = (e, t, n) => {
  const o = n.getDerivativeToken(e), {
    override: r,
    ...i
  } = t;
  let s = {
    ...o,
    override: r
  };
  return s = wi(s), i && Object.entries(i).forEach(([a, l]) => {
    const {
      theme: c,
      ...d
    } = l;
    let u = d;
    c && (u = nr({
      ...s,
      ...d
    }, {
      override: d
    }, c)), s[a] = u;
  }), s;
};
function Mi() {
  const {
    token: e,
    hashed: t,
    theme: n = Ri,
    override: o,
    cssVar: r
  } = v.useContext(Et._internalContext), [i, s, a] = Pr(n, [Et.defaultSeed, e], {
    salt: `${bo}-${t || ""}`,
    override: o,
    getComputedToken: nr,
    cssVar: r && {
      prefix: r.prefix,
      key: r.key,
      unitless: _i,
      ignore: Ti,
      preserve: Pi
    }
  });
  return [n, a, t ? s : "", i, r];
}
const {
  genStyleHooks: Oi,
  genComponentStyleHook: ls,
  genSubStyleComponent: us
} = Si({
  usePrefix: () => {
    const {
      getPrefixCls: e,
      iconPrefixCls: t
    } = Rt();
    return {
      iconPrefixCls: t,
      rootPrefixCls: e()
    };
  },
  useToken: () => {
    const [e, t, n, o, r] = Mi();
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
    } = Rt();
    return e ?? {};
  },
  layer: {
    name: "antdx",
    dependencies: ["antd"]
  }
});
var Ai = `accept acceptCharset accessKey action allowFullScreen allowTransparency
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
    summary tabIndex target title type useMap value width wmode wrap`, ki = `onCopy onCut onPaste onCompositionEnd onCompositionStart onCompositionUpdate onKeyDown
    onKeyPress onKeyUp onFocus onBlur onChange onInput onSubmit onClick onContextMenu onDoubleClick
    onDrag onDragEnd onDragEnter onDragExit onDragLeave onDragOver onDragStart onDrop onMouseDown
    onMouseEnter onMouseLeave onMouseMove onMouseOut onMouseOver onMouseUp onSelect onTouchCancel
    onTouchEnd onTouchMove onTouchStart onScroll onWheel onAbort onCanPlay onCanPlayThrough
    onDurationChange onEmptied onEncrypted onEnded onError onLoadedData onLoadedMetadata
    onLoadStart onPause onPlay onPlaying onProgress onRateChange onSeeked onSeeking onStalled onSuspend onTimeUpdate onVolumeChange onWaiting onLoad onError`, Li = "".concat(Ai, " ").concat(ki).split(/[\s\n]+/), Ii = "aria-", ji = "data-";
function yn(e, t) {
  return e.indexOf(t) === 0;
}
function Di(e) {
  var t = arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : !1, n;
  t === !1 ? n = {
    aria: !0,
    data: !0,
    attr: !0
  } : t === !0 ? n = {
    aria: !0
  } : n = w({}, t);
  var o = {};
  return Object.keys(e).forEach(function(r) {
    // Aria
    (n.aria && (r === "role" || yn(r, Ii)) || // Data
    n.data && yn(r, ji) || // Attr
    n.attr && Li.includes(r)) && (o[r] = e[r]);
  }), o;
}
function $i(e, t) {
  return cr(e, () => {
    const n = t(), {
      nativeElement: o
    } = n;
    return new Proxy(o, {
      get(r, i) {
        return n[i] ? n[i] : Reflect.get(r, i);
      }
    });
  });
}
const rr = /* @__PURE__ */ p.createContext({}), bn = () => ({
  height: 0
}), Sn = (e) => ({
  height: e.scrollHeight
});
function Ni(e) {
  const {
    title: t,
    onOpenChange: n,
    open: o,
    children: r,
    className: i,
    style: s,
    classNames: a = {},
    styles: l = {},
    closable: c,
    forceRender: d
  } = e, {
    prefixCls: u
  } = p.useContext(rr), f = `${u}-header`;
  return /* @__PURE__ */ p.createElement(Zn, {
    motionEnter: !0,
    motionLeave: !0,
    motionName: `${f}-motion`,
    leavedClassName: `${f}-motion-hidden`,
    onEnterStart: bn,
    onEnterActive: Sn,
    onLeaveStart: Sn,
    onLeaveActive: bn,
    visible: o,
    forceRender: d
  }, ({
    className: h,
    style: b
  }) => /* @__PURE__ */ p.createElement("div", {
    className: ee(f, h, i),
    style: {
      ...b,
      ...s
    }
  }, (c !== !1 || t) && /* @__PURE__ */ p.createElement("div", {
    className: (
      // We follow antd naming standard here.
      // So the header part is use `-header` suffix.
      // Though its little bit weird for double `-header`.
      ee(`${f}-header`, a.header)
    ),
    style: {
      ...l.header
    }
  }, /* @__PURE__ */ p.createElement("div", {
    className: `${f}-title`
  }, t), c !== !1 && /* @__PURE__ */ p.createElement("div", {
    className: `${f}-close`
  }, /* @__PURE__ */ p.createElement(Rn, {
    type: "text",
    icon: /* @__PURE__ */ p.createElement(xr, null),
    size: "small",
    onClick: () => {
      n == null || n(!o);
    }
  }))), r && /* @__PURE__ */ p.createElement("div", {
    className: ee(`${f}-content`, a.content),
    style: {
      ...l.content
    }
  }, r)));
}
const lt = /* @__PURE__ */ p.createContext(null);
function Bi(e, t) {
  const {
    className: n,
    action: o,
    onClick: r,
    ...i
  } = e, s = p.useContext(lt), {
    prefixCls: a,
    disabled: l
  } = s, c = s[o], d = l ?? i.disabled ?? s[`${o}Disabled`];
  return /* @__PURE__ */ p.createElement(Rn, se({
    type: "text"
  }, i, {
    ref: t,
    onClick: (u) => {
      d || (c && c(), r && r(u));
    },
    className: ee(a, n, {
      [`${a}-disabled`]: d
    })
  }));
}
const ut = /* @__PURE__ */ p.forwardRef(Bi);
function Hi(e, t) {
  return /* @__PURE__ */ p.createElement(ut, se({
    icon: /* @__PURE__ */ p.createElement(Cr, null)
  }, e, {
    action: "onClear",
    ref: t
  }));
}
const Vi = /* @__PURE__ */ p.forwardRef(Hi), Fi = /* @__PURE__ */ lr((e) => {
  const {
    className: t
  } = e;
  return /* @__PURE__ */ v.createElement("svg", {
    color: "currentColor",
    viewBox: "0 0 1000 1000",
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink",
    className: t
  }, /* @__PURE__ */ v.createElement("title", null, "Stop Loading"), /* @__PURE__ */ v.createElement("rect", {
    fill: "currentColor",
    height: "250",
    rx: "24",
    ry: "24",
    width: "250",
    x: "375",
    y: "375"
  }), /* @__PURE__ */ v.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    opacity: "0.45"
  }), /* @__PURE__ */ v.createElement("circle", {
    cx: "500",
    cy: "500",
    fill: "none",
    r: "450",
    stroke: "currentColor",
    strokeWidth: "100",
    strokeDasharray: "600 9999999"
  }, /* @__PURE__ */ v.createElement("animateTransform", {
    attributeName: "transform",
    dur: "1s",
    from: "0 500 500",
    repeatCount: "indefinite",
    to: "360 500 500",
    type: "rotate"
  })));
});
function zi(e, t) {
  const {
    prefixCls: n
  } = p.useContext(lt), {
    className: o
  } = e;
  return /* @__PURE__ */ p.createElement(ut, se({
    icon: null,
    color: "primary",
    variant: "text",
    shape: "circle"
  }, e, {
    className: ee(o, `${n}-loading-button`),
    action: "onCancel",
    ref: t
  }), /* @__PURE__ */ p.createElement(Fi, {
    className: `${n}-loading-icon`
  }));
}
const xn = /* @__PURE__ */ p.forwardRef(zi);
function Xi(e, t) {
  return /* @__PURE__ */ p.createElement(ut, se({
    icon: /* @__PURE__ */ p.createElement(Er, null),
    type: "primary",
    shape: "circle"
  }, e, {
    action: "onSend",
    ref: t
  }));
}
const Cn = /* @__PURE__ */ p.forwardRef(Xi), Me = 1e3, Oe = 4, Ue = 140, En = Ue / 2, He = 250, wn = 500, Ve = 0.8;
function Ui({
  className: e
}) {
  return /* @__PURE__ */ v.createElement("svg", {
    color: "currentColor",
    viewBox: `0 0 ${Me} ${Me}`,
    xmlns: "http://www.w3.org/2000/svg",
    xmlnsXlink: "http://www.w3.org/1999/xlink",
    className: e
  }, /* @__PURE__ */ v.createElement("title", null, "Speech Recording"), Array.from({
    length: Oe
  }).map((t, n) => {
    const o = (Me - Ue * Oe) / (Oe - 1), r = n * (o + Ue), i = Me / 2 - He / 2, s = Me / 2 - wn / 2;
    return /* @__PURE__ */ v.createElement("rect", {
      fill: "currentColor",
      rx: En,
      ry: En,
      height: He,
      width: Ue,
      x: r,
      y: i,
      key: n
    }, /* @__PURE__ */ v.createElement("animate", {
      attributeName: "height",
      values: `${He}; ${wn}; ${He}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ve}s`,
      begin: `${Ve / Oe * n}s`,
      repeatCount: "indefinite"
    }), /* @__PURE__ */ v.createElement("animate", {
      attributeName: "y",
      values: `${i}; ${s}; ${i}`,
      keyTimes: "0; 0.5; 1",
      dur: `${Ve}s`,
      begin: `${Ve / Oe * n}s`,
      repeatCount: "indefinite"
    }));
  }));
}
function Wi(e, t) {
  const {
    speechRecording: n,
    onSpeechDisabled: o,
    prefixCls: r
  } = p.useContext(lt);
  let i = null;
  return n ? i = /* @__PURE__ */ p.createElement(Ui, {
    className: `${r}-recording-icon`
  }) : o ? i = /* @__PURE__ */ p.createElement(wr, null) : i = /* @__PURE__ */ p.createElement(_r, null), /* @__PURE__ */ p.createElement(ut, se({
    icon: i,
    color: "primary",
    variant: "text"
  }, e, {
    action: "onSpeech",
    ref: t
  }));
}
const Ki = /* @__PURE__ */ p.forwardRef(Wi), Gi = (e) => {
  const {
    componentCls: t,
    calc: n
  } = e, o = `${t}-header`;
  return {
    [t]: {
      [o]: {
        borderBottomWidth: e.lineWidth,
        borderBottomStyle: "solid",
        borderBottomColor: e.colorBorder,
        // ======================== Header ========================
        "&-header": {
          background: e.colorFillAlter,
          fontSize: e.fontSize,
          lineHeight: e.lineHeight,
          paddingBlock: n(e.paddingSM).sub(e.lineWidthBold).equal(),
          paddingInlineStart: e.padding,
          paddingInlineEnd: e.paddingXS,
          display: "flex",
          [`${o}-title`]: {
            flex: "auto"
          }
        },
        // ======================= Content ========================
        "&-content": {
          padding: e.padding
        },
        // ======================== Motion ========================
        "&-motion": {
          transition: ["height", "border"].map((r) => `${r} ${e.motionDurationSlow}`).join(","),
          overflow: "hidden",
          "&-enter-start, &-leave-active": {
            borderBottomColor: "transparent"
          },
          "&-hidden": {
            display: "none"
          }
        }
      }
    }
  };
}, qi = (e) => {
  const {
    componentCls: t,
    padding: n,
    paddingSM: o,
    paddingXS: r,
    lineWidth: i,
    lineWidthBold: s,
    calc: a
  } = e;
  return {
    [t]: {
      position: "relative",
      width: "100%",
      boxSizing: "border-box",
      boxShadow: `${e.boxShadowTertiary}`,
      transition: `background ${e.motionDurationSlow}`,
      // Border
      borderRadius: {
        _skip_check_: !0,
        value: a(e.borderRadius).mul(2).equal()
      },
      borderColor: e.colorBorder,
      borderWidth: 0,
      borderStyle: "solid",
      // Border
      "&:after": {
        content: '""',
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        transition: `border-color ${e.motionDurationSlow}`,
        borderRadius: {
          _skip_check_: !0,
          value: "inherit"
        },
        borderStyle: "inherit",
        borderColor: "inherit",
        borderWidth: i
      },
      // Focus
      "&:focus-within": {
        boxShadow: `${e.boxShadowSecondary}`,
        borderColor: e.colorPrimary,
        "&:after": {
          borderWidth: s
        }
      },
      "&-disabled": {
        background: e.colorBgContainerDisabled
      },
      // ============================== RTL ==============================
      [`&${t}-rtl`]: {
        direction: "rtl"
      },
      // ============================ Content ============================
      [`${t}-content`]: {
        display: "flex",
        gap: r,
        width: "100%",
        paddingBlock: o,
        paddingInlineStart: n,
        paddingInlineEnd: o,
        boxSizing: "border-box",
        alignItems: "flex-end"
      },
      // ============================ Prefix =============================
      [`${t}-prefix`]: {
        flex: "none"
      },
      // ============================= Input =============================
      [`${t}-input`]: {
        padding: 0,
        borderRadius: 0,
        flex: "auto",
        alignSelf: "center",
        minHeight: "auto"
      },
      // ============================ Actions ============================
      [`${t}-actions-list`]: {
        flex: "none",
        display: "flex",
        "&-presets": {
          gap: e.paddingXS
        }
      },
      [`${t}-actions-btn`]: {
        "&-disabled": {
          opacity: 0.45
        },
        "&-loading-button": {
          padding: 0,
          border: 0
        },
        "&-loading-icon": {
          height: e.controlHeight,
          width: e.controlHeight,
          verticalAlign: "top"
        },
        "&-recording-icon": {
          height: "1.2em",
          width: "1.2em",
          verticalAlign: "top"
        }
      }
    }
  };
}, Qi = () => ({}), Yi = Oi("Sender", (e) => {
  const {
    paddingXS: t,
    calc: n
  } = e, o = Bt(e, {
    SenderContentMaxWidth: `calc(100% - ${wt(n(t).add(32).equal())})`
  });
  return [qi(o), Gi(o)];
}, Qi);
let Ge;
!Ge && typeof window < "u" && (Ge = window.SpeechRecognition || window.webkitSpeechRecognition);
function Zi(e, t) {
  const n = he(e), [o, r, i] = v.useMemo(() => typeof t == "object" ? [t.recording, t.onRecordingChange, typeof t.recording == "boolean"] : [void 0, void 0, !1], [t]), [s, a] = v.useState(null);
  v.useEffect(() => {
    if (typeof navigator < "u" && "permissions" in navigator) {
      let g = null;
      return navigator.permissions.query({
        name: "microphone"
      }).then((m) => {
        a(m.state), m.onchange = function() {
          a(this.state);
        }, g = m;
      }), () => {
        g && (g.onchange = null);
      };
    }
  }, []);
  const l = Ge && s !== "denied", c = v.useRef(null), [d, u] = In(!1, {
    value: o
  }), f = v.useRef(!1), h = () => {
    if (l && !c.current) {
      const g = new Ge();
      g.onstart = () => {
        u(!0);
      }, g.onend = () => {
        u(!1);
      }, g.onresult = (m) => {
        var x, E, T;
        if (!f.current) {
          const y = (T = (E = (x = m.results) == null ? void 0 : x[0]) == null ? void 0 : E[0]) == null ? void 0 : T.transcript;
          n(y);
        }
        f.current = !1;
      }, c.current = g;
    }
  }, b = he((g) => {
    g && !d || (f.current = g, i ? r == null || r(!d) : (h(), c.current && (d ? (c.current.stop(), r == null || r(!1)) : (c.current.start(), r == null || r(!0)))));
  });
  return [l, b, d];
}
function Ji(e, t, n) {
  return $o(e, t) || n;
}
const es = /* @__PURE__ */ v.forwardRef((e, t) => {
  const {
    prefixCls: n,
    styles: o = {},
    classNames: r = {},
    className: i,
    rootClassName: s,
    style: a,
    defaultValue: l,
    value: c,
    readOnly: d,
    submitType: u = "enter",
    onSubmit: f,
    loading: h,
    components: b,
    onCancel: g,
    onChange: m,
    actions: x,
    onKeyPress: E,
    onKeyDown: T,
    disabled: y,
    allowSpeech: R,
    prefix: S,
    header: M,
    onPaste: O,
    onPasteFile: L,
    ...B
  } = e, {
    direction: $,
    getPrefixCls: k
  } = Rt(), P = k("sender", n), I = v.useRef(null), j = v.useRef(null);
  $i(t, () => {
    var C, D;
    return {
      nativeElement: I.current,
      focus: (C = j.current) == null ? void 0 : C.focus,
      blur: (D = j.current) == null ? void 0 : D.blur
    };
  });
  const N = Co("sender"), Q = `${P}-input`, [Y, pe, me] = Yi(P), U = ee(P, N.className, i, s, pe, me, {
    [`${P}-rtl`]: $ === "rtl",
    [`${P}-disabled`]: y
  }), te = `${P}-actions-btn`, ae = `${P}-actions-list`, [H, ne] = In(l || "", {
    value: c
  }), ce = (C, D) => {
    ne(C), m && m(C, D);
  }, [G, ge, ve] = Zi((C) => {
    ce(`${H} ${C}`);
  }, R), ye = Ji(b, ["input"], br.TextArea), re = {
    ...Di(B, {
      attr: !0,
      aria: !0,
      data: !0
    }),
    ref: j
  }, le = () => {
    H && f && !h && f(H);
  }, ke = () => {
    ce("");
  }, _e = v.useRef(!1), oe = () => {
    _e.current = !0;
  }, ft = () => {
    _e.current = !1;
  }, Le = (C) => {
    const D = C.key === "Enter" && !_e.current;
    switch (u) {
      case "enter":
        D && !C.shiftKey && (C.preventDefault(), le());
        break;
      case "shiftEnter":
        D && C.shiftKey && (C.preventDefault(), le());
        break;
    }
    E && E(C);
  }, Te = (C) => {
    var Z;
    const D = (Z = C.clipboardData) == null ? void 0 : Z.files[0];
    D && L && (L(D), C.preventDefault()), O == null || O(C);
  }, Re = (C) => {
    var D, Z;
    C.target !== ((D = I.current) == null ? void 0 : D.querySelector(`.${Q}`)) && C.preventDefault(), (Z = j.current) == null || Z.focus();
  };
  let V = /* @__PURE__ */ v.createElement(Sr, {
    className: `${ae}-presets`
  }, R && /* @__PURE__ */ v.createElement(Ki, null), h ? /* @__PURE__ */ v.createElement(xn, null) : /* @__PURE__ */ v.createElement(Cn, null));
  return typeof x == "function" ? V = x(V, {
    components: {
      SendButton: Cn,
      ClearButton: Vi,
      LoadingButton: xn
    }
  }) : x && (V = x), Y(/* @__PURE__ */ v.createElement("div", {
    ref: I,
    className: U,
    style: {
      ...N.style,
      ...a
    }
  }, M && /* @__PURE__ */ v.createElement(rr.Provider, {
    value: {
      prefixCls: P
    }
  }, M), /* @__PURE__ */ v.createElement("div", {
    className: `${P}-content`,
    onMouseDown: Re
  }, S && /* @__PURE__ */ v.createElement("div", {
    className: ee(`${P}-prefix`, N.classNames.prefix, r.prefix),
    style: {
      ...N.styles.prefix,
      ...o.prefix
    }
  }, S), /* @__PURE__ */ v.createElement(ye, se({}, re, {
    disabled: y,
    style: {
      ...N.styles.input,
      ...o.input
    },
    className: ee(Q, N.classNames.input, r.input),
    autoSize: {
      maxRows: 8
    },
    value: H,
    onChange: (C) => {
      ce(C.target.value, C), ge(!0);
    },
    onPressEnter: Le,
    onCompositionStart: oe,
    onCompositionEnd: ft,
    onKeyDown: T,
    onPaste: Te,
    variant: "borderless",
    readOnly: d
  })), /* @__PURE__ */ v.createElement("div", {
    className: ee(ae, N.classNames.actions, r.actions),
    style: {
      ...N.styles.actions,
      ...o.actions
    }
  }, /* @__PURE__ */ v.createElement(lt.Provider, {
    value: {
      prefixCls: te,
      onSend: le,
      onSendDisabled: !H,
      onClear: ke,
      onClearDisabled: !H,
      onCancel: g,
      onCancelDisabled: !h,
      onSpeech: () => ge(!1),
      onSpeechDisabled: !G,
      speechRecording: ve,
      disabled: y
    }
  }, V)))));
}), or = es;
or.Header = Ni;
function ts(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ns(e, t = !1) {
  try {
    if (mr(e))
      return e;
    if (t && !ts(e))
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
function rs(e, t) {
  return ur(() => ns(e, t), [e, t]);
}
function os({
  value: e,
  onValueChange: t
}) {
  const [n, o] = Tn(e), r = J(t);
  r.current = t;
  const i = J(n);
  return i.current = n, fe(() => {
    r.current(n);
  }, [n]), fe(() => {
    Vr(e, i.current) || o(e);
  }, [e]), [n, o];
}
const is = ({
  children: e,
  ...t
}) => /* @__PURE__ */ W.jsx(W.Fragment, {
  children: e(t)
});
function ss(e) {
  return v.createElement(is, {
    children: e
  });
}
function _n(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? ss((n) => /* @__PURE__ */ W.jsx(vr, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ W.jsx(We, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...n
    })
  })) : /* @__PURE__ */ W.jsx(We, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function as({
  key: e,
  slots: t,
  targets: n
}, o) {
  return t[e] ? (...r) => n ? n.map((i, s) => /* @__PURE__ */ W.jsx(v.Fragment, {
    children: _n(i, {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }, s)) : /* @__PURE__ */ W.jsx(W.Fragment, {
    children: _n(t[e], {
      clone: !0,
      params: r,
      forceClone: (o == null ? void 0 : o.forceClone) ?? !0
    })
  }) : void 0;
}
const fs = po(({
  slots: e,
  children: t,
  setSlotParams: n,
  onValueChange: o,
  onChange: r,
  onPasteFile: i,
  upload: s,
  elRef: a,
  ...l
}) => {
  const c = rs(l.actions, !0), [d, u] = os({
    onValueChange: o,
    value: l.value
  });
  return /* @__PURE__ */ W.jsxs(W.Fragment, {
    children: [/* @__PURE__ */ W.jsx("div", {
      style: {
        display: "none"
      },
      children: t
    }), /* @__PURE__ */ W.jsx(or, {
      ...l,
      value: d,
      ref: a,
      onChange: (f) => {
        r == null || r(f), u(f);
      },
      onPasteFile: async (f) => {
        const h = await s(Array.isArray(f) ? f : [f]);
        i == null || i(h.map((b) => b.path));
      },
      header: e.header ? /* @__PURE__ */ W.jsx(We, {
        slot: e.header
      }) : l.header,
      prefix: e.prefix ? /* @__PURE__ */ W.jsx(We, {
        slot: e.prefix
      }) : l.prefix,
      actions: e.actions ? as({
        slots: e,
        setSlotParams: n,
        key: "actions"
      }, {
        clone: !0
      }) : c || l.actions
    })]
  });
});
export {
  fs as Sender,
  fs as default
};
