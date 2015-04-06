 count ← 0
 foreach side in polygon:
   if ray_intersects_segment(P,side) then
     count ← count + 1
 if is_odd(count) then
   return inside
 else
   return outside
,  ray_intersects_segment:
    P : the point from which the ray starts
    A : the end-point of the segment with the smallest y coordinate
        (A must be "below" B)
    B : the end-point of the segment with the greatest y coordinate
        (B must be "above" A)
 if Py = Ay or Py = By then
   Py ← Py + ε
 end if
 if Py < Ay or Py > By then 
   return false
 else if Px > max(Ax, Bx) then 
   return false
 else
   if Px < min(Ax, Bx) then
     return true
   else
     if Ax ≠ Bx then
       m_red ← (By - Ay)/(Bx - Ax)
     else
       m_red ← ∞
     end if
     if Ax ≠ Px then
       m_blue ← (Py - Ay)/(Px - Ax)
     else
       m_blue ← ∞
     end if
     if m_blue ≥ m_red then
       return true
     else
       return false
     end if
   end if
 end if
, package Polygons is    type Point is record      X, Y : Float;   end record;   type Point_List is array (Positive range <>) of Point;   subtype Segment is Point_List (1 .. 2);   type Polygon is array (Positive range <>) of Segment;    function Create_Polygon (List : Point_List) return Polygon;    function Is_Inside (Who : Point; Where : Polygon) return Boolean; end Polygons;, package body Polygons is   EPSILON : constant := 0.00001;    function Ray_Intersects_Segment     (Who   : Point;      Where : Segment)      return  Boolean   is      The_Point        : Point   := Who;      Above            : Point;      Below            : Point;      M_Red            : Float;      Red_Is_Infinity  : Boolean := False;      M_Blue           : Float;      Blue_Is_Infinity : Boolean := False;   begin      if Where (1).Y < Where (2).Y then         Above := Where (2);         Below := Where (1);      else         Above := Where (1);         Below := Where (2);      end if;      if The_Point.Y = Above.Y or The_Point.Y = Below.Y then         The_Point.Y := The_Point.Y + EPSILON;      end if;      if The_Point.Y < Below.Y or The_Point.Y > Above.Y then         return False;      elsif The_Point.X > Above.X and The_Point.X > Below.X then         return False;      elsif The_Point.X < Above.X and The_Point.X < Below.X then         return True;      else         if Above.X /= Below.X then            M_Red := (Above.Y - Below.Y) / (Above.X - Below.X);         else            Red_Is_Infinity := True;         end if;         if Below.X /= The_Point.X then            M_Blue := (The_Point.Y - Below.Y) / (The_Point.X - Below.X);         else            Blue_Is_Infinity := True;         end if;         if Blue_Is_Infinity then            return True;         elsif Red_Is_Infinity then            return False;         elsif M_Blue >= M_Red then            return True;         else            return False;         end if;      end if;   end Ray_Intersects_Segment;    function Create_Polygon (List : Point_List) return Polygon is      Result : Polygon (List'Range);      Side   : Segment;   begin      for I in List'Range loop         Side (1) := List (I);         if I = List'Last then            Side (2) := List (List'First);         else            Side (2) := List (I + 1);         end if;         Result (I) := Side;      end loop;      return Result;   end Create_Polygon;    function Is_Inside (Who : Point; Where : Polygon) return Boolean is      Count : Natural := 0;   begin      for Side in Where'Range loop         if Ray_Intersects_Segment (Who, Where (Side)) then            Count := Count + 1;         end if;      end loop;      if Count mod 2 = 0 then         return False;      else         return True;      end if;   end Is_Inside; end Polygons;, with Ada.Text_IO;with Polygons;procedure Main is   package Float_IO is new Ada.Text_IO.Float_IO (Float);   Test_Points : Polygons.Point_List :=     ((  5.0,  5.0),      (  5.0,  8.0),      (-10.0,  5.0),      (  0.0,  5.0),      ( 10.0,  5.0),      (  8.0,  5.0),      ( 10.0, 10.0));   Square      : Polygons.Polygon    :=     ((( 0.0,  0.0), (10.0,  0.0)),      ((10.0,  0.0), (10.0, 10.0)),      ((10.0, 10.0), ( 0.0, 10.0)),      (( 0.0, 10.0), ( 0.0,  0.0)));   Square_Hole : Polygons.Polygon    :=     ((( 0.0,  0.0), (10.0,  0.0)),      ((10.0,  0.0), (10.0, 10.0)),      ((10.0, 10.0), ( 0.0, 10.0)),      (( 0.0, 10.0), ( 0.0,  0.0)),      (( 2.5,  2.5), ( 7.5,  2.5)),      (( 7.5,  2.5), ( 7.5,  7.5)),      (( 7.5,  7.5), ( 2.5,  7.5)),      (( 2.5,  7.5), ( 2.5,  2.5)));   Strange     : Polygons.Polygon    :=     ((( 0.0,  0.0), ( 2.5,  2.5)),      (( 2.5,  2.5), ( 0.0, 10.0)),      (( 0.0, 10.0), ( 2.5,  7.5)),      (( 2.5,  7.5), ( 7.5,  7.5)),      (( 7.5,  7.5), (10.0, 10.0)),      ((10.0, 10.0), (10.0,  0.0)),      ((10.0,  0.0), ( 2.5,  2.5)));   Exagon      : Polygons.Polygon    :=     ((( 3.0,  0.0), ( 7.0,  0.0)),      (( 7.0,  0.0), (10.0,  5.0)),      ((10.0,  5.0), ( 7.0, 10.0)),      (( 7.0, 10.0), ( 3.0, 10.0)),      (( 3.0, 10.0), ( 0.0,  5.0)),      (( 0.0,  5.0), ( 3.0,  0.0)));begin   Ada.Text_IO.Put_Line ("Testing Square:");   for Point in Test_Points'Range loop      Ada.Text_IO.Put ("Point(");      Float_IO.Put (Test_Points (Point).X, 0, 0, 0);      Ada.Text_IO.Put (",");      Float_IO.Put (Test_Points (Point).Y, 0, 0, 0);      Ada.Text_IO.Put        ("): " &         Boolean'Image (Polygons.Is_Inside (Test_Points (Point), Square)));      Ada.Text_IO.New_Line;   end loop;   Ada.Text_IO.New_Line;   Ada.Text_IO.Put_Line ("Testing Square_Hole:");   for Point in Test_Points'Range loop      Ada.Text_IO.Put ("Point(");      Float_IO.Put (Test_Points (Point).X, 0, 0, 0);      Ada.Text_IO.Put (",");      Float_IO.Put (Test_Points (Point).Y, 0, 0, 0);      Ada.Text_IO.Put        ("): " &         Boolean'Image            (Polygons.Is_Inside (Test_Points (Point), Square_Hole)));      Ada.Text_IO.New_Line;   end loop;   Ada.Text_IO.New_Line;   Ada.Text_IO.Put_Line ("Testing Strange:");   for Point in Test_Points'Range loop      Ada.Text_IO.Put ("Point(");      Float_IO.Put (Test_Points (Point).X, 0, 0, 0);      Ada.Text_IO.Put (",");      Float_IO.Put (Test_Points (Point).Y, 0, 0, 0);      Ada.Text_IO.Put        ("): " &         Boolean'Image (Polygons.Is_Inside (Test_Points (Point), Strange)));      Ada.Text_IO.New_Line;   end loop;   Ada.Text_IO.New_Line;   Ada.Text_IO.Put_Line ("Testing Exagon:");   for Point in Test_Points'Range loop      Ada.Text_IO.Put ("Point(");      Float_IO.Put (Test_Points (Point).X, 0, 0, 0);      Ada.Text_IO.Put (",");      Float_IO.Put (Test_Points (Point).Y, 0, 0, 0);      Ada.Text_IO.Put        ("): " &         Boolean'Image (Polygons.Is_Inside (Test_Points (Point), Exagon)));      Ada.Text_IO.New_Line;   end loop;end Main;, Testing Square:
Point(5.0,5.0): TRUE
Point(5.0,8.0): TRUE
Point(-10.0,5.0): FALSE
Point(0.0,5.0): FALSE
Point(10.0,5.0): TRUE
Point(8.0,5.0): TRUE
Point(10.0,10.0): FALSE

Testing Square_Hole:
Point(5.0,5.0): FALSE
Point(5.0,8.0): TRUE
Point(-10.0,5.0): FALSE
Point(0.0,5.0): FALSE
Point(10.0,5.0): TRUE
Point(8.0,5.0): TRUE
Point(10.0,10.0): FALSE

Testing Strange:
Point(5.0,5.0): TRUE
Point(5.0,8.0): FALSE
Point(-10.0,5.0): FALSE
Point(0.0,5.0): FALSE
Point(10.0,5.0): TRUE
Point(8.0,5.0): TRUE
Point(10.0,10.0): FALSE

Testing Exagon:
Point(5.0,5.0): TRUE
Point(5.0,8.0): TRUE
Point(-10.0,5.0): FALSE
Point(0.0,5.0): FALSE
Point(10.0,5.0): TRUE
Point(8.0,5.0): TRUE
Point(10.0,10.0): FALSE, Points :=[{x:  5.0, y: 5.0}		, {x:  5.0, y: 8.0}		, {x:-10.0, y: 5.0}		, {x:  0.0, y: 5.0}		, {x: 10.0, y: 5.0}		, {x:  8.0, y: 5.0}		, {x: 10.0, y:10.0}]Square :=[{x: 0.0, y: 0.0}, {x:10.0, y: 0.0}		, {x:10.0, y: 0.0}, {x:10.0, y:10.0}		, {x:10.0, y:10.0}, {x: 0.0, y:10.0}		, {x: 0.0, y:10.0}, {x: 0.0, y: 0.0}]Sq_Hole:=[{x: 0.0, y: 0.0}, {x:10.0, y: 0.0}		, {x:10.0, y: 0.0}, {x:10.0, y:10.0}		, {x:10.0, y:10.0}, {x: 0.0, y:10.0}		, {x: 0.0, y:10.0}, {x: 0.0, y: 0.0}		, {x: 2.5, y: 2.5}, {x: 7.5, y: 2.5}		, {x: 7.5, y: 2.5}, {x: 7.5, y: 7.5}		, {x: 7.5, y: 7.5}, {x: 2.5, y: 7.5}		, {x: 2.5, y: 7.5}, {x: 2.5, y: 2.5}]Strange:=[{x: 0.0, y: 0.0}, {x: 2.5, y: 2.5}		, {x: 2.5, y: 2.5}, {x: 0.0, y:10.0}		, {x: 0.0, y:10.0}, {x: 2.5, y: 7.5}		, {x: 2.5, y: 7.5}, {x: 7.5, y: 7.5}		, {x: 7.5, y: 7.5}, {x:10.0, y:10.0}		, {x:10.0, y:10.0}, {x:10.0, y: 0.0}		, {x:10.0, y: 0.0}, {x: 2.5, y: 2.5}]Exagon :=[{x: 3.0, y: 0.0}, {x: 7.0, y: 0.0}		, {x: 7.0, y: 0.0}, {x:10.0, y: 5.0}		, {x:10.0, y: 5.0}, {x: 7.0, y:10.0}		, {x: 7.0, y:10.0}, {x: 3.0, y:10.0}		, {x: 3.0, y:10.0}, {x: 0.0, y: 5.0}		, {x: 0.0, y: 5.0}, {x: 3.0, y: 0.0}]Polygons := {"Square":Square, "Sq_Hole":Sq_Hole, "Strange":Strange, "Exagon":Exagon}For j, Poly in Polygons	For i, Point in Points		If (point_in_polygon(Point,Poly))			s.= j " does contain point " i "`n"		Else			s.= j " doesn't contain point " i "`n"Msgbox %s% point_in_polygon(Point,Poly) {	n:=Poly.MaxIndex()	count:=0	loop, %n% {		if (ray_intersects_segment(Point,Poly[A_Index],Poly[mod(A_Index,n)+1])) {			count++		}	}	if (mod(count,2)) { ; true = inside, false = outside		return true		; P is in the polygon	} else {		return false	; P isn't in the polygon	}} ray_intersects_segment(P,A,B) {	;P = the point from which the ray starts	;A = the end-point of the segment with the smallest y coordinate	;B = the end-point of the segment with the greatest y coordinate	if (A.y > B.y) {		temp:=A		A:=B		B:=temp	}	if (P.y = A.y or P.y = B.y) {		P.y += 0.000001	}	if (P.y < A.y or P.y > B.y) {		return false	} else if (P.x > A.x && P.x > B.x) {		return false	} else {		if (P.x < A.x && P.x < B.x) {			return true		} else {			if (A.x != B.x) {				m_red := (B.y - A.y)/(B.x - A.x)			} else {				m_red := "inf"			}			if (A.x != P.x) {				m_blue := (P.y - A.y)/(P.x - A.x)			} else {				m_blue := "inf"			}			if (m_blue >= m_red) {				return true			} else {				return false			}		}	}}, ---------------------------
Ray-casting_algorithm.ahkl
---------------------------
Exagon does contain point 1
Exagon does contain point 2
Exagon doesn't contain point 3
Exagon doesn't contain point 4
Exagon does contain point 5
Exagon does contain point 6
Exagon doesn't contain point 7
Sq_Hole doesn't contain point 1
Sq_Hole does contain point 2
Sq_Hole doesn't contain point 3
Sq_Hole doesn't contain point 4
Sq_Hole does contain point 5
Sq_Hole does contain point 6
Sq_Hole doesn't contain point 7
Square does contain point 1
Square does contain point 2
Square doesn't contain point 3
Square doesn't contain point 4
Square does contain point 5
Square does contain point 6
Square doesn't contain point 7
Strange does contain point 1
Strange doesn't contain point 2
Strange doesn't contain point 3
Strange doesn't contain point 4
Strange does contain point 5
Strange does contain point 6
Strange doesn't contain point 7

---------------------------
OK   
---------------------------, #include <stdio.h>#include <stdlib.h>#include <math.h> typedef struct { double x, y; } vec;typedef struct { int n; vec* v; } polygon_t, *polygon; #define BIN_V(op, xx, yy) vec v##op(vec a,vec b){vec c;c.x=xx;c.y=yy;return c;}#define BIN_S(op, r) double v##op(vec a, vec b){ return r; }BIN_V(sub, a.x - b.x, a.y - b.y);BIN_V(add, a.x + b.x, a.y + b.y);BIN_S(dot, a.x * b.x + a.y * b.y);BIN_S(cross, a.x * b.y - a.y * b.x); /* return a + s * b */vec vmadd(vec a, double s, vec b){	vec c;	c.x = a.x + s * b.x;	c.y = a.y + s * b.y;	return c;} /* check if x0->x1 edge crosses y0->y1 edge. dx = x1 - x0, dy = y1 - y0, then   solve  x0 + a * dx == y0 + b * dy with a, b in real   cross both sides with dx, then: (remember, cross product is a scalar)	x0 X dx = y0 X dx + b * (dy X dx)   similarly,	x0 X dy + a * (dx X dy) == y0 X dy   there is an intersection iff 0 <= a <= 1 and 0 <= b <= 1    returns: 1 for intersect, -1 for not, 0 for hard to say (if the intersect   point is too close to y0 or y1)*/int intersect(vec x0, vec x1, vec y0, vec y1, double tol, vec *sect){	vec dx = vsub(x1, x0), dy = vsub(y1, y0);	double d = vcross(dy, dx), a;	if (!d) return 0; /* edges are parallel */ 	a = (vcross(x0, dx) - vcross(y0, dx)) / d;	if (sect)		*sect = vmadd(y0, a, dy); 	if (a < -tol || a > 1 + tol) return -1;	if (a < tol || a > 1 - tol) return 0; 	a = (vcross(x0, dy) - vcross(y0, dy)) / d;	if (a < 0 || a > 1) return -1; 	return 1;} /* distance between x and nearest point on y0->y1 segment.  if the point   lies outside the segment, returns infinity */double dist(vec x, vec y0, vec y1, double tol){	vec dy = vsub(y1, y0);	vec x1, s;	int r; 	x1.x = x.x + dy.y; x1.y = x.y - dy.x;	r = intersect(x, x1, y0, y1, tol, &s);	if (r == -1) return HUGE_VAL;	s = vsub(s, x);	return sqrt(vdot(s, s));} #define for_v(i, z, p) for(i = 0, z = p->v; i < p->n; i++, z++)/* returns 1 for inside, -1 for outside, 0 for on edge */int inside(vec v, polygon p, double tol){	/* should assert p->n > 1 */	int i, k, crosses, intersectResult;	vec *pv;	double min_x, max_x, min_y, max_y; 	for (i = 0; i < p->n; i++) {		k = (i + 1) % p->n;		min_x = dist(v, p->v[i], p->v[k], tol);		if (min_x < tol) return 0;	} 	min_x = max_x = p->v[0].x;	min_y = max_y = p->v[1].y; 	/* calculate extent of polygon */	for_v(i, pv, p) {		if (pv->x > max_x) max_x = pv->x;		if (pv->x < min_x) min_x = pv->x;		if (pv->y > max_y) max_y = pv->y;		if (pv->y < min_y) min_y = pv->y;	}	if (v.x < min_x || v.x > max_x || v.y < min_y || v.y > max_y)		return -1; 	max_x -= min_x; max_x *= 2;	max_y -= min_y; max_y *= 2;	max_x += max_y; 	vec e;	while (1) {		crosses = 0;		/* pick a rand point far enough to be outside polygon */		e.x = v.x + (1 + rand() / (RAND_MAX + 1.)) * max_x;		e.y = v.y + (1 + rand() / (RAND_MAX + 1.)) * max_x; 		for (i = 0; i < p->n; i++) {			k = (i + 1) % p->n;			intersectResult = intersect(v, e, p->v[i], p->v[k], tol, 0); 			/* picked a bad point, ray got too close to vertex.			   re-pick */			if (!intersectResult) break; 			if (intersectResult == 1) crosses++;		}		if (i == p->n) break;	}	return (crosses & 1) ? 1 : -1;} int main(){	vec vsq[] = {	{0,0}, {10,0}, {10,10}, {0,10},			{2.5,2.5}, {7.5,0.1}, {7.5,7.5}, {2.5,7.5}}; 	polygon_t sq = { 4, vsq }, /* outer square */		sq_hole = { 8, vsq }; /* outer and inner square, ie hole */ 	vec c = { 10, 5 }; /* on edge */	vec d = { 5, 5 }; 	printf("%d\n", inside(c, &sq, 1e-10));	printf("%d\n", inside(c, &sq_hole, 1e-10)); 	printf("%d\n", inside(d, &sq, 1e-10));	/* in */	printf("%d\n", inside(d, &sq_hole, 1e-10));  /* out (in the hole) */ 	return 0;}, import std.stdio, std.math, std.algorithm; immutable struct Point { double x, y; }immutable struct Edge { Point a, b; }immutable struct Figure {    string name;    Edge[] edges;} bool contains(in Figure poly, in Point p) pure nothrow @safe @nogc {    static bool raySegI(in Point p, in Edge edge)    pure nothrow @safe @nogc {        enum double epsilon = 0.00001;        with (edge) {            if (a.y > b.y)                //swap(a, b); // if edge is mutable                return raySegI(p, Edge(b, a));            if (p.y == a.y || p.y == b.y)                //p.y += epsilon; // if p is mutable                return raySegI(Point(p.x, p.y + epsilon), edge);            if (p.y > b.y || p.y < a.y || p.x > max(a.x, b.x))                return false;            if (p.x < min(a.x, b.x))                return true;            immutable blue = (abs(a.x - p.x) > double.min_normal) ?                             ((p.y - a.y) / (p.x - a.x)) :                             double.max;            immutable red = (abs(a.x - b.x) > double.min_normal) ?                            ((b.y - a.y) / (b.x - a.x)) :                            double.max;            return blue >= red;        }    }     return poly.edges.count!(e => raySegI(p, e)) % 2;} void main() {    immutable Figure[] polys = [  {"Square", [    {{ 0.0,  0.0}, {10.0,  0.0}},  {{10.0,  0.0}, {10.0, 10.0}},    {{10.0, 10.0}, { 0.0, 10.0}},  {{ 0.0, 10.0}, { 0.0,  0.0}}]},  {"Square hole", [    {{ 0.0,  0.0}, {10.0,  0.0}},  {{10.0,  0.0}, {10.0, 10.0}},    {{10.0, 10.0}, { 0.0, 10.0}},  {{ 0.0, 10.0}, { 0.0,  0.0}},    {{ 2.5,  2.5}, { 7.5,  2.5}},  {{ 7.5,  2.5}, { 7.5,  7.5}},    {{ 7.5,  7.5}, { 2.5,  7.5}},  {{ 2.5,  7.5}, { 2.5,  2.5}}]},  {"Strange", [    {{ 0.0,  0.0}, { 2.5,  2.5}},  {{ 2.5,  2.5}, { 0.0, 10.0}},    {{ 0.0, 10.0}, { 2.5,  7.5}},  {{ 2.5,  7.5}, { 7.5,  7.5}},    {{ 7.5,  7.5}, {10.0, 10.0}},  {{10.0, 10.0}, {10.0,  0.0}},    {{10.0,  0},   { 2.5,  2.5}}]},  {"Exagon", [    {{ 3.0,  0.0}, { 7.0,  0.0}},  {{ 7.0,  0.0}, {10.0,  5.0}},    {{10.0,  5.0}, { 7.0, 10.0}},  {{ 7.0, 10.0}, { 3.0, 10.0}},    {{ 3.0, 10.0}, { 0.0,  5.0}},  {{ 0.0,  5.0}, { 3.0,  0.0}}]}];     immutable Point[] testPoints = [{ 5, 5}, {5, 8}, {-10,  5}, {0, 5},                                    {10, 5}, {8, 5}, { 10, 10}];     foreach (immutable poly; polys) {        writefln(`Is point inside figure "%s"?`, poly.name);        foreach (immutable p; testPoints)            writefln("  (%3s, %2s): %s", p.x, p.y, contains(poly, p));        writeln;    }}, Is point inside figure "Square"?
  (  5,  5): true
  (  5,  8): true
  (-10,  5): false
  (  0,  5): false
  ( 10,  5): true
  (  8,  5): true
  ( 10, 10): false

Is point inside figure "Square hole"?
  (  5,  5): false
  (  5,  8): true
  (-10,  5): false
  (  0,  5): false
  ( 10,  5): true
  (  8,  5): true
  ( 10, 10): false

Is point inside figure "Strange"?
  (  5,  5): true
  (  5,  8): false
  (-10,  5): false
  (  0,  5): false
  ( 10,  5): true
  (  8,  5): true
  ( 10, 10): false

Is point inside figure "Exagon"?
  (  5,  5): true
  (  5,  8): true
  (-10,  5): false
  (  0,  5): false
  ( 10,  5): true
  (  8,  5): true
  ( 10, 10): false,   Point = (@x,@y) ->   pointInPoly = (point,poly) ->    segments = for pointA, index in poly                 pointB = poly[(index + 1) % poly.length]                 [pointA,pointB]    intesected = (segment for segment in segments when rayIntesectsSegment(point,segment))    intesected.length % 2 != 0   rayIntesectsSegment = (p,segment) ->    [p1,p2] = segment    [a,b] = if p1.y < p2.y              [p1,p2]            else              [p2,p1]    if p.y == b.y || p.y == a.y      p.y += Number.MIN_VALUE     if p.y > b.y || p.y < a.y      false    else if p.x > a.x && p.x > b.x      false    else if p.x < a.x && p.x < b.x      true    else      mAB = (b.y - a.y) / (b.x - a.x)      mAP = (p.y - a.y) / (p.x - a.x)      mAP > mAB, (defun point-in-polygon (point polygon)  (do ((in-p nil)) ((endp polygon) in-p)    (when (ray-intersects-segment point (pop polygon))      (setf in-p (not in-p))))) (defun ray-intersects-segment (point segment &optional (epsilon .001))  (destructuring-bind (px . py) point    (destructuring-bind ((ax . ay) . (bx . by)) segment      (when (< ay by)        (rotatef ay by)        (rotatef ax bx))      (when (or (= py ay) (= py by))        (incf py epsilon))      (cond       ;; point is above, below, or to the right of the rectangle       ;; determined by segment; ray does not intesect the segment.       ((or (> px (max ax bx)) (> py (max ay by)) (< py (min ay by)))        nil)       ;; point is to left of the rectangle; ray intersects segment       ((< px (min ax bx))        t)       ;; point is within the rectangle...       (t (let ((m-red (if (= ax bx) nil                         (/ (- by ay) (- bx ax))))                (m-blue (if (= px ax) nil                          (/ (- py ay) (- px ax)))))            (cond             ((null m-blue) t)             ((null m-red) nil)             (t (>= m-blue m-red))))))))), (defparameter *points*  #((0 . 0) (10 . 0) (10 . 10) (0 . 10)      (2.5 . 2.5) (7.5 . 2.5) (7.5 . 7.5) (2.5 . 7.5)     (0 . 5) (10 . 5) (3 . 0) (7 . 0)    (7 . 10) (3 . 10))) (defun create-polygon (indices &optional (points *points*))  (loop for (a b) on indices by 'cddr        collecting (cons (aref points (1- a))                         (aref points (1- b))))) (defun square ()  (create-polygon '(1 2 2 3 3 4 4 1))) (defun square-hole ()  (create-polygon '(1 2 2 3 3 4 4 1 5 6 6 7 7 8 8 5))) (defun strange ()  (create-polygon '(1 5 5 4 4 8 8 7 7 3 3 2 2 5))) (defun exagon ()  (create-polygon '(11 12 12 10 10 13 13 14 14 9 9 11))) (defparameter *test-points*  #((5 . 5) (5 . 8) (-10 . 5) (0 . 5)    (10 . 5) (8 . 5) (10 . 10))) (defun test-pip ()  (dolist (shape '(square square-hole strange exagon))    (print shape)    (loop with polygon = (funcall shape)          for test-point across *test-points*          do (format t "~&~w ~:[outside~;inside ~]."                     test-point                     (point-in-polygon test-point polygon))))), USING: kernel prettyprint sequences arrays math math.vectors ;IN: raycasting : between ( a b x -- ? ) [ last ] tri@ [ < ] curry bi@ xor ; : lincomb ( a b x -- w )  3dup [ last ] tri@  [ - ] curry bi@  [ drop ] 2dip  neg 2dup + [ / ] curry bi@  [ [ v*n ] curry ] bi@ bi*  v+ ;: leftof ( a b x -- ? ) dup [ lincomb ] dip [ first ] bi@ > ; : ray ( a b x -- ? ) [ between ] [ leftof ] 3bi and ; : raycast ( poly x -- ? )  [ dup first suffix [ rest-slice ] [ but-last-slice ] bi ] dip  [ ray ] curry 2map  f [ xor ] reduce ;, ( scratchpad ) CONSTANT: square { { -2 -1 } { 1 -2 } { 2 1 } { -1 2 } }( scratchpad ) square { 0 0 } raycast .t( scratchpad ) square { 5 5 } raycast .f( scratchpad ) square { 2 0 } raycast .f, module Polygons  use Points_Module  implicit none   type polygon     type(point), dimension(:), allocatable :: points     integer, dimension(:), allocatable :: vertices  end type polygon contains   function create_polygon(pts, vt)    type(polygon) :: create_polygon    type(point), dimension(:), intent(in) :: pts    integer, dimension(:), intent(in) :: vt     integer :: np, nv     np = size(pts,1)    nv = size(vt,1)     allocate(create_polygon%points(np), create_polygon%vertices(nv))    create_polygon%points = pts    create_polygon%vertices = vt   end function create_polygon   subroutine free_polygon(pol)    type(polygon), intent(inout) :: pol     deallocate(pol%points, pol%vertices)   end subroutine free_polygon end module Polygons, module Ray_Casting_Algo  use Polygons  implicit none   real, parameter, private :: eps = 0.00001  private :: ray_intersects_seg contains   function ray_intersects_seg(p0, a0, b0) result(intersect)    type(point), intent(in) :: p0, a0, b0    logical :: intersect     type(point) :: a, b, p    real :: m_red, m_blue     p = p0    ! let variable "a" be the point with smallest y coordinate    if ( a0%y > b0%y ) then       b = a0       a = b0    else       a = a0       b = b0    end if     if ( (p%y == a%y) .or. (p%y == b%y) ) p%y = p%y + eps     intersect = .false.     if ( (p%y > b%y) .or. (p%y < a%y) ) return    if ( p%x > max(a%x, b%x) ) return     if ( p%x < min(a%x, b%x) ) then       intersect = .true.    else       if ( abs(a%x - b%x) > tiny(a%x) ) then          m_red = (b%y - a%y) / (b%x - a%x)       else          m_red = huge(m_red)       end if       if ( abs(a%x - p%x) > tiny(a%x) ) then          m_blue = (p%y - a%y) / (p%x - a%x)       else          m_blue = huge(m_blue)       end if       if ( m_blue >= m_red ) then          intersect = .true.       else          intersect = .false.       end if    end if   end function ray_intersects_seg   function point_is_inside(p, pol) result(inside)    logical :: inside    type(point), intent(in) :: p    type(polygon), intent(in) :: pol     integer :: i, cnt, pa, pb     cnt = 0    do i = lbound(pol%vertices,1), ubound(pol%vertices,1), 2       pa = pol%vertices(i)       pb = pol%vertices(i+1)       if ( ray_intersects_seg(p, pol%points(pa), pol%points(pb)) ) cnt = cnt + 1    end do     inside = .true.    if ( mod(cnt, 2) == 0 ) then       inside = .false.    end if   end function point_is_inside end module Ray_Casting_Algo, program Pointpoly  use Points_Module  use Ray_Casting_Algo  implicit none   character(len=16), dimension(4) :: names  type(polygon), dimension(4) :: polys  type(point), dimension(14) :: pts  type(point), dimension(7) :: p   integer :: i, j   pts = (/ point(0,0), point(10,0), point(10,10), point(0,10), &           point(2.5,2.5), point(7.5,2.5), point(7.5,7.5), point(2.5,7.5), &           point(0,5), point(10,5), &           point(3,0), point(7,0), point(7,10), point(3,10) /)   polys(1) = create_polygon(pts, (/ 1,2, 2,3, 3,4, 4,1 /) )  polys(2) = create_polygon(pts, (/ 1,2, 2,3, 3,4, 4,1, 5,6, 6,7, 7,8, 8,5 /) )  polys(3) = create_polygon(pts, (/ 1,5, 5,4, 4,8, 8,7, 7,3, 3,2, 2,5 /) )  polys(4) = create_polygon(pts, (/ 11,12, 12,10, 10,13, 13,14, 14,9, 9,11 /) )   names = (/ "square", "square hole", "strange", "exagon" /)   p = (/ point(5,5), point(5, 8), point(-10, 5), point(0,5), point(10,5), &         point(8,5), point(10,10) /)   do j = 1, size(p)     do i = 1, size(polys)        write(*, "('point (',F8.2,',',F8.2,') is inside ',A,'? ', L)") &             p(j)%x, p(j)%y, names(i), point_is_inside(p(j), polys(i))     end do     print *, ""  end do   do i = 1, size(polys)     call free_polygon(polys(i))  end do end program Pointpoly,   Type Point    As Single x,yEnd Type  Function inpolygon(p1() As Point,p2 As Point) As Integer    #macro isleft2(L,p)    -Sgn(  (L(1).x-L(2).x)*(p.y-L(2).y) - (p.x-L(2).x)*(L(1).y-L(2).y))    #endmacro    Dim As Integer index,nextindex    Dim k As Integer=Ubound(p1)+1    Dim send (1 To 2) As Point    Dim wn As Integer=0    For n As Integer=1 To Ubound(p1)        index=n Mod k:nextindex=(n+1) Mod k        If nextindex=0 Then nextindex=1        send(1).x=p1(index).x:send(2).x=p1(nextindex).x        send(1).y=p1(index).y:send(2).y=p1(nextindex).y        If p1(index).y<=p2.y Then            If p1(nextindex).y>p2.y Then                 If isleft2(send,p2)>=0 Then '=                    wn=wn+1                End If            End If        Else            If p1(nextindex).y<=p2.y Then                If isleft2(send,p2)<=0 Then'=                    wn=wn-1                End If            End If        End If    Next n    Return wnEnd Function  Dim As Point square(1 To 4)  ={(0,0),(10,0),(10,10),(0,10)} Dim As Point hole(1 To 4)    ={(2.5,2.5),(7.5,2.5),(7.5,7.5),(2.5,7.5)} Dim As Point strange(1 To 8) ={(0,0),(2.5,2.5),(0,10),(2.5,7.5),_                              (7.5,7.5),(10,10),(10,0),(2.5,2.5)} Dim As Point exagon(1 To 6)  ={(3,0),(7,0),(10,5),(7,10),(3,10),(0,5)}'printoutsFor z As Integer=1 To 4    Select Case z    Case 1: Print "squared"    Print "(5,5)  " ;Tab(12);    If inpolygon(square(),Type<Point>(5,5)) Then Print "in" Else Print "out"    Print "(5,8)  " ;Tab(12);    If inpolygon(square(),Type<Point>(5,8)) Then Print "in" Else Print "out"    Print "(-10,5)  " ;Tab(12);    If inpolygon(square(),Type<Point>(-10,5)) Then Print "in" Else Print "out"    Print "(0,5)  " ;Tab(12);    If inpolygon(square(),Type<Point>(0,5)) Then Print "in" Else Print "out"    Print "(10,5)  " ;Tab(12);    If inpolygon(square(),Type<Point>(10,5)) Then Print "in" Else Print "out"    Print "(8,5)  " ;Tab(12);    If inpolygon(square(),Type<Point>(8,5)) Then Print "in" Else Print "out"    Print "(10,10)  " ;Tab(12);    If inpolygon(square(),Type<Point>(10,10)) Then Print "in" Else Print "out"    PrintCase 2:Print "squared hole"Print "(5,5)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(5,5)) And inpolygon(square(),Type<Point>(5,5)) Then Print "in" Else Print "out"Print "(5,8)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(5,8)) And inpolygon(square(),Type<Point>(5,8))Then Print "in" Else Print "out"Print "(-10,5)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(-10,5))And inpolygon(square(),Type<Point>(-10,5)) Then Print "in" Else Print "out"Print "(0,5)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(0,5))And inpolygon(square(),Type<Point>(0,5)) Then Print "in" Else Print "out"Print "(10,5)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(10,5))And inpolygon(square(),Type<Point>(10,5)) Then Print "in" Else Print "out"Print "(8,5)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(8,5))And inpolygon(square(),Type<Point>(8,5)) Then Print "in" Else Print "out"Print "(10,10)  " ;Tab(12);If Not inpolygon(hole(),Type<Point>(10,10))And inpolygon(square(),Type<Point>(10,10)) Then Print "in" Else Print "out"PrintCase 3:Print "strange"Print "(5,5)  " ;Tab(12);If inpolygon(strange(),Type<Point>(5,5)) Then Print "in" Else Print "out"Print "(5,8)  " ;Tab(12);If inpolygon(strange(),Type<Point>(5,8)) Then Print "in" Else Print "out"Print "(-10,5)  " ;Tab(12);If inpolygon(strange(),Type<Point>(-10,5)) Then Print "in" Else Print "out"Print "(0,5)  " ;Tab(12);If inpolygon(strange(),Type<Point>(0,5)) Then Print "in" Else Print "out"Print "(10,5)  " ;Tab(12);If inpolygon(strange(),Type<Point>(10,5)) Then Print "in" Else Print "out"Print "(8,5)  " ;Tab(12);If inpolygon(strange(),Type<Point>(8,5)) Then Print "in" Else Print "out"Print "(10,10)  " ;Tab(12);If inpolygon(strange(),Type<Point>(10,10)) Then Print "in" Else Print "out"PrintCase 4:Print "exagon"Print "(5,5)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(5,5)) Then Print "in" Else Print "out"Print "(5,8)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(5,8)) Then Print "in" Else Print "out"Print "(-10,5)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(-10,5)) Then Print "in" Else Print "out"Print "(0,5)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(0,5)) Then Print "in" Else Print "out"Print "(10,5)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(10,5)) Then Print "in" Else Print "out"Print "(8,5)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(8,5)) Then Print "in" Else Print "out"Print "(10,10)  " ;Tab(12);If inpolygon(exagon(),Type<Point>(10,10)) Then Print "in" Else Print "out"PrintEnd SelectNext zsleep , 
squared
(5,5)      in
(5,8)      in
(-10,5)    out
(0,5)      out
(10,5)     in
(8,5)      in
(10,10)    out

squared hole
(5,5)      out
(5,8)      in
(-10,5)    out
(0,5)      out
(10,5)     in
(8,5)      in
(10,10)    out

strange
(5,5)      in
(5,8)      out
(-10,5)    out
(0,5)      out
(10,5)     in
(8,5)      in
(10,10)    out

exagon
(5,5)      in
(5,8)      in
(-10,5)    out
(0,5)      out
(10,5)     in
(8,5)      in
(10,10)    out
, package main import (    "math"    "fmt") type xy struct {    x, y float64} type seg struct {    p1, p2 xy} type poly struct {    name  string    sides []seg} func inside(pt xy, pg poly) (i bool) {    for _, side := range pg.sides {        if rayIntersectsSegment(pt, side) {            i = !i        }    }    return} func rayIntersectsSegment(p xy, s seg) bool {    var a, b xy    if s.p1.y < s.p2.y {        a, b = s.p1, s.p2    } else {        a, b = s.p2, s.p1    }    for p.y == a.y || p.y == b.y {        p.y = math.Nextafter(p.y, math.Inf(1))    }    if p.y < a.y || p.y > b.y {        return false    }    if a.x > b.x {        if p.x > a.x {            return false        }        if p.x < b.x {            return true        }    } else {        if p.x > b.x {            return false        }        if p.x < a.x {            return true        }    }    return (p.y-a.y)/(p.x-a.x) >= (b.y-a.y)/(b.x-a.x)} var (    p1  = xy{0, 0}    p2  = xy{10, 0}    p3  = xy{10, 10}    p4  = xy{0, 10}    p5  = xy{2.5, 2.5}    p6  = xy{7.5, 2.5}    p7  = xy{7.5, 7.5}    p8  = xy{2.5, 7.5}    p9  = xy{0, 5}    p10 = xy{10, 5}    p11 = xy{3, 0}    p12 = xy{7, 0}    p13 = xy{7, 10}    p14 = xy{3, 10}) var tpg = []poly{    {"square", []seg{{p1, p2}, {p2, p3}, {p3, p4}, {p4, p1}}},    {"square hole", []seg{{p1, p2}, {p2, p3}, {p3, p4}, {p4, p1},        {p5, p6}, {p6, p7}, {p7, p8}, {p8, p5}}},    {"strange", []seg{{p1, p5},        {p5, p4}, {p4, p8}, {p8, p7}, {p7, p3}, {p3, p2}, {p2, p5}}},    {"exagon", []seg{{p11, p12}, {p12, p10}, {p10, p13},        {p13, p14}, {p14, p9}, {p9, p11}}},} var tpt = []xy{{5, 5}, {5, 8}, {-10, 5}, {0, 5}, {10, 5}, {8, 5}, {10, 10}} func main() {    for _, pg := range tpg {        fmt.Printf("%s:\n", pg.name)        for _, pt := range tpt {            fmt.Println(pt, inside(pt, pg))        }    }}, 
square:
{5 5} true
{5 8} true
{-10 5} false
{0 5} false
{10 5} true
{8 5} true
{10 10} false
square hole:
{5 5} false
{5 8} true
{-10 5} false
{0 5} false
{10 5} true
{8 5} true
{10 10} false
strange:
{5 5} true
{5 8} false
{-10 5} false
{0 5} false
{10 5} true
{8 5} true
{10 10} false
exagon:
{5 5} true
{5 8} true
{-10 5} false
{0 5} false
{10 5} true
{8 5} true
{10 10} false
, package main import (    "math"    "fmt") type xy struct {    x, y float64} type closedPoly struct {    name string    vert []xy} func inside(pt xy, pg closedPoly) bool {    if len(pg.vert) < 3 {        return false    }    in := rayIntersectsSegment(pt, pg.vert[len(pg.vert)-1], pg.vert[0])    for i := 1; i < len(pg.vert); i++ {        if rayIntersectsSegment(pt, pg.vert[i-1], pg.vert[i]) {            in = !in        }    }    return in} func rayIntersectsSegment(p, a, b xy) bool {    if a.y > b.y {        a, b = b, a    }    for p.y == a.y || p.y == b.y {        p.y = math.Nextafter(p.y, math.Inf(1))    }    if p.y < a.y || p.y > b.y {        return false    }    if a.x > b.x {        if p.x > a.x {            return false        }        if p.x < b.x {            return true        }    } else {        if p.x > b.x {            return false        }        if p.x < a.x {            return true        }    }    return (p.y-a.y)/(p.x-a.x) >= (b.y-a.y)/(b.x-a.x)} var tpg = []closedPoly{    {"square", []xy{{0, 0}, {10, 0}, {10, 10}, {0, 10}}},    {"square hole", []xy{{0, 0}, {10, 0}, {10, 10}, {0, 10}, {0, 0},        {2.5, 2.5}, {7.5, 2.5}, {7.5, 7.5}, {2.5, 7.5}, {2.5, 2.5}}},    {"strange", []xy{{0, 0}, {2.5, 2.5}, {0, 10}, {2.5, 7.5}, {7.5, 7.5},        {10, 10}, {10, 0}, {2.5, 2.5}}},    {"exagon", []xy{{3, 0}, {7, 0}, {10, 5}, {7, 10}, {3, 10}, {0, 5}}},} var tpt = []xy{{1, 2}, {2, 1}} func main() {    for _, pg := range tpg {        fmt.Printf("%s:\n", pg.name)        for _, pt := range tpt {            fmt.Println(pt, inside(pt, pg))        }    }}, 
square:
{1 2} true
{2 1} true
square hole:
{1 2} true
{2 1} true
strange:
{1 2} false
{2 1} false
exagon:
{1 2} false
{2 1} false
, import Data.Ratio type Point = (Rational, Rational)type Polygon = [Point]data Line = Sloped {lineSlope, lineYIntercept :: Rational} |            Vert {lineXIntercept :: Rational} polygonSides :: Polygon -> [(Point, Point)]polygonSides poly@(p1 : ps) = zip poly $ ps ++ [p1] intersects :: Point -> Line -> Bool{- @intersects (px, py) l@ is true if the ray {(x, py) | x ≥ px}intersects l. -}intersects (px, _)  (Vert xint)  = px <= xintintersects (px, py) (Sloped m b) | m < 0     = py <= m * px + b                                 | otherwise = py >= m * px + b onLine :: Point -> Line -> Bool{- Is the point on the line? -}onLine (px, _)  (Vert xint)  = px == xintonLine (px, py) (Sloped m b) = py == m * px + b carrier :: (Point, Point) -> Line{- Finds the line containing the given line segment. -}carrier ((ax, ay), (bx, by)) | ax == bx  = Vert ax                             | otherwise = Sloped slope yint  where slope = (ay - by) / (ax - bx)        yint = ay - slope * ax between :: Ord a => a -> a -> a -> Boolbetween x a b | a > b     = b <= x && x <= a              | otherwise = a <= x && x <= b inPolygon :: Point -> Polygon -> BoolinPolygon p@(px, py) = f 0 . polygonSides  where f n []                             = odd n        f n (side : sides) | far           = f n       sides                           | onSegment     = True                           | rayIntersects = f (n + 1) sides                           | otherwise     = f n       sides          where far = not $ between py ay by                onSegment | ay == by  = between px ax bx                          | otherwise = p `onLine` line                rayIntersects =                    intersects p line &&                    (py /= ay || by < py) &&                    (py /= by || ay < py)                ((ax, ay), (bx, by)) = side                line = carrier side, NB.*crossPnP v point in closed polygon, crossing numberNB.  bool=. points crossPnP polygoncrossPnP=: 4 : 0"2  'X Y'=. |:x  'x0 y0 x1 y1'=. |:2 ,/\^:(2={:@$@]) y  p1=. ((y0<:/Y)*. y1>/Y) +. (y0>/Y)*. y1<:/Y  p2=. (x0-/X) < (x0-x1) * (y0-/Y) % (y0 - y1)  2|+/ p1*.p2), SQUAREV=:          0   0   , 10  0   , 10  10  ,: 0   10SQUAREV=: SQUAREV, 2.5 2.5 , 7.5 0.1 , 7.5 7.5 ,: 2.5 7.5 ESAV=: 3 0 , 7 0 , 10 5 , 7 10 , 3 10 ,: 0 5 ESA=:        (0 1,1 2,2 3,3 4,4 5,:5 0) , .{ ESAVSQUARE=:     (0 1,1 2,2 3,:3 0)         , .{ SQUAREVSQUAREHOLE=: (0 1,1 2,2 3,3 0,4 5,5 6,6 7,:7 4) , .{ SQUAREVSTRANGE=:    (0 4,4 3,3 7,7 6,6 2,2 1,1 5,:5 0) , .{ SQUAREV POINTS=: 5 5,5 8,2 2,0 0,10 10,2.5 2.5,0.01 5,2.2 7.4,0 5,10 5,:_4 10,    (<POINTS) crossPnP every ESA;SQUARE;SQUAREHOLE;STRANGE1 1 1 0 0 1 1 1 0 1 01 1 1 0 0 1 1 1 0 1 00 1 1 0 0 1 1 1 0 1 01 0 0 0 0 0 0 1 0 1 0, NoMainWinGlobal sw, sh, verts sw = 640 :   sh = 480WindowWidth  = sw+8 : WindowHeight = sh+31UpperLeftX = (DisplayWidth -sw)/2UpperLeftY = (DisplayHeight-sh)/2Open"Ray Casting Algorithm" For Graphics_nf_nsb As #g#g "Down; TrapClose [halt]"h$ = "#g" Dim xp(15),yp(15)#g "when leftButtonDown [halt];when mouseMove checkPoint"#g "when rightButtonDown [Repeat]" [Repeat]    #g "Cls;Fill 32 160 255; Color white;BackColor 32 160 255"    #g "Place 5 460;\L-click to exit"    #g "Place 485 460;\R-click for new polygon"     'generate polygon from random points    numPoints =  rand(4,15)    verts = numPoints    For i = 0 To numPoints-1        xp(i) = rand(20,620)        yp(i) = rand(40,420)    Next    Call drawPoly h$, verts, "white"    #g "Flush"    Wait [halt]Close #gEnd 'Point In Polygon FunctionFunction pnp(x, y, numSides)    j= numSides-1: oddNodes = 0    For i = 0 To numSides-1        If ((yp(i)<y) And (yp(j)>=y)) Or ((yp(j)<y) And (yp(i)>=y)) Then            f1 = y - yp(i):f2 = yp(j) - yp(i): f3 = xp(j) - xp(i)            If (xp(i) + f1 / f2 * f3) < x Then oddNodes = 1 - oddNodes        End If        j = i    Next    pnp = oddNodesEnd Function 'draw the polygonSub drawPoly h$, verts, colour$    #h$, "Color ";colour$    j = verts-1    For i = 0 To verts-1        #h$ "Line ";xp(j);" ";yp(j);" ";xp(i);" ";yp(i)        j = i    NextEnd Sub 'change message and color of polygonSub checkPoint h$, x, y    If pnp(x,y,verts) Then        #h$ "Color 32 160 255;BackColor 32 160 255"        #h$ "Place 5 0;BoxFilled 150 20;Color white"        #h$ "Place 7 15;\Mouse In Polygon"        Call drawPoly h$, verts, "red"    Else        #h$ "Color 32 160 255;BackColor 32 160 255"        #h$ "Place 5 0;BoxFilled 150 20;Color white"        #h$ "Place 7 15;\Mouse Not In Polygon"        Call drawPoly h$, verts, "white"    End IfEnd Sub Function rand(loNum,hiNum)    rand = Int(Rnd(0)*(hiNum-loNum+1)+loNum)End Function , type point = { x:float; y:float } type polygon = {  vertices: point array;  edges: (int * int) list;} let p x y = { x=x; y=y } let square_v = [|  (p 0. 0.); (p 10. 0.); (p 10. 10.); (p 0. 10.);  (p 2.5 2.5); (p 7.5 0.1); (p 7.5 7.5); (p 2.5 7.5)|] let esa_v = [|  (p 3. 0.); (p 7. 0.); (p 10. 5.); (p 7. 10.); (p 3. 10.); (p 0. 5.)|] let esa = {  vertices = esa_v;  edges = [ (0,1); (1,2); (2,3); (3,4); (4,5); (5,0) ]} let square = {  vertices = square_v;  edges = [ (0,1); (1,2); (2,3); (3,0) ]} let squarehole = {  vertices = square_v;  edges = [ (0,1); (1,2); (2,3); (3,0); (4,5); (5,6); (6,7); (7,4) ]} let strange = {  vertices = square_v;  edges = [ (0,4); (4,3); (3,7); (7,6); (6,2); (2,1); (1,5); (5,0) ]}  let min_y ~a ~b = if a.y > b.y then (b) else (a) let coeff_ang ~pa ~pb = (pb.y -. pa.y) /. (pb.x -. pa.x) let huge_val = infinity let hseg_intersect_seg ~s ~a ~b =  let _eps =    if s.y = (max a.y b.y) ||       s.y = (min a.y b.y) then 0.00001 else 0.0  in  if  (s.y +. _eps) > (max a.y b.y) ||      (s.y +. _eps) < (min a.y b.y) ||       s.x > (max a.x b.x) then (false)  else if s.x <= (min a.x b.x) then (true)  else    let ca = if a.x <> b.x then (coeff_ang a b) else (huge_val) in    let my = min_y ~a ~b in    let cp = if (s.x -. my.x) <> 0.0 then (coeff_ang my s) else (huge_val) in    (cp >= ca);;  let point_is_inside ~poly ~pt =  let cross = ref 0 in  List.iter (fun (a,b) ->    if hseg_intersect_seg pt             poly.vertices.(a)             poly.vertices.(b)    then incr cross  ) poly.edges;  ( (!cross mod 2) <> 0);;  let make_test p label s =  Printf.printf "point (%.5f,%.5f) is " p.x p.y;  print_string (if point_is_inside s p                then "INSIDE "                else "OUTSIDE ");  print_endline label;;;  let () =  let test_points = [    (p 5. 5.); (p 5. 8.); (p 2. 2.); (p 0. 0.);    (p 10. 10.); (p 2.5 2.5); (p 0.01 5.);    (p 2.2 7.4); (p 0. 5.); (p 10. 5.); (p (-4.) 10.) ] in   List.iter (fun p ->    make_test p "square"     square;    make_test p "squarehole" squarehole;    make_test p "strange"    strange;    make_test p "esa"        esa;    print_newline()  ) test_points;;;, use strict;use List::Util qw(max min); sub point_in_polygon{    my ( $point, $polygon ) = @_;     my $count = 0;    foreach my $side ( @$polygon ) {	$count++ if ray_intersect_segment($point, $side);    }    return ($count % 2 == 0) ? 0 : 1;}  my $eps = 0.0001;my $inf = 1e600; sub ray_intersect_segment{    my ($point, $segment) = @_;     my ($A, $B) = @$segment;     my @P = @$point; # copy it     ($A, $B) = ($B, $A) if $A->[1] > $B->[1];     $P[1] += $eps if ($P[1] == $A->[1]) || ($P[1] == $B->[1]);     return 0 if ($P[1] < $A->[1]) || ( $P[1] > $B->[1]) || ($P[0] > max($A->[0],$B->[1]) );    return 1 if $P[0] < min($A->[0], $B->[0]);     my $m_red = ($A->[0] != $B->[0]) ? ( $B->[1] - $A->[1] )/($B->[0] - $A->[0]) : $inf;    my $m_blue = ($A->[0] != $P[0]) ? ( $P[1] - $A->[1] )/($P[0] - $A->[0]) : $inf;     return ($m_blue >= $m_red) ? 1 : 0;}, # the following are utilities to use the same Fortran data...sub point{    [shift, shift];}sub create_polygon{    my ($pts, $sides) = @_;    my @poly;    for(my $i = 0; $i < $#$sides; $i += 2) {	push @poly, [ $pts->[$sides->[$i]-1], $pts->[$sides->[$i+1]-1] ];    }    @poly;} my @pts = ( point(0,0), point(10,0), point(10,10), point(0,10), 	    point(2.5,2.5), point(7.5,2.5), point(7.5,7.5), point(2.5,7.5), 	    point(0,5), point(10,5), 	    point(3,0), point(7,0), point(7,10), point(3,10) ); my @squared = create_polygon(\@pts, [ 1,2, 2,3, 3,4, 4,1 ] );my @squaredhole = create_polygon(\@pts, [ 1,2, 2,3, 3,4, 4,1, 5,6, 6,7, 7,8, 8,5 ] );my @strange = create_polygon(\@pts, [ 1,5, 5,4, 4,8, 8,7, 7,3, 3,2, 2,5 ] );my @exagon = create_polygon(\@pts, [ 11,12, 12,10, 10,13, 13,14, 14,9, 9,11 ]) ; my @p = ( point(5,5), point(5, 8), point(-10, 5), point(0,5), point(10,5), &	  point(8,5), point(10,10) ); foreach my $pol ( qw(squared squaredhole strange exagon) ) {    no strict 'refs';    print "$pol\n";    my @rp = @{$pol};    foreach my $tp ( @p ) {	print "\t($tp->[0],$tp->[1]) " .            ( point_in_polygon($tp, \@rp) ? "INSIDE" : "OUTSIDE" ) . "\n";    }}, constant ε = 0.0001; sub ray-hits-seg([\Px,\Py], [[\Ax,\Ay], [\Bx,\By]] --> Bool) {    Py += ε if Py == Ay | By;     if Py < Ay or Py > By or Px > (Ax max Bx) {	False;    }    elsif Px < (Ax min Bx) {	True;    }    else {	my \red  = Ax == Bx ?? Inf !! (By - Ay) / (Bx - Ax);	my \blue = Ax == Px ?? Inf !! (Py - Ay) / (Px - Ax);	blue >= red;    }} sub point-in-poly(@point, @polygon --> Bool) {    so 2 R% [+] gather for @polygon -> @side {	take ray-hits-seg @point, @side.sort(*.[1]);    }} my %poly =    squared => 	 [[[ 0.0,  0.0], [10.0,  0.0]],	  [[10.0,  0.0], [10.0, 10.0]],	  [[10.0, 10.0], [ 0.0, 10.0]],	  [[ 0.0, 10.0], [ 0.0,  0.0]]],    squaredhole =>	 [[[ 0.0,  0.0], [10.0,  0.0]],	  [[10.0,  0.0], [10.0, 10.0]],	  [[10.0, 10.0], [ 0.0, 10.0]],	  [[ 0.0, 10.0], [ 0.0,  0.0]],	  [[ 2.5,  2.5], [ 7.5,  2.5]],	  [[ 7.5,  2.5], [ 7.5,  7.5]],	  [[ 7.5,  7.5], [ 2.5,  7.5]],	  [[ 2.5,  7.5], [ 2.5,  2.5]]],    strange =>	 [[[ 0.0,  0.0], [ 2.5,  2.5]],	  [[ 2.5,  2.5], [ 0.0, 10.0]],	  [[ 0.0, 10.0], [ 2.5,  7.5]],	  [[ 2.5,  7.5], [ 7.5,  7.5]],	  [[ 7.5,  7.5], [10.0, 10.0]],	  [[10.0, 10.0], [10.0,  0.0]],	  [[10.0,  0.0], [ 2.5,  2.5]],	  [[ 2.5,  2.5], [ 0.0,  0.0]]],  # conjecturally close polygon    exagon =>	 [[[ 3.0,  0.0], [ 7.0,  0.0]],	  [[ 7.0,  0.0], [10.0,  5.0]],	  [[10.0,  5.0], [ 7.0, 10.0]],	  [[ 7.0, 10.0], [ 3.0, 10.0]],	  [[ 3.0, 10.0], [ 0.0,  5.0]],	  [[ 0.0,  5.0], [ 3.0,  0.0]]]; my @test-points =	  [  5.0,  5.0],	  [  5.0,  8.0],	  [-10.0,  5.0],	  [  0.0,  5.0],	  [ 10.0,  5.0],	  [  8.0,  5.0],	  [ 10.0, 10.0]; for <squared squaredhole strange exagon> -> $polywanna {    say "$polywanna";    my @poly = %poly{$polywanna}[];    for @test-points -> @point {	say "\t(@point.fmt('%.1f',','))\t{ point-in-poly(@point, @poly) ?? 'IN' !! 'OUT' }";    }}, squared
	(5.0,5.0)	IN
	(5.0,8.0)	IN
	(-10.0,5.0)	OUT
	(0.0,5.0)	OUT
	(10.0,5.0)	IN
	(8.0,5.0)	IN
	(10.0,10.0)	OUT
squaredhole
	(5.0,5.0)	OUT
	(5.0,8.0)	IN
	(-10.0,5.0)	OUT
	(0.0,5.0)	OUT
	(10.0,5.0)	IN
	(8.0,5.0)	IN
	(10.0,10.0)	OUT
strange
	(5.0,5.0)	IN
	(5.0,8.0)	OUT
	(-10.0,5.0)	OUT
	(0.0,5.0)	OUT
	(10.0,5.0)	IN
	(8.0,5.0)	IN
	(10.0,10.0)	OUT
exagon
	(5.0,5.0)	IN
	(5.0,8.0)	IN
	(-10.0,5.0)	OUT
	(0.0,5.0)	OUT
	(10.0,5.0)	IN
	(8.0,5.0)	IN
	(10.0,10.0)	OUT, (scl 4) (de intersects (Px Py Ax Ay Bx By)   (when (> Ay By)      (xchg 'Ax 'Bx)      (xchg 'Ay 'By) )   (when (or (= Py Ay) (= Py By))      (inc 'Py) )   (and      (>= Py Ay)      (>= By Py)      (>= (max Ax Bx) Px)      (or         (> (min Ax Bx) Px)         (= Ax Px)         (and            (<> Ax Bx)            (>=               (*/ (- Py Ay) 1.0 (- Px Ax))            # Blue               (*/ (- By Ay) 1.0 (- Bx Ax)) ) ) ) ) )  # Red (de inside (Pt Poly)   (let Res NIL      (for Edge Poly         (when (apply intersects Edge (car Pt) (cdr Pt))            (onOff Res) ) )      Res ) ), (de Square
   ( 0.0  0.0  10.0  0.0)
   (10.0  0.0  10.0 10.0)
   (10.0 10.0   0.0 10.0)
   ( 0.0 10.0   0.0  0.0) )

(de SquareHole
   ( 0.0  0.0  10.0  0.0)
   (10.0  0.0  10.0 10.0)
   (10.0 10.0   0.0 10.0)
   ( 0.0 10.0   0.0  0.0)
   ( 2.5  2.5   7.5  2.5)
   ( 7.5  2.5   7.5  7.5)
   ( 7.5  7.5   2.5  7.5)
   ( 2.5  7.5   2.5  2.5) )

(de Strange
   ( 0.0  0.0   2.5  2.5)
   ( 2.5  2.5   0.0 10.0)
   ( 0.0 10.0   2.5  7.5)
   ( 2.5  7.5   7.5  7.5)
   ( 7.5  7.5  10.0 10.0)
   (10.0 10.0  10.0  0.0)
   (10.0  0.0   2.5  2.5) )

(de Exagon
   ( 3.0  0.0   7.0  0.0)
   ( 7.0  0.0  10.0  5.0)
   (10.0  5.0   7.0 10.0)
   ( 7.0 10.0   3.0 10.0)
   ( 3.0 10.0   0.0  5.0)
   ( 0.0  5.0   3.0  0.0) ), : (inside (5.0 . 5.0) Square)
-> T
: (inside (5.0 . 8.0) Square)
-> T
: (inside (-10.0 . 5.0) Square)
-> NIL
: (inside (0.0 . 5.0) Square)
-> NIL
: (inside (10.0 . 5.0) Square)
-> T
: (inside (8.0 . 5.0) Square)
-> T
: (inside (10.0 . 10.0) Square)
-> NIL

: (inside (5.0 . 5.0) SquareHole)
-> NIL
: (inside (5.0 . 8.0) SquareHole)
-> T
: (inside (-10.0 . 5.0) SquareHole)
-> NIL
: (inside (0 . 5.0) SquareHole)
-> NIL
: (inside (10.0 . 5.0) SquareHole)
-> T
: (inside (8.0 . 5.0) SquareHole)
-> T
: (inside (10.0 . 10.0) SquareHole)
-> NIL

: (inside (5.0 . 5.0) Strange)
-> T
: (inside (5.0 . 8.0) Strange)
-> NIL
: (inside (-10.0 . 5.0) Strange)
-> NIL
: (inside (0 . 5.0) Strange)
-> NIL
: (inside (10.0 . 5.0) Strange)
-> T
: (inside (8.0 . 5.0) Strange)
-> T
: (inside (10.0 . 10.0) Strange)
-> NIL

: (inside (5.0 . 5.0) Exagon)
-> T
: (inside (5.0 . 8.0) Exagon)
-> T
: (inside (-10.0 . 5.0) Exagon)
-> NIL
: (inside (0.0 . 5.0) Exagon)
-> NIL
: (inside (10.0 . 5.0) Exagon)
-> T
: (inside (8.0 . 5.0) Exagon)
-> T
: (inside (10.0 . 10.0) Exagon)
-> NIL, Structure point_f  x.f  y.fEndStructureProcedure inpoly(*p.point_f, List poly.point_f())  Protected.point_f new, old, lp, rp  Protected inside  If ListSize(poly()) < 3: ProcedureReturn 0: EndIf   LastElement(poly()): old = poly()  ForEach poly()    ;find leftmost endpoint 'lp' and the rightmost endpoint 'rp' based on x value    If poly()\x > old\x       lp = old      rp = poly()    Else      lp = poly()      rp = old    EndIf     If lp\x < *p\x And *p\x <= rp\x And (*p\y - lp\y) * (rp\x - lp\x) < (rp\y - lp\y) * (*p\x - lp\x)      inside = ~inside    EndIf     old = poly()  Next   ProcedureReturn inside & 1EndProcedure If InitSprite()  If InitKeyboard() And InitMouse()    OpenWindow(0, 0, 0, 800, 600, "Press [Esc] to close, [Left mouse button] Add Point, [Right mouse button] Clear All Points.", #PB_Window_ScreenCentered | #PB_Window_SystemMenu)    OpenWindowedScreen(WindowID(0), 0, 0, 800, 600, 1, 0, 0)    SetFrameRate(60)  EndIfElse  MessageRequester("", "Unable to initsprite"): EndEndIf NewList v.point_f()Define.point_f pvp, mpDefine Col, EventID, mode.b, modetxt.sRepeat  Delay(1)  EventID = WindowEvent()  ExamineKeyboard()  ExamineMouse()  ClearScreen(Col)   mp\x = MouseX()  mp\y = MouseY()  If MouseButton(#PB_MouseButton_Left)    AddElement(v())    v()\x = mp\x    v()\y = mp\y    Delay(100)  EndIf   If MouseButton(#PB_MouseButton_Right)    ClearList(v())    Delay(100)  EndIf   StartDrawing(ScreenOutput())    If LastElement(v())      pvp = v()      ForEach v()        LineXY(pvp\x, pvp\y, v()\x, v()\y, RGB(0, $FF, 0)) ;Green        Circle(pvp\x, pvp\y, 5, RGB($FF, 0, 0)) ;Red        pvp = v()      Next    EndIf     Circle(MouseX(), MouseY(), 5, RGB($C0, $C0, $FF)) ;LightBlue      If inpoly(mp, v())      modetxt = "You are in the polygon."      Col = RGB(0, 0, 0)    Else      modetxt = "You are not in the polygon."      Col = RGB($50, $50, $50)    EndIf    DrawText((800 - TextWidth(modetxt)) / 2, 0, modetxt)   StopDrawing()   FlipBuffers()Until KeyboardReleased(#PB_Key_Escape) Or EventID = #PB_Event_CloseWindow, from collections import namedtuplefrom pprint import pprint as ppimport sys Pt = namedtuple('Pt', 'x, y')               # PointEdge = namedtuple('Edge', 'a, b')           # Polygon edge from a to bPoly = namedtuple('Poly', 'name, edges')    # Polygon _eps = 0.00001_huge = sys.float_info.max_tiny = sys.float_info.min def rayintersectseg(p, edge):    ''' takes a point p=Pt() and an edge of two endpoints a,b=Pt() of a line segment returns boolean    '''    a,b = edge    if a.y > b.y:        a,b = b,a    if p.y == a.y or p.y == b.y:        p = Pt(p.x, p.y + _eps)     intersect = False     if (p.y > b.y or p.y < a.y) or (        p.x > max(a.x, b.x)):        return False     if p.x < min(a.x, b.x):        intersect = True    else:        if abs(a.x - b.x) > _tiny:            m_red = (b.y - a.y) / float(b.x - a.x)        else:            m_red = _huge        if abs(a.x - p.x) > _tiny:            m_blue = (p.y - a.y) / float(p.x - a.x)        else:            m_blue = _huge        intersect = m_blue >= m_red    return intersect def _odd(x): return x%2 == 1 def ispointinside(p, poly):    ln = len(poly)    return _odd(sum(rayintersectseg(p, edge)                    for edge in poly.edges )) def polypp(poly):    print "\n  Polygon(name='%s', edges=(" % poly.name    print '   ', ',\n    '.join(str(e) for e in poly.edges) + '\n    ))' if __name__ == '__main__':    polys = [      Poly(name='square', edges=(        Edge(a=Pt(x=0, y=0), b=Pt(x=10, y=0)),        Edge(a=Pt(x=10, y=0), b=Pt(x=10, y=10)),        Edge(a=Pt(x=10, y=10), b=Pt(x=0, y=10)),        Edge(a=Pt(x=0, y=10), b=Pt(x=0, y=0))        )),      Poly(name='square_hole', edges=(        Edge(a=Pt(x=0, y=0), b=Pt(x=10, y=0)),        Edge(a=Pt(x=10, y=0), b=Pt(x=10, y=10)),        Edge(a=Pt(x=10, y=10), b=Pt(x=0, y=10)),        Edge(a=Pt(x=0, y=10), b=Pt(x=0, y=0)),        Edge(a=Pt(x=2.5, y=2.5), b=Pt(x=7.5, y=2.5)),        Edge(a=Pt(x=7.5, y=2.5), b=Pt(x=7.5, y=7.5)),        Edge(a=Pt(x=7.5, y=7.5), b=Pt(x=2.5, y=7.5)),        Edge(a=Pt(x=2.5, y=7.5), b=Pt(x=2.5, y=2.5))        )),      Poly(name='strange', edges=(        Edge(a=Pt(x=0, y=0), b=Pt(x=2.5, y=2.5)),        Edge(a=Pt(x=2.5, y=2.5), b=Pt(x=0, y=10)),        Edge(a=Pt(x=0, y=10), b=Pt(x=2.5, y=7.5)),        Edge(a=Pt(x=2.5, y=7.5), b=Pt(x=7.5, y=7.5)),        Edge(a=Pt(x=7.5, y=7.5), b=Pt(x=10, y=10)),        Edge(a=Pt(x=10, y=10), b=Pt(x=10, y=0)),        Edge(a=Pt(x=10, y=0), b=Pt(x=2.5, y=2.5))        )),      Poly(name='exagon', edges=(        Edge(a=Pt(x=3, y=0), b=Pt(x=7, y=0)),        Edge(a=Pt(x=7, y=0), b=Pt(x=10, y=5)),        Edge(a=Pt(x=10, y=5), b=Pt(x=7, y=10)),        Edge(a=Pt(x=7, y=10), b=Pt(x=3, y=10)),        Edge(a=Pt(x=3, y=10), b=Pt(x=0, y=5)),        Edge(a=Pt(x=0, y=5), b=Pt(x=3, y=0))        )),      ]    testpoints = (Pt(x=5, y=5), Pt(x=5, y=8),                  Pt(x=-10, y=5), Pt(x=0, y=5),                  Pt(x=10, y=5), Pt(x=8, y=5),                  Pt(x=10, y=10))     print "\n TESTING WHETHER POINTS ARE WITHIN POLYGONS"    for poly in polys:        polypp(poly)        print '   ', '\t'.join("%s: %s" % (p, ispointinside(p, poly))                               for p in testpoints[:3])        print '   ', '\t'.join("%s: %s" % (p, ispointinside(p, poly))                               for p in testpoints[3:6])        print '   ', '\t'.join("%s: %s" % (p, ispointinside(p, poly))                               for p in testpoints[6:]), 
 TESTING WHETHER POINTS ARE WITHIN POLYGONS

  Polygon(name='square', edges=(
    Edge(a=Pt(x=0, y=0), b=Pt(x=10, y=0)),
    Edge(a=Pt(x=10, y=0), b=Pt(x=10, y=10)),
    Edge(a=Pt(x=10, y=10), b=Pt(x=0, y=10)),
    Edge(a=Pt(x=0, y=10), b=Pt(x=0, y=0))
    ))
    Pt(x=5, y=5): True	Pt(x=5, y=8): True	Pt(x=-10, y=5): False
    Pt(x=0, y=5): False	Pt(x=10, y=5): True	Pt(x=8, y=5): True
    Pt(x=10, y=10): False

  Polygon(name='square_hole', edges=(
    Edge(a=Pt(x=0, y=0), b=Pt(x=10, y=0)),
    Edge(a=Pt(x=10, y=0), b=Pt(x=10, y=10)),
    Edge(a=Pt(x=10, y=10), b=Pt(x=0, y=10)),
    Edge(a=Pt(x=0, y=10), b=Pt(x=0, y=0)),
    Edge(a=Pt(x=2.5, y=2.5), b=Pt(x=7.5, y=2.5)),
    Edge(a=Pt(x=7.5, y=2.5), b=Pt(x=7.5, y=7.5)),
    Edge(a=Pt(x=7.5, y=7.5), b=Pt(x=2.5, y=7.5)),
    Edge(a=Pt(x=2.5, y=7.5), b=Pt(x=2.5, y=2.5))
    ))
    Pt(x=5, y=5): False	Pt(x=5, y=8): True	Pt(x=-10, y=5): False
    Pt(x=0, y=5): False	Pt(x=10, y=5): True	Pt(x=8, y=5): True
    Pt(x=10, y=10): False

  Polygon(name='strange', edges=(
    Edge(a=Pt(x=0, y=0), b=Pt(x=2.5, y=2.5)),
    Edge(a=Pt(x=2.5, y=2.5), b=Pt(x=0, y=10)),
    Edge(a=Pt(x=0, y=10), b=Pt(x=2.5, y=7.5)),
    Edge(a=Pt(x=2.5, y=7.5), b=Pt(x=7.5, y=7.5)),
    Edge(a=Pt(x=7.5, y=7.5), b=Pt(x=10, y=10)),
    Edge(a=Pt(x=10, y=10), b=Pt(x=10, y=0)),
    Edge(a=Pt(x=10, y=0), b=Pt(x=2.5, y=2.5))
    ))
    Pt(x=5, y=5): True	Pt(x=5, y=8): False	Pt(x=-10, y=5): False
    Pt(x=0, y=5): False	Pt(x=10, y=5): True	Pt(x=8, y=5): True
    Pt(x=10, y=10): False

  Polygon(name='exagon', edges=(
    Edge(a=Pt(x=3, y=0), b=Pt(x=7, y=0)),
    Edge(a=Pt(x=7, y=0), b=Pt(x=10, y=5)),
    Edge(a=Pt(x=10, y=5), b=Pt(x=7, y=10)),
    Edge(a=Pt(x=7, y=10), b=Pt(x=3, y=10)),
    Edge(a=Pt(x=3, y=10), b=Pt(x=0, y=5)),
    Edge(a=Pt(x=0, y=5), b=Pt(x=3, y=0))
    ))
    Pt(x=5, y=5): True	Pt(x=5, y=8): True	Pt(x=-10, y=5): False
    Pt(x=0, y=5): False	Pt(x=10, y=5): True	Pt(x=8, y=5): True
    Pt(x=10, y=10): False, def _convert_fortran_shapes():    point = Pt    pts = (point(0,0), point(10,0), point(10,10), point(0,10),            point(2.5,2.5), point(7.5,2.5), point(7.5,7.5), point(2.5,7.5),            point(0,5), point(10,5),            point(3,0), point(7,0), point(7,10), point(3,10))    p = (point(5,5), point(5, 8), point(-10, 5), point(0,5), point(10,5),         point(8,5), point(10,10) )     def create_polygon(pts,vertexindex):        return [tuple(Edge(pts[vertexindex[i]-1], pts[vertexindex[i+1]-1])                       for i in range(0, len(vertexindex), 2) )]    polys=[]    polys += create_polygon(pts, ( 1,2, 2,3, 3,4, 4,1 ) )    polys += create_polygon(pts, ( 1,2, 2,3, 3,4, 4,1, 5,6, 6,7, 7,8, 8,5 ) )    polys += create_polygon(pts, ( 1,5, 5,4, 4,8, 8,7, 7,3, 3,2, 2,5 ) )    polys += create_polygon(pts, ( 11,12, 12,10, 10,13, 13,14, 14,9, 9,11 ) )     names = ( "square", "square_hole", "strange", "exagon" )    polys = [Poly(name, edges)             for name, edges in zip(names, polys)]    print 'polys = ['    for p in polys:        print "  Poly(name='%s', edges=(" % p.name        print '   ', ',\n    '.join(str(e) for e in p.edges) + '\n    )),'    print '  ]' _convert_fortran_shapes(), point_in_polygon <- function(polygon, p) {  count <- 0  for(side in polygon) {    if ( ray_intersect_segment(p, side) ) {      count <- count + 1    }  }  if ( count %% 2 == 1 )    "INSIDE"  else    "OUTSIDE"} ray_intersect_segment <- function(p, side) {  eps <- 0.0001  a <- side$A  b <- side$B  if ( a$y > b$y ) {    a <- side$B    b <- side$A  }  if ( (p$y == a$y) || (p$y == b$y) ) {    p$y <- p$y + eps  }  if ( (p$y < a$y) || (p$y > b$y) )    return(FALSE)  else if ( p$x > max(a$x, b$x) )    return(FALSE)  else {    if ( p$x < min(a$x, b$x) )      return(TRUE)    else {      if ( a$x != b$x )        m_red <- (b$y - a$y) / (b$x - a$x)      else        m_red <- Inf      if ( a$x != p$x )        m_blue <- (p$y - a$y) / (p$x - a$x)      else        m_blue <- Inf      return( m_blue >= m_red )    }  }}, ######## utility functions ######### point <- function(x,y) list(x=x, y=y) # pts = list(p1, p2, ... )... coords# segs = list(c(1,2), c(2,1) ...) indicescreatePolygon <- function(pts, segs) {  pol <- list()  for(pseg in segs) {    pol <- c(pol, list(list(A=pts[[pseg[1]]], B=pts[[pseg[2]]])))  }  pol}, #### testing #### pts <- list(point(0,0), point(10,0), point(10,10), point(0,10),            point(2.5,2.5), point(7.5,2.5), point(7.5,7.5), point(2.5,7.5),             point(0,5), point(10,5),             point(3,0), point(7,0), point(7,10), point(3,10)) polygons <-  list(       square = createPolygon(pts, list(c(1,2), c(2,3), c(3,4), c(4,1))),       squarehole = createPolygon(pts, list(c(1,2), c(2,3), c(3,4), c(4,1), c(5,6), c(6,7), c(7,8), c(8,5))),       exagon = createPolygon(pts, list(c(11,12), c(12,10), c(10,13), c(13,14), c(14,9), c(9,11)))      ) testpoints <-  list(       point(5,5), point(5, 8), point(-10, 5), point(0,5), point(10,5),       point(8,5), point(9.9,9.9)      ) for(p in testpoints) {  for(polysi in 1:length(polygons)) {    cat(sprintf("point (%lf, %lf) is %s polygon (%s)\n",                  p$x, p$y, point_in_polygon(polygons[[polysi]], p), names(polygons[polysi])))  }},  #lang racket (module pip racket  (require racket/contract)   (provide point)  (provide seg)  (provide (contract-out [point-in-polygon? (->                                              point?                                              list?                                              boolean?)]))   (struct point (x y) #:transparent)  (struct seg (Ax Ay Bx By))  (define ε 0.000001)  (define (neq? x y) (not (eq? x y)))   (define (ray-cross-seg? r s)    (let* ([Ax (seg-Ax s)] [Ay (seg-Ay s)]           [Bx (seg-Bx s)] [By (seg-By s)]           [Px (point-x r)] [Pyo (point-y r)]           [Py (+ Pyo (if (or (eq? Pyo Ay)                               (eq? Pyo By))                           ε 0))])       (cond [(or (< Py Ay) (> Py By)) #f]            [(> Px (max Ax Bx)) #f]            [(< Px (min Ax Bx)) #t]            [else             (let ([red (if (neq? Ax Px)                            (/ (- By Ay) (- Bx Ax))                            +inf.0)]                   [blue (if (neq? Ax Px)                             (/ (- Py Ax) (- Px Ax))                             +inf.0)])               (if (>= blue red) #t #f))])))   (define (point-in-polygon? point polygon)    (odd?      (for/fold ([c 0]) ([seg polygon])       (+ c (if (ray-cross-seg? point seg) 1 0)))))) (require 'pip) (define test-point-list  (list   (point 5.0    5.0)    (point 5.0    8.0)    (point -10.0  5.0)    (point  0.0   5.0)    (point 10.0   5.0)    (point  8.0   5.0)    (point 10.0  10.0))) (define square  (list (seg 0.0   0.0  10.0   0.0)         (seg 10.0  0.0  10.0  10.0)         (seg 10.0  10.0  0.0  10.0)         (seg 0.0   0.0  0.0   10.0))) (define exagon  (list (seg  3.0   0.0   7.0   0.0)         (seg  7.0   0.0  10.0   5.0)         (seg 10.0   5.0   7.0  10.0)         (seg  7.0  10.0   3.0  10.0)         (seg  0.0   5.0   3.0   10.0)         (seg  3.0   0.0 0.0   5.0))) (define (test-figure fig name)  (printf "\ntesting ~a: \n" name)  (for ([p test-point-list])    (printf "testing ~v: ~a\n"  p (point-in-polygon? p fig)))) (test-figure square "square")(test-figure exagon "exagon") , 
testing square: 
testing (point 5.0 5.0): #t
testing (point 5.0 8.0): #t
testing (point -10.0 5.0): #f
testing (point 0.0 5.0): #f
testing (point 10.0 5.0): #t
testing (point 8.0 5.0): #t
testing (point 10.0 10.0): #f

testing exagon: 
testing (point 5.0 5.0): #t
testing (point 5.0 8.0): #t
testing (point -10.0 5.0): #f
testing (point 0.0 5.0): #f
testing (point 10.0 5.0): #t
testing (point 8.0 5.0): #t
testing (point 10.0 10.0): #f
, /*REXX program to see if a horizontal ray from pt P intersects a polygon*/call points   5 5,   5 8,  -10  5,  0  5,  10 5,   8 5,  10 10call polygon  0 0,  10 0,   10 10,  0 10                                 ; call test 'square'call polygon  0 0, 10 0, 10 10, 0 10, 2.5 2.5, 7.5 2.5, 7.5 7.5, 2.5 7.5 ; call test 'square hole'call polygon  0 0,  2.5 2.5,   0 10,   2.5 7.5,   7.5 7.5,  10 10,  10 0 ; call test 'irregular'call polygon  3 0,  7 0,    10 5,   7 10,  3 10,   0 5                   ; call test 'exagon'exit                                   /*stick a fork in it, we're done.*//*──────────────────────────────────IN_OUT subroutine────────────────────*/in_out: procedure expose point. poly.  /*note: // is division remainder.*/parse arg p;  #=0;    do side=1 to poly.0 by 2;  #=#+ray_intersect(p,side)                      end   /*side*/return #//2                            /*odd=inside,  return 1;  else 0.*//*──────────────────────────────────POINTS subroutine───────────────────*/points:  n=0;  v='POINT.';     do j=1  for arg();  n=n+1                               call  value v||n'.X', word(arg(j),1)                               call  value v||n'.Y', word(arg(j),2)                               end   /*j*/call value v'0',n                             /*define number of points.*/return/*──────────────────────────────────POLYGON subroutine──────────────────*/polygon:  n=0;  v='POLY.';     parse arg Fx Fy           do j=1  for arg();   _=arg(j);    n=n+1          call value v||n'.X', word(_,1);   call value v||n'.Y', word(_,2)          if n//2  then iterate          n=n+1          call value v||n'.X', word(_,1);   call value v||n'.Y', word(_,2)          end   /*j*/n=n+1call value v||n".X", Fx;    call value v||n".Y", Fy;    call value v'0',nreturn                                 /*POLY.0  is # of segments/sides.*//*──────────────────────────────────RAY_INTERSECT subroutine────────────*/ray_intersect: procedure expose point. poly.;  parse arg ?,s;   sp=s+1epsilon  = '1e'||(digits()%2);         infinity = '1e'||(digits()*2)Px=point.?.x;  Py=point.?.yAx=poly.s.x;   Bx=poly.sp.x  ;         Ay=poly.s.y;   By=poly.sp.yif Ay>By            then  parse value  Ax Ay  Bx By  with  Bx By  Ax Ayif Py=Ay | Py=By    then  Py=Py+epsilonif Py<Ay | Py>By |  Px>max(Ax,Bx)   then return 0if Px<min(Ax,Bx)    then return 1if Ax\=Bx  then m_red  = (By-Ay) / (Bx-Ax);    else m_red  = infinityif Ax\=Px  then m_blue = (Py-Ay) / (Px-Ax);    else return 1return m_blue>=m_red/*──────────────────────────────────TEST procedure──────────────────────*/test: say;  do k=1  for point.0        /*traipse through each test point*/            say '  ['arg(1)"]  point:"   right(point.k.x','point.k.y, 9),                "  is  "     word('outside inside', in_out(k)+1)            end   /*k*/return, 
  [square]  point:       5,5   is   inside
  [square]  point:       5,8   is   inside
  [square]  point:     -10,5   is   outside
  [square]  point:       0,5   is   outside
  [square]  point:      10,5   is   inside
  [square]  point:       8,5   is   inside
  [square]  point:     10,10   is   outside

  [square hole]  point:       5,5   is   outside
  [square hole]  point:       5,8   is   inside
  [square hole]  point:     -10,5   is   outside
  [square hole]  point:       0,5   is   outside
  [square hole]  point:      10,5   is   inside
  [square hole]  point:       8,5   is   inside
  [square hole]  point:     10,10   is   outside

  [irregular]  point:       5,5   is   inside
  [irregular]  point:       5,8   is   outside
  [irregular]  point:     -10,5   is   outside
  [irregular]  point:       0,5   is   outside
  [irregular]  point:      10,5   is   inside
  [irregular]  point:       8,5   is   inside
  [irregular]  point:     10,10   is   outside

  [exagon]  point:       5,5   is   outside
  [exagon]  point:       5,8   is   inside
  [exagon]  point:     -10,5   is   outside
  [exagon]  point:       0,5   is   outside
  [exagon]  point:      10,5   is   outside
  [exagon]  point:       8,5   is   outside
  [exagon]  point:     10,10   is   outside
, Object subclass: Segment [    |pts|    Segment class >> new: points [ |a|      a := super new.      ^ a init: points    ]    init: points [ pts := points copy. ^self ]    endPoints [ ^pts ]    "utility methods"    first [ ^ pts at: 1]    second [ ^ pts at: 2]    leftmostEndPoint [       ^ (self first x > self second x) ifTrue: [ self second ] ifFalse: [ self first ]    ]    rightmostEndPoint [      ^ (self first x > self second x) ifTrue: [ self first ] ifFalse: [ self second ]     ]    topmostEndPoint [      ^ (self first y > self second y) ifTrue: [ self first ] ifFalse: [ self second ]    ]    bottommostEndPoint [      ^ (self first y > self second y) ifTrue: [ self second ] ifFalse: [ self first ]    ]     slope [      (pts at: 1) x ~= (pts at: 2) x      ifTrue: [ ^ ((pts at: 1) y - (pts at: 2) y) / ((pts at: 1) x - (pts at: 2) x) ]      ifFalse: [ ^ FloatD infinity ]    ]     doesIntersectRayFrom: point [ |p A B|      (point y = (pts at: 1) y) | (point y = (pts at: 2) y)      ifTrue: [ p := Point x: (point x) y: (point y) + 0.00001 ]      ifFalse: [ p := point copy ].      A := self bottommostEndPoint.      B := self topmostEndPoint.      (p y < A y) | (p y > B y) | (p x > (self rightmostEndPoint x))        ifTrue: [ ^false ]        ifFalse: [ (p x < (self leftmostEndPoint x))                     ifTrue: [ ^true ]                     ifFalse: [ |s|                         s := Segment new: { A . point }.			(s slope) >= (self slope)			  ifTrue: [ ^ true ]                     ]                 ].        ^false    ]]. Object subclass: Polygon [    |polysegs|    Polygon class >> new [ |a| a := super new. ^ a init. ]    Polygon class >> fromSegments: segments [ |a|      a := super new.      ^ a initWithSegments: segments    ]    Polygon class >> fromPoints: pts and: indexes [ |a|      a := self new.      indexes do: [ :i |        a addSegment: ( Segment new: { pts at: (i at: 1) . pts at: (i at: 2) } )      ].      ^ a    ]    initWithSegments: segments [      polysegs := segments copy. ^self    ]    init [ polysegs := OrderedCollection new. ^ self ]    addSegment: segment [ polysegs add: segment ]     pointInside: point [ |cnt|      cnt := 0.      polysegs do: [ :s | (s doesIntersectRayFrom: point)                          ifTrue: [ cnt := cnt + 1 ] ].      ^ ( cnt \\ 2 = 0 ) not    ]]., |points names polys| points := {           0@0 . 10@0 . 10@10 . 0@10 .           2.5@2.5 . 7.5@2.5 . 7.5@7.5 .           2.5@7.5 . 0@5 . 10@5 .           3@0 . 7@0 . 7@10 . 3@10          }. names := { 'square' . 'square hole' . 'strange' . 'exagon' }. polys := OrderedCollection new. polys add:      (         Polygon fromPoints: points                 and: { {1 . 2}. {2 . 3}. {3 . 4}. {4 . 1} }      ) ;      add:      (        Polygon fromPoints: points                 and: { {1 . 2}. {2 . 3}. {3 . 4}. {4 . 1}. {5 . 6}. {6 . 7}. {7 . 8}. {8 . 5} }      ) ;      add:      (        Polygon fromPoints: points                 and: { {1 . 5}. {5 . 4}. {4 . 8}. {8 . 7}. {7 . 3}. {3 . 2}. {2 . 5} }      ) ;      add:      (        Polygon fromPoints: points                 and: { {11 . 12}. {12 . 10}. {10 . 13}. {13 . 14}. {14 . 9}. {9 . 11} }      ). { 5@5 . 5@8 . -10@5 . 0@5 . 10@5 . 8@5 . 10@10 } do: [ :p |  1 to: 4 do: [ :i |   ('point %1 inside %2? %3' %     { p . names at: i. (polys at: i) pointInside: p }) displayNl  ].  ' ' displayNl.], package require Tcl 8.5 proc point_in_polygon {point polygon} {    set count 0    foreach side [sides $polygon] {        if {[ray_intersects_line $point $side]} {            incr count        }    }    expr {$count % 2} ;#-- 1 = odd = true, 0 = even = false}proc sides polygon {    lassign $polygon x0 y0    foreach {x y} [lrange [lappend polygon $x0 $y0] 2 end] {        lappend res [list $x0 $y0 $x $y]        set x0 $x        set y0 $y    }    return $res}proc ray_intersects_line {point line} {    lassign $point Px Py    lassign $line Ax Ay Bx By    # Reverse line direction if necessary    if {$By < $Ay} {	lassign $line Bx By Ax Ay    }    # Add epsilon to     if {$Py == $Ay || $Py == $By} {	set Py [expr {$Py + abs($Py)/1e6}]    }    # Bounding box checks    if {$Py < $Ay || $Py > $By || $Px > max($Ax,$Bx)} {	return 0    } elseif {$Px < min($Ax,$Bx)} {	return 1    }    # Compare dot products to compare (cosines of) angles    set mRed [expr {$Ax != $Bx ? ($By-$Ay)/($Bx-$Ax) : Inf}]    set mBlu [expr {$Ax != $Px ? ($Py-$Ay)/($Px-$Ax) : Inf}]    return [expr {$mBlu >= $mRed}]} foreach {point poly} {    {0 0}	{-1 -1  -1 1  1 1  1 -1}    {2 2}	{-1 -1  -1 1  1 1  1 -1}    {0 0}	{-2 -2  -2 2  2 2  2 -2   2 -1  1 1  -1 1  -1 -1  1 -1  2 -1}    {1.5 1.5}	{-2 -2  -2 2  2 2  2 -2   2 -1  1 1  -1 1  -1 -1  1 -1  2 -1}    {5 5}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {5 8}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {2 2}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {0 0}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {10 10}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {2.5 2.5}	{0 0  2.5 2.5  0 10  2.5 7.5  7.5 7.5  10 10  10 0  7.5 0.1}    {-5 5}	{3 0  7 0  10 5  7 10  3 10  0 5}} {    puts "$point in $poly = [point_in_polygon $point $poly]"}, #import flo in = @lrzyCipPX ~|afatPRZaq ~&EZ+fleq~~lrPrbr2G&& ~&B+fleq~~lrPrbl2G!| -&   ~&Y+ ~~lrPrbl2G fleq,   ^E(fleq@lrrPX,@rl fleq\0.)^/~&lr ^(~&r,times)^/minus@llPrll2X vid+ minus~~rbbI&-, #cast %bL examples =  in* <   ((0.5,0.6),<(0.,0.),(1.,2.),(1.,0.)>),   ((0.5,0.6),<(0.,0.),(1.,1.),(1.,0.)>)>, <true,false>