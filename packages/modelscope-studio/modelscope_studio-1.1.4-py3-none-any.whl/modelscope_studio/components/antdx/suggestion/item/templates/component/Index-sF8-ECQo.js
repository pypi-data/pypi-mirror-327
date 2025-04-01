function sn(e) {
  return e.replace(/(^|_)(\w)/g, (t, n, r, i) => i === 0 ? r.toLowerCase() : r.toUpperCase());
}
var Tt = typeof global == "object" && global && global.Object === Object && global, un = typeof self == "object" && self && self.Object === Object && self, I = Tt || un || Function("return this")(), w = I.Symbol, Ot = Object.prototype, ln = Ot.hasOwnProperty, cn = Ot.toString, q = w ? w.toStringTag : void 0;
function fn(e) {
  var t = ln.call(e, q), n = e[q];
  try {
    e[q] = void 0;
    var r = !0;
  } catch {
  }
  var i = cn.call(e);
  return r && (t ? e[q] = n : delete e[q]), i;
}
var pn = Object.prototype, gn = pn.toString;
function dn(e) {
  return gn.call(e);
}
var _n = "[object Null]", bn = "[object Undefined]", He = w ? w.toStringTag : void 0;
function N(e) {
  return e == null ? e === void 0 ? bn : _n : He && He in Object(e) ? fn(e) : dn(e);
}
function M(e) {
  return e != null && typeof e == "object";
}
var hn = "[object Symbol]";
function Ae(e) {
  return typeof e == "symbol" || M(e) && N(e) == hn;
}
function Pt(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = Array(r); ++n < r; )
    i[n] = t(e[n], n, e);
  return i;
}
var S = Array.isArray, yn = 1 / 0, qe = w ? w.prototype : void 0, Ye = qe ? qe.toString : void 0;
function wt(e) {
  if (typeof e == "string")
    return e;
  if (S(e))
    return Pt(e, wt) + "";
  if (Ae(e))
    return Ye ? Ye.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -yn ? "-0" : t;
}
function z(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function At(e) {
  return e;
}
var mn = "[object AsyncFunction]", vn = "[object Function]", Tn = "[object GeneratorFunction]", On = "[object Proxy]";
function $t(e) {
  if (!z(e))
    return !1;
  var t = N(e);
  return t == vn || t == Tn || t == mn || t == On;
}
var _e = I["__core-js_shared__"], Je = function() {
  var e = /[^.]+$/.exec(_e && _e.keys && _e.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Pn(e) {
  return !!Je && Je in e;
}
var wn = Function.prototype, An = wn.toString;
function D(e) {
  if (e != null) {
    try {
      return An.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var $n = /[\\^$.*+?()[\]{}|]/g, Sn = /^\[object .+?Constructor\]$/, xn = Function.prototype, Cn = Object.prototype, En = xn.toString, In = Cn.hasOwnProperty, jn = RegExp("^" + En.call(In).replace($n, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function Mn(e) {
  if (!z(e) || Pn(e))
    return !1;
  var t = $t(e) ? jn : Sn;
  return t.test(D(e));
}
function Fn(e, t) {
  return e == null ? void 0 : e[t];
}
function K(e, t) {
  var n = Fn(e, t);
  return Mn(n) ? n : void 0;
}
var ye = K(I, "WeakMap"), Xe = Object.create, Ln = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!z(t))
      return {};
    if (Xe)
      return Xe(t);
    e.prototype = t;
    var n = new e();
    return e.prototype = void 0, n;
  };
}();
function Rn(e, t, n) {
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
function Nn(e, t) {
  var n = -1, r = e.length;
  for (t || (t = Array(r)); ++n < r; )
    t[n] = e[n];
  return t;
}
var Dn = 800, Kn = 16, Un = Date.now;
function Gn(e) {
  var t = 0, n = 0;
  return function() {
    var r = Un(), i = Kn - (r - n);
    if (n = r, i > 0) {
      if (++t >= Dn)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function Bn(e) {
  return function() {
    return e;
  };
}
var oe = function() {
  try {
    var e = K(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), zn = oe ? function(e, t) {
  return oe(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: Bn(t),
    writable: !0
  });
} : At, Hn = Gn(zn);
function qn(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r && t(e[n], n, e) !== !1; )
    ;
  return e;
}
var Yn = 9007199254740991, Jn = /^(?:0|[1-9]\d*)$/;
function St(e, t) {
  var n = typeof e;
  return t = t ?? Yn, !!t && (n == "number" || n != "symbol" && Jn.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function $e(e, t, n) {
  t == "__proto__" && oe ? oe(e, t, {
    configurable: !0,
    enumerable: !0,
    value: n,
    writable: !0
  }) : e[t] = n;
}
function Se(e, t) {
  return e === t || e !== e && t !== t;
}
var Xn = Object.prototype, Zn = Xn.hasOwnProperty;
function xt(e, t, n) {
  var r = e[t];
  (!(Zn.call(e, t) && Se(r, n)) || n === void 0 && !(t in e)) && $e(e, t, n);
}
function W(e, t, n, r) {
  var i = !n;
  n || (n = {});
  for (var o = -1, a = t.length; ++o < a; ) {
    var s = t[o], u = void 0;
    u === void 0 && (u = e[s]), i ? $e(n, s, u) : xt(n, s, u);
  }
  return n;
}
var Ze = Math.max;
function Wn(e, t, n) {
  return t = Ze(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var r = arguments, i = -1, o = Ze(r.length - t, 0), a = Array(o); ++i < o; )
      a[i] = r[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = r[i];
    return s[t] = n(a), Rn(e, this, s);
  };
}
var Qn = 9007199254740991;
function xe(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= Qn;
}
function Ct(e) {
  return e != null && xe(e.length) && !$t(e);
}
var Vn = Object.prototype;
function Ce(e) {
  var t = e && e.constructor, n = typeof t == "function" && t.prototype || Vn;
  return e === n;
}
function kn(e, t) {
  for (var n = -1, r = Array(e); ++n < e; )
    r[n] = t(n);
  return r;
}
var er = "[object Arguments]";
function We(e) {
  return M(e) && N(e) == er;
}
var Et = Object.prototype, tr = Et.hasOwnProperty, nr = Et.propertyIsEnumerable, Ee = We(/* @__PURE__ */ function() {
  return arguments;
}()) ? We : function(e) {
  return M(e) && tr.call(e, "callee") && !nr.call(e, "callee");
};
function rr() {
  return !1;
}
var It = typeof exports == "object" && exports && !exports.nodeType && exports, Qe = It && typeof module == "object" && module && !module.nodeType && module, ir = Qe && Qe.exports === It, Ve = ir ? I.Buffer : void 0, or = Ve ? Ve.isBuffer : void 0, ae = or || rr, ar = "[object Arguments]", sr = "[object Array]", ur = "[object Boolean]", lr = "[object Date]", cr = "[object Error]", fr = "[object Function]", pr = "[object Map]", gr = "[object Number]", dr = "[object Object]", _r = "[object RegExp]", br = "[object Set]", hr = "[object String]", yr = "[object WeakMap]", mr = "[object ArrayBuffer]", vr = "[object DataView]", Tr = "[object Float32Array]", Or = "[object Float64Array]", Pr = "[object Int8Array]", wr = "[object Int16Array]", Ar = "[object Int32Array]", $r = "[object Uint8Array]", Sr = "[object Uint8ClampedArray]", xr = "[object Uint16Array]", Cr = "[object Uint32Array]", v = {};
v[Tr] = v[Or] = v[Pr] = v[wr] = v[Ar] = v[$r] = v[Sr] = v[xr] = v[Cr] = !0;
v[ar] = v[sr] = v[mr] = v[ur] = v[vr] = v[lr] = v[cr] = v[fr] = v[pr] = v[gr] = v[dr] = v[_r] = v[br] = v[hr] = v[yr] = !1;
function Er(e) {
  return M(e) && xe(e.length) && !!v[N(e)];
}
function Ie(e) {
  return function(t) {
    return e(t);
  };
}
var jt = typeof exports == "object" && exports && !exports.nodeType && exports, Y = jt && typeof module == "object" && module && !module.nodeType && module, Ir = Y && Y.exports === jt, be = Ir && Tt.process, B = function() {
  try {
    var e = Y && Y.require && Y.require("util").types;
    return e || be && be.binding && be.binding("util");
  } catch {
  }
}(), ke = B && B.isTypedArray, Mt = ke ? Ie(ke) : Er, jr = Object.prototype, Mr = jr.hasOwnProperty;
function Ft(e, t) {
  var n = S(e), r = !n && Ee(e), i = !n && !r && ae(e), o = !n && !r && !i && Mt(e), a = n || r || i || o, s = a ? kn(e.length, String) : [], u = s.length;
  for (var l in e)
    (t || Mr.call(e, l)) && !(a && // Safari 9 has enumerable `arguments.length` in strict mode.
    (l == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (l == "offset" || l == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    o && (l == "buffer" || l == "byteLength" || l == "byteOffset") || // Skip index properties.
    St(l, u))) && s.push(l);
  return s;
}
function Lt(e, t) {
  return function(n) {
    return e(t(n));
  };
}
var Fr = Lt(Object.keys, Object), Lr = Object.prototype, Rr = Lr.hasOwnProperty;
function Nr(e) {
  if (!Ce(e))
    return Fr(e);
  var t = [];
  for (var n in Object(e))
    Rr.call(e, n) && n != "constructor" && t.push(n);
  return t;
}
function Q(e) {
  return Ct(e) ? Ft(e) : Nr(e);
}
function Dr(e) {
  var t = [];
  if (e != null)
    for (var n in Object(e))
      t.push(n);
  return t;
}
var Kr = Object.prototype, Ur = Kr.hasOwnProperty;
function Gr(e) {
  if (!z(e))
    return Dr(e);
  var t = Ce(e), n = [];
  for (var r in e)
    r == "constructor" && (t || !Ur.call(e, r)) || n.push(r);
  return n;
}
function je(e) {
  return Ct(e) ? Ft(e, !0) : Gr(e);
}
var Br = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, zr = /^\w*$/;
function Me(e, t) {
  if (S(e))
    return !1;
  var n = typeof e;
  return n == "number" || n == "symbol" || n == "boolean" || e == null || Ae(e) ? !0 : zr.test(e) || !Br.test(e) || t != null && e in Object(t);
}
var J = K(Object, "create");
function Hr() {
  this.__data__ = J ? J(null) : {}, this.size = 0;
}
function qr(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Yr = "__lodash_hash_undefined__", Jr = Object.prototype, Xr = Jr.hasOwnProperty;
function Zr(e) {
  var t = this.__data__;
  if (J) {
    var n = t[e];
    return n === Yr ? void 0 : n;
  }
  return Xr.call(t, e) ? t[e] : void 0;
}
var Wr = Object.prototype, Qr = Wr.hasOwnProperty;
function Vr(e) {
  var t = this.__data__;
  return J ? t[e] !== void 0 : Qr.call(t, e);
}
var kr = "__lodash_hash_undefined__";
function ei(e, t) {
  var n = this.__data__;
  return this.size += this.has(e) ? 0 : 1, n[e] = J && t === void 0 ? kr : t, this;
}
function R(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
R.prototype.clear = Hr;
R.prototype.delete = qr;
R.prototype.get = Zr;
R.prototype.has = Vr;
R.prototype.set = ei;
function ti() {
  this.__data__ = [], this.size = 0;
}
function ce(e, t) {
  for (var n = e.length; n--; )
    if (Se(e[n][0], t))
      return n;
  return -1;
}
var ni = Array.prototype, ri = ni.splice;
function ii(e) {
  var t = this.__data__, n = ce(t, e);
  if (n < 0)
    return !1;
  var r = t.length - 1;
  return n == r ? t.pop() : ri.call(t, n, 1), --this.size, !0;
}
function oi(e) {
  var t = this.__data__, n = ce(t, e);
  return n < 0 ? void 0 : t[n][1];
}
function ai(e) {
  return ce(this.__data__, e) > -1;
}
function si(e, t) {
  var n = this.__data__, r = ce(n, e);
  return r < 0 ? (++this.size, n.push([e, t])) : n[r][1] = t, this;
}
function F(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
F.prototype.clear = ti;
F.prototype.delete = ii;
F.prototype.get = oi;
F.prototype.has = ai;
F.prototype.set = si;
var X = K(I, "Map");
function ui() {
  this.size = 0, this.__data__ = {
    hash: new R(),
    map: new (X || F)(),
    string: new R()
  };
}
function li(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function fe(e, t) {
  var n = e.__data__;
  return li(t) ? n[typeof t == "string" ? "string" : "hash"] : n.map;
}
function ci(e) {
  var t = fe(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function fi(e) {
  return fe(this, e).get(e);
}
function pi(e) {
  return fe(this, e).has(e);
}
function gi(e, t) {
  var n = fe(this, e), r = n.size;
  return n.set(e, t), this.size += n.size == r ? 0 : 1, this;
}
function L(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.clear(); ++t < n; ) {
    var r = e[t];
    this.set(r[0], r[1]);
  }
}
L.prototype.clear = ui;
L.prototype.delete = ci;
L.prototype.get = fi;
L.prototype.has = pi;
L.prototype.set = gi;
var di = "Expected a function";
function Fe(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(di);
  var n = function() {
    var r = arguments, i = t ? t.apply(this, r) : r[0], o = n.cache;
    if (o.has(i))
      return o.get(i);
    var a = e.apply(this, r);
    return n.cache = o.set(i, a) || o, a;
  };
  return n.cache = new (Fe.Cache || L)(), n;
}
Fe.Cache = L;
var _i = 500;
function bi(e) {
  var t = Fe(e, function(r) {
    return n.size === _i && n.clear(), r;
  }), n = t.cache;
  return t;
}
var hi = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, yi = /\\(\\)?/g, mi = bi(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(hi, function(n, r, i, o) {
    t.push(i ? o.replace(yi, "$1") : r || n);
  }), t;
});
function vi(e) {
  return e == null ? "" : wt(e);
}
function pe(e, t) {
  return S(e) ? e : Me(e, t) ? [e] : mi(vi(e));
}
var Ti = 1 / 0;
function V(e) {
  if (typeof e == "string" || Ae(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -Ti ? "-0" : t;
}
function Le(e, t) {
  t = pe(t, e);
  for (var n = 0, r = t.length; e != null && n < r; )
    e = e[V(t[n++])];
  return n && n == r ? e : void 0;
}
function Oi(e, t, n) {
  var r = e == null ? void 0 : Le(e, t);
  return r === void 0 ? n : r;
}
function Re(e, t) {
  for (var n = -1, r = t.length, i = e.length; ++n < r; )
    e[i + n] = t[n];
  return e;
}
var et = w ? w.isConcatSpreadable : void 0;
function Pi(e) {
  return S(e) || Ee(e) || !!(et && e && e[et]);
}
function wi(e, t, n, r, i) {
  var o = -1, a = e.length;
  for (n || (n = Pi), i || (i = []); ++o < a; ) {
    var s = e[o];
    n(s) ? Re(i, s) : i[i.length] = s;
  }
  return i;
}
function Ai(e) {
  var t = e == null ? 0 : e.length;
  return t ? wi(e) : [];
}
function $i(e) {
  return Hn(Wn(e, void 0, Ai), e + "");
}
var Ne = Lt(Object.getPrototypeOf, Object), Si = "[object Object]", xi = Function.prototype, Ci = Object.prototype, Rt = xi.toString, Ei = Ci.hasOwnProperty, Ii = Rt.call(Object);
function me(e) {
  if (!M(e) || N(e) != Si)
    return !1;
  var t = Ne(e);
  if (t === null)
    return !0;
  var n = Ei.call(t, "constructor") && t.constructor;
  return typeof n == "function" && n instanceof n && Rt.call(n) == Ii;
}
function ji(e, t, n) {
  var r = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), n = n > i ? i : n, n < 0 && (n += i), i = t > n ? 0 : n - t >>> 0, t >>>= 0;
  for (var o = Array(i); ++r < i; )
    o[r] = e[r + t];
  return o;
}
function Mi() {
  this.__data__ = new F(), this.size = 0;
}
function Fi(e) {
  var t = this.__data__, n = t.delete(e);
  return this.size = t.size, n;
}
function Li(e) {
  return this.__data__.get(e);
}
function Ri(e) {
  return this.__data__.has(e);
}
var Ni = 200;
function Di(e, t) {
  var n = this.__data__;
  if (n instanceof F) {
    var r = n.__data__;
    if (!X || r.length < Ni - 1)
      return r.push([e, t]), this.size = ++n.size, this;
    n = this.__data__ = new L(r);
  }
  return n.set(e, t), this.size = n.size, this;
}
function E(e) {
  var t = this.__data__ = new F(e);
  this.size = t.size;
}
E.prototype.clear = Mi;
E.prototype.delete = Fi;
E.prototype.get = Li;
E.prototype.has = Ri;
E.prototype.set = Di;
function Ki(e, t) {
  return e && W(t, Q(t), e);
}
function Ui(e, t) {
  return e && W(t, je(t), e);
}
var Nt = typeof exports == "object" && exports && !exports.nodeType && exports, tt = Nt && typeof module == "object" && module && !module.nodeType && module, Gi = tt && tt.exports === Nt, nt = Gi ? I.Buffer : void 0, rt = nt ? nt.allocUnsafe : void 0;
function Bi(e, t) {
  if (t)
    return e.slice();
  var n = e.length, r = rt ? rt(n) : new e.constructor(n);
  return e.copy(r), r;
}
function zi(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length, i = 0, o = []; ++n < r; ) {
    var a = e[n];
    t(a, n, e) && (o[i++] = a);
  }
  return o;
}
function Dt() {
  return [];
}
var Hi = Object.prototype, qi = Hi.propertyIsEnumerable, it = Object.getOwnPropertySymbols, De = it ? function(e) {
  return e == null ? [] : (e = Object(e), zi(it(e), function(t) {
    return qi.call(e, t);
  }));
} : Dt;
function Yi(e, t) {
  return W(e, De(e), t);
}
var Ji = Object.getOwnPropertySymbols, Kt = Ji ? function(e) {
  for (var t = []; e; )
    Re(t, De(e)), e = Ne(e);
  return t;
} : Dt;
function Xi(e, t) {
  return W(e, Kt(e), t);
}
function Ut(e, t, n) {
  var r = t(e);
  return S(e) ? r : Re(r, n(e));
}
function ve(e) {
  return Ut(e, Q, De);
}
function Gt(e) {
  return Ut(e, je, Kt);
}
var Te = K(I, "DataView"), Oe = K(I, "Promise"), Pe = K(I, "Set"), ot = "[object Map]", Zi = "[object Object]", at = "[object Promise]", st = "[object Set]", ut = "[object WeakMap]", lt = "[object DataView]", Wi = D(Te), Qi = D(X), Vi = D(Oe), ki = D(Pe), eo = D(ye), $ = N;
(Te && $(new Te(new ArrayBuffer(1))) != lt || X && $(new X()) != ot || Oe && $(Oe.resolve()) != at || Pe && $(new Pe()) != st || ye && $(new ye()) != ut) && ($ = function(e) {
  var t = N(e), n = t == Zi ? e.constructor : void 0, r = n ? D(n) : "";
  if (r)
    switch (r) {
      case Wi:
        return lt;
      case Qi:
        return ot;
      case Vi:
        return at;
      case ki:
        return st;
      case eo:
        return ut;
    }
  return t;
});
var to = Object.prototype, no = to.hasOwnProperty;
function ro(e) {
  var t = e.length, n = new e.constructor(t);
  return t && typeof e[0] == "string" && no.call(e, "index") && (n.index = e.index, n.input = e.input), n;
}
var se = I.Uint8Array;
function Ke(e) {
  var t = new e.constructor(e.byteLength);
  return new se(t).set(new se(e)), t;
}
function io(e, t) {
  var n = t ? Ke(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.byteLength);
}
var oo = /\w*$/;
function ao(e) {
  var t = new e.constructor(e.source, oo.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var ct = w ? w.prototype : void 0, ft = ct ? ct.valueOf : void 0;
function so(e) {
  return ft ? Object(ft.call(e)) : {};
}
function uo(e, t) {
  var n = t ? Ke(e.buffer) : e.buffer;
  return new e.constructor(n, e.byteOffset, e.length);
}
var lo = "[object Boolean]", co = "[object Date]", fo = "[object Map]", po = "[object Number]", go = "[object RegExp]", _o = "[object Set]", bo = "[object String]", ho = "[object Symbol]", yo = "[object ArrayBuffer]", mo = "[object DataView]", vo = "[object Float32Array]", To = "[object Float64Array]", Oo = "[object Int8Array]", Po = "[object Int16Array]", wo = "[object Int32Array]", Ao = "[object Uint8Array]", $o = "[object Uint8ClampedArray]", So = "[object Uint16Array]", xo = "[object Uint32Array]";
function Co(e, t, n) {
  var r = e.constructor;
  switch (t) {
    case yo:
      return Ke(e);
    case lo:
    case co:
      return new r(+e);
    case mo:
      return io(e, n);
    case vo:
    case To:
    case Oo:
    case Po:
    case wo:
    case Ao:
    case $o:
    case So:
    case xo:
      return uo(e, n);
    case fo:
      return new r();
    case po:
    case bo:
      return new r(e);
    case go:
      return ao(e);
    case _o:
      return new r();
    case ho:
      return so(e);
  }
}
function Eo(e) {
  return typeof e.constructor == "function" && !Ce(e) ? Ln(Ne(e)) : {};
}
var Io = "[object Map]";
function jo(e) {
  return M(e) && $(e) == Io;
}
var pt = B && B.isMap, Mo = pt ? Ie(pt) : jo, Fo = "[object Set]";
function Lo(e) {
  return M(e) && $(e) == Fo;
}
var gt = B && B.isSet, Ro = gt ? Ie(gt) : Lo, No = 1, Do = 2, Ko = 4, Bt = "[object Arguments]", Uo = "[object Array]", Go = "[object Boolean]", Bo = "[object Date]", zo = "[object Error]", zt = "[object Function]", Ho = "[object GeneratorFunction]", qo = "[object Map]", Yo = "[object Number]", Ht = "[object Object]", Jo = "[object RegExp]", Xo = "[object Set]", Zo = "[object String]", Wo = "[object Symbol]", Qo = "[object WeakMap]", Vo = "[object ArrayBuffer]", ko = "[object DataView]", ea = "[object Float32Array]", ta = "[object Float64Array]", na = "[object Int8Array]", ra = "[object Int16Array]", ia = "[object Int32Array]", oa = "[object Uint8Array]", aa = "[object Uint8ClampedArray]", sa = "[object Uint16Array]", ua = "[object Uint32Array]", y = {};
y[Bt] = y[Uo] = y[Vo] = y[ko] = y[Go] = y[Bo] = y[ea] = y[ta] = y[na] = y[ra] = y[ia] = y[qo] = y[Yo] = y[Ht] = y[Jo] = y[Xo] = y[Zo] = y[Wo] = y[oa] = y[aa] = y[sa] = y[ua] = !0;
y[zo] = y[zt] = y[Qo] = !1;
function re(e, t, n, r, i, o) {
  var a, s = t & No, u = t & Do, l = t & Ko;
  if (n && (a = i ? n(e, r, i, o) : n(e)), a !== void 0)
    return a;
  if (!z(e))
    return e;
  var d = S(e);
  if (d) {
    if (a = ro(e), !s)
      return Nn(e, a);
  } else {
    var _ = $(e), f = _ == zt || _ == Ho;
    if (ae(e))
      return Bi(e, s);
    if (_ == Ht || _ == Bt || f && !i) {
      if (a = u || f ? {} : Eo(e), !s)
        return u ? Xi(e, Ui(a, e)) : Yi(e, Ki(a, e));
    } else {
      if (!y[_])
        return i ? e : {};
      a = Co(e, _, s);
    }
  }
  o || (o = new E());
  var p = o.get(e);
  if (p)
    return p;
  o.set(e, a), Ro(e) ? e.forEach(function(c) {
    a.add(re(c, t, n, c, e, o));
  }) : Mo(e) && e.forEach(function(c, h) {
    a.set(h, re(c, t, n, h, e, o));
  });
  var m = l ? u ? Gt : ve : u ? je : Q, b = d ? void 0 : m(e);
  return qn(b || e, function(c, h) {
    b && (h = c, c = e[h]), xt(a, h, re(c, t, n, h, e, o));
  }), a;
}
var la = "__lodash_hash_undefined__";
function ca(e) {
  return this.__data__.set(e, la), this;
}
function fa(e) {
  return this.__data__.has(e);
}
function ue(e) {
  var t = -1, n = e == null ? 0 : e.length;
  for (this.__data__ = new L(); ++t < n; )
    this.add(e[t]);
}
ue.prototype.add = ue.prototype.push = ca;
ue.prototype.has = fa;
function pa(e, t) {
  for (var n = -1, r = e == null ? 0 : e.length; ++n < r; )
    if (t(e[n], n, e))
      return !0;
  return !1;
}
function ga(e, t) {
  return e.has(t);
}
var da = 1, _a = 2;
function qt(e, t, n, r, i, o) {
  var a = n & da, s = e.length, u = t.length;
  if (s != u && !(a && u > s))
    return !1;
  var l = o.get(e), d = o.get(t);
  if (l && d)
    return l == t && d == e;
  var _ = -1, f = !0, p = n & _a ? new ue() : void 0;
  for (o.set(e, t), o.set(t, e); ++_ < s; ) {
    var m = e[_], b = t[_];
    if (r)
      var c = a ? r(b, m, _, t, e, o) : r(m, b, _, e, t, o);
    if (c !== void 0) {
      if (c)
        continue;
      f = !1;
      break;
    }
    if (p) {
      if (!pa(t, function(h, T) {
        if (!ga(p, T) && (m === h || i(m, h, n, r, o)))
          return p.push(T);
      })) {
        f = !1;
        break;
      }
    } else if (!(m === b || i(m, b, n, r, o))) {
      f = !1;
      break;
    }
  }
  return o.delete(e), o.delete(t), f;
}
function ba(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r, i) {
    n[++t] = [i, r];
  }), n;
}
function ha(e) {
  var t = -1, n = Array(e.size);
  return e.forEach(function(r) {
    n[++t] = r;
  }), n;
}
var ya = 1, ma = 2, va = "[object Boolean]", Ta = "[object Date]", Oa = "[object Error]", Pa = "[object Map]", wa = "[object Number]", Aa = "[object RegExp]", $a = "[object Set]", Sa = "[object String]", xa = "[object Symbol]", Ca = "[object ArrayBuffer]", Ea = "[object DataView]", dt = w ? w.prototype : void 0, he = dt ? dt.valueOf : void 0;
function Ia(e, t, n, r, i, o, a) {
  switch (n) {
    case Ea:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case Ca:
      return !(e.byteLength != t.byteLength || !o(new se(e), new se(t)));
    case va:
    case Ta:
    case wa:
      return Se(+e, +t);
    case Oa:
      return e.name == t.name && e.message == t.message;
    case Aa:
    case Sa:
      return e == t + "";
    case Pa:
      var s = ba;
    case $a:
      var u = r & ya;
      if (s || (s = ha), e.size != t.size && !u)
        return !1;
      var l = a.get(e);
      if (l)
        return l == t;
      r |= ma, a.set(e, t);
      var d = qt(s(e), s(t), r, i, o, a);
      return a.delete(e), d;
    case xa:
      if (he)
        return he.call(e) == he.call(t);
  }
  return !1;
}
var ja = 1, Ma = Object.prototype, Fa = Ma.hasOwnProperty;
function La(e, t, n, r, i, o) {
  var a = n & ja, s = ve(e), u = s.length, l = ve(t), d = l.length;
  if (u != d && !a)
    return !1;
  for (var _ = u; _--; ) {
    var f = s[_];
    if (!(a ? f in t : Fa.call(t, f)))
      return !1;
  }
  var p = o.get(e), m = o.get(t);
  if (p && m)
    return p == t && m == e;
  var b = !0;
  o.set(e, t), o.set(t, e);
  for (var c = a; ++_ < u; ) {
    f = s[_];
    var h = e[f], T = t[f];
    if (r)
      var P = a ? r(T, h, f, t, e, o) : r(h, T, f, e, t, o);
    if (!(P === void 0 ? h === T || i(h, T, n, r, o) : P)) {
      b = !1;
      break;
    }
    c || (c = f == "constructor");
  }
  if (b && !c) {
    var x = e.constructor, A = t.constructor;
    x != A && "constructor" in e && "constructor" in t && !(typeof x == "function" && x instanceof x && typeof A == "function" && A instanceof A) && (b = !1);
  }
  return o.delete(e), o.delete(t), b;
}
var Ra = 1, _t = "[object Arguments]", bt = "[object Array]", te = "[object Object]", Na = Object.prototype, ht = Na.hasOwnProperty;
function Da(e, t, n, r, i, o) {
  var a = S(e), s = S(t), u = a ? bt : $(e), l = s ? bt : $(t);
  u = u == _t ? te : u, l = l == _t ? te : l;
  var d = u == te, _ = l == te, f = u == l;
  if (f && ae(e)) {
    if (!ae(t))
      return !1;
    a = !0, d = !1;
  }
  if (f && !d)
    return o || (o = new E()), a || Mt(e) ? qt(e, t, n, r, i, o) : Ia(e, t, u, n, r, i, o);
  if (!(n & Ra)) {
    var p = d && ht.call(e, "__wrapped__"), m = _ && ht.call(t, "__wrapped__");
    if (p || m) {
      var b = p ? e.value() : e, c = m ? t.value() : t;
      return o || (o = new E()), i(b, c, n, r, o);
    }
  }
  return f ? (o || (o = new E()), La(e, t, n, r, i, o)) : !1;
}
function Ue(e, t, n, r, i) {
  return e === t ? !0 : e == null || t == null || !M(e) && !M(t) ? e !== e && t !== t : Da(e, t, n, r, Ue, i);
}
var Ka = 1, Ua = 2;
function Ga(e, t, n, r) {
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
      var d = new E(), _;
      if (!(_ === void 0 ? Ue(l, u, Ka | Ua, r, d) : _))
        return !1;
    }
  }
  return !0;
}
function Yt(e) {
  return e === e && !z(e);
}
function Ba(e) {
  for (var t = Q(e), n = t.length; n--; ) {
    var r = t[n], i = e[r];
    t[n] = [r, i, Yt(i)];
  }
  return t;
}
function Jt(e, t) {
  return function(n) {
    return n == null ? !1 : n[e] === t && (t !== void 0 || e in Object(n));
  };
}
function za(e) {
  var t = Ba(e);
  return t.length == 1 && t[0][2] ? Jt(t[0][0], t[0][1]) : function(n) {
    return n === e || Ga(n, e, t);
  };
}
function Ha(e, t) {
  return e != null && t in Object(e);
}
function qa(e, t, n) {
  t = pe(t, e);
  for (var r = -1, i = t.length, o = !1; ++r < i; ) {
    var a = V(t[r]);
    if (!(o = e != null && n(e, a)))
      break;
    e = e[a];
  }
  return o || ++r != i ? o : (i = e == null ? 0 : e.length, !!i && xe(i) && St(a, i) && (S(e) || Ee(e)));
}
function Ya(e, t) {
  return e != null && qa(e, t, Ha);
}
var Ja = 1, Xa = 2;
function Za(e, t) {
  return Me(e) && Yt(t) ? Jt(V(e), t) : function(n) {
    var r = Oi(n, e);
    return r === void 0 && r === t ? Ya(n, e) : Ue(t, r, Ja | Xa);
  };
}
function Wa(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function Qa(e) {
  return function(t) {
    return Le(t, e);
  };
}
function Va(e) {
  return Me(e) ? Wa(V(e)) : Qa(e);
}
function ka(e) {
  return typeof e == "function" ? e : e == null ? At : typeof e == "object" ? S(e) ? Za(e[0], e[1]) : za(e) : Va(e);
}
function es(e) {
  return function(t, n, r) {
    for (var i = -1, o = Object(t), a = r(t), s = a.length; s--; ) {
      var u = a[++i];
      if (n(o[u], u, o) === !1)
        break;
    }
    return t;
  };
}
var ts = es();
function ns(e, t) {
  return e && ts(e, t, Q);
}
function rs(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function is(e, t) {
  return t.length < 2 ? e : Le(e, ji(t, 0, -1));
}
function os(e, t) {
  var n = {};
  return t = ka(t), ns(e, function(r, i, o) {
    $e(n, t(r, i, o), r);
  }), n;
}
function as(e, t) {
  return t = pe(t, e), e = is(e, t), e == null || delete e[V(rs(t))];
}
function ss(e) {
  return me(e) ? void 0 : e;
}
var us = 1, ls = 2, cs = 4, Xt = $i(function(e, t) {
  var n = {};
  if (e == null)
    return n;
  var r = !1;
  t = Pt(t, function(o) {
    return o = pe(o, e), r || (r = o.length > 1), o;
  }), W(e, Gt(e), n), r && (n = re(n, us | ls | cs, ss));
  for (var i = t.length; i--; )
    as(n, t[i]);
  return n;
});
async function fs() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function ps(e) {
  return await fs(), e().then((t) => t.default);
}
const Zt = [
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
], gs = Zt.concat(["attached_events"]);
function ds(e, t = {}, n = !1) {
  return os(Xt(e, n ? [] : Zt), (r, i) => t[i] || sn(i));
}
function _s(e, t) {
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
    }).filter(Boolean), ...s.map((u) => u)])).reduce((u, l) => {
      const d = l.split("_"), _ = (...p) => {
        const m = p.map((c) => p && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        let b;
        try {
          b = JSON.parse(JSON.stringify(m));
        } catch {
          let c = function(h) {
            try {
              return JSON.stringify(h), h;
            } catch {
              return me(h) ? Object.fromEntries(Object.entries(h).map(([T, P]) => {
                try {
                  return JSON.stringify(P), [T, P];
                } catch {
                  return me(P) ? [T, Object.fromEntries(Object.entries(P).filter(([x, A]) => {
                    try {
                      return JSON.stringify(A), !0;
                    } catch {
                      return !1;
                    }
                  }))] : null;
                }
              }).filter(Boolean)) : {};
            }
          };
          b = m.map((h) => c(h));
        }
        return n.dispatch(l.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: b,
          component: {
            ...a,
            ...Xt(o, gs)
          }
        });
      };
      if (d.length > 1) {
        let p = {
          ...a.props[d[0]] || (i == null ? void 0 : i[d[0]]) || {}
        };
        u[d[0]] = p;
        for (let b = 1; b < d.length - 1; b++) {
          const c = {
            ...a.props[d[b]] || (i == null ? void 0 : i[d[b]]) || {}
          };
          p[d[b]] = c, p = c;
        }
        const m = d[d.length - 1];
        return p[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = _, u;
      }
      const f = d[0];
      return u[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = _, u;
    }, {}),
    __render_eventProps: {
      props: e,
      eventsMapping: t
    }
  };
}
function ie() {
}
function bs(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function hs(e, ...t) {
  if (e == null) {
    for (const r of t)
      r(void 0);
    return ie;
  }
  const n = e.subscribe(...t);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function Wt(e) {
  let t;
  return hs(e, (n) => t = n)(), t;
}
const U = [];
function j(e, t = ie) {
  let n;
  const r = /* @__PURE__ */ new Set();
  function i(s) {
    if (bs(e, s) && (e = s, n)) {
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
  function a(s, u = ie) {
    const l = [s, u];
    return r.add(l), r.size === 1 && (n = t(i, o) || ie), s(e), () => {
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
  getContext: ys,
  setContext: iu
} = window.__gradio__svelte__internal, ms = "$$ms-gr-loading-status-key";
function vs() {
  const e = window.ms_globals.loadingKey++, t = ys(ms);
  return (n) => {
    if (!t || !n)
      return;
    const {
      loadingStatusMap: r,
      options: i
    } = t, {
      generating: o,
      error: a
    } = Wt(i);
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
  getContext: ge,
  setContext: H
} = window.__gradio__svelte__internal, Ts = "$$ms-gr-slots-key";
function Os() {
  const e = j({});
  return H(Ts, e);
}
const Qt = "$$ms-gr-slot-params-mapping-fn-key";
function Ps() {
  return ge(Qt);
}
function ws(e) {
  return H(Qt, j(e));
}
const As = "$$ms-gr-slot-params-key";
function $s() {
  const e = H(As, j({}));
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
const Vt = "$$ms-gr-sub-index-context-key";
function Ss() {
  return ge(Vt) || null;
}
function yt(e) {
  return H(Vt, e);
}
function xs(e, t, n) {
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const r = en(), i = Ps();
  ws().set(void 0);
  const a = Es({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  }), s = Ss();
  typeof s == "number" && yt(void 0);
  const u = vs();
  typeof e._internal.subIndex == "number" && yt(e._internal.subIndex), r && r.subscribe((f) => {
    a.slotKey.set(f);
  }), Cs();
  const l = e.as_item, d = (f, p) => f ? {
    ...ds({
      ...f
    }, t),
    __render_slotParamsMappingFn: i ? Wt(i) : void 0,
    __render_as_item: p,
    __render_restPropsMapping: t
  } : void 0, _ = j({
    ...e,
    _internal: {
      ...e._internal,
      index: s ?? e._internal.index
    },
    restProps: d(e.restProps, l),
    originalRestProps: e.restProps
  });
  return i && i.subscribe((f) => {
    _.update((p) => ({
      ...p,
      restProps: {
        ...p.restProps,
        __slotParamsMappingFn: f
      }
    }));
  }), [_, (f) => {
    var p;
    u((p = f.restProps) == null ? void 0 : p.loading_status), _.set({
      ...f,
      _internal: {
        ...f._internal,
        index: s ?? f._internal.index
      },
      restProps: d(f.restProps, f.as_item),
      originalRestProps: f.restProps
    });
  }];
}
const kt = "$$ms-gr-slot-key";
function Cs() {
  H(kt, j(void 0));
}
function en() {
  return ge(kt);
}
const tn = "$$ms-gr-component-slot-context-key";
function Es({
  slot: e,
  index: t,
  subIndex: n
}) {
  return H(tn, {
    slotKey: j(e),
    slotIndex: j(t),
    subSlotIndex: j(n)
  });
}
function ou() {
  return ge(tn);
}
function Is(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var nn = {
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
})(nn);
var js = nn.exports;
const Ms = /* @__PURE__ */ Is(js), {
  SvelteComponent: Fs,
  assign: we,
  check_outros: Ls,
  claim_component: Rs,
  component_subscribe: ne,
  compute_rest_props: mt,
  create_component: Ns,
  create_slot: Ds,
  destroy_component: Ks,
  detach: rn,
  empty: le,
  exclude_internal_props: Us,
  flush: C,
  get_all_dirty_from_scope: Gs,
  get_slot_changes: Bs,
  get_spread_object: zs,
  get_spread_update: Hs,
  group_outros: qs,
  handle_promise: Ys,
  init: Js,
  insert_hydration: on,
  mount_component: Xs,
  noop: O,
  safe_not_equal: Zs,
  transition_in: G,
  transition_out: Z,
  update_await_block_branch: Ws,
  update_slot_base: Qs
} = window.__gradio__svelte__internal;
function vt(e) {
  let t, n, r = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: tu,
    then: ks,
    catch: Vs,
    value: 25,
    blocks: [, , ,]
  };
  return Ys(
    /*AwaitedSuggestionItem*/
    e[3],
    r
  ), {
    c() {
      t = le(), r.block.c();
    },
    l(i) {
      t = le(), r.block.l(i);
    },
    m(i, o) {
      on(i, t, o), r.block.m(i, r.anchor = o), r.mount = () => t.parentNode, r.anchor = t, n = !0;
    },
    p(i, o) {
      e = i, Ws(r, e, o);
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
      i && rn(t), r.block.d(i), r.token = null, r = null;
    }
  };
}
function Vs(e) {
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
function ks(e) {
  let t, n;
  const r = [
    /*itemProps*/
    e[1].props,
    {
      slots: (
        /*itemProps*/
        e[1].slots
      )
    },
    {
      itemIndex: (
        /*$mergedProps*/
        e[0]._internal.index || 0
      )
    },
    {
      itemSlotKey: (
        /*$slotKey*/
        e[2]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [eu]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let o = 0; o < r.length; o += 1)
    i = we(i, r[o]);
  return t = new /*SuggestionItem*/
  e[25]({
    props: i
  }), {
    c() {
      Ns(t.$$.fragment);
    },
    l(o) {
      Rs(t.$$.fragment, o);
    },
    m(o, a) {
      Xs(t, o, a), n = !0;
    },
    p(o, a) {
      const s = a & /*itemProps, $mergedProps, $slotKey*/
      7 ? Hs(r, [a & /*itemProps*/
      2 && zs(
        /*itemProps*/
        o[1].props
      ), a & /*itemProps*/
      2 && {
        slots: (
          /*itemProps*/
          o[1].slots
        )
      }, a & /*$mergedProps*/
      1 && {
        itemIndex: (
          /*$mergedProps*/
          o[0]._internal.index || 0
        )
      }, a & /*$slotKey*/
      4 && {
        itemSlotKey: (
          /*$slotKey*/
          o[2]
        )
      }]) : {};
      a & /*$$scope*/
      2097152 && (s.$$scope = {
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
      Ks(t, o);
    }
  };
}
function eu(e) {
  let t;
  const n = (
    /*#slots*/
    e[20].default
  ), r = Ds(
    n,
    e,
    /*$$scope*/
    e[21],
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
      2097152) && Qs(
        r,
        n,
        i,
        /*$$scope*/
        i[21],
        t ? Bs(
          n,
          /*$$scope*/
          i[21],
          o,
          null
        ) : Gs(
          /*$$scope*/
          i[21]
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
function tu(e) {
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
function nu(e) {
  let t, n, r = (
    /*$mergedProps*/
    e[0].visible && vt(e)
  );
  return {
    c() {
      r && r.c(), t = le();
    },
    l(i) {
      r && r.l(i), t = le();
    },
    m(i, o) {
      r && r.m(i, o), on(i, t, o), n = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[0].visible ? r ? (r.p(i, o), o & /*$mergedProps*/
      1 && G(r, 1)) : (r = vt(i), r.c(), G(r, 1), r.m(t.parentNode, t)) : r && (qs(), Z(r, 1, 1, () => {
        r = null;
      }), Ls());
    },
    i(i) {
      n || (G(r), n = !0);
    },
    o(i) {
      Z(r), n = !1;
    },
    d(i) {
      i && rn(t), r && r.d(i);
    }
  };
}
function ru(e, t, n) {
  let r;
  const i = ["gradio", "props", "_internal", "as_item", "label", "value", "visible", "elem_id", "elem_classes", "elem_style"];
  let o = mt(t, i), a, s, u, l, {
    $$slots: d = {},
    $$scope: _
  } = t;
  const f = ps(() => import("./suggestion.item-bn28h06-.js"));
  let {
    gradio: p
  } = t, {
    props: m = {}
  } = t;
  const b = j(m);
  ne(e, b, (g) => n(19, u = g));
  let {
    _internal: c = {}
  } = t, {
    as_item: h
  } = t, {
    label: T
  } = t, {
    value: P
  } = t, {
    visible: x = !0
  } = t, {
    elem_id: A = ""
  } = t, {
    elem_classes: k = []
  } = t, {
    elem_style: ee = {}
  } = t;
  const Ge = en();
  ne(e, Ge, (g) => n(2, l = g));
  const [Be, an] = xs({
    gradio: p,
    props: u,
    _internal: c,
    visible: x,
    elem_id: A,
    elem_classes: k,
    elem_style: ee,
    as_item: h,
    label: T,
    value: P,
    restProps: o
  });
  ne(e, Be, (g) => n(0, s = g));
  const de = $s(), ze = Os();
  return ne(e, ze, (g) => n(18, a = g)), e.$$set = (g) => {
    t = we(we({}, t), Us(g)), n(24, o = mt(t, i)), "gradio" in g && n(8, p = g.gradio), "props" in g && n(9, m = g.props), "_internal" in g && n(10, c = g._internal), "as_item" in g && n(11, h = g.as_item), "label" in g && n(12, T = g.label), "value" in g && n(13, P = g.value), "visible" in g && n(14, x = g.visible), "elem_id" in g && n(15, A = g.elem_id), "elem_classes" in g && n(16, k = g.elem_classes), "elem_style" in g && n(17, ee = g.elem_style), "$$scope" in g && n(21, _ = g.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    512 && b.update((g) => ({
      ...g,
      ...m
    })), an({
      gradio: p,
      props: u,
      _internal: c,
      visible: x,
      elem_id: A,
      elem_classes: k,
      elem_style: ee,
      as_item: h,
      label: T,
      value: P,
      restProps: o
    }), e.$$.dirty & /*$mergedProps, $slots*/
    262145 && n(1, r = {
      props: {
        style: s.elem_style,
        className: Ms(s.elem_classes, "ms-gr-antd-suggestion-item"),
        id: s.elem_id,
        label: s.label,
        value: s.value,
        ...s.restProps,
        ...s.props,
        ..._s(s)
      },
      slots: {
        ...a,
        extra: {
          el: a.extra,
          clone: !0,
          callback: de
        },
        icon: {
          el: a.icon,
          clone: !0,
          callback: de
        },
        label: {
          el: a.label,
          clone: !0,
          callback: de
        }
      }
    });
  }, [s, r, l, f, b, Ge, Be, ze, p, m, c, h, T, P, x, A, k, ee, a, u, d, _];
}
class au extends Fs {
  constructor(t) {
    super(), Js(this, t, ru, nu, Zs, {
      gradio: 8,
      props: 9,
      _internal: 10,
      as_item: 11,
      label: 12,
      value: 13,
      visible: 14,
      elem_id: 15,
      elem_classes: 16,
      elem_style: 17
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), C();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(t) {
    this.$$set({
      props: t
    }), C();
  }
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), C();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), C();
  }
  get label() {
    return this.$$.ctx[12];
  }
  set label(t) {
    this.$$set({
      label: t
    }), C();
  }
  get value() {
    return this.$$.ctx[13];
  }
  set value(t) {
    this.$$set({
      value: t
    }), C();
  }
  get visible() {
    return this.$$.ctx[14];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), C();
  }
  get elem_id() {
    return this.$$.ctx[15];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), C();
  }
  get elem_classes() {
    return this.$$.ctx[16];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), C();
  }
  get elem_style() {
    return this.$$.ctx[17];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), C();
  }
}
export {
  au as I,
  ou as g,
  j as w
};
