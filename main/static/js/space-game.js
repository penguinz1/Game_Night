const canvas = document.getElementById("space-game");
const templates_score = document.getElementById("personal-score");
const templates_message = document.getElementById("space-text");
const templates_pb = document.getElementById("personal-best");
const templates_site_top = document.getElementById("site-best");
const templates_site_drifters = document.getElementById("drifters-destroyed");
const canvas_rect = {
    left: 0,
    right: canvas.width,
    top: 0,
    bottom: canvas.height
};
const DRIFTER_COLOR = '#D3D3D3';
const BEAM_COLORS = ['#FFFFFF', '#9B30FF', '#2a52be'];
const BASE_SHIP_COLOR = '#7CFC00';
const SHIP_OUTLINE = '#FFA500';
const SHIP_STROKE_SIZE = 2;
const rect = canvas.getBoundingClientRect();
const ctx = canvas.getContext("2d")
const SPEED = 2;
const CIRCLE_SIZE = 2.5;
const startX = canvas.width / 2;
const startY = canvas.height / 2;
const BASE_SHIP_SIZE = 5;
const DRIFTER_MAX_SIZE = 5;
const POINTS = [1, 1, 2, 3, 5];
const TIME_DELAY = 25;
const DIFFICULTY_INTERVAL = 5000;
const BASE_DRIFTER_INTERVAL = 1000;
const DIFFICULTY_STEP = 1.1;
const DRIFTER_SPEED = 4.5;
const SHIP_SPEED = 10;
const SIZE_MOMENTUM = 1.3;
const SIZE_MULT = 3;
const SHIP_MULT = 5;
const MEDIUM_POWER = 500;
const HIGH_POWER = 3000;
const BEAM_PERSIST = [50, 200, 500];
const BEAM_DAMAGE = [1, 2, 7];
var game_active = false;
var drifters;
var beams;
var drifters_destroyed;
var score;
var ship_momentum;
var ship_size;
var drifter_interval;
var difficulty_time;
var drifter_time;
var ship_x;
var ship_y;
var beam_charge;
var beam_amount;
var medium_beam_message = false;
var high_beam_message = false;
var beam_loc;
var ship_momentum_x;
var ship_momentum_y;
var ship_color;

const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!game_active) {
        draw_stars();
        move_stars();
    } else {
        if (difficulty_time >= DIFFICULTY_INTERVAL) {
            drifter_interval = Math.ceil(drifter_interval / DIFFICULTY_STEP);
            difficulty_time = 0;
            templates_message.innerHTML = "Difficulty increased";
        }
        if (drifter_time >= drifter_interval) {
            drifters.push(gen_drifter());
            drifter_time = 0;
        }

        if (beam_charge) {
            beam_amount += TIME_DELAY;
            if (beam_amount > HIGH_POWER) {
                if (high_beam_message) {
                    templates_message.innerHTML = "High beam ready";
                    high_beam_message = false;
                }
                ship_color = BEAM_COLORS[2];
            } else if (beam_amount > MEDIUM_POWER) {
                if (medium_beam_message) {
                    templates_message.innerHTML = "Medium beam ready";
                    medium_beam_message = false;
                }
                ship_color = BEAM_COLORS[1];
            } else {
                ship_color = BEAM_COLORS[0];
            }
        } else if (beam_amount !== 0) {
            let beam_power;
            if (beam_amount < MEDIUM_POWER) {
                beam_power = 0;
                templates_message.innerHTML = "Small beam fired";
            } else if (beam_amount < HIGH_POWER) {
                beam_power = 1;
                templates_message.innerHTML = "Medium beam fired";
            } else {
                templates_message.innerHTML = "High beam fired";
                beam_power = 2;
            }
            beam_amount = 0;
            ship_color = BASE_SHIP_COLOR;

            let beam = {
                power: beam_power,
                life: BEAM_PERSIST[beam_power],
                damage: BEAM_DAMAGE[beam_power],
                x1: ship_x + ship_size * SHIP_MULT / 2,
                y1: ship_y + ship_size * SHIP_MULT / 2,
                x2: beam_loc.x,
                y2: beam_loc.y
            };
            beams.push(beam);

            propel_ship(beam);
        }

        draw_sprites();
        move_sprites();
        check_collisions();
        decay_beams();

        difficulty_time += TIME_DELAY;
        drifter_time += TIME_DELAY;
    }
}

