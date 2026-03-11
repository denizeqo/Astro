// Chart
const svg = document.getElementById('Chart');

// Circle center
const cx = 450;
const cy = 450;

const rInsideCircle = 80;
const rOutsideCircle = 380;

// Main Circle radius
const rDynamicHouseCircle = rInsideCircle;
const rStaticHouseCircle = rInsideCircle + 20;
const rDynamicTermsCircle = rOutsideCircle - 80;
const rDynamicSymbolCircle = rOutsideCircle - 60;
const rStaticTermsCircle = rOutsideCircle - 20;
const rStaticSymbolCircle = rOutsideCircle;


// Symbols radius
const rStaticHouseSymbol = rOutsideCircle + 40;
const rDynamicTermsSymbol = rDynamicTermsCircle + 10;
const rDynamicSymbolSymbol = rDynamicSymbolCircle + 10;
const rStaticTermsSymbol = rStaticTermsCircle + 10;
const rStaticSymbolSymbol = rStaticSymbolCircle + 10;

// Text radius
const rDegText = rOutsideCircle + 45;
const rStaticHouseNum = rStaticHouseCircle + 10;
const rDynamicHouseText = rDynamicHouseCircle + 10;
const rAscText = rStaticHouseCircle + 30;


//Planets orbite
const rMoon = rDynamicHouseCircle + 80;
const rMercury = rMoon + 20;
const rVenus = rMercury + 20;
const rSun = rVenus + 20;
const rMars = rSun + 20;
const rJupiter = rMars + 20;
const rSaturn = rJupiter + 20;

// Signs list
const signs = [
  'aries','taurus','gemini','cancer',
  'leo','virgo','libra','scorpio',
  'sagittarius','capricorn','aquarius','pisces'
];


const signsDeg = {
    'aries': 360,
    'taurus': 330,
    'gemini': 300,
    'cancer': 270,
    'leo': 240,
    'virgo': 210,
    'libra': 180,
    'scorpio': 150,
    'sagittarius': 120,
    'capricorn': 90,
    'aquarius': 60,
    'pisces': 30
  };

const decans = {
    1:['mars', 'sun', 'jupiter'],
    2:['venus', 'mercury', 'saturn'],
    3:['mercury', 'venus', 'saturn'],
    4:['moon', 'mars', 'jupiter'],
    5:['sun', 'jupiter', 'mars'],
    6:['mercury', 'saturn', 'venus'],
    7:['venus', 'saturn', 'mercury'],
    8:['mars', 'jupiter', 'moon'],
    9:['jupiter', 'mars', 'sun'],
    10:['saturn', 'venus', 'mercury'],
    11:['saturn', 'mercury', 'venus'],
    12:['jupiter', 'moon', 'mars']
  };

const termsPlaceList = {
  1:[6, 12, 20, 25],
  2:[8, 14, 22, 27],
  3:[6, 12, 17, 24],
  4:[7, 13, 19, 26],
  5:[6, 11, 18, 24],
  6:[7, 17, 21, 28],
  7:[6, 14, 21, 28],
  8:[7, 11, 19, 24],
  9:[12, 17, 21, 26],
  10:[7, 14, 22, 26],
  11:[7, 13, 20, 25],
  12:[12, 16, 19, 28]
}

const termsSymbolsList = {
    1:['jupiter', 'venus', 'mercury', 'mars', 'saturn'],
    2:['venus', 'mercury', 'jupiter', 'saturn', 'mars'],
    3:['mercury', 'jupiter', 'venus', 'mars', 'saturn'],
    4:['mars', 'venus', 'mercury', 'jupiter', 'saturn'],
    5:['jupiter', 'venus', 'saturn', 'mercury', 'mars'],
    6:['mercury', 'venus', 'jupiter', 'mars', 'saturn'],
    7:['saturn', 'mercury', 'jupiter', 'venus', 'mars'],
    8:['mars', 'venus', 'mercury', 'jupiter', 'saturn'],
    9:['jupiter', 'venus', 'mercury', 'saturn', 'mars'],
    10:['mercury', 'jupiter', 'venus', 'saturn', 'mars'],
    11:['mercury', 'venus', 'jupiter', 'mars', 'saturn'],
    12:['venus', 'jupiter', 'mercury', 'mars', 'saturn']
  };


