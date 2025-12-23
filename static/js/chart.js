// Chart
const svg = document.getElementById('Chart');

// Circle center
const cx = 450;
const cy = 450;

// Circle radius
const rDegCircle = 400;
const rHouseCircle = 150;
const rSymbolCircle = 340;

// Ticket height
const majorTickLength = 10;
const tickLength = 7;

// Radius of text and symbols
const rDegText = rDegCircle + majorTickLength + 15;
const rSmallSigns = rSymbolCircle + 10;
const rHouseText = rHouseCircle + 10;
const rHouseSign = rSymbolCircle + 37;
const rCText = rHouseCircle - 15;

// Signs list
const signs = [
  'aries','taurus','gemini','cancer',
  'leo','virgo','libra','scorpio',
  'sagittarius','capricorn','aquarius','pisces'
];

// Adding the AC IC DC MC text
addText('AC', 0, rCText);
addText('IC', 270, rCText);
addText('DC', 180, rCText);
addText('MC', 90, rCText);


// Current house num
var houseNum = 12;

for (let deg = 0; deg < 360; deg += 2.5) {
    houseCircle(deg);
    degCircle(deg);
    symbolCircle(deg); 
}

// Draw Deg Circle
function degCircle(deg){

    // Check if the line needs to be longer or not
    const isMajor = deg % 10 === 0;

    // Finds in which radius the line starts and ends
    var rOut = (isMajor) ? rDegCircle + majorTickLength : rDegCircle + tickLength;
    var rIn = (isMajor) ? rDegCircle - majorTickLength : rDegCircle - tickLength;

    drawLine(deg, rOut, rIn, isMajor);

    if (isMajor) {
        // Write Deg Text
        var text = (deg == 0) ? deg + '°' : (360 - deg) + '°';
        addText(text, deg, rDegText);
    }
}

function symbolCircle(deg){

    var rOut = rSymbolCircle + 20;
    var rIn = rSymbolCircle;

    drawLine(deg, rOut, rIn);
    deg = deg + 2.5;
    var signsIndex = (deg == 0) ? 0 : (deg / 2.5) % 12;

    signsIndex = 11 - signsIndex;
    
    addSymbol(signs[signsIndex], 10, deg + 1.25, rSmallSigns);
}

function houseCircle(deg){

    const isHouse = deg % 30 === 0;

    if (isHouse){

        var rOut = rDegCircle;
        var rIn = rHouseCircle;

        drawLine(deg, rOut, rIn, true);
        addText(houseNum, deg + 15, rHouseText);
        addSymbol(signs[(houseNum - 1) % 12], 15, deg + 15, rHouseSign);

        houseNum--;
    }
}


function drawLine(deg, rOut, rIn, isMajor=false){

    var rad = (deg - 180) * Math.PI / 180;
    
    const x1 = cx + Math.cos(rad) * rOut;
    const y1 = cy + Math.sin(rad) * rOut;
    const x2 = cx + Math.cos(rad) * rIn;
    const y2 = cy + Math.sin(rad) * rIn;

    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', x1);
    line.setAttribute('y1', y1);
    line.setAttribute('x2', x2);
    line.setAttribute('y2', y2);
    line.setAttribute('class', 'tick' + (isMajor ? ' major' : ''));
    svg.appendChild(line);
}

function addText(text, deg, radius){

    var rad = (deg - 180) * Math.PI / 180;

    const tx = cx + Math.cos(rad) * radius;
    const ty = cy + Math.sin(rad) * radius;

    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', tx);
    label.setAttribute('y', ty);
    label.setAttribute('class', 'degree');
    label.textContent = text;
    svg.appendChild(label);
}


function addSymbol(symbolId, symbolSize, deg, radius){

    var rad = (deg - 180) * Math.PI / 180;

    const x = cx + Math.cos(rad) * radius;
    const y = cy + Math.sin(rad) * radius;
    const signId = symbolId;

    const use = document.createElementNS(
    'http://www.w3.org/2000/svg',
    'use'
    );

    use.setAttributeNS(
    'http://www.w3.org/1999/xlink',
    'href',
    '#' + signId
    );

    const size = symbolSize;

  use.setAttribute('x', x - size / 2);
  use.setAttribute('y', y - size / 2);
  use.setAttribute('width', size);
  use.setAttribute('height', size);

  svg.appendChild(use);

}
















const svg1 = document.getElementById('Chart');

// graph size (SVG content size)
const GRAPH_SIZE = 900;

// viewBox state
let viewBoxSize = 900;
let viewBoxX = 0;
let viewBoxY = 0;

// zoom limits
const MIN_ZOOM = 300;
const MAX_ZOOM = 900;

function updateViewBox() {
  svg1.setAttribute(
    'viewBox',
    `${viewBoxX} ${viewBoxY} ${viewBoxSize} ${viewBoxSize}`
  );
}

updateViewBox();

// keep viewBox inside graph bounds
function clampViewBox() {
  if (viewBoxX < 0) viewBoxX = 0;
  if (viewBoxY < 0) viewBoxY = 0;

  if (viewBoxX + viewBoxSize > GRAPH_SIZE) {
    viewBoxX = GRAPH_SIZE - viewBoxSize;
  }

  if (viewBoxY + viewBoxSize > GRAPH_SIZE) {
    viewBoxY = GRAPH_SIZE - viewBoxSize;
  }
}

// convert mouse position to SVG coordinates
function getSVGPoint(evt) {
  const rect = svg1.getBoundingClientRect();

  return {
    x: (evt.clientX - rect.left) * (viewBoxSize / rect.width) + viewBoxX,
    y: (evt.clientY - rect.top)  * (viewBoxSize / rect.height) + viewBoxY
  };
}

svg1.addEventListener('wheel', (e) => {
  e.preventDefault();

  const zoomFactor = 1.05;
  let newSize;
  var mouse = getSVGPoint(e);

  if (e.deltaY < 0) {
    // ===== ZOOM IN (toward mouse) =====

    newSize = viewBoxSize / zoomFactor;
    newSize = Math.max(MIN_ZOOM, newSize);

    viewBoxSize = newSize;
    viewBoxX = mouse.x - viewBoxSize / 2;
    viewBoxY = mouse.y - viewBoxSize / 2;

  } else {
    // ===== ZOOM OUT (centered) =====
    newSize = viewBoxSize * zoomFactor;
    newSize = Math.min(MAX_ZOOM, newSize);

    viewBoxSize = newSize;
    viewBoxX = mouse.x  - viewBoxSize / 2;
    viewBoxY = mouse.y  - viewBoxSize / 2;
  }

  clampViewBox();
  updateViewBox();
});