// STAR DECORATION CODE
const gen_star = () => {
    return {
        x: Math.floor(Math.random() * 1400),
        y: Math.floor(Math.random() * 250)
    };
}
const gen_star_coords = () => {
    let arr = []
    for (let i = 0; i < 200; i++) {
        let elem = gen_star();
        arr.push(elem);
    }
    return arr;
}
var star_arr = gen_star_coords();
var star_move = [];
const moving = (index) => {
    for (let i = 0; i < star_move.length; i++) {
        if (star_move[i].index == index) {
            return true;
        }
    }
    return false;
}

const dist = (x1, y1, x2, y2) => {
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

const out_of_range = (star) => {
    return star.x < 0
        || star.y < 0
        || star.x > canvas.width
        || star.y > canvas.height;
}

const draw_stars = () => {
    star_arr.forEach((elem) => {
        ctx.beginPath();
        ctx.arc(elem.x, elem.y, CIRCLE_SIZE, 0, Math.PI * 2, false);
        ctx.fillStyle = "white";
        ctx.fill();
        ctx.closePath();
    });
}

const move_stars = () => {
    for (let i = star_move.length - 1; i >= 0; i--) {
        let move_obj = star_move[i];
        star_arr[move_obj.index].x += Math.round(Math.cos(move_obj.dir) * SPEED);
        star_arr[move_obj.index].y += Math.round(Math.sin(move_obj.dir) * SPEED);
        if (out_of_range(star_arr[move_obj.index])) {
            star_arr[move_obj.index] = gen_star();
            star_move.splice(i, 1);
        }
    }
}


// GAME CODE
const setupGame = () => {
    drifters = [];
    beams = [];
    drifters_destroyed = 0;
    score = 0;
    ship_size = BASE_SHIP_SIZE;
    drifter_interval = BASE_DRIFTER_INTERVAL;
    drifter_time = 0;
    difficulty_time = 0;
    game_active = true;
    ship_x = startX;
    ship_y = startY;
    ship_momentum_x = 0;
    ship_momentum_y = 0;
    ship_color = BASE_SHIP_COLOR;
    beam_charge = false;
    beam_amount = 0;
}

const gen_drifter = () => {
    let startX;
    let startY;
    let dir;
    let size = Math.floor(Math.random() * DRIFTER_MAX_SIZE) + 1;
    let rand = Math.floor(Math.random() * 4);
    if (rand == 0) {
        startY = 1 - size;
        startX = Math.floor(Math.random() * canvas.width);
        dir = Math.random() * Math.PI / 2 + Math.PI / 4;
    } else if (rand == 1) {
        startX = canvas.width - 1;
        startY = Math.floor(Math.random() * canvas.height);
        dir = Math.random() * Math.PI / 2 + Math.PI / 2 + Math.PI / 4;
    } else if (rand == 2) {
        startY = canvas.height - 1;
        startX = Math.floor(Math.random() * canvas.width);
        dir = Math.random() * Math.PI / 2 + Math.PI + Math.PI / 4;
    } else {
        startX = 1 - size;
        startY = Math.floor(Math.random() * canvas.height);
        dir = Math.random() / 2 - Math.PI / 2 + Math.PI / 4
    }

    return {
        x: startX,
        y: startY,
        dir: dir,
        size: size,
        points: POINTS[size - 1]
    }
}

const draw_sprites = () => {
    drifters.forEach((elem) => {
        if (elem.size > 0 && elem.size <= DRIFTER_MAX_SIZE) {
            ctx.beginPath();
            ctx.rect(elem.x, elem.y, elem.size * SIZE_MULT, elem.size * SIZE_MULT);
            ctx.fillStyle = DRIFTER_COLOR;
            ctx.fill();
            ctx.closePath();
        }
    });

    beams.forEach((elem) => {
        ctx.beginPath();

        ctx.moveTo(elem.x1, elem.y1);
        if (elem.x1 == elem.x2) {
            if (elem.y2 >= elem.y1) {
                ctx.lineTo(elem.x2, canvas.height);
            } else {
                ctx.lineTo(elem.x2, 0);
            }
        } else {
            let slope = (elem.y2 - elem.y1) / (elem.x2 - elem.x1);
            if (elem.x2 > elem.x1) {
                ctx.lineTo(canvas.width, elem.y1 + slope * (canvas.width - elem.x1));
            } else {
                ctx.lineTo(0, elem.y1 - 1 * slope * elem.x1);
            }
        }

        ctx.lineWidth = elem.power + 1;
        ctx.strokeStyle = BEAM_COLORS[elem.power];
        ctx.stroke();
        ctx.closePath();
    });

    if (ship_size > 0){
        ctx.beginPath();
        ctx.rect(ship_x, ship_y, ship_size * SHIP_MULT, ship_size * SHIP_MULT);
        ctx.fillStyle = ship_color;
        ctx.fill();
        ctx.strokeStyle = SHIP_OUTLINE;
        ctx.lineWidth = SHIP_STROKE_SIZE;
        ctx.stroke();
        ctx.closePath();
    }
}

const move_sprites = () => {
    for (let i = drifters.length - 1; i >= 0; i--) {
        size_slowdown = drifters[i].size * SIZE_MOMENTUM;
        let moveX = Math.cos(drifters[i].dir) * DRIFTER_SPEED / size_slowdown
        let moveY = Math.sin(drifters[i].dir) * DRIFTER_SPEED / size_slowdown
        drifters[i].x += moveX;
        drifters[i].y += moveY;
        drifter_rect = {
            left: drifters[i].x,
            right: drifters[i].x + drifters[i].size * SIZE_MULT,
            top: drifters[i].y,
            bottom: drifters[i].y + drifters[i].size * SIZE_MULT
        };
        if (!intersectRect(drifter_rect, canvas_rect) 
            || drifters[i].size <= 0 || drifters[i].size > DRIFTER_MAX_SIZE) {
            drifters.splice(i, 1);
        }
    }

    ship_x += ship_momentum_x / ship_size;
    ship_y += ship_momentum_y / ship_size;
    ship_rect = {
        left: ship_x,
        right: ship_x + ship_size * SHIP_MULT,
        top: ship_y,
        bottom: ship_y + ship_size * SHIP_MULT
    }

    if (!intersectRect(ship_rect, canvas_rect)) {
        gameover("You drifted away!");
    }
}

const propel_ship = (beam) => {
    deltaX = beam.x2 - beam.x1;
    deltaY = beam.y2 - beam.y1;

    magnitude = Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));

    if (magnitude === 0) {
        magnitude = 1;
    }

    deltaX = beam.damage * deltaX / magnitude;
    deltaY = beam.damage * deltaY / magnitude;

    ship_momentum_x -= deltaX;
    ship_momentum_y -= deltaY;
}

