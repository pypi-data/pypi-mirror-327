import { g as M, w as m } from "./Index-D5-DX1EY.js";
const v = window.ms_globals.ReactDOM.createPortal, N = window.ms_globals.antd.Skeleton, {
  SvelteComponent: U,
  assign: I,
  binding_callbacks: k,
  check_outros: V,
  children: R,
  claim_element: D,
  claim_space: W,
  component_subscribe: y,
  compute_slots: j,
  create_slot: F,
  detach: u,
  element: A,
  empty: S,
  exclude_internal_props: E,
  get_all_dirty_from_scope: H,
  get_slot_changes: J,
  group_outros: Q,
  init: X,
  insert_hydration: p,
  safe_not_equal: Y,
  set_custom_element_data: K,
  space: Z,
  transition_in: g,
  transition_out: h,
  update_slot_base: $
} = window.__gradio__svelte__internal, {
  beforeUpdate: ee,
  getContext: te,
  onDestroy: se,
  setContext: oe
} = window.__gradio__svelte__internal;
function C(r) {
  let s, n;
  const l = (
    /*#slots*/
    r[7].default
  ), o = F(
    l,
    r,
    /*$$scope*/
    r[6],
    null
  );
  return {
    c() {
      s = A("svelte-slot"), o && o.c(), this.h();
    },
    l(e) {
      s = D(e, "SVELTE-SLOT", {
        class: !0
      });
      var t = R(s);
      o && o.l(t), t.forEach(u), this.h();
    },
    h() {
      K(s, "class", "svelte-1rt0kpf");
    },
    m(e, t) {
      p(e, s, t), o && o.m(s, null), r[9](s), n = !0;
    },
    p(e, t) {
      o && o.p && (!n || t & /*$$scope*/
      64) && $(
        o,
        l,
        e,
        /*$$scope*/
        e[6],
        n ? J(
          l,
          /*$$scope*/
          e[6],
          t,
          null
        ) : H(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (g(o, e), n = !0);
    },
    o(e) {
      h(o, e), n = !1;
    },
    d(e) {
      e && u(s), o && o.d(e), r[9](null);
    }
  };
}
function ne(r) {
  let s, n, l, o, e = (
    /*$$slots*/
    r[4].default && C(r)
  );
  return {
    c() {
      s = A("react-portal-target"), n = Z(), e && e.c(), l = S(), this.h();
    },
    l(t) {
      s = D(t, "REACT-PORTAL-TARGET", {
        class: !0
      }), R(s).forEach(u), n = W(t), e && e.l(t), l = S(), this.h();
    },
    h() {
      K(s, "class", "svelte-1rt0kpf");
    },
    m(t, c) {
      p(t, s, c), r[8](s), p(t, n, c), e && e.m(t, c), p(t, l, c), o = !0;
    },
    p(t, [c]) {
      /*$$slots*/
      t[4].default ? e ? (e.p(t, c), c & /*$$slots*/
      16 && g(e, 1)) : (e = C(t), e.c(), g(e, 1), e.m(l.parentNode, l)) : e && (Q(), h(e, 1, 1, () => {
        e = null;
      }), V());
    },
    i(t) {
      o || (g(e), o = !0);
    },
    o(t) {
      h(e), o = !1;
    },
    d(t) {
      t && (u(s), u(n), u(l)), r[8](null), e && e.d(t);
    }
  };
}
function P(r) {
  const {
    svelteInit: s,
    ...n
  } = r;
  return n;
}
function le(r, s, n) {
  let l, o, {
    $$slots: e = {},
    $$scope: t
  } = s;
  const c = j(e);
  let {
    svelteInit: i
  } = s;
  const _ = m(P(s)), f = m();
  y(r, f, (a) => n(0, l = a));
  const d = m();
  y(r, d, (a) => n(1, o = a));
  const w = [], L = te("$$ms-gr-react-wrapper"), {
    slotKey: O,
    slotIndex: x,
    subSlotIndex: B
  } = M() || {}, q = i({
    parent: L,
    props: _,
    target: f,
    slot: d,
    slotKey: O,
    slotIndex: x,
    subSlotIndex: B,
    onDestroy(a) {
      w.push(a);
    }
  });
  oe("$$ms-gr-react-wrapper", q), ee(() => {
    _.set(P(s));
  }), se(() => {
    w.forEach((a) => a());
  });
  function z(a) {
    k[a ? "unshift" : "push"](() => {
      l = a, f.set(l);
    });
  }
  function G(a) {
    k[a ? "unshift" : "push"](() => {
      o = a, d.set(o);
    });
  }
  return r.$$set = (a) => {
    n(17, s = I(I({}, s), E(a))), "svelteInit" in a && n(5, i = a.svelteInit), "$$scope" in a && n(6, t = a.$$scope);
  }, s = E(s), [l, o, f, d, c, i, t, e, z, G];
}
class re extends U {
  constructor(s) {
    super(), X(this, s, le, ne, Y, {
      svelteInit: 5
    });
  }
}
const T = window.ms_globals.rerender, b = window.ms_globals.tree;
function ae(r, s = {}) {
  function n(l) {
    const o = m(), e = new re({
      ...l,
      props: {
        svelteInit(t) {
          window.ms_globals.autokey += 1;
          const c = {
            key: window.ms_globals.autokey,
            svelteInstance: o,
            reactComponent: r,
            props: t.props,
            slot: t.slot,
            target: t.target,
            slotIndex: t.slotIndex,
            subSlotIndex: t.subSlotIndex,
            ignore: s.ignore,
            slotKey: t.slotKey,
            nodes: []
          }, i = t.parent ?? b;
          return i.nodes = [...i.nodes, c], T({
            createPortal: v,
            node: b
          }), t.onDestroy(() => {
            i.nodes = i.nodes.filter((_) => _.svelteInstance !== o), T({
              createPortal: v,
              node: b
            });
          }), c;
        },
        ...l.props
      }
    });
    return o.set(e), e;
  }
  return new Promise((l) => {
    window.ms_globals.initializePromise.then(() => {
      l(n);
    });
  });
}
const ie = ae(N.Button);
export {
  ie as SkeletonButton,
  ie as default
};
