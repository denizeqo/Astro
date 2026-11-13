// 28 Lunar Mansions chart ("Horoskopi Ditor Lunar")
// Self-contained SVG renderer for the /lunarChart endpoint payload.

const SVG_NS = "http://www.w3.org/2000/svg";

const LC = {
    cx: 500,
    cy: 500,
    rMansionOut: 480,
    rMansionIn: 400,
    rGlyphs: 340,
    rAspect: 250,
};

// Screen point for an absolute zodiac longitude.
// The whole wheel is rotated so the Ascendant sits at the left (9 o'clock).
function lcPoint(lon, r, asc) {
    const a = (180 - (lon - asc)) * Math.PI / 180;
    return [LC.cx + r * Math.cos(a), LC.cy - r * Math.sin(a)];
}

function lcEl(tag, attrs) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    return el;
}

// Annular (ring) segment between two absolute longitudes.
function lcSegment(lon1, lon2, asc) {
    const [x1, y1] = lcPoint(lon1, LC.rMansionOut, asc);
    const [x2, y2] = lcPoint(lon2, LC.rMansionOut, asc);
    const [x3, y3] = lcPoint(lon2, LC.rMansionIn, asc);
    const [x4, y4] = lcPoint(lon1, LC.rMansionIn, asc);
    return `M ${x1} ${y1} A ${LC.rMansionOut} ${LC.rMansionOut} 0 0 1 ${x2} ${y2} ` +
           `L ${x3} ${y3} A ${LC.rMansionIn} ${LC.rMansionIn} 0 0 0 ${x4} ${y4} Z`;
}

function lcFormatDeg(pos) {
    const d = Math.floor(pos % 360);
    const m = Math.floor((pos % 1) * 60);
    return d + "° " + m + "'";
}

// Simple collision avoidance for glyph display positions (min separation in degrees).
function lcSpreadPositions(points, minSep) {
    const sorted = points.slice().sort((a, b) => a.position - b.position);
    const display = {};
    let last = -Infinity;
    for (const p of sorted) {
        let pos = p.position;
        if (pos - last < minSep) pos = last + minSep;
        display[p.name] = pos;
        last = pos;
    }
    return display;
}

