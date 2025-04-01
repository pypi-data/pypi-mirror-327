import { b as G, w as p } from "./Index-mcoHlxSs.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal;
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
var J = B, M = Symbol.for("react.element"), V = Symbol.for("react.fragment"), Y = Object.prototype.hasOwnProperty, H = J.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Q = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(l, t, r) {
  var n, o = {}, e = null, s = null;
  r !== void 0 && (e = "" + r), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) Y.call(t, n) && !Q.hasOwnProperty(n) && (o[n] = t[n]);
  if (l && l.defaultProps) for (n in t = l.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: M,
    type: l,
    key: e,
    ref: s,
    props: o,
    _owner: H.current
  };
}
g.Fragment = V;
g.jsx = C;
g.jsxs = C;
T.exports = g;
var ge = T.exports;
const {
  SvelteComponent: X,
  assign: I,
  binding_callbacks: k,
  check_outros: Z,
  children: j,
  claim_element: D,
  claim_space: $,
  component_subscribe: R,
  compute_slots: ee,
  create_slot: te,
  detach: _,
  element: L,
  empty: E,
  exclude_internal_props: S,
  get_all_dirty_from_scope: se,
  get_slot_changes: oe,
  group_outros: ne,
  init: le,
  insert_hydration: m,
  safe_not_equal: re,
  set_custom_element_data: A,
  space: ae,
  transition_in: b,
  transition_out: w,
  update_slot_base: ie
} = window.__gradio__svelte__internal, {
  beforeUpdate: ce,
  getContext: _e,
  onDestroy: ue,
  setContext: fe
} = window.__gradio__svelte__internal;
function x(l) {
  let t, r;
  const n = (
    /*#slots*/
    l[7].default
  ), o = te(
    n,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = L("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(t);
      o && o.l(s), s.forEach(_), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      m(e, t, s), o && o.m(t, null), l[9](t), r = !0;
    },
    p(e, s) {
      o && o.p && (!r || s & /*$$scope*/
      64) && ie(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        r ? oe(
          n,
          /*$$scope*/
          e[6],
          s,
          null
        ) : se(
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
      w(o, e), r = !1;
    },
    d(e) {
      e && _(t), o && o.d(e), l[9](null);
    }
  };
}
function de(l) {
  let t, r, n, o, e = (
    /*$$slots*/
    l[4].default && x(l)
  );
  return {
    c() {
      t = L("react-portal-target"), r = ae(), e && e.c(), n = E(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(_), r = $(s), e && e.l(s), n = E(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      m(s, t, i), l[8](t), m(s, r, i), e && e.m(s, i), m(s, n, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = x(s), e.c(), b(e, 1), e.m(n.parentNode, n)) : e && (ne(), w(e, 1, 1, () => {
        e = null;
      }), Z());
    },
    i(s) {
      o || (b(e), o = !0);
    },
    o(s) {
      w(e), o = !1;
    },
    d(s) {
      s && (_(t), _(r), _(n)), l[8](null), e && e.d(s);
    }
  };
}
function O(l) {
  const {
    svelteInit: t,
    ...r
  } = l;
  return r;
}
function pe(l, t, r) {
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = ee(e);
  let {
    svelteInit: c
  } = t;
  const u = p(O(t)), f = p();
  R(l, f, (a) => r(0, n = a));
  const d = p();
  R(l, d, (a) => r(1, o = a));
  const v = [], N = _e("$$ms-gr-react-wrapper"), {
    slotKey: K,
    slotIndex: U,
    subSlotIndex: q
  } = G() || {}, F = c({
    parent: N,
    props: u,
    target: f,
    slot: d,
    slotKey: K,
    slotIndex: U,
    subSlotIndex: q,
    onDestroy(a) {
      v.push(a);
    }
  });
  fe("$$ms-gr-react-wrapper", F), ce(() => {
    u.set(O(t));
  }), ue(() => {
    v.forEach((a) => a());
  });
  function W(a) {
    k[a ? "unshift" : "push"](() => {
      n = a, f.set(n);
    });
  }
  function z(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return l.$$set = (a) => {
    r(17, t = I(I({}, t), S(a))), "svelteInit" in a && r(5, c = a.svelteInit), "$$scope" in a && r(6, s = a.$$scope);
  }, t = S(t), [n, o, f, d, i, c, s, e, W, z];
}
class me extends X {
  constructor(t) {
    super(), le(this, t, pe, de, re, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, h = window.ms_globals.tree;
function he(l, t = {}) {
  function r(n) {
    const o = p(), e = new me({
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
          return c.nodes = [...c.nodes, i], P({
            createPortal: y,
            node: h
          }), s.onDestroy(() => {
            c.nodes = c.nodes.filter((u) => u.svelteInstance !== o), P({
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
export {
  ge as j,
  he as s
};
