// Transparent indicator frames for the interactive audit example. Three.js r160.
import * as T from 'three';

export function buildAuditModel(canvas, width, height) {
  const renderer = new T.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true, alpha: true });
  renderer.setSize(width, height, false);
  renderer.setClearColor(0, 0);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = T.PCFSoftShadowMap;
  renderer.toneMapping = T.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;

  const scene = new T.Scene();
  const studio = new T.Scene();
  studio.background = new T.Color(0x4e5155);
  function reflector(x, y, z, w, h, strength, tint) {
    const color = new T.Color(tint).multiplyScalar(strength);
    const panel = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({color, side:T.DoubleSide}));
    panel.position.set(x, y, z);
    panel.lookAt(0, 0, 0);
    studio.add(panel);
  }
  reflector(-4, 6, 1, 4, 8, 6, 0xfff4de);
  reflector(3, 3, -5, 2, 9, 9, 0xf2f6ff);
  reflector(1, 5, 4, 6, 2, 4, 0xffffff);
  reflector(-4, 1.2, 5, 3.5, 4.5, 2.8, 0xe7efff);
  reflector(5, .3, 3.2, 1.1, 6, 2.6, 0xffe4c4);
  reflector(-2, 0, -4, 4, 3, 0.02, 0x101010);
  const pmrem = new T.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(studio, 0.02).texture;
  const camera = new T.PerspectiveCamera(29,width/height,.1,50);
  camera.position.set(5.1, 4.7, 7.3);
  camera.lookAt(0, .86, 0);

  const key = new T.DirectionalLight(0xffedda, 2.4);
  key.position.set(-3, 8, 5);
  key.castShadow = true;
  key.shadow.mapSize.set(2048,2048);
  Object.assign(key.shadow.camera, {left:-5, right:5, top:5, bottom:-5});
  key.shadow.normalBias = .018;
  key.shadow.bias = -.00035;
  scene.add(key, new T.HemisphereLight(0xffffff, 0x635751, 1.6));
  const metal = (color, roughness, metalness=1) => new T.MeshStandardMaterial({color,roughness,metalness});
  const graphite = metal(0x383e41,.32,.89);
  const recess = metal(0x121617,.4,.55);
  const satin = metal(0xbec2c0,.32);
  const silver = metal(0xd1cfc6,.19);
  const copper = metal(0xd99c76,.28);
  const amber = new T.MeshPhysicalMaterial({color:0xad623a, metalness:.84,roughness:.23,clearcoat:1,clearcoatRoughness:.11});
  function slab(w,d,h,r,bevel,material) {
    const s = new T.Shape(), x=-w/2, y=-d/2;
    s.moveTo(x+r,y); s.lineTo(x+w-r,y); s.quadraticCurveTo(x+w,y,x+w,y+r);
    s.lineTo(x+w,y+d-r); s.quadraticCurveTo(x+w,y+d,x+w-r,y+d);
    s.lineTo(x+r,y+d); s.quadraticCurveTo(x,y+d,x,y+d-r);
    s.lineTo(x,y+r); s.quadraticCurveTo(x,y,x+r,y);
    const g = new T.ExtrudeGeometry(s,{depth:h,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel,bevelSegments:4,curveSegments:9});
    // The extruder splits each chamfer into strips. Share their normals so the
    // long reflections flow across the turned corners of the metal.
    const pos=g.getAttribute('position'), normal=g.getAttribute('normal');
    const sums=new Map(), keys=[];
    for(let j=0;j<pos.count;j++){
      const id=[pos.getX(j),pos.getY(j),pos.getZ(j)].map(v=>Math.round(v*10000)).join(',');
      keys.push(id);
      if(!sums.has(id)) sums.set(id,new T.Vector3());
      sums.get(id).add(new T.Vector3().fromBufferAttribute(normal,j));
    }
    for(const sum of sums.values()) sum.normalize();
    keys.forEach((id,j)=>{const n=sums.get(id);normal.setXYZ(j,n.x,n.y,n.z);});
    g.rotateX(-Math.PI/2);
    const mesh=new T.Mesh(g,material);
    mesh.castShadow=true; mesh.receiveShadow=true;
    return mesh;
  }
  function place(parent, mesh, x, y, z) {
    mesh.position.set(x,y,z); parent.add(mesh); return mesh;
  }
  const model = new T.Group();
  scene.add(model);
  place(model,slab(4.25,2.42,.14,.27,.04,graphite),0,.04,0);
  place(model,slab(4.18,2.35,.025,.24,.018,copper),0,.22,0);
  place(model,slab(4.22,2.39,.12,.25,.04,satin),0,.277,0);
  const columns = [];
  for(let i=0;i<3;i++) {
    const x=(i-1)*1.22;
    place(model,slab(1.03,1.39,.014,.18,.038,recess),x,.407,-.12);
    const slide = new T.Group();
    place(model,slide,x,.425,-.12);
    const finish = [graphite,silver,amber][i];
    const shaft=place(slide,slab(.62,.93,1,.15,.02,graphite),0,0,0);
    const cap=place(slide,slab(.87,1.20,.08,.19,.065,finish),0,1,0);
    // Three physical inlays identify the measured channels: text, source and link.
    if(i===0) {
      for(let j=0;j<3;j++) place(cap,slab(j===2?.28:.47,.026,.003,.01,.002,satin),j===2?-.09:0,.153,(j-1)*.135);
    } else if(i===1) {
      const tab=place(cap,slab(.4,.5,.012,.04,.008,graphite),0,.153,0);
      place(tab,slab(.3,.4,.012,.03,.008,satin),0,.018,0);
    } else {
      for(let j=0;j<2;j++) {
        const link = new T.Mesh(new T.TorusGeometry(.145,.025,10,40),copper);
        link.rotation.x=-Math.PI/2; link.scale.x=.7;
        place(cap,link,0,.175,(j-.5)*.20);
      }
    }
    const leaves=[];
    const leafCount=6;
    for(let j=0;j<leafCount;j++) {
      const leaf=place(slide,slab(.86,1.19,.065,.19,.045,finish),0,0,0);
      leaves.push(leaf);
    }
    columns.push({shaft,cap,leaves});
    for(let j=0;j<9;j++) {
      const tick=slab(.013,j%4===0?.13:.065,.001,.005,.001,graphite);
      place(model,tick,x+(j-4)*.09,.44,.92);
    }
  }
  return function draw(phase) {
    // Four positions: neutral, mention, source, then mention plus a direct URL.
    const poses = [[0,0,0], [1,0,0], [0,1,0], [1,0,1]];
    const cursor = Math.max(0, Math.min(3, phase * 3));
    const step = Math.min(2, Math.floor(cursor)), mix = cursor - step;
    const smooth = mix * mix * (3 - 2 * mix);
    columns.forEach(({shaft,cap,leaves},i)=>{
      const level = poses[step][i] + (poses[step+1][i] - poses[step][i]) * smooth;
      const height = .28 + level * 1.35;
      shaft.scale.y = height;
      cap.position.y = height;
      leaves.forEach((leaf,j)=>{
        const fraction=j/leaves.length;
        leaf.scale.y=.58+.42*level;
        leaf.position.y=height*fraction;
        leaf.rotation.y=.12*fraction*level;
      });
      cap.rotation.y=.12*level;
    });
    model.rotation.y=-.31;
    renderer.render(scene,camera);
  };
}
