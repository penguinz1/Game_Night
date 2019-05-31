const canvas = document.getElementById("space-game"); // canvas space for the space game
const templates_score = document.getElementById("personal-score"); // displays current score
const templates_message = document.getElementById("space-text"); // dissplays current message
const templates_pb = document.getElementById("personal-best"); // displays personal best score
const templates_site_top = document.getElementById("site-best"); // displays site top score
const templates_site_drifters = document.getElementById("drifters-destroyed"); // displays total sitewide drifters destroyed
// the dimensions of the canvas
const canvas_rect = {
    left: 0,
    right: canvas.width,
    top: 0,
    bottom: canvas.height
};
const NUM_STAR = 400; // number of stars to generate
const DRIFTER_COLOR = '#D3D3D3'; // color of the drifters
const BEAM_COLORS = ['#FFFFFF', '#9B30FF', '#2a52be']; // colors of the beam: [low, medium, high]
const BASE_SHIP_COLOR = '#7CFC00'; // color of the ship
const SHIP_OUTLINE = '#FFA500'; // color of the ship outline
const SHIP_STROKE_SIZE = 2; // thickness of the ship outline
const rect = canvas.getBoundingClientRect(); // coordinates of the canvas bounds
const ctx = canvas.getContext("2d") // 'pencil' of the canvas used to draw objects
const SPEED = 2; // speed of the stars
const CIRCLE_SIZE = 2.5; // size of the stars
const startX = canvas.width / 2; // starting X position of the ship
const startY = canvas.height / 2; // starting Y position of the ship
const BASE_SHIP_SIZE = 5; // starting ship size
const DRIFTER_MAX_SIZE = 5; // max size of drifters
const POINTS = [1, 1, 2, 3, 5]; // points that drifters are worth: size = [1, 2, 3, 4, 5]
const TIME_DELAY = 25; // tick delay of animations
const DIFFICULTY_INTERVAL = 5000; // time before game difficulty increases
const BASE_DRIFTER_INTERVAL = 1000; // base time for drifter generation
const DIFFICULTY_STEP = 1.1; // difficulty step per each difficulty increase
const DRIFTER_SPEED = 4.5; // base speed of drifters
const SHIP_SPEED = 10; // base speed of the ship
const SIZE_MOMENTUM = 1.3; // base ship resistance to changes in velocity
const SIZE_MULT = 3; // display size augmentation of drifters
const SHIP_MULT = 5; // display size augmentation of ship
const MEDIUM_POWER = 500; // time to charge medium beam
const HIGH_POWER = 3000; // time to charge high beam
const BEAM_PERSIST = [50, 200, 500]; // time beam lasts after being fired: [low, medium, high]
const BEAM_DAMAGE = [1, 2, 7]; // amount of damage the beam inflicts: [low, medium, high]
var game_active = false; // flag indicating whether the game is in progress
var drifters; // array of drifters
var beams; // array of beams
var drifters_destroyed; // number of drifters destroyed
var score; // current score
var ship_momentum; // current ship momentum (see above)
var ship_size; // current ship size
var drifter_interval; // current interval of drifter generation
var difficulty_time; // stores time until next difficulty step
var drifter_time; // stores time until next drifter generated
var ship_x; // current X position of ship
var ship_y; // current Y position of ship
var beam_charge; // flag indicating whether beam is charging
var beam_amount; // current charge amount of beam
var medium_beam_message = false; // flag on whether to display medium beam ready message
var high_beam_message = false; // flag on whether to display high beam ready message
var beam_loc; // location of mouse when beam is fired
var ship_momentum_x; // momentum of ship in the X direction
var ship_momentum_y; // momentum of ship in the Y direction
var ship_color; // current color of the ship

// draws the canvas
const draw = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // clears canvas

    if (!game_active) {
        // draws stars
        draw_stars();
        move_stars();
    } else {
        // draws the game
        // check time counters
        if (difficulty_time >= DIFFICULTY_INTERVAL) {
            drifter_interval = Math.ceil(drifter_interval / DIFFICULTY_STEP);
            difficulty_time = 0;
            templates_message.innerHTML = "Difficulty increased";
        }
        if (drifter_time >= drifter_interval) {
            drifters.push(gen_drifter());
            drifter_time = 0;
        }

        // updating beam charge and fire
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

        // draws and updates the game
        draw_sprites();
        move_sprites();
        check_collisions();
        decay_beams();

        // updates time counters
        difficulty_time += TIME_DELAY;
        drifter_time += TIME_DELAY;
    }
}

// STAR DECORATION CODE

// generates a position of a star
const gen_star = () => {
    return {
        x: Math.floor(Math.random() * canvas.width),
        y: Math.floor(Math.random() * canvas.height)
    };
}

