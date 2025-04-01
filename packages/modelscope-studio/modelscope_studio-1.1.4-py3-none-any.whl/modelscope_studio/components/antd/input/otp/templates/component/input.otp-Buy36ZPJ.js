import { b as Y, g as H, w as m, i as Q } from "./Index-D4UYpzkB.js";
const B = window.ms_globals.React, G = window.ms_globals.React.useMemo, J = window.ms_globals.React.useState, y = window.ms_globals.React.useRef, R = window.ms_globals.React.useEffect, I = window.ms_globals.ReactDOM.createPortal, X = window.ms_globals.antd.Input;
function Z(s, e) {
  return Y(s, e);
}
var j = {
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
var $ = B, ee = Symbol.for("react.element"), te = Symbol.for("react.fragment"), se = Object.prototype.hasOwnProperty, ne = $.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, oe = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function C(s, e, n) {
  var l, r = {}, t = null, o = null;
  n !== void 0 && (t = "" + n), e.key !== void 0 && (t = "" + e.key), e.ref !== void 0 && (o = e.ref);
  for (l in e) se.call(e, l) && !oe.hasOwnProperty(l) && (r[l] = e[l]);
  if (s && s.defaultProps) for (l in e = s.defaultProps, e) r[l] === void 0 && (r[l] = e[l]);
  return {
    $$typeof: ee,
    type: s,
    key: t,
    ref: o,
    props: r,
    _owner: ne.current
  };
}
g.Fragment = te;
g.jsx = C;
g.jsxs = C;
j.exports = g;
var re = j.exports;
const {
  SvelteComponent: le,
  assign: E,
  binding_callbacks: S,
  check_outros: ie,
  children: D,
  claim_element: L,
  claim_space: ue,
  component_subscribe: k,
  compute_slots: ce,
  create_slot: ae,
  detach: a,
  element: V,
  empty: x,
  exclude_internal_props: O,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  group_outros: de,
  init: me,
  insert_hydration: p,
  safe_not_equal: pe,
  set_custom_element_data: q,
  space: we,
  transition_in: w,
  transition_out: h,
  update_slot_base: ge
} = window.__gradio__svelte__internal, {
  beforeUpdate: be,
  getContext: he,
  onDestroy: ve,
  setContext: ye
} = window.__gradio__svelte__internal;
function P(s) {
  let e, n;
  const l = (
    /*#slots*/
    s[7].default
  ), r = ae(
    l,
    s,
    /*$$scope*/
    s[6],
    null
  );
  return {
    c() {
      e = V("svelte-slot"), r && r.c(), this.h();
    },
    l(t) {
      e = L(t, "SVELTE-SLOT", {
        class: !0
      });
      var o = D(e);
      r && r.l(o), o.forEach(a), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(t, o) {
      p(t, e, o), r && r.m(e, null), s[9](e), n = !0;
    },
    p(t, o) {
      r && r.p && (!n || o & /*$$scope*/
      64) && ge(
        r,
        l,
        t,
        /*$$scope*/
        t[6],
        n ? _e(
          l,
          /*$$scope*/
          t[6],
          o,
          null
        ) : fe(
          /*$$scope*/
          t[6]
        ),
        null
      );
    },
    i(t) {
      n || (w(r, t), n = !0);
    },
    o(t) {
      h(r, t), n = !1;
    },
    d(t) {
      t && a(e), r && r.d(t), s[9](null);
    }
  };
}
function Re(s) {
  let e, n, l, r, t = (
    /*$$slots*/
    s[4].default && P(s)
  );
  return {
    c() {
      e = V("react-portal-target"), n = we(), t && t.c(), l = x(), this.h();
    },
    l(o) {
      e = L(o, "REACT-PORTAL-TARGET", {
        class: !0
      }), D(e).forEach(a), n = ue(o), t && t.l(o), l = x(), this.h();
    },
    h() {
      q(e, "class", "svelte-1rt0kpf");
    },
    m(o, u) {
      p(o, e, u), s[8](e), p(o, n, u), t && t.m(o, u), p(o, l, u), r = !0;
    },
    p(o, [u]) {
      /*$$slots*/
      o[4].default ? t ? (t.p(o, u), u & /*$$slots*/
      16 && w(t, 1)) : (t = P(o), t.c(), w(t, 1), t.m(l.parentNode, l)) : t && (de(), h(t, 1, 1, () => {
        t = null;
      }), ie());
    },
    i(o) {
      r || (w(t), r = !0);
    },
    o(o) {
      h(t), r = !1;
    },
    d(o) {
      o && (a(e), a(n), a(l)), s[8](null), t && t.d(o);
    }
  };
}
function T(s) {
  const {
    svelteInit: e,
    ...n
  } = s;
  return n;
}
function Ie(s, e, n) {
  let l, r, {
    $$slots: t = {},
    $$scope: o
  } = e;
  const u = ce(t);
  let {
    svelteInit: c
  } = e;
  const f = m(T(e)), _ = m();
  k(s, _, (i) => n(0, l = i));
  const d = m();
  k(s, d, (i) => n(1, r = i));
  const v = [], A = he("$$ms-gr-react-wrapper"), {
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W
  } = H() || {}, K = c({
    parent: A,
    props: f,
    target: _,
    slot: d,
    slotKey: M,
    slotIndex: N,
    subSlotIndex: W,
    onDestroy(i) {
      v.push(i);
    }
  });
  ye("$$ms-gr-react-wrapper", K), be(() => {
    f.set(T(e));
  }), ve(() => {
    v.forEach((i) => i());
  });
  function U(i) {
    S[i ? "unshift" : "push"](() => {
      l = i, _.set(l);
    });
  }
  function z(i) {
    S[i ? "unshift" : "push"](() => {
      r = i, d.set(r);
    });
  }
  return s.$$set = (i) => {
    n(17, e = E(E({}, e), O(i))), "svelteInit" in i && n(5, c = i.svelteInit), "$$scope" in i && n(6, o = i.$$scope);
  }, e = O(e), [l, r, _, d, u, c, o, t, U, z];
}
class Ee extends le {
  constructor(e) {
    super(), me(this, e, Ie, Re, pe, {
      svelteInit: 5
    });
  }
}
const F = window.ms_globals.rerender, b = window.ms_globals.tree;
function Se(s, e = {}) {
  function n(l) {
    const r = m(), t = new Ee({
      ...l,
      props: {
        svelteInit(o) {
          window.ms_globals.autokey += 1;
          const u = {
            key: window.ms_globals.autokey,
            svelteInstance: r,
            reactComponent: s,
            props: o.props,
            slot: o.slot,
            target: o.target,
            slotIndex: o.slotIndex,
            subSlotIndex: o.subSlotIndex,
            ignore: e.ignore,
            slotKey: o.slotKey,
            nodes: []
          }, c = o.parent ?? b;
          return c.nodes = [...c.nodes, u], F({
            createPortal: I,
            node: b
          }), o.onDestroy(() => {
            c.nodes = c.nodes.filter((f) => f.svelteInstance !== r), F({
              createPortal: I,
              node: b
            });
          }), u;
        },
        ...l.props
      }
    });
    return r.set(t), t;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
function ke(s) {
  return /^(?:async\s+)?(?:function\s*(?:\w*\s*)?\(|\([\w\s,=]*\)\s*=>|\(\{[\w\s,=]*\}\)\s*=>|function\s*\*\s*\w*\s*\()/i.test(s.trim());
}
function xe(s, e = !1) {
  try {
    if (Q(s))
      return s;
    if (e && !ke(s))
      return;
    if (typeof s == "string") {
      let n = s.trim();
      return n.startsWith(";") && (n = n.slice(1)), n.endsWith(";") && (n = n.slice(0, -1)), new Function(`return (...args) => (${n})(...args)`)();
    }
    return;
  } catch {
    return;
  }
}
function Oe(s, e) {
  return G(() => xe(s, e), [s, e]);
}
function Pe({
  value: s,
  onValueChange: e
}) {
  const [n, l] = J(s), r = y(e);
  r.current = e;
  const t = y(n);
  return t.current = n, R(() => {
    r.current(n);
  }, [n]), R(() => {
    Z(s, t.current) || l(s);
  }, [s]), [n, l];
}
const Fe = Se(({
  formatter: s,
  onValueChange: e,
  onChange: n,
  elRef: l,
  ...r
}) => {
  const t = Oe(s), [o, u] = Pe({
    onValueChange: e,
    value: r.value
  });
  return /* @__PURE__ */ re.jsx(X.OTP, {
    ...r,
    value: o,
    ref: l,
    formatter: t,
    onChange: (c) => {
      n == null || n(c), u(c);
    }
  });
});
export {
  Fe as InputOTP,
  Fe as default
};
