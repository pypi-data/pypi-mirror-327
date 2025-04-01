import { g as G, w as p } from "./Index-BoEqYwCh.js";
const B = window.ms_globals.React, y = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Checkbox;
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
var M = B, V = Symbol.for("react.element"), Y = Symbol.for("react.fragment"), H = Object.prototype.hasOwnProperty, Q = M.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, X = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(r, t, l) {
  var n, o = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (n in t) H.call(t, n) && !X.hasOwnProperty(n) && (o[n] = t[n]);
  if (r && r.defaultProps) for (n in t = r.defaultProps, t) o[n] === void 0 && (o[n] = t[n]);
  return {
    $$typeof: V,
    type: r,
    key: e,
    ref: s,
    props: o,
    _owner: Q.current
  };
}
g.Fragment = Y;
g.jsx = C;
g.jsxs = C;
T.exports = g;
var Z = T.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: I,
  check_outros: ee,
  children: j,
  claim_element: D,
  claim_space: te,
  component_subscribe: x,
  compute_slots: se,
  create_slot: oe,
  detach: _,
  element: L,
  empty: E,
  exclude_internal_props: R,
  get_all_dirty_from_scope: ne,
  get_slot_changes: re,
  group_outros: le,
  init: ce,
  insert_hydration: m,
  safe_not_equal: ie,
  set_custom_element_data: A,
  space: ae,
  transition_in: b,
  transition_out: h,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: pe
} = window.__gradio__svelte__internal;
function S(r) {
  let t, l;
  const n = (
    /*#slots*/
    r[7].default
  ), o = oe(
    n,
    r,
    /*$$scope*/
    r[6],
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
      m(e, t, s), o && o.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      o && o.p && (!l || s & /*$$scope*/
      64) && _e(
        o,
        n,
        e,
        /*$$scope*/
        e[6],
        l ? re(
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
      l || (b(o, e), l = !0);
    },
    o(e) {
      h(o, e), l = !1;
    },
    d(e) {
      e && _(t), o && o.d(e), r[9](null);
    }
  };
}
function me(r) {
  let t, l, n, o, e = (
    /*$$slots*/
    r[4].default && S(r)
  );
  return {
    c() {
      t = L("react-portal-target"), l = ae(), e && e.c(), n = E(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(_), l = te(s), e && e.l(s), n = E(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, i) {
      m(s, t, i), r[8](t), m(s, l, i), e && e.m(s, i), m(s, n, i), o = !0;
    },
    p(s, [i]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = S(s), e.c(), b(e, 1), e.m(n.parentNode, n)) : e && (le(), h(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(s) {
      o || (b(e), o = !0);
    },
    o(s) {
      h(e), o = !1;
    },
    d(s) {
      s && (_(t), _(l), _(n)), r[8](null), e && e.d(s);
    }
  };
}
function O(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function be(r, t, l) {
  let n, o, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const i = se(e);
  let {
    svelteInit: a
  } = t;
  const u = p(O(t)), f = p();
  x(r, f, (c) => l(0, n = c));
  const d = p();
  x(r, d, (c) => l(1, o = c));
  const v = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, F = a({
    parent: N,
    props: u,
    target: f,
    slot: d,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(c) {
      v.push(c);
    }
  });
  pe("$$ms-gr-react-wrapper", F), ue(() => {
    u.set(O(t));
  }), de(() => {
    v.forEach((c) => c());
  });
  function W(c) {
    I[c ? "unshift" : "push"](() => {
      n = c, f.set(n);
    });
  }
  function z(c) {
    I[c ? "unshift" : "push"](() => {
      o = c, d.set(o);
    });
  }
  return r.$$set = (c) => {
    l(17, t = k(k({}, t), R(c))), "svelteInit" in c && l(5, a = c.svelteInit), "$$scope" in c && l(6, s = c.$$scope);
  }, t = R(t), [n, o, f, d, i, a, s, e, W, z];
}
class ge extends $ {
  constructor(t) {
    super(), ce(this, t, be, me, ie, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function we(r, t = {}) {
  function l(n) {
    const o = p(), e = new ge({
      ...n,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, a = s.parent ?? w;
          return a.nodes = [...a.nodes, i], P({
            createPortal: y,
            node: w
          }), s.onDestroy(() => {
            a.nodes = a.nodes.filter((u) => u.svelteInstance !== o), P({
              createPortal: y,
              node: w
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
      n(l);
    });
  });
}
const ve = we(({
  onValueChange: r,
  onChange: t,
  elRef: l,
  ...n
}) => /* @__PURE__ */ Z.jsx(J, {
  ...n,
  ref: l,
  onChange: (o) => {
    t == null || t(o), r(o.target.checked);
  }
}));
export {
  ve as Checkbox,
  ve as default
};
