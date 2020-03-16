import { CARDINALS, opposed_cardinal, angle_cardinal } from '@/assets/js/cardinal.js';
import { for_index, for_map, remap } from '@/assets/js/all.js';

function compute_path_name(origin, destination) {
    if (origin <= destination) {
        return origin + destination;
    } else {
        return compute_path_name(destination, origin);
    }
}

function compute_paths(points) {
    const paths = [];
    for (const a in points) {
        for (const b in points) {
            for (const i in CARDINALS) {
                const card = CARDINALS[i];
                if (points[a][card] === b) {
                    paths.push({
                        origin: a,
                        destination: b,
                        direction: card,
                        span_name: compute_path_name(a, b)
                    });
                }
            }
        }
    }
    return paths;
}

// --------------------------------- END PATH

function compute_spans(paths) {
    var spans = {};
    paths.map(path => {
        if (!(path.span_name in spans)) {
            spans[path.span_name] = [];
        }
        spans[path.span_name].push(path);
    });
    return spans;
}

function categorize_spans(spans) {
    let category = {
        sin: [],
        semi: [],
        plain: [],
        none: [],
        unknow: []
    };
    for_map(spans, (span, sn) => {
        const paths = for_index(span);
        if (paths.length == 6) {
            category.sin.push(sn);
        } else if (paths.length == 3) {
            category.none.push(sn);
        } else if (paths.length == 2) {
            if (opposed_cardinal(paths[0].direction) === paths[1].direction) {
                category.plain.push(sn);
            } else {
                category.semi.push(sn);
            }
        } else {
            category.unknow.push(sn);
        }
    });
    return category;
}
// --------------------------------- END SPANS
/* eslint-disable no-console */

function compute_tile_name(a, b, c) {
    if (c > b) {
        return compute_tile_name(a, c, b);
    } else if (b > a) {
        return compute_tile_name(b, a, c);
    } else if (c > a) {
        return compute_tile_name(c, a, b);
    } else {
        return a + b + c;
    }
}

function compute_angles(paths) {
    var angles = [];
    paths.map(pa => {
        paths.map(pb => {
            if (pa.origin === pb.origin && (angle_cardinal(pa.direction, pb.direction) === 1 || angle_cardinal(pa.direction, pb.direction) === -5)) {
                angles.push({
                    origin: pa.origin,
                    first: pa.destination,
                    second: pb.destination,
                    first_span_direction: pa.direction,
                    second_span_direction: pb.direction,
                    tile_name: compute_tile_name(pa.origin, pa.destination, pb.destination)
                });
            }
        });
    });
    return angles;
}
// --------------------------------- END ANGLES

function compute_tiles(angles) {
    var tiles = {};
    angles.map(angle => {
        if (!(angle.tile_name in tiles)) {
            tiles[angle.tile_name] = [];
        }
        tiles[angle.tile_name].push(angle);
    });
    return tiles;
}

function categorize_tiles(tiles) {
    let category = {
        sin: [],
        semi: [],
        part: [],
        plain: [],
        unknow: []
    };
    for_map(tiles, (tile, tn) => {
        const angles = for_index(tile);
        if (angles.length === 6) {
            category.sin.push(tn);
        } else if (angles.length === 1) {
            category.semi.push(tn);
        } else if (angles.length === 2) {
            category.part.push(tn);
        } else if (angles.length === 3) {
            category.plain.push(tn);
        } else {
            category.unknow.push(tn);
        }
    });
    return category;
}
// --------------------------------- END TILES


// INTERFACE
function to_interface(INTERFACE, points) {
    var result = {
        points: '',
        spans: '',
        tiles: '',
    };
    result.points = "/* ORIGINAL GRAPH */\n";
    // STARTING
    result.points += INTERFACE('code', 'init');
    for_map(points, (point, name) => {
        result.points += INTERFACE('code', 'create', [name]);
        CARDINALS.map(card => {
            result.points += INTERFACE('code', 'set', [name, card], point[card]);
        });
    });
    result.points += INTERFACE('code', 'return');
    // hardcode DONE
    var paths = compute_paths(points);
    var spans = compute_spans(paths);
    // Hardcode definition SPANS
    result.spans = "/* GRAPH SPANS */\n";
    result.spans += INTERFACE('code', 'init');
    for_map(spans, (span, sn) => {
        result.spans += INTERFACE('code', 'create', [sn]);
        span.map((path, i) => {
            result.spans += INTERFACE('code', 'create', [sn, i]);
            result.spans += INTERFACE('code', 'set', [sn, i, 'origin'], path.origin);
            result.spans += INTERFACE('code', 'set', [sn, i, 'destination'], path.destination);
            result.spans += INTERFACE('code', 'set', [sn, i, 'direction'], path.direction);
            result.spans += INTERFACE('code', 'set', [sn, i, 'span_name'], path.span_name);
        });
    });
    result.spans += INTERFACE('code', 'return');
    // Hardcode DONE
    var angles = compute_angles(paths);
    var tiles = compute_tiles(angles);
    // Hardcode definition TILES
    result.tiles = "/* GRAPH TILES */\n";
    result.tiles += INTERFACE('code', 'init');
    for_map(tiles, (tile, tn) => {
        result.tiles += INTERFACE('code', 'create', [tn]);
        tile.map((angle, i) => {
            result.tiles += INTERFACE('code', 'create', [tn, i]);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'origin'], angle.origin);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'first'], angle.first);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'second'], angle.second);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'first_span_direction'], angle.first_span_direction);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'second_span_direction'], angle.second_span_direction);
            result.tiles += INTERFACE('code', 'set', [tn, i, 'tile_name'], angle.tile_name);
        });
    });
    result.tiles += INTERFACE('code', 'return');
    // Hardcode done
    return result;
}


