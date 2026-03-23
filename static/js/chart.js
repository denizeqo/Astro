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
const rStaticHouseSymbol = rOutsideCircle - 20;
const rDynamicTermsSymbol = rDynamicTermsCircle + 10;
const rDynamicSymbolSymbol = rDynamicSymbolCircle + 10;
const rStaticTermsSymbol = rStaticTermsCircle + 10;
const rStaticSymbolSymbol = rStaticSymbolCircle + 10;

// Text radius
const rDegText = rOutsideCircle - 20;
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

// Stars orbite
const rStarts = [rStaticSymbolCircle + 30, rStaticSymbolCircle + 45, rStaticSymbolCircle + 60, rStaticSymbolCircle + 37.5, rStaticSymbolCircle + 52.5];

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

starsData = {
  // 1 House
  'Deneb Kaitos': {'deg': 1.23, 'r': rStarts[0], 'color': '#FFEA99'},
  'Kereb': {'deg': 1.38, 'r': rStarts[1], 'color': '#880808'},
  'Algenib': {'deg': 9.48, 'r': rStarts[0], 'color': '#4E9FE5'},
  'Erakis': {'deg': 10.2, 'r': rStarts[1], 'color': '#880808'},
  'Alderamina' : {'deg': 13, 'r': rStarts[0], 'color': '#ffffff'},
  'Alpheratz' : {'deg': 14.63, 'r': rStarts[0], 'color': '#ffed29'},
  'Nodus 1' : {'deg': 17.46, 'r': rStarts[0], 'color': '#5c5c5c'},
  'Nodus 2' : {'deg': 17.46, 'r': rStarts[1], 'color': '#FFEA99'},
  'Baten Kaitos' : {'deg': 22.28, 'r': rStarts[0], 'color': '#FFAF3D'},
  'Acamar' : {'deg': 23.36, 'r': rStarts[1], 'color': '#ffffff'},
  'Curda' : {'deg': 24.53, 'r': rStarts[0], 'color': '#E3242B'},
  'Al Pherg' : {'deg': 27, 'r': rStarts[0], 'color': '#ffed29'},
  'Alrischa' : {'deg': 29.7, 'r': rStarts[0], 'color': '#4E9FE5'},

  //2 House
  'Mirach' : {'deg': 30.73, 'r': rStarts[1], 'color': '#E3242B'},
  'Mira' : {'deg': 31.85, 'r': rStarts[0], 'color': '#E3242B'},
  'Angetenar' : {'deg': 32.96, 'r': rStarts[2], 'color': '#ffed29'},
  'Tyl' : {'deg': 33, 'r': rStarts[0], 'color': '#ffed29'},
  'Mesarthim' : {'deg': 33.51, 'r': rStarts[1], 'color': '#4E9FE5'},
  'Sheratan' : {'deg': 34.3, 'r': rStarts[0], 'color': '#ffffff'},
  'Caph' : {'deg': 35.45, 'r': rStarts[1], 'color': '#ffed29'},
  'Alfio' : {'deg': 35.86, 'r': rStarts[0], 'color': '#5c5c5c'},
  'Metallah' : {'deg': 37.18, 'r': rStarts[1], 'color': '#ffffff'},
  'Hamal' : {'deg': 37.98, 'r': rStarts[0], 'color': '#FFEA99'},
  'Schedir' : {'deg': 38.11, 'r': rStarts[2], 'color': '#FFEA99'},
  'Adhil' : {'deg': 38.18, 'r': rStarts[1], 'color': '#FFEA99'},
  'Azha' : {'deg': 39.08, 'r': rStarts[1], 'color': '#8968CD'},
  'Kaffaljidhma' : {'deg': 39.76, 'r': rStarts[2], 'color': '#FFAF3D'},
  'Achirardo' : {'deg': 40.58, 'r': rStarts[0], 'color': '#E3242B'},
  'Zibal' : {'deg': 44.15, 'r': rStarts[2], 'color': '#FFEA99'},
  'Cih' : {'deg': 44.26, 'r': rStarts[0], 'color': '#4E9FE5'},
  'Almach' : {'deg': 44.55, 'r': rStarts[1], 'color': '#ffed29'},
  'Menkare' : {'deg': 44.65, 'r': rStarts[3], 'color': '#E3242B'},
  'Rucha' : {'deg': 48.26, 'r': rStarts[0], 'color': '#ffffff'},
  'Boteina' : {'deg': 51.18, 'r': rStarts[0], 'color': '#FFEA99'},
  'Rana' : {'deg': 51.2, 'r': rStarts[0], 'color': '#FFEA99'},
  'Zaurak' : {'deg': 54.2, 'r': rStarts[0], 'color': '#E3242B'},
  'Capulo' : {'deg': 54.51, 'r': rStarts[1], 'color': '#5c5c5c'},
  'Segnin' : {'deg': 55.1, 'r': rStarts[3], 'color': '#5c5c5c'},
  'Algo' : {'deg': 56.50, 'r': rStarts[0], 'color': '#ffffff'},
  'Misam' : {'deg': 58, 'r': rStarts[0], 'color': '#FFAF3D'},
  'Miram' : {'deg': 59.1, 'r': rStarts[1], 'color': '#FFEA99'},
  'Elettra' : {'deg': 59.75, 'r': rStarts[2], 'color': '#5c5c5c'},
  'Beida' : {'deg': 59.76, 'r': rStarts[0], 'color': '#ffffff'},
  'Celeno' : {'deg': 59.76, 'r': rStarts[3], 'color': '#ffffff'},
  'Taigeta' : {'deg': 59.9, 'r': rStarts[4], 'color': '#ffffff'},
}



