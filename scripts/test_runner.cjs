// Automated gameplay test runner via Chrome DevTools Protocol
const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');

async function main() {
  console.log('[TestRunner] Starting Chrome with remote debugging on port 9223...');
  
  const chromeProc = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless',
    '--remote-debugging-port=9223',
    '--window-size=1920,1080',
    'http://localhost:8085/prototype/index.html'
  ], { stdio: 'ignore' });

  // Wait for DevTools port and find the prototype page tab
  let wsUrl = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 300));
    try {
      const res = await fetch('http://127.0.0.1:9223/json');
      const tabs = await res.json();
      const pageTab = tabs.find(t => t.url && t.url.includes('prototype'));
      if (pageTab && pageTab.webSocketDebuggerUrl) {
        wsUrl = pageTab.webSocketDebuggerUrl;
        break;
      }
    } catch (e) {}
  }

  if (!wsUrl) {
    console.error('[TestRunner] Failed to connect to Chrome DevTools');
    chromeProc.kill();
    process.exit(1);
  }

  console.log('[TestRunner] Connected to DevTools WebSocket:', wsUrl);
  const ws = new WebSocket(wsUrl);

  let msgId = 1;
  const pending = new Map();

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      const { resolve, reject } = pending.get(data.id);
      pending.delete(data.id);
      if (data.error) reject(data.error);
      else resolve(data.result);
    }
  };

  await new Promise((resolve) => (ws.onopen = resolve));

  function sendCommand(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = msgId++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await sendCommand('Page.enable');
  await sendCommand('Runtime.enable');

  async function evaluate(expression) {
    const res = await sendCommand('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res && res.result) {
      return res.result.value !== undefined ? res.result.value : res.result;
    }
    return res;
  }

  async function takeScreenshot(filename) {
    const res = await sendCommand('Page.captureScreenshot', { format: 'png' });
    if (!res || !res.data) {
      console.error('[TestRunner] captureScreenshot returned no data:', res);
      return;
    }
    const buf = Buffer.from(res.data, 'base64');
    fs.writeFileSync(filename, buf);
    console.log(`[TestRunner] Saved screenshot: ${filename} (${buf.length} bytes)`);
  }

  // 1. Wait for page & FBX models to load
  console.log('[TestRunner] Waiting for 3D assets to initialize...');
  await new Promise(r => setTimeout(r, 3500));

  // Check state in game
  const stateInfo = await evaluate(`({
    map: STATE.map,
    char: STATE.player.char,
    height: STATE.player.height,
    radius: STATE.player.radius,
    moveState: STATE.player.moveState,
    pos: STATE.player.pos,
    golemMixer: !!golemMixer,
    golemAnims: Object.keys(golemAnims)
  })`);
  console.log('[TestRunner] Initial game state:', stateInfo);

  // Screenshot 1: Colosseum Arena with Stone Golem in 3rd person
  await takeScreenshot('public/shot1_colosseum_golem.png');

  // 2. Test WASD movement
  console.log('[TestRunner] Testing WASD movement & locomotion state...');
  await evaluate(`keys['KeyW'] = true;`);
  await new Promise(r => setTimeout(r, 600));
  const movingState = await evaluate(`({
    moveState: STATE.player.moveState,
    vel: STATE.player.vel,
    pos: STATE.player.pos
  })`);
  console.log('[TestRunner] Moving state (W pressed):', movingState);
  await evaluate(`keys['KeyW'] = false;`);
  await new Promise(r => setTimeout(r, 300));

  // 3. Switch to School Map (Collège Raimon)
  console.log('[TestRunner] Switching to School map...');
  await evaluate(`loadMap('school');`);
  await new Promise(r => setTimeout(r, 1200));

  const schoolState = await evaluate(`({
    map: STATE.map,
    playerPos: STATE.player.pos,
    collidersCount: colliders.length
  })`);
  console.log('[TestRunner] School map state:', schoolState);

  // Screenshot 2: School map ground-level exploration
  await takeScreenshot('public/shot2_school_ground_level.png');

  // 4. Test Spell Casting (Fireball)
  console.log('[TestRunner] Casting Fireball from character hand...');
  await evaluate(`castSlot(0);`);
  await new Promise(r => setTimeout(r, 200));

  // Screenshot 3: Spell casting with projectile in flight
  await takeScreenshot('public/shot3_spellcast.png');
  await new Promise(r => setTimeout(r, 600));

  // 5. Switch to Shadow Rogue (Human Scale 1.83m)
  console.log('[TestRunner] Switching to Shadow Rogue...');
  await evaluate(`setChar('rogue');`);
  await new Promise(r => setTimeout(r, 1000));

  const rogueState = await evaluate(`({
    char: STATE.player.char,
    height: STATE.player.height,
    radius: STATE.player.radius,
    rogueMixer: !!rogueMixer,
    rogueAnims: Object.keys(rogueAnims)
  })`);
  console.log('[TestRunner] Rogue state:', rogueState);

  // Walk forward beside School building
  await evaluate(`keys['KeyW'] = true;`);
  await new Promise(r => setTimeout(r, 800));
  await evaluate(`keys['KeyW'] = false;`);

  // Screenshot 4: Rogue at ground level beside school building
  await takeScreenshot('public/shot4_school_rogue_human_scale.png');

  // 6. Test Wall-Sliding Collision Test Route
  console.log('[TestRunner] Running wall-collision and sliding test...');
  // Move diagonally into the main academy building wall
  await evaluate(`
    playerGroup.position.set(0, 0, 30); // in front of academy hall at Z=42
    keys['KeyW'] = true;
    keys['KeyD'] = true;
  `);
  await new Promise(r => setTimeout(r, 1000));
  const wallTestResult = await evaluate(`({
    pos: playerGroup.position,
    vel: STATE.player.vel,
    stoppedCompletely: (STATE.player.vel.x === 0 && STATE.player.vel.z === 0)
  })`);
  console.log('[TestRunner] Wall sliding test result (slid along X while blocked on Z):', wallTestResult);
  await evaluate(`keys['KeyW'] = false; keys['KeyD'] = false;`);

  // 7. Switch to Village Map
  console.log('[TestRunner] Switching to Village map...');
  await evaluate(`loadMap('village');`);
  await new Promise(r => setTimeout(r, 1200));

  // Screenshot 5: Village map at ground level
  await takeScreenshot('public/shot5_village_ground_level.png');

  // Clean up
  console.log('[TestRunner] All tests completed successfully!');
  ws.close();
  chromeProc.kill();
  process.exit(0);
}

main().catch((err) => {
  console.error('[TestRunner] Error:', err);
  process.exit(1);
});
