/* eslint-disable no-console */
import { CARDINALS, opposed_cardinal, orientation_from_cardinal, symetric_cardinal, side_cardinal } from '@/assets/js/cardinal.js';
import gf from '@/assets/js/graph.js';
import { for_index, for_zip, reduce_fun, for_map } from '@/assets/js/all.js';

// Naming functions
function intersection_point_name(pa, pb) {
    if (pa <= pb) {
        return pa + pb;
    } else {
        return intersection_point_name(pb, pa);
    }
}

function path_point_name(path) {
    let pn = path.origin;
    if (side_cardinal(path.direction) === 'W') {
        pn += 'w';
    } else {
        pn += 'e'
    }
    return pn;
}

// Devs functions
// eslint-disable-next-line no-unused-vars
function log_undefined_cardinals(ii, pn) {
    CARDINALS.map(cardinal => {
        if (ii.points[pn][cardinal] == undefined) {
            console.warn(pn + '.' + cardinal + " => " + ii.points[pn][cardinal]);
        }
    });

}

// Delayed operations
function operate_point_cardinal(ii, pn, cardinal, dpn) {
    ii.points[pn][cardinal] = dpn;
    return () => {
        //console.log('set', dpn + '.' + opposed_cardinal(cardinal), 'as', pn)
        ii.points[dpn][opposed_cardinal(cardinal)] = pn;
    }
}

// Specialized
function point_of_plain_span(ii, npn, path) {
    operate_point_cardinal(ii, npn, path.direction, path.destination)();
    let pov = orientation_from_cardinal(path.direction);
    return () => {
        let pnl = ii.points[path.origin][pov.bottom_l];
        let pnr = ii.points[path.origin][pov.top_l];
        let funl = operate_point_cardinal(ii, npn, pov.bottom_r, pnl);
        let funr = operate_point_cardinal(ii, npn, pov.top_r, pnr);
        if (pnl != "NONE") funl();
        if (pnr != "NONE") funr();

    }
}

function point_of_semi_span(ii, path) {
    const pn = path_point_name(path);
    const opp = opposed_cardinal(path.direction);
    const sym = symetric_cardinal(path.direction);
    ii.points[pn] = {};
    let fun = operate_point_cardinal(ii, pn, opp, path.origin);
    operate_point_cardinal(ii, pn, path.direction, path.destination);
    operate_point_cardinal(ii, pn, sym, path.destination);
    let pov = orientation_from_cardinal(path.direction);
    return () => {
        fun();
        return () => {
            /* Semi-singularity new-points links (XNW - XNE & XSE - XSW) */
            if (sym === 'NE' || sym === 'SW') {
                ii.points[pn][pov.top_r] = ii.points[path.origin][sym];
            } else {
                ii.points[pn][pov.bottom_r] = ii.points[path.origin][sym];
            }
            //log_undefined_cardinals(ii, pn);
        }
    };
}

export default function multiplicate(ii) {
    if (for_map(ii.points).length > 1000) {
        console.log('cant multiplicate', for_map(ii.points));
        return ii;
    }
    const categories = gf.categorize_spans(ii.spans);
    if (categories.unknow.length > 0) {
        for_zip(categories.unknow, ii.spans, span => {
            console.log(span.length, span[0].span_name, span);
        });
        throw new Error('Unknow span type in graph definition');
    }
    // Assertion end
    let funs_part1 = [];
    if (!(categories.none.length > 0))
        for_zip(categories.semi, ii.spans, (span) => {
            for_index(span, path => {
                let fun = point_of_semi_span(ii, path);
                funs_part1.push(fun);
            });
        });
    let fun_part2 = reduce_fun(funs_part1);
    if (!(categories.none.length > 0))
        for_zip(categories.semi, ii.spans, (span) => {
            for_index(span, path => { /* New Crown */
                if (path.direction === 'NE' || path.direction === 'SW') {
                    let neig = ii.points[path.origin][side_cardinal(path.direction)];
                    let crown_neig = ii.points[neig][symetric_cardinal(path.direction)];
                    operate_point_cardinal(ii, path_point_name(path), side_cardinal(path.direction), crown_neig)();
                }
            });
        });
    // COMPUTE PLAIN
    for_zip(categories.plain, ii.spans, span => {
        const npn = intersection_point_name(span[0].origin, span[0].destination);
        ii.points[npn] = {};
        for_index(span, path => {
            let fun = point_of_plain_span(ii, npn, path);
            fun_part2.push(fun);
        });
    });
    reduce_fun(fun_part2);
    // Compute paths and spans
    let paths = gf.compute_paths(ii.points);
    let spans = gf.compute_spans(paths);
    ii.spans = spans;
    let angles = gf.compute_angles(paths);
    let tiles = gf.compute_tiles(angles);
    ii.tiles = tiles;
    return ii;
}