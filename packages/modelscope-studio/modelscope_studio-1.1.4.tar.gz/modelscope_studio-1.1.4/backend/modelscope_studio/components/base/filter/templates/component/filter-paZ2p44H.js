import { g as V, w as p, i as Y } from "./Index-CvWXnwRQ.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, G = window.ms_globals.React.useState, J = window.ms_globals.React.useEffect, y = window.ms_globals.ReactDOM.createPortal, H = window.ms_globals.internalContext.useContextPropsContext, Q = window.ms_globals.internalContext.ContextPropsProvider;
var O = {
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
var X = z, Z = Symbol.for("react.element"), $ = Symbol.for("react.fragment"), ee = Object.prototype.hasOwnProperty, te = X.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, se = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, e, o) {
  var r, l = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (r in e) ee.call(e, r) && !se.hasOwnProperty(r) && (l[r] = e[r]);
  if (n && n.defaultProps) for (r in e = n.defaultProps, e) l[r] === void 0 && (l[r] = e[r]);
  return {
    $$typeof: Z,
    type: n,
    key: t,
    ref: s,
    props: l,
    _owner: te.current
  };
}
g.Fragment = $;
g.jsx = F;
g.jsxs = F;
O.exports = g;
var ne = O.exports;
const {
  SvelteComponent: oe,
  assign: x,
  binding_callbacks: C,
  check_outros: re,
  children: T,
  claim_element: j,
  claim_space: le,
  component_subscribe: R,
  compute_slots: ie,
  create_slot: ce,
  detach: a,
  element: D,
  empty: S,
  exclude_internal_props: E,
  get_all_dirty_from_scope: ue,
  get_slot_changes: ae,
  group_outros: fe,
  init: _e,
  insert_hydration: m,
  safe_not_equal: de,
  set_custom_element_data: L,
  space: pe,
  transition_in: w,
  transition_out: v,
  update_slot_base: me
} = window.__gradio__svelte__internal, {
  beforeUpdate: we,
  getContext: ge,
  onDestroy: be,
  setContext: ve
} = window.__gradio__svelte__internal;
function P(n) {
  let e, o;
  const r = (
    /*#slots*/
    n[7].default
  ), l = ce(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = D("svelte-slot"), l && l.c(), this.h();
    },
    l(t) {
      e = j(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = T(e);
      l && l.l(s), s.forEach(a), this.h();
    },
    h() {
      L(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      m(t, e, s), l && l.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      l && l.p && (!o || s & /*$$scope*/
      64) && me(
        l,
        r,
        t,
        /*$$scope*/
        t[6],
        o ? ae(
          r,
          /*$$scope*/
          t[6],
          s,
          null
        ) : ue(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      o || (w(l, t), o = !0);
    },
    o(t) {
      v(l, t), o = !1;
    },
    d(t) {
      t && a(e), l && l.d(t), n[9](null);
    }
  };
}
function he(n) {
  let e, o, r, l, t = (
    /*$$slots*/
    n[4].default && P(n)
  );
  return {
    c() {
      e = D("react-portal-target"), o = pe(), t && t.c(), r = S(), this.h();
    },
    l(s) {
      e = j(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), T(e).forEach(a), o = le(s), t && t.l(s), r = S(), this.h();
    },
    h() {
      L(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      m(s, e, c), n[8](e), m(s, o, c), t && t.m(s, c), m(s, r, c), l = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && w(t, 1)) : (t = P(s), t.c(), w(t, 1), t.m(r.parentNode, r)) : t && (fe(), v(t, 1, 1, () => {
        t = null;
      }), re());
    },
    i(s) {
      l || (w(t), l = !0);
    },
    o(s) {
      v(t), l = !1;
    },
    d(s) {
      s && (a(e), a(o), a(r)), n[8](null), t && t.d(s);
    }
  };
}
function k(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function ye(n, e, o) {
  let r, l, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = ie(t);
  let {
    svelteInit: u
  } = e;
  const f = p(k(e)), _ = p();
  R(n, _, (i) => o(0, r = i));
  const d = p();
  R(n, d, (i) => o(1, l = i));
  const h = [], A = ge("$$ms-gr-react-wrapper"), {
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W
  } = V() || {}, q = u({
    parent: A,
    props: f,
    target: _,
    slot: d,
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W,
    onDestroy(i) {
      h.push(i);
    }
  });
  ve("$$ms-gr-react-wrapper", q), we(() => {
    f.set(k(e));
  }), be(() => {
    h.forEach((i) => i());
  });
  function K(i) {
    C[i ? "unshift" : "push"](() => {
      r = i, _.set(r);
    });
  }
  function U(i) {
    C[i ? "unshift" : "push"](() => {
      l = i, d.set(l);
    });
  }
  return n.$$set = (i) => {
    o(17, e = x(x({}, e), E(i))), "svelteInit" in i && o(5, u = i.svelteInit), "$$scope" in i && o(6, s = i.$$scope);
  }, e = E(e), [r, l, _, d, c, u, s, t, K, U];
}
class xe extends oe {
  constructor(e) {
    super(), _e(this, e, ye, he, de, {
      svelteInit: 5
    });
  }
}
const I = window.ms_globals.rerender, b = window.ms_globals.tree;
function Ce(n, e = {}) {
  function o(r) {
    const l = p(), t = new xe({
      ...r,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: l,
            reactComponent: n,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: e.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, u = s.parent ?? b;
          return u.nodes = [...u.nodes, c], I({
            createPortal: y,
            node: b
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((f) => f.svelteInstance !== l), I({
              createPortal: y,
              node: b
            });
          }), c;
        },
        ...r.props
      }
    });
    return l.set(t), t;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(o);
    });
  });
}
function Re(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Se(n, e = !1) {
  try {
    if (Y(n))
      return n;
    if (e && !Re(n))
      return;
    if (typeof n == "string") {
      let o = n.trim();
      return o.startsWith(";") && (o = o.slice(1)), o.endsWith(";") && (o = o.slice(0, -1)), new Function(`return (...args) => (${o})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Ee(n, e) {
  return B(() => Se(n, e), [n, e]);
}
const ke = Ce(({
  children: n,
  paramsMapping: e,
  asItem: o
}) => {
  const r = Ee(e), [l, t] = G(void 0), {
    forceClone: s,
    ctx: c
  } = H();
  return J(() => {
    r ? t(r(c)) : o && t(c == null ? void 0 : c[o]);
  }, [o, c, r]), /* @__PURE__ */ ne.jsx(Q, {
    forceClone: s,
    ctx: l,
    children: n
  });
});
export {
  ke as Filter,
  ke as default
};
