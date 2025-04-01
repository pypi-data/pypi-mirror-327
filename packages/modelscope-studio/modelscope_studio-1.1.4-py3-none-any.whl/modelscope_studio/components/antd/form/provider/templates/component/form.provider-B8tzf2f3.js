import { g as G, w as m } from "./Index-BEu1CFDh.js";
const B = window.ms_globals.React, h = window.ms_globals.ReactDOM.createPortal, J = window.ms_globals.antd.Form;
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
var M = B, Y = Symbol.for("react.element"), H = Symbol.for("react.fragment"), Q = Object.prototype.hasOwnProperty, X = M.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, Z = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function j(l, s, n) {
  var r, o = {}, e = null, t = null;
  n !== void 0 && (e = "" + n), s.key !== void 0 && (e = "" + s.key), s.ref !== void 0 && (t = s.ref);
  for (r in s) Q.call(s, r) && !Z.hasOwnProperty(r) && (o[r] = s[r]);
  if (l && l.defaultProps) for (r in s = l.defaultProps, s) o[r] === void 0 && (o[r] = s[r]);
  return {
    $$typeof: Y,
    type: l,
    key: e,
    ref: t,
    props: o,
    _owner: X.current
  };
}
g.Fragment = H;
g.jsx = j;
g.jsxs = j;
T.exports = g;
var F = T.exports;
const {
  SvelteComponent: $,
  assign: k,
  binding_callbacks: I,
  check_outros: ee,
  children: D,
  claim_element: L,
  claim_space: te,
  component_subscribe: E,
  compute_slots: se,
  create_slot: oe,
  detach: _,
  element: C,
  empty: R,
  exclude_internal_props: O,
  get_all_dirty_from_scope: re,
  get_slot_changes: le,
  group_outros: ne,
  init: ae,
  insert_hydration: p,
  safe_not_equal: ce,
  set_custom_element_data: A,
  space: ie,
  transition_in: b,
  transition_out: v,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: ue,
  getContext: fe,
  onDestroy: de,
  setContext: me
} = window.__gradio__svelte__internal;
function S(l) {
  let s, n;
  const r = (
    /*#slots*/
    l[7].default
  ), o = oe(
    r,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      s = C("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      s = L(e, "SVELTE-SLOT", {
        class: !0
      });
      var t = D(s);
      o && o.l(t), t.forEach(_), this.h();
    },
    h() {
      A(s, "class", "svelte-1rt0kpf");
    },
    m(e, t) {
      p(e, s, t), o && o.m(s, null), l[9](s), n = !0;
    },
    p(e, t) {
      o && o.p && (!n || t & /*$$scope*/
      64) && _e(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        n ? le(
          r,
          /*$$scope*/
          e[6],
          t,
          null
        ) : re(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (b(o, e), n = !0);
    },
    o(e) {
      v(o, e), n = !1;
    },
    d(e) {
      e && _(s), o && o.d(e), l[9](null);
    }
  };
}
function pe(l) {
  let s, n, r, o, e = (
    /*$$slots*/
    l[4].default && S(l)
  );
  return {
    c() {
      s = C("react-portal-target"), n = ie(), e && e.c(), r = R(), this.h();
    },
    l(t) {
      s = L(t, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(s).forEach(_), n = te(t), e && e.l(t), r = R(), this.h();
    },
    h() {
      A(s, "class", "svelte-1rt0kpf");
    },
    m(t, c) {
      p(t, s, c), l[8](s), p(t, n, c), e && e.m(t, c), p(t, r, c), o = !0;
    },
    p(t, [c]) {
      /*$$slots*/
      t[4].default ? e ? (e.p(t, c), c & /*$$slots*/
      16 && b(e, 1)) : (e = S(t), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (ne(), v(e, 1, 1, () => {
        e = null;
      }), ee());
    },
    i(t) {
      o || (b(e), o = !0);
    },
    o(t) {
      v(e), o = !1;
    },
    d(t) {
      t && (_(s), _(n), _(r)), l[8](null), e && e.d(t);
    }
  };
}
function x(l) {
  const {
    svelteInit: s,
    ...n
  } = l;
  return n;
}
function be(l, s, n) {
  let r, o, {
    $$slots: e = {},
    $$scope: t
  } = s;
  const c = se(e);
  let {
    svelteInit: i
  } = s;
  const u = m(x(s)), f = m();
  E(l, f, (a) => n(0, r = a));
  const d = m();
  E(l, d, (a) => n(1, o = a));
  const y = [], N = fe("$$ms-gr-react-wrapper"), {
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U
  } = G() || {}, V = i({
    parent: N,
    props: u,
    target: f,
    slot: d,
    slotKey: q,
    slotIndex: K,
    subSlotIndex: U,
    onDestroy(a) {
      y.push(a);
    }
  });
  me("$$ms-gr-react-wrapper", V), ue(() => {
    u.set(x(s));
  }), de(() => {
    y.forEach((a) => a());
  });
  function W(a) {
    I[a ? "unshift" : "push"](() => {
      r = a, f.set(r);
    });
  }
  function z(a) {
    I[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return l.$$set = (a) => {
    n(17, s = k(k({}, s), O(a))), "svelteInit" in a && n(5, i = a.svelteInit), "$$scope" in a && n(6, t = a.$$scope);
  }, s = O(s), [r, o, f, d, c, i, t, e, W, z];
}
class ge extends $ {
  constructor(s) {
    super(), ae(this, s, be, pe, ce, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, w = window.ms_globals.tree;
function we(l, s = {}) {
  function n(r) {
    const o = m(), e = new ge({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: l,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            ignore: s.ignore,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? w;
          return i.nodes = [...i.nodes, c], P({
            createPortal: h,
            node: w
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((u) => u.svelteInstance !== o), P({
              createPortal: h,
              node: w
            });
          }), c;
        },
        ...r.props
      }
    });
    return o.set(e), e;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(n);
    });
  });
}
const ye = we(({
  onFormChange: l,
  onFormFinish: s,
  ...n
}) => /* @__PURE__ */ F.jsx(J.Provider, {
  ...n,
  onFormChange: (r, o) => {
    l == null || l(r, {
      ...o,
      forms: Object.keys(o.forms).reduce((e, t) => ({
        ...e,
        [t]: o.forms[t].getFieldsValue()
      }), {})
    });
  },
  onFormFinish: (r, o) => {
    s == null || s(r, {
      ...o,
      forms: Object.keys(o.forms).reduce((e, t) => ({
        ...e,
        [t]: o.forms[t].getFieldsValue()
      }), {})
    });
  }
}));
export {
  ye as FormProvider,
  ye as default
};
