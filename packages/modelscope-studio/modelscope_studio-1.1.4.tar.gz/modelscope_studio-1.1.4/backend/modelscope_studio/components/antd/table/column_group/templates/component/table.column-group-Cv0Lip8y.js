import { g as B, w as m } from "./Index-DKAwaO6h.js";
const z = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, w = window.ms_globals.createItemsContext.createItemsContext;
var T = {
  exports: {}
}, g = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var J = z, M = Symbol.for("react.element"), V = Symbol.for("react.fragment"), Y = Object.prototype.hasOwnProperty, Q = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, X = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(l, t, r) {
  var n, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Y.call(t, n) && !X.hasOwnProperty(n) && (o[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: M,
    type: l,
    key: e,
    ref: s,
    props: o,
    _owner: Q.current
  };
}
g.Fragment = V;
g.jsx = j;
g.jsxs = j;
T.exports = g;
var Z = T.exports;
const {
  SvelteComponent: $,
  assign: x,
  binding_callbacks: C,
  check_outros: ee,
  children: D,
  claim_element: L,
  claim_space: te,
  component_subscribe: k,
  compute_slots: se,
  create_slot: oe,
  detach: u,
  element: A,
  empty: E,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ne,
  get_slot_changes: le,
  group_outros: re,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ie,
  set_custom_element_data: N,
  space: ce,
  transition_in: b,
  transition_out: I,
  update_slot_base: ue
} = window.__gradio__svelte__internal, {
  beforeUpdate: _e,
  getContext: fe,
  onDestroy: de,
  setContext: me
} = window.__gradio__svelte__internal;
function S(l) {
  let t, r;
  const n = (
    /*#slots*/
    l[7].default
  ), o = oe(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = A("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = D(t);
      o && o.l(s), s.forEach(u), this.h();
    },
    h() {
      N(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      p(e, t, s), o && o.m(t, null), l[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ue(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        r ? le(
          n,
          /*$$scope*/
          e[6],
          s,
          null
        ) : ne(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      r || (b(o, e), r = !0);
    },
    o(e) {
      I(o, e), r = !1;
    },
    d(e) {
      e && u(t), o && o.d(e), l[9](null);
    }
  };
}
function pe(l) {
  let t, r, n, o, e = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      t = A("react-portal-target"), r = ce(), e && e.c(), n = E(), this.h();
    },
    l(s) {
      t = L(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(t).forEach(u), r = te(s), e && e.l(s), n = E(), this.h();
    },
    h() {
      N(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      p(s, t, i), l[8](t), p(s, r, i), e && e.m(s, i), p(s, n, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = S(s), e.c(), b(e, 1), e.m(n.parentNode, n)) : e && (re(), I(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      o || (b(e), o = !0);
    },
    o(s) {
      I(e), o = !1;
    },
    d(s) {
      s && (u(t), u(r), u(n)), l[8](null), e && e.d(s);
    }
  };
}
function P(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function be(l, t, r) {
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = se(e);
  let {
    svelteInit: c
  } = t;
  const _ = m(P(t)), f = m();
  k(l, f, (a) => r(0, n = a));
  const d = m();
  k(l, d, (a) => r(1, o = a));
  const v = [], q = fe("$$ms-gr-react-wrapper"), {
    slotKey: K,
    slotIndex: U,
    subSlotIndex: F
  } = B() || {}, G = c({
    parent: q,
    props: _,
    target: f,
    slot: d,
    slotKey: K,
    slotIndex: U,
    subSlotIndex: F,
    onDestroy(a) {
      v.push(a);
    }
  });
  me("$$ms-gr-react-wrapper", G), _e(() => {
    _.set(P(t));
  }), de(() => {
    v.forEach((a) => a());
  });
  function H(a) {
    C[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  function W(a) {
    C[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return l.$$set = (a) => {
    r(17, t = x(x({}, t), R(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = R(t), [n, o, f, d, i, c, s, e, H, W];
}
class we extends $ {
  constructor(t) {
    super(), ae(this, t, be, pe, ie, {
      svelteInit: 5
    });
  }
}
const O = window.ms_globals.rerender, h = window.ms_globals.tree;
function ge(l, t = {}) {
  function r(n) {
    const o = m(), e = new we({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, c = s.parent ?? h;
          return c.nodes = [...c.nodes, i], O({
            createPortal: y,
            node: h
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== o), O({
              createPortal: y,
              node: h
            });
          }), i;
        },
        ...n.props
      }
    });
    return o.set(e), e;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(r);
    });
  });
}
const {
  useItems: ve,
  withItemsContextProvider: ye,
  ItemHandler: he
} = w("antd-table-columns");
w("antd-table-row-selection-selections");
w("antd-table-row-selection");
w("antd-table-expandable");
const xe = ge((l) => /* @__PURE__ */ Z.jsx(he, {
  ...l,
  allowedSlots: ["default"],
  itemChildren: (t) => t.default || []
}));
export {
  xe as TableColumnGroup,
  xe as default
};
