import { i as Le, a as K, r as Se, g as Fe, w as D, b as Ce } from "./Index-DxIJOfMG.js";
const S = window.ms_globals.React, ue = window.ms_globals.React.useMemo, Re = window.ms_globals.React.forwardRef, de = window.ms_globals.React.useRef, fe = window.ms_globals.React.useState, me = window.ms_globals.React.useEffect, H = window.ms_globals.ReactDOM.createPortal, Ue = window.ms_globals.internalContext.useContextPropsContext, ke = window.ms_globals.internalContext.ContextPropsProvider, Te = window.ms_globals.antd.Upload;
var Oe = /\s/;
function Pe(e) {
  for (var t = e.length; t-- && Oe.test(e.charAt(t)); )
    ;
  return t;
}
var je = /^\s+/;
function Ne(e) {
  return e && e.slice(0, Pe(e) + 1).replace(je, "");
}
var V = NaN, We = /^[-+]0x[0-9a-f]+$/i, Ae = /^0b[01]+$/i, De = /^0o[0-7]+$/i, Me = parseInt;
function $(e) {
  if (typeof e == "number")
    return e;
  if (Le(e))
    return V;
  if (K(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = K(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Ne(e);
  var r = Ae.test(e);
  return r || De.test(e) ? Me(e.slice(2), r ? 2 : 8) : We.test(e) ? V : +e;
}
function ze() {
}
var B = function() {
  return Se.Date.now();
}, qe = "Expected a function", Be = Math.max, Ge = Math.min;
function He(e, t, r) {
  var s, i, n, o, c, f, _ = 0, g = !1, l = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(qe);
  t = $(t) || 0, K(r) && (g = !!r.leading, l = "maxWait" in r, n = l ? Be($(r.maxWait) || 0, t) : n, w = "trailing" in r ? !!r.trailing : w);
  function m(d) {
    var b = s, U = i;
    return s = i = void 0, _ = d, o = e.apply(U, b), o;
  }
  function I(d) {
    return _ = d, c = setTimeout(h, t), g ? m(d) : o;
  }
  function E(d) {
    var b = d - f, U = d - _, A = t - b;
    return l ? Ge(A, n - U) : A;
  }
  function a(d) {
    var b = d - f, U = d - _;
    return f === void 0 || b >= t || b < 0 || l && U >= n;
  }
  function h() {
    var d = B();
    if (a(d))
      return y(d);
    c = setTimeout(h, E(d));
  }
  function y(d) {
    return c = void 0, w && s ? m(d) : (s = i = void 0, o);
  }
  function p() {
    c !== void 0 && clearTimeout(c), _ = 0, s = f = i = c = void 0;
  }
  function u() {
    return c === void 0 ? o : y(B());
  }
  function C() {
    var d = B(), b = a(d);
    if (s = arguments, i = this, f = d, b) {
      if (c === void 0)
        return I(f);
      if (l)
        return clearTimeout(c), c = setTimeout(h, t), m(f);
    }
    return c === void 0 && (c = setTimeout(h, t)), o;
  }
  return C.cancel = p, C.flush = u, C;
}
var pe = {
  exports: {}
}, q = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Ke = S, Je = Symbol.for("react.element"), Xe = Symbol.for("react.fragment"), Ye = Object.prototype.hasOwnProperty, Qe = Ke.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Ze = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function we(e, t, r) {
  var s, i = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) Ye.call(t, s) && !Ze.hasOwnProperty(s) && (i[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) i[s] === void 0 && (i[s] = t[s]);
  return {
    $$typeof: Je,
    type: e,
    key: n,
    ref: o,
    props: i,
    _owner: Qe.current
  };
}
q.Fragment = Xe;
q.jsx = we;
q.jsxs = we;
pe.exports = q;
var F = pe.exports;
const {
  SvelteComponent: Ve,
  assign: ee,
  binding_callbacks: te,
  check_outros: $e,
  children: he,
  claim_element: _e,
  claim_space: et,
  component_subscribe: ne,
  compute_slots: tt,
  create_slot: nt,
  detach: N,
  element: ge,
  empty: re,
  exclude_internal_props: oe,
  get_all_dirty_from_scope: rt,
  get_slot_changes: ot,
  group_outros: it,
  init: st,
  insert_hydration: M,
  safe_not_equal: ct,
  set_custom_element_data: Ie,
  space: lt,
  transition_in: z,
  transition_out: J,
  update_slot_base: at
} = window.__gradio__svelte__internal, {
  beforeUpdate: ut,
  getContext: dt,
  onDestroy: ft,
  setContext: mt
} = window.__gradio__svelte__internal;
function ie(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), i = nt(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ge("svelte-slot"), i && i.c(), this.h();
    },
    l(n) {
      t = _e(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = he(t);
      i && i.l(o), o.forEach(N), this.h();
    },
    h() {
      Ie(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      M(n, t, o), i && i.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      i && i.p && (!r || o & /*$$scope*/
      64) && at(
        i,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? ot(
          s,
          /*$$scope*/
          n[6],
          o,
          null
        ) : rt(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (z(i, n), r = !0);
    },
    o(n) {
      J(i, n), r = !1;
    },
    d(n) {
      n && N(t), i && i.d(n), e[9](null);
    }
  };
}
function pt(e) {
  let t, r, s, i, n = (
    /*$$slots*/
    e[4].default && ie(e)
  );
  return {
    c() {
      t = ge("react-portal-target"), r = lt(), n && n.c(), s = re(), this.h();
    },
    l(o) {
      t = _e(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), he(t).forEach(N), r = et(o), n && n.l(o), s = re(), this.h();
    },
    h() {
      Ie(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      M(o, t, c), e[8](t), M(o, r, c), n && n.m(o, c), M(o, s, c), i = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, c), c & /*$$slots*/
      16 && z(n, 1)) : (n = ie(o), n.c(), z(n, 1), n.m(s.parentNode, s)) : n && (it(), J(n, 1, 1, () => {
        n = null;
      }), $e());
    },
    i(o) {
      i || (z(n), i = !0);
    },
    o(o) {
      J(n), i = !1;
    },
    d(o) {
      o && (N(t), N(r), N(s)), e[8](null), n && n.d(o);
    }
  };
}
function se(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function wt(e, t, r) {
  let s, i, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const c = tt(n);
  let {
    svelteInit: f
  } = t;
  const _ = D(se(t)), g = D();
  ne(e, g, (u) => r(0, s = u));
  const l = D();
  ne(e, l, (u) => r(1, i = u));
  const w = [], m = dt("$$ms-gr-react-wrapper"), {
    slotKey: I,
    slotIndex: E,
    subSlotIndex: a
  } = Fe() || {}, h = f({
    parent: m,
    props: _,
    target: g,
    slot: l,
    slotKey: I,
    slotIndex: E,
    subSlotIndex: a,
    onDestroy(u) {
      w.push(u);
    }
  });
  mt("$$ms-gr-react-wrapper", h), ut(() => {
    _.set(se(t));
  }), ft(() => {
    w.forEach((u) => u());
  });
  function y(u) {
    te[u ? "unshift" : "push"](() => {
      s = u, g.set(s);
    });
  }
  function p(u) {
    te[u ? "unshift" : "push"](() => {
      i = u, l.set(i);
    });
  }
  return e.$$set = (u) => {
    r(17, t = ee(ee({}, t), oe(u))), "svelteInit" in u && r(5, f = u.svelteInit), "$$scope" in u && r(6, o = u.$$scope);
  }, t = oe(t), [s, i, g, l, c, f, o, n, y, p];
}
class ht extends Ve {
  constructor(t) {
    super(), st(this, t, wt, pt, ct, {
      svelteInit: 5
    });
  }
}
const ce = window.ms_globals.rerender, G = window.ms_globals.tree;
function _t(e, t = {}) {
  function r(s) {
    const i = D(), n = new ht({
      ...s,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: i,
            reactComponent: e,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: t.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, f = o.parent ?? G;
          return f.nodes = [...f.nodes, c], ce({
            createPortal: H,
            node: G
          }), o.onDestroy(() => {
            f.nodes = f.nodes.filter((_) => _.svelteInstance !== i), ce({
              createPortal: H,
              node: G
            });
          }), c;
        },
        ...s.props
      }
    });
    return i.set(n), n;
  }
  return new Promise((s) => {
    window.ms_globals.initializePromise.then(() => {
      s(r);
    });
  });
}
function gt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function It(e, t = !1) {
  try {
    if (Ce(e))
      return e;
    if (t && !gt(e))
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
function x(e, t) {
  return ue(() => It(e, t), [e, t]);
}
const vt = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function yt(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return t[r] = bt(r, s), t;
  }, {}) : {};
}
function bt(e, t) {
  return typeof t == "number" && !vt.includes(e) ? t + "px" : t;
}
function X(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const i = S.Children.toArray(e._reactElement.props.children).map((n) => {
      if (S.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: c
        } = X(n.props.el);
        return S.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...S.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return i.originalChildren = e._reactElement.props.children, t.push(H(S.cloneElement(e._reactElement, {
      ...e._reactElement.props,
      children: i
    }), r)), {
      clonedElement: r,
      portals: t
    };
  }
  Object.keys(e.getEventListeners()).forEach((i) => {
    e.getEventListeners(i).forEach(({
      listener: o,
      type: c,
      useCapture: f
    }) => {
      r.addEventListener(c, o, f);
    });
  });
  const s = Array.from(e.childNodes);
  for (let i = 0; i < s.length; i++) {
    const n = s[i];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = X(n);
      t.push(...c), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function xt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const le = Re(({
  slot: e,
  clone: t,
  className: r,
  style: s,
  observeAttributes: i
}, n) => {
  const o = de(), [c, f] = fe([]), {
    forceClone: _
  } = Ue(), g = _ ? !0 : t;
  return me(() => {
    var E;
    if (!o.current || !e)
      return;
    let l = e;
    function w() {
      let a = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (a = l.children[0], a.tagName.toLowerCase() === "react-portal-target" && a.children[0] && (a = a.children[0])), xt(n, a), r && a.classList.add(...r.split(" ")), s) {
        const h = yt(s);
        Object.keys(h).forEach((y) => {
          a.style[y] = h[y];
        });
      }
    }
    let m = null, I = null;
    if (g && window.MutationObserver) {
      let a = function() {
        var u, C, d;
        (u = o.current) != null && u.contains(l) && ((C = o.current) == null || C.removeChild(l));
        const {
          portals: y,
          clonedElement: p
        } = X(e);
        l = p, f(y), l.style.display = "contents", I && clearTimeout(I), I = setTimeout(() => {
          w();
        }, 50), (d = o.current) == null || d.appendChild(l);
      };
      a();
      const h = He(() => {
        a(), m == null || m.disconnect(), m == null || m.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      m = new window.MutationObserver(h), m.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", w(), (E = o.current) == null || E.appendChild(l);
    return () => {
      var a, h;
      l.style.display = "", (a = o.current) != null && a.contains(l) && ((h = o.current) == null || h.removeChild(l)), m == null || m.disconnect();
    };
  }, [e, g, r, s, n, i]), S.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...c);
}), Et = ({
  children: e,
  ...t
}) => /* @__PURE__ */ F.jsx(F.Fragment, {
  children: e(t)
});
function Rt(e) {
  return S.createElement(Et, {
    children: e
  });
}
function ae(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? Rt((r) => /* @__PURE__ */ F.jsx(ke, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ F.jsx(le, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ F.jsx(le, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function j({
  key: e,
  slots: t,
  targets: r
}, s) {
  return t[e] ? (...i) => r ? r.map((n, o) => /* @__PURE__ */ F.jsx(S.Fragment, {
    children: ae(n, {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ F.jsx(F.Fragment, {
    children: ae(t[e], {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }) : void 0;
}
const Lt = (e) => !!e.name;
function St(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const Ct = _t(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: s,
  beforeUpload: i,
  customRequest: n,
  previewFile: o,
  isImageUrl: c,
  itemRender: f,
  iconRender: _,
  data: g,
  onChange: l,
  onValueChange: w,
  onRemove: m,
  maxCount: I,
  fileList: E,
  setSlotParams: a,
  ...h
}) => {
  const y = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = St(r), u = x(p.showPreviewIcon), C = x(p.showRemoveIcon), d = x(p.showDownloadIcon), b = x(i), U = x(n), A = x(s == null ? void 0 : s.format), ve = x(o), ye = x(c), be = x(f), xe = x(_), Ee = x(g), W = de(!1), [k, Y] = fe(E);
  me(() => {
    Y(E);
  }, [E]);
  const Q = ue(() => (k == null ? void 0 : k.map((v) => Lt(v) ? v : {
    ...v,
    name: v.orig_name || v.path,
    uid: v.uid || v.url || v.path,
    status: "done"
  })) || [], [k]);
  return /* @__PURE__ */ F.jsx(Te, {
    ...h,
    fileList: Q,
    data: Ee || g,
    previewFile: ve,
    isImageUrl: ye,
    maxCount: 1,
    itemRender: e.itemRender ? j({
      slots: e,
      setSlotParams: a,
      key: "itemRender"
    }) : be,
    iconRender: e.iconRender ? j({
      slots: e,
      setSlotParams: a,
      key: "iconRender"
    }) : xe,
    onRemove: (v) => {
      if (W.current)
        return;
      m == null || m(v);
      const O = Q.findIndex((T) => T.uid === v.uid), L = k.slice();
      L.splice(O, 1), w == null || w(L), l == null || l(L.map((T) => T.path));
    },
    customRequest: U || ze,
    beforeUpload: async (v, O) => {
      if (b && !await b(v, O) || W.current)
        return !1;
      W.current = !0;
      let L = O;
      if (typeof I == "number") {
        const R = I - k.length;
        L = O.slice(0, R < 0 ? 0 : R);
      } else if (I === 1)
        L = O.slice(0, 1);
      else if (L.length === 0)
        return W.current = !1, !1;
      Y((R) => [...I === 1 ? [] : R, ...L.map((P) => ({
        ...P,
        size: P.size,
        uid: P.uid,
        name: P.name,
        status: "uploading"
      }))]);
      const T = (await t(L)).filter((R) => R), Z = I === 1 ? T : [...k.filter((R) => !T.some((P) => P.uid === R.uid)), ...T];
      return W.current = !1, w == null || w(Z), l == null || l(Z.map((R) => R.path)), !1;
    },
    progress: s && {
      ...s,
      format: A
    },
    showUploadList: y ? {
      ...p,
      showDownloadIcon: d || p.showDownloadIcon,
      showRemoveIcon: C || p.showRemoveIcon,
      showPreviewIcon: u || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? j({
        slots: e,
        setSlotParams: a,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? j({
        slots: e,
        setSlotParams: a,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? j({
        slots: e,
        setSlotParams: a,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? j({
        slots: e,
        setSlotParams: a,
        key: "showUploadList.extra"
      }) : p.extra
    } : r
  });
});
export {
  Ct as Upload,
  Ct as default
};
