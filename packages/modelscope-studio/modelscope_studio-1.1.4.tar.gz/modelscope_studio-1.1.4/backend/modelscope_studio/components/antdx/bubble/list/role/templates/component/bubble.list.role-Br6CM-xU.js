import { g as G, w as m, j as M } from "./Role-0I2c7txo.js";
const w = window.ms_globals.ReactDOM.createPortal, S = window.ms_globals.createItemsContext.createItemsContext, {
  SvelteComponent: N,
  assign: v,
  binding_callbacks: x,
  check_outros: U,
  children: T,
  claim_element: D,
  claim_space: V,
  component_subscribe: y,
  compute_slots: W,
  create_slot: F,
  detach: u,
  element: L,
  empty: C,
  exclude_internal_props: k,
  get_all_dirty_from_scope: J,
  get_slot_changes: Q,
  group_outros: X,
  init: Y,
  insert_hydration: p,
  safe_not_equal: Z,
  set_custom_element_data: j,
  space: $,
  transition_in: b,
  transition_out: h,
  update_slot_base: ee
} = window.__gradio__svelte__internal, {
  beforeUpdate: te,
  getContext: se,
  onDestroy: oe,
  setContext: ne
} = window.__gradio__svelte__internal;
function R(n) {
  let s, l;
  const r = (
    /*#slots*/
    n[7].default
  ), o = F(
    r,
    n,
    /*$$scope*/
    n[6],
    null
  );
  return {
    c() {
      s = L("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      s = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var t = T(s);
      o && o.l(t), t.forEach(u), this.h();
    },
    h() {
      j(s, "class", "svelte-1rt0kpf");
    },
    m(e, t) {
      p(e, s, t), o && o.m(s, null), n[9](s), l = !0;
    },
    p(e, t) {
      o && o.p && (!l || t & /*$$scope*/
      64) && ee(
        o,
        r,
        e,
        /*$$scope*/
        e[6],
        l ? Q(
          r,
          /*$$scope*/
          e[6],
          t,
          null
        ) : J(
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
      e && u(s), o && o.d(e), n[9](null);
    }
  };
}
function le(n) {
  let s, l, r, o, e = (
    /*$$slots*/
    n[4].default && R(n)
  );
  return {
    c() {
      s = L("react-portal-target"), l = $(), e && e.c(), r = C(), this.h();
    },
    l(t) {
      s = D(t, "REACT-PORTAL-TARGET", {
        class: !0
      }), T(s).forEach(u), l = V(t), e && e.l(t), r = C(), this.h();
    },
    h() {
      j(s, "class", "svelte-1rt0kpf");
    },
    m(t, i) {
      p(t, s, i), n[8](s), p(t, l, i), e && e.m(t, i), p(t, r, i), o = !0;
    },
    p(t, [i]) {
      /*$$slots*/
      t[4].default ? e ? (e.p(t, i), i & /*$$slots*/
      16 && b(e, 1)) : (e = R(t), e.c(), b(e, 1), e.m(r.parentNode, r)) : e && (X(), h(e, 1, 1, () => {
        e = null;
      }), U());
    },
    i(t) {
      o || (b(e), o = !0);
    },
    o(t) {
      h(e), o = !1;
    },
    d(t) {
      t && (u(s), u(l), u(r)), n[8](null), e && e.d(t);
    }
  };
}
function E(n) {
  const {
    svelteInit: s,
    ...l
  } = n;
  return l;
}
function re(n, s, l) {
  let r, o, {
    $$slots: e = {},
    $$scope: t
  } = s;
  const i = W(e);
  let {
    svelteInit: c
  } = s;
  const _ = m(E(s)), f = m();
  y(n, f, (a) => l(0, r = a));
  const d = m();
  y(n, d, (a) => l(1, o = a));
  const I = [], A = se("$$ms-gr-react-wrapper"), {
    slotKey: K,
    slotIndex: O,
    subSlotIndex: H
  } = G() || {}, q = c({
    parent: A,
    props: _,
    target: f,
    slot: d,
    slotKey: K,
    slotIndex: O,
    subSlotIndex: H,
    onDestroy(a) {
      I.push(a);
    }
  });
  ne("$$ms-gr-react-wrapper", q), te(() => {
    _.set(E(s));
  }), oe(() => {
    I.forEach((a) => a());
  });
  function z(a) {
    x[a ? "unshift" : "push"](() => {
      r = a, f.set(r);
    });
  }
  function B(a) {
    x[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return n.$$set = (a) => {
    l(17, s = v(v({}, s), k(a))), "svelteInit" in a && l(5, c = a.svelteInit), "$$scope" in a && l(6, t = a.$$scope);
  }, s = k(s), [r, o, f, d, i, c, t, e, z, B];
}
class ae extends N {
  constructor(s) {
    super(), Y(this, s, re, le, Z, {
      svelteInit: 5
    });
  }
}
const P = window.ms_globals.rerender, g = window.ms_globals.tree;
function ie(n, s = {}) {
  function l(r) {
    const o = m(), e = new ae({
      ...r,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const i = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: n,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            ignore: s.ignore,
            slotKey: t.slotKey,
            nodes: []
          }, c = t.parent ?? g;
          return c.nodes = [...c.nodes, i], P({
            createPortal: w,
            node: g
          }), t.onDestroy(() => {
            c.nodes = c.nodes.filter((_) => _.svelteInstance !== o), P({
              createPortal: w,
              node: g
            });
          }), i;
        },
        ...r.props
      }
    });
    return o.set(e), e;
  }
  return new Promise((r) => {
    window.ms_globals.initializePromise.then(() => {
      r(l);
    });
  });
}
S("antdx-bubble.list-items");
const {
  useItems: _e,
  withItemsContextProvider: fe,
  ItemHandler: ce
} = S("antdx-bubble.list-roles"), de = ie((n) => /* @__PURE__ */ M.jsx(ce, {
  ...n
}));
export {
  de as BubbleListRole,
  de as default
};