// COORDS TO POINT
function orientation_coords(coords, karma) {
    let y = coords[0],
        x = coords[1];
    let base = {
        left: [y, x - 1],
        right: [y, x + 1],
    };
    if (karma)
        return {
            ...base,
            bottom_l: [y + 1, x - 1],
            bottom_r: [y + 1, x],
            top_l: [y - 1, x - 1],
            top_r: [y - 1, x],
        };
    else return {
        ...base,
        bottom_l: [y + 1, x],
        bottom_r: [y + 1, x + 1],
        top_l: [y - 1, x],
        top_r: [y - 1, x + 1],
    }
}

function relative_point(points, center_name, center_coords, dest_coords, orientation) {
    if (!('__memory__' in points)) {
        points.__memory__ = {};
    }
    let memname = center_name + center_coords[0] + ',' + center_coords[1] + ',' + dest_coords[0] + ',' + dest_coords[1] + orientation.left;
    if (memname in points.__memory__) {
        return points.__memory__[memname];
    }
    let rs = [dest_coords[0] - center_coords[0], dest_coords[1] - center_coords[1]];
    let karma = center_coords[0] % 2 == 1;
    let pc = points[center_name];
    let y = rs[0];
    let x = rs[1];
    let debug = y + ',' + x;
    if (y == 0 && x == 0) {
        return center_name;
    } else if (y == 0 && x == 1) {
        return pc[orientation.right];
    } else if (y == 0 && x == -1) {
        return pc[orientation.left];
    } else if (y == 1 && ((x == 0 && karma) || (x == 1 && !karma))) {
        return pc[orientation.bottom_r];
    } else if (y == 1 && ((x == 0 && !karma) || (x == -1 && karma))) {
        return pc[orientation.bottom_l];
    } else if (y == -1 && ((x == 0 && karma) || (x == 1 && !karma))) {
        return pc[orientation.top_r];
    } else if (y == -1 && ((x == 0 && !karma) || (x == -1 && karma))) {
        return pc[orientation.top_l];
    } else {
        if (center_name === pc.W && pc.W === pc.SW && pc.SW === pc.SE && pc.SE === pc.E && pc.E === pc.NE && pc.NE === pc.NW) {
            return null;
        }
        let oc = orientation_coords(center_coords, karma);
        let res = remap(oc, (nc, or) => {
            return [pc[orientation[or]], relative_point(points, pc[orientation[or]], nc, dest_coords, orientation)];
        }, (_, or) => {
            if (or === 'left') return x < 0;
            if (or === 'right') return x > 0;
            if (or.includes('bottom')) return y > 0;
            if (or.includes('top')) return y < 0;
            return false;
        });
        let final = for_map(res, (r, o) => {
            return [o, r[0], r[1]];
        }, (r) => {
            return r[1] != null && r[0] != r[1];
        });
        if (final.length === 0) {
            let mem = Object.values(res)[0][0];
            points.__memory__[memname] = mem;
            return mem;
        } else if (final.length === 1) {
            let mem = final[0][2];
            points.__memory__[memname] = mem;
            return mem;
        } else if (final.length === 2) {
            if (final[0][2] === final[1][2]) {
                let mem = final[0][2];
                points.__memory__[memname] = mem;
                return mem;
            }
            console.log(debug, 'SOLUTIONS', final);
            return debug;
        } else if (final.length === 3) {
            if (final[0][2] === final[1][2] && final[1][2] === final[2][2]) {
                let mem = final[0][2];
                points.__memory__[memname] = mem;
                return mem;
            }
            console.log(debug, 'SOLUTIONS', final);
            return debug;
        } else {
            return debug;
        }
    }
}

export default {
    compute_path_name,
    compute_tile_name,
    compute_paths,
    compute_spans,
    categorize_spans,
    compute_angles,
    compute_tiles,
    categorize_tiles,
    relative_point,
    to_interface,
};