// generates NUM_STAR positions of stars
const gen_star_coords = () => {
    let arr = []
    for (let i = 0; i < NUM_STAR; i++) {
        let elem = gen_star();
        arr.push(elem);
    }
    return arr;
}

var star_arr = gen_star_coords(); // stores the star positons
var star_move = []; // stores stars that are moving

// finds if a star is moving
const moving = (index) => {
    for (let i = 0; i < star_move.length; i++) {
        if (star_move[i].index == index) {
            return true;
        }
    }
    return false;
}

// calculates distance between two points (x1, y1), (x2, y2)
const dist = (x1, y1, x2, y2) => {
    return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
}

// calculates whether a star is outside the canvas boundaries
const out_of_range = (star) => {
    return star.x < 0
        || star.y < 0
        || star.x > canvas.width
        || star.y > canvas.height;
}

// draws the stars
const draw_stars = () => {
    star_arr.forEach((elem) => {
        ctx.beginPath();
        ctx.arc(elem.x, elem.y, CIRCLE_SIZE, 0, Math.PI * 2, false);
        ctx.fillStyle = "white";
        ctx.fill();
        ctx.closePath();
    });
}

// moves the stars
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

// resets all game variables to set up the game
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

// generates a coordinates and a size for a drifter
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

// draws the drifters, ship, and beams on the canvas
const draw_sprites = () => {
    // draws drifters
    drifters.forEach((elem) => {
        if (elem.size > 0 && elem.size <= DRIFTER_MAX_SIZE) {
            ctx.beginPath();
            ctx.rect(elem.x, elem.y, elem.size * SIZE_MULT, elem.size * SIZE_MULT);
            ctx.fillStyle = DRIFTER_COLOR;
            ctx.fill();
            ctx.closePath();
        }
    });

    // draws beams
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

    // draws the ship
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

// moves the drifters and the ship
const move_sprites = () => {
    // moves each drifter
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
        // check if the drifter is outside the canvas
        if (!intersectRect(drifter_rect, canvas_rect) 
            || drifters[i].size <= 0 || drifters[i].size > DRIFTER_MAX_SIZE) {
            drifters.splice(i, 1);
        }
    }

    // move the ship
    ship_x += ship_momentum_x / ship_size;
    ship_y += ship_momentum_y / ship_size;
    ship_rect = {
        left: ship_x,
        right: ship_x + ship_size * SHIP_MULT,
        top: ship_y,
        bottom: ship_y + ship_size * SHIP_MULT
    }

    // check if ship is outside the canvas
    if (!intersectRect(ship_rect, canvas_rect)) {
        gameover("You drifted away!");
    }
}

// propels the ship in the opposite direction of the beam shot
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

// checks if a beam and a drifter intersect
const intersectBeam = (beam, drifter) => {
    // ~confusing geometry`
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

// checks game collisions
const check_collisions = () => {
    // checks if a ship and a drifter intersect
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

    // check if a beam and a drifter intersect
    // updates scores if drifters are destroyed
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

    // bonus points for combo'ing drifters
    let bonus = Math.pow(drifter_combo, 2) / 2 - drifter_combo / 2

    if (drifter_combo > 0) {
        // updates score display
        score += score_combo + bonus;
        templates_score.innerHTML = score;

        if (bonus > 0) {
            templates_message.innerHTML = `Scored ${score_combo} points: ${score_combo} points from destroying drifters + ${bonus} bonus points from a ${drifter_combo} combo!`;
        } else {
            templates_message.innerHTML = `Scored ${score_combo} points: ${score_combo} points from destroying drifters!`;
        }
    }
    drifters_destroyed += drifter_combo;

    // updates personal best score
    if (user && score > personal_best) {
        personal_best = score;
        templates_pb.innerHTML = personal_best;
    }

    // updates site best score
    if (score > site_best) {
        site_best = score;
        templates_site_top.innerHTML = site_best;
    }

    // updates number of drifters destroyed sitewide
    site_drifters += drifter_combo;
    templates_site_drifters.innerHTML = site_drifters;
}

// destroys beams that have persisted for long enough
const decay_beams = () => {
    for (let i = beams.length - 1; i >= 0; i--) {
        beams[i].life -= TIME_DELAY;
        if (beams[i].life <= 0) {
            beams.splice(i, 1);
        }
    }
}

// simple function to determine whether two rectangles intersect
const intersectRect = (r1, r2) => {
    return !(r2.left > r1.right || 
           r2.right < r1.left || 
           r2.top > r1.bottom ||
           r2.bottom < r1.top);
}

// helper function to determine whether a beam intersects a drifter
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

// gameover resolving function
const gameover = (message) => {
    game_active = false; // sets the game as inactive
    templates_message.innerHTML = message + ` You scored: ${score}. Game over! Click to play again`;

    // posts the score to the database
    if (score > 0) {
        $.ajax({
            url: base_url,
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