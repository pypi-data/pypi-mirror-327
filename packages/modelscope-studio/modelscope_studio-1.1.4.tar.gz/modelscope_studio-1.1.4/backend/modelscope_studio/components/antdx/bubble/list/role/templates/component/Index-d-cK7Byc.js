function Mt(e) {
  return e.replace(/(^|_)(\w)/g, (t, r, n, i) => i === 0 ? n.toLowerCase() : n.toUpperCase());
}
var ot = typeof global == "object" && global && global.Object === Object && global, Rt = typeof self == "object" && self && self.Object === Object && self, S = ot || Rt || Function("return this")(), T = S.Symbol, st = Object.prototype, Nt = st.hasOwnProperty, Dt = st.toString, G = T ? T.toStringTag : void 0;
function Ut(e) {
  var t = Nt.call(e, G), r = e[G];
  try {
    e[G] = void 0;
    var n = !0;
  } catch {
  }
  var i = Dt.call(e);
  return n && (t ? e[G] = r : delete e[G]), i;
}
var Gt = Object.prototype, Bt = Gt.toString;
function zt(e) {
  return Bt.call(e);
}
var Kt = "[object Null]", Ht = "[object Undefined]", Ce = T ? T.toStringTag : void 0;
function L(e) {
  return e == null ? e === void 0 ? Ht : Kt : Ce && Ce in Object(e) ? Ut(e) : zt(e);
}
function P(e) {
  return e != null && typeof e == "object";
}
var Yt = "[object Symbol]";
function ge(e) {
  return typeof e == "symbol" || P(e) && L(e) == Yt;
}
function ut(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, i = Array(n); ++r < n; )
    i[r] = t(e[r], r, e);
  return i;
}
var A = Array.isArray, Jt = 1 / 0, Ie = T ? T.prototype : void 0, xe = Ie ? Ie.toString : void 0;
function lt(e) {
  if (typeof e == "string")
    return e;
  if (A(e))
    return ut(e, lt) + "";
  if (ge(e))
    return xe ? xe.call(e) : "";
  var t = e + "";
  return t == "0" && 1 / e == -Jt ? "-0" : t;
}
function D(e) {
  var t = typeof e;
  return e != null && (t == "object" || t == "function");
}
function ft(e) {
  return e;
}
var Xt = "[object AsyncFunction]", qt = "[object Function]", Zt = "[object GeneratorFunction]", Wt = "[object Proxy]";
function ct(e) {
  if (!D(e))
    return !1;
  var t = L(e);
  return t == qt || t == Zt || t == Xt || t == Wt;
}
var re = S["__core-js_shared__"], Le = function() {
  var e = /[^.]+$/.exec(re && re.keys && re.keys.IE_PROTO || "");
  return e ? "Symbol(src)_1." + e : "";
}();
function Qt(e) {
  return !!Le && Le in e;
}
var Vt = Function.prototype, kt = Vt.toString;
function F(e) {
  if (e != null) {
    try {
      return kt.call(e);
    } catch {
    }
    try {
      return e + "";
    } catch {
    }
  }
  return "";
}
var er = /[\\^$.*+?()[\]{}|]/g, tr = /^\[object .+?Constructor\]$/, rr = Function.prototype, nr = Object.prototype, ir = rr.toString, ar = nr.hasOwnProperty, or = RegExp("^" + ir.call(ar).replace(er, "\\$&").replace(/hasOwnProperty|(function).*?(?=\\\()| for .+?(?=\\\])/g, "$1.*?") + "$");
function sr(e) {
  if (!D(e) || Qt(e))
    return !1;
  var t = ct(e) ? or : tr;
  return t.test(F(e));
}
function ur(e, t) {
  return e == null ? void 0 : e[t];
}
function M(e, t) {
  var r = ur(e, t);
  return sr(r) ? r : void 0;
}
var ae = M(S, "WeakMap"), Fe = Object.create, lr = /* @__PURE__ */ function() {
  function e() {
  }
  return function(t) {
    if (!D(t))
      return {};
    if (Fe)
      return Fe(t);
    e.prototype = t;
    var r = new e();
    return e.prototype = void 0, r;
  };
}();
function fr(e, t, r) {
  switch (r.length) {
    case 0:
      return e.call(t);
    case 1:
      return e.call(t, r[0]);
    case 2:
      return e.call(t, r[0], r[1]);
    case 3:
      return e.call(t, r[0], r[1], r[2]);
  }
  return e.apply(t, r);
}
function cr(e, t) {
  var r = -1, n = e.length;
  for (t || (t = Array(n)); ++r < n; )
    t[r] = e[r];
  return t;
}
var gr = 800, pr = 16, dr = Date.now;
function _r(e) {
  var t = 0, r = 0;
  return function() {
    var n = dr(), i = pr - (n - r);
    if (r = n, i > 0) {
      if (++t >= gr)
        return arguments[0];
    } else
      t = 0;
    return e.apply(void 0, arguments);
  };
}
function hr(e) {
  return function() {
    return e;
  };
}
var Z = function() {
  try {
    var e = M(Object, "defineProperty");
    return e({}, "", {}), e;
  } catch {
  }
}(), br = Z ? function(e, t) {
  return Z(e, "toString", {
    configurable: !0,
    enumerable: !1,
    value: hr(t),
    writable: !0
  });
} : ft, yr = _r(br);
function mr(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n && t(e[r], r, e) !== !1; )
    ;
  return e;
}
var vr = 9007199254740991, Tr = /^(?:0|[1-9]\d*)$/;
function gt(e, t) {
  var r = typeof e;
  return t = t ?? vr, !!t && (r == "number" || r != "symbol" && Tr.test(e)) && e > -1 && e % 1 == 0 && e < t;
}
function pe(e, t, r) {
  t == "__proto__" && Z ? Z(e, t, {
    configurable: !0,
    enumerable: !0,
    value: r,
    writable: !0
  }) : e[t] = r;
}
function de(e, t) {
  return e === t || e !== e && t !== t;
}
var Or = Object.prototype, Ar = Or.hasOwnProperty;
function pt(e, t, r) {
  var n = e[t];
  (!(Ar.call(e, t) && de(n, r)) || r === void 0 && !(t in e)) && pe(e, t, r);
}
function H(e, t, r, n) {
  var i = !r;
  r || (r = {});
  for (var a = -1, o = t.length; ++a < o; ) {
    var s = t[a], u = void 0;
    u === void 0 && (u = e[s]), i ? pe(r, s, u) : pt(r, s, u);
  }
  return r;
}
var Me = Math.max;
function wr(e, t, r) {
  return t = Me(t === void 0 ? e.length - 1 : t, 0), function() {
    for (var n = arguments, i = -1, a = Me(n.length - t, 0), o = Array(a); ++i < a; )
      o[i] = n[t + i];
    i = -1;
    for (var s = Array(t + 1); ++i < t; )
      s[i] = n[i];
    return s[t] = r(o), fr(e, this, s);
  };
}
var $r = 9007199254740991;
function _e(e) {
  return typeof e == "number" && e > -1 && e % 1 == 0 && e <= $r;
}
function dt(e) {
  return e != null && _e(e.length) && !ct(e);
}
var Sr = Object.prototype;
function he(e) {
  var t = e && e.constructor, r = typeof t == "function" && t.prototype || Sr;
  return e === r;
}
function Pr(e, t) {
  for (var r = -1, n = Array(e); ++r < e; )
    n[r] = t(r);
  return n;
}
var Er = "[object Arguments]";
function Re(e) {
  return P(e) && L(e) == Er;
}
var _t = Object.prototype, jr = _t.hasOwnProperty, Cr = _t.propertyIsEnumerable, be = Re(/* @__PURE__ */ function() {
  return arguments;
}()) ? Re : function(e) {
  return P(e) && jr.call(e, "callee") && !Cr.call(e, "callee");
};
function Ir() {
  return !1;
}
var ht = typeof exports == "object" && exports && !exports.nodeType && exports, Ne = ht && typeof module == "object" && module && !module.nodeType && module, xr = Ne && Ne.exports === ht, De = xr ? S.Buffer : void 0, Lr = De ? De.isBuffer : void 0, W = Lr || Ir, Fr = "[object Arguments]", Mr = "[object Array]", Rr = "[object Boolean]", Nr = "[object Date]", Dr = "[object Error]", Ur = "[object Function]", Gr = "[object Map]", Br = "[object Number]", zr = "[object Object]", Kr = "[object RegExp]", Hr = "[object Set]", Yr = "[object String]", Jr = "[object WeakMap]", Xr = "[object ArrayBuffer]", qr = "[object DataView]", Zr = "[object Float32Array]", Wr = "[object Float64Array]", Qr = "[object Int8Array]", Vr = "[object Int16Array]", kr = "[object Int32Array]", en = "[object Uint8Array]", tn = "[object Uint8ClampedArray]", rn = "[object Uint16Array]", nn = "[object Uint32Array]", h = {};
h[Zr] = h[Wr] = h[Qr] = h[Vr] = h[kr] = h[en] = h[tn] = h[rn] = h[nn] = !0;
h[Fr] = h[Mr] = h[Xr] = h[Rr] = h[qr] = h[Nr] = h[Dr] = h[Ur] = h[Gr] = h[Br] = h[zr] = h[Kr] = h[Hr] = h[Yr] = h[Jr] = !1;
function an(e) {
  return P(e) && _e(e.length) && !!h[L(e)];
}
function ye(e) {
  return function(t) {
    return e(t);
  };
}
var bt = typeof exports == "object" && exports && !exports.nodeType && exports, B = bt && typeof module == "object" && module && !module.nodeType && module, on = B && B.exports === bt, ne = on && ot.process, N = function() {
  try {
    var e = B && B.require && B.require("util").types;
    return e || ne && ne.binding && ne.binding("util");
  } catch {
  }
}(), Ue = N && N.isTypedArray, yt = Ue ? ye(Ue) : an, sn = Object.prototype, un = sn.hasOwnProperty;
function mt(e, t) {
  var r = A(e), n = !r && be(e), i = !r && !n && W(e), a = !r && !n && !i && yt(e), o = r || n || i || a, s = o ? Pr(e.length, String) : [], u = s.length;
  for (var c in e)
    (t || un.call(e, c)) && !(o && // Safari 9 has enumerable `arguments.length` in strict mode.
    (c == "length" || // Node.js 0.10 has enumerable non-index properties on buffers.
    i && (c == "offset" || c == "parent") || // PhantomJS 2 has enumerable non-index properties on typed arrays.
    a && (c == "buffer" || c == "byteLength" || c == "byteOffset") || // Skip index properties.
    gt(c, u))) && s.push(c);
  return s;
}
function vt(e, t) {
  return function(r) {
    return e(t(r));
  };
}
var ln = vt(Object.keys, Object), fn = Object.prototype, cn = fn.hasOwnProperty;
function gn(e) {
  if (!he(e))
    return ln(e);
  var t = [];
  for (var r in Object(e))
    cn.call(e, r) && r != "constructor" && t.push(r);
  return t;
}
function Y(e) {
  return dt(e) ? mt(e) : gn(e);
}
function pn(e) {
  var t = [];
  if (e != null)
    for (var r in Object(e))
      t.push(r);
  return t;
}
var dn = Object.prototype, _n = dn.hasOwnProperty;
function hn(e) {
  if (!D(e))
    return pn(e);
  var t = he(e), r = [];
  for (var n in e)
    n == "constructor" && (t || !_n.call(e, n)) || r.push(n);
  return r;
}
function me(e) {
  return dt(e) ? mt(e, !0) : hn(e);
}
var bn = /\.|\[(?:[^[\]]*|(["'])(?:(?!\1)[^\\]|\\.)*?\1)\]/, yn = /^\w*$/;
function ve(e, t) {
  if (A(e))
    return !1;
  var r = typeof e;
  return r == "number" || r == "symbol" || r == "boolean" || e == null || ge(e) ? !0 : yn.test(e) || !bn.test(e) || t != null && e in Object(t);
}
var z = M(Object, "create");
function mn() {
  this.__data__ = z ? z(null) : {}, this.size = 0;
}
function vn(e) {
  var t = this.has(e) && delete this.__data__[e];
  return this.size -= t ? 1 : 0, t;
}
var Tn = "__lodash_hash_undefined__", On = Object.prototype, An = On.hasOwnProperty;
function wn(e) {
  var t = this.__data__;
  if (z) {
    var r = t[e];
    return r === Tn ? void 0 : r;
  }
  return An.call(t, e) ? t[e] : void 0;
}
var $n = Object.prototype, Sn = $n.hasOwnProperty;
function Pn(e) {
  var t = this.__data__;
  return z ? t[e] !== void 0 : Sn.call(t, e);
}
var En = "__lodash_hash_undefined__";
function jn(e, t) {
  var r = this.__data__;
  return this.size += this.has(e) ? 0 : 1, r[e] = z && t === void 0 ? En : t, this;
}
function x(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
x.prototype.clear = mn;
x.prototype.delete = vn;
x.prototype.get = wn;
x.prototype.has = Pn;
x.prototype.set = jn;
function Cn() {
  this.__data__ = [], this.size = 0;
}
function k(e, t) {
  for (var r = e.length; r--; )
    if (de(e[r][0], t))
      return r;
  return -1;
}
var In = Array.prototype, xn = In.splice;
function Ln(e) {
  var t = this.__data__, r = k(t, e);
  if (r < 0)
    return !1;
  var n = t.length - 1;
  return r == n ? t.pop() : xn.call(t, r, 1), --this.size, !0;
}
function Fn(e) {
  var t = this.__data__, r = k(t, e);
  return r < 0 ? void 0 : t[r][1];
}
function Mn(e) {
  return k(this.__data__, e) > -1;
}
function Rn(e, t) {
  var r = this.__data__, n = k(r, e);
  return n < 0 ? (++this.size, r.push([e, t])) : r[n][1] = t, this;
}
function E(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
E.prototype.clear = Cn;
E.prototype.delete = Ln;
E.prototype.get = Fn;
E.prototype.has = Mn;
E.prototype.set = Rn;
var K = M(S, "Map");
function Nn() {
  this.size = 0, this.__data__ = {
    hash: new x(),
    map: new (K || E)(),
    string: new x()
  };
}
function Dn(e) {
  var t = typeof e;
  return t == "string" || t == "number" || t == "symbol" || t == "boolean" ? e !== "__proto__" : e === null;
}
function ee(e, t) {
  var r = e.__data__;
  return Dn(t) ? r[typeof t == "string" ? "string" : "hash"] : r.map;
}
function Un(e) {
  var t = ee(this, e).delete(e);
  return this.size -= t ? 1 : 0, t;
}
function Gn(e) {
  return ee(this, e).get(e);
}
function Bn(e) {
  return ee(this, e).has(e);
}
function zn(e, t) {
  var r = ee(this, e), n = r.size;
  return r.set(e, t), this.size += r.size == n ? 0 : 1, this;
}
function j(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.clear(); ++t < r; ) {
    var n = e[t];
    this.set(n[0], n[1]);
  }
}
j.prototype.clear = Nn;
j.prototype.delete = Un;
j.prototype.get = Gn;
j.prototype.has = Bn;
j.prototype.set = zn;
var Kn = "Expected a function";
function Te(e, t) {
  if (typeof e != "function" || t != null && typeof t != "function")
    throw new TypeError(Kn);
  var r = function() {
    var n = arguments, i = t ? t.apply(this, n) : n[0], a = r.cache;
    if (a.has(i))
      return a.get(i);
    var o = e.apply(this, n);
    return r.cache = a.set(i, o) || a, o;
  };
  return r.cache = new (Te.Cache || j)(), r;
}
Te.Cache = j;
var Hn = 500;
function Yn(e) {
  var t = Te(e, function(n) {
    return r.size === Hn && r.clear(), n;
  }), r = t.cache;
  return t;
}
var Jn = /[^.[\]]+|\[(?:(-?\d+(?:\.\d+)?)|(["'])((?:(?!\2)[^\\]|\\.)*?)\2)\]|(?=(?:\.|\[\])(?:\.|\[\]|$))/g, Xn = /\\(\\)?/g, qn = Yn(function(e) {
  var t = [];
  return e.charCodeAt(0) === 46 && t.push(""), e.replace(Jn, function(r, n, i, a) {
    t.push(i ? a.replace(Xn, "$1") : n || r);
  }), t;
});
function Zn(e) {
  return e == null ? "" : lt(e);
}
function te(e, t) {
  return A(e) ? e : ve(e, t) ? [e] : qn(Zn(e));
}
var Wn = 1 / 0;
function J(e) {
  if (typeof e == "string" || ge(e))
    return e;
  var t = e + "";
  return t == "0" && 1 / e == -Wn ? "-0" : t;
}
function Oe(e, t) {
  t = te(t, e);
  for (var r = 0, n = t.length; e != null && r < n; )
    e = e[J(t[r++])];
  return r && r == n ? e : void 0;
}
function Qn(e, t, r) {
  var n = e == null ? void 0 : Oe(e, t);
  return n === void 0 ? r : n;
}
function Ae(e, t) {
  for (var r = -1, n = t.length, i = e.length; ++r < n; )
    e[i + r] = t[r];
  return e;
}
var Ge = T ? T.isConcatSpreadable : void 0;
function Vn(e) {
  return A(e) || be(e) || !!(Ge && e && e[Ge]);
}
function kn(e, t, r, n, i) {
  var a = -1, o = e.length;
  for (r || (r = Vn), i || (i = []); ++a < o; ) {
    var s = e[a];
    r(s) ? Ae(i, s) : i[i.length] = s;
  }
  return i;
}
function ei(e) {
  var t = e == null ? 0 : e.length;
  return t ? kn(e) : [];
}
function ti(e) {
  return yr(wr(e, void 0, ei), e + "");
}
var we = vt(Object.getPrototypeOf, Object), ri = "[object Object]", ni = Function.prototype, ii = Object.prototype, Tt = ni.toString, ai = ii.hasOwnProperty, oi = Tt.call(Object);
function oe(e) {
  if (!P(e) || L(e) != ri)
    return !1;
  var t = we(e);
  if (t === null)
    return !0;
  var r = ai.call(t, "constructor") && t.constructor;
  return typeof r == "function" && r instanceof r && Tt.call(r) == oi;
}
function si(e, t, r) {
  var n = -1, i = e.length;
  t < 0 && (t = -t > i ? 0 : i + t), r = r > i ? i : r, r < 0 && (r += i), i = t > r ? 0 : r - t >>> 0, t >>>= 0;
  for (var a = Array(i); ++n < i; )
    a[n] = e[n + t];
  return a;
}
function ui() {
  this.__data__ = new E(), this.size = 0;
}
function li(e) {
  var t = this.__data__, r = t.delete(e);
  return this.size = t.size, r;
}
function fi(e) {
  return this.__data__.get(e);
}
function ci(e) {
  return this.__data__.has(e);
}
var gi = 200;
function pi(e, t) {
  var r = this.__data__;
  if (r instanceof E) {
    var n = r.__data__;
    if (!K || n.length < gi - 1)
      return n.push([e, t]), this.size = ++r.size, this;
    r = this.__data__ = new j(n);
  }
  return r.set(e, t), this.size = r.size, this;
}
function $(e) {
  var t = this.__data__ = new E(e);
  this.size = t.size;
}
$.prototype.clear = ui;
$.prototype.delete = li;
$.prototype.get = fi;
$.prototype.has = ci;
$.prototype.set = pi;
function di(e, t) {
  return e && H(t, Y(t), e);
}
function _i(e, t) {
  return e && H(t, me(t), e);
}
var Ot = typeof exports == "object" && exports && !exports.nodeType && exports, Be = Ot && typeof module == "object" && module && !module.nodeType && module, hi = Be && Be.exports === Ot, ze = hi ? S.Buffer : void 0, Ke = ze ? ze.allocUnsafe : void 0;
function bi(e, t) {
  if (t)
    return e.slice();
  var r = e.length, n = Ke ? Ke(r) : new e.constructor(r);
  return e.copy(n), n;
}
function yi(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length, i = 0, a = []; ++r < n; ) {
    var o = e[r];
    t(o, r, e) && (a[i++] = o);
  }
  return a;
}
function At() {
  return [];
}
var mi = Object.prototype, vi = mi.propertyIsEnumerable, He = Object.getOwnPropertySymbols, $e = He ? function(e) {
  return e == null ? [] : (e = Object(e), yi(He(e), function(t) {
    return vi.call(e, t);
  }));
} : At;
function Ti(e, t) {
  return H(e, $e(e), t);
}
var Oi = Object.getOwnPropertySymbols, wt = Oi ? function(e) {
  for (var t = []; e; )
    Ae(t, $e(e)), e = we(e);
  return t;
} : At;
function Ai(e, t) {
  return H(e, wt(e), t);
}
function $t(e, t, r) {
  var n = t(e);
  return A(e) ? n : Ae(n, r(e));
}
function se(e) {
  return $t(e, Y, $e);
}
function St(e) {
  return $t(e, me, wt);
}
var ue = M(S, "DataView"), le = M(S, "Promise"), fe = M(S, "Set"), Ye = "[object Map]", wi = "[object Object]", Je = "[object Promise]", Xe = "[object Set]", qe = "[object WeakMap]", Ze = "[object DataView]", $i = F(ue), Si = F(K), Pi = F(le), Ei = F(fe), ji = F(ae), O = L;
(ue && O(new ue(new ArrayBuffer(1))) != Ze || K && O(new K()) != Ye || le && O(le.resolve()) != Je || fe && O(new fe()) != Xe || ae && O(new ae()) != qe) && (O = function(e) {
  var t = L(e), r = t == wi ? e.constructor : void 0, n = r ? F(r) : "";
  if (n)
    switch (n) {
      case $i:
        return Ze;
      case Si:
        return Ye;
      case Pi:
        return Je;
      case Ei:
        return Xe;
      case ji:
        return qe;
    }
  return t;
});
var Ci = Object.prototype, Ii = Ci.hasOwnProperty;
function xi(e) {
  var t = e.length, r = new e.constructor(t);
  return t && typeof e[0] == "string" && Ii.call(e, "index") && (r.index = e.index, r.input = e.input), r;
}
var Q = S.Uint8Array;
function Se(e) {
  var t = new e.constructor(e.byteLength);
  return new Q(t).set(new Q(e)), t;
}
function Li(e, t) {
  var r = t ? Se(e.buffer) : e.buffer;
  return new e.constructor(r, e.byteOffset, e.byteLength);
}
var Fi = /\w*$/;
function Mi(e) {
  var t = new e.constructor(e.source, Fi.exec(e));
  return t.lastIndex = e.lastIndex, t;
}
var We = T ? T.prototype : void 0, Qe = We ? We.valueOf : void 0;
function Ri(e) {
  return Qe ? Object(Qe.call(e)) : {};
}
function Ni(e, t) {
  var r = t ? Se(e.buffer) : e.buffer;
  return new e.constructor(r, e.byteOffset, e.length);
}
var Di = "[object Boolean]", Ui = "[object Date]", Gi = "[object Map]", Bi = "[object Number]", zi = "[object RegExp]", Ki = "[object Set]", Hi = "[object String]", Yi = "[object Symbol]", Ji = "[object ArrayBuffer]", Xi = "[object DataView]", qi = "[object Float32Array]", Zi = "[object Float64Array]", Wi = "[object Int8Array]", Qi = "[object Int16Array]", Vi = "[object Int32Array]", ki = "[object Uint8Array]", ea = "[object Uint8ClampedArray]", ta = "[object Uint16Array]", ra = "[object Uint32Array]";
function na(e, t, r) {
  var n = e.constructor;
  switch (t) {
    case Ji:
      return Se(e);
    case Di:
    case Ui:
      return new n(+e);
    case Xi:
      return Li(e, r);
    case qi:
    case Zi:
    case Wi:
    case Qi:
    case Vi:
    case ki:
    case ea:
    case ta:
    case ra:
      return Ni(e, r);
    case Gi:
      return new n();
    case Bi:
    case Hi:
      return new n(e);
    case zi:
      return Mi(e);
    case Ki:
      return new n();
    case Yi:
      return Ri(e);
  }
}
function ia(e) {
  return typeof e.constructor == "function" && !he(e) ? lr(we(e)) : {};
}
var aa = "[object Map]";
function oa(e) {
  return P(e) && O(e) == aa;
}
var Ve = N && N.isMap, sa = Ve ? ye(Ve) : oa, ua = "[object Set]";
function la(e) {
  return P(e) && O(e) == ua;
}
var ke = N && N.isSet, fa = ke ? ye(ke) : la, ca = 1, ga = 2, pa = 4, Pt = "[object Arguments]", da = "[object Array]", _a = "[object Boolean]", ha = "[object Date]", ba = "[object Error]", Et = "[object Function]", ya = "[object GeneratorFunction]", ma = "[object Map]", va = "[object Number]", jt = "[object Object]", Ta = "[object RegExp]", Oa = "[object Set]", Aa = "[object String]", wa = "[object Symbol]", $a = "[object WeakMap]", Sa = "[object ArrayBuffer]", Pa = "[object DataView]", Ea = "[object Float32Array]", ja = "[object Float64Array]", Ca = "[object Int8Array]", Ia = "[object Int16Array]", xa = "[object Int32Array]", La = "[object Uint8Array]", Fa = "[object Uint8ClampedArray]", Ma = "[object Uint16Array]", Ra = "[object Uint32Array]", _ = {};
_[Pt] = _[da] = _[Sa] = _[Pa] = _[_a] = _[ha] = _[Ea] = _[ja] = _[Ca] = _[Ia] = _[xa] = _[ma] = _[va] = _[jt] = _[Ta] = _[Oa] = _[Aa] = _[wa] = _[La] = _[Fa] = _[Ma] = _[Ra] = !0;
_[ba] = _[Et] = _[$a] = !1;
function q(e, t, r, n, i, a) {
  var o, s = t & ca, u = t & ga, c = t & pa;
  if (r && (o = i ? r(e, n, i, a) : r(e)), o !== void 0)
    return o;
  if (!D(e))
    return e;
  var g = A(e);
  if (g) {
    if (o = xi(e), !s)
      return cr(e, o);
  } else {
    var p = O(e), d = p == Et || p == ya;
    if (W(e))
      return bi(e, s);
    if (p == jt || p == Pt || d && !i) {
      if (o = u || d ? {} : ia(e), !s)
        return u ? Ai(e, _i(o, e)) : Ti(e, di(o, e));
    } else {
      if (!_[p])
        return i ? e : {};
      o = na(e, p, s);
    }
  }
  a || (a = new $());
  var l = a.get(e);
  if (l)
    return l;
  a.set(e, o), fa(e) ? e.forEach(function(f) {
    o.add(q(f, t, r, f, e, a));
  }) : sa(e) && e.forEach(function(f, y) {
    o.set(y, q(f, t, r, y, e, a));
  });
  var m = c ? u ? St : se : u ? me : Y, b = g ? void 0 : m(e);
  return mr(b || e, function(f, y) {
    b && (y = f, f = e[y]), pt(o, y, q(f, t, r, y, e, a));
  }), o;
}
var Na = "__lodash_hash_undefined__";
function Da(e) {
  return this.__data__.set(e, Na), this;
}
function Ua(e) {
  return this.__data__.has(e);
}
function V(e) {
  var t = -1, r = e == null ? 0 : e.length;
  for (this.__data__ = new j(); ++t < r; )
    this.add(e[t]);
}
V.prototype.add = V.prototype.push = Da;
V.prototype.has = Ua;
function Ga(e, t) {
  for (var r = -1, n = e == null ? 0 : e.length; ++r < n; )
    if (t(e[r], r, e))
      return !0;
  return !1;
}
function Ba(e, t) {
  return e.has(t);
}
var za = 1, Ka = 2;
function Ct(e, t, r, n, i, a) {
  var o = r & za, s = e.length, u = t.length;
  if (s != u && !(o && u > s))
    return !1;
  var c = a.get(e), g = a.get(t);
  if (c && g)
    return c == t && g == e;
  var p = -1, d = !0, l = r & Ka ? new V() : void 0;
  for (a.set(e, t), a.set(t, e); ++p < s; ) {
    var m = e[p], b = t[p];
    if (n)
      var f = o ? n(b, m, p, t, e, a) : n(m, b, p, e, t, a);
    if (f !== void 0) {
      if (f)
        continue;
      d = !1;
      break;
    }
    if (l) {
      if (!Ga(t, function(y, w) {
        if (!Ba(l, w) && (m === y || i(m, y, r, n, a)))
          return l.push(w);
      })) {
        d = !1;
        break;
      }
    } else if (!(m === b || i(m, b, r, n, a))) {
      d = !1;
      break;
    }
  }
  return a.delete(e), a.delete(t), d;
}
function Ha(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n, i) {
    r[++t] = [i, n];
  }), r;
}
function Ya(e) {
  var t = -1, r = Array(e.size);
  return e.forEach(function(n) {
    r[++t] = n;
  }), r;
}
var Ja = 1, Xa = 2, qa = "[object Boolean]", Za = "[object Date]", Wa = "[object Error]", Qa = "[object Map]", Va = "[object Number]", ka = "[object RegExp]", eo = "[object Set]", to = "[object String]", ro = "[object Symbol]", no = "[object ArrayBuffer]", io = "[object DataView]", et = T ? T.prototype : void 0, ie = et ? et.valueOf : void 0;
function ao(e, t, r, n, i, a, o) {
  switch (r) {
    case io:
      if (e.byteLength != t.byteLength || e.byteOffset != t.byteOffset)
        return !1;
      e = e.buffer, t = t.buffer;
    case no:
      return !(e.byteLength != t.byteLength || !a(new Q(e), new Q(t)));
    case qa:
    case Za:
    case Va:
      return de(+e, +t);
    case Wa:
      return e.name == t.name && e.message == t.message;
    case ka:
    case to:
      return e == t + "";
    case Qa:
      var s = Ha;
    case eo:
      var u = n & Ja;
      if (s || (s = Ya), e.size != t.size && !u)
        return !1;
      var c = o.get(e);
      if (c)
        return c == t;
      n |= Xa, o.set(e, t);
      var g = Ct(s(e), s(t), n, i, a, o);
      return o.delete(e), g;
    case ro:
      if (ie)
        return ie.call(e) == ie.call(t);
  }
  return !1;
}
var oo = 1, so = Object.prototype, uo = so.hasOwnProperty;
function lo(e, t, r, n, i, a) {
  var o = r & oo, s = se(e), u = s.length, c = se(t), g = c.length;
  if (u != g && !o)
    return !1;
  for (var p = u; p--; ) {
    var d = s[p];
    if (!(o ? d in t : uo.call(t, d)))
      return !1;
  }
  var l = a.get(e), m = a.get(t);
  if (l && m)
    return l == t && m == e;
  var b = !0;
  a.set(e, t), a.set(t, e);
  for (var f = o; ++p < u; ) {
    d = s[p];
    var y = e[d], w = t[d];
    if (n)
      var C = o ? n(w, y, d, t, e, a) : n(y, w, d, e, t, a);
    if (!(C === void 0 ? y === w || i(y, w, r, n, a) : C)) {
      b = !1;
      break;
    }
    f || (f = d == "constructor");
  }
  if (b && !f) {
    var U = e.constructor, R = t.constructor;
    U != R && "constructor" in e && "constructor" in t && !(typeof U == "function" && U instanceof U && typeof R == "function" && R instanceof R) && (b = !1);
  }
  return a.delete(e), a.delete(t), b;
}
var fo = 1, tt = "[object Arguments]", rt = "[object Array]", X = "[object Object]", co = Object.prototype, nt = co.hasOwnProperty;
function go(e, t, r, n, i, a) {
  var o = A(e), s = A(t), u = o ? rt : O(e), c = s ? rt : O(t);
  u = u == tt ? X : u, c = c == tt ? X : c;
  var g = u == X, p = c == X, d = u == c;
  if (d && W(e)) {
    if (!W(t))
      return !1;
    o = !0, g = !1;
  }
  if (d && !g)
    return a || (a = new $()), o || yt(e) ? Ct(e, t, r, n, i, a) : ao(e, t, u, r, n, i, a);
  if (!(r & fo)) {
    var l = g && nt.call(e, "__wrapped__"), m = p && nt.call(t, "__wrapped__");
    if (l || m) {
      var b = l ? e.value() : e, f = m ? t.value() : t;
      return a || (a = new $()), i(b, f, r, n, a);
    }
  }
  return d ? (a || (a = new $()), lo(e, t, r, n, i, a)) : !1;
}
function Pe(e, t, r, n, i) {
  return e === t ? !0 : e == null || t == null || !P(e) && !P(t) ? e !== e && t !== t : go(e, t, r, n, Pe, i);
}
var po = 1, _o = 2;
function ho(e, t, r, n) {
  var i = r.length, a = i;
  if (e == null)
    return !a;
  for (e = Object(e); i--; ) {
    var o = r[i];
    if (o[2] ? o[1] !== e[o[0]] : !(o[0] in e))
      return !1;
  }
  for (; ++i < a; ) {
    o = r[i];
    var s = o[0], u = e[s], c = o[1];
    if (o[2]) {
      if (u === void 0 && !(s in e))
        return !1;
    } else {
      var g = new $(), p;
      if (!(p === void 0 ? Pe(c, u, po | _o, n, g) : p))
        return !1;
    }
  }
  return !0;
}
function It(e) {
  return e === e && !D(e);
}
function bo(e) {
  for (var t = Y(e), r = t.length; r--; ) {
    var n = t[r], i = e[n];
    t[r] = [n, i, It(i)];
  }
  return t;
}
function xt(e, t) {
  return function(r) {
    return r == null ? !1 : r[e] === t && (t !== void 0 || e in Object(r));
  };
}
function yo(e) {
  var t = bo(e);
  return t.length == 1 && t[0][2] ? xt(t[0][0], t[0][1]) : function(r) {
    return r === e || ho(r, e, t);
  };
}
function mo(e, t) {
  return e != null && t in Object(e);
}
function vo(e, t, r) {
  t = te(t, e);
  for (var n = -1, i = t.length, a = !1; ++n < i; ) {
    var o = J(t[n]);
    if (!(a = e != null && r(e, o)))
      break;
    e = e[o];
  }
  return a || ++n != i ? a : (i = e == null ? 0 : e.length, !!i && _e(i) && gt(o, i) && (A(e) || be(e)));
}
function To(e, t) {
  return e != null && vo(e, t, mo);
}
var Oo = 1, Ao = 2;
function wo(e, t) {
  return ve(e) && It(t) ? xt(J(e), t) : function(r) {
    var n = Qn(r, e);
    return n === void 0 && n === t ? To(r, e) : Pe(t, n, Oo | Ao);
  };
}
function $o(e) {
  return function(t) {
    return t == null ? void 0 : t[e];
  };
}
function So(e) {
  return function(t) {
    return Oe(t, e);
  };
}
function Po(e) {
  return ve(e) ? $o(J(e)) : So(e);
}
function Eo(e) {
  return typeof e == "function" ? e : e == null ? ft : typeof e == "object" ? A(e) ? wo(e[0], e[1]) : yo(e) : Po(e);
}
function jo(e) {
  return function(t, r, n) {
    for (var i = -1, a = Object(t), o = n(t), s = o.length; s--; ) {
      var u = o[++i];
      if (r(a[u], u, a) === !1)
        break;
    }
    return t;
  };
}
var Co = jo();
function Io(e, t) {
  return e && Co(e, t, Y);
}
function xo(e) {
  var t = e == null ? 0 : e.length;
  return t ? e[t - 1] : void 0;
}
function Lo(e, t) {
  return t.length < 2 ? e : Oe(e, si(t, 0, -1));
}
function Fo(e, t) {
  var r = {};
  return t = Eo(t), Io(e, function(n, i, a) {
    pe(r, t(n, i, a), n);
  }), r;
}
function Mo(e, t) {
  return t = te(t, e), e = Lo(e, t), e == null || delete e[J(xo(t))];
}
function Ro(e) {
  return oe(e) ? void 0 : e;
}
var No = 1, Do = 2, Uo = 4, Lt = ti(function(e, t) {
  var r = {};
  if (e == null)
    return r;
  var n = !1;
  t = ut(t, function(a) {
    return a = te(a, e), n || (n = a.length > 1), a;
  }), H(e, St(e), r), n && (r = q(r, No | Do | Uo, Ro));
  for (var i = t.length; i--; )
    Mo(r, t[i]);
  return r;
});
async function Go() {
  window.ms_globals || (window.ms_globals = {}), window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Bo(e) {
  return await Go(), e().then((t) => t.default);
}
const Ft = [
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
], zo = Ft.concat(["attached_events"]);
function gs(e, t = {}, r = !1) {
  return Fo(Lt(e, r ? [] : Ft), (n, i) => t[i] || Mt(i));
}
function ps(e, t) {
  const {
    gradio: r,
    _internal: n,
    restProps: i,
    originalRestProps: a,
    ...o
  } = e, s = (i == null ? void 0 : i.attachedEvents) || [];
  return {
    ...Array.from(/* @__PURE__ */ new Set([...Object.keys(n).map((u) => {
      const c = u.match(/bind_(.+)_event/);
      return c && c[1] ? c[1] : null;
    }).filter(Boolean), ...s.map((u) => t && t[u] ? t[u] : u)])).reduce((u, c) => {
      const g = c.split("_"), p = (...l) => {
        const m = l.map((f) => l && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
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
        let b;
        try {
          b = JSON.parse(JSON.stringify(m));
        } catch {
          let f = function(y) {
            try {
              return JSON.stringify(y), y;
            } catch {
              return oe(y) ? Object.fromEntries(Object.entries(y).map(([w, C]) => {
                try {
                  return JSON.stringify(C), [w, C];
                } catch {
                  return oe(C) ? [w, Object.fromEntries(Object.entries(C).filter(([U, R]) => {
                    try {
                      return JSON.stringify(R), !0;
                    } catch {
                      return !1;
                    }
                  }))] : null;
                }
              }).filter(Boolean)) : {};
            }
          };
          b = m.map((y) => f(y));
        }
        return r.dispatch(c.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: b,
          component: {
            ...o,
            ...Lt(a, zo)
          }
        });
      };
      if (g.length > 1) {
        let l = {
          ...o.props[g[0]] || (i == null ? void 0 : i[g[0]]) || {}
        };
        u[g[0]] = l;
        for (let b = 1; b < g.length - 1; b++) {
          const f = {
            ...o.props[g[b]] || (i == null ? void 0 : i[g[b]]) || {}
          };
          l[g[b]] = f, l = f;
        }
        const m = g[g.length - 1];
        return l[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = p, u;
      }
      const d = g[0];
      return u[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = p, u;
    }, {}),
    __render_eventProps: {
      props: e,
      eventsMapping: t
    }
  };
}
const {
  SvelteComponent: Ko,
  assign: ce,
  claim_component: Ho,
  create_component: Yo,
  create_slot: Jo,
  destroy_component: Xo,
  detach: qo,
  empty: it,
  exclude_internal_props: at,
  flush: I,
  get_all_dirty_from_scope: Zo,
  get_slot_changes: Wo,
  get_spread_object: Qo,
  get_spread_update: Vo,
  handle_promise: ko,
  init: es,
  insert_hydration: ts,
  mount_component: rs,
  noop: v,
  safe_not_equal: ns,
  transition_in: Ee,
  transition_out: je,
  update_await_block_branch: is,
  update_slot_base: as
} = window.__gradio__svelte__internal;
function os(e) {
  return {
    c: v,
    l: v,
    m: v,
    p: v,
    i: v,
    o: v,
    d: v
  };
}
function ss(e) {
  let t, r;
  const n = [
    /*$$props*/
    e[8],
    {
      gradio: (
        /*gradio*/
        e[0]
      )
    },
    {
      props: (
        /*props*/
        e[1]
      )
    },
    {
      as_item: (
        /*as_item*/
        e[2]
      )
    },
    {
      visible: (
        /*visible*/
        e[3]
      )
    },
    {
      elem_id: (
        /*elem_id*/
        e[4]
      )
    },
    {
      elem_classes: (
        /*elem_classes*/
        e[5]
      )
    },
    {
      elem_style: (
        /*elem_style*/
        e[6]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [us]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let a = 0; a < n.length; a += 1)
    i = ce(i, n[a]);
  return t = new /*BubbleListRole*/
  e[11]({
    props: i
  }), {
    c() {
      Yo(t.$$.fragment);
    },
    l(a) {
      Ho(t.$$.fragment, a);
    },
    m(a, o) {
      rs(t, a, o), r = !0;
    },
    p(a, o) {
      const s = o & /*$$props, gradio, props, as_item, visible, elem_id, elem_classes, elem_style*/
      383 ? Vo(n, [o & /*$$props*/
      256 && Qo(
        /*$$props*/
        a[8]
      ), o & /*gradio*/
      1 && {
        gradio: (
          /*gradio*/
          a[0]
        )
      }, o & /*props*/
      2 && {
        props: (
          /*props*/
          a[1]
        )
      }, o & /*as_item*/
      4 && {
        as_item: (
          /*as_item*/
          a[2]
        )
      }, o & /*visible*/
      8 && {
        visible: (
          /*visible*/
          a[3]
        )
      }, o & /*elem_id*/
      16 && {
        elem_id: (
          /*elem_id*/
          a[4]
        )
      }, o & /*elem_classes*/
      32 && {
        elem_classes: (
          /*elem_classes*/
          a[5]
        )
      }, o & /*elem_style*/
      64 && {
        elem_style: (
          /*elem_style*/
          a[6]
        )
      }]) : {};
      o & /*$$scope*/
      1024 && (s.$$scope = {
        dirty: o,
        ctx: a
      }), t.$set(s);
    },
    i(a) {
      r || (Ee(t.$$.fragment, a), r = !0);
    },
    o(a) {
      je(t.$$.fragment, a), r = !1;
    },
    d(a) {
      Xo(t, a);
    }
  };
}
function us(e) {
  let t;
  const r = (
    /*#slots*/
    e[9].default
  ), n = Jo(
    r,
    e,
    /*$$scope*/
    e[10],
    null
  );
  return {
    c() {
      n && n.c();
    },
    l(i) {
      n && n.l(i);
    },
    m(i, a) {
      n && n.m(i, a), t = !0;
    },
    p(i, a) {
      n && n.p && (!t || a & /*$$scope*/
      1024) && as(
        n,
        r,
        i,
        /*$$scope*/
        i[10],
        t ? Wo(
          r,
          /*$$scope*/
          i[10],
          a,
          null
        ) : Zo(
          /*$$scope*/
          i[10]
        ),
        null
      );
    },
    i(i) {
      t || (Ee(n, i), t = !0);
    },
    o(i) {
      je(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function ls(e) {
  return {
    c: v,
    l: v,
    m: v,
    p: v,
    i: v,
    o: v,
    d: v
  };
}
function fs(e) {
  let t, r, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ls,
    then: ss,
    catch: os,
    value: 11,
    blocks: [, , ,]
  };
  return ko(
    /*AwaitedBubbleListRole*/
    e[7],
    n
  ), {
    c() {
      t = it(), n.block.c();
    },
    l(i) {
      t = it(), n.block.l(i);
    },
    m(i, a) {
      ts(i, t, a), n.block.m(i, n.anchor = a), n.mount = () => t.parentNode, n.anchor = t, r = !0;
    },
    p(i, [a]) {
      e = i, is(n, e, a);
    },
    i(i) {
      r || (Ee(n.block), r = !0);
    },
    o(i) {
      for (let a = 0; a < 3; a += 1) {
        const o = n.blocks[a];
        je(o);
      }
      r = !1;
    },
    d(i) {
      i && qo(t), n.block.d(i), n.token = null, n = null;
    }
  };
}
function cs(e, t, r) {
  let {
    $$slots: n = {},
    $$scope: i
  } = t;
  const a = Bo(() => import("./Role-0I2c7txo.js").then((l) => l.R));
  let {
    gradio: o
  } = t, {
    props: s = {}
  } = t, {
    as_item: u
  } = t, {
    visible: c = !0
  } = t, {
    elem_id: g = ""
  } = t, {
    elem_classes: p = []
  } = t, {
    elem_style: d = {}
  } = t;
  return e.$$set = (l) => {
    r(8, t = ce(ce({}, t), at(l))), "gradio" in l && r(0, o = l.gradio), "props" in l && r(1, s = l.props), "as_item" in l && r(2, u = l.as_item), "visible" in l && r(3, c = l.visible), "elem_id" in l && r(4, g = l.elem_id), "elem_classes" in l && r(5, p = l.elem_classes), "elem_style" in l && r(6, d = l.elem_style), "$$scope" in l && r(10, i = l.$$scope);
  }, t = at(t), [o, s, u, c, g, p, d, a, t, n, i];
}
class ds extends Ko {
  constructor(t) {
    super(), es(this, t, cs, fs, ns, {
      gradio: 0,
      props: 1,
      as_item: 2,
      visible: 3,
      elem_id: 4,
      elem_classes: 5,
      elem_style: 6
    });
  }
  get gradio() {
    return this.$$.ctx[0];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), I();
  }
  get props() {
    return this.$$.ctx[1];
  }
  set props(t) {
    this.$$set({
      props: t
    }), I();
  }
  get as_item() {
    return this.$$.ctx[2];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), I();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), I();
  }
  get elem_id() {
    return this.$$.ctx[4];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), I();
  }
  get elem_classes() {
    return this.$$.ctx[5];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), I();
  }
  get elem_style() {
    return this.$$.ctx[6];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), I();
  }
}
export {
  ds as I,
  D as a,
  ct as b,
  Bo as c,
  ps as d,
  ge as i,
  gs as m,
  S as r
};