const intersectBeam = (beam, drifter) => {
    drifter_rect = {
        left: drifter.x,
        right: drifter.x + drifter.size * SIZE_MULT,
        top: drifter.y,
        bottom: drifter.y + drifter.size * SIZE_MULT
    };
    if (beam.x1 == beam.x2) {
        if (beam.y2 >= beam.y1) {
            if (drifter_rect.bottom > beam.y1 
                && drifter_rect.left < beam.x1
                && drifter_rect.right > beam.x1) {
                return true;
            }
        } else {
            if (drifter_rect.top < beam.y1
                && drifter_rect.left < beam.x1
                && drifter_rect.right > beam.x1) {
                return true;
            }
        }
    } else {
        let slope = (beam.y2 - beam.y1) / (beam.x2 - beam.x1);
        if (beam.x2 > beam.x1) {
            if (drifter_rect.right <= beam.x1) {
                return false;
            } else if (drifter_rect.left < beam.x1) {
                let y1 = beam.y1;
                let y2 = beam.y1 + slope * (drifter_rect.right - beam.x1);
                return crosses(y1, y2, drifter_rect.bottom, drifter_rect.top);
            } else {
                let y1 = beam.y1 + slope * (drifter_rect.left - beam.x1);
                let y2 = beam.y1 + slope * (drifter_rect.right - beam.x1);
                return crosses(y1, y2, drifter_rect.bottom, drifter_rect.top);
            }
        } else {
            if (drifter_rect.left >= beam.x1) {
                return false;
            } else if (drifter_rect.right > beam.x1) {
                let y1 = beam.y1;
                let y2 = beam.y1 - slope * (beam.x1 - drifter_rect.left);
                return crosses(y1, y2, drifter_rect.bottom, drifter_rect.top);
            } else {
                let y1 = beam.y1 - slope * (beam.x1 - drifter_rect.right);
                let y2 = beam.y1 - slope * (beam.x1 - drifter_rect.left);
                return crosses(y1, y2, drifter_rect.bottom, drifter_rect.top);
            }
        }
    }

    return false;
}

