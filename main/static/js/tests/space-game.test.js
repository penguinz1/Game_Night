const gen_star_test = () => {
    let star = gen_star();
    if (star.x < 0 || star.x > 100 || star.y < 0 || star.y > 100) {
        console.log("FAIL: gen_star_test");
        success = false;
    }
}

const gen_star_coords_test = () => {
    let stars = gen_star_coords();
    for (let i = 0; i < stars.length; i++) {
        let star = stars[i];
        if (star.x < 0 || star.x > 100 || star.y < 0 || star.y > 100) {
            console.log("FAIL: gen_star_coords_test");
            success = false;
            return;
        }
    }
}

const dist_test = () => {
    let e = 0.00001;
    let x1 = 2;
    let x2 = 5;
    let y1 = 4;
    let y2 = 8;

    let distance = dist(x1, y1, x2, y2);
    if (Math.abs(distance - 5) > e) {
        console.log("FAIL: dist_test");
        success = false;
    }
}

const out_of_range_test = () => {
    star1 = {
        x: 50,
        y: 101
    }

    star2 = {
        x: 101,
        y: 99
    }

    star3 = {
        x: 1,
        y: 99
    }

    if (!out_of_range(star1) || !out_of_range(star2) || out_of_range(star3)) {
        console.log("FAIL: out_of_range_test");
        success = false;
    }
}

const intersect_beam_test = () => {
    beam1 = {
        x1: 1,
        y1: 1,
        x2: 2,
        y2: 2
    }
    beam2 = {
        x1: 2,
        y1: 2,
        x2: 1,
        y2: 1
    }
    drifter = {
        x: 3,
        y: 4,
        size: 5
    }

    if (!intersectBeam(beam1, drifter) || intersectBeam(beam2, drifter)) {
        console.log("FAIL: intersect_beam_test");
        success = false;
    }
}

const intersect_rect_test = () => {
    rect1 = {
        left: 1,
        right: 3,
        top: 1,
        bottom: 3
    }
    rect2 = {
        left: 2,
        right: 4,
        top: 2,
        bottom: 4
    }
    rect3 = {
        left: -1,
        right: 0,
        top: -1,
        bottom: 0
    }

    if (!intersectRect(rect1, rect2) || intersectRect(rect1, rect3)) {
        console.log("FAIL: intersect_rect_test");
        success = false;
    }
}

const run_space_game_test = () => {
    gen_star_test();
    gen_star_coords_test();
    dist_test();
    out_of_range_test();
    intersect_beam_test();
    intersect_rect_test();
}