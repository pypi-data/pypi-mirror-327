function rn(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, i) => i === 0 ? r.toLowerCase() : r.toUpperCase());
}
var mt = typeof global == "object" && global && global.Object === Object && global, on = typeof self == "object" && self && self.Object === Object && self, C = mt || on || Function("return this")(), w = C.Symbol, vt = Object.prototype, an = vt.hasOwnProperty, sn = vt.toString, q = w ? w.toStringTag : void 0;
function un(e) {
  var t = an.call(e, q), n = e[q];
  try {
    e[q] = void 0;
    var r = !0;
  } catch {
  }
  var i = sn.call(e);
  return r && (t ? e[q] = n : delete e[q]), i;
}
var ln = Object.prototype, fn = ln.toString;
function cn(e) {
  return fn.call(e);
}
var pn = "[object Null]", gn = "[object Undefined]", Ue = w ? w.toStringTag : void 0;
function N(e) {
  return e == null ? e === void 0 ? gn : pn : Ue && Ue in Object(e) ? un(e) : cn(e);
}
function E(e) {
  return e != null && typeof e == "object";
}
var dn = "[object Symbol]";
function Pe(e) {
  return typeof e == "symbol" || E(e) && N(e) == dn;
}
function Tt(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = Array(r); ++n < r; )
    i[n] = t(e[n], n, e);
  return i;
}
var A = Array.isArray, _n = 1 / 0, Ge = w ? w.prototype : void 0, Be = Ge ? Ge.toString : void 0;
function Ot(e) {
  if (typeof e == "string")
    return e;
  if (A(e))
    return Tt(e, Ot) + "";
  if (Pe(e))
    return Be ? Be.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -_n ? "-0" : t;
}
function z(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function Pt(e) {
  return e;
}
var bn = "[object AsyncFunction]", hn = "[object Function]", yn = "[object GeneratorFunction]", mn = "[object Proxy]";
function wt(e) {
  if (!z(e))
    return !1;
  var t = N(e);
  return t == hn || t == yn || t == bn || t == mn;
}
var ce = C["__core-js_shared__"], ze = function() {
  var e = /[^.]+$/.exec(ce && ce.keys && ce.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function vn(e) {
  return !!ze && ze in e;
}
var Tn = Function.prototype, On = Tn.toString;
function D(e) {
  if (e != null) {
    try {
      return On.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var Pn = /[\\^$.*+?()[\]{}|]/g, wn = /^\[object .+?Constructor\]$/, $n = Function.prototype, An = Object.prototype, Sn = $n.toString, Cn = An.hasOwnProperty, xn = RegExp("^" + Sn.call(Cn).replace(Pn, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function En(e) {
  if (!z(e) || vn(e))
    return !1;
  var t = wt(e) ? xn : wn;
  return t.test(D(e));
}
function jn(e, t) {
  return e == null ? void 0 : e[t];
}
function K(e, t) {
  var n = jn(e, t);
  return En(n) ? n : void 0;
}
var be = K(C, "WeakMap"), He = Object.create, In = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!z(t))
      return {};
    if (He)
      return He(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Fn(e, t, n) {
  switch (n.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, n[0]);
    case 2:
      return e.call(t, n[0], n[1]);
    case 3:
      return e.call(t, n[0], n[1], n[2]);
  }
  return e.apply(t, n);
}
function Mn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Ln = 800, Rn = 16, Nn = Date.now;
function Dn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Nn(), i = Rn - (r - n);
    if (n = r, i > 0) {
      if (++t >= Ln)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Kn(e) {
  return function() {
    return e;
  };
}
var ne = function() {
  try {
    var e = K(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), Un = ne ? function(e, t) {
  return ne(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Kn(t),
    writable: !0
  });
} : Pt, Gn = Dn(Un);
function Bn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var zn = 9007199254740991, Hn = /^(?:0|[1-9]\d*)$/;
function $t(e, t) {
  var n = typeof e;
  return t = t ?? zn, !!t && (n == "number" || n != "symbol" && Hn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function we(e, t, n) {
  t == "__proto__" && ne ? ne(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function $e(e, t) {
  return e === t || e !== e && t !== t;
}
var qn = Object.prototype, Yn = qn.hasOwnProperty;
function At(e, t, n) {
  var r = e[t];
  (!(Yn.call(e, t) && $e(r, n)) || n === void 0 && !(t in e)) && we(e, t, n);
}
function W(e, t, n, r) {
  var i = !n;
  n || (n = {});
  for (var o = -1, a = t.length; ++o < a; ) {
    var s = t[o], u = void 0;
    u === void 0 && (u = e[s]), i ? we(n, s, u) : At(n, s, u);
  }
  return n;
}
var qe = Math.max;
function Jn(e, t, n) {
  return t = qe(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, i = -1, o = qe(r.length - t, 0), a = Array(o); ++i < o; )
      a[i] = r[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = r[i];
    return s[t] = n(a), Fn(e, this, s);
  };
}
var Xn = 9007199254740991;
function Ae(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Xn;
}
function St(e) {
  return e != null && Ae(e.length) && !wt(e);
}
var Zn = Object.prototype;
function Se(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Zn;
  return e === n;
}
function Wn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var Qn = "[object Arguments]";
function Ye(e) {
  return E(e) && N(e) == Qn;
}
var Ct = Object.prototype, Vn = Ct.hasOwnProperty, kn = Ct.propertyIsEnumerable, Ce = Ye(/* @__PURE__ */ function() {
  return arguments;
}()) ? Ye : function(e) {
  return E(e) && Vn.call(e, "callee") && !kn.call(e, "callee");
};
function er() {
  return !1;
}
var xt = typeof exports == "object" && exports && !exports.nodeType && exports, Je = xt && typeof module == "object" && module && !module.nodeType && module, tr = Je && Je.exports === xt, Xe = tr ? C.Buffer : void 0, nr = Xe ? Xe.isBuffer : void 0, re = nr || er, rr = "[object Arguments]", ir = "[object Array]", or = "[object Boolean]", ar = "[object Date]", sr = "[object Error]", ur = "[object Function]", lr = "[object Map]", fr = "[object Number]", cr = "[object Object]", pr = "[object RegExp]", gr = "[object Set]", dr = "[object String]", _r = "[object WeakMap]", br = "[object ArrayBuffer]", hr = "[object DataView]", yr = "[object Float32Array]", mr = "[object Float64Array]", vr = "[object Int8Array]", Tr = "[object Int16Array]", Or = "[object Int32Array]", Pr = "[object Uint8Array]", wr = "[object Uint8ClampedArray]", $r = "[object Uint16Array]", Ar = "[object Uint32Array]", v = {};
v[yr] = v[mr] = v[vr] = v[Tr] = v[Or] = v[Pr] = v[wr] = v[$r] = v[Ar] = !0;
v[rr] = v[ir] = v[br] = v[or] = v[hr] = v[ar] = v[sr] = v[ur] = v[lr] = v[fr] = v[cr] = v[pr] = v[gr] = v[dr] = v[_r] = !1;
function Sr(e) {
  return E(e) && Ae(e.length) && !!v[N(e)];
}
function xe(e) {
  return function(t) {
    return e(t);
  };
}
var Et = typeof exports == "object" && exports && !exports.nodeType && exports, Y = Et && typeof module == "object" && module && !module.nodeType && module, Cr = Y && Y.exports === Et, pe = Cr && mt.process, B = function() {
  try {
    var e = Y && Y.require && Y.require("util").types;
    return e || pe && pe.binding && pe.binding("util");
  } catch {
  }
}(), Ze = B && B.isTypedArray, jt = Ze ? xe(Ze) : Sr, xr = Object.prototype, Er = xr.hasOwnProperty;
function It(e, t) {
  var n = A(e), r = !n && Ce(e), i = !n && !r && re(e), o = !n && !r && !i && jt(e), a = n || r || i || o, s = a ? Wn(e.length, String) : [], u = s.length;
  for (var l in e)
    (t || Er.call(e, l)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (l == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (l == "offset" || l == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (l == "buffer" || l == "byteLength" || l == "byteOffset") || // Skip index properties.
    $t(l, u))) && s.push(l);
  return s;
}
function Ft(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var jr = Ft(Object.keys, Object), Ir = Object.prototype, Fr = Ir.hasOwnProperty;
function Mr(e) {
  if (!Se(e))
    return jr(e);
  var t = [];
  for (var n in Object(e))
    Fr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function Q(e) {
  return St(e) ? It(e) : Mr(e);
}
function Lr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Rr = Object.prototype, Nr = Rr.hasOwnProperty;
function Dr(e) {
  if (!z(e))
    return Lr(e);
  var t = Se(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Nr.call(e, r)) || n.push(r);
  return n;
}
function Ee(e) {
  return St(e) ? It(e, !0) : Dr(e);
}
var Kr = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, Ur = /^\w*$/;
function je(e, t) {
  if (A(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Pe(e) ? !0 : Ur.test(e) || !Kr.test(e) || t != null && e in Object(t);
}
var J = K(Object, "create");
function Gr() {
  this.__data__ = J ? J(null) : {}, this.size = 0;
}
function Br(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var zr = "__lodash_hash_undefined__", Hr = Object.prototype, qr = Hr.hasOwnProperty;
function Yr(e) {
  var t = this.__data__;
  if (J) {
    var n = t[e];
    return n === zr ? void 0 : n;
  }
  return qr.call(t, e) ? t[e] : void 0;
}
var Jr = Object.prototype, Xr = Jr.hasOwnProperty;
function Zr(e) {
  var t = this.__data__;
  return J ? t[e] !== void 0 : Xr.call(t, e);
}
var Wr = "__lodash_hash_undefined__";
function Qr(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = J && t === void 0 ? Wr : t, this;
}
function R(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
R.prototype.clear = Gr;
R.prototype.delete = Br;
R.prototype.get = Yr;
R.prototype.has = Zr;
R.prototype.set = Qr;
function Vr() {
  this.__data__ = [], this.size = 0;
}
function se(e, t) {
  for (var n = e.length; n--; )
    if ($e(e[n][0], t))
      return n;
  return -1;
}
var kr = Array.prototype, ei = kr.splice;
function ti(e) {
  var t = this.__data__, n = se(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : ei.call(t, n, 1), --this.size, !0;
}
function ni(e) {
  var t = this.__data__, n = se(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function ri(e) {
  return se(this.__data__, e) > -1;
}
function ii(e, t) {
  var n = this.__data__, r = se(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function j(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
j.prototype.clear = Vr;
j.prototype.delete = ti;
j.prototype.get = ni;
j.prototype.has = ri;
j.prototype.set = ii;
var X = K(C, "Map");
function oi() {
  this.size = 0, this.__data__ = {
    hash: new R(),
    map: new (X || j)(),
    string: new R()
  };
}
function ai(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function ue(e, t) {
  var n = e.__data__;
  return ai(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function si(e) {
  var t = ue(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function ui(e) {
  return ue(this, e).get(e);
}
function li(e) {
  return ue(this, e).has(e);
}
function fi(e, t) {
  var n = ue(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function I(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
I.prototype.clear = oi;
I.prototype.delete = si;
I.prototype.get = ui;
I.prototype.has = li;
I.prototype.set = fi;
var ci = "Expected a function";
function Ie(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(ci);
  var n = function() {
    var r = arguments, i = t ? t.apply(this, r) : r[0], o = n.cache;
    if (o.has(i))
      return o.get(i);
    var a = e.apply(this, r);
    return n.cache = o.set(i, a) || o, a;
  };
  return n.cache = new (Ie.Cache || I)(), n;
}
Ie.Cache = I;
var pi = 500;
function gi(e) {
  var t = Ie(e, function(r) {
    return n.size === pi && n.clear(), r;
  }), n = t.cache;
  return t;
}
var di = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, _i = /\\(\\)?/g, bi = gi(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(di, function(n, r, i, o) {
    t.push(i ? o.replace(_i, "$1") : r || n);
  }), t;
});
function hi(e) {
  return e == null ? "" : Ot(e);
}
function le(e, t) {
  return A(e) ? e : je(e, t) ? [e] : bi(hi(e));
}
var yi = 1 / 0;
function V(e) {
  if (typeof e == "string" || Pe(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -yi ? "-0" : t;
}
function Fe(e, t) {
  t = le(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[V(t[n++])];
  return n && n == r ? e : void 0;
}
function mi(e, t, n) {
  var r = e == null ? void 0 : Fe(e, t);
  return r === void 0 ? n : r;
}
function Me(e, t) {
  for (var n = -1, r = t.length, i = e.length; ++n < r; )
    e[i + n] = t[n];
  return e;
}
var We = w ? w.isConcatSpreadable : void 0;
function vi(e) {
  return A(e) || Ce(e) || !!(We && e && e[We]);
}
function Ti(e, t, n, r, i) {
  var o = -1, a = e.length;
  for (n || (n = vi), i || (i = []); ++o < a; ) {
    var s = e[o];
    n(s) ? Me(i, s) : i[i.length] = s;
  }
  return i;
}
function Oi(e) {
  var t = e == null ? 0 : e.length;
  return t ? Ti(e) : [];
}
function Pi(e) {
  return Gn(Jn(e, void 0, Oi), e + "");
}
var Le = Ft(Object.getPrototypeOf, Object), wi = "[object Object]", $i = Function.prototype, Ai = Object.prototype, Mt = $i.toString, Si = Ai.hasOwnProperty, Ci = Mt.call(Object);
function he(e) {
  if (!E(e) || N(e) != wi)
    return !1;
  var t = Le(e);
  if (t === null)
    return !0;
  var n = Si.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Mt.call(n) == Ci;
}
function xi(e, t, n) {
  var r = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), n = n > i ? i : n, n < 0 && (n += i), i = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++r < i; )
    o[r] = e[r + t];
  return o;
}
function Ei() {
  this.__data__ = new j(), this.size = 0;
}
function ji(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Ii(e) {
  return this.__data__.get(e);
}
function Fi(e) {
  return this.__data__.has(e);
}
var Mi = 200;
function Li(e, t) {
  var n = this.__data__;
  if (n instanceof j) {
    var r = n.__data__;
    if (!X || r.length < Mi - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new I(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function S(e) {
  var t = this.__data__ = new j(e);
  this.size = t.size;
}
S.prototype.clear = Ei;
S.prototype.delete = ji;
S.prototype.get = Ii;
S.prototype.has = Fi;
S.prototype.set = Li;
function Ri(e, t) {
  return e && W(t, Q(t), e);
}
function Ni(e, t) {
  return e && W(t, Ee(t), e);
}
var Lt = typeof exports == "object" && exports && !exports.nodeType && exports, Qe = Lt && typeof module == "object" && module && !module.nodeType && module, Di = Qe && Qe.exports === Lt, Ve = Di ? C.Buffer : void 0, ke = Ve ? Ve.allocUnsafe : void 0;
function Ki(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = ke ? ke(n) : new e.constructor(n);
  return e.copy(r), r;
}
function Ui(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = 0, o = []; ++n < r; ) {
    var a = e[n];
    t(a, n, e) && (o[i++] = a);
  }
  return o;
}
function Rt() {
  return [];
}
var Gi = Object.prototype, Bi = Gi.propertyIsEnumerable, et = Object.getOwnPropertySymbols, Re = et ? function(e) {
  return e == null ? [] : (e = Object(e), Ui(et(e), function(t) {
    return Bi.call(e, t);
  }));
} : Rt;
function zi(e, t) {
  return W(e, Re(e), t);
}
var Hi = Object.getOwnPropertySymbols, Nt = Hi ? function(e) {
  for (var t = []; e; )
    Me(t, Re(e)), e = Le(e);
  return t;
} : Rt;
function qi(e, t) {
  return W(e, Nt(e), t);
}
function Dt(e, t, n) {
  var r = t(e);
  return A(e) ? r : Me(r, n(e));
}
function ye(e) {
  return Dt(e, Q, Re);
}
function Kt(e) {
  return Dt(e, Ee, Nt);
}
var me = K(C, "DataView"), ve = K(C, "Promise"), Te = K(C, "Set"), tt = "[object Map]", Yi = "[object Object]", nt = "[object Promise]", rt = "[object Set]", it = "[object WeakMap]", ot = "[object DataView]", Ji = D(me), Xi = D(X), Zi = D(ve), Wi = D(Te), Qi = D(be), $ = N;
(me && $(new me(new ArrayBuffer(1))) != ot || X && $(new X()) != tt || ve && $(ve.resolve()) != nt || Te && $(new Te()) != rt || be && $(new be()) != it) && ($ = function(e) {
  var t = N(e), n = t == Yi ? e.constructor : void 0, r = n ? D(n) : "";
  if (r)
    switch (r) {
      case Ji:
        return ot;
      case Xi:
        return tt;
      case Zi:
        return nt;
      case Wi:
        return rt;
      case Qi:
        return it;
    }
  return t;
});
var Vi = Object.prototype, ki = Vi.hasOwnProperty;
function eo(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && ki.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var ie = C.Uint8Array;
function Ne(e) {
  var t = new e.constructor(e.byteLength);
  return new ie(t).set(new ie(e)), t;
}
function to(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var no = /\w*$/;
function ro(e) {
  var t = new e.constructor(e.source, no.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var at = w ? w.prototype : void 0, st = at ? at.valueOf : void 0;
function io(e) {
  return st ? Object(st.call(e)) : {};
}
function oo(e, t) {
  var n = t ? Ne(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var ao = "[object Boolean]", so = "[object Date]", uo = "[object Map]", lo = "[object Number]", fo = "[object RegExp]", co = "[object Set]", po = "[object String]", go = "[object Symbol]", _o = "[object ArrayBuffer]", bo = "[object DataView]", ho = "[object Float32Array]", yo = "[object Float64Array]", mo = "[object Int8Array]", vo = "[object Int16Array]", To = "[object Int32Array]", Oo = "[object Uint8Array]", Po = "[object Uint8ClampedArray]", wo = "[object Uint16Array]", $o = "[object Uint32Array]";
function Ao(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case _o:
      return Ne(e);
    case ao:
    case so:
      return new r(+e);
    case bo:
      return to(e, n);
    case ho:
    case yo:
    case mo:
    case vo:
    case To:
    case Oo:
    case Po:
    case wo:
    case $o:
      return oo(e, n);
    case uo:
      return new r();
    case lo:
    case po:
      return new r(e);
    case fo:
      return ro(e);
    case co:
      return new r();
    case go:
      return io(e);
  }
}
function So(e) {
  return typeof e.constructor == "function" && !Se(e) ? In(Le(e)) : {};
}
var Co = "[object Map]";
function xo(e) {
  return E(e) && $(e) == Co;
}
var ut = B && B.isMap, Eo = ut ? xe(ut) : xo, jo = "[object Set]";
function Io(e) {
  return E(e) && $(e) == jo;
}
var lt = B && B.isSet, Fo = lt ? xe(lt) : Io, Mo = 1, Lo = 2, Ro = 4, Ut = "[object Arguments]", No = "[object Array]", Do = "[object Boolean]", Ko = "[object Date]", Uo = "[object Error]", Gt = "[object Function]", Go = "[object GeneratorFunction]", Bo = "[object Map]", zo = "[object Number]", Bt = "[object Object]", Ho = "[object RegExp]", qo = "[object Set]", Yo = "[object String]", Jo = "[object Symbol]", Xo = "[object WeakMap]", Zo = "[object ArrayBuffer]", Wo = "[object DataView]", Qo = "[object Float32Array]", Vo = "[object Float64Array]", ko = "[object Int8Array]", ea = "[object Int16Array]", ta = "[object Int32Array]", na = "[object Uint8Array]", ra = "[object Uint8ClampedArray]", ia = "[object Uint16Array]", oa = "[object Uint32Array]", y = {};
y[Ut] = y[No] = y[Zo] = y[Wo] = y[Do] = y[Ko] = y[Qo] = y[Vo] = y[ko] = y[ea] = y[ta] = y[Bo] = y[zo] = y[Bt] = y[Ho] = y[qo] = y[Yo] = y[Jo] = y[na] = y[ra] = y[ia] = y[oa] = !0;
y[Uo] = y[Gt] = y[Xo] = !1;
function ee(e, t, n, r, i, o) {
  var a, s = t & Mo, u = t & Lo, l = t & Ro;
  if (n && (a = i ? n(e, r, i, o) : n(e)), a !== void 0)
    return a;
  if (!z(e))
    return e;
  var g = A(e);
  if (g) {
    if (a = eo(e), !s)
      return Mn(e, a);
  } else {
    var p = $(e), c = p == Gt || p == Go;
    if (re(e))
      return Ki(e, s);
    if (p == Bt || p == Ut || c && !i) {
      if (a = u || c ? {} : So(e), !s)
        return u ? qi(e, Ni(a, e)) : zi(e, Ri(a, e));
    } else {
      if (!y[p])
        return i ? e : {};
      a = Ao(e, p, s);
    }
  }
  o || (o = new S());
  var d = o.get(e);
  if (d)
    return d;
  o.set(e, a), Fo(e) ? e.forEach(function(f) {
    a.add(ee(f, t, n, f, e, o));
  }) : Eo(e) && e.forEach(function(f, b) {
    a.set(b, ee(f, t, n, b, e, o));
  });
  var m = l ? u ? Kt : ye : u ? Ee : Q, _ = g ? void 0 : m(e);
  return Bn(_ || e, function(f, b) {
    _ && (b = f, f = e[b]), At(a, b, ee(f, t, n, b, e, o));
  }), a;
}
var aa = "__lodash_hash_undefined__";
function sa(e) {
  return this.__data__.set(e, aa), this;
}
function ua(e) {
  return this.__data__.has(e);
}
function oe(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new I(); ++t < n; )
    this.add(e[t]);
}
oe.prototype.add = oe.prototype.push = sa;
oe.prototype.has = ua;
function la(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function fa(e, t) {
  return e.has(t);
}
var ca = 1, pa = 2;
function zt(e, t, n, r, i, o) {
  var a = n & ca, s = e.length, u = t.length;
  if (s != u && !(a && u > s))
    return !1;
  var l = o.get(e), g = o.get(t);
  if (l && g)
    return l == t && g == e;
  var p = -1, c = !0, d = n & pa ? new oe() : void 0;
  for (o.set(e, t), o.set(t, e); ++p < s; ) {
    var m = e[p], _ = t[p];
    if (r)
      var f = a ? r(_, m, p, t, e, o) : r(m, _, p, e, t, o);
    if (f !== void 0) {
      if (f)
        continue;
      c = !1;
      break;
    }
    if (d) {
      if (!la(t, function(b, T) {
        if (!fa(d, T) && (m === b || i(m, b, n, r, o)))
          return d.push(T);
      })) {
        c = !1;
        break;
      }
    } else if (!(m === _ || i(m, _, n, r, o))) {
      c = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), c;
}
function ga(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, i) {
    n[++t] = [i, r];
  }), n;
}
function da(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var _a = 1, ba = 2, ha = "[object Boolean]", ya = "[object Date]", ma = "[object Error]", va = "[object Map]", Ta = "[object Number]", Oa = "[object RegExp]", Pa = "[object Set]", wa = "[object String]", $a = "[object Symbol]", Aa = "[object ArrayBuffer]", Sa = "[object DataView]", ft = w ? w.prototype : void 0, ge = ft ? ft.valueOf : void 0;
function Ca(e, t, n, r, i, o, a) {
  switch (n) {
    case Sa:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case Aa:
      return !(e.byteLength != t.byteLength || !o(new ie(e), new ie(t)));
    case ha:
    case ya:
    case Ta:
      return $e(+e, +t);
    case ma:
      return e.name == t.name && e.message == t.message;
    case Oa:
    case wa:
      return e == t + "";
    case va:
      var s = ga;
    case Pa:
      var u = r & _a;
      if (s || (s = da), e.size != t.size && !u)
        return !1;
      var l = a.get(e);
      if (l)
        return l == t;
      r |= ba, a.set(e, t);
      var g = zt(s(e), s(t), r, i, o, a);
      return a.delete(e), g;
    case $a:
      if (ge)
        return ge.call(e) == ge.call(t);
  }
  return !1;
}
var xa = 1, Ea = Object.prototype, ja = Ea.hasOwnProperty;
function Ia(e, t, n, r, i, o) {
  var a = n & xa, s = ye(e), u = s.length, l = ye(t), g = l.length;
  if (u != g && !a)
    return !1;
  for (var p = u; p--; ) {
    var c = s[p];
    if (!(a ? c in t : ja.call(t, c)))
      return !1;
  }
  var d = o.get(e), m = o.get(t);
  if (d && m)
    return d == t && m == e;
  var _ = !0;
  o.set(e, t), o.set(t, e);
  for (var f = a; ++p < u; ) {
    c = s[p];
    var b = e[c], T = t[c];
    if (r)
      var P = a ? r(T, b, c, t, e, o) : r(b, T, c, e, t, o);
    if (!(P === void 0 ? b === T || i(b, T, n, r, o) : P)) {
      _ = !1;
      break;
    }
    f || (f = c == "constructor");
  }
  if (_ && !f) {
    var F = e.constructor, M = t.constructor;
    F != M && "constructor" in e && "constructor" in t && !(typeof F == "function" && F instanceof F && typeof M == "function" && M instanceof M) && (_ = !1);
  }
  return o.delete(e), o.delete(t), _;
}
var Fa = 1, ct = "[object Arguments]", pt = "[object Array]", k = "[object Object]", Ma = Object.prototype, gt = Ma.hasOwnProperty;
function La(e, t, n, r, i, o) {
  var a = A(e), s = A(t), u = a ? pt : $(e), l = s ? pt : $(t);
  u = u == ct ? k : u, l = l == ct ? k : l;
  var g = u == k, p = l == k, c = u == l;
  if (c && re(e)) {
    if (!re(t))
      return !1;
    a = !0, g = !1;
  }
  if (c && !g)
    return o || (o = new S()), a || jt(e) ? zt(e, t, n, r, i, o) : Ca(e, t, u, n, r, i, o);
  if (!(n & Fa)) {
    var d = g && gt.call(e, "__wrapped__"), m = p && gt.call(t, "__wrapped__");
    if (d || m) {
      var _ = d ? e.value() : e, f = m ? t.value() : t;
      return o || (o = new S()), i(_, f, n, r, o);
    }
  }
  return c ? (o || (o = new S()), Ia(e, t, n, r, i, o)) : !1;
}
function De(e, t, n, r, i) {
  return e === t ? !0 : e == null || t == null || !E(e) && !E(t) ? e !== e && t !== t : La(e, t, n, r, De, i);
}
var Ra = 1, Na = 2;
function Da(e, t, n, r) {
  var i = n.length, o = i;
  if (e == null)
    return !o;
  for (e = Object(e); i--; ) {
    var a = n[i];
    if (a[2] ? a[1] !== e[a[0]] : !(a[0] in e))
      return !1;
  }
  for (; ++i < o; ) {
    a = n[i];
    var s = a[0], u = e[s], l = a[1];
    if (a[2]) {
      if (u === void 0 && !(s in e))
        return !1;
    } else {
      var g = new S(), p;
      if (!(p === void 0 ? De(l, u, Ra | Na, r, g) : p))
        return !1;
    }
  }
  return !0;
}
function Ht(e) {
  return e === e && !z(e);
}
function Ka(e) {
  for (var t = Q(e), n = t.length; n--; ) {
    var r = t[n], i = e[r];
    t[n] = [r, i, Ht(i)];
  }
  return t;
}
function qt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function Ua(e) {
  var t = Ka(e);
  return t.length == 1 && t[0][2] ? qt(t[0][0], t[0][1]) : function(n) {
    return n === e || Da(n, e, t);
  };
}
function Ga(e, t) {
  return e != null && t in Object(e);
}
function Ba(e, t, n) {
  t = le(t, e);
  for (var r = -1, i = t.length, o = !1; ++r < i; ) {
    var a = V(t[r]);
    if (!(o = e != null && n(e, a)))
      break;
    e = e[a];
  }
  return o || ++r != i ? o : (i = e == null ? 0 : e.length, !!i && Ae(i) && $t(a, i) && (A(e) || Ce(e)));
}
function za(e, t) {
  return e != null && Ba(e, t, Ga);
}
var Ha = 1, qa = 2;
function Ya(e, t) {
  return je(e) && Ht(t) ? qt(V(e), t) : function(n) {
    var r = mi(n, e);
    return r === void 0 && r === t ? za(n, e) : De(t, r, Ha | qa);
  };
}
function Ja(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Xa(e) {
  return function(t) {
    return Fe(t, e);
  };
}
function Za(e) {
  return je(e) ? Ja(V(e)) : Xa(e);
}
function Wa(e) {
  return typeof e == "function" ? e : e == null ? Pt : typeof e == "object" ? A(e) ? Ya(e[0], e[1]) : Ua(e) : Za(e);
}
function Qa(e) {
  return function(t, n, r) {
    for (var i = -1, o = Object(t), a = r(t), s = a.length; s--; ) {
      var u = a[++i];
      if (n(o[u], u, o) === !1)
        break;
    }
    return t;
  };
}
var Va = Qa();
function ka(e, t) {
  return e && Va(e, t, Q);
}
function es(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function ts(e, t) {
  return t.length < 2 ? e : Fe(e, xi(t, 0, -1));
}
function ns(e, t) {
  var n = {};
  return t = Wa(t), ka(e, function(r, i, o) {
    we(n, t(r, i, o), r);
  }), n;
}
function rs(e, t) {
  return t = le(t, e), e = ts(e, t), e == null || delete e[V(es(t))];
}
function is(e) {
  return he(e) ? void 0 : e;
}
var os = 1, as = 2, ss = 4, Yt = Pi(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = Tt(t, function(o) {
    return o = le(o, e), r || (r = o.length > 1), o;
  }), W(e, Kt(e), n), r && (n = ee(n, os | as | ss, is));
  for (var i = t.length; i--; )
    rs(n, t[i]);
  return n;
});
async function us() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function ls(e) {
  return await us(), e().then((t) => t.default);
}
const Jt = [
  "interactive",
  "gradio",
  "server",
  "target",
  "theme_mode",
  "root",
  "name",
  // 'visible',
  // 'elem_id',
  // 'elem_classes',
  // 'elem_style',
  "_internal",
  "props",
  // 'value',
  "_selectable",
  "loading_status",
  "value_is_output"
], fs = Jt.concat(["attached_events"]);
function cs(e, t = {}, n = !1) {
  return ns(Yt(e, n ? [] : Jt), (r, i) => t[i] || rn(i));
}
function dt(e, t) {
  const {
    gradio: n,
    _internal: r,
    restProps: i,
    originalRestProps: o,
    ...a
  } = e, s = (i == null ? void 0 : i.attachedEvents) || [];
  return {
    ...Array.from(/* @__PURE__ */ new Set([...Object.keys(r).map((u) => {
      const l = u.match(/bind_(.+)_event/);
      return l && l[1] ? l[1] : null;
    }).filter(Boolean), ...s.map((u) => t && t[u] ? t[u] : u)])).reduce((u, l) => {
      const g = l.split("_"), p = (...d) => {
        const m = d.map((f) => d && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        let _;
        try {
          _ = JSON.parse(JSON.stringify(m));
        } catch {
          let f = function(b) {
            try {
              return JSON.stringify(b), b;
            } catch {
              return he(b) ? Object.fromEntries(Object.entries(b).map(([T, P]) => {
                try {
                  return JSON.stringify(P), [T, P];
                } catch {
                  return he(P) ? [T, Object.fromEntries(Object.entries(P).filter(([F, M]) => {
                    try {
                      return JSON.stringify(M), !0;
                    } catch {
                      return !1;
                    }
                  }))] : null;
                }
              }).filter(Boolean)) : {};
            }
          };
          _ = m.map((b) => f(b));
        }
        return n.dispatch(l.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: _,
          component: {
            ...a,
            ...Yt(o, fs)
          }
        });
      };
      if (g.length > 1) {
        let d = {
          ...a.props[g[0]] || (i == null ? void 0 : i[g[0]]) || {}
        };
        u[g[0]] = d;
        for (let _ = 1; _ < g.length - 1; _++) {
          const f = {
            ...a.props[g[_]] || (i == null ? void 0 : i[g[_]]) || {}
          };
          d[g[_]] = f, d = f;
        }
        const m = g[g.length - 1];
        return d[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = p, u;
      }
      const c = g[0];
      return u[`on${c.slice(0, 1).toUpperCase()}${c.slice(1)}`] = p, u;
    }, {}),
    __render_eventProps: {
      props: e,
      eventsMapping: t
    }
  };
}
function te() {
}
function ps(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function gs(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return te;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function Xt(e) {
  let t;
  return gs(e, (n) => t = n)(), t;
}
const U = [];
function x(e, t = te) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(s) {
    if (ps(e, s) && (e = s, n)) {
      const u = !U.length;
      for (const l of r)
        l[1](), U.push(l, e);
      if (u) {
        for (let l = 0; l < U.length; l += 2)
          U[l][0](U[l + 1]);
        U.length = 0;
      }
    }
  }
  function o(s) {
    i(s(e));
  }
  function a(s, u = te) {
    const l = [s, u];
    return r.add(l), r.size === 1 && (n = t(i, o) || te), s(e), () => {
      r.delete(l), r.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: a
  };
}
const {
  getContext: ds,
  setContext: ks
} = window.__gradio__svelte__internal, _s = "$$ms-gr-loading-status-key";
function bs() {
  const e = window.ms_globals.loadingKey++, t = ds(_s);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: i
    } = t, {
      generating: o,
      error: a
    } = Xt(i);
    (n == null ? void 0 : n.status) === "pending" || a && (n == null ? void 0 : n.status) === "error" || (o && (n == null ? void 0 : n.status)) === "generating" ? r.update(({
      map: s
    }) => (s.set(e, n), {
      map: s
    })) : r.update(({
      map: s
    }) => (s.delete(e), {
      map: s
    }));
  };
}
const {
  getContext: fe,
  setContext: H
} = window.__gradio__svelte__internal, hs = "$$ms-gr-slots-key";
function ys() {
  const e = x({});
  return H(hs, e);
}
const Zt = "$$ms-gr-slot-params-mapping-fn-key";
function ms() {
  return fe(Zt);
}
function vs(e) {
  return H(Zt, x(e));
}
const Ts = "$$ms-gr-slot-params-key";
function Os() {
  const e = H(Ts, x({}));
  return (t, n) => {
    e.update((r) => typeof n == "function" ? {
      ...r,
      [t]: n(r[t])
    } : {
      ...r,
      [t]: n
    });
  };
}
const Wt = "$$ms-gr-sub-index-context-key";
function Ps() {
  return fe(Wt) || null;
}
function _t(e) {
  return H(Wt, e);
}
function ws(e, t, n) {
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = As(), i = ms();
  vs().set(void 0);
  const a = Ss({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = Ps();
  typeof s == "number" && _t(void 0);
  const u = bs();
  typeof e._internal.subIndex == "number" && _t(e._internal.subIndex), r && r.subscribe((c) => {
    a.slotKey.set(c);
  }), $s();
  const l = e.as_item, g = (c, d) => c ? {
    ...cs({
      ...c
    }, t),
    __render_slotParamsMappingFn: i ? Xt(i) : void 0,
    __render_as_item: d,
    __render_restPropsMapping: t
  } : void 0, p = x({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    restProps: g(e.restProps, l),
    originalRestProps: e.restProps
  });
  return i && i.subscribe((c) => {
    p.update((d) => ({
      ...d,
      restProps: {
        ...d.restProps,
        __slotParamsMappingFn: c
      }
    }));
  }), [p, (c) => {
    var d;
    u((d = c.restProps) == null ? void 0 : d.loading_status), p.set({
      ...c,
      _internal: {
        ...c._internal,
        index: s ?? c._internal.index
      },
      restProps: g(c.restProps, c.as_item),
      originalRestProps: c.restProps
    });
  }];
}
const Qt = "$$ms-gr-slot-key";
function $s() {
  H(Qt, x(void 0));
}
function As() {
  return fe(Qt);
}
const Vt = "$$ms-gr-component-slot-context-key";
function Ss({
  slot: e,
  index: t,
  subIndex: n
}) {
  return H(Vt, {
    slotKey: x(e),
    slotIndex: x(t),
    subSlotIndex: x(n)
  });
}
function eu() {
  return fe(Vt);
}
function Cs(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var kt = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function n() {
      for (var o = "", a = 0; a < arguments.length; a++) {
        var s = arguments[a];
        s && (o = i(o, r(s)));
      }
      return o;
    }
    function r(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return n.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var a = "";
      for (var s in o)
        t.call(o, s) && o[s] && (a = i(a, s));
      return a;
    }
    function i(o, a) {
      return a ? o ? o + " " + a : o + a : o;
    }
    e.exports ? (n.default = n, e.exports = n) : window.classNames = n;
  })();
})(kt);
var xs = kt.exports;
const bt = /* @__PURE__ */ Cs(xs), {
  SvelteComponent: Es,
  assign: Oe,
  check_outros: js,
  claim_component: Is,
  component_subscribe: de,
  compute_rest_props: ht,
  create_component: Fs,
  create_slot: Ms,
  destroy_component: Ls,
  detach: en,
  empty: ae,
  exclude_internal_props: Rs,
  flush: L,
  get_all_dirty_from_scope: Ns,
  get_slot_changes: Ds,
  get_spread_object: _e,
  get_spread_update: Ks,
  group_outros: Us,
  handle_promise: Gs,
  init: Bs,
  insert_hydration: tn,
  mount_component: zs,
  noop: O,
  safe_not_equal: Hs,
  transition_in: G,
  transition_out: Z,
  update_await_block_branch: qs,
  update_slot_base: Ys
} = window.__gradio__svelte__internal;
function yt(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ws,
    then: Xs,
    catch: Js,
    value: 20,
    blocks: [, , ,]
  };
  return Gs(
    /*AwaitedBubble*/
    e[2],
    r
  ), {
    c() {
      t = ae(), r.block.c();
    },
    l(i) {
      t = ae(), r.block.l(i);
    },
    m(i, o) {
      tn(i, t, o), r.block.m(i, r.anchor = o), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(i, o) {
      e = i, qs(r, e, o);
    },
    i(i) {
      n || (G(r.block), n = !0);
    },
    o(i) {
      for (let o = 0; o < 3; o += 1) {
        const a = r.blocks[o];
        Z(a);
      }
      n = !1;
    },
    d(i) {
      i && en(t), r.block.d(i), r.token = null, r = null;
    }
  };
}
function Js(e) {
  return {
    c: O,
    l: O,
    m: O,
    p: O,
    i: O,
    o: O,
    d: O
  };
}
function Xs(e) {
  let t, n;
  const r = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: bt(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antdx-bubble"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].restProps,
    /*$mergedProps*/
    e[0].props,
    dt(
      /*$mergedProps*/
      e[0],
      {
        typing_complete: "typingComplete"
      }
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      setSlotParams: (
        /*setSlotParams*/
        e[5]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Zs]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let o = 0; o < r.length; o += 1)
    i = Oe(i, r[o]);
  return t = new /*Bubble*/
  e[20]({
    props: i
  }), {
    c() {
      Fs(t.$$.fragment);
    },
    l(o) {
      Is(t.$$.fragment, o);
    },
    m(o, a) {
      zs(t, o, a), n = !0;
    },
    p(o, a) {
      const s = a & /*$mergedProps, $slots, setSlotParams*/
      35 ? Ks(r, [a & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          o[0].elem_style
        )
      }, a & /*$mergedProps*/
      1 && {
        className: bt(
          /*$mergedProps*/
          o[0].elem_classes,
          "ms-gr-antdx-bubble"
        )
      }, a & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          o[0].elem_id
        )
      }, a & /*$mergedProps*/
      1 && _e(
        /*$mergedProps*/
        o[0].restProps
      ), a & /*$mergedProps*/
      1 && _e(
        /*$mergedProps*/
        o[0].props
      ), a & /*$mergedProps*/
      1 && _e(dt(
        /*$mergedProps*/
        o[0],
        {
          typing_complete: "typingComplete"
        }
      )), a & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          o[1]
        )
      }, a & /*setSlotParams*/
      32 && {
        setSlotParams: (
          /*setSlotParams*/
          o[5]
        )
      }]) : {};
      a & /*$$scope*/
      131072 && (s.$$scope = {
        dirty: a,
        ctx: o
      }), t.$set(s);
    },
    i(o) {
      n || (G(t.$$.fragment, o), n = !0);
    },
    o(o) {
      Z(t.$$.fragment, o), n = !1;
    },
    d(o) {
      Ls(t, o);
    }
  };
}
function Zs(e) {
  let t;
  const n = (
    /*#slots*/
    e[16].default
  ), r = Ms(
    n,
    e,
    /*$$scope*/
    e[17],
    null
  );
  return {
    c() {
      r && r.c();
    },
    l(i) {
      r && r.l(i);
    },
    m(i, o) {
      r && r.m(i, o), t = !0;
    },
    p(i, o) {
      r && r.p && (!t || o & /*$$scope*/
      131072) && Ys(
        r,
        n,
        i,
        /*$$scope*/
        i[17],
        t ? Ds(
          n,
          /*$$scope*/
          i[17],
          o,
          null
        ) : Ns(
          /*$$scope*/
          i[17]
        ),
        null
      );
    },
    i(i) {
      t || (G(r, i), t = !0);
    },
    o(i) {
      Z(r, i), t = !1;
    },
    d(i) {
      r && r.d(i);
    }
  };
}
function Ws(e) {
  return {
    c: O,
    l: O,
    m: O,
    p: O,
    i: O,
    o: O,
    d: O
  };
}
function Qs(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && yt(e)
  );
  return {
    c() {
      r && r.c(), t = ae();
    },
    l(i) {
      r && r.l(i), t = ae();
    },
    m(i, o) {
      r && r.m(i, o), tn(i, t, o), n = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[0].visible ? r ? (r.p(i, o), o & /*$mergedProps*/
      1 && G(r, 1)) : (r = yt(i), r.c(), G(r, 1), r.m(t.parentNode, t)) : r && (Us(), Z(r, 1, 1, () => {
        r = null;
      }), js());
    },
    i(i) {
      n || (G(r), n = !0);
    },
    o(i) {
      Z(r), n = !1;
    },
    d(i) {
      i && en(t), r && r.d(i);
    }
  };
}
function Vs(e, t, n) {
  const r = ["gradio", "props", "_internal", "as_item", "visible", "elem_id", "elem_classes", "elem_style"];
  let i = ht(t, r), o, a, s, {
    $$slots: u = {},
    $$scope: l
  } = t;
  const g = ls(() => import("./bubble-CSmAZOmy.js"));
  let {
    gradio: p
  } = t, {
    props: c = {}
  } = t;
  const d = x(c);
  de(e, d, (h) => n(15, o = h));
  let {
    _internal: m = {}
  } = t, {
    as_item: _
  } = t, {
    visible: f = !0
  } = t, {
    elem_id: b = ""
  } = t, {
    elem_classes: T = []
  } = t, {
    elem_style: P = {}
  } = t;
  const [F, M] = ws({
    gradio: p,
    props: o,
    _internal: m,
    visible: f,
    elem_id: b,
    elem_classes: T,
    elem_style: P,
    as_item: _,
    restProps: i
  });
  de(e, F, (h) => n(0, a = h));
  const nn = Os(), Ke = ys();
  return de(e, Ke, (h) => n(1, s = h)), e.$$set = (h) => {
    t = Oe(Oe({}, t), Rs(h)), n(19, i = ht(t, r)), "gradio" in h && n(7, p = h.gradio), "props" in h && n(8, c = h.props), "_internal" in h && n(9, m = h._internal), "as_item" in h && n(10, _ = h.as_item), "visible" in h && n(11, f = h.visible), "elem_id" in h && n(12, b = h.elem_id), "elem_classes" in h && n(13, T = h.elem_classes), "elem_style" in h && n(14, P = h.elem_style), "$$scope" in h && n(17, l = h.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && d.update((h) => ({
      ...h,
      ...c
    })), M({
      gradio: p,
      props: o,
      _internal: m,
      visible: f,
      elem_id: b,
      elem_classes: T,
      elem_style: P,
      as_item: _,
      restProps: i
    });
  }, [a, s, g, d, F, nn, Ke, p, c, m, _, f, b, T, P, o, u, l];
}
class tu extends Es {
  constructor(t) {
    super(), Bs(this, t, Vs, Qs, Hs, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), L();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), L();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), L();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), L();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), L();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), L();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), L();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), L();
  }
}
export {
  tu as I,
  z as a,
  wt as b,
  bt as c,
  eu as g,
  Pe as i,
  C as r,
  x as w
};
