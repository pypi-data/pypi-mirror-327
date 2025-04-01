import { g as B, w as m, c as G } from "./Index-Dy-BQ0pu.js";
const z = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, H = window.ms_globals.createItemsContext.createItemsContext;
var P = {
  exports: {}
}, b = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J = z, V = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function T(l, e, r) {
  var o, n = {}, t = null, s = null;
  r !== void 0 && (t = "" + r), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (o in e) Q.call(e, o) && !Z.hasOwnProperty(o) && (n[o] = e[o]);
  if (l && l.defaultProps) for (o in e = l.defaultProps, e) n[o] === void 0 && (n[o] = e[o]);
  return {
    $$typeof: V,
    type: l,
    key: t,
    ref: s,
    props: n,
    _owner: X.current
  };
}
b.Fragment = Y;
b.jsx = T;
b.jsxs = T;
P.exports = b;
var $ = P.exports;
const {
  SvelteComponent: ee,
  assign: I,
  binding_callbacks: x,
  check_outros: te,
  children: j,
  claim_element: D,
  claim_space: se,
  component_subscribe: k,
  compute_slots: ne,
  create_slot: oe,
  detach: u,
  element: L,
  empty: E,
  exclude_internal_props: R,
  get_all_dirty_from_scope: le,
  get_slot_changes: re,
  group_outros: ae,
  init: ie,
  insert_hydration: p,
  safe_not_equal: ce,
  set_custom_element_data: N,
  space: ue,
  transition_in: g,
  transition_out: w,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: fe,
  getContext: de,
  onDestroy: me,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(l) {
  let e, r;
  const o = (
    /*#slots*/
    l[7].default
  ), n = oe(
    o,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      e = L("svelte-slot"), n && n.c(), this.h();
    },
    l(t) {
      e = D(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(e);
      n && n.l(s), s.forEach(u), this.h();
    },
    h() {
      N(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      p(t, e, s), n && n.m(e, null), l[9](e), r = !0;
    },
    p(t, s) {
      n && n.p && (!r || s & /*$$scope*/
      64) && _e(
        n,
        o,
        t,
        /*$$scope*/
        t[6],
        r ? re(
          o,
          /*$$scope*/
          t[6],
          s,
          null
        ) : le(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      r || (g(n, t), r = !0);
    },
    o(t) {
      w(n, t), r = !1;
    },
    d(t) {
      t && u(e), n && n.d(t), l[9](null);
    }
  };
}
function ge(l) {
  let e, r, o, n, t = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      e = L("react-portal-target"), r = ue(), t && t.c(), o = E(), this.h();
    },
    l(s) {
      e = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(e).forEach(u), r = se(s), t && t.l(s), o = E(), this.h();
    },
    h() {
      N(e, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, e, i), l[8](e), p(s, r, i), t && t.m(s, i), p(s, o, i), n = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, i), i & /*$$slots*/
      16 && g(t, 1)) : (t = S(s), t.c(), g(t, 1), t.m(o.parentNode, o)) : t && (ae(), w(t, 1, 1, () => {
        t = null;
      }), te());
    },
    i(s) {
      n || (g(t), n = !0);
    },
    o(s) {
      w(t), n = !1;
    },
    d(s) {
      s && (u(e), u(r), u(o)), l[8](null), t && t.d(s);
    }
  };
}
function C(l) {
  const {
    svelteInit: e,
    ...r
  } = l;
  return r;
}
function be(l, e, r) {
  let o, n, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const i = ne(t);
  let {
    svelteInit: c
  } = e;
  const _ = m(C(e)), f = m();
  k(l, f, (a) => r(0, o = a));
  const d = m();
  k(l, d, (a) => r(1, n = a));
  const v = [], A = de("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = B() || {}, F = c({
    parent: A,
    props: _,
    target: f,
    slot: d,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      v.push(a);
    }
  });
  pe("$$ms-gr-react-wrapper", F), fe(() => {
    _.set(C(e));
  }), me(() => {
    v.forEach((a) => a());
  });
  function M(a) {
    x[a ? "unshift" : "push"](() => {
      o = a, f.set(o);
    });
  }
  function W(a) {
    x[a ? "unshift" : "push"](() => {
      n = a, d.set(n);
    });
  }
  return l.$$set = (a) => {
    r(17, e = I(I({}, e), R(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, e = R(e), [o, n, f, d, i, c, s, t, M, W];
}
class he extends ee {
  constructor(e) {
    super(), ie(this, e, be, ge, ce, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function we(l, e = {}) {
  function r(o) {
    const n = m(), t = new he({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: l,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? h;
          return c.nodes = [...c.nodes, i], O({
            createPortal: y,
            node: h
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== n), O({
              createPortal: y,
              node: h
            });
          }), i;
        },
        ...o.props
      }
    });
    return n.set(t), t;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(r);
    });
  });
}
const {
  useItems: Ie,
  withItemsContextProvider: xe,
  ItemHandler: ve
} = H("antd-menu-items"), ke = we((l) => /* @__PURE__ */ $.jsx(ve, {
  ...l,
  allowedSlots: ["default"],
  itemProps: (e, r) => ({
    ...e,
    className: G(e.className, e.type ? `ms-gr-antd-menu-item-${e.type}` : "ms-gr-antd-menu-item", r.default.length > 0 ? "ms-gr-antd-menu-item-submenu" : "")
  }),
  itemChildren: (e) => e.default.length > 0 ? e.default : void 0
}));
export {
  ke as MenuItem,
  ke as default
};