const planetsOrbite = {
  'moon' : rMoon,
  'northMoon' : rMoon,
  'southMoon': rMoon,
  'sun': rSun,
  'mercury': rMercury,
  'venus': rVenus,
  'mars': rMars,
  'jupiter': rJupiter,
  'saturn': rSaturn,
  'uranus': rSaturn,
  'neptune': rSaturn,
  'pluto': rSaturn,
  'chiron': rSaturn
}

const staticChartNum1 = []
const staticChartNum2 = []
var num1 = 9
var num2 = 1

// Static Chart
function staticChart(deg){

  const isMajor = deg % 10 === 0;
  const isHouse = deg % 30 === 0;

  let num3 = '';

  if (isMajor){
    // Write Deg Text
    var text = (deg == 0) ? deg + '°' : (360 - deg) + '°';
    // Add Deg in the chart
    addText(text, deg, rDegText);

    if (isHouse){
      // If isHouse true draw a longer line
      drawLine(deg, rOutsideCircle + 30, rStaticTermsCircle, isMajor);
      //  Seperate the dynamic
      drawLine(deg, rDynamicSymbolCircle + 20, rDynamicTermsCircle, isMajor);
      drawLine(deg, rStaticHouseCircle + 20, rDynamicHouseCircle, isMajor);
    }else{
      // Draw deg tick
      drawLine(deg, rOutsideCircle + 23, rOutsideCircle, isMajor);
    } 
  }

  if (isHouse){
    // Add house num in 
    addText(houseNum, deg + 15, rStaticHouseCircle + 10);

    // Add house symbol (symbols that are at degtext)
    addSymbol(signs[(houseNum - 1) % 12], 15, deg + 15, rStaticHouseSymbol);

    // Seperat a house for each term based on termsLine and houseNum
    let termsLine = termsPlaceList[houseNum];
    drawLine(deg + 30 - termsLine[0], rOutsideCircle, rStaticTermsCircle, isMajor);
    drawLine(deg + 30 - termsLine[1], rOutsideCircle, rStaticTermsCircle, isMajor);
    drawLine(deg + 30 - termsLine[2], rOutsideCircle, rStaticTermsCircle, isMajor);
    drawLine(deg + 30 - termsLine[3], rOutsideCircle, rStaticTermsCircle, isMajor);

    // Add terms Symbols based on 
    let termsSymbols = termsSymbolsList[houseNum];
    addSymbol(termsSymbols[0], 10, deg + 30 - termsLine[0] / 2, rStaticTermsSymbol);
    addSymbol(termsSymbols[1], 10, deg + 30 - ((termsLine[1] - termsLine[0])  / 2) - termsLine[0], rStaticTermsSymbol);
    addSymbol(termsSymbols[2], 10, deg + 30 - ((termsLine[2] - termsLine[1])  / 2) - termsLine[1], rStaticTermsSymbol);
    addSymbol(termsSymbols[3], 10, deg + 30 - ((termsLine[3] - termsLine[2])  / 2) - termsLine[2], rStaticTermsSymbol);
    addSymbol(termsSymbols[4], 10, deg + 30 - ((30 - termsLine[3])  / 2) - termsLine[3], rStaticTermsSymbol);

    houseNum--;
  }

  // create the static symbols chart( chart that is devidet at 144 at deg)
  // find sing index
  let signsIndex = ((deg + 30 - (2.5 * houseNum))  / 2.5) % 12;

  // add the sing symbol
  addSymbol(signs[11 - signsIndex], 10, deg + 1.25, rStaticSymbolSymbol);

  num1 = (num1 <= 1) ? 9 : num1;
  num2 = (num2 >= 100) ? 28 : num2;

  num3 = num1 + ' ' + signs[11 - signsIndex].slice(0, 2).toUpperCase()

  staticChartNum1.push(num3)
  staticChartNum2.push( (deg / 2.5) % 12)
  num1 ++;
  num2 ++;
  // draw a line every 2.5 deg
  drawLine(deg, rOutsideCircle + 20, rOutsideCircle, true);

}




