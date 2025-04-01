import { i as Re, a as q, r as je, g as Se, w as A, b as Pe } from "./Index-BCFDDsbi.js";
const S = window.ms_globals.React, ye = window.ms_globals.React.forwardRef, we = window.ms_globals.React.useRef, Ee = window.ms_globals.React.useState, Ce = window.ms_globals.React.useEffect, j = window.ms_globals.React.useMemo, G = window.ms_globals.ReactDOM.createPortal, ke = window.ms_globals.internalContext.useContextPropsContext, J = window.ms_globals.internalContext.ContextPropsProvider, Oe = window.ms_globals.antd.DatePicker, Q = window.ms_globals.dayjs, Te = window.ms_globals.createItemsContext.createItemsContext;
var Fe = /\s/;
function De(e) {
  for (var t = e.length; t-- && Fe.test(e.charAt(t)); )
    ;
  return t;
}
var Le = /^\s+/;
function Ne(e) {
  return e && e.slice(0, De(e) + 1).replace(Le, "");
}
var Z = NaN, Ae = /^[-+]0x[0-9a-f]+$/i, We = /^0b[01]+$/i, Me = /^0o[0-7]+$/i, Ue = parseInt;
function V(e) {
  if (typeof e == "number")
    return e;
  if (Re(e))
    return Z;
  if (q(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = q(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ne(e);
  var s = We.test(e);
  return s || Me.test(e) ? Ue(e.slice(2), s ? 2 : 8) : Ae.test(e) ? Z : +e;
}
var B = function() {
  return je.Date.now();
}, Be = "Expected a function", He = Math.max, ze = Math.min;
function Ge(e, t, s) {
  var l, r, n, o, i, f, x = 0, h = !1, c = !1, v = !0;
  if (typeof e != "function")
    throw new TypeError(Be);
  t = V(t) || 0, q(s) && (h = !!s.leading, c = "maxWait" in s, n = c ? He(V(s.maxWait) || 0, t) : n, v = "trailing" in s ? !!s.trailing : v);
  function d(p) {
    var E = l, O = r;
    return l = r = void 0, x = p, o = e.apply(O, E), o;
  }
  function y(p) {
    return x = p, i = setTimeout(m, t), h ? d(p) : o;
  }
  function I(p) {
    var E = p - f, O = p - x, D = t - E;
    return c ? ze(D, n - O) : D;
  }
  function u(p) {
    var E = p - f, O = p - x;
    return f === void 0 || E >= t || E < 0 || c && O >= n;
  }
  function m() {
    var p = B();
    if (u(p))
      return b(p);
    i = setTimeout(m, I(p));
  }
  function b(p) {
    return i = void 0, v && l ? d(p) : (l = r = void 0, o);
  }
  function k() {
    i !== void 0 && clearTimeout(i), x = 0, l = f = r = i = void 0;
  }
  function a() {
    return i === void 0 ? o : b(B());
  }
  function P() {
    var p = B(), E = u(p);
    if (l = arguments, r = this, f = p, E) {
      if (i === void 0)
        return y(f);
      if (c)
        return clearTimeout(i), i = setTimeout(m, t), d(f);
    }
    return i === void 0 && (i = setTimeout(m, t)), o;
  }
  return P.cancel = k, P.flush = a, P;
}
var ce = {
  exports: {}
}, U = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var qe = S, Je = Symbol.for("react.element"), Xe = Symbol.for("react.fragment"), Ye = Object.prototype.hasOwnProperty, Ke = qe.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Qe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function ae(e, t, s) {
  var l, r = {}, n = null, o = null;
  s !== void 0 && (n = "" + s), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (l in t) Ye.call(t, l) && !Qe.hasOwnProperty(l) && (r[l] = t[l]);
  if (e && e.defaultProps) for (l in t = e.defaultProps, t) r[l] === void 0 && (r[l] = t[l]);
  return {
    $$typeof: Je,
    type: e,
    key: n,
    ref: o,
    props: r,
    _owner: Ke.current
  };
}
U.Fragment = Xe;
U.jsx = ae;
U.jsxs = ae;
ce.exports = U;
var _ = ce.exports;
const {
  SvelteComponent: Ze,
  assign: $,
  binding_callbacks: ee,
  check_outros: Ve,
  children: ue,
  claim_element: fe,
  claim_space: $e,
  component_subscribe: te,
  compute_slots: et,
  create_slot: tt,
  detach: F,
  element: de,
  empty: ne,
  exclude_internal_props: re,
  get_all_dirty_from_scope: nt,
  get_slot_changes: rt,
  group_outros: ot,
  init: st,
  insert_hydration: W,
  safe_not_equal: lt,
  set_custom_element_data: me,
  space: it,
  transition_in: M,
  transition_out: X,
  update_slot_base: ct
} = window.__gradio__svelte__internal, {
  beforeUpdate: at,
  getContext: ut,
  onDestroy: ft,
  setContext: dt
} = window.__gradio__svelte__internal;
function oe(e) {
  let t, s;
  const l = (
    /*#slots*/
    e[7].default
  ), r = tt(
    l,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = de("svelte-slot"), r && r.c(), this.h();
    },
    l(n) {
      t = fe(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = ue(t);
      r && r.l(o), o.forEach(F), this.h();
    },
    h() {
      me(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      W(n, t, o), r && r.m(t, null), e[9](t), s = !0;
    },
    p(n, o) {
      r && r.p && (!s || o & /*$$scope*/
      64) && ct(
        r,
        l,
        n,
        /*$$scope*/
        n[6],
        s ? rt(
          l,
          /*$$scope*/
          n[6],
          o,
          null
        ) : nt(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      s || (M(r, n), s = !0);
    },
    o(n) {
      X(r, n), s = !1;
    },
    d(n) {
      n && F(t), r && r.d(n), e[9](null);
    }
  };
}
function mt(e) {
  let t, s, l, r, n = (
    /*$$slots*/
    e[4].default && oe(e)
  );
  return {
    c() {
      t = de("react-portal-target"), s = it(), n && n.c(), l = ne(), this.h();
    },
    l(o) {
      t = fe(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), ue(t).forEach(F), s = $e(o), n && n.l(o), l = ne(), this.h();
    },
    h() {
      me(t, "class", "svelte-1rt0kpf");
    },
    m(o, i) {
      W(o, t, i), e[8](t), W(o, s, i), n && n.m(o, i), W(o, l, i), r = !0;
    },
    p(o, [i]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, i), i & /*$$slots*/
      16 && M(n, 1)) : (n = oe(o), n.c(), M(n, 1), n.m(l.parentNode, l)) : n && (ot(), X(n, 1, 1, () => {
        n = null;
      }), Ve());
    },
    i(o) {
      r || (M(n), r = !0);
    },
    o(o) {
      X(n), r = !1;
    },
    d(o) {
      o && (F(t), F(s), F(l)), e[8](null), n && n.d(o);
    }
  };
}
function se(e) {
  const {
    svelteInit: t,
    ...s
  } = e;
  return s;
}
function pt(e, t, s) {
  let l, r, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const i = et(n);
  let {
    svelteInit: f
  } = t;
  const x = A(se(t)), h = A();
  te(e, h, (a) => s(0, l = a));
  const c = A();
  te(e, c, (a) => s(1, r = a));
  const v = [], d = ut("$$ms-gr-react-wrapper"), {
    slotKey: y,
    slotIndex: I,
    subSlotIndex: u
  } = Se() || {}, m = f({
    parent: d,
    props: x,
    target: h,
    slot: c,
    slotKey: y,
    slotIndex: I,
    subSlotIndex: u,
    onDestroy(a) {
      v.push(a);
    }
  });
  dt("$$ms-gr-react-wrapper", m), at(() => {
    x.set(se(t));
  }), ft(() => {
    v.forEach((a) => a());
  });
  function b(a) {
    ee[a ? "unshift" : "push"](() => {
      l = a, h.set(l);
    });
  }
  function k(a) {
    ee[a ? "unshift" : "push"](() => {
      r = a, c.set(r);
    });
  }
  return e.$$set = (a) => {
    s(17, t = $($({}, t), re(a))), "svelteInit" in a && s(5, f = a.svelteInit), "$$scope" in a && s(6, o = a.$$scope);
  }, t = re(t), [l, r, h, c, i, f, o, n, b, k];
}
class _t extends Ze {
  constructor(t) {
    super(), st(this, t, pt, mt, lt, {
      svelteInit: 5
    });
  }
}
const le = window.ms_globals.rerender, H = window.ms_globals.tree;
function ht(e, t = {}) {
  function s(l) {
    const r = A(), n = new _t({
      ...l,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, f = o.parent ?? H;
          return f.nodes = [...f.nodes, i], le({
            createPortal: G,
            node: H
          }), o.onDestroy(() => {
            f.nodes = f.nodes.filter((x) => x.svelteInstance !== r), le({
              createPortal: G,
              node: H
            });
          }), i;
        },
        ...l.props
      }
    });
    return r.set(n), n;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(s);
    });
  });
}
const xt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function gt(e) {
  return e ? Object.keys(e).reduce((t, s) => {
    const l = e[s];
    return t[s] = vt(s, l), t;
  }, {}) : {};
}
function vt(e, t) {
  return typeof t == "number" && !xt.includes(e) ? t + "px" : t;
}
function Y(e) {
  const t = [], s = e.cloneNode(!1);
  if (e._reactElement) {
    const r = S.Children.toArray(e._reactElement.props.children).map((n) => {
      if (S.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: i
        } = Y(n.props.el);
        return S.cloneElement(n, {
          ...n.props,
          el: i,
          children: [...S.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return r.originalChildren = e._reactElement.props.children, t.push(G(S.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: r
    }), s)), {
      clonedElement: s,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((r) => {
    e.getEventListeners(r).forEach(({
      listener: o,
      type: i,
      useCapture: f
    }) => {
      s.addEventListener(i, o, f);
    });
  });
  const l = Array.from(e.childNodes);
  for (let r = 0; r < l.length; r++) {
    const n = l[r];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: i
      } = Y(n);
      t.push(...i), s.appendChild(o);
    } else n.nodeType === 3 && s.appendChild(n.cloneNode());
  }
  return {
    clonedElement: s,
    portals: t
  };
}
function It(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const w = ye(({
  slot: e,
  clone: t,
  className: s,
  style: l,
  observeAttributes: r
}, n) => {
  const o = we(), [i, f] = Ee([]), {
    forceClone: x
  } = ke(), h = x ? !0 : t;
  return Ce(() => {
    var I;
    if (!o.current || !e)
      return;
    let c = e;
    function v() {
      let u = c;
      if (c.tagName.toLowerCase() === "svelte-slot" && c.children.length === 1 && c.children[0] && (u = c.children[0], u.tagName.toLowerCase() === "react-portal-target" && u.children[0] && (u = u.children[0])), It(n, u), s && u.classList.add(...s.split(" ")), l) {
        const m = gt(l);
        Object.keys(m).forEach((b) => {
          u.style[b] = m[b];
        });
      }
    }
    let d = null, y = null;
    if (h && window.MutationObserver) {
      let u = function() {
        var a, P, p;
        (a = o.current) != null && a.contains(c) && ((P = o.current) == null || P.removeChild(c));
        const {
          portals: b,
          clonedElement: k
        } = Y(e);
        c = k, f(b), c.style.display = "contents", y && clearTimeout(y), y = setTimeout(() => {
          v();
        }, 50), (p = o.current) == null || p.appendChild(c);
      };
      u();
      const m = Ge(() => {
        u(), d == null || d.disconnect(), d == null || d.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: r
        });
      }, 50);
      d = new window.MutationObserver(m), d.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      c.style.display = "contents", v(), (I = o.current) == null || I.appendChild(c);
    return () => {
      var u, m;
      c.style.display = "", (u = o.current) != null && u.contains(c) && ((m = o.current) == null || m.removeChild(c)), d == null || d.disconnect();
    };
  }, [e, h, s, l, n, r]), S.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...i);
});
function bt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function yt(e, t = !1) {
  try {
    if (Pe(e))
      return e;
    if (t && !bt(e))
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
function L(e, t) {
  return j(() => yt(e, t), [e, t]);
}
const wt = ({
  children: e,
  ...t
}) => /* @__PURE__ */ _.jsx(_.Fragment, {
  children: e(t)
});
function pe(e) {
  return S.createElement(wt, {
    children: e
  });
}
function _e(e, t, s) {
  const l = e.filter(Boolean);
  if (l.length !== 0)
    return l.map((r, n) => {
      var x;
      if (typeof r != "object")
        return r;
      const o = {
        ...r.props,
        key: ((x = r.props) == null ? void 0 : x.key) ?? (s ? `${s}-${n}` : `${n}`)
      };
      let i = o;
      Object.keys(r.slots).forEach((h) => {
        if (!r.slots[h] || !(r.slots[h] instanceof Element) && !r.slots[h].el)
          return;
        const c = h.split(".");
        c.forEach((m, b) => {
          i[m] || (i[m] = {}), b !== c.length - 1 && (i = o[m]);
        });
        const v = r.slots[h];
        let d, y, I = !1, u = t == null ? void 0 : t.forceClone;
        v instanceof Element ? d = v : (d = v.el, y = v.callback, I = v.clone ?? I, u = v.forceClone ?? u), u = u ?? !!y, i[c[c.length - 1]] = d ? y ? (...m) => (y(c[c.length - 1], m), /* @__PURE__ */ _.jsx(J, {
          ...r.ctx,
          params: m,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(w, {
            slot: d,
            clone: I
          })
        })) : pe((m) => /* @__PURE__ */ _.jsx(J, {
          ...r.ctx,
          forceClone: u,
          children: /* @__PURE__ */ _.jsx(w, {
            slot: d,
            clone: I,
            ...m
          })
        })) : i[c[c.length - 1]], i = o;
      });
      const f = "children";
      return r[f] && (o[f] = _e(r[f], t, `${n}`)), o;
    });
}
function ie(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? pe((s) => /* @__PURE__ */ _.jsx(J, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ _.jsx(w, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...s
    })
  })) : /* @__PURE__ */ _.jsx(w, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function z({
  key: e,
  slots: t,
  targets: s
}, l) {
  return t[e] ? (...r) => s ? s.map((n, o) => /* @__PURE__ */ _.jsx(S.Fragment, {
    children: ie(n, {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ _.jsx(_.Fragment, {
    children: ie(t[e], {
      clone: !0,
      params: r,
      forceClone: !0
    })
  }) : void 0;
}
const {
  withItemsContextProvider: Et,
  useItems: Ct,
  ItemHandler: jt
} = Te("antd-date-picker-presets");
function R(e) {
  return Q(typeof e == "number" ? e * 1e3 : e);
}
function N(e) {
  return (e == null ? void 0 : e.map((t) => t ? t.valueOf() / 1e3 : null)) || [null, null];
}
const St = ht(Et(["presets"], ({
  slots: e,
  disabledDate: t,
  value: s,
  defaultValue: l,
  defaultPickerValue: r,
  pickerValue: n,
  presets: o,
  showTime: i,
  onChange: f,
  minDate: x,
  maxDate: h,
  cellRender: c,
  panelRender: v,
  getPopupContainer: d,
  onValueChange: y,
  onPanelChange: I,
  onCalendarChange: u,
  children: m,
  setSlotParams: b,
  elRef: k,
  ...a
}) => {
  const P = L(t), p = L(d), E = L(c), O = L(v), D = j(() => {
    var g;
    return typeof i == "object" ? {
      ...i,
      defaultValue: (g = i.defaultValue) == null ? void 0 : g.map((C) => R(C))
    } : i;
  }, [i]), he = j(() => s == null ? void 0 : s.map((g) => R(g)), [s]), xe = j(() => l == null ? void 0 : l.map((g) => R(g)), [l]), ge = j(() => Array.isArray(r) ? r.map((g) => R(g)) : r ? R(r) : void 0, [r]), ve = j(() => Array.isArray(n) ? n.map((g) => R(g)) : n ? R(n) : void 0, [n]), Ie = j(() => x ? R(x) : void 0, [x]), be = j(() => h ? R(h) : void 0, [h]), {
    items: {
      presets: K
    }
  } = Ct();
  return /* @__PURE__ */ _.jsxs(_.Fragment, {
    children: [/* @__PURE__ */ _.jsx("div", {
      style: {
        display: "none"
      },
      children: m
    }), /* @__PURE__ */ _.jsx(Oe.RangePicker, {
      ...a,
      ref: k,
      value: he,
      defaultValue: xe,
      defaultPickerValue: ge,
      pickerValue: ve,
      minDate: Ie,
      maxDate: be,
      showTime: D,
      disabledDate: P,
      getPopupContainer: p,
      cellRender: e.cellRender ? z({
        slots: e,
        setSlotParams: b,
        key: "cellRender"
      }) : E,
      panelRender: e.panelRender ? z({
        slots: e,
        setSlotParams: b,
        key: "panelRender"
      }) : O,
      presets: j(() => {
        var g;
        return (g = o || _e(K)) == null ? void 0 : g.map((C) => ({
          ...C,
          value: N(C.value)
        }));
      }, [o, K]),
      onPanelChange: (g, ...C) => {
        const T = N(g);
        I == null || I(T, ...C);
      },
      onChange: (g, ...C) => {
        const T = N(g);
        f == null || f(T, ...C), y(T);
      },
      onCalendarChange: (g, ...C) => {
        const T = N(g);
        u == null || u(T, ...C);
      },
      renderExtraFooter: e.renderExtraFooter ? z({
        slots: e,
        setSlotParams: b,
        key: "renderExtraFooter"
      }) : a.renderExtraFooter,
      prefix: e.prefix ? /* @__PURE__ */ _.jsx(w, {
        slot: e.prefix
      }) : a.prefix,
      prevIcon: e.prevIcon ? /* @__PURE__ */ _.jsx(w, {
        slot: e.prevIcon
      }) : a.prevIcon,
      nextIcon: e.nextIcon ? /* @__PURE__ */ _.jsx(w, {
        slot: e.nextIcon
      }) : a.nextIcon,
      suffixIcon: e.suffixIcon ? /* @__PURE__ */ _.jsx(w, {
        slot: e.suffixIcon
      }) : a.suffixIcon,
      superNextIcon: e.superNextIcon ? /* @__PURE__ */ _.jsx(w, {
        slot: e.superNextIcon
      }) : a.superNextIcon,
      superPrevIcon: e.superPrevIcon ? /* @__PURE__ */ _.jsx(w, {
        slot: e.superPrevIcon
      }) : a.superPrevIcon,
      allowClear: e["allowClear.clearIcon"] ? {
        clearIcon: /* @__PURE__ */ _.jsx(w, {
          slot: e["allowClear.clearIcon"]
        })
      } : a.allowClear,
      separator: e.separator ? /* @__PURE__ */ _.jsx(w, {
        slot: e.separator,
        clone: !0
      }) : a.separator
    })]
  });
}));
export {
  St as DateRangePicker,
  St as default
};