const check_collisions = () => {
    let ship_damaged = false;
    ship_rect = {
        left: ship_x,
        right: ship_x + ship_size * SHIP_MULT,
        top: ship_y,
        bottom: ship_y + ship_size * SHIP_MULT
    };
    for (let i = drifters.length - 1; i >= 0; i--) {
        drifter_rect = {
            left: drifters[i].x,
            right: drifters[i].x + drifters[i].size * SIZE_MULT,
            top: drifters[i].y,
            bottom: drifters[i].y + drifters[i].size * SIZE_MULT
        };
        if (intersectRect(drifter_rect, ship_rect)) {
            ship_damaged = true;
            drifters.splice(i, 1);
        }
    }
    if (ship_damaged) {
        ship_size -= 1;
        if (ship_size > 0) templates_message.innerHTML = `Took damage. Health is at ${ship_size}`;
        else {
            gameover("You were destroyed!");
        }
    }

    let drifter_combo = 0;
    let score_combo = 0;
    beams.forEach((beam) => {
        for (let i = drifters.length - 1; i >= 0; i--) {
            if (intersectBeam(beam, drifters[i])) {
                drifters[i].size -= beam.damage;
                let curr_size = drifters[i].size;
                if (curr_size <= 0) {
                    drifter_combo += 1;
                    score_combo += drifters[i].points;
                    drifters.splice(i, 1);
                }
            }
        }
    });

    let bonus = Math.pow(drifter_combo, 2) / 2 - drifter_combo / 2

    if (drifter_combo > 0) {
        score += score_combo + bonus;
        templates_score.innerHTML = score;

        if (bonus > 0) {
            templates_message.innerHTML = `Scored ${score_combo} points: ${score_combo} points from destroying drifters + ${bonus} bonus points from a ${drifter_combo} combo!`;
        } else {
            templates_message.innerHTML = `Scored ${score_combo} points: ${score_combo} points from destroying drifters!`;
        }
    }
    drifters_destroyed += drifter_combo;

    if (user && score > personal_best) {
        personal_best = score;
        templates_pb.innerHTML = personal_best;
    }

    if (score > site_best) {
        site_best = score;
        templates_site_top.innerHTML = site_best;
    }

    site_drifters += drifter_combo;
    templates_site_drifters.innerHTML = site_drifters;
}

const decay_beams = () => {
    for (let i = beams.length - 1; i >= 0; i--) {
        beams[i].life -= TIME_DELAY;
        if (beams[i].life <= 0) {
            beams.splice(i, 1);
        }
    }
}

const intersectRect = (r1, r2) => {
    return !(r2.left > r1.right || 
           r2.right < r1.left || 
           r2.top > r1.bottom ||
           r2.bottom < r1.top);
}

const crosses = (y1, y2, target1, target2) => {
    if (y1 >= target1 && y1 <= target2) {
        return true;
    }
    if (y2 >= target1 && y2 <= target2) {
        return true;
    }

    if (y1 < target1 && y2 > target2) {
        return true;
    }
    if (y1 > target2 && y2 < target1) {
        return true;
    }

    return false;
}

const gameover = (message) => {
    game_active = false;
    templates_message.innerHTML = message + ` You scored: ${score}. Game over! Click to play again`;

    if (score > 0) {
        $.ajax({
            url: '/',
            cache: 'false',
            dataType: 'json',
            type: 'POST',
            data:{
                    'score': score,
                    'drifters': drifters_destroyed,
                }
            ,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', $.cookie('csrftoken'))
            },
            success: function(data) {},
            error: function(error) {}
        });
    }
}

// Draw function
draw();
setInterval(draw, TIME_DELAY);

// Star decoration event
canvas.onmousemove = (event) => {
    if (!game_active){
        let x_pos = event.clientX - rect.left;
        let y_pos = event.clientY - rect.top;

        for (let i = 0; i < star_arr.length; i++) {
            let elem = star_arr[i];
            if (dist(x_pos, y_pos, elem.x, elem.y) <= 6 * CIRCLE_SIZE && !moving(i)) {
                star_move.push({
                    index: i,
                    dir: Math.random() * Math.PI * 2
                });
            }
        }
    }   
}

// Start the game
canvas.addEventListener('click', (event) => {
    if (!game_active) {
        setupGame();
        templates_message.innerHTML = "Hold and click to shoot. Destroy as many drifters as possible";
        templates_score.innerHTML = "0";
    }
});


// Play the game
canvas.addEventListener('mousedown', (event) => {
    if (game_active) {
        beam_charge = true;
        beam_amount = 0;
        templates_message.innerHTML = "Charging beam";
        medium_beam_message = true;
        high_beam_message = true;
    }
});

canvas.addEventListener('mouseup', (event) => {
    if (game_active) {
        beam_charge = false;
        beam_loc = {
            x: event.clientX - rect.left,
            y: event.clientY - rect.top
        }
    }
});