var staticChartNum = []
var staticChartSymbols = []
var num = 1



// Static Chart
function staticChart(deg){

  const isMajor = deg % 10 === 0;
  const isHouse = deg % 30 === 0;

  if (isMajor){
    // Write Deg Text
    var text = (deg == 0) ? deg + '°' : (360 - deg) + '°';
    // Add Deg in the chart
    addText(text, deg, rDegText);

    if (isHouse){
      // If isHouse true draw a longer line
      drawLine(deg, rOutsideCircle + 20, rOutsideCircle - 5, isMajor);
      //  Seperate the dynamic
      drawLine(deg, rDynamicSymbolCircle + 25, rDynamicTermsCircle, isMajor);
      drawLine(deg, rStaticHouseCircle + 20, rDynamicHouseCircle, isMajor);
    }else{
      // Draw deg tick
      drawLine(deg, rOutsideCircle, rOutsideCircle - 3, isMajor);
      drawLine(deg, rDynamicSymbolCircle + 23, rDynamicSymbolCircle, isMajor);
    } 
  }

  if (isHouse){
    // Add house num in 
    addText(houseNum, deg + 15, rStaticHouseCircle + 10);

    // Add house symbol (symbols that are at degtext)
    addSymbol(signs[(houseNum - 1) % 12], 15, deg + 15, rStaticHouseSymbol);

    // Seperat a house for each term based on termsLine and houseNum
    //let termsLine = termsPlaceList[houseNum];
    //drawLine(deg + 30 - termsLine[0], rOutsideCircle, rStaticTermsCircle, isMajor);
    //drawLine(deg + 30 - termsLine[1], rOutsideCircle, rStaticTermsCircle, isMajor);
    //drawLine(deg + 30 - termsLine[2], rOutsideCircle, rStaticTermsCircle, isMajor);
    //drawLine(deg + 30 - termsLine[3], rOutsideCircle, rStaticTermsCircle, isMajor);

    // Add terms Symbols based on 
    //let termsSymbols = termsSymbolsList[houseNum];
    //addSymbol(termsSymbols[0], 10, deg + 30 - termsLine[0] / 2, rStaticTermsSymbol);
    //addSymbol(termsSymbols[1], 10, deg + 30 - ((termsLine[1] - termsLine[0])  / 2) - termsLine[0], rStaticTermsSymbol);
    //addSymbol(termsSymbols[2], 10, deg + 30 - ((termsLine[2] - termsLine[1])  / 2) - termsLine[1], rStaticTermsSymbol);
    //addSymbol(termsSymbols[3], 10, deg + 30 - ((termsLine[3] - termsLine[2])  / 2) - termsLine[2], rStaticTermsSymbol);
    //addSymbol(termsSymbols[4], 10, deg + 30 - ((30 - termsLine[3])  / 2) - termsLine[3], rStaticTermsSymbol);

    houseNum--;
  }

  // create the static symbols chart( chart that is devidet at 144 at deg)
  // find sing index
  let signsIndex = ((deg + 30 - (2.5 * houseNum))  / 2.5) % 12;

  // add the sing symbol
  addSymbol(signs[11 - signsIndex], 10, deg + 1.25, rStaticSymbolSymbol);



  num = (num >= 100) ? 28 : num;

  staticChartNum.unshift(num)
  staticChartSymbols.push(signs[11 - signsIndex].slice(0, 2).toUpperCase())
  num ++;
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

function dynamicAscMcIcDsc(data){

  colorMap = {
    0 : '#ffffff',
    1 : '#E3242B',
    2 : '#4E9FE5'
  }

  for(let i in data) {

    let position = 360 - data[i]
    addAngledText2(i.toUpperCase(), position, rAscText);
    drawLine(position, rAscText + 10, rDynamicTermsCircle, true);

    let staticSymbolIndex = 143 - parseInt(data[i]/ 2.5);

    let color = colorMap[staticChartNum[staticSymbolIndex ]%3]

    if (staticSymbolIndex <= 44){
      let textSpace = 1500 / rAscText;
      addAngledText2(staticChartNum[staticSymbolIndex], position + textSpace, rAscText, staticChartSymbols[staticSymbolIndex], 11, color=color);
    }else{
      let textSpace = 1200 / rAscText;
      addAngledText2(staticChartNum[staticSymbolIndex], position + textSpace, rAscText, '', 11, color=color);
    }

  }
}


function addPlanetSymbols(planets){

  colorMap = {
    0 : '#ffffff',
    1 : '#E3242B',
    2 : '#4E9FE5'
  }

  
  for (let planet in planets){

    planetPosition = 360 - planets[planet]
    addSymbol(planet, 20, planetPosition, planetsOrbite[planet]);
    drawLine(planetPosition, rDynamicSymbolCircle - 20, rDynamicSymbolCircle - 24, true);

    let planetNum = 143 - parseInt(planets[planet]/ 2.5);
    
    let color = colorMap[staticChartNum[planetNum]%3]

    if (planetNum <= 44){
      let textSpace = 1300 / planetsOrbite[planet] ;
      addAngledText2(staticChartNum[planetNum], planetPosition + textSpace, planetsOrbite[planet] + 7, staticChartSymbols[planetNum], 11, color=color);
    }else{
      let textSpace = 1000 / planetsOrbite[planet] ; 
      addAngledText2(staticChartNum[planetNum], planetPosition + textSpace, planetsOrbite[planet] + 7, '', 11, color=color);
    }
  }
}


function addStarsSymbol(stars){

  for (let star in stars){
    let position = 360 - stars[star]['deg']
    addSymbol('star', 12, position, stars[star]['r'], color=stars[star]['color']);
    drawLine(position, rStaticSymbolCircle + 20, rStaticSymbolCircle + 23, true, color=stars[star]['color']);
  }

}

function tableData(planets, tbody, table){

  for (let planet in planets){

    let tr = document.createElement("tr");

    let planetName = planet;
    let planetDeg = degMin(planets[planet])
    let planetHouseNum = parseInt(planets[planet] / 30) + 1;
    let planetSign = signs[parseInt(planets[planet] / 30)]
    let planetNum1 =143 - parseInt(planets[planet] / 2.5)


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
    planetNumCol.textContent = staticChartNum[planetNum1];
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


function addSymbol(symbolId, symbolSize, deg, radius, color=''){

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

  if (color){
    use.setAttribute('fill', color);
  }

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

function addAngledText2(text, deg, radius, supText='', fontSize=10, color='#ffffff') {

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

    const normal = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    normal.textContent = text;
    normal.setAttribute('font-size', fontSize + 'px');
    normal.setAttribute('fill', color);
    normal.setAttribute('class', 'chartText')

    const sup = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
    sup.textContent = supText;
    sup.setAttribute("baseline-shift", "super");
    sup.setAttribute("font-size", "50%");
    sup.setAttribute('fill', color);
    sup.setAttribute('class', 'chartText')

    label.appendChild(normal);
    label.appendChild(sup);
    
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
            <svg id="star" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M11.245 4.174C11.4765 3.50808 11.5922 3.17513 11.7634 3.08285C11.9115 3.00298 12.0898 3.00298 12.238 3.08285C12.4091 3.17513 12.5248 3.50808 12.7563 4.174L14.2866 8.57639C14.3525 8.76592 14.3854 8.86068 14.4448 8.93125C14.4972 8.99359 14.5641 9.04218 14.6396 9.07278C14.725 9.10743 14.8253 9.10947 15.0259 9.11356L19.6857 9.20852C20.3906 9.22288 20.743 9.23007 20.8837 9.36432C21.0054 9.48051 21.0605 9.65014 21.0303 9.81569C20.9955 10.007 20.7146 10.2199 20.1528 10.6459L16.4387 13.4616C16.2788 13.5829 16.1989 13.6435 16.1501 13.7217C16.107 13.7909 16.0815 13.8695 16.0757 13.9507C16.0692 14.0427 16.0982 14.1387 16.1563 14.3308L17.506 18.7919C17.7101 19.4667 17.8122 19.8041 17.728 19.9793C17.6551 20.131 17.5108 20.2358 17.344 20.2583C17.1513 20.2842 16.862 20.0829 16.2833 19.6802L12.4576 17.0181C12.2929 16.9035 12.2106 16.8462 12.1211 16.8239C12.042 16.8043 11.9593 16.8043 11.8803 16.8239C11.7908 16.8462 11.7084 16.9035 11.5437 17.0181L7.71805 19.6802C7.13937 20.0829 6.85003 20.2842 6.65733 20.2583C6.49056 20.2358 6.34626 20.131 6.27337 19.9793C6.18915 19.8041 6.29123 19.4667 6.49538 18.7919L7.84503 14.3308C7.90313 14.1387 7.93218 14.0427 7.92564 13.9507C7.91986 13.8695 7.89432 13.7909 7.85123 13.7217C7.80246 13.6435 7.72251 13.5829 7.56262 13.4616L3.84858 10.6459C3.28678 10.2199 3.00588 10.007 2.97101 9.81569C2.94082 9.65014 2.99594 9.48051 3.11767 9.36432C3.25831 9.23007 3.61074 9.22289 4.31559 9.20852L8.9754 9.11356C9.176 9.10947 9.27631 9.10743 9.36177 9.07278C9.43726 9.04218 9.50414 8.99359 9.55657 8.93125C9.61593 8.86068 9.64887 8.76592 9.71475 8.57639L11.245 4.174Z" stroke="none" stroke-width="0" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
            <svg id="star2" xmlns="http://www.w3.org/2000/svg"><circle cx="10" cy="10" r="3" style="filter: blur(0.5px);"/></svg>
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

  staticChartNum = []
  staticChartSymbols = []
  num = 1

  for (let deg = 0; deg < 360; deg += 2.5) {
    //staticHouseCircle(deg);
    //staticDegCircle(deg);
    //staticSymbolCircle(deg); 
    staticChart(deg);
  }

  addStarsSymbol(starsData);

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