// Dynamic Part
function dynamicChart(ascDeg){
  let signsIndex;
  let startdeg;
  let houseNum = 12;

  startdeg = signsDeg[signs[parseInt(ascDeg / 30)]];

  for (let deg = 0; deg < 360; deg += 2.5) {
     
    if(deg % 30 == 0){
      addText(houseNum, startdeg + deg + 15, rDynamicHouseText);

      let termsLine = termsPlaceList[houseNum];
      drawLine(startdeg + deg + 30 - termsLine[0], rDynamicTermsCircle, rDynamicSymbolCircle, true);
      drawLine(startdeg + deg + 30 - termsLine[1], rDynamicTermsCircle, rDynamicSymbolCircle, true);
      drawLine(startdeg + deg + 30 - termsLine[2], rDynamicTermsCircle, rDynamicSymbolCircle, true);
      drawLine(startdeg + deg + 30 - termsLine[3], rDynamicTermsCircle, rDynamicSymbolCircle, true);

      let termsSymbols1 = termsSymbolsList[houseNum];
      addSymbol(termsSymbols1[0], 10, startdeg + deg + 30 - termsLine[0] / 2, rDynamicTermsSymbol);
      addSymbol(termsSymbols1[1], 10, startdeg + deg + 30 - ((termsLine[1] - termsLine[0])  / 2) - termsLine[0], rDynamicTermsSymbol);
      addSymbol(termsSymbols1[2], 10, startdeg + deg + 30 - ((termsLine[2] - termsLine[1])  / 2) - termsLine[1], rDynamicTermsSymbol);
      addSymbol(termsSymbols1[3], 10, startdeg + deg + 30 - ((termsLine[3] - termsLine[2])  / 2) - termsLine[2], rDynamicTermsSymbol);
      addSymbol(termsSymbols1[4], 10, startdeg + deg + 30 - ((30 - termsLine[3])  / 2) - termsLine[3], rDynamicTermsSymbol);

      houseNum--;
    }

    signsIndex = ((deg + 30 +  - (2.5 * houseNum))  / 2.5) % 12;

    addSymbol(signs[11 - signsIndex], 9, 1.3 + startdeg + deg, rDynamicSymbolSymbol);
    drawLine(startdeg + deg, rDynamicSymbolCircle + 20, rDynamicSymbolCircle, true);
  }
}

function  dynamicAscMcIcDsc(asc, mc, ic, dsc){

  addAngledText2('ASC', 360 - asc, rAscText);
  drawLine(360 - asc, rAscText + 10, rDynamicTermsCircle, true);
  //drawLine(360 - asc, rDynamicSymbolCircle + 20, rDegCircle, true);

  addAngledText2('MC', 360 - mc, rAscText);
  drawLine(360 - mc, rAscText + 10, rDynamicTermsCircle, true);
  //drawLine(360 - mc, rDynamicSymbolCircle + 20, rDegCircle, true);

  addAngledText2('IC', 360 - ic, rAscText);
  drawLine(360 - ic, rAscText + 10, rDynamicTermsCircle, true);
  //drawLine(360 - ic, rDynamicSymbolCircle + 20, rDegCircle, true);

  addAngledText2('DSC', 360 - dsc, rAscText);
  drawLine(360 - dsc, rAscText + 10, rDynamicTermsCircle, true);
  //drawLine(360 - dsc, rDynamicSymbolCircle + 20, rDegCircle, true);

}

function addPlanetSymbols(planets){

  
  for (let planet in planets){

    let planetNum = 143 - parseInt(planets[planet]/ 2.5);

    let textSpace = 1800 / planetsOrbite[planet] ;

    planetPosition = 360 - planets[planet]
    addSymbol(planet, 20, planetPosition, planetsOrbite[planet]);
    drawLine(planetPosition, rDynamicSymbolCircle - 20, rDynamicSymbolCircle - 24, true);
    addAngledText2(staticChartNum1[planetNum], planetPosition + textSpace, planetsOrbite[planet]);

  }
}


function addStarsSymbol(stars){
  algenib = 360 - stars['algenib']
  addSymbol('star', 10, 180, 445);
  drawLine(algenib, rDynamicSymbolCircle, rPlanetsCircle + 20, true)
  //addText(parseInt(stars['algenib']) + ' °', algenib, 430 )
}

