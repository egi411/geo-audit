(() => {
  "use strict";
  const canvas = document.getElementById("resonance");
  if (!canvas) return;
  const container = canvas.parentElement;
  const gl = canvas.getContext("webgl", {
    alpha: true,
    antialias: false,
    powerPreference: "low-power",
    premultipliedAlpha: false,
  });
  if (!gl) return;
  const vertex = `attribute vec2 position; void main(){gl_Position=vec4(position,0.,1.);}`;
  const fragment = `
  precision highp float;
  uniform vec2 resolution;
  uniform vec2 pointer;
  uniform float time;
  mat2 rot(float a){float c=cos(a),s=sin(a);return mat2(c,-s,s,c);}
  float torus(vec3 p,float r,float t){return length(vec2(length(p.xy)-r,p.z))-t;}
  vec2 scene(vec3 p){
    p.xz=rot(.30+sin(time*.12)*.18+pointer.x*.16)*p.xz;
    p.yz=rot(-.38+cos(time*.1)*.12+pointer.y*.12)*p.yz;
    p.xy=rot(-.38)*p.xy;
    float a=torus(p,1.22,.17);
    vec3 q=p;q.xz=rot(.38+sin(time*.16)*.38)*q.xz;
    float b=torus(q,.86,.14);
    vec3 r=p;r.yz=rot(-.5+sin(time*.14)*.35)*r.yz;
    float c=torus(r,.50,.115);
    vec2 d=vec2(a,0.);if(b<d.x)d=vec2(b,1.);if(c<d.x)d=vec2(c,2.);
    return d;
  }
  vec3 normal(vec3 p){vec2 e=vec2(.001,0);return normalize(vec3(scene(p+e.xyy).x-scene(p-e.xyy).x,scene(p+e.yxy).x-scene(p-e.yxy).x,scene(p+e.yyx).x-scene(p-e.yyx).x));}
  vec3 studio(vec3 r){
    vec3 col=vec3(.032,.028,.023);
    float soft=pow(max(0.,dot(r,normalize(vec3(-.6,.9,1.2)))),5.);
    col+=vec3(1.,.92,.78)*soft*1.35;
    float strip=exp(-pow((r.x-.15)*8.,2.))*smoothstep(-.4,.5,r.y);
    col+=vec3(1.4,1.3,1.1)*strip;
    float edge=pow(max(0.,dot(r,normalize(vec3(.9,.1,-.4)))),15.);
    col+=vec3(1.1,.62,.29)*edge*2.;
    float ribbon=exp(-pow((r.y+.32)*18.,2.))*smoothstep(-1.,.5,r.x);
    col+=vec3(.8,.91,1.)*ribbon*.8;
    return col;
  }
  void main(){
    vec2 uv=(gl_FragCoord.xy-.5*resolution)/min(resolution.x,resolution.y);
    vec3 ro=vec3(0.,0.,4.9);vec3 rd=normalize(vec3(uv*3.7,-4.8));
    float t=0.;vec2 d=vec2(0.);bool hit=false;
    for(int i=0;i<84;i++){d=scene(ro+rd*t);if(d.x<.0015){hit=true;break;}t+=d.x*.85;if(t>8.)break;}
    if(!hit){gl_FragColor=vec4(0.);return;}
    vec3 p=ro+rd*t;vec3 n=normal(p);vec3 reflected=reflect(rd,n);
    vec3 metal=d.y<.5?vec3(.72,.46,.25):(d.y<1.5?vec3(.91,.78,.58):vec3(.65,.39,.19));
    vec3 env=studio(reflected);
    float fres=pow(1.-max(0.,dot(-rd,n)),4.);
    vec3 col=env*mix(metal,vec3(1.),fres*.65);
    float diffuse=max(0.,dot(n,normalize(vec3(-2.,3.,4.))));
    col+=metal*diffuse*.095;
    float ao=clamp(scene(p+n*.13).x/.13,.22,1.);
    col*=ao;
    col=col/(col+vec3(.55));
    col=pow(col,vec3(.84));
    gl_FragColor=vec4(col,1.);
  }`;
  function compile(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }
  const vs = compile(gl.VERTEX_SHADER, vertex),
    fs = compile(gl.FRAGMENT_SHADER, fragment);
  if (!vs || !fs) return;
  const program = gl.createProgram();
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) return;
  gl.useProgram(program);
  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
    gl.STATIC_DRAW,
  );
  const position = gl.getAttribLocation(program, "position");
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
  const uniforms = Object.fromEntries(
    ["resolution", "pointer", "time"].map((key) => [
      key,
      gl.getUniformLocation(program, key),
    ]),
  );
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  let visible = true,
    frame = 0,
    last = 0,
    elapsed = 0,
    targetX = 0,
    targetY = 0,
    x = 0,
    y = 0,
    lost = false;
  function draw(stamp) {
    frame = 0;
    if (lost || document.hidden || !visible) return;
    const mobile = window.innerWidth < 769;
    const interval = mobile ? 66 : 33;
    if (stamp - last >= interval || reduced.matches) {
      const delta = last ? Math.min(stamp - last, 100) : 0;
      last = stamp;
      if (!reduced.matches) elapsed += delta * 0.001;
      const rect = canvas.getBoundingClientRect();
      const scale = Math.min(devicePixelRatio || 1, mobile ? 1 : 1.35);
      const width = Math.max(1, Math.round(rect.width * scale)),
        height = Math.max(1, Math.round(rect.height * scale));
      if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
        gl.viewport(0, 0, width, height);
      }
      x += (targetX - x) * 0.04;
      y += (targetY - y) * 0.04;
      gl.uniform2f(uniforms.resolution, width, height);
      gl.uniform2f(
        uniforms.pointer,
        reduced.matches ? 0 : x,
        reduced.matches ? 0 : y,
      );
      gl.uniform1f(uniforms.time, elapsed);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
      container.classList.add("ready");
    }
    if (!reduced.matches) frame = requestAnimationFrame(draw);
  }
  function resume() {
    if (frame) cancelAnimationFrame(frame);
    frame = 0;
    last = 0;
    if (!document.hidden && visible && !lost)
      frame = requestAnimationFrame(draw);
  }
  window.addEventListener(
    "pointermove",
    (e) => {
      if (e.pointerType !== "mouse") return;
      targetX = (e.clientX / innerWidth) * 2 - 1;
      targetY = (e.clientY / innerHeight) * 2 - 1;
    },
    { passive: true },
  );
  if ("IntersectionObserver" in window)
    new IntersectionObserver((entries) => {
      visible = entries[0].isIntersecting;
      resume();
    }).observe(canvas);
  document.addEventListener("visibilitychange", resume);
  window.addEventListener("resize", resume, { passive: true });
  reduced.addEventListener("change", resume);
  canvas.addEventListener("webglcontextlost", (e) => {
    e.preventDefault();
    lost = true;
    if (frame) cancelAnimationFrame(frame);
    container.classList.remove("ready");
  });
  canvas.addEventListener("webglcontextrestored", () => {
    /* Keep the SVG fallback after a GPU context reset. */
  });
  resume();
})();