function drawLunarChart(data, mode, staticUrl) {
    const payload = data[mode];
    const asc = payload.asc;
    const svg = document.getElementById('LunarChart');
    svg.innerHTML = '';

    // Base circles
    for (const r of [LC.rMansionOut, LC.rMansionIn, LC.rAspect]) {
        svg.appendChild(lcEl('circle', {
            cx: LC.cx, cy: LC.cy, r: r,
            fill: 'none', stroke: '#fff', 'stroke-width': r === LC.rMansionOut ? 2 : 1, opacity: 0.6
        }));
    }

    // 28 mansion segments
    for (const mansion of data.mansions) {
        const isMoonMansion = mansion.number === payload.moonMansion.number;
        const seg = lcEl('path', {
            d: lcSegment(mansion.startDeg, mansion.endDeg, asc),
            fill: mansion.rulerColor,
            'fill-opacity': isMoonMansion ? 0.22 : 0.04,
            stroke: isMoonMansion ? mansion.rulerColor : 'rgba(255,255,255,0.35)',
            'stroke-width': isMoonMansion ? 2 : 0.7,
            cursor: 'pointer'
        });
        seg.addEventListener('click', () => showMansionCard(mansion, staticUrl, isMoonMansion));
        svg.appendChild(seg);

        const mid = (mansion.startDeg + mansion.endDeg) / 2;
        const [nx, ny] = lcPoint(mid, 455, asc);
        svg.appendChild(lcEl('text', {
            x: nx, y: ny, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
            'font-size': 15, fill: '#ede1ff', 'font-family': 'Poppins, sans-serif'
        })).textContent = mansion.number;

        const [gx, gy] = lcPoint(mid, 422, asc);
        svg.appendChild(lcEl('text', {
            x: gx, y: gy, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
            'font-size': 22, fill: mansion.rulerColor
        })).textContent = mansion.rulerGlyph;
    }

    // Aspect lines between reference points
    const aspectColors = {
        '0': '#ffffff',
        '30': '#FFAF3D',
        '60': '#a8e4a0',
        '90': '#E3242B',
        '120': '#a8e4a0',
        '150': '#FFAF3D',
        '180': '#E3242B'
    };
    for (const aspect of payload.aspects) {
        const [ax, ay] = lcPoint(aspect.activePosition, LC.rAspect, asc);
        const [px, py] = lcPoint(aspect.passivePosition, LC.rAspect, asc);
        const hard = aspect.deg === '90' || aspect.deg === '180';
        svg.appendChild(lcEl('line', {
            x1: ax, y1: ay, x2: px, y2: py,
            stroke: aspectColors[aspect.deg] || '#FFAF3D',
            'stroke-width': 1.5, 'stroke-dasharray': hard ? '6 5' : 'none', opacity: 0.7
        }));
    }

    // Reference points: Moon, ASC, Sun, Saturn, Lunar Nodes
    const displayPos = lcSpreadPositions(payload.referencePoints, 9);
    for (const point of payload.referencePoints) {
        const dp = displayPos[point.name];
        const [tx, ty] = lcPoint(point.position, LC.rMansionIn, asc);
        const [dx, dy] = lcPoint(dp, LC.rGlyphs, asc);

        // connector line when the glyph was shifted to avoid overlap
        if (Math.abs(dp - point.position) > 0.01) {
            svg.appendChild(lcEl('line', {
                x1: tx, y1: ty, x2: dx, y2: dy,
                stroke: point.color, 'stroke-width': 0.6, opacity: 0.5
            }));
        }

        svg.appendChild(lcEl('circle', {
            cx: dx, cy: dy, r: 22,
            fill: '#0d0820', stroke: point.color, 'stroke-width': 1.5
        }));
        const glyph = lcEl('text', {
            x: dx, y: dy, 'text-anchor': 'middle', 'dominant-baseline': 'middle',
            'font-size': point.name === 'Asc' ? 13 : 24,
            fill: point.color, 'font-family': point.name === 'Asc' ? 'Poppins, sans-serif' : 'serif'
        });
        glyph.textContent = point.glyph;
        svg.appendChild(glyph);

        const title = lcEl('title', {});
        title.textContent = point.name + ' ' + lcFormatDeg(point.position) +
            ' — Mansion ' + point.mansion.number + ' ' + point.mansion.name;
        glyph.appendChild(title);
    }

    // Ascendant marker line
    const [asx1, asy1] = lcPoint(asc, LC.rAspect, asc);
    const [asx2, asy2] = lcPoint(asc, LC.rMansionOut, asc);
    svg.appendChild(lcEl('line', {
        x1: asx1, y1: asy1, x2: asx2, y2: asy2,
        stroke: '#E3242B', 'stroke-width': 2, opacity: 0.8
    }));

    // Center: lunar phase
    const phase = payload.moonPhase;
    const phaseGlyph = lcEl('text', {
        x: LC.cx, y: LC.cy - 20, 'text-anchor': 'middle',
        'font-size': 90, fill: '#ede1ff'
    });
    phaseGlyph.textContent = phase.glyph;
    svg.appendChild(phaseGlyph);

    const phaseName = lcEl('text', {
        x: LC.cx, y: LC.cy + 45, 'text-anchor': 'middle',
        'font-size': 26, fill: '#ede1ff', 'font-family': 'Poppins, sans-serif'
    });
    phaseName.textContent = phase.name;
    svg.appendChild(phaseName);

    const phaseInfo = lcEl('text', {
        x: LC.cx, y: LC.cy + 75, 'text-anchor': 'middle',
        'font-size': 16, fill: '#BFAEDC', 'font-family': 'Poppins, sans-serif'
    });
    phaseInfo.textContent = phase.illumination + '% — ' + phase.elongation + '°';
    svg.appendChild(phaseInfo);

    if (payload.eclipse) {
        const eclipse = lcEl('text', {
            x: LC.cx, y: LC.cy + 105, 'text-anchor': 'middle',
            'font-size': 20, fill: '#FFAF3D', 'font-family': 'Poppins, sans-serif'
        });
        eclipse.textContent = payload.eclipse.glyph + ' ' + payload.eclipse.name;
        svg.appendChild(eclipse);
    }
}

