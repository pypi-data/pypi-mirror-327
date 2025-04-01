import { i as ge, a as z, r as ve, g as ye, w as P, b as be } from "./Index-B_vJtcGi.js";
const R = window.ms_globals.React, oe = window.ms_globals.React.useMemo, we = window.ms_globals.React.forwardRef, he = window.ms_globals.React.useRef, _e = window.ms_globals.React.useState, Ie = window.ms_globals.React.useEffect, q = window.ms_globals.ReactDOM.createPortal, xe = window.ms_globals.internalContext.useContextPropsContext, Ee = window.ms_globals.internalContext.ContextPropsProvider, Re = window.ms_globals.antd.Upload;
var Ce = /\s/;
function Se(e) {
  for (var t = e.length; t-- && Ce.test(e.charAt(t)); )
    ;
  return t;
}
var Fe = /^\s+/;
function Le(e) {
  return e && e.slice(0, Se(e) + 1).replace(Fe, "");
}
var K = NaN, ke = /^[-+]0x[0-9a-f]+$/i, Ue = /^0b[01]+$/i, Te = /^0o[0-7]+$/i, Oe = parseInt;
function J(e) {
  if (typeof e == "number")
    return e;
  if (ge(e))
    return K;
  if (z(e)) {
    var t = typeof e.valueOf == "function" ? e.valueOf() : e;
    e = z(t) ? t + "" : t;
  }
  if (typeof e != "string")
    return e === 0 ? e : +e;
  e = Le(e);
  var r = Ue.test(e);
  return r || Te.test(e) ? Oe(e.slice(2), r ? 2 : 8) : ke.test(e) ? K : +e;
}
var A = function() {
  return ve.Date.now();
}, Pe = "Expected a function", je = Math.max, De = Math.min;
function Ne(e, t, r) {
  var s, i, n, o, c, u, I = 0, g = !1, l = !1, w = !0;
  if (typeof e != "function")
    throw new TypeError(Pe);
  t = J(t) || 0, z(r) && (g = !!r.leading, l = "maxWait" in r, n = l ? je(J(r.maxWait) || 0, t) : n, w = "trailing" in r ? !!r.trailing : w);
  function f(d) {
    var x = s, L = i;
    return s = i = void 0, I = d, o = e.apply(L, x), o;
  }
  function _(d) {
    return I = d, c = setTimeout(h, t), g ? f(d) : o;
  }
  function v(d) {
    var x = d - u, L = d - I, O = t - x;
    return l ? De(O, n - L) : O;
  }
  function m(d) {
    var x = d - u, L = d - I;
    return u === void 0 || x >= t || x < 0 || l && L >= n;
  }
  function h() {
    var d = A();
    if (m(d))
      return p(d);
    c = setTimeout(h, v(d));
  }
  function p(d) {
    return c = void 0, w && s ? f(d) : (s = i = void 0, o);
  }
  function F() {
    c !== void 0 && clearTimeout(c), I = 0, s = u = i = c = void 0;
  }
  function a() {
    return c === void 0 ? o : p(A());
  }
  function S() {
    var d = A(), x = m(d);
    if (s = arguments, i = this, u = d, x) {
      if (c === void 0)
        return _(u);
      if (l)
        return clearTimeout(c), c = setTimeout(h, t), f(u);
    }
    return c === void 0 && (c = setTimeout(h, t)), o;
  }
  return S.cancel = F, S.flush = a, S;
}
var ie = {
  exports: {}
}, N = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var We = R, Ae = Symbol.for("react.element"), Me = Symbol.for("react.fragment"), qe = Object.prototype.hasOwnProperty, ze = We.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Be = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function se(e, t, r) {
  var s, i = {}, n = null, o = null;
  r !== void 0 && (n = "" + r), t.key !== void 0 && (n = "" + t.key), t.ref !== void 0 && (o = t.ref);
  for (s in t) qe.call(t, s) && !Be.hasOwnProperty(s) && (i[s] = t[s]);
  if (e && e.defaultProps) for (s in t = e.defaultProps, t) i[s] === void 0 && (i[s] = t[s]);
  return {
    $$typeof: Ae,
    type: e,
    key: n,
    ref: o,
    props: i,
    _owner: ze.current
  };
}
N.Fragment = Me;
N.jsx = se;
N.jsxs = se;
ie.exports = N;
var C = ie.exports;
const {
  SvelteComponent: Ge,
  assign: X,
  binding_callbacks: Y,
  check_outros: He,
  children: ce,
  claim_element: le,
  claim_space: Ke,
  component_subscribe: Q,
  compute_slots: Je,
  create_slot: Xe,
  detach: T,
  element: ae,
  empty: Z,
  exclude_internal_props: V,
  get_all_dirty_from_scope: Ye,
  get_slot_changes: Qe,
  group_outros: Ze,
  init: Ve,
  insert_hydration: j,
  safe_not_equal: $e,
  set_custom_element_data: de,
  space: et,
  transition_in: D,
  transition_out: B,
  update_slot_base: tt
} = window.__gradio__svelte__internal, {
  beforeUpdate: nt,
  getContext: rt,
  onDestroy: ot,
  setContext: it
} = window.__gradio__svelte__internal;
function $(e) {
  let t, r;
  const s = (
    /*#slots*/
    e[7].default
  ), i = Xe(
    s,
    e,
    /*$$scope*/
    e[6],
    null
  );
  return {
    c() {
      t = ae("svelte-slot"), i && i.c(), this.h();
    },
    l(n) {
      t = le(n, "SVELTE-SLOT", {
        class: !0
      });
      var o = ce(t);
      i && i.l(o), o.forEach(T), this.h();
    },
    h() {
      de(t, "class", "svelte-1rt0kpf");
    },
    m(n, o) {
      j(n, t, o), i && i.m(t, null), e[9](t), r = !0;
    },
    p(n, o) {
      i && i.p && (!r || o & /*$$scope*/
      64) && tt(
        i,
        s,
        n,
        /*$$scope*/
        n[6],
        r ? Qe(
          s,
          /*$$scope*/
          n[6],
          o,
          null
        ) : Ye(
          /*$$scope*/
          n[6]
        ),
        null
      );
    },
    i(n) {
      r || (D(i, n), r = !0);
    },
    o(n) {
      B(i, n), r = !1;
    },
    d(n) {
      n && T(t), i && i.d(n), e[9](null);
    }
  };
}
function st(e) {
  let t, r, s, i, n = (
    /*$$slots*/
    e[4].default && $(e)
  );
  return {
    c() {
      t = ae("react-portal-target"), r = et(), n && n.c(), s = Z(), this.h();
    },
    l(o) {
      t = le(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), ce(t).forEach(T), r = Ke(o), n && n.l(o), s = Z(), this.h();
    },
    h() {
      de(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      j(o, t, c), e[8](t), j(o, r, c), n && n.m(o, c), j(o, s, c), i = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? n ? (n.p(o, c), c & /*$$slots*/
      16 && D(n, 1)) : (n = $(o), n.c(), D(n, 1), n.m(s.parentNode, s)) : n && (Ze(), B(n, 1, 1, () => {
        n = null;
      }), He());
    },
    i(o) {
      i || (D(n), i = !0);
    },
    o(o) {
      B(n), i = !1;
    },
    d(o) {
      o && (T(t), T(r), T(s)), e[8](null), n && n.d(o);
    }
  };
}
function ee(e) {
  const {
    svelteInit: t,
    ...r
  } = e;
  return r;
}
function ct(e, t, r) {
  let s, i, {
    $$slots: n = {},
    $$scope: o
  } = t;
  const c = Je(n);
  let {
    svelteInit: u
  } = t;
  const I = P(ee(t)), g = P();
  Q(e, g, (a) => r(0, s = a));
  const l = P();
  Q(e, l, (a) => r(1, i = a));
  const w = [], f = rt("$$ms-gr-react-wrapper"), {
    slotKey: _,
    slotIndex: v,
    subSlotIndex: m
  } = ye() || {}, h = u({
    parent: f,
    props: I,
    target: g,
    slot: l,
    slotKey: _,
    slotIndex: v,
    subSlotIndex: m,
    onDestroy(a) {
      w.push(a);
    }
  });
  it("$$ms-gr-react-wrapper", h), nt(() => {
    I.set(ee(t));
  }), ot(() => {
    w.forEach((a) => a());
  });
  function p(a) {
    Y[a ? "unshift" : "push"](() => {
      s = a, g.set(s);
    });
  }
  function F(a) {
    Y[a ? "unshift" : "push"](() => {
      i = a, l.set(i);
    });
  }
  return e.$$set = (a) => {
    r(17, t = X(X({}, t), V(a))), "svelteInit" in a && r(5, u = a.svelteInit), "$$scope" in a && r(6, o = a.$$scope);
  }, t = V(t), [s, i, g, l, c, u, o, n, p, F];
}
class lt extends Ge {
  constructor(t) {
    super(), Ve(this, t, ct, st, $e, {
      svelteInit: 5
    });
  }
}
const te = window.ms_globals.rerender, M = window.ms_globals.tree;
function at(e, t = {}) {
  function r(s) {
    const i = P(), n = new lt({
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
          }, u = o.parent ?? M;
          return u.nodes = [...u.nodes, c], te({
            createPortal: q,
            node: M
          }), o.onDestroy(() => {
            u.nodes = u.nodes.filter((I) => I.svelteInstance !== i), te({
              createPortal: q,
              node: M
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
function dt(e) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(e.trim());
}
function ut(e, t = !1) {
  try {
    if (be(e))
      return e;
    if (t && !dt(e))
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
function b(e, t) {
  return oe(() => ut(e, t), [e, t]);
}
const ft = ["animationIterationCount", "borderImageOutset", "borderImageSlice", "borderImageWidth", "boxFlex", "boxFlexGroup", "boxOrdinalGroup", "columnCount", "columns", "flex", "flexGrow", "flexPositive", "flexShrink", "flexNegative", "flexOrder", "gridArea", "gridColumn", "gridColumnEnd", "gridColumnStart", "gridRow", "gridRowEnd", "gridRowStart", "lineClamp", "lineHeight", "opacity", "order", "orphans", "tabSize", "widows", "zIndex", "zoom", "fontWeight", "letterSpacing", "lineHeight"];
function mt(e) {
  return e ? Object.keys(e).reduce((t, r) => {
    const s = e[r];
    return t[r] = pt(r, s), t;
  }, {}) : {};
}
function pt(e, t) {
  return typeof t == "number" && !ft.includes(e) ? t + "px" : t;
}
function G(e) {
  const t = [], r = e.cloneNode(!1);
  if (e._reactElement) {
    const i = R.Children.toArray(e._reactElement.props.children).map((n) => {
      if (R.isValidElement(n) && n.props.__slot__) {
        const {
          portals: o,
          clonedElement: c
        } = G(n.props.el);
        return R.cloneElement(n, {
          ...n.props,
          el: c,
          children: [...R.Children.toArray(n.props.children), ...o]
        });
      }
      return null;
    });
    return i.originalChildren = e._reactElement.props.children, t.push(q(R.cloneElement(e._reactElement, {
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
      useCapture: u
    }) => {
      r.addEventListener(c, o, u);
    });
  });
  const s = Array.from(e.childNodes);
  for (let i = 0; i < s.length; i++) {
    const n = s[i];
    if (n.nodeType === 1) {
      const {
        clonedElement: o,
        portals: c
      } = G(n);
      t.push(...c), r.appendChild(o);
    } else n.nodeType === 3 && r.appendChild(n.cloneNode());
  }
  return {
    clonedElement: r,
    portals: t
  };
}
function wt(e, t) {
  e && (typeof e == "function" ? e(t) : e.current = t);
}
const ne = we(({
  slot: e,
  clone: t,
  className: r,
  style: s,
  observeAttributes: i
}, n) => {
  const o = he(), [c, u] = _e([]), {
    forceClone: I
  } = xe(), g = I ? !0 : t;
  return Ie(() => {
    var v;
    if (!o.current || !e)
      return;
    let l = e;
    function w() {
      let m = l;
      if (l.tagName.toLowerCase() === "svelte-slot" && l.children.length === 1 && l.children[0] && (m = l.children[0], m.tagName.toLowerCase() === "react-portal-target" && m.children[0] && (m = m.children[0])), wt(n, m), r && m.classList.add(...r.split(" ")), s) {
        const h = mt(s);
        Object.keys(h).forEach((p) => {
          m.style[p] = h[p];
        });
      }
    }
    let f = null, _ = null;
    if (g && window.MutationObserver) {
      let m = function() {
        var a, S, d;
        (a = o.current) != null && a.contains(l) && ((S = o.current) == null || S.removeChild(l));
        const {
          portals: p,
          clonedElement: F
        } = G(e);
        l = F, u(p), l.style.display = "contents", _ && clearTimeout(_), _ = setTimeout(() => {
          w();
        }, 50), (d = o.current) == null || d.appendChild(l);
      };
      m();
      const h = Ne(() => {
        m(), f == null || f.disconnect(), f == null || f.observe(e, {
          childList: !0,
          subtree: !0,
          attributes: i
        });
      }, 50);
      f = new window.MutationObserver(h), f.observe(e, {
        attributes: !0,
        childList: !0,
        subtree: !0
      });
    } else
      l.style.display = "contents", w(), (v = o.current) == null || v.appendChild(l);
    return () => {
      var m, h;
      l.style.display = "", (m = o.current) != null && m.contains(l) && ((h = o.current) == null || h.removeChild(l)), f == null || f.disconnect();
    };
  }, [e, g, r, s, n, i]), R.createElement("react-child", {
    ref: o,
    style: {
      display: "contents"
    }
  }, ...c);
}), ht = ({
  children: e,
  ...t
}) => /* @__PURE__ */ C.jsx(C.Fragment, {
  children: e(t)
});
function _t(e) {
  return R.createElement(ht, {
    children: e
  });
}
function re(e, t) {
  return e ? t != null && t.forceClone || t != null && t.params ? _t((r) => /* @__PURE__ */ C.jsx(Ee, {
    forceClone: t == null ? void 0 : t.forceClone,
    params: t == null ? void 0 : t.params,
    children: /* @__PURE__ */ C.jsx(ne, {
      slot: e,
      clone: t == null ? void 0 : t.clone,
      ...r
    })
  })) : /* @__PURE__ */ C.jsx(ne, {
    slot: e,
    clone: t == null ? void 0 : t.clone
  }) : null;
}
function U({
  key: e,
  slots: t,
  targets: r
}, s) {
  return t[e] ? (...i) => r ? r.map((n, o) => /* @__PURE__ */ C.jsx(R.Fragment, {
    children: re(n, {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }, o)) : /* @__PURE__ */ C.jsx(C.Fragment, {
    children: re(t[e], {
      clone: !0,
      params: i,
      forceClone: !0
    })
  }) : void 0;
}
function It(e) {
  return typeof e == "object" && e !== null ? e : {};
}
const vt = at(({
  slots: e,
  upload: t,
  showUploadList: r,
  progress: s,
  beforeUpload: i,
  customRequest: n,
  previewFile: o,
  isImageUrl: c,
  itemRender: u,
  iconRender: I,
  data: g,
  onChange: l,
  onValueChange: w,
  onRemove: f,
  fileList: _,
  setSlotParams: v,
  ...m
}) => {
  const h = e["showUploadList.downloadIcon"] || e["showUploadList.removeIcon"] || e["showUploadList.previewIcon"] || e["showUploadList.extra"] || typeof r == "object", p = It(r), F = b(p.showPreviewIcon), a = b(p.showRemoveIcon), S = b(p.showDownloadIcon), d = b(i), x = b(n), L = b(s == null ? void 0 : s.format), O = b(o), ue = b(c), fe = b(u), me = b(I), pe = b(g), H = oe(() => (_ == null ? void 0 : _.map((y) => ({
    ...y,
    name: y.orig_name || y.path,
    uid: y.url || y.path,
    status: "done"
  }))) || [], [_]);
  return /* @__PURE__ */ C.jsx(Re.Dragger, {
    ...m,
    fileList: H,
    data: pe || g,
    previewFile: O,
    isImageUrl: ue,
    itemRender: e.itemRender ? U({
      slots: e,
      setSlotParams: v,
      key: "itemRender"
    }) : fe,
    iconRender: e.iconRender ? U({
      slots: e,
      setSlotParams: v,
      key: "iconRender"
    }) : me,
    onRemove: (y) => {
      f == null || f(y);
      const W = H.findIndex((E) => E.uid === y.uid), k = _.slice();
      k.splice(W, 1), w == null || w(k), l == null || l(k.map((E) => E.path));
    },
    beforeUpload: async (y, W) => {
      if (d && !await d(y, W))
        return !1;
      const k = (await t([y])).filter((E) => E);
      return w == null || w([..._, ...k]), l == null || l([..._.map((E) => E.path), ...k.map((E) => E.path)]), !1;
    },
    maxCount: 1,
    customRequest: x,
    progress: s && {
      ...s,
      format: L
    },
    showUploadList: h ? {
      ...p,
      showDownloadIcon: S || p.showDownloadIcon,
      showRemoveIcon: a || p.showRemoveIcon,
      showPreviewIcon: F || p.showPreviewIcon,
      downloadIcon: e["showUploadList.downloadIcon"] ? U({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.downloadIcon"
      }) : p.downloadIcon,
      removeIcon: e["showUploadList.removeIcon"] ? U({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.removeIcon"
      }) : p.removeIcon,
      previewIcon: e["showUploadList.previewIcon"] ? U({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.previewIcon"
      }) : p.previewIcon,
      extra: e["showUploadList.extra"] ? U({
        slots: e,
        setSlotParams: v,
        key: "showUploadList.extra"
      }) : p.extra
    } : r
  });
});
export {
  vt as UploadDragger,
  vt as default
};
