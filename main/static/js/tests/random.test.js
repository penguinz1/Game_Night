const make_randoms_test = () => {
    let maximum = 20;
    let randoms = make_randoms(maximum, 0, 5);

    for (let i = 0; i < randoms.length; i++) {
        if (randoms[i][0] < 0 || randoms[i][0] > maximum) {
            console.log("FAIL: make_randoms_test");
            success = false;
            return;
        }
    }
}

const make_random_test = () => {
    let randoms = [];
    let maximum = 20;

    for (let i = 0; i < 50; i++) {
        randoms.push(make_random(maximum, i));
    }

    for (let i = 0; i < randoms.length; i++) {
        if (randoms[i][0] < 0 || randoms[i][0] > maximum) {
            console.log("FAIL: make_random_test");
            success = false;
            return;
        }
    }
}

const make_groups_test = () => {
    let group_list = ["a", "b", "c", "d", "e", "f"];
    let splits = make_groups(group_list, 0, 3)[0];

    if (splits.length !== 3) {
        console.log("FAIL: make_groups_test");
        success = false;
        return;
    }

    for (let i = 0; i < splits.length; i++) {
        if (splits[i].length !== 2) {
            console.log("FAIL: make_groups test");
            success = false;
            return;
        }
    }
}

const run_random_test = () => {
    make_random_test();
    make_randoms_test();
    make_groups_test();
}