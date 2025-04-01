import { g as H, w as p, c as J } from "./Index-CSZVK068.js";
const z = window.ms_globals.React, G = window.ms_globals.React.useMemo, I = window.ms_globals.ReactDOM.createPortal, _ = window.ms_globals.antd.Layout;
var L = {
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
var V = z, Y = Symbol.for("react.element"), Q = Symbol.for("react.fragment"), X = Object.prototype.hasOwnProperty, Z = V.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED.ReactCurrentOwner, $ = {
  key: !0,
  ref: !0,
  __self: !0,
  __source: !0
};
function T(r, t, l) {
  var o, n = {}, e = null, s = null;
  l !== void 0 && (e = "" + l), t.key !== void 0 && (e = "" + t.key), t.ref !== void 0 && (s = t.ref);
  for (o in t) X.call(t, o) && !$.hasOwnProperty(o) && (n[o] = t[o]);
  if (r && r.defaultProps) for (o in t = r.defaultProps, t) n[o] === void 0 && (n[o] = t[o]);
  return {
    $$typeof: Y,
    type: r,
    key: e,
    ref: s,
    props: n,
    _owner: Z.current
  };
}
b.Fragment = Q;
b.jsx = T;
b.jsxs = T;
L.exports = b;
var ee = L.exports;
const {
  SvelteComponent: te,
  assign: k,
  binding_callbacks: R,
  check_outros: se,
  children: j,
  claim_element: D,
  claim_space: oe,
  component_subscribe: E,
  compute_slots: ne,
  create_slot: re,
  detach: u,
  element: N,
  empty: S,
  exclude_internal_props: x,
  get_all_dirty_from_scope: le,
  get_slot_changes: ae,
  group_outros: ce,
  init: ie,
  insert_hydration: g,
  safe_not_equal: ue,
  set_custom_element_data: A,
  space: _e,
  transition_in: w,
  transition_out: h,
  update_slot_base: fe
} = window.__gradio__svelte__internal, {
  beforeUpdate: de,
  getContext: me,
  onDestroy: pe,
  setContext: ge
} = window.__gradio__svelte__internal;
function O(r) {
  let t, l;
  const o = (
    /*#slots*/
    r[7].default
  ), n = re(
    o,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      t = N("svelte-slot"), n && n.c(), this.h();
    },
    l(e) {
      t = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var s = j(t);
      n && n.l(s), s.forEach(u), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(e, s) {
      g(e, t, s), n && n.m(t, null), r[9](t), l = !0;
    },
    p(e, s) {
      n && n.p && (!l || s & /*$$scope*/
      64) && fe(
        n,
        o,
        e,
        /*$$scope*/
        e[6],
        l ? ae(
          o,
          /*$$scope*/
          e[6],
          s,
          null
        ) : le(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      l || (w(n, e), l = !0);
    },
    o(e) {
      h(n, e), l = !1;
    },
    d(e) {
      e && u(t), n && n.d(e), r[9](null);
    }
  };
}
function we(r) {
  let t, l, o, n, e = (
    /*$$slots*/
    r[4].default && O(r)
  );
  return {
    c() {
      t = N("react-portal-target"), l = _e(), e && e.c(), o = S(), this.h();
    },
    l(s) {
      t = D(s, "REACT-PORTAL-TARGET", {
        class: !0
      }), j(t).forEach(u), l = oe(s), e && e.l(s), o = S(), this.h();
    },
    h() {
      A(t, "class", "svelte-1rt0kpf");
    },
    m(s, c) {
      g(s, t, c), r[8](t), g(s, l, c), e && e.m(s, c), g(s, o, c), n = !0;
    },
    p(s, [c]) {
      /*$$slots*/
      s[4].default ? e ? (e.p(s, c), c & /*$$slots*/
      16 && w(e, 1)) : (e = O(s), e.c(), w(e, 1), e.m(o.parentNode, o)) : e && (ce(), h(e, 1, 1, () => {
        e = null;
      }), se());
    },
    i(s) {
      n || (w(e), n = !0);
    },
    o(s) {
      h(e), n = !1;
    },
    d(s) {
      s && (u(t), u(l), u(o)), r[8](null), e && e.d(s);
    }
  };
}
function C(r) {
  const {
    svelteInit: t,
    ...l
  } = r;
  return l;
}
function be(r, t, l) {
  let o, n, {
    $$slots: e = {},
    $$scope: s
  } = t;
  const c = ne(e);
  let {
    svelteInit: i
  } = t;
  const f = p(C(t)), d = p();
  E(r, d, (a) => l(0, o = a));
  const m = p();
  E(r, m, (a) => l(1, n = a));
  const v = [], q = me("$$ms-gr-react-wrapper"), {
    slotKey: F,
    slotIndex: K,
    subSlotIndex: M
  } = H() || {}, U = i({
    parent: q,
    props: f,
    target: d,
    slot: m,
    slotKey: F,
    slotIndex: K,
    subSlotIndex: M,
    onDestroy(a) {
      v.push(a);
    }
  });
  ge("$$ms-gr-react-wrapper", U), de(() => {
    f.set(C(t));
  }), pe(() => {
    v.forEach((a) => a());
  });
  function B(a) {
    R[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  function W(a) {
    R[a ? "unshift" : "push"](() => {
      n = a, m.set(n);
    });
  }
  return r.$$set = (a) => {
    l(17, t = k(k({}, t), x(a))), "svelteInit" in a && l(5, i = a.svelteInit), "$$scope" in a && l(6, s = a.$$scope);
  }, t = x(t), [o, n, d, m, c, i, s, e, B, W];
}
class ye extends te {
  constructor(t) {
    super(), ie(this, t, be, we, ue, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, y = window.ms_globals.tree;
function he(r, t = {}) {
  function l(o) {
    const n = p(), e = new ye({
      ...o,
      props: {
        svelteInit(s) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: n,
            reactComponent: r,
            props: s.props,
            slot: s.slot,
            target: s.target,
            slotIndex: s.slotIndex,
            subSlotIndex: s.subSlotIndex,
            ignore: t.ignore,
            slotKey: s.slotKey,
            nodes: []
          }, i = s.parent ?? y;
          return i.nodes = [...i.nodes, c], P({
            createPortal: I,
            node: y
          }), s.onDestroy(() => {
            i.nodes = i.nodes.filter((f) => f.svelteInstance !== n), P({
              createPortal: I,
              node: y
            });
          }), c;
        },
        ...o.props
      }
    });
    return n.set(e), e;
  }
  return new Promise((o) => {
    window.ms_globals.initializePromise.then(() => {
      o(l);
    });
  });
}
const Ie = he(({
  component: r,
  className: t,
  ...l
}) => {
  const o = G(() => {
    switch (r) {
      case "content":
        return _.Content;
      case "footer":
        return _.Footer;
      case "header":
        return _.Header;
      case "layout":
        return _;
      default:
        return _;
    }
  }, [r]);
  return /* @__PURE__ */ ee.jsx(o, {
    ...l,
    className: J(t, r === "layout" ? null : `ms-gr-antd-layout-${r}`)
  });
});
export {
  Ie as Base,
  Ie as default
};
