import { g as G, w as m, i as J } from "./Index-BqjcRVuo.js";
const z = window.ms_globals.React, B = window.ms_globals.React.useMemo, y = window.ms_globals.ReactDOM.createPortal, V = window.ms_globals.antd.Affix;
var C = {
  exports: {}
}, w = {};
/**
 * @license React
 * react-jsx-runtime.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
var Y = z, H = Symbol.for("react.element"), Q = Symbol.for("react.fragment"), X = Object.prototype.hasOwnProperty, Z = Y.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $ = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function F(n, e, o) {
  var l, r = {}, t = null, s = null;
  o !== void 0 && (t = "" + o), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (s = e.ref);
  for (l in e) X.call(e, l) && !$.hasOwnProperty(l) && (r[l] = e[l]);
  if (n && n.defaultProps) for (l in e = n.defaultProps, e) r[l] === void 0 && (r[l] = e[l]);
  return {
    $$typeof: H,
    type: n,
    key: t,
    ref: s,
    props: r,
    _owner: Z.current
  };
}
w.Fragment = Q;
w.jsx = F;
w.jsxs = F;
C.exports = w;
var ee = C.exports;
const {
  SvelteComponent: te,
  assign: I,
  binding_callbacks: R,
  check_outros: se,
  children: T,
  claim_element: A,
  claim_space: ne,
  component_subscribe: x,
  compute_slots: oe,
  create_slot: re,
  detach: a,
  element: j,
  empty: k,
  exclude_internal_props: S,
  get_all_dirty_from_scope: le,
  get_slot_changes: ie,
  group_outros: ce,
  init: ue,
  insert_hydration: p,
  safe_not_equal: ae,
  set_custom_element_data: D,
  space: fe,
  transition_in: g,
  transition_out: h,
  update_slot_base: _e
} = window.__gradio__svelte__internal, {
  beforeUpdate: de,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function E(n) {
  let e, o;
  const l = (
    /*#slots*/
    n[7].default
  ), r = re(
    l,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      e = j("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = A(t, "SVELTE-SLOT", {
        class: !0
      });
      var s = T(e);
      r && r.l(s), s.forEach(a), this.h();
    },
    h() {
      D(e, "class", "svelte-1rt0kpf");
    },
    m(t, s) {
      p(t, e, s), r && r.m(e, null), n[9](e), o = !0;
    },
    p(t, s) {
      r && r.p && (!o || s & /*$$scope*/
      64) && _e(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        o ? ie(
          l,
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
      o || (g(r, t), o = !0);
    },
    o(t) {
      h(r, t), o = !1;
    },
    d(t) {
      t && a(e), r && r.d(t), n[9](null);
    }
  };
}
function we(n) {
  let e, o, l, r, t = (
    /*$$slots*/
    n[4].default && E(n)
  );
  return {
    c() {
      e = j("react-portal-target"), o = fe(), t && t.c(), l = k(), this.h();
    },
    l(s) {
      e = A(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), T(e).forEach(a), o = ne(s), t && t.l(s), l = k(), this.h();
    },
    h() {
      D(e, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      p(s, e, c), n[8](e), p(s, o, c), t && t.m(s, c), p(s, l, c), r = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? t ? (t.p(s, c), c & /*$$slots*/
      16 && g(t, 1)) : (t = E(s), t.c(), g(t, 1), t.m(l.parentNode, l)) : t && (ce(), h(t, 1, 1, () => {
        t = null;
      }), se());
    },
    i(s) {
      r || (g(t), r = !0);
    },
    o(s) {
      h(t), r = !1;
    },
    d(s) {
      s && (a(e), a(o), a(l)), n[8](null), t && t.d(s);
    }
  };
}
function O(n) {
  const {
    svelteInit: e,
    ...o
  } = n;
  return o;
}
function be(n, e, o) {
  let l, r, {
    $$slots: t = {},
    $$scope: s
  } = e;
  const c = oe(t);
  let {
    svelteInit: u
  } = e;
  const f = m(O(e)), _ = m();
  x(n, _, (i) => o(0, l = i));
  const d = m();
  x(n, d, (i) => o(1, r = i));
  const v = [], L = me("$$ms-gr-react-wrapper"), {
    slotKey: N,
    slotIndex: W,
    subSlotIndex: q
  } = G() || {}, K = u({
    parent: L,
    props: f,
    target: _,
    slot: d,
    slotKey: N,
    slotIndex: W,
    subSlotIndex: q,
    onDestroy(i) {
      v.push(i);
    }
  });
  ge("$$ms-gr-react-wrapper", K), de(() => {
    f.set(O(e));
  }), pe(() => {
    v.forEach((i) => i());
  });
  function M(i) {
    R[i ? "unshift" : "push"](() => {
      l = i, _.set(l);
    });
  }
  function U(i) {
    R[i ? "unshift" : "push"](() => {
      r = i, d.set(r);
    });
  }
  return n.$$set = (i) => {
    o(17, e = I(I({}, e), S(i))), "svelteInit" in i && o(5, u = i.svelteInit), "$$scope" in i && o(6, s = i.$$scope);
  }, e = S(e), [l, r, _, d, c, u, s, t, M, U];
}
class he extends te {
  constructor(e) {
    super(), ue(this, e, be, we, ae, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, b = window.ms_globals.tree;
function ve(n, e = {}) {
  function o(l) {
    const r = m(), t = new he({
      ...l,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
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
          return u.nodes = [...u.nodes, c], P({
            createPortal: y,
            node: b
          }), s.onDestroy(() => {
            u.nodes = u.nodes.filter((f) => f.svelteInstance !== r), P({
              createPortal: y,
              node: b
            });
          }), c;
        },
        ...l.props
      }
    });
    return r.set(t), t;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(o);
    });
  });
}
function ye(n) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(n.trim());
}
function Ie(n, e = !1) {
  try {
    if (J(n))
      return n;
    if (e && !ye(n))
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
function Re(n, e) {
  return B(() => Ie(n, e), [n, e]);
}
const ke = ve(({
  target: n,
  ...e
}) => {
  const o = Re(n);
  return /* @__PURE__ */ ee.jsx(V, {
    ...e,
    target: o
  });
});
export {
  ke as Affix,
  ke as default
};
