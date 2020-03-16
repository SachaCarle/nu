const CARDINALS = ["W", "SW", "SE", "E", "NE", "NW"];
const ALTERNATE_CARDINALS = [
    "SOUTH-WESTWEST", "SOUTH-EASTSOUTH-WEST",
    "EASTSOUTH-EAST", "EASTNORTH-EAST",
    "NORTH-EASTNORTH-WEST", "NORTH-WESTWEST"
];
const INVERTED_CARDINALS = {
    "W": 0,
    "SW": 1,
    "SE": 2,
    "E": 3,
    "NE": 4,
    "NW": 5
};

function orientation_from_cardinal(projection) {
    return {
        left: CARDINALS[(INVERTED_CARDINALS[projection]) % 6], // W
        right: CARDINALS[(INVERTED_CARDINALS[projection] + 3) % 6], // E
        top_r: CARDINALS[(INVERTED_CARDINALS[projection] + 4) % 6], // NE
        top_l: CARDINALS[(INVERTED_CARDINALS[projection] + 5) % 6], // NW
        bottom_r: CARDINALS[(INVERTED_CARDINALS[projection] + 2) % 6], // SE
        bottom_l: CARDINALS[(INVERTED_CARDINALS[projection] + 1) % 6], // SW
    }
}

function angle_cardinal(ca, cb) {
    return INVERTED_CARDINALS[cb] - INVERTED_CARDINALS[ca];
}

function next_cardinal(edge, rev = false, repeat = 1) {
    if (repeat > 1) {
        return next_cardinal(next_cardinal(edge, rev), rev, repeat - 1);
    } else if (edge == 'W') {
        return rev ? 'NW' : 'SW';
    } else if (edge == 'SW') {
        return rev ? 'W' : 'SE';
    } else if (edge == 'SE') {
        return rev ? 'SW' : 'E';
    } else if (edge == 'E') {
        return rev ? 'SE' : 'NE';
    } else if (edge == 'NE') {
        return rev ? 'E' : 'NW';
    } else if (edge == 'NW') {
        return rev ? 'NE' : 'W';
    } else {
        throw new Error(edge + ' Unknow cardinal');
    }
}

function opposed_cardinal(edge) {
    return next_cardinal(edge, false, 3);
}

function symetric_cardinal(edge) {
    if (edge == 'NW') {
        return 'NE';
    } else if (edge == 'NE') {
        return 'NW';
    } else if (edge == 'W') {
        return 'E';
    } else if (edge == 'E') {
        return 'W';
    } else if (edge == 'SW') {
        return 'SE';
    } else if (edge == 'SE') {
        return 'SW';
    } else {
        throw new Error(edge + ' Unknow cardinal');
    }
}

function side_cardinal(edge) {
    if (edge == 'NW' || edge == 'SW' || edge == 'W') {
        return 'W';
    } else if (edge == 'NE' || edge == 'SE' || edge == 'E') {
        return 'E';
    } else {
        throw new Error(edge + ' Unknow cardinal');
    }
}