function tableData(planets, tbody, table){

  for (let planet in planets){

    let tr = document.createElement("tr");

    let planetName = planet;
    let planetDeg = degMin(planets[planet])
    let planetHouseNum = parseInt(planets[planet] / 30) + 1;
    let planetSign = signs[parseInt(planets[planet] / 30)]
    let planetNum1 = parseInt(planets[planet] / 2.5)


    let planetNameCol = document.createElement("td");
    planetNameCol.textContent = planetName;
    tr.appendChild(planetNameCol);

    let planetSignCol = document.createElement("td");
    planetSignCol.textContent = planetSign;
    tr.appendChild(planetSignCol);

    let planetHouseNumCol = document.createElement("td");
    planetHouseNumCol.textContent = planetHouseNum;
    tr.appendChild(planetHouseNumCol);

    let planetDegCol = document.createElement("td");
    planetDegCol.textContent = planetDeg;
    tr.appendChild(planetDegCol);

    let planetNumCol = document.createElement("td");
    planetNumCol.textContent = staticChartNum1[planetNum1] + '/' + staticChartNum2[planetNum1] ;
    tr.appendChild(planetNumCol);

    tbody.appendChild(tr);
  }

  table.classList.remove('hiddenWidget');
}




// Chart Utility
function drawLine(deg, rOut, rIn, isMajor=false, color='#ffffff'){

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
    line.setAttribute('stroke', color);
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


function showPlanetPopup(event, planet, planetDeg){

    const popup = document.getElementById("planetPopup");

    // get svg position on the page
    const rect = svg.getBoundingClientRect();

    let planetNum = parseInt(planetDeg / 2.5)

    popup.innerHTML = `<strong>${planet}</strong><br>${degMin(planetDeg)}<br>${staticChartNum1[planetNum]}/${staticChartNum2[planetNum]}`;

    popup.style.left = (event.clientX - rect.left) + "px";
    popup.style.top  = (event.clientY - rect.top) + "px";

    popup.style.display = "block";
}






function addAngledText(text, deg, radius) {

    const rad = (deg - 180) * Math.PI / 180;

    const tx = cx + Math.cos(rad) * radius;
    const ty = cy + Math.sin(rad) * radius;

    // Flip text if upside down
    if (deg > 90 && deg < 270) {
        deg += 180;
    }

    const label = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'text'
    );

    label.setAttribute('x', tx);
    label.setAttribute('y', ty);
    label.setAttribute(
        'transform',
        `rotate(${deg} ${tx} ${ty})`
    );

    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('dominant-baseline', 'middle');
    label.setAttribute('class', 'chartText');
    

    label.textContent = text;
    svg.appendChild(label);
}

function addAngledText2(text, deg, radius) {

    const rad = (deg - 180) * Math.PI / 180;

    const tx = cx + Math.cos(rad) * radius;
    const ty = cy + Math.sin(rad) * radius;

    // Flip text if upside down
    if (deg > 0 && deg < 180) {
        deg -= 90;
    }else{
      deg += 90;
    }

    const label = document.createElementNS(
        'http://www.w3.org/2000/svg',
        'text'
    );

    label.setAttribute('x', tx);
    label.setAttribute('y', ty);
    label.setAttribute(
        'transform',
        `rotate(${deg} ${tx} ${ty})`
    );

    label.setAttribute('text-anchor', 'middle');
    label.setAttribute('dominant-baseline', 'middle');
    label.setAttribute('class', 'chartText');

    label.textContent = text;
    svg.appendChild(label);
}


function degMin(lat){

  latDeg = parseInt(lat);
  latMin = parseInt((lat - latDeg) * 60);

  return latDeg + '°' + latMin + "'";
}


function emptyTable(tbody){
  tbody.innerHTML= '';
}