function showMansionCard(mansion, staticUrl, isMoonMansion) {
    const card = document.getElementById('MansionCard');
    card.innerHTML = `
        <img src="${staticUrl}${mansion.image}" alt="Mansion ${mansion.number}" style="width: 140px; height: 140px;">
        <h3 style="color: ${mansion.rulerColor}; font-family: 'Poppins', sans-serif; margin-top: 15px;">
            ${mansion.number}. ${mansion.name}
        </h3>
        <h5 style="color: #ede1ff;">${mansion.title}</h5>
        <p style="color: ${mansion.rulerColor}; font-family: 'Poppins', sans-serif;">
            ${mansion.rulerGlyph} ${mansion.ruler} — ${lcFormatDeg(mansion.startDeg)} → ${lcFormatDeg(mansion.endDeg)}
        </p>
        ${isMoonMansion ? `<p style="color: #AAD5DB; font-family: 'Poppins', sans-serif;">☽ ${mansion.progress !== undefined ? mansion.progress + '%' : ''}</p>` : ''}
        <p style="color: #BFAEDC; font-family: 'Poppins', sans-serif;">${mansion.description}</p>
    `;
}

function fillLunarPanels(data, mode, staticUrl) {
    const payload = data[mode];

    showMansionCard(payload.moonMansion, staticUrl, true);

    const phaseCard = document.getElementById('PhaseCard');
    phaseCard.innerHTML = `
        <div style="font-size: 90px;">${payload.moonPhase.glyph}</div>
        <h3 style="color: #ede1ff; font-family: 'Poppins', sans-serif;">${payload.moonPhase.name}</h3>
        <p style="color: #BFAEDC; font-family: 'Poppins', sans-serif;">
            ${payload.moonPhase.illumination}% ☽ ${payload.moonPhase.elongation}°
        </p>
    `;

    const banner = document.getElementById('EclipseBanner');
    if (payload.eclipse) {
        banner.innerHTML = `
            <div class="glassBg" style="padding: 15px; text-align: center; border: 1px solid #FFAF3D;">
                <span style="font-size: 1.5rem;">${payload.eclipse.glyph}</span>
                <strong style="color: #FFAF3D; font-family: 'Poppins', sans-serif;">${payload.eclipse.name}</strong>
                <span style="color: #BFAEDC; font-family: 'Poppins', sans-serif;"> — ☊ ${payload.eclipse.nodeDistance}°</span>
            </div>
        `;
    } else {
        banner.innerHTML = '';
    }
}

function fillRefTable(payload) {
    const tbody = document.getElementById('RefTbody');
    tbody.innerHTML = '';
    for (const point of payload.referencePoints) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="color: ${point.color};">${point.glyph} ${point.name}</td>
            <td>${lcFormatDeg(point.position)}</td>
            <td>${point.mansion.number}. ${point.mansion.name}</td>
            <td>${point.house.num} (${point.house.symbol})</td>
            <td><span style="color: ${point.num.color};">${point.num.value}${point.num.sup}</span> — ${point.num.arketip}</td>
        `;
        tbody.appendChild(tr);
    }
}

function fillAspectTable(payload) {
    const tbody = document.getElementById('AspectTbody');
    tbody.innerHTML = '';
    for (const aspect of payload.aspects) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="color: ${aspect.activeColor};">${aspect.active}</td>
            <td>${aspect.type}</td>
            <td style="color: ${aspect.passiveColor};">${aspect.passive}</td>
            <td>${aspect.orb}</td>
            <td>${aspect.category}</td>
        `;
        tbody.appendChild(tr);
    }
}

