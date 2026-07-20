# Generates src/v2/map-roads.html — an interstate-corridor layer plus the
# missing secondary cities for the Network map, in the map's own projection.
#
# The design source projects the Southeast US equirectangularly; the affine
# fit below reproduces the existing DAL/MEM/ATL/ORL anchors (and the
# already-present Houston/New Orleans dots) to within ~1px:
#   x = 43.53·lon + 4439.6      y = −47.45·lat + 1778.3
from pathlib import Path

AX, BX = 43.53, 4439.6
AY, BY = -47.45, 1778.3


def P(lon, lat):
    return (round(AX * lon + BX, 1), round(AY * lat + BY, 1))


C = {
    'houston': (-95.37, 29.76), 'batonrouge': (-91.15, 30.45), 'nola': (-90.07, 29.95),
    'mobile': (-88.04, 30.69), 'tallahassee': (-84.28, 30.44), 'jax': (-81.66, 30.33),
    'miami': (-80.19, 25.76), 'wpb': (-80.05, 26.71), 'daytona': (-81.02, 29.21),
    'savannah': (-81.10, 32.08), 'charleston': (-79.93, 32.78), 'florence': (-79.77, 34.19),
    'fayetteville': (-78.88, 35.05), 'norfolkish': (-77.90, 36.50),
    'naples': (-81.79, 26.14), 'tampa': (-82.46, 27.95), 'ocala': (-82.14, 29.19),
    'gainesville': (-82.32, 29.65), 'valdosta': (-83.28, 30.83), 'macon': (-83.63, 32.84),
    'atlanta': (-84.39, 33.75), 'chattanooga': (-85.31, 35.05), 'knoxville': (-83.92, 35.96),
    'orlando': (-81.38, 28.54),
    'dallas': (-96.80, 32.78), 'shreveport': (-93.75, 32.52), 'monroe': (-92.12, 32.51),
    'jacksonms': (-90.18, 32.30), 'meridian': (-88.70, 32.36), 'birmingham': (-86.80, 33.52),
    'augusta': (-82.01, 33.47), 'columbia': (-81.03, 34.00),
    'okc': (-97.52, 35.47), 'littlerock': (-92.29, 34.75), 'memphis': (-90.05, 35.15),
    'nashville': (-86.78, 36.16), 'montgomery': (-86.30, 32.37), 'louisville': (-85.76, 38.25),
    'greenville': (-82.39, 34.85), 'charlotte': (-80.84, 35.23), 'durham': (-78.90, 35.99),
    'asheville': (-82.55, 35.60), 'stlouisish': (-89.50, 36.70),
}

ROADS = [
    ['houston', 'batonrouge', 'nola', 'mobile', 'tallahassee', 'jax'],                 # I-10
    ['miami', 'wpb', 'daytona', 'jax', 'savannah', 'charleston', 'florence', 'fayetteville', 'norfolkish'],  # I-95
    ['naples', 'tampa', 'ocala', 'gainesville', 'valdosta', 'macon', 'atlanta', 'chattanooga', 'knoxville'], # I-75
    ['tampa', 'orlando', 'daytona'],                                                    # I-4
    ['dallas', 'shreveport', 'monroe', 'jacksonms', 'meridian', 'birmingham', 'atlanta', 'augusta', 'columbia', 'florence'],  # I-20
    ['okc', 'littlerock', 'memphis', 'nashville', 'knoxville'],                         # I-40
    ['mobile', 'montgomery', 'birmingham', 'nashville', 'louisville'],                  # I-65
    ['montgomery', 'atlanta', 'greenville', 'charlotte', 'durham'],                     # I-85
    ['nola', 'jacksonms', 'memphis', 'stlouisish'],                                     # I-55
    ['dallas', 'okc'],                                                                  # I-35
    ['dallas', 'houston'],                                                              # I-45
    ['charleston', 'columbia', 'asheville'],                                            # I-26
    ['macon', 'savannah'],                                                              # I-16
]

# Secondary cities the map lacks (Houston/NOLA/Birmingham/Charlotte exist).
NEW_CITIES = [
    ('Tampa', 'tampa'), ('Miami', 'miami'), ('Jacksonville', 'jax'),
    ('Savannah', 'savannah'), ('Nashville', 'nashville'),
]

roads = ''
for r in ROADS:
    pts = ' '.join(f'{P(*C[k])[0]},{P(*C[k])[1]}' for k in r)
    roads += f'<polyline points="{pts}" fill="none" stroke="#D2D7DC" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"></polyline>'

cities = ''
for name, key in NEW_CITIES:
    x, y = P(*C[key])
    cities += (f'<g transform="translate({x} {y}) scale({{{{ mGl }}}})" style="pointer-events:none;paint-order:stroke;stroke:#FFFFFF;stroke-width:2.4px">'
               f'<circle r="2.5" fill="#A9AAAC"></circle>'
               f'<text y="14" text-anchor="middle" font-size="9.5" font-family="Inter, sans-serif" fill="#A9AAAC">{name}</text></g>')

out = ('<g style="pointer-events:none" opacity="0.9">' + roads + '</g>\n              '
       + cities + '\n              ')
Path(__file__).parent.joinpath('map-roads.html').write_text(out)
print(f'wrote map-roads.html: {len(out)} chars, {len(ROADS)} corridors, {len(NEW_CITIES)} cities')