function drawEmptyChart(svg){

  svg.innerHTML= `<defs>
            <svg id="star" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12 2L14.012 7.23109C14.294 7.96432 14.435 8.33093 14.6542 8.63931C14.8486 8.91262 15.0874 9.15141 15.3607 9.34575C15.6691 9.56503 16.0357 9.70603 16.7689 9.98804L22 12L16.7689 14.012C16.0357 14.294 15.6691 14.435 15.3607 14.6542C15.0874 14.8486 14.8486 15.0874 14.6542 15.3607C14.435 15.6691 14.294 16.0357 14.012 16.7689L12 22L9.98804 16.7689C9.70603 16.0357 9.56503 15.6691 9.34575 15.3607C9.15141 15.0874 8.91262 14.8486 8.63931 14.6542C8.33093 14.435 7.96432 14.294 7.23109 14.012L2 12L7.23108 9.98804C7.96431 9.70603 8.33093 9.56503 8.63931 9.34575C8.91262 9.15141 9.15141 8.91262 9.34575 8.63931C9.56503 8.33093 9.70603 7.96431 9.98804 7.23108L12 2Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
            <svg id="chiron" viewBox="0 0 32 32" fill="#ffffff"><text x="16" y="24" text-anchor="middle" font-size="30">⚷</text></svg>
            <svg id="pluto"  viewBox="0 0 32 32" fill="#ffffff"><text x="16" y="24" text-anchor="middle" font-size="30">♇</text></svg>
            <svg id="neptune" viewBox="0 0 32 32" fill="#8968CD"><text x="16" y="24" text-anchor="middle" font-size="30">♆</text></svg>
            <svg id="uranus" viewBox="0 0 32 32" fill="#4E9FE5"><text x="16" y="24" text-anchor="middle" font-size="30">♅</text></svg>
            <svg id="jupiter" viewBox="0 0 32 32" fill="#FFAF3D"><text x="16" y="24" text-anchor="middle" font-size="30">♃</text></svg>
            <svg id="saturn" viewBox="0 0 32 32" fill="#808080"><text x="16" y="24" text-anchor="middle" font-size="30">♄</text></svg>
            <svg id="mars" viewBox="0 0 32 32" fill="none" stroke="#E3242B" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="13" cy="19" r="6"/><line x1="17.5" y1="14.5" x2="24" y2="8"/><line x1="20.5" y1="8" x2="24" y2="8"/><line x1="24" y1="8" x2="24" y2="11.5"/></svg>
            <svg id="venus" viewBox="0 0 32 32" fill="" stroke="#a8e4a0" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="16" cy="11" r="6"/><line x1="16" y1="17" x2="16" y2="26"/><line x1="12" y1="22" x2="20" y2="22"/></svg>
            <svg id="mercury" viewBox="0 0 32 32" fill="#cdb891"><text x="16" y="22" text-anchor="middle" font-size="30">☿</text></svg>
            <svg id="sun" viewBox="0 0 32 32" fill="#FFEA99"><text x="16" y="22" text-anchor="middle" font-size="30">☉</text></svg>
            <svg id="moon" viewBox="0 0 32 32" fill="#AAD5DB"><text x="16" y="22" text-anchor="middle" font-size="30">☽</text></svg>
            <svg id="northMoon" viewBox="0 0 32 32" fill="#AAD5DB"><text x="16" y="24" text-anchor="middle" font-size="30">☊</text></svg>
            <svg id="southMoon" viewBox="0 0 32 32" fill="#AAD5DB"><text x="16" y="24" text-anchor="middle" font-size="30">☋</text></svg>
            <svg id="gemini" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg" fill="#EEDEC5" stroke=""><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="Layer_2" data-name="Layer 2"> <g id="invisible_box" data-name="invisible box"> <rect width="48" height="48" fill="none"></rect> </g> <g id="Horoscope"> <path d="M33,34.1V11.9A26.5,26.5,0,0,0,43.4,5.4a1.9,1.9,0,0,0,0-2.8,1.9,1.9,0,0,0-2.8,0,23.6,23.6,0,0,1-33.2,0,1.9,1.9,0,0,0-2.8,0,1.9,1.9,0,0,0,0,2.8A26.5,26.5,0,0,0,15,11.9V34.1A26.5,26.5,0,0,0,4.6,40.6a1.9,1.9,0,0,0,0,2.8,1.9,1.9,0,0,0,2.8,0,23.6,23.6,0,0,1,33.2,0,1.9,1.9,0,0,0,2.8,0,1.9,1.9,0,0,0,0-2.8A26.5,26.5,0,0,0,33,34.1ZM19,33V13a27.3,27.3,0,0,0,5,.5,27.3,27.3,0,0,0,5-.5V33a27.3,27.3,0,0,0-5-.5A27.3,27.3,0,0,0,19,33Z" fill=""></path> </g> </g> </g></svg>
            <svg id="aries" viewBox="0 0 16 16" fill="#E3242B" xmlns="http://www.w3.org/2000/svg" stroke=""><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M0 4.19056C0 2.42846 1.42846 1 3.19056 1C4.72033 1 6.03482 2.08579 6.32371 3.58803L8 12.3047L9.67629 3.58803C9.96518 2.08579 11.2797 1 12.8094 1C14.5715 1 16 2.42846 16 4.19056V6H14V4.19056C14 3.53303 13.467 3 12.8094 3C12.2386 3 11.7481 3.40516 11.6403 3.96573L9.32602 16H6.67398L4.3597 3.96573C4.2519 3.40516 3.7614 3 3.19056 3C2.53303 3 2 3.53303 2 4.19056V6H0V4.19056Z" fill=""></path> </g></svg>
            <svg id="taurus" viewBox="0 0 16 16" fill="#7BB369" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M8 4C5.79086 4 4 2.20914 4 0H2C2 2.08697 3.06551 3.92508 4.68221 5C3.06551 6.07492 2 7.91303 2 10C2 13.3137 4.68629 16 8 16C11.3137 16 14 13.3137 14 10C14 7.91303 12.9345 6.07492 11.3178 5C12.9345 3.92508 14 2.08697 14 0H12C12 2.20914 10.2091 4 8 4ZM8 6C5.79086 6 4 7.79086 4 10C4 12.2091 5.79086 14 8 14C10.2091 14 12 12.2091 12 10C12 7.79086 10.2091 6 8 6Z" fill=""></path> </g></svg>
            <svg id="cancer" viewBox="0 0 16 16" fill="#0077BE" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M3.11091 4.5214C4.88239 2.02543 8.29622 1.24283 11.0001 2.8039L12.0001 1.07185C8.17373 -1.13729 3.28101 0.173713 1.07187 4.00005C0.343994 5.26077 -0.00235856 6.64014 -0.00109519 8.00094L2.59202e-05 8.00094C0.000527265 9.93351 1.56734 11.5 3.50003 11.5C5.43302 11.5 7.00003 9.93301 7.00003 8.00001C7.00003 6.06701 5.43302 4.50001 3.50003 4.50001C3.3685 4.50001 3.23867 4.50727 3.11091 4.5214ZM3.50003 6.50001C2.6716 6.50001 2.00003 7.17158 2.00003 8.00001C2.00003 8.82844 2.6716 9.50001 3.50003 9.50001C4.32845 9.50001 5.00003 8.82844 5.00003 8.00001C5.00003 7.17158 4.32845 6.50001 3.50003 6.50001Z" fill=""></path> <path fill-rule="evenodd" clip-rule="evenodd" d="M12.8893 11.4786C12.7615 11.4927 12.6316 11.5 12.5 11.5C10.567 11.5 9.00003 9.93301 9.00003 8.00001C9.00003 6.06701 10.567 4.50001 12.5 4.50001C14.4327 4.50001 15.9995 6.06651 16 7.99907L16.0012 7.99907C16.0025 9.3599 15.6562 10.7393 14.9283 12.0001C12.7191 15.8264 7.82641 17.1374 4.00007 14.9283L5.00007 13.1962C7.70396 14.7573 11.1179 13.9747 12.8893 11.4786ZM12.5 6.50001C11.6716 6.50001 11 7.17158 11 8.00001C11 8.82844 11.6716 9.50001 12.5 9.50001C13.3285 9.50001 14 8.82844 14 8.00001C14 7.17158 13.3285 6.50001 12.5 6.50001Z" fill=""></path> </g></svg>
            <svg id="leo" viewBox="0 0 16 16" fill="#FFEA99" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M6.36074 4.19126C6.23086 3.02232 7.14588 2 8.32201 2C9.57833 2 10.5148 3.15839 10.2516 4.38682L8.71738 11.5463C8.22619 13.8385 9.97358 16 12.3178 16C14.3514 16 16 14.3514 16 12.3178V10H14V12.3178C14 13.2469 13.2469 14 12.3178 14C11.2469 14 10.4486 13.0125 10.673 11.9654L12.2072 4.80587C12.7372 2.33242 10.8516 0 8.32201 0C5.95386 0 4.11145 2.05845 4.37297 4.41212L4.7993 8.2491C4.39758 8.0884 3.95911 8 3.5 8C1.567 8 0 9.567 0 11.5C0 13.433 1.567 15 3.5 15C5.433 15 7 13.433 7 11.5V9.94461L6.36074 4.19126ZM5 11.5C5 10.6716 4.32843 10 3.5 10C2.67157 10 2 10.6716 2 11.5C2 12.3284 2.67157 13 3.5 13C4.32843 13 5 12.3284 5 11.5Z" fill=""></path> </g></svg>
            <svg id="virgo" viewBox="0 0 16 16" fill="#9F8C76" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M1 3C1.55228 3 2 3.44772 2 4V14H4V4C4 3.44772 4.44772 3 5 3C5.55228 3 6 3.44772 6 4V14H8V4C8 3.44772 8.44772 3 9 3C9.55228 3 10 3.44772 10 4V9H9V11H10V13C10 14.6569 11.3431 16 13 16V14C12.4477 14 12 13.5523 12 13V11H13C14.6569 11 16 9.65685 16 8C16 6.34315 14.6569 5 13 5H12V4C12 2.34315 10.6569 1 9 1C8.23165 1 7.53076 1.28885 7 1.76389C6.46924 1.28885 5.76835 1 5 1C4.23165 1 3.53076 1.28885 3 1.76389C2.46924 1.28885 1.76835 1 1 1V3ZM12 7V9H13C13.5523 9 14 8.55228 14 8C14 7.44772 13.5523 7 13 7H12Z" fill=""></path> </g></svg>
            <svg id="libra" viewBox="0 0 16 16" fill="#008000" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M5 6C5 4.34315 6.34315 3 8 3C9.65685 3 11 4.34315 11 6C11 6.76152 10.7176 7.45464 10.2503 7.98409L10 8.26763V10H16V8H12.5837C12.8513 7.38734 13 6.71065 13 6C13 3.23858 10.7614 1 8 1C5.23858 1 3 3.23858 3 6C3 6.71065 3.14867 7.38734 3.41633 8H0V10H6V8.26763L5.74974 7.98409C5.28243 7.45464 5 6.76152 5 6Z" fill=""></path> <path d="M0 12V14H16V12H0Z" fill=""></path> </g></svg>
            <svg id="scorpio" viewBox="0 0 16 16" fill="#880808" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M0 3C0.552285 3 1 3.44772 1 4V14H3V4C3 3.44772 3.44772 3 4 3C4.55228 3 5 3.44772 5 4V14H7V4C7 3.44772 7.44772 3 8 3C8.55228 3 9 3.44772 9 4V11.1716C9 13.8443 12.2314 15.1828 14.1213 13.2929L14.4571 12.9571L15 13.5H16V10H12.5V11L13.0429 11.5429L12.7071 11.8787C12.0771 12.5086 11 12.0625 11 11.1716V4C11 2.34315 9.65685 1 8 1C7.23165 1 6.53076 1.28885 6 1.76389C5.46924 1.28885 4.76835 1 4 1C3.23165 1 2.53076 1.28885 2 1.76389C1.46924 1.28885 0.768354 1 0 1V3Z" fill=""></path> </g></svg>
            <svg id="sagittarius" viewBox="0 0 16 16" fill="#FFAF3D" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M12.5857 2H7.99995V0H16V8H14V3.41421L8.41417 9L10.7071 11.2929L9.29285 12.7071L6.99995 10.4142L1.70706 15.7071L0.292847 14.2929L5.58574 9L3.29285 6.70711L4.70706 5.29289L6.99995 7.58579L12.5857 2Z" fill=""></path> </g></svg>
            <svg id="capricorn" viewBox="0 0 16 16" fill="#808080" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path fill-rule="evenodd" clip-rule="evenodd" d="M0 1H1C1.91694 1 2.73781 1.41138 3.28809 2.05964C4.00095 1.40184 4.95354 1 6 1C8.20914 1 10 2.79086 10 5V7.53513C10.5883 7.19479 11.2714 7 12 7C14.2091 7 16 8.79086 16 11C16 13.2091 14.2091 15 12 15C10.8053 15 9.73295 14.4762 9 13.6458C8.26706 14.4762 7.19469 15 6 15V13C7.10457 13 8 12.1046 8 11V5C8 3.89543 7.10457 3 6 3C4.89543 3 4 3.89543 4 5V13H2V4C2 3.44772 1.55228 3 1 3H0V1ZM10 11C10 12.1046 10.8954 13 12 13C13.1046 13 14 12.1046 14 11C14 9.89543 13.1046 9 12 9C10.8954 9 10 9.89543 10 11Z" fill=""></path> </g></svg>
            <svg id="aquarius" viewBox="0 0 16 16" fill="#4E9FE5" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4.50005 1.34827L8.00005 3.34827L11.5 1.34827L15.4962 3.63177L14.5039 5.36826L11.5 3.65177L8.00005 5.65177L4.50005 3.65177L1.49618 5.36826L0.503906 3.63177L4.50005 1.34827Z" fill=""></path> <path d="M4.50005 10.3483L8.00005 12.3483L11.5 10.3483L15.4962 12.6318L14.5039 14.3683L11.5 12.6518L8.00005 14.6518L4.50005 12.6518L1.49618 14.3683L0.503906 12.6318L4.50005 10.3483Z" fill=""></path> <path d="M4.50005 5.84827L0.503906 8.13177L1.49618 9.86826L4.50005 8.15177L8.00005 10.1518L11.5 8.15177L14.5039 9.86826L15.4962 8.13177L11.5 5.84827L8.00005 7.84827L4.50005 5.84827Z" fill=""></path> </g></svg>
            <svg id="pisces" viewBox="0 0 16 16" fill="#8968CD" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M4.94517 8.99997H2V6.99997H4.94517C4.71828 4.94564 3.80038 3.10059 2.42738 1.70002L3.85558 0.299927C5.58105 2.06004 6.72069 4.40009 6.95516 6.99997H9.04493C9.2794 4.40009 10.419 2.06004 12.1445 0.299927L13.5727 1.70002C12.1997 3.10059 11.2818 4.94564 11.0549 6.99997H14V8.99997H11.0549C11.2818 11.0543 12.1997 12.8994 13.5727 14.2999L12.1445 15.7C10.419 13.9399 9.2794 11.5999 9.04493 8.99997H6.95516C6.72069 11.5999 5.58105 13.9399 3.85558 15.7L2.42738 14.2999C3.80038 12.8994 4.71828 11.0543 4.94517 8.99997Z" fill=""></path> </g></svg>
        </defs>

        <circle cx="450" cy="450" r="380" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="400" fill="none" stroke="#fff" stroke-width="1" />
        
        <circle cx="450" cy="450" r="300" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="320" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="340" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="360" fill="none" stroke="#fff" stroke-width="1" />

        <circle cx="450" cy="450" r="120" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="100" fill="none" stroke="#fff" stroke-width="1" />
        <circle cx="450" cy="450" r="80" fill="none" stroke="#fff" stroke-width="1" />

        <circle cx="450" cy="450" r="160" fill="none" stroke="#AAD5DB50" stroke-width="1" />
        <circle cx="450" cy="450" r="180" fill="none" stroke="#cdb89150" stroke-width="1" />
        <circle cx="450" cy="450" r="200" fill="none" stroke="#a8e4a050" stroke-width="1" />
        <circle cx="450" cy="450" r="220" fill="none" stroke="#FFEA9950" stroke-width="1" />
        <circle cx="450" cy="450" r="240" fill="none" stroke="#E3242B50" stroke-width="1" />
        <circle cx="450" cy="450" r="260" fill="none" stroke="#FFAF3D50" stroke-width="1" />
        <circle cx="450" cy="450" r="280" fill="none" stroke="#80808050" stroke-width="1" />
        `


  houseNum = 12;

  for (let deg = 0; deg < 360; deg += 2.5) {
    //staticHouseCircle(deg);
    //staticDegCircle(deg);
    //staticSymbolCircle(deg); 
    staticChart(deg);
  }

    console.log(staticChartNum1)
    console.log(staticChartNum2)

    console.log(11%12)
    console.log(0%12)
    console.log(1%12)
    console.log(2%12)
    console.log(12%12)
    console.log(13%12)
    console.log(14%12)
    

  let ChartWidget = document.getElementById('ChartWidget');
  ChartWidget.classList.remove('hiddenWidget')

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



