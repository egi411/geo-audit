(() => {
  "use strict";
  // The first two coordinates register each bevel to the original texture
  // crop. The third is its distance from the centre plane in the same units.
  const profiles = {
    metal: {
      vertices: [
        145, 115, 60, 599, 108, 80, 456, 527, 94, 19, 530, 60,
        249, 60, -71, 666, 39, -88, 692, 68, -103, 699, 482, -96,
        476, 593, -5, 130, 863, -54, 98, 859, 35, 338, 532, 83,
        297, 562, 0, 155, 563, -73, 210, 333, 71, 468, 296, 80,
        609, 324, -8, 488, 494, 81, 370, 691, 27, 0, 0, -90,
        752, 0, -90, 0, 900, -82, 752, 900, -82,
      ],
      triangles: [
        3, 21, 19, 20, 4, 19, 22, 7, 20, 0, 3, 19, 4, 0, 19, 9, 22, 21,
        9, 18, 22, 9, 13, 18, 8, 18, 11, 18, 8, 22, 8, 7, 22, 3, 10, 21,
        10, 9, 21, 13, 10, 3, 10, 13, 9, 18, 12, 11, 13, 12, 18, 14, 15, 11,
        14, 0, 4, 15, 14, 4, 12, 14, 11, 14, 12, 13, 0, 14, 3, 14, 13, 3,
        1, 16, 15, 1, 15, 4, 16, 17, 15, 15, 17, 11, 8, 17, 7, 17, 16, 7,
        1, 6, 16, 7, 6, 20, 16, 6, 7, 2, 8, 11, 17, 2, 11, 2, 17, 8,
        6, 5, 20, 5, 6, 1, 5, 4, 20, 5, 1, 4,
      ]
    },
    glass: {
      vertices: [
        145, 120, 70, 586, 115, 85, 443, 540, 95, 29, 529, 64,
        251, 66, -74, 663, 35, -95, 692, 61, -108, 698, 484, -94,
        525, 561, -62, 513, 655, -75, 342, 822, -65, 130, 864, -47,
        114, 856, 37, 302, 568, 72, 283, 546, 88, 44, 546, 37,
        197, 324, 79, 471, 313, 86, 587, 338, -17, 417, 552, 69,
        0, 0, -90, 752, 0, -90, 0, 900, -82, 752, 900, -82,
      ],
      triangles: [
        3, 22, 20, 21, 4, 20, 23, 7, 21, 11, 23, 22, 11, 10, 23, 11, 13, 10,
        9, 7, 23, 10, 9, 23, 9, 13, 19, 13, 9, 10, 4, 0, 20, 16, 0, 4,
        0, 3, 20, 0, 16, 3, 13, 14, 19, 9, 8, 7, 5, 4, 21, 5, 1, 4,
        7, 6, 21, 6, 5, 21, 5, 6, 1, 17, 16, 4, 1, 17, 4, 14, 17, 19,
        17, 14, 16, 16, 15, 3, 14, 15, 16, 3, 15, 22, 15, 14, 13, 17, 2, 19,
        2, 9, 19, 2, 8, 9, 18, 17, 1, 18, 6, 7, 6, 18, 1, 8, 18, 7,
        2, 18, 8, 18, 2, 17, 12, 13, 11, 12, 15, 13, 12, 11, 22, 15, 12, 22,
      ]
    },
  };

  // A relief field describes the visible faces of each square product plate.
  // Heights use the same pixel scale as the texture, like the two quote meshes.
  function bevel(edge, width) {
    const t = Math.max(0, Math.min(1, edge / width + 0.5));
    return t * t * (3 - 2 * t);
  }

  function productDepth(name, u, v) {
    if (name === "lens") {
      const radius = Math.hypot((u - 0.62 - (v - 0.48) * 0.14) / 0.35, (v - 0.48) / 0.41);
      return -85 + 129 * bevel(1.19 - radius, 0.21) + 31 * Math.max(0, 1 - radius * radius);
    }
    if (name === "shortlist") {
      const face = Math.min(u - (0.48 - v * 0.085), (0.90 - v * 0.14) - u);
      return -60 + 50 * bevel(u + v * 0.14 - 0.32, 0.04) + 85 * bevel(face, 0.045);
    }
    const front = Math.min(u - 0.43, v - (0.54 - u * 0.18));
    return -65 + 49 * bevel(u + v * 0.21 - 0.15, 0.07) + 102 * bevel(front, 0.06);
  }

  function productProfile(name) {
    const steps = 24;
    const vertices = [], triangles = [];
    for (let row = 0; row <= steps; row++) {
      for (let col = 0; col <= steps; col++) {
        const u = col / steps, v = row / steps;
        vertices.push(u * 724, v * 724, productDepth(name, u, v));
        if (row === steps || col === steps) continue;
        const i = row * (steps + 1) + col;
        triangles.push(i, i + 1, i + steps + 2, i, i + steps + 2, i + steps + 1);
      }
    }
    return {vertices, triangles};
  }

  const stage = document.querySelector("[data-quote-stage]");
  if (!stage || !window.IntersectionObserver || !window.ResizeObserver) return;

  const layer = stage.querySelector(".quote-objects");
  const canvas = layer.querySelector("canvas");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const pointer = matchMedia("(hover: hover) and (pointer: fine)");
  const objects = Array.from(layer.querySelectorAll("[data-profile]"), image => {
    const name = image.dataset.profile;
    const size = profiles[name] ? [752, 900] : [724, 724];
    return {name, image, size};
  });

  // Move registered points in three dimensions before mapping them back to the viewport.
  const vertexSource = `
    attribute vec3 aPoint;
    attribute vec3 aNormal;
    uniform vec2 uViewport, uCenter, uSize, uTextureSize;
    uniform vec3 uAngles;
    varying vec2 vUV;
    varying vec3 vNormal;
    mat2 turn(float a) {
      float c = cos(a), s = sin(a);
      return mat2(c, s, -s, c);
    }
    void main() {
      vUV = aPoint.xy / uTextureSize;
      vec3 p = vec3((vUV - 0.5) * uSize, aPoint.z * uSize.x / uTextureSize.x);
      float restZ = p.z;
      vec3 n = aNormal;
      p.xz = turn(uAngles.y) * p.xz;
      p.yz = turn(uAngles.x) * p.yz;
      p.xy = turn(uAngles.z) * p.xy;
      n.xz = turn(uAngles.y) * n.xz;
      n.yz = turn(uAngles.x) * n.yz;
      n.xy = turn(uAngles.z) * n.xy;
      vNormal = n;
      float camera = uSize.x * 3.2;
      float perspective = camera / (camera + restZ - p.z);
      vec2 screen = (uCenter + p.xy * perspective) / uViewport;
      gl_Position = vec4(screen.x * 2.0 - 1.0, 1.0 - screen.y * 2.0, -p.z / 1600.0, 1.0);
    }`;
  const fragmentSource = `
    precision mediump float;
    uniform sampler2D uPlate;
    uniform vec3 uLight;
    uniform float uGlass;
    varying vec2 vUV;
    varying vec3 vNormal;
    void main() {
      vec4 plate = texture2D(uPlate, vUV);
      if (plate.a < 0.008) discard;
      vec3 n = normalize(vNormal);
      float edge = 1.0 - abs(n.z);
      float specular = pow(max(0.0, dot(reflect(-uLight, n), vec3(0., 0., 1.))), 16.0);
      vec3 reflection = vec3(1.0, 0.81, 0.59) * specular * (0.09 + 0.20 * uGlass);
      vec3 color = plate.rgb * (0.95 + 0.10 * dot(n, uLight)) + reflection * (0.28 + edge);
      gl_FragColor = vec4(color * plate.a, plate.a);
    }`;

  // Smooth normals keep the travelling softbox reflection continuous across the bevels.
  function interleavedMesh(profile) {
    const {vertices, triangles} = profile;
    const normals = new Float32Array(vertices.length);
    for (let index = 0; index < triangles.length; index += 3) {
      const [a, b, c] = triangles.slice(index, index + 3).map(i => i * 3);
      const ab = [0, 1, 2].map(i => vertices[b + i] - vertices[a + i]);
      const ac = [0, 1, 2].map(i => vertices[c + i] - vertices[a + i]);
      const normal = [ab[1]*ac[2] - ab[2]*ac[1], ab[2]*ac[0] - ab[0]*ac[2], ab[0]*ac[1] - ab[1]*ac[0]];
      const length = Math.hypot(...normal) * Math.sign(normal[2]);
      for (const point of [a, b, c]) {
        normal.forEach((value, axis) => { normals[point + axis] += value / length; });
      }
    }
    return new Float32Array(triangles.flatMap(i => {
      const offset = i * 3;
      const normal = normals.slice(offset, offset + 3);
      const length = Math.hypot(...normal);
      return [...vertices.slice(offset, offset + 3), ...normal.map(v => v / length)];
    }));
  }

  let gl, program, uniforms, aPoint, aNormal, frame = 0, last = 0, elapsed = 0;
  let visible = false, ready = false, loading = false;
  let aimX = 0, aimY = 0, smoothX = 0, smoothY = 0;
  const bounds = {width: 0, height: 0};

  function shader(type, source) {
    const result = gl.createShader(type);
    gl.shaderSource(result, source);
    gl.compileShader(result);
    if (!gl.getShaderParameter(result, gl.COMPILE_STATUS)) throw Error("shader");
    return result;
  }

  function upload(object) {
    const mesh = interleavedMesh(profiles[object.name] || productProfile(object.name));
    object.buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, object.buffer);
    gl.bufferData(gl.ARRAY_BUFFER, mesh, gl.STATIC_DRAW);
    object.count = mesh.length / 6;
    object.texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, object.texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, object.image);
  }

  function measure() {
    bounds.width = layer.clientWidth;
    bounds.height = layer.clientHeight;
    if (!ready || !bounds.width || !bounds.height) return;
    const density = Math.min(devicePixelRatio || 1, 1.6, Math.sqrt(1700000 / (bounds.width * bounds.height)));
    canvas.width = Math.round(bounds.width * density);
    canvas.height = Math.round(bounds.height * density);
    gl.viewport(0, 0, canvas.width, canvas.height);
    for (const item of objects) {
      const image = item.image;
      item.width = image.offsetWidth;
      item.height = image.offsetHeight;
      item.x = image.offsetLeft + item.width / 2;
      item.y = image.offsetTop + item.height / 2;
      item.roll = parseFloat(getComputedStyle(image).getPropertyValue("--rest-angle")) * Math.PI / 180;
    }
    if (visible && !document.hidden && !reduced.matches) draw();
  }

  function draw() {
    const scroll = Math.min(1, Math.max(0, -stage.getBoundingClientRect().top / bounds.height));
    const t = elapsed / 1000;
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.uniform2f(uniforms.Viewport, bounds.width, bounds.height);
    gl.uniform3f(uniforms.Light, -0.42 + 0.28 * Math.sin(t * 0.41), -0.4 + smoothY * 0.1, 0.84);
    objects.forEach((item, index) => {
      const side = index ? 1 : -1;
      const wave = Math.sin(t * 0.49 + index * 2);
      gl.uniform2f(uniforms.TextureSize, ...item.size);
      gl.uniform2f(uniforms.Size, item.width, item.height);
      gl.uniform2f(uniforms.Center, item.x + smoothX * side * 12 + wave * 5, item.y + wave * (index ? 10 : 7) - scroll * (index ? 62 : 29));
      gl.uniform3f(uniforms.Angles, wave * 0.13 + smoothY * 0.13, Math.cos(t * 0.42 + index) * 0.16 + smoothX * 0.21 + side * scroll * 0.2, item.roll + wave * 0.045);
      gl.uniform1f(uniforms.Glass, item.name === "metal" ? 0 : 1);
      gl.bindBuffer(gl.ARRAY_BUFFER, item.buffer);
      gl.vertexAttribPointer(aPoint, 3, gl.FLOAT, false, 24, 0);
      gl.vertexAttribPointer(aNormal, 3, gl.FLOAT, false, 24, 12);
      gl.bindTexture(gl.TEXTURE_2D, item.texture);
      gl.drawArrays(gl.TRIANGLES, 0, item.count);
    });
    layer.classList.add("is-rendered");
    stage.style.setProperty("--horizon-rise", Math.round(scroll * 34 + smoothY * 3) + "px");
  }
  function tick(now) {
    frame = 0;
    const d = last ? Math.min(64, now-last) : 32;
    last = now;
    elapsed = Math.min(2300,elapsed+d);
    const blend=1-Math.exp(-d/80);
    smoothX += (aimX-smoothX)*blend;
    smoothY += (aimY-smoothY)*blend;
    draw();
    if (elapsed < 2300 || Math.abs(smoothX-aimX)+Math.abs(smoothY-aimY) > .003) wake();
  }
  function wake() {
    if (!frame && ready && visible && !document.hidden && !reduced.matches) frame=requestAnimationFrame(tick);
  }
  function sync() {
    cancelAnimationFrame(frame);
    frame=last=0;
    if (reduced.matches) {
      layer.classList.remove("is-rendered");
      stage.style.removeProperty("--horizon-rise");
    } else if (visible && !document.hidden) {
      if (!ready) initialize();
      else wake();
    }
  }
  async function initialize() {
    if (loading) return;
    loading = true;
    try {
      await Promise.all(objects.map(item => item.image.decode()));
      gl = canvas.getContext("webgl", {alpha:true, antialias:false, powerPreference:"low-power"});
      if (!gl || gl.isContextLost()) return;
      program = gl.createProgram();
      const shaders = [shader(gl.VERTEX_SHADER, vertexSource), shader(gl.FRAGMENT_SHADER, fragmentSource)];
      shaders.forEach(s => gl.attachShader(program, s));
      gl.linkProgram(program);
      shaders.forEach(s => gl.deleteShader(s));
      if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw Error("program");
      gl.useProgram(program);
      uniforms = Object.fromEntries(["Viewport","Center","Size","TextureSize","Angles","Light","Glass"].map(key => [key, gl.getUniformLocation(program, "u"+key)]));
      aPoint = gl.getAttribLocation(program, "aPoint");
      aNormal = gl.getAttribLocation(program, "aNormal");
      gl.enableVertexAttribArray(aPoint);
      gl.enableVertexAttribArray(aNormal);
      gl.enable(gl.BLEND);
      gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      gl.enable(gl.DEPTH_TEST);
      objects.forEach(upload);
      ready = true;
      measure();
      sync();
    } catch {
      layer.classList.remove("is-rendered");
    }
  }
  stage.addEventListener("pointermove", e => {
    if (!pointer.matches || reduced.matches) return;
    const box = stage.getBoundingClientRect();
    aimX = (e.clientX-box.left) / box.width * 2 - 1;
    aimY = (e.clientY-box.top) / box.height * 2 - 1;
    wake();
  }, {passive:true});
  stage.addEventListener("pointerleave", () => { aimX = aimY = 0; wake(); });
  document.addEventListener("scroll",wake,{passive:true});
  canvas.addEventListener("webglcontextlost", e => {
    e.preventDefault();
    ready = false;
    layer.classList.remove("is-rendered");
    sync();
  });
  canvas.addEventListener("webglcontextrestored", () => {loading = false; sync();});
  new ResizeObserver(measure).observe(layer);
  new IntersectionObserver(([entry]) => {visible = entry.isIntersecting; sync();}).observe(stage);
  reduced.addEventListener("change", sync);
  document.addEventListener("visibilitychange", sync);
})();
